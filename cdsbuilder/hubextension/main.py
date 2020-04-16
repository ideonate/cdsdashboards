from tornado.web import authenticated

from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Group

from ..orm import Dashboard
from .base import DashboardBaseMixin
from ..util import DefaultObjDict, url_path_join


class DashboardBaseHandler(BaseHandler, DashboardBaseMixin):
    pass


class AllDashboardsHandler(DashboardBaseHandler):

    @authenticated
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


class DashboardEditHandler(DashboardBaseHandler):

    @authenticated
    async def get(self, dashboard_urlname=None):

        current_user = await self.get_current_user()

        dashboard = None
        dashboard_name = ''
        dashboard_description = ''

        if dashboard_urlname is not None:

            dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

            if dashboard is None:
                return self.send_error(404)

            if current_user.name != dashboard.user.name: # Only allowed to edit your own dashboard
                return self.send_error(403)

            dashboard_name = dashboard.name
            dashboard_description = dashboard.description

        # Get List of possible visitor users
        existing_group_users = None
        if dashboard is not None and dashboard.group:
            existing_group_users = dashboard.group.users
        all_visitors = self.get_visitor_tuples(current_user.id, existing_group_users)

        # Get User's spawners:

        spawners = self.get_source_spawners(current_user)

        spawner_name=None
        if dashboard is not None and dashboard.source_spawner is not None:
            spawner_name=dashboard.source_spawner.name

        errors = DefaultObjDict()

        html = self.render_template(
            "editdashboard.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            dashboard_name=dashboard_name,
            dashboard_description=dashboard_description,
            spawner_name=spawner_name,
            current_user=current_user,
            spawners=spawners,
            all_visitors=all_visitors,
            errors=errors
        )
        self.write(html)

    @authenticated
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

        errors = DefaultObjDict()

        if dashboard_name == '':
            errors.name = 'Please enter a name'
        elif not self.name_regex.match(dashboard_name):
            errors.name = 'Please use letters and digits (start with one of these), and then spaces or these characters _-!@$()*+?<>. Max 100 chars.'

        # Get Spawners
        
        spawner_name = self.get_argument('spawner_name', None)

        spawners = self.get_source_spawners(current_user)

        self.log.debug('Got spawner_name {}.'.format(spawner_name))

        spawner = None
        thisspawners = [spawner for spawner in spawners if spawner.name == spawner_name]

        if len(thisspawners) == 1:
            spawner = thisspawners[0]
        else:
            if spawner_name is None:
                errors.spawner = 'Please select a source spawner'
            else:
                errors.spawner = 'Spawner {} not found'.format(spawner_name)

            # Pick the existing one again
            if dashboard is not None and dashboard.source_spawner is not None:
                spawner_name=dashboard.source_spawner.name
  
        if len(errors) == 0:
            db = self.db

            try:

                if dashboard is None:

                    urlname = self.calc_urlname(dashboard_name)    

                    self.log.debug('Final urlname is '+urlname)  

                    dashboard = Dashboard(
                        name=dashboard_name, urlname=urlname, user=current_user.orm_user, 
                        description=dashboard_description, source_spawner=spawner.orm_spawner
                        )
                    self.log.debug('dashboard urlname '+dashboard.urlname+', main name '+dashboard.name)

                else:
                    dashboard.name = dashboard_name
                    dashboard.description = dashboard_description
                    dashboard.source_spawner = spawner.orm_spawner
                    
                if group is None:
                    # Group could exist - what if it does? TODO
                    group = Group(name=dashboard.groupname)
                    self.db.add(group)
                    dashboard.group = group

                db.add(dashboard)
                    
                db.commit()

                # Now cancel any existing build and force a rebuild
                # TODO delete existing final_spawner
                builders_store = self.settings['cds_builders']
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

            html = self.render_template(
                "editdashboard.html",
                base_url=self.settings['base_url'],
                dashboard=dashboard,
                dashboard_name=dashboard_name,
                dashboard_description=dashboard_description,
                spawner_name=spawner_name,
                spawners=spawners,
                errors=errors,
                current_user=current_user
            )
            return self.write(html)
        
        self.redirect("{}hub/dashboards/{}".format(self.settings['base_url'], dashboard.urlname))


class MainViewDashboardHandler(DashboardBaseHandler):
    
    @authenticated
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
    async def get(self, dashboard_urlname=''):

        current_user = await self.get_current_user()

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            pass # Redirect anyway, to let regular MainViewDashboardHandler handle the error

        elif dashboard.is_orm_user_allowed(current_user.orm_user):
            builders_store = self.settings['cds_builders']

            builder = builders_store[dashboard]

            if not builder.pending and builder._build_future and builder._build_future.done() and builder._build_future.exception():
                builder._build_future = None

        self.redirect(url_path_join(self.settings['base_url'], "hub", "dashboards", dashboard_urlname))


