import sys
from concurrent.futures import ThreadPoolExecutor
import functools

import docker
from docker.utils import kwargs_from_env
from traitlets import Dict, Unicode, Any
from tornado import ioloop
from tornado.log import app_log
from .builders import BuildException
from .processbuilder import ProcessBuilder
from .. import hookimpl
from ..pluggymanager import pm


class BasicDockerBuilder(ProcessBuilder):

    user = Any()

    @property
    def client(self):
        """single global client instance"""
        cls = self.__class__
        if cls._client is None:
            kwargs = {"version": "auto"}
            if self.tls_config:
                kwargs["tls"] = docker.tls.TLSConfig(**self.tls_config)
            kwargs.update(kwargs_from_env())
            kwargs.update(self.client_kwargs)
            client = docker.APIClient(**kwargs)
            cls._client = client
        return cls._client

    tls_config = Dict(
        config=True,
        help="""Arguments to pass to docker TLS configuration.
        See docker.client.TLSConfig constructor for options.
        """,
    )

    client_kwargs = Dict(
        config=True,
        help="Extra keyword arguments to pass to the docker.Client constructor.",
    )

    _client = None

    def _docker(self, method, *args, **kwargs):
        """wrapper for calling docker methods
        to be passed to ThreadPoolExecutor
        """
        m = getattr(self.client, method)
        return m(*args, **kwargs)

    def docker(self, method, *args, **kwargs):
        """Call a docker method in a background thread
        returns a Future
        """
        fn = functools.partial(self._docker, method, *args, **kwargs)
        return ioloop.IOLoop.current().run_in_executor(self._executor, fn)

    _executor = None

    @property
    def executor(self):
        """single global executor"""
        cls = self.__class__
        if cls._executor is None:
            cls._executor = ThreadPoolExecutor(1)
        return cls._executor

    repo_prefix = Unicode(default_value='cdsuser').tag(config=True)

    async def prespawn_server_options(self, dashboard, dashboard_user, ns):

        source_spawner_orm = dashboard.source_spawner

        if source_spawner_orm is None:
            return {} # Just use default image

        tag = self.format_string('{date}-{time}', ns=ns)

        source_spawner_name = source_spawner_orm.name

        #if source_spawner_name not in dashboard_user.spawners:
        #    raise BuildException('The source server is not currently available for this dashboard')

        source_spawner = dashboard_user.spawners[source_spawner_name]

        app_log.debug('source_spawner {}'.format(source_spawner))

        #if source_spawner.state is None:
        #    raise BuildException('Source server has never been run, so there is nothing to clone!')

        object_id = source_spawner.object_id #source_spawner.state.get('object_id', None)

        app_log.debug('Docker object_id is {}'.format(object_id))

        if object_id is None:
            raise BuildException('No docker object specified in spawner state - maybe the source server has never been run')

        source_container = await self.docker('inspect_container', object_id)

        if source_container is None:
            raise BuildException('No docker object returned as source container')

        # Commit image of current server

        reponame = '{}/{}'.format(self.repo_prefix, dashboard.urlname)

        image_name = '{}:{}'.format(reponame, tag)

        app_log.info('Committing Docker image {}'.format(image_name))

        dockerfile_changes="\n".join([
            'CMD ["{}-entrypoint.sh"]'.format(dashboard.presentation_type),
            'ENV JUPYTERHUB_GROUP {}'.format(dashboard.groupname),
            'ENV JUPYTERHUB_ANYONE {}'.format(dashboard.allow_all and '1' or '0'),
            'ENV JUPYTERHUB_CDS_PRESENTATION_PATH "{}"'.format(dashboard.start_path or ''),
        ])

        await self.docker('commit', object_id, repository=reponame, tag=tag, changes=dockerfile_changes)

        self.log.info('Finished commit of Docker image {}:{}'.format(reponame, tag))

        return {'image': image_name}


DockerBuilder = BasicDockerBuilder
# Register plugin hooks so we use the Basic handlers by default, unless overridden

@hookimpl
def get_builder_DockerBuilder():
    return BasicDockerBuilder

pm.register(sys.modules[__name__])

DockerBuilder = pm.hook.get_builder_DockerBuilder()[0]
