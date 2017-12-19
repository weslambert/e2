# alert2

IN PROGRESS...

Some (not optimal, but useable) python scriptage to assist with information gathering (from Google [GRR](https://github.com/google/grr)) upon an alert match from Yelp's [Elastalert](https://github.com/Yelp/elastalert).

`e2grr.py` will query [GRR](https://github.com/google/grr) for a relevant source or destination IP address, then gather the client URN and use that to automatically start a flow on said client.

`e2hive_case.py` will create a case in [TheHive](https://github.com/CERT-BDF/TheHive), based on the `alert` and `message` field derived from matching alerts found through the use of an Elastalert rule file, `hive.yaml`.

An example rule (for GRR) has been included in this repo that will query all indexes prefixed with `logstash-*` every minute for a user-supplied source IP address.  This example could also be modfied to match on destination address by modifying the following in `rule_example.yaml`.

    filter:
    - term:
        source_ip: 'SOURCE_IP_FOR_WHICH_YOU_WOULD_LIKE_TO_ALERT'
        
and
    
    alert:
    - "command"
    command: ["/YOUR_SCRIPT_DIRECTORY/elastalert2grr.py", "-s", "%(source_ip)s"]

You will also need to modify `e2grr.py` to use the address and user/pass of a user able to authenticate to GRR.

Be default, configuration is as follows (based off of [officical GRR Docker Image](https://github.com/google/grr-doc/blob/master/docker.adoc)):

    grrserver = 'http://YOUR_SERVER_IP:8000'
    username = 'admin'
    password = 'demo' 

It is highly recommended to only use this user as an dedicated API user, separate from normal user accounts.

For Security Onion users,  simply place your example rule in `/etc/elastalert/rules` and reference the `elastalert2grr.py` script location in the above `command` line for the alert type.

You can then check `/var/log/elastalert/elastalert_stderr.log` and `/YOUR_LOG_DIRECTORY/elastalert2grr.log` to see if things are working as they should.


