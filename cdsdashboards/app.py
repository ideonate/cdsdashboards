"""
Application for configuring and building the app environments.
"""

import os, re, sys
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from traitlets import Unicode, Integer, Bool, Dict, validate, Any, default, observe, List, TraitError
from traitlets.config import Application, catch_config_error, SingletonConfigurable
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.options
import tornado.log
from sqlalchemy.exc import OperationalError
from jinja2 import Environment, FileSystemLoader, PrefixLoader, ChoiceLoader
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub import __version__ as __jh_version__
from jupyterhub import dbutil
from jupyterhub.traitlets import EntryPointType

from .dashboard import DashboardRepr
from .util import url_path_join
from jupyterhub import orm as jhorm
from .builder.builders import BuildersDict, Builder
from ._data import DATA_FILES_PATH
from .pluggymanager import pm
from . import hookimpl


_TEMPLATE_PATH_OPEN = os.path.join(DATA_FILES_PATH, 'templates-open')
_TEMPLATE_PATH_RESTRICTED = os.path.join(DATA_FILES_PATH, 'templates-restricted')
_TEMPLATE_PATH_COMMON = os.path.join(DATA_FILES_PATH, 'templates-common')


CDS_TEMPLATE_PATHS = [_TEMPLATE_PATH_OPEN, _TEMPLATE_PATH_COMMON]
CDS_TEMPLATE_PATHS_RESTRICTED = [_TEMPLATE_PATH_RESTRICTED, _TEMPLATE_PATH_COMMON]

_all_allowed_presentation_types = ['voila', 'streamlit', 'plotlydash', 'bokeh', 'rshiny']


class CDSDashboardsConfig(SingletonConfigurable):

    builder_class = EntryPointType(
        default_value='cdsdashboards.builder.builders.Builder',
        klass=Builder,
        entry_point_group="cdsdashboards.builders",
        help="""The class to use for building dashboard servers.

        Should be a subclass of :class:`cdsdashboards.builder.builders.Builder`.

        May be registered via entry points,
            e.g. `c.cdsdashboards.builders = 'localprocess'`
        """,
    ).tag(config=True)

    server_name_template = Unicode(
        'dash-{urlname}',
        help="""
        How to name the final user server that runs the dashboard. Template vars will be expanded:

        {urlname} : dashboard URL-safe name
        {date} : <current date in YYmmdd format>
        {time} : <current date in HHMMSS format>

        """
    ).tag(config=True)

    presentation_types = List(
        trait=Unicode,
        default_value=_all_allowed_presentation_types,
        minlen=1,
        help="""
        Allowed presentation types for Dashboards. A list, allowed strings are: {}.
        There must be at least one valid entry.
        Default value is all the allowed presentation types.
        Add any custom frameworks to the extra_presentation_types config if you want to augment instead of overwrite the default list.
        """.format(_all_allowed_presentation_types)
    ).tag(config=True)

    extra_presentation_types = List(
        trait=Unicode,
        default_value=[],
        minlen=0,
        help="""
        Extra custom presentation types for Dashboards, to be added to the presentation_types list.
        A list.
        Default value is the empty list.
        """
    ).tag(config=True)

    @property
    def merged_presentation_types(self):
        return self.presentation_types + self.extra_presentation_types

    show_source_servers = Bool(
        False,
        help="""
        Allow the user to select a source server when creating a Dashboard (currently only relevant for DockerSpawner).
        """
    ).tag(config=True)

    require_source_server = Bool(
        False,
        help="""
        Require the user to select a source server when creating a Dashboard (currently only relevant for DockerSpawner).
        You must set show_source_servers to True if you set require_source_server to True.
        """
    ).tag(config=True)

    show_source_git = Bool(
        True,
        help="""
        Allow the user to enter a git repo to fetch files for a dashboard. 
        """
    ).tag(config=True)

    default_allow_all = Bool(
        True,
        help="""
        If True (default) then newly-created Dashboards will be accessible to all authenticated JupyterHub users.
        If False, only members of the dashboard's own group will be allowed to access it.
        This flag is passed on to the Dashboard object's allow_all field so can be subsequently overridden in the database.
        """
    ).tag(config=True)

    conda_envs = List(
        trait=Unicode,
        default_value=[],
        minlen=0,
        help="""
        A list of Conda env names for the dashboard creator to select.
        A list.
        Default value is the empty list.
        """
    ).tag(config=True)

    allow_custom_conda_env = Bool(
        False,
        help="""
        If True then dashboard creators can type any value for the Conda env to use, even if none is provided in the conda_envs list of pre-defined env names.
        If False (default), only Conda env names listed in the conda_envs setting can be selected - if any are present.
        """
    ).tag(config=True)

    spawn_allow_group = Unicode(
        '',
        help="""
        Name of a JupyterHub group whose users should be allowed to spawn servers and create dashboards.
        See also spawn_block_group.
        """
    ).tag(config=True)

    spawn_block_group = Unicode(
        '',
        help="""
        Name of a JupyterHub group whose users should be blocked from spawning servers and creating dashboards.
        If blank, spawn_allow_group will determine which users should be able to spawn.
        If both settings are blank, all users will be allowed to spawn.
        If both are non-blank, spawn_block_group will take priority.
        """
    ).tag(config=True)
    

class CDSConfigStore():

    _instance = None

    @classmethod
    def get_instance(cls, config):
        """
        Supply a config object to get the singleton CDSDashboardsConfig instance - only normally available from web handlers
        """
        if cls._instance:
            return cls._instance
        
        cls._instance = CDSDashboardsConfig(config=config)

        return cls._instance


class BuildersStore():

    _instance = None

    @classmethod
    def get_instance(cls, config):
        """
        Supply a config object to get the singleton instance - only normally available from web handlers
        """
        if cls._instance:
            return cls._instance
        
        cdsconfig = CDSConfigStore.get_instance(config)

        builder_class = cdsconfig.builder_class

        def builder_factory(dashboard):
            return builder_class(dashboard=dashboard, cdsconfig=cdsconfig)

        cls._instance = BuildersDict(builder_factory)
        return cls._instance
        

cds_tornado_settings = {}
