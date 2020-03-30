#!/bin/bash

# For a command line such as:
# "/home/jovyan/entrypoint.sh jupyter notebook --ip 0.0.0.0 --port 59537 --NotebookApp.custom_display_url=http://127.0.0.1:59537"
# strip out most args, just pass on the port


collect_port=0
port="8888"
delim='='

for var in "$@"
do
    echo "$var"

    if [ "$collect_port" == "1" ]; then
       echo "Collecting external port $var"
       port=$var
       collect_port=0
    fi

    splitarg=${var%%$delim*}

    if [ "$splitarg" == "--port" ]; then
       if [ ${#splitarg} == ${#var} ]; then
         collect_port=1
       else
         port=${var#*$delim}
         echo "Setting external port $port"
       fi
    fi
done


# Remove trailing slash
base_url=${JUPYTERHUB_SERVICE_PREFIX%/}

voila /home/jovyan --port=${port} --no-browser --Voila.base_url=${base_url}/ --Voila.server_url=${base_url} --Voila.ip=0.0.0.0
