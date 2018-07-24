# Last Quarter Availability Dashboard
This project will allow you to grab Last Quarter Availability percentage from your Site24x7 account via their API and present it via a web interface for you to display on a wallboard.

### What's needed.
This script uses the Site24x7 API to gather the needed information, you will need an AUTH Token. To get an Auth Token, log into your Site24x7 account then go to this URL:
https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api

### Getting it done
I won't go into how to setup your server with a web server to allow web files to run but you will need to get this done to use this script.

Once you get the server setup properly, drop this script and css file into the /var/www directory or wherever your web root directory is located.

#### Of Note
* Ensure the script remains executable. If needed, run `chmod +x generate_report.py` in a terminal.
* The page layout is fluid.

#### Screenshot
![lastq-availability-dashboard](https://github.com/Computero/Monitoring/blob/master/Site24x7/LastQuarterAvailability/LastQuarterScreenshot.png?raw=true "Last Quarter Availability Dashboard")
