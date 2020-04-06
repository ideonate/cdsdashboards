import re
from datetime import timedelta, datetime
from collections import defaultdict

from tornado.web import authenticated, HTTPError
from tornado import gen

from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Group, User
from sqlalchemy import and_, or_

from ..util import maybe_future
from ..orm import Dashboard
from ..util import DefaultObjDict


class DashboardBaseHandler(BaseHandler):

    unsafe_regex = re.compile(r'[^a-zA-Z0-9]+')

    name_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_\- \!\@\$\(\)\*\+\?\<\>]+$')
    
    def calc_urlname(self, dashboard_name):
        urlname = base_urlname = re.sub(self.unsafe_regex, '-', dashboard_name).lower()

        self.log.debug('calc safe name from '+urlname)

        now_unique = False
        counter = 1
        while not now_unique:
            orm_dashboard = Dashboard.find(db=self.db, urlname=urlname)
            self.log.info("{} - {}".format(urlname,orm_dashboard))
            if orm_dashboard is None or counter >= 100:
                now_unique = True
            else:
                urlname = "{}-{}".format(base_urlname, counter)
                counter += 1

        self.log.debug('calc safe name : '+urlname)
        return urlname

    def get_source_spawners(self, user):
        return [spawner for spawner in user.all_spawners(include_default=True) if not spawner.orm_spawner.dashboard_final_of]

    def get_visitor_dashboards(self, user):
        orm_dashboards = set()

        for group in user.groups:
            if group.dashboard_visitors_for:
                orm_dashboards.add(group.dashboard_visitors_for)

        orm_dashboards.update(self.db.query(Dashboard).filter(Dashboard.allow_all==True).filter(Dashboard.user != user.orm_user).all())

        user_dashboard_groups = defaultdict(list)

        for dash in orm_dashboards:
            user_dashboard_groups[dash.user.name].append(dash)

        return user_dashboard_groups

    def get_visitor_users(self, exclude_user_id):
        return self.db.query(User).filter(User.id != exclude_user_id).all()

    def get_visitor_tuples(self, exclude_user_id, existing_group_users=None):
        possible_visitor_users = self.get_visitor_users(exclude_user_id)

        visitor_users = []

        if existing_group_users is not None:
            visitor_users = existing_group_users

        return [(True, user) for user in visitor_users] + [(False, user) for user in set(possible_visitor_users) - set(visitor_users)]
        
    def sync_group(self, group, visitor_users):
        """
        Make sure all allowed JupyterHub users are part of this group
        Returns True if changes made, False otherwise
        """
        unwantedusers = set(group.users) - set(visitor_users)
        newusers = set(visitor_users) - set(group.users)

        if len(unwantedusers) + len(newusers) > 0:

            for user in unwantedusers:
                group.users.remove(user)

            for user in newusers:
                group.users.append(user)

            return True

        return False

    async def maybe_start_build(self, dashboard, dashboard_user, force_start=False):

        builders_store = self.settings['cds_builders']

        builder = builders_store[dashboard]

        #if builder._build_future and builder._build_future.done():
        #    builder._build_future = None

        status = ''

        def do_final_build(f):
            if f.cancelled() or f.exception() is None:
                builder._build_future = None
            builder._build_pending = False

        if not builder.active and (dashboard.final_spawner is None or force_start):
            
            if builder._build_future and builder._build_future.done() and builder._build_future.exception() and not force_start:
                status = 'Error: {}'.format(builder._build_future.exception())

            else:
                self.log.debug('starting builder')
                status = 'Started build'

                builder._build_pending = True

                async def do_build():

                    await self.maybe_delete_existing_server(dashboard.final_spawner, dashboard_user)

                    (new_server_name, new_server_options) =  await builder.start(dashboard, self.db)

                    await self.spawn_single_user(dashboard_user, new_server_name, options=new_server_options)

                    self.db.expire(dashboard) # May have changed during async code above

                    if new_server_name in dashboard_user.orm_user.orm_spawners:
                        dashboard.final_spawner = dashboard_user.orm_user.orm_spawners[new_server_name]

                    # TODO if not, then what?

                    dashboard.started = datetime.utcnow()

                    self.db.commit()

                builder._build_future = maybe_future(do_build())

                builder._build_future.add_done_callback(do_final_build)

        elif builder.pending:
            status = 'Pending build'

        elif dashboard.final_spawner:
            user = self._user_from_orm(dashboard_user)

            final_spawner = user.spawners[dashboard.final_spawner.name]

            if final_spawner.ready:
                status = 'Spawner already active'
            elif final_spawner.pending:
                status = 'Spawner is pending...'
            else:
                status = 'Final spawner is dormant - starting up...'

                f = maybe_future(self.spawn_single_user(dashboard_user, final_spawner.name))

                f.add_done_callback(do_final_build)

        return status

    async def maybe_delete_existing_server(self, orm_spawner, dashboard_user):
        if not orm_spawner:
            return
        
        server_name = orm_spawner.name

        user = self._user_from_orm(dashboard_user)

        spawner = user.spawners[server_name]

        if server_name:
            if not self.allow_named_servers:
                raise HTTPError(400, "Named servers are not enabled.")
            if server_name not in user.orm_spawners:
                self.log.debug("%s does not exist anyway", spawner._log_name)
                return
        else:
            raise HTTPError(400, "Cannot delete the default server")

        if spawner.pending == 'stop':
            self.log.debug("%s already stopping", spawner._log_name)

            await spawner._stop_future

        if spawner.ready or spawner.pending == 'spawn':

            if spawner.pending == 'spawn':
                self.log.debug("%s awaiting spawn to finish so can shut it down", spawner._log_name)
                await spawner._spawn_future

            # include notify, so that a server that died is noticed immediately
            status = await spawner.poll_and_notify()
            if status is None:
                stop_future = await self.stop_single_user(user, server_name)
                await stop_future

        self.log.info("Deleting spawner %s", spawner._log_name)
        self.db.delete(spawner.orm_spawner)
        user.spawners.pop(server_name, None)
        self.db.commit()


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



class DashboardNewHandler(DashboardBaseHandler):

    @authenticated
    async def get(self):

        self.log.debug('calling DashboardNewHandler')

        current_user = await self.get_current_user()

        errors = DefaultObjDict()

        html = self.render_template(
            "newdashboard.html",
            base_url=self.settings['base_url'],
            current_user=current_user,
            dashboard_name='',
            errors=errors
        )
        self.write(html)

    @authenticated
    async def post(self):

        current_user = await self.get_current_user()

        dashboard_name = self.get_argument('name').strip()

        errors = DefaultObjDict()

        if dashboard_name == '':
            errors.name = 'Please enter a name'
        elif not self.name_regex.match(dashboard_name):
            errors.name = 'Please use letters and digits (start with one of these), and then spaces or these characters _-!@$()*+?<>'
        else:
            urlname = self.calc_urlname(dashboard_name)    

            self.log.debug('Final urlname is '+urlname)  

            db = self.db

            try:

                d = Dashboard(name=dashboard_name, urlname=urlname, user=current_user.orm_user)
                self.log.debug('dashboard urlname '+d.urlname+', main name '+d.name)
                db.add(d)
                db.commit()

            except Exception as e:
                errors.all = str(e)

        if len(errors):
            html = self.render_template(
                "newdashboard.html",
                base_url=self.settings['base_url'],
                dashboard_name=dashboard_name,
                errors=errors,
                current_user=current_user
            )
            return self.write(html)
        
        # redirect to edit dashboard page

        self.redirect("{}hub/dashboards/{}/{}/edit".format(self.settings['base_url'], current_user.name, urlname))


class DashboardEditHandler(DashboardBaseHandler):

    @authenticated
    async def get(self, user_name, dashboard_urlname=''):

        current_user = await self.get_current_user()

        if current_user.name != user_name:
            return self.send_error(403)

        dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

        if dashboard is None:
            return self.send_error(404)

        # Get List of possible visitor users
        existing_group_users = None
        if dashboard.group:
            existing_group_users = dashboard.group.users
        all_visitors = self.get_visitor_tuples(dashboard.user.id, existing_group_users)

        # Get User's spawners:

        spawners = self.get_source_spawners(current_user)

        spawner_name=None
        if dashboard.source_spawner is not None:
            spawner_name=dashboard.source_spawner.name

        errors = DefaultObjDict()

        html = self.render_template(
            "editdashboard.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            dashboard_name=dashboard.name,
            dashboard_description=dashboard.description,
            spawner_name=spawner_name,
            current_user=current_user,
            spawners=spawners,
            all_visitors=all_visitors,
            errors=errors
        )
        self.write(html)

    @authenticated
    async def post(self, user_name, dashboard_urlname=''):

        current_user = await self.get_current_user()

        if current_user.name != user_name:
            return self.send_error(403)

        dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

        if dashboard is None:
            return self.send_error(404)

        dashboard_name = self.get_argument('name').strip()

        dashboard_description = self.get_argument('description').strip()

        errors = DefaultObjDict()

        if dashboard_name == '':
            errors.name = 'Please enter a name'
        elif not self.name_regex.match(dashboard_name):
            errors.name = 'Please use letters and digits (start with one of these), and then spaces or these characters _-!@$()*+?<>'

        # Get or create group

        group = dashboard.group

        all_visitors = self.get_arguments('all_visitors[]')

        #.filter(User.name != dashboard.user.name)
        all_visitors_users = self.db.query(User).filter(User.name.in_(all_visitors)).all()

        # Get Spawners
        
        spawner_name = self.get_argument('spawner_name', None)

        spawners = self.get_source_spawners(current_user)

        self.log.debug('Got spawner_name {}.'.format(spawner_name))

        spawner = None
        thisspawners = [spawner for spawner in spawners if spawner.name == spawner_name]

        if len(thisspawners) == 1:
            spawner = thisspawners[0]
        else:
            errors.spawner = 'Spawner {} not found'.format(spawner_name)

            # Pick the existing one again
            if dashboard.source_spawner is not None:
                spawner_name=dashboard.source_spawner.name

        # In case we have to display an error, we also need all these users
        all_visitors = self.get_visitor_tuples(dashboard.user.id, all_visitors_users)
        
        if len(errors) == 0:
            db = self.db

            try:

                dashboard.name = dashboard_name
                dashboard.description = dashboard_description
                dashboard.source_spawner = spawner.orm_spawner
                

                if group is None:
                    # Group could exist - what if it does? TODO
                    group = Group(name=dashboard.groupname, users=all_visitors_users)
                    self.db.add(group)
                    dashboard.group = group

                db.add(dashboard)

                if self.sync_group(group, all_visitors_users):
                    self.db.add(group)
                    
                db.commit()

                # Now cancel any existing build and force a rebuild
                # TODO delete existing final_spawner
                builders_store = self.settings['cds_builders']
                builder = builders_store[dashboard]

                status = ''

                async def do_restart_build(f):
                    status = await self.maybe_start_build(dashboard, current_user, True)
                    self.log.debug('Force build start: {}'.format(status))
                    return status

                if builder.pending and builder._build_future and not builder._build_future.done():

                    self.log.debug('Cancelling build')
                    builder._build_future.add_done_callback(do_restart_build)
                    builder._build_future.cancel()

                else:
                    status = await do_restart_build(None)


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
                all_visitors=all_visitors,
                errors=errors,
                current_user=current_user
            )
            return self.write(html)
        
        # redirect to main dashboard page

        #self.redirect("{}hub/dashboards/{}/{}/edit".format(self.settings['base_url'], current_user.name, dashboard.urlname))
        self.redirect("{}hub/dashboards".format(self.settings['base_url']))


class MainViewDashboardHandler(DashboardBaseHandler):
    
    @authenticated
    async def get(self, user_name, dashboard_urlname=''):

        current_user = await self.get_current_user()

        dashboard_user = self.user_from_username(user_name)

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None or dashboard_user is None:
            return self.send_error(404)

        if dashboard.user.name != dashboard_user.name:
            raise Exception('Dashboard user {} does not match {}'.format(dashboard.user.name, dashboard_user.name))

        # Get User's builders:

        status = await self.maybe_start_build(dashboard, dashboard_user)

        html = self.render_template(
            "viewdashboard.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            current_user=current_user,
            dashboard_user=dashboard_user,
            status=status
        )
        self.write(html)

