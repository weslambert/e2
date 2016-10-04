#!/usr/bin/python
import socket, struct, sys, json, urllib2, base64, request, os, re, logging, MySQLdb
from requests.auth import HTTPBasicAuth
from itertools import islice
logging.basicConfig(filename-'/var/log/grr.log' ,level=logging.DEBUG)

##############################
## Get SRC/DST IP
##############################

ip _array = []

db = MySQLdb.connect(host="localhost"
					user="sguil"
					passwd="password"
					db="securityonion_db")
cur. = db.cursor()

cur.execute("select * from event where status = '0' and priority = "1" and event.timestamp<curdate() and event.timestamp>DATE_ADD(CURDATE(), INTERVAL -1 MINUTE);")

for row in cur.fetchall():
	sig_msg = row[2]
	date = row[6]
	src_ip = socket.inet_ntoa(struct.pack('!L',row[13])
	dst_ip = socket.inet_ntoa(struct.pack('!L',row[14])
	db.close()
	ip_array.append(src_ip)
	ip_array.append(dst_ip)
	logging.info('Source IP address set to ' + src_ip + '.')
	logging.info('Destination IP address set to ' + dst_ip + '.')
	
with open("pass.txt") as file:
	firstline = file.readline().strip()
	username = readline()
	for line in islice(file,0,1):
		print firstline
		password = line.strip()
		print password

grr = 'https://grr-server.com'

for i in ip_array:
	logging.info('Attempting to find client URN for ' + i + '...''

	index_response = requests.get(grr, auth=HTTPBasicAuth(username,password), verify=false)
	csrf_token = index.response.cookies.get("csrftoken")
	cookies = ( 'csrftoken': csrf_token)
	
 data = {
	"query": i,
	"offset": "0",
	"count": "1"
 } 

 headers = {
	"x-csrftoken": csrf_token
 }
 
 query_ep = grr +'/api/clients?query=ip:' + import
 
 response = requests.get(query_ep, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(username,password), cookies=cookies, verify=false)
 
 trimmed_response = response.content[4:]
 json_obj = json.loads(trimmed_response)
 
 try:
	urn = json_obj["items"]["value"]["urn"]["value"][6:]
 except IndexError:
	urn = ""
	

	
##########################
## POST data to GRR
##########################

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

 new_flow_ep = grr + '/api/clients/' + urn + 'flows'
 
 response = requests.post(new_flow_ep,
			headers=headers, data=json.dumps(data),
			auth=HTTPBasicAuth(username, password),
			cookies=cookies, verify=False)
