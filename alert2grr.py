#!/usr/bin/python
import socket, struct, sys, json, urllib2, base64, requests, os, re, logging, MySQLdb
from requests.auth import HTTPBasicAuth
from itertools import islice

logging.basicConfig(filename='/var/log/grr_flow.log',level=logging.DEBUG)


#############################
## Get SRC\DST IP
#############################

ip_array = []

db = MySQLdb.connect(host="localhost",
                     user="sguil",
                     passwd="password",
                     db="securityonion_db")

cur = db.cursor()

# Get all events (within the last minute) from securityonion_db where uncategorized and priority of "1"
cur.execute("select * FROM event where status = '1' and priority = '1' and event.timestamp<curdate() and event.timestamp>DATE_ADD(CURDATE(), INTERVAL -5 DAY);")

# Get alert values
for row in cur.fetchall():
    sig_msg = row[2]
    date = row[6]
    src_ip = socket.inet_ntoa(struct.pack('!L',row[13]))
    dst_ip = socket.inet_ntoa(struct.pack('!L',row[14]))
    db.close()
    ip_array.append(src_ip)
    ip_array.append(dst_ip)
    logging.info('Source IP address set to ' + src_ip + '.')
    logging.info('Destination IP address set to ' + dst_ip + '.')

#############################
## Credentials 
#############################

with open("pass.txt", "r") as file:
        firstline = file.readline().strip()
        username = firstline
        for line in islice(file, 0,1):
                password = line.strip()

				
grr = 'https://grr-server.com'

#############################
## Get client URN from GRR
#############################

for i in ip_array:
 print "Attempting to find client URN for " + i + "..."
 logging.info('Attempting to find client URN for ' + i + '...')

 index_response = requests.get(grr, auth=HTTPBasicAuth(username, password), verify=False)
 csrf_token = index_response.cookies.get("csrftoken")
 cookies = { 'csrftoken': csrf_token }

 data = {
   "query" : i,
   "offset" : "0",
   "count" : "1"
 }

 headers = {
   "x-csrftoken": csrf_token
 }

 query_ep = grr + '/api/clients?query=ip:' + i

 response = requests.get(query_ep , headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(username, password), cookies=cookies, verify=False)
 print "Status Code:"
 print  response.status_code

 trimmed_response = response.content[4:]
 json_obj = json.loads(trimmed_response)
 
 try:
   urn = json_obj["items"][0]["value"]["urn"]["value"][6:]
   print "Found URN (" + urn + ") for " + i + "." 
 except IndexError:
   urn = ""
   print "Could not find a client URN for the specified IP address."

 ##########################
 ## POST data to GRR
 #########################

 data = {
  "flow": {
    "args": {
    },
    "name": "ListProcesses",
    "runner_args": {
      "output_plugins": [],
    }
  }
 }

 new_flow_ep = grr + "/api/clients/" + urn + "flows"
 
 response = requests.post(new_flow_ep,
         headers=headers, data=json.dumps(data),
         auth=HTTPBasicAuth(username, password),
         cookies=cookies, verify=False)
