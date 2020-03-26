import re
from datetime import timedelta

from tornado.web import authenticated
from tornado import gen

from jupyterhub.handlers.base import BaseHandler

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
            orm_dashboard = Dashboard.find(db=self.db, urlname=urlname) #self.db.query(Dashboard).filter(urlname==urlname).one_or_none()
            self.log.info("{} - {}".format(urlname,orm_dashboard))
            if orm_dashboard is None or counter >= 100:
                now_unique = True
            else:
                urlname = "{}-{}".format(base_urlname, counter)
                counter += 1

        self.log.debug('calc safe name : '+urlname)
        return urlname

    def get_users_dashboards(self, user):
        orm_dashboards = self.db.query(Dashboard).filter(user==user)
        return orm_dashboards
        

class AllDashboardsHandler(DashboardBaseHandler):

    @authenticated
    async def get(self):

        current_user = await self.get_current_user()

        dashboards = self.get_users_dashboards(current_user)

        html = self.render_template(
            "alldashboards.html",
            base_url=self.settings['base_url'],
            dashboards=dashboards,
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

                d = Dashboard(name=dashboard_name, urlname=urlname, user_id=current_user.id)
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

        # Get User's spawners:

        spawners = current_user.all_spawners(include_default=True)

        spawner_name=None
        if dashboard.source_spawner is not None:
            spawner_name=dashboard.source_spawner.name

        errors = DefaultObjDict()

        html = self.render_template(
            "editdashboard.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            dashboard_name=dashboard.name,
            spawner_name=spawner_name,
            current_user=current_user,
            spawners=spawners,
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

        errors = DefaultObjDict()

        if dashboard_name == '':
            errors.name = 'Please enter a name'
        elif not self.name_regex.match(dashboard_name):
            errors.name = 'Please use letters and digits (start with one of these), and then spaces or these characters _-!@$()*+?<>'
        

        spawners = current_user.all_spawners(include_default=True)

        spawner_name = self.get_argument('spawner_name')

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

        if len(errors) == 0:
            db = self.db

            try:

                dashboard.name = dashboard_name
                dashboard.source_spawner = spawner.orm_spawner
                db.add(dashboard)
                db.commit()

            except Exception as e:
                errors.all = str(e)

        if len(errors):
            html = self.render_template(
                "editdashboard.html",
                base_url=self.settings['base_url'],
                dashboard=dashboard,
                dashboard_name=dashboard_name,
                spawner_name=spawner_name,
                spawners=spawners,
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

        # TODO maybe authorised visitors should also see something here
        if current_user.name != user_name:
            return self.send_error(403)

        dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

        if dashboard is None:
            return self.send_error(404)

        # Get User's builders:

        status = 'Nothing'

        builders_store = self.settings['cds_builders']

        builder = builders_store[dashboard]

        if builder._build_future and builder._build_future.done():
            builder._build_future = None

        if not builder.active:
            self.log.debug('starting builder')
            status = 'Started build'

            builder._build_pending = True

            async def do_build():
            
                (new_server_name, new_server_options) =  await builder.start(dashboard, self.settings['db'])

                await self.spawn_single_user(current_user, new_server_name, options=new_server_options)

                builder._build_pending = False

            builder._build_future = maybe_future(do_build())

            #f = maybe_future(do_build())
            # TODO commit any changes in spawner.start (always commit db changes before yield)
            #gen.with_timeout(timedelta(seconds=builder.start_timeout), f)

        elif builder.pending:
            status = 'Pending'

        html = self.render_template(
            "viewdashboard.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            builder=builder,
            current_user=current_user,
            status=status,
            build_pending=builder._build_pending
        )
        self.write(html)