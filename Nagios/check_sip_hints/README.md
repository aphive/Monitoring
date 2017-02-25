Monitoring Asterisk Hints
=======

This script checks the number of watchers on sip servers and reports it in a graphable manner ie:  name:value

Hints Explained
-----------

Hints *(also called “presence”)* are a way to let SIP phones *(that are using the same Asterisk server)* know the status of their peers. The connection between an extension and a device in Asterisk is called a hint.

SIP protocol allows us to use the general framework for event notification without defining the actual events or device names. Asterisk uses 'hint' to map an extension number or name to a device.
```
 [subscribers]
 exten => 57644,hint,SIP/57644
```
In this example, SIP device SIP/57644 is mapped to 57644 using hint.
```
 [subscribers]
 exten => john,hint,SIP/57644
```
*SIP/57644* can also be mapped to name *'john'* using hint. It's all up to you, how you want to name it.


Asterisk receives a **SIP SUBSCRIBE** request, it checks for a '**hint**' in a dialplan that matches the name of the device to be monitored. 'hint' tells Asterisk which device this corresponds to.
