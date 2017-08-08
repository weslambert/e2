#!/user/bin/python
# Format data for generating request to GRR to interrogate a particular client
import json, urllib2, base64, requests
from requests.auth import HTTPBasicAuth
def interrogate(clientid,grrserver,headers,cookies,username,password):
  data = {
         "client_id": clientid
      }

  response = requests.post(grrserver + "/api/clients/" + clientid + "/actions/interrogate",
                           headers=headers, data=json.dumps(data),
                           cookies=cookies, auth=HTTPBasicAuth(username, password))
  print response.content.lstrip(")]}'")

