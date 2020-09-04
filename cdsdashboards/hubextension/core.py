from jupyterhub.handlers.pages import HomeHandler
from .base import DashboardBaseMixin

class OurHomeHandler(HomeHandler, DashboardBaseMixin):

    async def get(self, *args, **kwargs):

        current_user = await self.get_current_user()

        if not self.can_user_spawn(current_user):
            html = self.render_template(
                "homecds.html",
                base_url=self.settings['base_url'],
                current_user=current_user
            )
            return self.write(html)

        return await super().get(*args, **kwargs)
    