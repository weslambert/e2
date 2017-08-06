#!/usr/bin/python
# Modified from script by Keith Taylor, found here:
# http://informationonsecurity.blogspot.com/2015/10/automating-forensic-artifact-collection.html
import json, urllib2, base64, requests
from requests.auth import HTTPBasicAuth
import argparse
import sys

sys.stdout = open('/YOUR_LOG_DIRECTORY/grr-test.log', 'w')

parser = argparse.ArgumentParser(description='This script will query GRR for a client ID for the source and destination IP of machines found in an alert')
parser.add_argument('-s','--source_ip', help='Input file name',required=True)
parser.add_argument('-d','--dest_ip',help='Output file name', required=False)
args = parser.parse_args()

grrserver = 'http://YOUR_SERVER_IP:8000'
username = 'admin'
password = 'demo'
source_ip = args.source_ip 
#clientid = 'YOUR_CLIENT_ID'

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
authheader =  "Basic %s" % base64string

index_response = requests.get(grrserver, auth=HTTPBasicAuth(username, password))

csrf_token = index_response.cookies.get("csrftoken")

headers = {
    "Authorization": authheader,
    "x-csrftoken": csrf_token,
    "x-requested-with": "XMLHttpRequest"
    }

cookies = {
    "csrftoken": csrf_token
    }

# Query for GRR client and grab client ID
response = requests.get(grrserver + "/api/clients?query=" + source_ip,
                         headers=headers,
                         cookies=cookies, auth=HTTPBasicAuth(username, password))

print "Source IP:"
print source_ip

result = response.content.lstrip(")]}'")
fin_result = json.loads(result)
clientid = fin_result["items"][0]["value"]["urn"]["value"].lstrip("aff4:/")

print "Found client URN:"
print clientid

# Format data for generating request to GRR to interrogate a particular client
data = {
       "client_id": clientid
    }

response = requests.post(grrserver + "/api/clients/" + clientid + "/actions/interrogate",
                         headers=headers, data=json.dumps(data),
			 cookies=cookies, auth=HTTPBasicAuth(username, password))
print response.content.lstrip(")]}'")
  
