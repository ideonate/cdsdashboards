First create docker container:
```
docker run \
  --privileged \
  --detach \
  --name=tljh-dev \
  --publish 12000:80 \
  --mount type=bind,source=$(pwd),target=/srv/src \
  ideonate/tljh-dev:20200604
```

Within docker exec -it tljh-dev /bin/bash:

source /opt/tljh/hub/bin/activate 

cd /opt/tljh/
git clone https://github.com/ideonate/cdsdashboards

cd cdsdashboards/
pip install -e .

source /opt/tljh/user/bin/activate
pip install -e .[user]



source /opt/tljh/user/bin/activate 
conda install r-base
conda install r-essentials
conda install -c r r-irkernel


apt-get update
apt-get install vim
vim /opt/tljh/config/jupyterhub_config.d/cdsdashboards_config.py

https://cdsdashboards.readthedocs.io/en/latest/chapters/setup/tljh.html#installing-cdsdashboards


sudo tljh-config reload

source /opt/tljh/user/bin/activate 

R -e "install.packages('shiny', repos='https://cran.rstudio.com/')"



apt-get install wget

apt-get install gdebi-core
wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.13.944-amd64.deb
gdebi shiny-server-1.5.13.944-amd64.deb


systemctl stop shiny-server


# Try example 2 here https://shiny.rstudio.com/articles/basics.html


# Visit 127.0.0.1:12000/hub/home
# login with admin/password