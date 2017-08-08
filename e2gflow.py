#!/user/bin/python
# Format data for generating request to GRR to interrogate a particular client
import json, urllib2, base64, requests
from requests.auth import HTTPBasicAuth
def flow(clientid,name,grrserver,headers,cookies,username,password):
  data = {
    "flow": {
     #"args": {
     #  "fetch_binaries": True,
     #  "filename_regex": "."
    #},
    "name": name,
    "runner_args": {
      "notify_to_user": False,
      "output_plugins": [],
      "priority": "HIGH_PRIORITY"
    }
  }
	}

  response = requests.post(grrserver + "/api/clients/" + clientid + "/flows",
                           headers=headers, data=json.dumps(data),
                           cookies=cookies, auth=HTTPBasicAuth(username, password))
  print response.content.lstrip(")]}'")

