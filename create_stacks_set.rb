=begin
Title: Create Stacks Items Set API
Author: Alex Cooper
Date: 09/08/2017
=end

require 'rubygems'
require 'rest_client'
require 'cgi'
require 'rexml/document'
include REXML

def post_stacks_set(url,apikey,xml)

    outcome = 1
    begin
        values = xml
        headers = { 'Content-Type' => 'application/xml' , :params => { CGI::escape('apikey') => apikey }}
        response = RestClient::Request.execute :method => 'POST' , :url => url , :payload => values , :headers => headers
        outcome = 0
    rescue RestClient::ExceptionWithResponse => e
        STDERR.puts e.response
    end
    return response,outcome

end

# reads configuration file
begin
    configuration = File.open("files/create_set.cfg")
rescue
    STDERR.puts 'Could not read configuration file'
end
# reads set xml
begin
    xml = File.open("files/set.xml")
rescue
    STDERR.puts 'Could not read set xml'
end
# parse configuration file
begin
    for line in configuration
        line = line.chomp
        line = line.split("=")
        if line[0] == "url"
            url = line[1]
        elsif line[0] == "apikey"
            apikey = line[1]
        else
            continue
        end
    end
rescue
    STDERR.puts 'Could not parse configuration file'
end
configuration.close
response,outcome = post_stacks_set(url,apikey,xml)
if outcome == 0
    doc = REXML::Document.new response
    setId = doc.elements["set/id"].text
    File.write('files/setId', setId)
#    puts setId
end
