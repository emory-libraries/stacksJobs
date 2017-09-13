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
=begin
        url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/13170727290002486'
        values   = '<set><members><member><id>000011151287</id></member><member><id>000011537344</id></member><member><id>010002582406</id></member><member><id>010002977142</id></member><member><id>010002740484</id></member></members></set>'
        headers  = { 'Content-Type' => 'application/xml' , :params => { CGI::escape('id_type') => 'BARCODE',CGI::escape('op') => 'add_members',CGI::escape('apikey') => 'l7xxaa2eb31e052643c093b484bd3d81617d' } }
        response = RestClient::Request.execute :method => 'POST', :url => url  , :payload => values, :headers => headers
=end
        headers = { 'Content-Type' => 'application/xml' , :params => { CGI::escape('id_type') =>'BARCODE' , CGI::escape('op') => 'add_members' , CGI::escape('apikey') => apikey } }
        response = RestClient::Request.execute :method => 'POST' , :url => url , :payload => values , :headers => headers
    rescue RestClient::ExceptionWithResponse => e
        puts e.response
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
puts response
