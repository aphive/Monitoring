#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# List all devices in Maintenance state for specified group.
import Globals, sys
import transaction
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
dmd = None
try:
    dmd = ZenScriptBase(connect=True).dmd
except Exception, e:
    print "Connection to zenoss dmd failed: %s\n" % e
    sys.exit(1)
print ""
print "Devices currently in Maintenance State within Zenoss:"
print ""
for dev in dmd.Devices.<group>.getSubDevices_recursive():
        if dev.productionState == 300:
                print dev.id
trans = transaction.get()
trans.commit()
