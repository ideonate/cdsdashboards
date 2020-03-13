"""
Application for configuring and building the app environments.
"""

import os
import re
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from traitlets import Unicode, Integer, Bool, Dict, validate, TraitError, Union, default
from traitlets.config import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.options
import tornado.log
from jinja2 import Environment, FileSystemLoader, PrefixLoader, ChoiceLoader
from jupyterhub.services.auth import HubOAuthCallbackHandler

from .handlers.main import MainHandler
from .util import url_path_join


HERE = os.path.dirname(os.path.abspath(__file__))


class CDSBuilder(Application):
    """An Application for starting a builder."""

    @default('log_level')
    def _log_level(self):
        return logging.INFO

    debug = Bool(
        False,
        help="""
        Turn on debugging.
        """,
        config=True
    )

    use_registry = Bool(
        False,
        help="""
        Set to true to push images to a registry & check for images in registry.

        Set to false to use only local docker images. Useful when running
        in a single node.
        """,
        config=True
    )

    port = Integer(
        8585,
        help="""
        Port for the builder to listen on.
        """,
        config=True
    )

    config_file = Unicode(
        'cdsbuilder_config.py',
        help="""
        Config file to load.

        If a relative path is provided, it is taken relative to current directory
        """,
        config=True
    )

    concurrent_build_limit = Integer(
        32,
        config=True,
        help="""The number of concurrent builds to allow."""
    )
    executor_threads = Integer(
        5,
        config=True,
        help="""The number of threads to use for blocking calls

        Should generaly be a small number because we don't
        care about high concurrency here, just not blocking the webserver.
        This executor is not used for long-running tasks (e.g. builds).
        """,
    )

    template_path = Unicode(
        help="Path to search for custom jinja templates, before using the default templates.",
        config=True,
    )

    @default('template_path')
    def _template_path_default(self):
        return os.path.join(HERE, 'templates')

    tornado_settings = Dict(
        config=True,
        help="""
        additional settings to pass through to tornado.

        can include things like additional headers, etc.
        """
    )

    base_url = Unicode(
        '/',
        help="The base URL of the entire application",
        config=True)

    @validate('base_url')
    def _valid_base_url(self, proposal):
        if not proposal.value.startswith('/'):
            proposal.value = '/' + proposal.value
        if not proposal.value.endswith('/'):
            proposal.value = proposal.value + '/'
        return proposal.value

    def init_pycurl(self):
        try:
            AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        except ImportError as e:
            self.log.debug("Could not load pycurl: %s\npycurl is recommended if you have a large number of users.", e)
        # set max verbosity of curl_httpclient at INFO
        # because debug-logging from curl_httpclient
        # includes every full request and response
        if self.log_level < logging.INFO:
            curl_log = logging.getLogger('tornado.curl_httpclient')
            curl_log.setLevel(logging.INFO)

    def initialize(self, *args, **kwargs):
        """Load configuration settings."""
        super().initialize(*args, **kwargs)
        self.load_config_file(self.config_file)
        # hook up tornado logging
        if self.debug:
            self.log_level = logging.DEBUG
        tornado.options.options.logging = logging.getLevelName(self.log_level)
        tornado.log.enable_pretty_logging()
        self.log = tornado.log.app_log

        self.init_pycurl()

        # times 2 for log + build threads
        self.build_pool = ThreadPoolExecutor(self.concurrent_build_limit * 2)
        # default executor for asyncifying blocking calls (e.g. to kubernetes, docker).
        # this should not be used for long-running requests
        self.executor = ThreadPoolExecutor(self.executor_threads)

        jinja_options = dict(autoescape=True, )
        template_paths = [self.template_path]
        base_template_path = self._template_path_default()
        if base_template_path not in template_paths:
            # add base templates to the end, so they are looked up at last after custom templates
            template_paths.append(base_template_path)
        loader = ChoiceLoader([
            # first load base templates with prefix
            PrefixLoader({'templates': FileSystemLoader([base_template_path])}, '/'),
            # load all templates
            FileSystemLoader(template_paths)
        ])
        jinja_env = Environment(loader=loader, **jinja_options)
        if self.use_registry and self.builder_required:
            #registry = DockerRegistry(parent=self)
            pass
        else:
            registry = None

        #self.launcher = Launcher(
        #    parent=self,
        #    hub_url=self.hub_url,
        #    hub_api_token=self.hub_api_token,
        #    create_user=not self.auth_enabled,
        #)

        #self.event_log = EventLog(parent=self)

        #for schema_file in glob(os.path.join(HERE, 'event-schemas','*.json')):
        #    with open(schema_file) as f:
        #        self.event_log.register_schema(json.load(f))

        self.tornado_settings.update({
            "debug": self.debug,
            #"static_path": os.path.join(HERE, "static"),
            #'static_url_prefix': url_path_join(self.base_url, 'static/'),
            #'template_variables': self.template_variables,
            #'executor': self.executor,
            'build_pool': self.build_pool,
            'use_registry': self.use_registry,
            'traitlets_config': self.config,
            'registry': registry,
            'build_pool': self.build_pool,
            'jinja2_env': jinja_env,
            #'event_log': self.event_log,
            #'normalized_origin': self.normalized_origin
        })

        self.tornado_settings['cookie_secret'] = os.urandom(32)

        handlers = [
            #(r'/metrics', MetricsHandler),
            #(r'/versions', VersionHandler),
            #(r"/build/([^/]+)/(.+)", BuildHandler),
            #(r"/v2/([^/]+)/(.+)", ParameterizedMainHandler),
            #(r"/repo/([^/]+)/([^/]+)(/.*)?", LegacyRedirectHandler),
            ## for backward-compatible mybinder.org badge URLs
            ## /assets/images/badge.svg
            #(r'/assets/(images/badge\.svg)',
            # tornado.web.StaticFileHandler,
            # {'path': self.tornado_settings['static_path']}),
            ## /badge.svg
            #(r'/(badge\.svg)',
            # tornado.web.StaticFileHandler,
            # {'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            ## /badge_logo.svg
            #(r'/(badge\_logo\.svg)',
             #tornado.web.StaticFileHandler,
             #{'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            # /logo_social.png
            #(r'/(logo\_social\.png)',
             #tornado.web.StaticFileHandler,
             #{'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            # /favicon_XXX.ico
            #(r'/(favicon\_fail\.ico)',
            # tornado.web.StaticFileHandler,
            # {'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            #(r'/(favicon\_success\.ico)',
            # tornado.web.StaticFileHandler,
            # {'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            #(r'/(favicon\_building\.ico)',
            # tornado.web.StaticFileHandler,
            # {'path': os.path.join(self.tornado_settings['static_path'], 'images')}),
            #(r'/about', AboutHandler),
            #(r'/health', HealthHandler, {'hub_url': self.hub_url}),
            (r'/builder/(?P<user_name>[^/]+)/app/(?P<server_mame>[^/]+)?', MainHandler),
            #(r'.*', Custom404),
        ]
        #handlers = self.add_url_prefix(self.base_url, handlers)
        #if self.extra_static_path:
        #    handlers.insert(-1, (re.escape(url_path_join(self.base_url, self.extra_static_url_prefix)) + r"(.*)",
        #                         tornado.web.StaticFileHandler,
        #                         {'path': self.extra_static_path}))

        oauth_redirect_uri = os.getenv('JUPYTERHUB_OAUTH_CALLBACK_URL') or \
                             url_path_join(self.base_url, 'oauth_callback')
        oauth_redirect_uri = urlparse(oauth_redirect_uri).path
        handlers.insert(-1, (re.escape(oauth_redirect_uri), HubOAuthCallbackHandler))

        self.tornado_app = tornado.web.Application(handlers, **self.tornado_settings)


    def start(self, run_loop=True):
        self.log.info("CDSBuilder starting on port %i", self.port)
        self.http_server = HTTPServer(
            self.tornado_app,
            xheaders=True,
        )
        self.http_server.listen(self.port)
        #if self.builder_required:
        #    asyncio.ensure_future(self.watch_build_pods())
        if run_loop:
            tornado.ioloop.IOLoop.current().start()

    def stop(self):
        self.http_server.stop()
        #self.build_pool.shutdown()

main = CDSBuilder.launch_instance

if __name__ == '__main__':
    main()
