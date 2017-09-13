#!/bin/bash

script="/home/alex/ruby/create_stacks_set.rb"
set_id_file="/home/alex/ruby/files/setId"

ruby ${script} > ${set_id_file}

exit 0
