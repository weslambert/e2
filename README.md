# alert2
Some (not optimal, but useable) python scriptage to assist with information gathering (from Google [GRR](https://github.com/google/grr)) upon an alert match from Yelp's [Elastalert](https://github.com/Yelp/elastalert).

`elastalert2grr.py` will query GRR for a relevant source or destination IP address, then gather the client URN and use that to automatically start a flow on said client.

Most testing has been performed alongside [Technology Preview 3](http://blog.securityonion.net/2017/07/towards-elastic-on-security-onion.html) of [Security Onion](https://securityonion.net) on the [Elastic](https://www.elastic.co/) Stack.

In such configuration, ElastAlert rules are stord in `/etc/elastalert/rules/`.

An example rule has been included in this repo that will query all indexes prefixed with `logstash-*` every minute for a user-supplied source IP address.  This example could also be modfied to match on destination address by modifying the following in `rule_example.yaml`.

    filter:
    - term:
        source_ip: 'SOURCE_IP_FOR_WHICH_YOU_WOULD_LIKE_TO_ALERT'
        
and
    
    alert:
    - "command"
    command: ["/YOUR_SCRIPT_DIRECTORY/elastalert2grr.py", "-s", "%(source_ip)s"]

You will also need to modify `elastalert2grr.py` to use the address and user/pass of a user able to authenticate to GRR.

Be default, configuration is as follows (based off of [officical GRR Docker Image](https://github.com/google/grr-doc/blob/master/docker.adoc)):

    grrserver = 'http://YOUR_SERVER_IP:8000'
    username = 'admin'
    password = 'demo' 

It is highly recommended to only use this user as an dedicated API user, separate from normal user accounts.

For Security Onion users,  simply place your example rule in `/etc/elastalert/rules` and reference the `elastalert2grr.py` script location in the above `command` line for the alert type.

You can then check `/var/log/elastalert/elastalert_stderr.log` and `/YOUR_LOG_DIRECTORY/elastalert2grr.log` to see if things are working as they should.


