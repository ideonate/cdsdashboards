import re

from tornado.web import authenticated

from jupyterhub.handlers.base import BaseHandler

from ..orm import Dashboard
from ..util import DefaultObjDict


class DashboardBaseHandler(BaseHandler):

    unsafe_regex = re.compile(r'[^a-zA-Z0-9]+')
    
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


class DashboardConfigHandler(DashboardBaseHandler):

    @authenticated
    async def get(self, user_name, dashboard_urlname=''):

        current_user = await self.get_current_user()

        if current_user.name != user_name:
            return self.send_error(403)

        dashboard = Dashboard.find(db=self.db, urlname=dashboard_urlname, user=current_user)

        if dashboard is None:
            return self.send_error(404)

        html = self.render_template(
            "appconfig.html",
            base_url=self.settings['base_url'],
            dashboard=dashboard,
            current_user=current_user
        )
        self.write(html)
