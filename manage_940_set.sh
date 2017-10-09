#!/bin/bash

config="/sirsi/webserver/config/"
. ${config}environ     # dot in environ variables

# export all of the environ variables to my children
for env_var in $(cat ${config}environ | awk -F'=' '{print $1}')
do
  export ${env_var}
done

run_job="/sirsi/webserver/bin/stacks_jobs/run_940_job.rb"
ruby ${run_job}

exit 0
