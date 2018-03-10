# e2fir

`e2fir.py` will create a case in [FIR](https://github.com/certsocietegenerale/FIR), based on the `alert` and `message` field derived from matching alerts found through the use of an Elastalert rule file, `fir.yaml`.

If running Security Onion, you'll want to put these files in `/etc/elastalert/rules`

Configuration information can be found in `e2fir.conf`.  This is includes:   
- `url` of FIR instance
- `apikey` for user performing request to FIR

The default path for `e2fir.conf` is set to `/etc/elastalert/rules/e2fir.conf`.  If putting in a different directory, you'll want to modify this path in `e2fir.py`.

Options in `fir.yaml` can be modified to change the type of information for which we are searching and/or sending to FIR.

Currently the rule file will search for any IDS event in Elasticseach (`event_type:snort`) for the last minute.  This is used for testing purposes and is not intended to be used in production.  You will likely want to specify more specific search criteria to ensure you are inserting data in to FIR that really matters.
