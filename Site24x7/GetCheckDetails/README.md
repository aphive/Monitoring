# Get Check Details
Use this script to gather needed data to be used with the Availability Dashboard package or just to get data pertinent to your account.

**NOTE**:
    This will only generate output for DNS, PING and URL checks. If you want to expand further; you will need to get the actual check type
	as used in Site24x7 as well as add a new output section at the end of the script to output the data.

## What's needed.
This script uses the Site24x7 API to gather the needed information, you will need an AUTH Token. To get an Auth Token, log into your Site24x7 account then go to this URL:
https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api

This script will scrape your Site24x7 account and list the checks, monitor_id and other details.

For URL checks the raw output will look like this:

```json
{
    "code": 0,
    "data": [
        {
            "check_frequency": "10",
            "display_name": "Check Name",
            "http_method": "H",
            "isServerIntegrated": false,
            "location_profile_id": "000000000000000000",
            "match_case": false,
            "monitor_id": "000000000000000000",
            "notification_profile_id": "000000000000000000",
            "probeProxyEnabled": false,
            "state": 0,
            "threshold_profile_id": "000000000000000000",
            "timeout": 30,
            "type": "URL",
            "use_ipv6": false,
            "use_name_server": false,
            "user_group_ids": [
                "000000000000000000"
            ],
            "website": "https://domain.com"
        },
    ],
    "message": "success"
}
```

## Usage
To use it to get your URL monitors, just run `./listmonitors.py -t url`

* Change url to the appropriate type ( dns   ping   url )

The output will look like this:

```URL:    name:    Wesite-Name    mon_id:    113770000025720011    url:    https://www.website.com/```
