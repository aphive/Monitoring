# Last Quarter Availability Dashboard
This project will allow you to grab Last Quarter Availability percentage from your Site24x7 account via their API and present it via a web interface for you to display on a wallboard.

### What's needed.
This script uses the Site24x7 API to gather the needed information, you will need an AUTH Token. To get an Auth Token, log into your Site24x7 account then go to this URL:
https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api

### Getting it done
I won't go into how to setup your server with a web server to allow web files to run but you will need to get this done to use this script.

Once you get the server setup properly, drop `generate_report.py` and `style.css` into `/var/www/<directory name>` or wherever your web root directory is located.

### Automating the generation
The `generate_report.py` script should be run by cron job on the 4th of the month after a quarter ends to produce and update the page content from Site24x7 under the user that owns `/var/www`
#### Add a crontab entry as follows:
`0 0 4 1,4,7,10 * cd /var/www/<directory name>; ./generate_report.py > index.html.new 2>generate_failures.log; mv -f index.html.new index.html`

#### Example Runs
```
next at 2018-10-04 00:00:00
then at 2019-01-04 00:00:00
then at 2019-04-04 00:00:00
then at 2019-07-04 00:00:00
then at 2019-10-04 00:00:00
```

#### Of Note
* Ensure the script remains executable. If needed, run `chmod +x generate_report.py` in a terminal.
* The page layout is fluid.

#### Screenshot
![lastq-availability-dashboard](https://github.com/Computero/Monitoring/blob/master/Site24x7/LastQuarterAvailability/LastQuarterScreenshot.png?raw=true "Last Quarter Availability Dashboard")
