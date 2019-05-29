#!/opt/rh/python27/root/usr/bin/python
"""
   This script deletes expired Georgia Tech patrons from Alma, as determined by an Alma Analytics report
"""
__author__= 'Lisa Hamlett'
__date__ = 'May 2019'

import sys
import requests
import xml.etree.ElementTree as ET

# DEFINE SECONDARY FUNCTIONS FOR USE BY MAIN FUNCTION

## GET ANALYTICS REPORT
def analytics_report(analytics_url,path,analytics_apikey):
  payload = {'apikey':analytics_apikey, 'path':path}
  try:
    r = requests.get(analytics_url,params=payload)
    response = r.content
    url = r.url
  except:
    sys.stderr.write("Could not get analytics report"+"\n")
  return r

## GET USER IDENTIFIERS FROM ANALYTICS REPORT
def userids(xml):
  xml = xml.replace("\n", "")
  xml = xml.replace(' xmlns="urn:schemas-microsoft-com:xml-analysis:rowset"', "")
  tree = ET.fromstring(xml)

  userid = ""
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
          userid = row.find("Column1")
          userid = str(userid.text)
        except:
          sys.stderr.write("Could not find userid"+"\n")
        parsed_xml.append(userid)
    else:
      sys.stderr.write("No items found"+"\n")
      return "Fail"
  except:
    sys.stderr.write("Could not find rows"+"\n")
  return parsed_xml

## GET DELETE USER API LINK
def delete_user_api(alma_api_url,user_id_type,alma_apikey):
  payload = {'user_id_type':user_id_type, 'apikey':alma_apikey}
  try:
    r = requests.delete(alma_api_url,params=payload)
    response = r.content
    url = r.url
  except:
    sys.stderr.write("Could not get delete user api link"+"\n")
  return r

# DEFINE MAIN FUNCTION
def main():

## OPEN CONFIGURATION FILES
  try:
    configurations = ("job_keys_delete_gt.cfg")
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
      elif value[0] == "path":
        path = value[1]
      elif value[0] == "analytics_apikey":
        analytics_apikey = value[1]
      elif value[0] == "alma_api_url":
        alma_api_url = value[1]
      elif value[0] == "alma_apikey":
        alma_apikey = value[1]
      elif value[0] == "user_id_type":
        user_id_type = value[1]
    except:
      sys.stderr.write("Could not assign values from array to variables"+"\n")

## CALL ANALYTICS FOR REPORT XML
  try:
    result = analytics_report(analytics_url,path,analytics_apikey)
  except:
    sys.stderr.write("Could not call analytics for report XML"+"\n")

## PARSE ANALYTICS REPORT XML
  try:
    users = userids(result.content)
  except:
    sys.stderr.write("Could not call analytics for report XML"+"\n")

## PARSE USERS FROM XML, CREATES LINK, AND DELETES USERS
  try:
    for user in users:
      try:
        alma_api_url_test = alma_api_url.replace("USERID",str(user))
      except:
        sys.stderr.write("Could not replace USERID with users in alma_api_url"+"\n")
      try:
        deleted = delete_user_api(alma_api_url_test,user_id_type,alma_apikey)
      except:
        sys.stderr.write("Could not delete users"+"\n")
  except:
    sys.stderr.write("Count not parse users from XML"+"\n")

## CLOSE FILES
  try:
    configfile.close()
  except:
    sys.stderr.write("Could not close configuration file"+"\n")

# EXIT SCRIPT
if __name__ == "__main__":
  sys.exit(main())
