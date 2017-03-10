# Get Check Details
Use this script to gather needed data to be used with the Availability Dashboard package or just to get data pertinent to your account.

## What's needed.
This script uses the Site24x7 API to gather the needed information, you will need an AUTH Token. To get an Auth Token, log into your Site24x7 account then go to this URL:
https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api

This script will scrape your Site24x7 account and list the checks, monitor_id and other details.

For URL checks the raw output will look like this:

`{
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
}`

In this excerpt we would be pulling the following `display_name` , `monitor_id` and `website` so that we can get a printout like: `Check Name 000000000000000000  https://domain.com`
