# JupyterHub Image containing cdsdashboards package

## docker build

docker build -t ideonate/cdsdashboards-jupyter-hub:0.9.0-0.0.17-dev -f ./Dockerfile  ../../../

## Persistent Storage

There are two options here:

1. Have each user always mount the same PVC and as 'ReadWriteMany' (but this access mode is not supported on all hardware) https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes see also https://discourse.jupyter.org/t/hosting-jupyterhubs-any-tips-for-new-admins/3433/13
2. Clone the PVC using dataSource just for the dashboard server (requires a fairly new k8s) https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/

## config.yaml

hub:
  allowNamedServers: true
  image:
    name: ideonate/cdsdashboards-jupyter-hub
    tag: 0.9.0-0.0.16

  extraConfig:
    cds-handlers: |
      from cdsdashboards.hubextension import cds_extra_handlers
      c.JupyterHub.extra_handlers = cds_extra_handlers
    cds-templates: |
      from cdsdashboards.app import CDS_TEMPLATE_PATHS
      c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
    cds-builder: |
      c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'
    cds-kube: |
      c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablekube.VariableKubeSpawner'

singleuser:
  image:
    name: ideonate/containds-all-basic
    tag: latest

debug:
  enabled: true


## Working on K8S API within hub pod

e.g. kubectl exec -it hub-... /bin/bash
python3

```
from kubernetes import config

config.load_incluster_config()

from kubespawner.clients import shared_client
from kubespawner.objects import make_pvc


api = shared_client('CoreV1Api')

pvc = make_pvc(name='claim-dan-dash-2dtest', storage_class=None, access_modes="ReadWriteOnce", selector=None, storage=None)

pvc = make_pvc(name='claim-dan-dash-2dtest', storage_class='hostpath', access_modes="ReadWriteOnce", selector=None, storage=None)


pvc.spec.data_source = {'kind': 'PersistentVolumeClaim', 'name': 'claim-dan'}

api.create_namespaced_persistent_volume_claim(namespace='jhub', body=pvc)
```