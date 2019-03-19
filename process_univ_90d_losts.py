#!/opt/rh/python27/root/usr/bin/python
import sys
import requests
import xml.etree.ElementTree as ET
import time

# DEFINE SECONDARY FUNCTIONS FOR USE BY MAIN FUNCTION

## MAKE API CALL TO GET CONTENT
def get_lost_items(analytics_url,path,analytics_apikey):
  payload = {'apikey':analytics_apikey, 'path':path}
  try:
    r = requests.get(analytics_url,params=payload)
    response = r.content
    url = r.url
  except:
    sys.stderr.write("Could not find get_lost_items"+"\n")
  return response,url

## USE CONTENT FROM API CALL TO CREATE BARCODE LIST
def get_barcode_from_xml(xml):
  xml = xml.replace("\n", "")
  xml = xml.replace(' xmlns="urn:schemas-microsoft-com:xml-analysis:rowset"', "")
  tree = ET.fromstring(xml)

  barcode = ""
  parsed_xml = []
  try:
    rowset = tree.find("QueryResult/ResultXml/rowset")
  except:
    sys.stderr.write("Could not find rowset"+"\n")
  try:
    rows = rowset.findall("Row")
    if rows != None:
      for row in rows:
        try:
          barcode = row.find("Column6")
          barcode = str(barcode.text)
        except:
          sys.stderr.write("Could not find barcode"+"\n")
        parsed_xml.append(barcode)      
    else:
      sys.stderr.write("No items found"+"\n")
      return "Fail"
  except:
    sys.stderr.write("Could not find rows"+"\n") 
  return parsed_xml

## USE CONTENT FROM API CALL TO COLLECT SETIDs
def get_setid_from_content(xml):
  xml = xml.replace("\n", "")
  tree = ET.fromstring(xml)

  setid = ""
  parsed_xml = []
  try:
    setid = tree.find("id")
    setid = str(setid.text)
  except:
    sys.stderr.write("Could not find set id"+"\n")
  return setid

## CREATE A SET
def create_set(alma_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'apikey':alma_apikey}
  try:
    r = requests.post(alma_url,headers=headers,params=payload,data=xml)
    response = r.content
  except:
    sys.stderr.write("Could not place API call to create set"+"\n")
  return response

## ADD MEMBERS TO SET
def add_members_to_set(alma_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'id_type':"BARCODE",'op':"add_members",'apikey':alma_apikey}
  try:
    r = requests.post(alma_url,headers=headers,params=payload,data=xml)
    response2 = r.content
  except:
    sys.stderr.write("Could not define add members to set"+"\n")
  return response2

## PREPARE FIRST JOB XML
def prepare_job1_xml(setids,xml):
  xml = xml.replace("\n", "")
  xml = xml.replace("{set_id}", setids)
  return xml

## RUN FIRST JOB
def job1(alma_job1_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'op':"run",'apikey':alma_apikey}
  try:
    r = requests.post(alma_job1_url,headers=headers,params=payload,data=xml)
    response3 = r.content
  except:
    sys.stderr.write("Could not define first job"+"\n")
  return response3

## PREPARE SECOND JOB XML
def prepare_job2_xml(setids,xml):
  xml = xml.replace("\n", "")
  xml = xml.replace("{set_id}", setids)
  return xml

## RUN SECOND JOB
def job2(alma_job2_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'op':"run",'apikey':alma_apikey}
  try:
    r = requests.post(alma_job2_url,headers=headers,params=payload,data=xml)
    response4 = r.content
  except:
    sys.stderr.write("Could not define second job"+"\n")
  return response4

## PREPARE THIRD JOB XML
def prepare_job3_xml(setids,xml):
  xml = xml.replace("\n", "")
  xml = xml.replace("{set_id}", setids)
  return xml

## RUN THIRD JOB
def job3(alma_job3_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'op':"run",'apikey':alma_apikey}
  try:
    r = requests.post(alma_job3_url,headers=headers,params=payload,data=xml)
    response5 = r.content
  except:
    sys.stderr.write("Could not define second job"+"\n")
  return response5
 
## PREPARE FOURTH JOB XML
def prepare_job4_xml(setids,xml):
  xml = xml.replace("\n", "")
  xml = xml.replace("{set_id}", setids)
  return xml

## RUN FOURTH JOB
def job4(alma_job4_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'op':"run",'apikey':alma_apikey}
  try:
    r = requests.post(alma_job4_url,headers=headers,params=payload,data=xml)
    response6 = r.content
  except:
    sys.stderr.write("Could not define first job"+"\n")
  return response6

## DELETE SET
def delete_set(alma_url,alma_apikey):
  payload = {'apikey':alma_apikey}
  try:
    r = requests.delete(alma_url,params=payload)
    delresponse = r.content
  except:
    sys.stderr.write("Could not place API call to delete set"+"\n")
  return delresponse


# DEFINE MAIN FUNCTION
def main():

## OPEN CONFIGURATION FILES
  try: 
    configurations = ("/sirsi/webserver/bin/stacks_jobs/files/job_keys_univ_90d.cfg")
    configfile = open(configurations, "r")
  except:
    sys.stderr.write("Could not open configuration file"+"\n")

## FOR EACH LINE IN THE CONFIGURATION FILE
  for line in configfile:

### STRIP OUT NEW LINE VALUES
    try:
      line = line.rstrip("\n")
    except:
      sys.stderr.write("Could not strip out new lines")

### SPLIT LINES AT EQUAL SIGN
    try:
      value = line.split("=")
    except:
      sys.stderr.write("Could not split lines at equal sign"+"\n")

### ASSIGN VALUES FROM ARRAY TO VARIABLES
    try:
      if value[0] == "analytics_url":
        analytics_url = value[1]
      elif value[0] == "alma_url":
        alma_url = value[1]
      elif value[0] == "analytics_apikey":
        analytics_apikey = value[1]
      elif value[0] == "alma_apikey":
        alma_apikey = value[1]
      elif value[0] == "path":
        path = value[1]
      elif value[0] == "alma_job1_url":
        alma_job1_url = value[1]
      elif value[0] == "alma_job2_url":
        alma_job2_url = value[1]
      elif value[0] == "alma_job3_url":
        alma_job3_url = value[1]
      elif value[0] == "alma_job4_url":
        alma_job4_url = value[1]
    except:
      sys.stderr.write("Could not assign values from array to variables"+"\n")

## OPEN SET XML
  try:
    set_xml = ("/sirsi/webserver/bin/stacks_jobs/files/set_univ_90d.xml")
    univloststoxl = open(set_xml, "r")
  except:
    sys.stderr.write("Could not open set xml"+"\n")

## CALL SECONDARY FUNCTION TO NEW VARIABLES
  try:
    response,url = get_lost_items(analytics_url,path,analytics_apikey)
  except:
    sys.stderr.write("Could not call secondary function to new variables"+"\n")
  try:
    barcode = get_barcode_from_xml(response)
  except:
    sys.stderr.write("Could not get barcode from xml"+"\n")
  try:
    content = create_set(alma_url,alma_apikey,univloststoxl)
  except:
    sys.stderr.write("Could not get content from create set"+"\n")
  try:
    setids = get_setid_from_content(content)
  except:
    sys.stderr.write("Could not get set id from content"+"\n")

## CREATE XML OF BARCODES
  barcode_xml = ""
  for line in barcode:
    barcode_xml += "<member><id>" + line + "</id></member>"
  members_xml = "<set><members>" + barcode_xml + "</members></set>"

## CALL SECONDARY FUNCTION TO PREPARE FINAL SET
  try:
    final_set = add_members_to_set(alma_url+"/"+setids,alma_apikey,members_xml)
  except:
    sys.stderr.write("Could not create final set"+"\n")

## DELAY TO ALLOW TIME FOR TO CREATE SET (in seconds)
  try:
    time.sleep(60)
  except:
    sys.stderr.write("Could not delay after creating final set"+"\n")


## OPEN FIRST JOB XML
  try:
    job1_xml = ("/sirsi/webserver/bin/stacks_jobs/files/job_univ_90d_1.xml")
    cancelrequests = open(job1_xml, "r")
    cancelrequests = cancelrequests.read()
  except:
    sys.stderr.write("Could not open first job xml"+"\n")
 
## CALL TO UPDATE FIRST JOB XML WITH SET ID FROM SET CREATED ABOVE
  try:
    job1_xml = prepare_job1_xml(setids,cancelrequests)
  except:
    sys.stderr.write("Could not update first job xml"+"\n")

## CALL SECONDARY FUNCTION TO RUN FIRST JOB
  try:
    run_job1 = job1(alma_job1_url,alma_apikey,job1_xml)
  except:
    sys.stderr.write("Could not run first job"+"\n")

## DELAY TO ALLOW TIME FOR FIRST JOB TO RUN IN ALMA (in seconds)
  try:
    time.sleep(60)
  except:
    sys.stderr.write("Could not delay after first job"+"\n")



## OPEN SECOND JOB XML
  try:
    job2_xml = ("/sirsi/webserver/bin/stacks_jobs/files/job_univ_90d_2.xml")
    changeitems = open(job2_xml, "r")
    changeitems = changeitems.read()
  except:
    sys.stderr.write("Could not open second job xml"+"\n")

## CALL TO UPDATE SECOND JOB XML WITH SET ID FROM SET CREATED ABOVE
  try:
    job2_xml = prepare_job2_xml(setids,changeitems)
  except:
    sys.stderr.write("Could not update second job xml"+"\n")

## CALL SECONDARY FUNCTION TO RUN SECOND JOB
  try:
    run_job2 = job2(alma_job2_url,alma_apikey,job2_xml)
  except:
    sys.stderr.write("Could not run second job"+"\n")

## DELAY TO ALLOW TIME FOR SECOND JOB TO RUN IN ALMA (in seconds)
  try:
    time.sleep(60)
  except:
    sys.stderr.write("Could not delay after second job"+"\n")


## OPEN THIRD JOB XML
  try:
    job3_xml = ("/sirsi/webserver/bin/stacks_jobs/files/job_univ_90d_3.xml")
    closelostloans = open(job3_xml, "r")
    closelostloans = closelostloans.read()
  except:
    sys.stderr.write("Could not open first job xml"+"\n")

## CALL TO UPDATE THIRD JOB XML WITH SET ID FROM SET CREATED ABOVE
  try:
    job3_xml = prepare_job3_xml(setids,closelostloans)
  except:
    sys.stderr.write("Could not update third job xml"+"\n")

## CALL SECONDARY FUNCTION TO RUN THIRD JOB
  try:
    run_job3 = job3(alma_job3_url,alma_apikey,job3_xml)
  except:
    sys.stderr.write("Could not run third job"+"\n")

## DELAY TO ALLOW TIME FOR THIRD JOB TO RUN IN ALMA (in seconds)
  try:
    time.sleep(60)
  except:
    sys.stderr.write("Could not delay after third job"+"\n")


## OPEN FOURTH JOB XML
  try:
    job4_xml = ("/sirsi/webserver/bin/stacks_jobs/files/job_univ_90d_4.xml")
    changeitemsagain = open(job4_xml, "r")
    changeitemsagain = changeitemsagain.read()
  except:
    sys.stderr.write("Could not open fourth job xml"+"\n")

## CALL TO UPDATE FOURTH JOB XML WITH SET ID FROM SET CREATED ABOVE
  try:
    job4_xml = prepare_job4_xml(setids,changeitemsagain)
  except:
    sys.stderr.write("Could not update fourth job xml"+"\n")

## CALL SECONDARY FUNCTION TO RUN FOURTH JOB
  try:
    run_job4 = job4(alma_job4_url,alma_apikey,job4_xml)
  except:
    sys.stderr.write("Could not run fourth job"+"\n")

## DELAY TO ALLOW TIME FOR FOURTH JOB TO RUN IN ALMA (in seconds)
  try:
    time.sleep(60)
  except:
    sys.stderr.write("Could not delay after fourth job"+"\n")


## CALL TO DELETE SET
  try:
    deleteset = delete_set(alma_url+"/"+setids,alma_apikey)
  except:
    sys.stderr.write("Could not delete set"+"\n")

## PRINT VARIABLES
#  print run_job1
#  print "\n"
#  print run_job2
#  print "\n"
#  print run_job3
#  print "\n"
#  print run_job4

## CLOSE FILES
  try:
    configfile.close()
  except:
    sys.stderr.write("Could not close configuration file"+"\n")
  try:
    univloststoxl.close()
  except:
    sys.stderr.write("Could not close set file"+"\n")

# EXIT SCRIPT
if __name__ == "__main__":
  sys.exit(main())
