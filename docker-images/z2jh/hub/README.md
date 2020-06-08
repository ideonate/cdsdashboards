# JupyterHub Image containing cdsdashboards package

## docker build

docker build -t ideonate/cdsdashboards-jupyter-hub:0.9.0-0.0.17-dev -f ./Dockerfile  ../../../

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
    