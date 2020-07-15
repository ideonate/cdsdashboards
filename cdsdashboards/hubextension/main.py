import sys, re

from tornado.web import authenticated

from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Group

from ..orm import Dashboard
from .base import DashboardBaseMixin, check_database_upgrade, spawner_to_dict
from ..util import DefaultObjDict, url_path_join
from .. import hookimpl
from ..pluggymanager import pm
from ..app import BuildersStore, CDSConfigStore


class DashboardBaseHandler(BaseHandler, DashboardBaseMixin):
    pass


class AllDashboardsHandler(DashboardBaseHandler):

    @authenticated
    @check_database_upgrade
    async def get(self):

        current_user = await self.get_current_user()

        my_dashboards = current_user.dashboards_own

        visitor_dashboard_groups = self.get_visitor_dashboards(current_user)

        html = self.render_template(
            "alldashboards.html",
            base_url=self.settings['base_url'],
            my_dashboards=my_dashboards,
            visitor_dashboard_groups=visitor_dashboard_groups,
            current_user=current_user
        )
        self.write(html)


class BasicDashboardEditHandler(DashboardBaseHandler):

    @authenticated
    @check_database_upgrade
    async def get(self, dashboard_urlname=None):

        current_user = await self.get_current_user()

        dashboard = None
        dashboard_name = ''
        dashboard_description = ''
        dashboard_presentation_type = ''
        dashboard_start_path = ''
        dashboard_options = {}

        if dashboard_urlname is not None:

            dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

            if dashboard is None:
                return self.send_error(404)

            if current_user.name != dashboard.user.name: # Only allowed to edit your own dashboard
                return self.send_error(403)

            dashboard_name = dashboard.name
            dashboard_description = dashboard.description
            dashboard_start_path = dashboard.start_path or ''
            dashboard_presentation_type = dashboard.presentation_type
            dashboard_options = dashboard.options

        cdsconfig = CDSConfigStore.get_instance(self.settings['config'])

        # Get List of possible visitor users
        existing_group_users = None
        if dashboard is not None and dashboard.group:
            existing_group_users = dashboard.group.users
        all_visitors = self.get_visitor_tuples(current_user.id, existing_group_users)

        # Get User's spawners:

        spawners = []
        spawner_id = ''
        source_type = dashboard_options.get('source_type', 'jupytertree')
        git_repo = ''

        if cdsconfig.show_source_servers:

            spawners = self.get_source_spawners(current_user)
            spawner_id = 'default'

            if dashboard is not None and dashboard.source_spawner is not None:
                spawner_id = spawner_to_dict(dashboard.source_spawner).id

        if cdsconfig.show_source_git:
            git_repo = dashboard_options.get('git_repo', '')
        else:
            source_type = 'jupytertree'

        errors = DefaultObjDict()
        
        merged_presentation_types = cdsconfig.merged_presentation_types

        html = self.render_template(
            "editdashboard.html",
            **self.template_vars(dict(
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            dashboard_name=dashboard_name,
            dashboard_description=dashboard_description,
            dashboard_start_path=dashboard_start_path,
            dashboard_presentation_type=dashboard_presentation_type,
            dashboard_options=dashboard_options,
            source_type=source_type,
            git_repo=git_repo,
            presentation_types=merged_presentation_types,
            spawner_id=spawner_id,
            current_user=current_user,
            spawners=spawners,
            show_source_servers=cdsconfig.show_source_servers,
            show_source_git=cdsconfig.show_source_git,
            require_source_server=cdsconfig.require_source_server,
            all_visitors=all_visitors,
            errors=errors)
            )
        )
        self.write(html)

    def template_vars(self, d):
        return d

    @authenticated
    @check_database_upgrade
    async def post(self, dashboard_urlname=None):

        current_user = await self.get_current_user()

        dashboard = None
        group = None

        if dashboard_urlname is not None:
            # Edit (not new)

            dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

            if dashboard is None:
                return self.send_error(404)

            if current_user.name != dashboard.user.name:
                return self.send_error(403)

            group = dashboard.group

        dashboard_name = self.get_argument('name').strip()

        dashboard_description = self.get_argument('description').strip()

        dashboard_presentation_type = self.get_argument('presentation_type').strip()

        dashboard_start_path = self.get_argument('start_path').strip()

        errors = DefaultObjDict()

        if dashboard_name == '':
            errors.name = 'Please enter a name'
        elif not self.name_regex.match(dashboard_name):
            errors.name = 'Please use letters and digits (start with one of these), and then spaces or these characters _-!@$()*+?<>. Max 100 chars.'

        if '..' in dashboard_start_path:
            errors.start_path = 'Path must not contain ..'
        elif not self.start_path_regex.match(dashboard_start_path):
            errors.start_path = 'Please enter valid URL path characters'

        merged_presentation_types = CDSConfigStore.get_instance(self.settings['config']).merged_presentation_types
        
        if not dashboard_presentation_type in merged_presentation_types:
            errors.presentation_type = 'Framework {} invalid - it must be one of the allowed types: {}'.format(
                dashboard_presentation_type, ', '.join(merged_presentation_types)
                )

        cdsconfig = CDSConfigStore.get_instance(self.settings['config'])

        dashboard_options = {}

        git_repo = ''
        source_type = self.get_argument('source_type', '').strip()

        if cdsconfig.show_source_git and source_type == 'gitrepo':
            git_repo = self.get_argument('git_repo', '').strip()

            # TODO check git repo is valid
            # if not then errors.git_repo = 'Please enter a valid git repo'
            if git_repo != '':
                if not re.match('^((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(/)?$', git_repo):
                    errors.git_repo = 'Please enter a valid git repo URL'
        else:
            source_type = 'jupytertree'

        dashboard_options['source_type'] = source_type
        dashboard_options['git_repo'] = git_repo

        spawners = []
        spawner = None
        spawner_id = ''

        if cdsconfig.show_source_servers:
            spawners = self.get_source_spawners(current_user)
            spawner, spawner_id = self.read_spawner(dashboard, spawners, dashboard_options, errors, cdsconfig.require_source_server)
 
        if len(errors) == 0:
            db = self.db

            try:

                orm_spawner = None
                if spawner:
                    orm_spawner = spawner.orm_spawner

                if dashboard is None:

                    urlname = self.calc_urlname(dashboard_name)    

                    self.log.debug('Final urlname is '+urlname)  

                    dashboard = Dashboard(
                        name=dashboard_name, urlname=urlname, user=current_user.orm_user, 
                        description=dashboard_description, start_path=dashboard_start_path, 
                        presentation_type=dashboard_presentation_type,
                        source_spawner=orm_spawner,
                        options=dashboard_options,
                        allow_all=cdsconfig.default_allow_all
                        )
                    self.log.debug('dashboard urlname '+dashboard.urlname+', main name '+dashboard.name)

                else:
                    dashboard.name = dashboard_name
                    dashboard.description = dashboard_description
                    dashboard.start_path = dashboard_start_path
                    dashboard.presentation_type = dashboard_presentation_type
                    dashboard.source_spawner = orm_spawner
                    dashboard.options = dashboard_options
                    
                if group is None:
                    group = Group.find(db, dashboard.groupname)
                    if group is None:
                        group = Group(name=dashboard.groupname)
                        self.db.add(group)
                    dashboard.group = group

                db.add(dashboard)
                    
                db.commit()

                # Now cancel any existing build and force a rebuild
                # TODO delete existing final_spawner
                builders_store = BuildersStore.get_instance(self.settings['config'])
                builder = builders_store[dashboard]

                async def do_restart_build(_):
                    await self.maybe_start_build(dashboard, current_user, True)
                    self.log.debug('Force build start')

                if builder.pending and builder._build_future and not builder._build_future.done():

                    self.log.debug('Cancelling build')
                    builder._build_future.add_done_callback(do_restart_build)
                    builder._build_future.cancel()

                else:
                    await do_restart_build(None)


            except Exception as e:
                errors.all = str(e)

        if len(errors):

            git_repo = dashboard_options['git_repo'] = dashboard_options.get('git_repo', '')

            html = self.render_template(
                "editdashboard.html",
                **self.template_vars(dict(
                base_url=self.settings['base_url'],
                dashboard=dashboard,
                dashboard_name=dashboard_name,
                dashboard_description=dashboard_description,
                dashboard_start_path=dashboard_start_path,
                dashboard_presentation_type=dashboard_presentation_type,
                dashboard_options=dashboard_options,
                git_repo=git_repo,
                source_type=source_type,
                presentation_types=merged_presentation_types,
                spawner_id=spawner_id,
                spawners=spawners,
                show_source_servers=cdsconfig.show_source_servers,
                show_source_git=cdsconfig.show_source_git,
                require_source_server=cdsconfig.require_source_server,
                errors=errors,
                current_user=current_user))
            )
            return self.write(html)
        
        self.redirect("{}hub/dashboards/{}".format(self.settings['base_url'], dashboard.urlname))

    def read_spawner(self, dashboard, spawners, dashboard_options, errors, require_source_server):

        # Get Spawners
        
        spawner_id = self.get_argument('spawner_id', '')

        self.log.debug('Got spawner_id {}.'.format(spawner_id))

        spawner = None
        thisspawners = [spawner for spawner in spawners if spawner.id == spawner_id]

        if len(thisspawners) == 1:
            spawner = thisspawners[0]
        else:
            if spawner_id == '':
                if require_source_server:
                    errors.spawner = 'Please select a source spawner'
                else:
                    return spawner, spawner_id
            else:
                errors.spawner = 'Spawner {} not found'.format(spawner_id)

            # Pick the existing one again
            if dashboard is not None and dashboard.source_spawner is not None:
                spawner_id = spawner_to_dict(dashboard.source_spawner).id
            else:
                spawner_id = ''

        return spawner, spawner_id


class MainViewDashboardHandler(DashboardBaseHandler):
    
    @authenticated
    @check_database_upgrade
    async def get(self, dashboard_urlname=''):

        current_user = await self.get_current_user()

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            return self.send_error(404)

        if not dashboard.is_orm_user_allowed(current_user.orm_user):
            return self.send_error(403)

        dashboard_user = self._user_from_orm(dashboard.user.name)

        need_follow_progress = await self.maybe_start_build(dashboard, dashboard_user)

        base_url = self.settings['base_url']

        html = self.render_template(
            "viewdashboard.html",
            base_url=base_url,
            dashboard=dashboard,
            current_user=current_user,
            dashboard_user=dashboard_user,
            need_follow_progress=need_follow_progress,
            progress_url=url_path_join(base_url, 'hub', 'dashboards-api', dashboard_urlname, 'progress')
        )
        self.write(html)


class ClearErrorDashboardHandler(DashboardBaseHandler):
    
    @authenticated
    @check_database_upgrade
    async def get(self, dashboard_urlname=''):

        current_user = await self.get_current_user()

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            pass # Redirect anyway, to let regular MainViewDashboardHandler handle the error

        elif dashboard.is_orm_user_allowed(current_user.orm_user):
            builders_store = BuildersStore.get_instance(self.settings['config'])

            builder = builders_store[dashboard]

            if not builder.pending and builder._build_future and builder._build_future.done() and builder._build_future.exception():
                builder._build_future = None

        self.redirect(url_path_join(self.settings['base_url'], "hub", "dashboards", dashboard_urlname))


class UpgradeDashboardsHandler(DashboardBaseHandler):

    @authenticated
    async def get(self):

        from ..dbutil import is_upgrade_needed

        engine = self.db.get_bind()
        if not is_upgrade_needed(engine):
            return self.redirect("{}".format(self.settings['base_url']))

        current_user = await self.get_current_user()

        is_sqlite = str(engine.url).startswith('sqlite:///')

        html = self.render_template(
            "upgrade-db.html",
            is_admin=current_user.admin,
            base_url=self.settings['base_url'],
            error='',
            is_sqlite=is_sqlite,
            success=False
        )
        self.write(html)

    @authenticated
    async def post(self):

        current_user = await self.get_current_user()

        if not current_user.admin:
            return self.send_error(403)

        error = ''
        success = True

        from ..dbutil import upgrade_if_needed

        engine = self.db.get_bind()

        is_sqlite = str(engine.url).startswith('sqlite:///')

        try:
            upgrade_if_needed(engine, log=self.log)
        except Exception as e:
            success = False
            error = str(e)

        html = self.render_template(
            "upgrade-db.html",
            is_admin=current_user.admin,
            error=error,
            success=success,
            is_sqlite=is_sqlite,
            base_url=self.settings['base_url']
        )
        self.write(html)


# Register plugin hooks so we use the Basic handlers by default, unless overridden

@hookimpl
def get_hubextension_main_DashboardEditHandler():
    return BasicDashboardEditHandler

pm.register(sys.modules[__name__])

DashboardEditHandler = pm.hook.get_hubextension_main_DashboardEditHandler()[0]
