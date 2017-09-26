#!/bin/ruby
=begin
Title: Process Used New Books
Author: Alex Cooper
Date: 09/26/2017
=end

require 'rubygems'
require 'rest_client'
require 'cgi'
require 'rexml/document'
include REXML

def getAnalytics(url,apikey,path,limit)

    outcome = 1
    headers = { :params => { CGI::escape('path') => path, CGI::escape('apikey') => apikey, CGI::escape('limit') => limit }}
    begin
        response = RestClient::Request.execute :method => 'GET', :url => url, :headers => headers
        outcome = 0
    rescue RestClient::ExceptionWithResponse => e
        return e.response, outcome
    end
    return response,outcome
end

def parseAnalyticsXML(xml)

    outcome = 1
    begin
        doc = Document.new xml
        root = doc.root
        barcodes = root.elements.each("QueryResult/ResultXml/rowset/Row/Column6") { |element| element.text }
#        puts barcodes
        outcome = 0
    rescue
        STDERR.puts 'Could not parse xml'
    end
    return barcodes,outcome
end

#### Process configuration file
begin
    configuration = File.open("/sirsi/webserver/bin/stacks_jobs/files/stacks.cfg")
rescue
    STDERR.puts 'Could not open configuration file'
end
for line in configuration
    line = line.chomp
    line = line.split("=")
    begin
        if line[0] == "limit"
            limit = line[1]
        elsif line[0] == "analytics_url"
            analytics_url = line[1]
        elsif line[0] == "analytics_apikey"
            analytics_apikey = line[1]
        elsif line[0] == "path_new"
            path = line[1]
        end
    rescue
        STDERR.puts 'Could not parse configuration file'
    end
end
#### Place API call
xml,outcome = getAnalytics(analytics_url,analytics_apikey,path,limit)
if outcome == 1
    puts xml 
end
#### Parse Analytics XML
barcodes,outcome = parseAnalyticsXML(xml)
string = ""
for line in barcodes
    barcode = line.text
    barcode = barcode.to_s
    string = string << "<member><id>#{barcode}</id></member>"
end
if not string.empty?
    xml = "<set><members>#{string}</members></set>"
    STDOUT.puts xml
else
    STDOUT.puts 'end'
end
