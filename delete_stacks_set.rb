=begin
Title: Delete Stacks Items Set API
Author: Alex Cooper
Date: 09/08/2017
=end

require 'rubygems'
require 'rest_client'
require 'cgi'
require 'rexml/document'
include REXML

#13146090710002486

def delete_stacks_set(url,apikey)

    outcome = 1
    begin
        headers = { :params => { CGI::escape('apikey') => apikey }}
        response = RestClient::Request.execute :method => 'DELETE' , :url => url , :headers => headers
        outcome = 0
    rescue RestClient::ExceptionWithResponse => e
        return e.response,outcome
    end
    return response,outcome

end

# reads configuration file
begin
    configuration = File.open("files/create_set.cfg")
rescue
    STDERR.puts 'Could not read configuration file'
end
#reads setId file
begin
    setIdFile = File.open("files/setId")
    for line in setIdFile
        setId = line.chomp
        setId = setId.to_s
    end
rescue
    STDERR.puts 'Could not read setIdFile'
end
# parse configuration file
begin
    for line in configuration
        line = line.chomp
        line = line.split("=")
        if line[0] == "url"
            url = line[1]
            url = url + "/#{setId}"
        elsif line[0] == "apikey"
            apikey = line[1]
        else
            continue
        end
    end
rescue
    STDERR.puts 'Could not parse configuration file'
end
response,outcome = delete_stacks_set(url,apikey)
if outcome == 0
    STDOUT.puts response
else
    STDERR.puts response
end
