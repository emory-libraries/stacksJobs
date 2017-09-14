#!/bin/bash

stacks_api="/home/alex/stacksJobs/stacks_apis.rb"
create_set="/home/alex/stacksJobs/create_stacks_set.rb"
delete_set="/home/alex/stacksJobs/delete_stacks_set.rb"
set_id_file="/home/alex/stacksJobs/files/setId"

ruby 
ruby ${create_set} > ${set_id_file}

exit 0
