#!/usr/bin/python
import sys, struct, json, urllib2, base64, requests, os, re, logging, socket, MySQLdb
from requests.auth import HTTPBasicAuth

logging.basicConfig(filename='/var/log/fir_incident.log',level=logging.DEBUG)

############################
## Get SRC\DST IP
#############################

ip_array = []

db = MySQLdb.connect(host="localhost",
                     user="sguil",
                     passwd="password",
                     db="securityonion_db")

cur = db.cursor()

# Get all events (within the last minute) from securityonion_db where uncategorized and priority of "1"
cur.execute("select * FROM event where status = '0' and priority = '1' and event.timestamp<curdate() and event.timestamp>DATE_ADD(CURDATE(), INTERVAL -1 MINUTE);")

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


fir = "https://fir-server.com/api/incidents"

headers = {
   'Authorization' : '<individual_user_token>',
   'Content-type' : 'application/json'
}

#response = requests.get(fir, headers=headers, verify=False)
#print response.content

data = {

    "actor" : "3",
    "category": "3",
    "confidentiality": "1",
    "description": "This is a test ticket created by the API. SRCIP: " + src_ip ,
    "detection": "2",
    "plan" : "8",
    "severity": "2",
    "subject": sig_msg
}

response = requests.post(fir,
         headers=headers, data=json.dumps(data), verify=False)
print response.content
logging.warning(response.content)
