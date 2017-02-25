#!/usr/bin/perl -w
#
## Author: Robert Lowe (robert.h.lowe@gmail.com)
## Edited : Computero
## Version: 2.0
## Copyright (C) 2008
##
## This script will send e-mail warnings to users of an impending Active
## Directory password expiration
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
#
## Net::LDAP, Config::IniFiles and Mail::Send. If these are not installed, enter
## the shell command "perl -MCPAN -e shell" and then, e.g. "install Net::LDAP".
  
use strict;
  
use Net::LDAP;
use Net::LDAP::Control::Paged;
use Net::LDAP::Constant ( "LDAP_CONTROL_PAGED" );
use Mail::Send;
use Config::IniFiles;
  
my $cfg = new Config::IniFiles( -file => "/path/to/pwdexpire/pwdexpire.ini",
                                -allowcontinue => 1
                                ) or die "Could not retrieve configuration: $!\n";
  
my @LDAP_SVRS = split( /\s+/, $cfg->val( 'AD', 'DCs' ) )
           or die "Config: no DCs specified!\n";
my $LDAP_PORT = $cfg->val( 'AD', 'defPort' );
my $LDAP_TIMEOUT = $cfg->val( 'AD', 'timeout' );
my $ROOTDN = $cfg->val( 'AD', 'rootDN' )
           or die "Config: no rootDN specified!\n"
my $BASEDN = $cfg->val( 'AD', 'baseDN' )
           or die "Config: no baseDN specified!\n";
my $SEARCHFILTER = $cfg->val( 'AD', 'searchFilter' )
           or die "Config: no search filter specified!\n";
my $LDAP_BIND_ANON = $cfg->val( 'AD', 'bindAnon' );
my $USER = $cfg->val( 'AD', 'user' );
my $PASSWD = $cfg->val( 'AD', 'passwd' );
my $OUTFILE = $cfg->val( 'OUTPUT', 'outFile', 'STDOUT' );
my $WARNDAYS = $cfg->val( 'EXPIRE', 'warnDays', 7 );
my $FROMADDR = $cfg->val( 'EXPIRE', 'fromAddr' )
           or die "Config: no reply-to/from address specified!\n";
my $ORGSIG = $cfg->val( 'EXPIRE', 'orgSig' )
           or die "Config: no organizational signature specified!\n";
my $ORGSVCS = $cfg->val( 'EXPIRE', 'orgSvcs' )
           or die "Config: no organizational services specified!\n";
my $HELPURL = $cfg->val( 'EXPIRE', 'helpURL' )
           or die "Config: no URL for additional help specified!\n";
my $TESTADDR = $cfg->val( 'EXPIRE', 'testAddr', 'root@localhost' );
my $TESTMODE = $cfg->val( 'EXPIRE', 'testMode', 0 );
my $RPTADDR = $cfg->val( 'EXPIRE', 'rptAddr' )
           or die "Config: no report address specified!\n";
  
# AD stores time in 10-7 units of seconds since Jan 1, 1601AD (ANSI time)
# # Unix stores time as seconds since Jan 1, 1970.
# #
# # offset is the approximate number of 10 millionths of a second between
# # 1/1/1601 and 1/1/1970 (leap years including; no clue about leap seconds)
# # This is the suggested value
# #
# # daysToWarn is the number of 10 millionths of a second in N days.
# # Seasonal time changes may affect this, but we only need to be close.
  
my $offset = 116444736000000000;
my $oneDay = 864000000000;
my $daysToWarn = $oneDay * $WARNDAYS;
  
# Find an AD domain controller and bind...
  
my $ldap; # Must be undef !!!
my ($result,$tmp,$ldapsvr,$ldapHost,$ldapPort);
  
my $i = $#LDAP_SVRS;
my $n = 0;
until ($ldap || $i<0) {
   $n = int( rand $i+1 ); # 0..$i
   if ($n < $i) { # Swap with last position
      $tmp = $LDAP_SVRS[$i];
      LDAP_SVRS[$i] = $LDAP_SVRS[$n];
      $LDAP_SVRS[$n] = $tmp;
   }
  
   $ldapsvr = pop @LDAP_SVRS;
  
   $i--;
   ($ldapHost,$ldapPort) = split(/:/, $ldapsvr);
   if (! defined $ldapPort) {
      $ldapPort = $LDAP_PORT; # Default port
 }
 $ldap = Net::LDAP->new($ldapHost,port=>$ldapPort,timeout=>$LDAP_TIMEOUT)
    || (undef $ldap, next);
 if ($LDAP_BIND_ANON) {
    $result = $ldap->bind;
    if ($result->code) {
       die $result->error;
    }
    last; # Success
 }
 else {
    $result = $ldap->bind($USER, password=>$PASSWD) || die $result->error;
 }
}
  
if (! defined $ldap) {
   die "Failed to bind to any of the configured LDAP servers";
}
  
# Retrieve the maxPwdAge field
  
my $mesg = $ldap->search( base => $ROOTDN,
       attrs => "maxPwdAge",
       scope => "base",
       filter => "distinguishedName=$ROOTDN"
       );
  
# Die if there was an error
$mesg->code && die $mesg->error;
  
# Get the first entry
my $entry = $mesg->entry(0);
  
# Get the maxPwdAge attribute -- it is maximum age of a password in
# 10-7 seconds before expiration. This value is negative.
my $maxPwdAge = $entry->get_value( 'maxPwdAge' );
  
# Get the current time
my $now = time();
  
# Put it in AD format by multiplying by 10 million and adding the offset factor
$now = ($now * 10000000) + $offset;
  
# Make a range within which passwords will soon expire.
# We want passwords that will expire in the next WARNDAYS days but not ones
# that have already expired -- they can't read their mail anyway.
  
# Calculate the value of a pwdLastSet that would expire right now
# Remember, maxPwdAge is negative!
  
my $expNow = $now + $maxPwdAge;
  
# Calculate the value of a pwdLastSet that would expire in WARNDAYS days
my $warnThreshold = $expNow + $daysToWarn;
  
# How many LDAP query results to grab for each paged round
# Set to under 1000 for Active Directory
my $page = Net::LDAP::Control::Paged->new( size => 90 );
  
my @args = ( base => $BASEDN,
        filter => "$SEARCHFILTER",
        control => [ $page ],
        attrs => "distinguishedName,sAMAccountName,userPrincipalName," .
        "pwdLastSet,userAccountControl"
        );
  
my $cookie;
my %expiry;
  
# Setup the message and report
my $msg = new Mail::Send;
my $rpt = new Mail::Send;
  
# Setup the email that goes to the employees
$msg->add('Reply-To', $FROMADDR);
$msg->add('From', $FROMADDR);
  
# Setup the email that goes to the support team
$rpt->add('Reply-To', $FROMADDR);
$rpt->add('From', $FROMADDR);
$rpt->to($RPTADDR);
$rpt->subject("Exchange password expiration report");
  
my $rfh;
$rfh = $rpt->open;
  
while(1) {
   # Perform search
   $mesg = $ldap->search( @args );
   my $howLong;
  
   # For each user with a pending password expiration...
   foreach my $entry ( $mesg->entries ) {
   # LDAP Attributes are multi-valued, but we just need the first (and only)
       my $user = $entry->get_value( "sAMAccountName" );
       my $pwdSet = $entry->get_value( "pwdLastSet" );
       my $uac = $entry->get_value( "userAccountControl" );
       my $upn = $entry->get_value( "userPrincipalName" );
  
       if (( $pwdSet < $warnThreshold ) and ( $pwdSet > $expNow ) and !( $uac & 0x10000 ) ) {
          $howLong = int( ( ( $pwdSet - $expNow ) / 10000000 ) / 86400 );
          $expiry{$upn} = $howLong;
       }
    }
  
 # Only continue on LDAP_SUCCESS
 $mesg->code and last;
  
 # Get cookie from paged control
 my ($resp) = $mesg->control( LDAP_CONTROL_PAGED ) or last;
 $cookie = $resp->cookie or last;
  
 # Set cookie in paged control
 $page->cookie($cookie);
}
  
if ($cookie) {
   # We had an abnormal exit, so let the server know we do not want any more
   $page->cookie($cookie);
   $page->size(0);
   $ldap->search( @args );
   # Also would be a good idea to die unhappily and inform OP at this point
   die("LDAP query unsuccessful");
}
  
# Put user-friendly dates in the e-mail message
#my $day = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[(localtime)[6]];
#my $month = (January,February,March,April,May,June,July,August,September,October,November,December)[(localtime)[4]];
my $day = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[(localtime)[6]];
my $month = ('January','February','March','April','May','June','July','August','September','October','November','December')[(localtime)[4]];
my $mday = (localtime)[3];
my $year = 1900 + (localtime)[5];
  
my $critSubj = "URGENT: Echange access via Outlook is no-longer possible!!";
my ($upn, $days, $when, $warnSubj, $fh);
  
foreach $upn (sort sortExpAsc keys(%expiry)) {
   $days = $expiry{$upn};
   $when = $days . " day" . (($days != 1) ? "s" : "");
   #print "$when\t\t$upn\n";
  
   print $rfh <<"RPT";
$when: $upn
RPT
  
  
   # Define the subject lines used in emails
   $warnSubj = "Warning: Your Exchange password expires in $when";
  
   # set the outgoing username to current user, unless in test mode
   if ($TESTMODE) {
   $msg->to($TESTADDR);
   }
   else {
   $msg->to($upn);
   }
  
   # if the password expire time is below threshold, use a more urgent subject line. This is set at 15 days.
   if ( $days <= 15 ) {
  
   $msg->subject($critSubj);
   }
   else {
   $msg->subject($warnSubj);
   }
  
   # start a new email with vars defined above
   $fh = $msg->open;
  
   # Put the body into the email
   print $fh <<"END";
  
This is an automated message sent on $day, $month $mday, $year to $upn. DO NOT REPLY to this message unless you need additional help.
  
Your E Mail password for Acme Inc account is due to expire in $when. When it expires you will lose access to your email services until your password is changed.
  
IMPORTANT: At 15 days before your password expires, email will not be accessible via Outlook, you may change it before this happens by going to https://owa.domain.com
  
For more detailed instructions please see $HELPURL
  
If you have any questions or problems relating to changing your password, please don't hesitate to contact us at $HELPADD.
  
$ORGSIG
  
END
  
   $fh->close; # complete the message and send it
}
  
$rfh->close; # complete the report and send it
  
sub sortExpAsc {
   $expiry{$a} <=> $expiry{$b};
  
}
