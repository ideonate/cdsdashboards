from asyncio import sleep
from datetime import datetime

from traitlets.config import LoggingConfigurable
from traitlets import Any, Bool, Integer
from tornado.log import app_log


class Builder(LoggingConfigurable):
    """Base class for building a dashboard, e.g. by cloning an existing server which is a Docker container.

    Subclass this, and override the following methods:

    - start

    """

    dashboard = None

    cdsconfig = None

    # private attributes for tracking status
    _build_pending = False
    _build_future = None

    event_queue = []

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
    def _log_name(self):
        """Return username:dashboard_urlname
        """
        if self.dashboard:
            return '%s:%s' % (self.dashboard.user.name, self.dashboard.urlname)
        else:
            return 'Dashboard Builder {}'.format(self)

    @property
    def pending(self):
        """Return the current pending event, if any

        Return False if nothing is pending.
        """
        if self._build_pending:
            return 'build'

        return None

    @property
    def ready(self):
        """Is this builder finished, up to assigning a spawner (which may still be starting up)

        A builder is not ready if an event is pending.
        """
        if self.pending:
            return False
        if self.dashboard is None:
            return False
        if self.dashboard.final_spawner is None:
            return False
        if self._build_future and self._build_future.done() and self._build_future.exception():
            return False
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

    log = Any(default_value=app_log).tag(config=True)

    user = Any()

    def __init_subclass__(cls, **kwargs):

        app_log.debug('init subclass of builder')

        super().__init_subclass__()

        missing = []
        for attr in ('start',):
            if getattr(Builder, attr) is getattr(cls, attr):
                missing.append(attr)

        if missing:
            raise NotImplementedError(
                "class `{}` needs to redefine the `start` method(s). `{}` not redefined.".format(
                    cls.__name__, '`, `'.join(missing)
                )
            )

    def __init__(self, dashboard, cdsconfig, config=None):
        super().__init__(config=config)

        self.dashboard = dashboard
        self.cdsconfig = cdsconfig

    @property
    def last_activity(self):
        return self.orm_builder.last_activity

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

    debug = Bool(False, help="Enable debug-logging of the single-user server").tag(
        config=True
    )

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

        yield {"progress": 0, "message": "Builder requested"}
        from async_generator import aclosing

        async with aclosing(self.progress()) as progress:
            async for event in progress:
                yield event

    async def progress(self):
        """Async generator for progress events

        Must be an async generator

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

        """
        next_event = 0

        break_while_loop = False
        while True:
            # Ensure we always capture events following the start_future
            # signal has fired.
            if self._build_future.done():
                break_while_loop = True
            event_queue = self.event_queue

            len_events = len(event_queue)
            if next_event < len_events:

                for i in range(next_event, len_events):
                    event = event_queue[i]

                    yield event 
                
                next_event = len_events

            if break_while_loop:
                break

            await sleep(1)

    def add_progress_event(self, event):
        self.event_queue.append(event)

    async def start(self, dashboard, dashboard_user, db):
        """Start the dashboard

        Returns:
          (str, str): the (new_server_name, new_server_options) of the new dashboard server.

        """
        raise NotImplementedError(
            "You must specify a c.CDSDashboardsConfig.builder_class in your JupyterHub jupyterhub_config.py file."
        )

    allow_named_servers = True # TODO take from main app config

    def template_namespace(self):
        """Return the template namespace for format-string formatting.

        Subclasses may add items to the available namespace.

        The default implementation includes::

            {
              'urlname': dashboard.urlname,
              'date': <current date in YYmmdd format>,
              'time': <current date in HHMMSS format>,
            }

        Returns:

            ns (dict): namespace for string formatting.
        """
        date = datetime.today().strftime('%Y%m%d')
        time = datetime.today().strftime('%H%M%S')
        d = {
            'urlname': self.dashboard.urlname,
            'date': date,
            'time': time
            }
        return d

    def format_string(self, s, ns=None):
        """Render a Python format string

        Uses :meth:`Builder.template_namespace` to populate format namespace, based on self.dashboard.

        Optionally provide the namespace as ns.

        Args:

            s (str): Python format-string to be formatted.

        Returns:

            str: Formatted string, rendered
        """
        if ns is None:
            ns = self.template_namespace()
        return s.format(**ns)


class BuildersDict(dict):
    def __init__(self, builder_factory):
        self.builder_factory = builder_factory

    def __getitem__(self, orm_dashboard):
        if orm_dashboard not in self:
            self[orm_dashboard] = self.builder_factory(orm_dashboard)
        return super().__getitem__(orm_dashboard)


class BuildException(Exception):
    pass
