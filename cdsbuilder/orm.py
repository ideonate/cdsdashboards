__all__ = ['Dashboard', 'user_dashboard_map']

from jupyterhub.orm import Base, Column, Integer, ForeignKey, relationship, JSONDict, Unicode, DateTime, Server, Table

class Dashboard(Base):
    """"State about a Dashboard"""

    __tablename__ = 'dashboards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    source_server_id = Column(Integer, ForeignKey('servers.id', ondelete='SET NULL'))
    source_server = relationship(Server, cascade="all")

    state = Column(JSONDict)
    name = Column(Unicode(255))

    started = Column(DateTime)
    last_activity = Column(DateTime, nullable=True)
    dashboard_options = Column(JSONDict)

    # properties on the dashboard wrapper
    # some APIs get these low-level objects
    # when the dashboard isn't running,
    # for which these should all be False
    active = running = ready = False
    pending = None

    @property
    def orm_dashboard(self):
        return self


# user:dashboard many:many mapping table
user_dashboard_map = Table(
    'user_dashboard_map',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('dashboard_id', ForeignKey('dashboards.id', ondelete='CASCADE'), primary_key=True),
)

