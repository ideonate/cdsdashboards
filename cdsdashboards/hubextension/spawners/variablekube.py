from kubespawner import KubeSpawner

from .variablemixin import VariableMixin, MetaVariableMixin, Command


class VariableKubeSpawner(KubeSpawner, VariableMixin, metaclass=MetaVariableMixin):

    default_presentation_cmd = Command(
        ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'],
        allow_none=False,
        help="""
        The command to run presentations through jhsingle_native_proxy, can be a string or list.
        Default is ['python3', '-m', 'jhsingle_native_proxy.main']
        Change to e.g. ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'] to ensure start hooks are
        run in the singleuser Docker images.
        """
    ).tag(config=True)
    
    def get_pvc_manifest(self):
        presentation_type = self._get_presentation_type()

        pvc = super().get_pvc_manifest()
        
        if presentation_type != '':
            pass
            #pvc.spec.data_source = {'kind': 'PersistentVolumeClaim', 'name': 'claim-dan'}
        
        return pvc
