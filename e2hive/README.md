Prerequisites:

Security Onion (installed, configured)    
TheHive (and API Key)

- Clone the repo:   
`git clone https://github.com/weslambert/e2`  

- Copy files into place:   
`sudo cp e2/e2hive/* /etc/elastalert/rules`    

- Modify config files:    
Modify `/etc/elastalert/rules/hive.yaml` to contain the alert you would like to send to TheHive.     
Modify `/etc/elastalert/rules/e2hive.conf` to contain the url for TheHive and an API Key.    
