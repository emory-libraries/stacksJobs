#!/bin/bash

stacks_api="/home/alex/stacksJobs/stacks_apis.rb"
create_set="/home/alex/stacksJobs/create_stacks_set.rb"
delete_set="/home/alex/stacksJobs/delete_stacks_set.rb"
add_barcodes="/home/alex/stacksJobs/add_barcodes_to_set.rb"
run_job="/home/alex/stacksJobs/run_stacks_job.rb"
add_members="/home/alex/stacksJobs/files/addMembers.xml"
set_id_file="/home/alex/stacksJobs/files/setId"

ruby ${stacks_api} > ${add_members}
cat ${add_members} |\
while read line; do
    if [ ${line} != "end" ]; then
        ruby ${create_set}
        ruby ${add_barcodes}
        status=`ruby ${run_job}`
        if [ ${status} == "Done" ]; then
            ruby ${delete_set}
        fi
    else
        echo "no barcodes found"
        exit 1
    fi
done

exit 0
