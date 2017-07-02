# Zenoss
Here you will find Zenoss utilities.

### zenoss_maintenance.py

Reports all devices in Maintenance mode for a specified device group. To set it up, modify line 17 from and set `<group>` to the group you want to get the report for:

```for dev in dmd.Devices.<group>.getSubDevices_recursive():```
