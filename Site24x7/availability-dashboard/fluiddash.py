#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###############################################################################
#        Name: fluiddash.py
# Description: Display current mounth's hourly availability data
#              in a dashboard format.
#              Use the GetCheckDetails script to get the monitor IDs
#              you will need to make this dashboard work.
#      Author: MrTechBot
#        Date: March/2017
#     Version: 1.0.0
###############################################################################

import json
import pycurl
from io import BytesIO

# Monitor IDs to pull data for
monitors = ['113770000000191032', '113770000000191032', '113770000000191032']

# Make calls to get the Avaiability Details
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
print "Content-type: text/html"
print """<html>
<head>
<title>Availability Dashboard</title>
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
<h1>Availability Dashboard</h1><hr />
</header><!-- END HEADER -->
<p>Thresholds: Above 99.95 = <span class="normthresh">Normal</span> | Below 99.95 = <span class="critthresh">Critical</span></p>
<div class="container"><!-- START CONTAINER -->"""

for monitor in monitors:
    base_url = 'https://www.site24x7.com/api/reports/summary/'
    putData = monitor + '?period=13&unit_of_time=1'
    req_url = base_url + putData
    listOfAvail = json.loads(connectSite247('GET', req_url))
    returned_monitors[monitor] = listOfAvail
    name = listOfAvail['data']['info']['resource_name']
    avail_pct = listOfAvail['data']['summary_details']['availability_percentage']

    if avail_pct >= 99.95: # Normal
        print '<div class="column"><!-- START COLUMN -->'
        print '<div class="group linen"><!-- START GROUP -->'
        print '<div class="skillbar clearfix" data-percent="%s%%">' % (avail_pct)
        print '<div class="skillbar-title"><span>%s</span></div>' % (name)
        print '<div class="skillbar-bar normal"></div>'
        print '<div class="skill-bar-percent">%s%%</div>' % (avail_pct)
        print '</div>'
        print '</div><!-- END GROUP -->'
        print '</div><!-- END COLUMN -->'
    elif avail_pct < 99.95: # Critical
        print '<div class="column"><!-- START COLUMN -->'
        print '<div class="group linen"><!-- START GROUP -->'
        print '<div class="skillbar clearfix" data-percent="%s%%">' % (avail_pct)
        print '<div class="skillbar-title"><span>%s</span></div>' % (name)
        print '<div class="skillbar-bar critical"></div>'
        print '<div class="skill-bar-percent">%s%%</div>' % (avail_pct)
        print '</div>'
        print '</div><!-- END GROUP -->'
        print '</div><!-- END COLUMN -->'

print """</div>
</div>
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
