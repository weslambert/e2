# e2misp

`misp.yaml` will allow you to use the existing [PyMISP](https://github.com/MISP/PyMISP) library and example scripts, and is currently setup to create an event using `create_events.py` or any other script provided by the great folks at [The MISP Project](https://github.com/MISP).

For Security Onion users, this rule file should be placed in `/etc/elastalert/rules/`

We can download/install the PyMISP library and examples scripts as follows:

    sudo apt-get install python3-pip
    sudo pip3 install pymisp
    cd /etc/elastalert/rules
    git clone https://github.com/MISP/PyMISP.git && cd PyMISP
    git submodule update --init
    sudo pip3 install -I .

We'll need to specify our `url`, and `apikey` to be used to insert events and/or make updates to our MISP instance:

    cd /etc/elastalert/rules/PyMISP/examples
    cp keys.py.sample keys.py
    vi keys.py

Next, we need to specify the path for PyMISP in each MISP python example script (adding at the top) to ensure that we can load the appropriate modules when Elastalert is executing the rule.  

For example, in `/etc/elastalert/rules/PyMISP/examples/create_events.py`, we might add:

    import sys
    sys.path.append('/etc/elastalert/rules/PyMISP')
    
Finally, we can modify our search criteria and script parameters in `/etc/elastalert/rules/misp.yaml`.
