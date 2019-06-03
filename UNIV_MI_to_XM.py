#!/opt/rh/python27/root/usr/bin/python
"""
   This script changes missing UNIV items to the UNIV XM location, as determined by an Alma Analytics report
"""
__author__= 'Lisa Hamlett'
__date__ = 'May 2019'

import sys
import requests
import xml.etree.ElementTree as ET
import time

# DEFINE SECONDARY FUNCTIONS FOR USE BY MAIN FUNCTION

## GET ANALYTICS REPORT
def get_analytics_report(analytics_url,path,analytics_apikey):
  payload = {'path':path, 'apikey':analytics_apikey}
  r = requests.get(analytics_url,params=payload)
  response = r.content
  url = r.url
  return response,url

## GET BARCODES FROM ANALYTICS REPORT
def get_barcodes(xml):
  xml = xml.replace("\n", "")
  xml = xml.replace(' xmlns="urn:schemas-microsoft-com:xml-analysis:rowset"', "")
  tree = ET.fromstring(xml)

  barcode = ""
  parsed_xml = []
  rowset = tree.find("QueryResult/ResultXml/rowset")
  rows = rowset.findall("Row")
  if rows != None:
    for row in rows:
      barcode = row.find("Column1")
      barcode = str(barcode.text)
      parsed_xml.append(barcode)
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
def create_set(alma_api_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'apikey':alma_apikey}
  r = requests.post(alma_api_url,headers=headers,params=payload,data=xml)
  response = r.content
  return response

## ADD MEMBERS TO SET
def add_members_to_set(alma_api_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'id_type':"BARCODE",'op':"add_members",'apikey':alma_apikey}
  try:
    r = requests.post(alma_api_url,headers=headers,params=payload,data=xml)
    response2 = r.content
  except:
    sys.stderr.write("Could not define add members to set"+"\n")
  return response2

## PREPARE JOB XML
def prepare_job_xml(setids,xml):
  xml = xml.replace("\n", "")
  xml = xml.replace("{set_id}", setids)
  return xml

## RUN JOB
def job(alma_job_url,alma_apikey,xml):
  headers = {'Content-Type':'application/xml'}
  payload = {'op':"run",'apikey':alma_apikey}
  r = requests.post(alma_job_url,headers=headers,params=payload,data=xml)
  response3 = r.content
  return response3

## DELETE SET
def delete_set(alma_api_url,alma_apikey):
  payload = {'apikey':alma_apikey}
  try:
    r = requests.delete(alma_api_url,params=payload)
    delresponse = r.content
  except:
    sys.stderr.write("Could not place API call to delete set"+"\n")
  return delresponse

# DEFINE MAIN FUNCTION
def main():

## OPEN CONFIGURATION FILE AND FOR EACH LINE IN THE CONFIGURATION FILE, STRIP OUT NEW LINE VALUES, SPLIT LINES AT EQUAL SIGN, AND ASSIGN VALUES FROM ARRAY TO VARIABLE
  configurations = ("job_keys_UNIV_MI_to_XM.cfg")
  configfile = open(configurations, "r")

  for line in configfile:
    line = line.rstrip("\n")
    value = line.split("=")
    if value[0] == "analytics_url":
      analytics_url = value[1]
    elif value[0] == "path":
      path = value[1]
    elif value[0] == "analytics_apikey":
      analytics_apikey = value[1]
    elif value[0] == "alma_api_url":
      alma_api_url = value[1]
    elif value[0] == "alma_apikey":
      alma_apikey = value[1]
    elif value[0] == "alma_job_url":
      alma_job_url = value[1]

## OPEN SET XML
  set_xml = ("set_UNIV_MI_to_XM.xml")
  univmitoxm = open(set_xml, "r")

## CALL SECONDARY FUNCTION TO NEW VARIABLES
  response,url = get_analytics_report(analytics_url,path,analytics_apikey)
  barcode = get_barcodes(response)
  content = create_set(alma_api_url,alma_apikey,univmitoxm)
  setids = get_setid_from_content(content)

## CREATE XML OF BARCODES
  barcode_xml = ""
  for line in barcode:
    barcode_xml += "<member><id>" + line + "</id></member>"
    members_xml = "<set><members>" + barcode_xml + "</members></set>"

## CALL SECONDARY FUNCTION TO PREPARE FINAL SET
  try:
    final_set = add_members_to_set(alma_api_url+"/"+setids,alma_apikey,members_xml)
  except:
    sys.stderr.write("Could not create final set"+"\n")

## OPEN JOB XML
  job_xml = ("job_xml_UNIV_MI_to_XM.xml")
  processitems = open(job_xml, "r")
  processitems = processitems.read()
 
## CALL TO UPDATE JOB XML WITH SET ID FROM SET CREATED ABOVE
  job_xml = prepare_job_xml(setids,processitems)

## CALL SECONDARY FUNCTION TO RUN JOB
  run_job = job(alma_job_url,alma_apikey,job_xml)

## DELAY TO ALLOW TIME FOR JOB TO RUN IN ALMA (in seconds)
  time.sleep(60)

## CALL TO DELETE SET
  try:
    deleteset = delete_set(alma_api_url+"/"+setids,alma_apikey)
  except:
    sys.stderr.write("Could not delete set"+"\n")

## CLOSE FILES
  configfile.close()
  univmitoxm.close()

# EXIT SCRIPT
if __name__ == "__main__":
  sys.exit(main())
