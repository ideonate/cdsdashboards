import re

from tornado.web import authenticated

from jupyterhub.handlers.base import BaseHandler

from ..orm import Dashboard
from ..util import DefaultObjDict


class DashboardBaseHandler(BaseHandler):

    unsafe_regex = re.compile(r'[^a-zA-Z0-9]+')
    
    def calc_safe_name(self, dashboard_name):
        safe_name = re.sub(self.unsafe_regex, '-', dashboard_name).lower()

        # TODO If already exists, add -1 etc 

        return safe_name

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

    name_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_\- \!\@\$\(\)\*\+\?\<\>]+$')

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
            safe_name = self.calc_safe_name(dashboard_name)      

            db = self.db

            try:

                d = Dashboard(name=dashboard_name, safe_name=safe_name, user_id=current_user.id)
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

        #reverse_url('cds_dashboard_config_handler', )

        url = "{}hub/dashboards/{}/{}/edit".format(self.settings['base_url'], current_user.name, safe_name)

        self.log.debug("Redirect to "+url)

        self.redirect(url)


class DashboardConfigHandler(DashboardBaseHandler):

    @authenticated
    async def get(self, user_name, dashboard_name=''):

        #dashboard_store = self.settings['dashboard']

        self.log.debug('calling get_app_server')

        #dashboard = await dashboard_store.get_app_server(user_name, server_name)

        self.log.info('finding user ')

        user = self.find_user(user_name)

        current_user = await self.get_current_user()


        db = self.db

        d = Dashboard(name=dashboard_name, user_id=current_user.id)
        db.add(d)
        db.commit()

        html = self.render_template(
            "appconfig.html",
            base_url=self.settings['base_url'],
            user_name=user_name,
            server_name=dashboard_name,
            user=user,
            current_user=current_user
        )
        self.write(html)
