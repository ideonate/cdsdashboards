#!/bin/bash

# For a command line such as:
# "/home/jovyan/entrypoint.sh jupyter notebook --ip 0.0.0.0 --port 59537 --NotebookApp.custom_display_url=http://127.0.0.1:59537"
# strip out most args, just pass on the port and notebook_dir
#
# Requires bash v4+


port="8888"

echo "Command line: $@"

# Iterate through cmd line arguments, picking out args
declare -A args

delim='='
collect_next=''

for var in "$@"
do

  if [ ! -z "$collect_next" ]; then
    echo "Collecting $collect_next $var"
    args[$collect_next]=$var
    collect_next=''
  else

    splitarg=${var%%$delim*}

    if [ "${splitarg:0:2}" == "--" ]; then
      if [ ${#splitarg} == ${#var} ]; then # There is no = in this argument
        collect_next="${splitarg:2}"
      else
        args["${splitarg:2}"]=${var#*$delim}
        echo "Setting ${splitarg:2} ${var#*$delim}"
      fi
    fi
  fi

done

# Update port if found in args
if [ ! -z ${args["port"]} ]; then
  port=${args["port"]}
fi

# Starting folder or file
notebook=`pwd`
if [ ! -z ${args["notebook-dir"]} ]; then
  notebook=${args["notebook-dir"]}
fi

if [ ! -z "$JUPYTERHUB_CDS_PRESENTATION_PATH" ]; then
  notebook="$notebook/$JUPYTERHUB_CDS_PRESENTATION_PATH"
fi

echo "Using file/folder location $notebook"

# Run the proxy process
jhsingle-native-proxy --destport 0 --authtype oauth voila "$notebook" {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --port $port
