# Site24x7 Availability Dashboard
This project will allow you to grab Availability percentage from your Site24x7 account via their API and present it via a web interface for you to display on a wallboard.

### What's needed.
This script uses the Site24x7 API to gather the needed information, you will need an AUTH Token. To get an Auth Token, log into your Site24x7 account then go to this URL:
https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api

### Getting it done
I won't go into how to setup your server with a web server to allow CGI to run but you will need to get this done to use this script.

Once you get the server setup properly, drop this script and css file into the /var/www directory or wherever your web root directory is located.

#### Important Note
* Ensure the script is execuable.
* The page layout is fluid.

####Screenshot
![availability-dashboard](https://raw.githubusercontent.com/Computero/Monitoring/master/Site24x7/availability-dashboard/Availability-Dashboard.png?raw=true "Availability Dashboard")

**ps**: _The screenshot shows 99.97 and above as normal and below 99.95 as critical, the reason being that initially I had 99.95 to 99.96 as warning but ended up removing it and I forgot to update the dashboard with the proper numbers. The script has been properly updated however. I did not want to take another screenshot and go through another commit just for that._
