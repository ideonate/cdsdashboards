from tornado.log import app_log

from .builders import Builder, BuildException


class ProcessBuilder(Builder):
 
    async def start(self, dashboard, dashboard_user, db):
        """Start the dashboard

        Returns:
          (str, str): the (new_server_name, new_server_options) of the new dashboard server.

        """

        app_log.info('Starting Builder start function')

        self.event_queue = []

        self.add_progress_event({'progress': 10, 'message': 'Starting builder'})

        self._build_pending = True

        ns = self.template_namespace()

        new_server_name = self.format_string(self.cdsconfig.server_name_template, ns=ns)

        new_server_options = await self.prespawn_server_options(dashboard, dashboard_user, ns)

        if not self.allow_named_servers:
            raise BuildException(400, "Named servers are not enabled.")

        spawner = dashboard_user.spawners[new_server_name] # Could be orm_spawner or Spawner wrapper

        if spawner.ready:
            # include notify, so that a server that died is noticed immediately
            # set _spawn_pending flag to prevent races while we wait
            spawner._spawn_pending = True
            try:
                state = await spawner.poll_and_notify()
            finally:
                spawner._spawn_pending = False

        git_repo = dashboard.options.get('git_repo', '')
        conda_env = dashboard.options.get('conda_env', '')

        new_server_options.update({
            'presentation_type': dashboard.presentation_type or 'voila',
            'presentation_path': dashboard.start_path,
            'git_repo': git_repo,
            'conda_env': conda_env})
        
        if 'environment' not in new_server_options:
            new_server_options['environment'] = {}

        new_server_options['environment'].update({
                'JUPYTERHUB_ANYONE': '{}'.format(dashboard.allow_all and '1' or '0'),
                'JUPYTERHUB_GROUP': '{}'.format(dashboard.groupname)
                })

        return (new_server_name, new_server_options)

    async def prespawn_server_options(self, dashboard, dashboard_user, ns):
        return {} # Empty options - override in subclasses if needed

