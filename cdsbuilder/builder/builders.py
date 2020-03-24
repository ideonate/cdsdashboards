from async_generator import yield_, async_generator

from traitlets.config import LoggingConfigurable
from tornado.ioloop import PeriodicCallback
from tornado.log import app_log
from traitlets import Any
from traitlets import Bool
from traitlets import Float
from traitlets import Integer
from traitlets import List

from jupyterhub.utils import exponential_backoff
from jupyterhub.utils import maybe_future


class Builder(LoggingConfigurable):
    """Base class for building a dashboard, e.g. by cloning an existing server which is a Docker container.

    Subclass this, and override the following methods:

    - load_state
    - get_state
    - start
    - stop
    - poll

    """

    dashboard_id = None

    # private attributes for tracking status
    _build_pending = False
    _start_pending = False
    _stop_pending = False
    _proxy_pending = False
    _check_pending = False
    _waiting_for_response = False
    _jupyterhub_version = None
    _build_future = None

    @property
    def _failed(self):
        """Did the last build fail?"""
        return (
            not self.active
            and self._build_future
            and self._build_future.done()
            and self._build_future.exception()
        )

    @property
    def pending(self):
        """Return the current pending event, if any

        Return False if nothing is pending.
        """
        if self._build_pending:
            return 'spawn'
        elif self._stop_pending:
            return 'stop'
        elif self._check_pending:
            return 'check'
        return None

    @property
    def ready(self):
        """Is this server ready to use?

        A server is not ready if an event is pending.
        """
        if self.pending:
            return False
        #if self.server is None:
        #    return False
        return True

    @property
    def active(self):
        """Return True if the server is active.

        This includes fully running and ready or any pending start/stop event.
        """
        return bool(self.pending or self.ready)

    # options passed by constructor
    orm_builder = Any()
    db = Any()

    #@observe('orm_builder')
    #def _orm_spawner_changed(self, change):
    #    if change.new and change.new.server:
    #        self._server = Server(orm_server=change.new.server)
    #    else:
    #        self._server = None

    user = Any()

    def __init_subclass__(cls, **kwargs):

        app_log.debug('init subclass of builder')

        super().__init_subclass__()

        missing = []
        for attr in ('start', 'stop', 'poll'):
            if getattr(Builder, attr) is getattr(cls, attr):
                missing.append(attr)

        if missing:
            raise NotImplementedError(
                "class `{}` needs to redefine the `start`,"
                "`stop` and `poll` methods. `{}` not redefined.".format(
                    cls.__name__, '`, `'.join(missing)
                )
            )

    @property
    def last_activity(self):
        return self.orm_builder.last_activity

    will_resume = Bool(
        False,
        help="""Whether the Builder will resume on next start


        Default is False where each launch of the Spawner will be a new instance.
        If True, an existing Spawner will resume instead of starting anew
        (e.g. resuming a Docker container),
        and API tokens in use when the Spawner stops will not be deleted.
        """,
    )

    consecutive_failure_limit = Integer(
        0,
        help="""
        Maximum number of consecutive failures to allow before
        shutting down JupyterHub.

        This helps JupyterHub recover from a certain class of problem preventing launch
        in contexts where the Hub is automatically restarted (e.g. systemd, docker, kubernetes).

        A limit of 0 means no limit and consecutive failures will not be tracked.
        """,
    ).tag(config=True)

    start_timeout = Integer(
        60,
        help="""
        Timeout (in seconds) before giving up on starting of single-user server.

        This is the timeout for start to return, not the timeout for the server to respond.
        Callers of spawner.start will assume that startup has failed if it takes longer than this.
        start should return when the server process is started and its location is known.
        """,
    ).tag(config=True)

    http_timeout = Integer(
        30,
        help="""
        Timeout (in seconds) before giving up on a spawned HTTP server

        Once a server has successfully been spawned, this is the amount of time
        we wait before assuming that the server is unable to accept
        connections.
        """,
    ).tag(config=True)

    poll_interval = Integer(
        30,
        help="""
        Interval (in seconds) on which to poll the spawner for single-user server's status.

        At every poll interval, each spawner's `.poll` method is called, which checks
        if the single-user server is still running. If it isn't running, then JupyterHub modifies
        its own state accordingly and removes appropriate routes from the configurable proxy.
        """,
    ).tag(config=True)

    _callbacks = List()
    _poll_callback = Any()

    debug = Bool(False, help="Enable debug-logging of the single-user server").tag(
        config=True
    )

    def load_state(self, state):
        """Restore state of spawner from database.

        Called for each user's spawner after the hub process restarts.

        `state` is a dict that'll contain the value returned by `get_state` of
        the spawner, or {} if the spawner hasn't persisted any state yet.

        Override in subclasses to restore any extra state that is needed to track
        the single-user server for that user. Subclasses should call super().
        """
        pass

    def get_state(self):
        """Save state of spawner into database.

        A black box of extra state for custom spawners. The returned value of this is
        passed to `load_state`.

        Subclasses should call `super().get_state()`, augment the state returned from
        there, and return that state.

        Returns
        -------
        state: dict
             a JSONable dict of state
        """
        state = {}
        return state

    def clear_state(self):
        """Clear any state that should be cleared when the single-user server stops.

        State that should be preserved across single-user server instances should not be cleared.

        Subclasses should call super, to ensure that state is properly cleared.
        """
        self.api_token = ''

    #@property
    #def _progress_url(self):
    #    return self.user.progress_url(self.name)

    @async_generator
    async def _generate_progress(self):
        """Private wrapper of progress generator

        This method is always an async generator and will always yield at least one event.
        """
        if not self._build_pending:
            self.log.warning(
                #"Build not pending, can't generate progress for %s", self._log_name
                "Build not pending, can't generate progress"
            )
            return

        await yield_({"progress": 0, "message": "Server requested"})
        from async_generator import aclosing

        async with aclosing(self.progress()) as progress:
            async for event in progress:
                await yield_(event)

    @async_generator
    async def progress(self):
        """Async generator for progress events

        Must be an async generator

        For Python 3.5-compatibility, use the async_generator package

        Should yield messages of the form:

        ::

          {
            "progress": 80, # integer, out of 100
            "message": text, # text message (will be escaped for HTML)
            "html_message": html_text, # optional html-formatted message (may have links)
          }

        In HTML contexts, html_message will be displayed instead of message if present.
        Progress will be updated if defined.
        To update messages without progress omit the progress field.

        .. versionadded:: 0.9
        """
        await yield_({"progress": 50, "message": "Spawning server..."})

    async def start(self):
        """Start the single-user server

        Returns:
          (str, int): the (ip, port) where the Hub can connect to the server.

        .. versionchanged:: 0.7
            Return ip, port instead of setting on self.user.server directly.
        """
        raise NotImplementedError(
            "Override in subclass. Must be a Tornado gen.coroutine."
        )

    async def stop(self, now=False):
        """Stop the single-user server

        If `now` is False (default), shutdown the server as gracefully as possible,
        e.g. starting with SIGINT, then SIGTERM, then SIGKILL.
        If `now` is True, terminate the server immediately.

        The coroutine should return when the single-user server process is no longer running.

        Must be a coroutine.
        """
        raise NotImplementedError(
            "Override in subclass. Must be a Tornado gen.coroutine."
        )

    async def poll(self):
        """Check if the single-user process is running

        Returns:
          None if single-user process is running.
          Integer exit status (0 if unknown), if it is not running.

        State transitions, behavior, and return response:

        - If the Spawner has not been initialized (neither loaded state, nor called start),
          it should behave as if it is not running (status=0).
        - If the Spawner has not finished starting,
          it should behave as if it is running (status=None).

        Design assumptions about when `poll` may be called:

        - On Hub launch: `poll` may be called before `start` when state is loaded on Hub launch.
          `poll` should return exit status 0 (unknown) if the Spawner has not been initialized via
          `load_state` or `start`.
        - If `.start()` is async: `poll` may be called during any yielded portions of the `start`
          process. `poll` should return None when `start` is yielded, indicating that the `start`
          process has not yet completed.

        """
        raise NotImplementedError(
            "Override in subclass. Must be a Tornado gen.coroutine."
        )

    def add_poll_callback(self, callback, *args, **kwargs):
        """Add a callback to fire when the single-user server stops"""
        if args or kwargs:
            cb = callback
            callback = lambda: cb(*args, **kwargs)
        self._callbacks.append(callback)

    def stop_polling(self):
        """Stop polling for single-user server's running state"""
        if self._poll_callback:
            self._poll_callback.stop()
            self._poll_callback = None

    def start_polling(self):
        """Start polling periodically for single-user server's running state.

        Callbacks registered via `add_poll_callback` will fire if/when the server stops.
        Explicit termination via the stop method will not trigger the callbacks.
        """
        if self.poll_interval <= 0:
            self.log.debug("Not polling subprocess")
            return
        else:
            self.log.debug("Polling subprocess every %is", self.poll_interval)

        self.stop_polling()

        self._poll_callback = PeriodicCallback(
            self.poll_and_notify, 1e3 * self.poll_interval
        )
        self._poll_callback.start()

    async def poll_and_notify(self):
        """Used as a callback to periodically poll the process and notify any watchers"""
        status = await self.poll()
        if status is None:
            # still running, nothing to do here
            return

        self.stop_polling()

        # clear callbacks list
        self._callbacks, callbacks = ([], self._callbacks)

        for callback in callbacks:
            try:
                await maybe_future(callback())
            except Exception:
                self.log.exception("Unhandled error in poll callback for %s", self)
        return status

    death_interval = Float(0.1)

    async def wait_for_death(self, timeout=10):
        """Wait for the single-user server to die, up to timeout seconds"""

        async def _wait_for_death():
            status = await self.poll()
            return status is not None

        try:
            r = await exponential_backoff(
                _wait_for_death,
                'Process did not die in {timeout} seconds'.format(timeout=timeout),
                start_wait=self.death_interval,
                timeout=timeout,
            )
            return r
        except TimeoutError:
            return False


class BuildersDict(dict):
    def __init__(self, builder_factory):
        self.builder_factory = builder_factory

    def __getitem__(self, key):
        if key not in self:
            self[key] = self.builder_factory(key)
        return super().__getitem__(key)


def builder_factory(key):
    app_log.debug("Builder factory for key {}".format(key))
    return Builder(dashboard_id=key)

builders_store = BuildersDict(builder_factory)
