from datetime import datetime
import alembic.command
import alembic.config
from alembic.script import ScriptDirectory
from tornado.log import app_log

from jupyterhub.orm import Base, Column, Integer, ForeignKey, relationship, JSONDict, Unicode, DateTime, Spawner, Group, User, Boolean
from sqlalchemy.orm import backref

my_table_names = {'dashboards'}


class Dashboard(Base):
    """"Database class for a Dashboard"""

    __tablename__ = 'dashboards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship(User, backref=backref("dashboards_own", uselist=True, cascade='all, delete-orphan'))

    # Which spawner/server is being cloned
    source_spawner_id = Column(Integer, ForeignKey('spawners.id', ondelete='SET NULL'))
    source_spawner = relationship(Spawner, foreign_keys=[source_spawner_id], backref=backref('dashboard_source_for', uselist=True))

    name = Column(Unicode(255))
    description = Column(Unicode(255), default='')

    urlname = Column(Unicode(255), index=True, unique=True, nullable=False)

    created = Column(DateTime, default=datetime.utcnow)

    started = Column(DateTime)

    start_path = Column(Unicode(255), default='') # E.g. which ipynb file should Voila display

    presentation_type = Column(Unicode(255), default='') # Code for framework: voila, streamlit, dash etc

    allow_all = Column(Boolean, index=True, default=True)
    
    # The resulting spawner displaying the finished dashboard, once ready
    final_spawner_id = Column(Integer, ForeignKey('spawners.id', ondelete='SET NULL'))
    final_spawner = relationship(Spawner, foreign_keys=[final_spawner_id], backref=backref('dashboard_final_of', uselist=False))

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL'))
    group = relationship(Group, foreign_keys=[group_id], backref=backref('dashboard_visitors_for', uselist=False))

    options = Column(JSONDict)

    @property
    def groupname(self):
        if not self.urlname:
            raise Exception('Cannot calculate groupname before urlname is set')
        return 'dash-{}'.format(self.urlname)

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

    def is_orm_user_allowed(self, user):
        if user == self.user:
            return True
        if not self.allow_all:
            if not user in self.group.users:
                return False
        return True

    def __iter__(self):
        """
        Fix for bug in JH 1.1, which was fixed in JH 1.2 by:
        https://github.com/jupyterhub/jupyterhub/commit/84acdd5a7ffb3d79ca04aa86ffcea7e067cce6ee#diff-ea603eff790f5d20b768e093b5340908
        (Actually, the real fix was a little bit earlier, but this is the right place).
        Without this, delete dashboard causes an error when corresponding relationships were expired.
        """
        return iter([self])


class DatabaseSchemaMismatch(Exception):
    """Exception raised when the database schema version does not match

    the current version of JupyterHub.
    """


def check_db_revision(engine):
    """Check the JupyterHub database revision

    After calling this function, an alembic tag is guaranteed to be stored in the db.

    - Checks the alembic tag and raises a ValueError if it's not the current revision
    - If no tag is stored (Bug in Hub prior to 0.8),
      guess revision based on db contents and tag the revision.
    - Empty databases are tagged with the current revision
    """
    # Check database schema version
    current_table_names = set(engine.table_names())

    from .dbutil import _temp_alembic_ini

    with _temp_alembic_ini(engine.url) as ini:
        cfg = alembic.config.Config(ini)
        scripts = ScriptDirectory.from_config(cfg)
        head = scripts.get_heads()[0]
        base = scripts.get_base()

        if not my_table_names.intersection(current_table_names):
            # no tables have been created, stamp with current revision
            app_log.debug("Stamping empty dashboards database with alembic revision %s", head)
            alembic.command.stamp(cfg, head)
            return

        if 'cds_alembic_version' not in current_table_names:
            # Has not been tagged or upgraded before.
            # This should only occur for databases created on cdsdashboards 0.0.11 or earlier
            rev = base
            app_log.debug("Stamping dashboards database schema version %s", rev)
            alembic.command.stamp(cfg, rev)

    # check database schema version
    # it should always be defined at this point
    alembic_revision = engine.execute(
        'SELECT version_num FROM cds_alembic_version'
    ).first()[0]
    if alembic_revision == head:
        app_log.debug("database dashboards schema version found: %s", alembic_revision)
        pass
    else:
        raise DatabaseSchemaMismatch(
            "Found database schema version {found} != {head}. "
            "Backup your database and run `jupyterhub upgrade-db`"
            " to upgrade to the latest schema.".format(
                found=alembic_revision, head=head
            )
        )
