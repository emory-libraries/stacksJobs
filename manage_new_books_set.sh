#!/bin/bash

config="/sirsi/webserver/config/"
. ${config}environ     # dot in environ variables

# export all of the environ variables to my children
for env_var in $(cat ${config}environ | awk -F'=' '{print $1}')
do
  export ${env_var}
done

function run_scripts {
    cat ${add_members} |\
    while read line; do
        if [ ${line} != "end" ]; then
            ruby ${create_new_books_set}
            ruby ${add_barcodes}
            ruby ${run_job} ${library}
            sleep 2m
            ruby ${delete_set}
        else
            echo "no barcodes found"
            exit 1
        fi
    done
}

new_books_api="/sirsi/webserver/bin/stacks_jobs/new_books_api.rb"
create_new_books_set="/sirsi/webserver/bin/stacks_jobs/create_new_books_set.rb"
delete_set="/sirsi/webserver/bin/stacks_jobs/delete_stacks_set.rb"
add_barcodes="/sirsi/webserver/bin/stacks_jobs/add_barcodes_to_set.rb"
run_job="/sirsi/webserver/bin/stacks_jobs/run_stacks_job.rb"
add_members="/sirsi/webserver/bin/stacks_jobs/files/addMembers.xml"
set_id_file="/sirsi/webserver/bin/stacks_jobs/files/setId"

#New Books
ruby ${new_books_api} "new" > ${add_members}
library="new"
run_scripts

exit 0
