#!/bin/sh
# Author: Computero
# Description: Nagios check command for Microsoft Exchange
# Date: 2009.05.06 # Version: 1.0

if [ -z $1 ];
   then echo 'UNKNOWN: command is wrong'
exit 3 fi

curl -skIf -u 'user@domain.com:password' "https://${1}/owa/" >/dev/null 2>&1

if [ $? != 0 ];
   then echo 'CRITICAL: Exchange login failure' exit 2
fi

echo 'OK: Exchange login successful'
exit 0
