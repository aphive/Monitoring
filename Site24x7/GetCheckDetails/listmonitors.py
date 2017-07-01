#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import json
from io import BytesIO
from optparse import OptionParser

# Define Options
parser = OptionParser(usage='Usage: %prog [options] arguments. Type -h for more info.')
parser.add_option('-t', '--type',
        type='choice',
        choices=['dns', 'url', 'ping'],
        help='Type of check to pull. ie: dns, ping, url',
        dest='checkType')
(options, args) = parser.parse_args()

# Define how to connect to Site24x7 API
def connectSite247(method,putData):
    c = pycurl.Curl()
    connectReturn = BytesIO()
    c.setopt(pycurl.URL, 'https://www.site24x7.com/api/monitors')
    c.setopt(pycurl.HTTPHEADER, ["Accept: application/json; version=2.0"])
    c.setopt(pycurl.HTTPHEADER, ["Authorization: Zoho-authtoken a12345b6c8de901f2gh3456ij78k901l"])
    c.setopt(c.WRITEFUNCTION, connectReturn.write)
    c.setopt (pycurl.CUSTOMREQUEST, method)
    c.setopt (pycurl.POSTFIELDS, putData)
    c.perform()
    c.close()
    connectOutput = connectReturn.getvalue()
    return connectOutput

# Get the API Output
listOfMonitors = json.loads(connectSite247('GET',''))

# List URL checks
################################################################################
if options.checkType == 'url':
    for i in listOfMonitors['data']:
        if i['type'] == 'URL':
            print "URL:\tname:\t%s\tmon_id:\t%s\turl:\t%s" % (i['display_name'], i['monitor_id'], i['website'])

# List DNS checks
################################################################################
if options.checkType == 'dns':
    for i in listOfMonitors['data']:
        if i['type'] == 'DNS':
            print "DNS:\tname:\t%s\tmon_id:\t%s\tdns_host:\t%s\tdomain:\t%s" % (i['display_name'], i['monitor_id'], i['dns_host'], i['domain_name'])

# List PING checks
################################################################################
if options.checkType == 'ping':
    for i in listOfMonitors['data']:
        if i['type'] == 'PING':
            print "PING:\tname:\t%s\tmon_id:\t%s\thost_name:\t%s" % (i['display_name'], i['monitor_id'], i['host_name']
