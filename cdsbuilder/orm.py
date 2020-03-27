__all__ = ['Dashboard', 'user_dashboard_map']

from datetime import datetime

from jupyterhub.orm import Base, Column, Integer, ForeignKey, relationship, JSONDict, Unicode, DateTime, Spawner, Table, User


class Dashboard(Base):
    """"Database class for a Dashboard"""

    __tablename__ = 'dashboards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship(User, cascade="all")

    # Which spawner/server is being cloned
    source_spawner_id = Column(Integer, ForeignKey('spawners.id', ondelete='SET NULL'))
    source_spawner = relationship(Spawner, cascade="all", foreign_keys=[source_spawner_id])

    state = Column(JSONDict)
    name = Column(Unicode(255))
    description = Column(Unicode(255))
    urlname = Column(Unicode(255), index=True, unique=True, nullable=False)

    created = Column(DateTime, default=datetime.utcnow)

    started = Column(DateTime)
    
    # The resulting spawner displaying the finished dashboad, once ready
    final_spawner_id = Column(Integer, ForeignKey('spawners.id', ondelete='SET NULL'))
    final_spawner = relationship(Spawner, cascade="all", foreign_keys=[final_spawner_id])

    # properties on the dashboard wrapper
    # some APIs get these low-level objects
    # when the dashboard isn't running,
    # for which these should all be False
    active = running = ready = False
    pending = None

    @property
    def orm_dashboard(self):
        return self

    @classmethod
    def find(cls, db, urlname, user=None):
        """Find a Dashboard by urlname.
        Returns None if not found.
        """
        if user is None:
            return db.query(cls).filter(cls.urlname == urlname).first()
        return db.query(cls).filter(cls.urlname == urlname, cls.user_id == user.id).first()


# user:dashboard many:many mapping table
user_dashboard_map = Table(
    'user_dashboard_map',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('dashboard_id', ForeignKey('dashboards.id', ondelete='CASCADE'), primary_key=True),
)

