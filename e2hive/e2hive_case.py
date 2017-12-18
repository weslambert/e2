#!/usr/bin/python
# Modified from script by Keith Taylor, found here:
# http://informationonsecurity.blogspot.com/2015/10/automating-forensic-artifact-collection.html
import json, urllib2, base64, requests
import requests
import argparse
import sys
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('/etc/elastalert/rules/e2hive.conf')

url = parser.get('config', 'url')
apikey = parser.get('config', 'apikey')

sys.stdout = open('/tmp/e2hive.log', 'w')

parser = argparse.ArgumentParser(description='Post a case to the Hive')
parser.add_argument('-t','--title', help='Input file name',required=True)
parser.add_argument('-d','--description',help='Output file name', required=False)
args = parser.parse_args()

title = args.title
description = args.description 

authheader =  "Bearer " + apikey
headers = {
    "Authorization": authheader,
    "Content-Type": "application/json"
}

data = {
  "title": title,
  "description": description
}

response = requests.post(url + "/api/case",
                          headers=headers, data=json.dumps(data)
			)
print response.content
