=begin
Title: Add Memebers to Stacks Set
Author: Alex C.
Date: 09/13/2017
Purpose: Post XML containing barcodes of members in Alma set
=end
require 'rubygems'
require 'rest_client'
require 'cgi'

def add_members(url,apikey,values)

    outcome = 1
    begin
        headers = { 'Content-Type' => 'application/xml' , :params => { CGI::escape('id_type') =>'BARCODE' , CGI::escape('op') => 'add_members' , CGI::escape('apikey') => apikey } }
        response = RestClient::Request.execute :method => 'POST' , :url => url , :payload => values , :headers => headers
        outcome = 0
    rescue RestClient::ExceptionWithResponse => e
        return e.response,outcome
    end
    return response,outcome

end

begin
    xml = File.open("files/addMembers.xml")
rescue
    STDERR.puts 'Could not open xml file'
end
begin
    setId = File.open("files/setId")
    setId = setId.read
    setId = setId.chomp
    setId = setId.to_s
rescue
    STDERR.puts 'Could not read setId file'
end
begin
    configuration = File.open("files/create_set.cfg")
rescue
    STDERR.puts 'Could not open configuration file'
end
begin
    for line in configuration
        line = line.chomp
        line = line.split("=")
        if line[0] == "url"
            url = line[1]
            url = url + "/#{setId}"
        elsif line[0] == "apikey"
            apikey = line[1]
        end
    end
rescue
    STDERR.puts 'Could not parse configuration file'
end
begin
    xml = xml.read
    xml = xml.chomp
    values = xml
rescue
    STDERR.puts 'Could not read xml file'
end
response,outcome = add_members(url,apikey,values)
if outcome == 0
    STDOUT.puts response
else
    STDERR.puts response
end
