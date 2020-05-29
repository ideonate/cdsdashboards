from tornado.log import app_log

from .builders import Builder, BuildException


class ProcessBuilder(Builder):
 
    async def start(self, dashboard, dashboard_user, db):
        """Start the dashboard

        Returns:
          (str, str): the (new_server_name, new_server_options) of the new dashboard server.

        """

        app_log.info('Starting LocalProcess Builder start function')

        self.event_queue = []

        self.add_progress_event({'progress': 10, 'message': 'Starting builder'})

        self._build_pending = True

        new_server_name = self.format_string(self.cdsconfig.server_name_template)

        if not self.allow_named_servers:
            raise BuildException(400, "Named servers are not enabled.")
        if (
            self.named_server_limit_per_user > 0
            and new_server_name not in dashboard_user.orm_spawners
        ):
            named_spawners = list(dashboard_user.all_spawners(include_default=False))
            if self.named_server_limit_per_user <= len(named_spawners):
                raise BuildException(
                    "User {} already has the maximum of {} named servers."
                    "  One must be deleted before a new server can be created".format(
                        dashboard_user.name, self.named_server_limit_per_user
                    ),
                )
        spawner = dashboard_user.spawners[new_server_name] # Could be orm_spawner or Spawner wrapper

        if spawner.ready:
            # include notify, so that a server that died is noticed immediately
            # set _spawn_pending flag to prevent races while we wait
            spawner._spawn_pending = True
            try:
                state = await spawner.poll_and_notify()
            finally:
                spawner._spawn_pending = False

        new_server_options = {
            'presentation_type': dashboard.presentation_type or 'voila',
            'presentation_path': dashboard.start_path,
            'cmd': ['python3', '-m', 'jhsingle_native_proxy.main'],
            'environment': {
                'JUPYTERHUB_ANYONE': '{}'.format(dashboard.allow_all and '1' or '0'),
                'JUPYTERHUB_GROUP': '{}'.format(dashboard.groupname)
                }
            }

        return (new_server_name, new_server_options)



