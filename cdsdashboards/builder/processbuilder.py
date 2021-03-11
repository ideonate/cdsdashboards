from tornado.log import app_log

from .builders import Builder, BuildException
from ..util import maybe_future, url_path_join

class ProcessBuilder(Builder):
 
    async def start(self, dashboard, dashboard_user, form_options=None, spawn_default_options=True):
        """Start the dashboard

        Returns:
          (str, str, None): the (new_server_name, new_server_options, None) of the new dashboard server.
          or
          (None, None, str): (None, None, user_options_form) if a user options form needs to be presented to the user.

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

        # Does this spawner need user options?
        if not spawn_default_options:

            if not form_options:
                
                spawner_options_form = await spawner.get_options_form()
                if spawner_options_form:
                    app_log.info('Options form is present')
                    return (None, None, spawner_options_form) # Tell caller that we need to go to the options form

            else:

                try:
                    user_options = await maybe_future(spawner.options_from_form(form_options))
                    new_server_options.update(user_options)
                except Exception as e:
                    app_log.error(
                        "Failed to spawn dashboard server with form", exc_info=True
                    )
                    spawner_options_form = await spawner.get_options_form()
                    if spawner_options_form:
                        app_log.info('Options form is present after failure')
                        return (None, None, spawner_options_form)
                        
        # Dashboard-specific options
        git_repo = dashboard.options.get('git_repo', '')
        git_repo_branch = dashboard.options.get('git_repo_branch', '')
        conda_env = dashboard.options.get('conda_env', '')

        new_server_options.update({
            'presentation_type': dashboard.presentation_type or 'voila',
            'presentation_path': dashboard.start_path,
            'git_repo': git_repo,
            'git_repo_branch': git_repo_branch,
            'conda_env': conda_env})
        
        if 'environment' not in new_server_options:
            new_server_options['environment'] = {}

        new_server_options['environment'].update({
                'JUPYTERHUB_ANYONE': '{}'.format(dashboard.allow_all and '1' or '0'),
                'JUPYTERHUB_GROUP': '{}'.format(dashboard.groupname)
                })

        return (new_server_name, new_server_options, None)

    async def prespawn_server_options(self, dashboard, dashboard_user, ns):
        return {} # Empty options - override in subclasses if needed

