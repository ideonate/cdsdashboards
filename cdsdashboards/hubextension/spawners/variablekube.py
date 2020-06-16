from kubespawner import KubeSpawner

from .variablemixin import VariableMixin, MetaVariableMixin


class VariableKubeSpawner(KubeSpawner, VariableMixin, metaclass=MetaVariableMixin):
    
    def get_pvc_manifest(self):
        presentation_type = self._get_presentation_type()

        pvc = super().get_pvc_manifest()
        
        if presentation_type != '':
            pass
            #pvc.spec.data_source = {'kind': 'PersistentVolumeClaim', 'name': 'claim-dan'}
        
        return pvc
