#!/usr/bin/python
import base64, json, logging, os, re, requests, socket, struct, sys, urllib2
from requests.auth import HTTPBasicAuth
import argparse
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('/etc/elastalert/rules/e2fir.conf')
#parser.read('/etc/elastalert/rules/e2hive.conf')

url = parser.get('config', 'url')
token = parser.get('config', 'token')

logging.basicConfig(filename='/tmp/fir_incident.log',level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Post an event to FIR')
parser.add_argument('-a','--actor', help='Actor',required=False)
parser.add_argument('-c','--category',help='Category', required=False)
parser.add_argument('-l','--confidentiality',help='Confidentiality', required=False)
parser.add_argument('-d','--description', help='Description',required=True)
parser.add_argument('-t','--detection',help='Detection', required=False)
parser.add_argument('-p','--plan',help='Plan', required=False)
parser.add_argument('-s','--severity',help='Severity', required=False)
parser.add_argument('-j','--subject',help='Subject', required=True)

args = parser.parse_args()

actor = args.actor
category = args.category
confidentiality = args.confidentiality
description = args.description
detection = args.detection
plan = args.plan
severity = args.severity
subject = args.subject


headers = {
  'Authorization' : 'Token ' + token,
  'Content-type' : 'application/json'
}

response = requests.get(url, headers=headers, verify=False)
#print response.content
data = {
   "actor" : actor,
   "category": category,
   "confidentiality": confidentiality,
   "description": description,
   "detection": detection,
   "plan" : plan,
   "severity": severity,
   "subject": subject
}
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
print response.content
#logging.warning(response.content)
