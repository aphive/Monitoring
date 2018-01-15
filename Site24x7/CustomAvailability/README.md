# Site24x7 Availability Over Date Range
This script will allow you to pull availability for your checks over a specific date range. Say you want to get your availability for the last quarter of 2017, you'd simply need to add your monitor ID's to the list and then run this script like so:

```./customdates.py -s 2017-10-01 -e 2017-12-31```

This will output data like:

```
Site Name	100.0%
Site Name	99.99%
```
