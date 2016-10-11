#!/usr/bin/python
import base64, json, logging, MySQLdb, os, re, requests, socket, struct, sys, urllib2
from requests.auth import HTTPBasicAuth

logging.basicConfig(filename='/var/log/fir_incident.log',level=logging.DEBUG)

sig_list = []

db = MySQLdb.connect (host="localhost",
                     user="sguil",
                     passwd="password",
                     db="securityonion_db")
cur = db.cursor()

cur.execute("select distinct signature from event where status = '0' and priority = '1' and event.signature_gen != 10001 and event.signature_id != 420042 and event.timestamp>date_sub(now(), INTERVAL 1 MINUTE);")

db.close()

for row in cur.fetchall():
    signature = row[0]
    sig_list.append(signature)
    
for i in sig_list:
 db = MySQLdb.connect (host="localhost",
                      user="sguil",
                      passwd="password",
                      db="securityonion_db")

 cur = db.cursor()
 cur.execute("select timestamp from event where signature = '%s' and status = '0' and priority = '1' and event.signature_gen != 10001 and event.signature_id != 420042 and event.timestamp>date_sub(now(), INTERVAL 1 MINUTE) order by timestamp limit 1;" %(i))
 for row in cur.fetchall():
    date = row [0]
 cur.execute("select distinct src_ip,dst_ip from event where signature = '%s' and status = '0' and priority = '1' and event.signature_gen != 10001 and event.signature_id != 420042 and event.timestamp>date_sub(now(), INTERVAL 1 MINUTE);" %(i))
 for row in cur.fetchall():
    body_data = []
    src_ip = socket.inet_ntoa(struct.pack('!L',row[0]))
    dst_ip = socket.inet_ntoa(struct.pack('!L',row[1]))
    body_data.append(src_ip)
    body_data.append(dst_ip)
 db.close()
 fir = "https://local-fir-server.com/api/incidents"

 headers = {
   'Authorization' : 'Token <token>',
   'Content-type' : 'application/json'
 }

 response = requests.get(fir, headers=headers, verify=False)
 #print response.content

 data = {

    "actor" : "3",
    "category": "3",
    "confidentiality": "1",
    "description": body_data,
    "detection": "2",
    "plan" : "8",
    "severity": "2",
    "subject": i
 }
 response = requests.post(fir, headers=headers, data=json.dumps(data), verify=False)
 #print response.content
 #logging.warning(response.content)
