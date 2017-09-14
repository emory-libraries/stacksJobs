#!/bin/bash

stacks_api="/home/alex/stacksJobs/stacks_apis.rb"
create_set="/home/alex/stacksJobs/create_stacks_set.rb"
delete_set="/home/alex/stacksJobs/delete_stacks_set.rb"
add_barcodes="/home/alex/stacksJobs/add_barcodes_to_set.rb"
add_members="/home/alex/stacksJobs/files/addMembers.xml"
set_id_file="/home/alex/stacksJobs/files/setId"

ruby ${stacks_api} > ${add_members}
ruby ${create_set}
ruby ${add_barcodes}

exit 0
