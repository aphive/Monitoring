AD Password Reminder Script
=======

This setup is for those of you that have a Linux environment but have an Active Directory doing some sort of password management for example: all your systems are running Linux but your email is provided by Exchange and you have a password policy where they must be changed every x days.

There are two files that makes the magic happen:

1. pwdexpire.pl
2. pwdexpire.ini

The only file we would ever need to touch is the **pwdexpire.ini** and it has instructions for when you are editing it. There are however some changes that will need to be made in the pl file but it should only be once and those changes are to add the company name and the url employees should go to change their owa password.

One thing to keep in mind, when testing, find the line starting with **rptAddr**, make a copy and put your email address in it; also comment out the original line so it does not send reports to your production address.

Important
-----------

After making your changes, remember to set rptAddr and testMode back to the original
