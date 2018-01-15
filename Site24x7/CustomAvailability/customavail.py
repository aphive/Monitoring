#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###############################################################################
#        Name: customavail.py
# Description: Display availability for a custom date range
#      Author: Computero
#        Date: January/2018
#     Version: 1.0.0
###############################################################################

import json
import pycurl
from io import BytesIO
from optparse import OptionParser

# Define Options
parser = OptionParser(usage='Usage: %prog [options] arguments. Type -h for more information.')
parser.add_option('-s', '--start',
                  type='string',
                  help='Start Date as yyyy-mm-dd.',
                  dest='startDate')
parser.add_option('-e', '--end',
                  type='string',
                  help='End Date as yyyy-mm-dd.',
                  dest='endDate')
(options, args) = parser.parse_args()

# Which monitors should data be retrieved for?
monitors = ['113770000000191032', '113770000000191032']

returned_monitors = {}

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

# Get the information and parse out the important bits
if options.startDate and options.endDate:
    for monitor in monitors:
        base_url = 'https://www.site24x7.com/api/reports/summary/'
        putData = monitor + '?period=50&start_date=' + options.startDate + '&end_date=' + options.endDate
        req_url = base_url + putData
        listOfAvail = json.loads(connectSite247('GET', req_url))
        returned_monitors[monitor] = listOfAvail
        name = listOfAvail['data']['info']['resource_name']
        avail_pct = listOfAvail['data']['summary_details']['availability_percentage']

        try:
            print '%s\t%s%%' % (name, avail_pct)
        except KeyError:
            print json.dumps(i, indent=4, sort_keys=True)
else:
    parser.error('All required flags not provided.')
