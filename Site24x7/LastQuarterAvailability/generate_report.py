#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###############################################################################
#        Name: generate_report.py
# Description: Display Last Quartey Availability data in a dashboard format.
#      Author: Computero
#        Date: July/2018
#     Version: 1.0.0
###############################################################################

# Imports
import json
import pycurl
import time
from datetime import datetime
from datetime import timedelta
from io import BytesIO

# Get the Dates
current_date=datetime.now()
lastQuarter = (current_date.month - 1) / 3
dtFirstDay = datetime(current_date.year, 3 * lastQuarter - 2, 1)
startDate = dtFirstDay.strftime('%Y-%m-%d')
dtLastDay = datetime(current_date.year, 3 * lastQuarter + 1, 1) + timedelta(days=-1)
endDate = dtLastDay.strftime('%Y-%m-%d')

# Group Names as they are in Site24x7
groups = ['Group1', 'Group2', 'Group3']

# Define how to connect to Site24x7 API
def connectSite247(method, url):
    c = pycurl.Curl()
    connectReturn = BytesIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, ["Authorization: Zoho-authtoken a12345b6c8de901f2gh3456ij78k901l"])
    c.setopt(c.WRITEFUNCTION, connectReturn.write)
    c.setopt (pycurl.CUSTOMREQUEST, method)
    c.perform()
    c.close()
    connectOutput = connectReturn.getvalue()
    return connectOutput

returned_monitors = {}

# Putting it all together
print """<html>
<head>
<title>Last Quarter Availability Dashboard</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
<link rel="stylesheet" href="style.css">
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/JavaScript">
<!--
function TimedRefresh( t ) {
setTimeout("location.reload(true);", t);
}
//   -->
</script>
</head>
<body>
<header><!-- START HEADER -->
<h1>Last Quarter Availability Dashboard</h1>
</header><!-- END HEADER -->
<p>Thresholds: Above 99.95 = <span class="normal thresh">Normal</span> | Below 99.95 = <span class="critical thresh">Critical</span></p>
<div class="container"><!-- START CONTAINER -->"""

for group in groups:
    req_url = 'https://www.site24x7.com/api/monitor_groups'
    listOfMonitors = json.loads(connectSite247('GET', req_url))
    monitors = []
    for i in listOfMonitors['data']:
        if i['display_name'] == group:
            items = i['monitors']
            for item in items:
                monitors.append(item)

    returned_monitors = {}

    for monitor in monitors:
        base_url = 'https://www.site24x7.com/api/reports/summary/'
        putData = monitor + '?period=50&start_date=' + startDate + '&end_date=' + endDate
        req_url = base_url + putData
        listOfAvail = json.loads(connectSite247('GET', req_url))
        returned_monitors[monitor] = listOfAvail
        name = listOfAvail['data']['info']['resource_name']
        avail_pct = listOfAvail['data']['summary_details']['availability_percentage']

        if avail_pct >= 99.95: # Normal
            print '<div class="column">'
            print '<div class="group">'
            print '<div class="skillbar clearfix" data-percent="%s%%">' % (avail_pct)
            print '<div class="skillbar-title"><span>%s</span></div>' % (name)
            print '<div class="skillbar-bar normal"></div>'
            print '<div class="skill-bar-percent">%s%%</div>' % (avail_pct)
            print '</div>'
            print '</div>'
            print '</div>'
        elif avail_pct < 99.95: # Critical
            print '<div class="column">'
            print '<div class="group">'
            print '<div class="skillbar clearfix" data-percent="%s%%">' % (avail_pct)
            print '<div class="skillbar-title"><span>%s</span></div>' % (name)
            print '<div class="skillbar-bar critical"></div>'
            print '<div class="skill-bar-percent">%s%%</div>' % (avail_pct)
            print '</div>'
            print '</div>'
            print '</div>'

print """</div>
</div>"""
print '<p>Report data generated for %s to %s on %s</p>' % (startDate,endDate,time.strftime('%Y-%m-%d %I:%M', time.localtime()),)
print """<p>This is raw data only, you will need to figure in whatever conditions to get actual percentage.</p>
</body>
<!-- BAR ANIMATION SCRIPT -->
<script type="text/javascript">
jQuery(document).ready(function(){
jQuery('.skillbar').each(function(){
    jQuery(this).find('.skillbar-bar').animate({
        width:jQuery(this).attr('data-percent')
    },2000);
});
});
</script>
</html>
"""
