from tornado import gen

from .builders import Builder


class DockerBuilder(Builder):

    async def start(self):
        """Start the dashboard

        Returns:
          (str, int): the (ip, port) where the Hub can connect to the server.

        """

        for i in range(20):
            await gen.sleep(2)
            self.log.debug('Still starting dashboard {} ({})'.format(self.dashboard_id, i))


        return ('localhost', 80152)

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