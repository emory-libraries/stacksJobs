#!/bin/bash
config="/sirsi/webserver/config/"
. ${config}environ     # dot in environ variables

# export all of the environ variables to my children
for env_var in $(cat ${config}environ | awk -F'=' '{print $1}')
do
  export ${env_var}
done

python /sirsi/webserver/bin/stacks_jobs/UNIV_MI_to_XM.py

exit 0

