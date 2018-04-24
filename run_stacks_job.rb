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

def parse_xml(xml)

    outcome = 1
    begin
        job_id = /Job no\.\ ([0-9]+)\ triggered/.match(xml)
        response = job_id[1]
        outcome = 0
    rescue
        STDERR.puts 'Could not parse xml'
        return outcome
    end
    return response

end

def listener(job_id)

    outcome = 1
    begin
        running = true
        job_dir = "/sirsi/webserver/integrations/jobs/M0/"
        webhook = job_dir + job_id
        while running
            if not File.file?(webhook)
                running = true
            else
                running = false
            end
        end
        outcome = 0
    rescue
        STDERR.puts 'Could not find webkook'
        return outcome
    end
    return outcome

end

# process argument
input_arg = ARGV[0]
if input_arg == "univ"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_univ.xml")
elsif input_arg == "bus"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_bus.xml")
elsif input_arg == "chem"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_chem.xml")
elsif input_arg == "hlth"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_hlth.xml")
elsif input_arg == "lsc"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_lsc.xml")
elsif input_arg == "musme"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_musme.xml")
elsif input_arg == "wd"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_withdraw.xml")
elsif input_arg == "new"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_new.xml")
elsif input_arg == "940"
    job_xml = File.open("/sirsi/webserver/bin/stacks_jobs/files/job_940.xml")
else
    STDERR.puts 'Expected input argument but failed'
end
# build job xml
begin
    setId = File.open("/sirsi/webserver/bin/stacks_jobs/files/setId")
    setId = setId.read
    setId = setId.chomp
    setId = setId.to_s
    job_xml = job_xml.read
    values = job_xml.sub! 'setId', setId
    puts values
rescue
    STDERR.puts 'Could not open and edit job xml'
end
begin
    configuration = File.open("/sirsi/webserver/bin/stacks_jobs/files/run_a_job.cfg")
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
        elsif line[0] == "wd_url"
            wd_url = line[1]
        elsif line[0] == "apikey"
            apikey = line[1]
        end
    end
rescue
    STDERR.puts 'Could not parse configuration file'
end
if input_arg == "wd"
    url = wd_url
else
    url = url
end
response,outcome = run_job(url,apikey,values)
xml = response
response = parse_xml(xml)
job_id = response
response = listener(job_id)
if response == 0
    STDOUT.puts 'Done'
else
    STDERR.puts response
end
