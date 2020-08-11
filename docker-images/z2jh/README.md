# JupyterHub Image containing cdsdashboards package

## docker build of new hub image

From docker-images/z2jh/hub:

```
docker build -t ideonate/cdsdashboards-jupyter-k8s-hub:0.9.0-0.0.19 -f ./Dockerfile  ../../../
```

## config.yaml

imagePullPolicy: IfNotPresent

hub:
  allowNamedServers: true
  image:
    name: ideonate/cdsdashboards-jupyter-k8s-hub
    tag: 0.9.0-0.0.20

  extraConfig:
    cds-handlers: |
      from cdsdashboards.hubextension import cds_extra_handlers
      c.JupyterHub.extra_handlers = cds_extra_handlers
    cds-templates: |
      from cdsdashboards.app import CDS_TEMPLATE_PATHS
      c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
    cds-kube: |
      c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablekube.VariableKubeSpawner'
      c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.kubebuilder.KubeBuilder'

singleuser:
  image:
    name: ideonate/containds-all-basic
    tag: 0.0.20


## Persistent Storage

There are options here:

Dynamic:

### Dynamic RWX

Have each user always mount the same PVC and as 'ReadWriteMany' - but this access mode is [not supported on all hardware](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes). See also [discourse](https://discourse.jupyter.org/t/hosting-jupyterhubs-any-tips-for-new-admins/3433/13)

```
singleuser:
  storage:
    type: dynamic
    capacity: 10Gi
    dynamic:
      pvcNameTemplate: claim-{username}
      volumeNameTemplate: volume-{username}
      storageAccessModes: [ReadWriteMany]
```

### Dynamic RWO with Cloning

Clone the PVC using dataSource just for the dashboard server (requires a fairly new k8s and supporting drivers) https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/

### Static Peristent Volume

Should be fine as long as servername-independent.

```
singleuser:

  storage:
    type: static
    static:
      pvcName: "fspersist-claim"
      subPath: 'home/{username}'
```

For example, to create a local persistent volume for testing:

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: fspersist
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  storageClassName: manual
  hostPath:
    path: /Users/dan/Dev/z2jh/localstorage

---

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fspersist-claim
spec:
  resources:
    requests:
      storage: 10Gi
  accessModes:
    - ReadWriteMany
  storageClassName: manual
```


## Working on K8S API within hub pod

e.g. kubectl exec -it hub-... /bin/bash
python3

```
from kubernetes import config

config.load_incluster_config()

from kubespawner.clients import shared_client
from kubespawner.objects import make_pvc

api = shared_client('CoreV1Api')

labels = { 'app': 'jupyterhub', 'heritage': 'jupyterhub', 'component': 'singleuser-storage'}

annotations = {'hub.jupyter.org/username': 'dan', 'hub.jupyter.org/servername': 'dan-dash-2dtest'}

pvc = make_pvc(name='claim-dan-dash-2dtest', storage_class='hostpath', access_modes="ReadWriteOnce", selector=None, storage=None, labels=labels, annotations=annotations)

pvc.spec.data_source = {'kind': 'PersistentVolumeClaim', 'name': 'claim-dan'}

api.create_namespaced_persistent_volume_claim(namespace='jhub', body=pvc)
```

### More config

```
debug:
  enabled: true

auth:
  type: dummy
  dummy:
    password: 'password'
  admin:
    access: true
    users:
      - dan
  whitelist:
    users:
      - bob
```

# Minikube for testing

```
minikube start --driver=hyperkit

(OR: minikube config set driver hyperkit)

# To use minikube's docker registry e.g. for docker build:
eval $(minikube docker-env)

# Use mk instead of kubectl

alias mk="minikube kubectl --"

mk create namespace khub

helm upgrade --install khubrel jupyterhub/jupyterhub   --namespace khub    --version=0.9.0   --values config.yaml

mk config set-context --current --namespace=khub

mk port-forward svc/proxy-public 8000:80



minikube delete
```


## Build local hub image

Don't tag local images as 'latest' otherwise k8s will always attempt to pull first.

Ensure `imagePullPolicy: IfNotPresent` is in the config.yaml.

```
eval $(minikube docker-env)

cd ~/Dev/cdsdashboards

docker build -t cdsdashboards-jupyter-k8s-hub:now -f ./docker-images/z2jh/hub/Dockerfile .

cd docker-images/singleuser-example/containds-all-example

docker build -t containds-all-example:now --build-arg FRAMEWORKS_LINE=streamlit .

```





