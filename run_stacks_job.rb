=begin
Title: Run Change Item Job
Author: Alex Cooper
Date: 09/13/2017
Purpose: Run the change items job for Stacks team
=end

require 'rexml/document'
require 'rest_client'
require 'cgi'
include REXML

def run_job(url,apikey,values)

    outcome = 1
    begin
        headers = { 'Content-Type' => 'application/xml' , :params => { CGI::escape('op') => 'run' , CGI::escape('apikey') => apikey }}
        response = RestClient::Request.execute :method => 'POST' , :url => url , :payload => values , :headers => headers
        outcome = 0
    rescue RestClient::ExceptionWithResponse => e
        return e.response,outcome
    end
    return response,outcome

end

# build job xml
begin
    job_xml = File.open("files/job.xml")
    setId = File.open("files/setId")
    setId = setId.read
    setId = setId.chomp
    setId = setId.to_s
    job_xml = job_xml.read
    values = job_xml.sub! 'setId', setId
rescue
    STDERR.puts 'Could not open and edit job xml'
end
begin
    configuration = File.open("files/run_a_job.cfg")
rescue
    STDERR.puts 'Could not open configuration file'
end
# get configuration items
begin
    for line in configuration
        line = line.chomp
        line = line.split("=")
        if line[0] == "url"
            url = line[1]
        elsif line[0] == "apikey"
            apikey = line[1]
        end
    end
rescue
    STDERR.puts 'Could not parse configuration file'
end
response,outcome = run_job(url,apikey,values)
if outcome == 0
    STDOUT.puts response
else
    STDERR.puts response
end
