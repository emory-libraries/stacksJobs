=begin
Title: Process Stacks Items
Author: Alex Cooper
Date: 09/01/2017
=end

require 'rubygems'
require 'rest_client'
require 'cgi'
require 'rexml/document'
include REXML

def getAnalytics(url,path,apikey,limit)

    outcome = 1
    response = 'N/A'
    headers = { :params => { CGI::escape('path') => path, CGI::escape('apikey') => apikey, CGI::escape('limit') => limit } }
    begin
        response = RestClient::Request.execute :method => 'GET', :url => url, :headers => headers
        outcome = 0
    rescue
        STDERR.puts 'API call failed'
    end
    return response,outcome
end

def parseAnalyticsXml(xml)

    mmsid = []
    outcome = 1
    mmsids = xml.elements.each("QueryResult/ResultXml/rowset/Row/Column2") { |element| element.text }
    library = xml.elements.each("QueryResult/ResultXml/rowset/Row/Column7") { |element| element.text }
    barcodes = xml.elements.each("QueryResult/ResultXml/rowset/Row/Column9") { |element| element.text }
    return barcodes,outcome
end

# open file with api information
begin
    configuration = File.open("files/stacks.cfg", "r")
rescue
    STDERR.puts 'Could not read configuration file'
end

# loops over api parameters
for line in configuration
    line = line.chomp
    line = line.split("=")
    begin
        if line[0] == "limit"
            limit = line[1]
        elsif line[0] == "analytics_url"
            analytics_url = line[1]
        elsif line[0] == "path_xmxl_univ"
            path_xmxl_univ = line[1]
        elsif line[0] == "analytics_apikey"
            analytics_apikey = line[1]
        elsif line[0] == "alma_bib_apikey"
            alma_bib_apikey = line[1]
        elsif line[0] == "alma_bib_url"
            alma_bib_url = line[1]
        end
    rescue
        STDERR.puts 'Could not parse configuration file'
    end
end

# pass arguments to analyitcs api method
xml,outcome = getAnalytics(analytics_url,path_xmxl,analytics_apikey,limit)
#puts xml
# parses XML
if outcome == 0
    begin
        doc = Document.new xml
        root = doc.root
    rescue
        STDERR.puts 'Could not read XML'
    end
    begin
        finished = root.elements["QueryResult/IsFinished"].text
        token = root.elements["QueryResult/ResumptionToken"].text
    rescue
        STDERR.puts 'Could not parse XML results'
    end
    if finished
        parsedXml,outcome = parseAnalyticsXml(root)
        string = ""
        for line in parsedXml
# build set xml
####<set><members><member><id>010000690077</id></member></members></set>
            barcode = line.text
            barcode = barcode.to_s
            string = string << "<member><id>#{barcode}</id></member>"
        end
    xml = "<set><members>#{string}</members></set>"
    puts xml
    else
        workToDo = true
    end
else
    STDERR.puts 'getAnalytics failed'
end
