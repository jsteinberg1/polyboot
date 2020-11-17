# polyboot
Reboot or reset Polycom phones remotely using curl commands (OS X / Linux).

Based on jgulczyn's post on the Polycom forums:

http://community.polycom.com/t5/VoIP/Remote-reboot-of-VVX-600s/m-p/89610#M19979

Tested on VVX300 and SoundPoint 331 phones.

## Usage:
```
./polyboot.py (-s / -f) (ip address / file) (reboot / factory) (admin PW)

Reboot (single phone /IP):        polyboot.py -s 127.0.0.1 reboot 1234
Factory Reset (single IP):        polyboot.py -s 127.0.0.1 factory 1234

Reboot (IP list):                 polyboot.py -f iplist.txt reboot 1234
Factory Reset (IP list):          polyboot.py -f iplist.txt factory 1234
```

The default Polycom Admin password is *456*. You should probably change that.

If you're using an IP list, set your `batch_size` and `batch_timeout` values in `polyboot.py` (lines 29 and 32) appropriately to reflect your infrastructure's capabilities. These values work well for our single host and 400 phones, but if you have a smaller setup you may not need it at all.

## IP List:

The IP list file should have one IP per line:

```
127.0.0.1
192.168.10.1
192.168.10.2
10.81.11.22
```

By default, you can pull all Polycom phones out of all local DHCP scopes using the following Powershell snippet:

```
Get-DhcpServerv4Scope -cn (DHCP Server) | select ScopeID | ForEach-Object {
Get-DhcpServerv4Lease -cn (DHCP Server) -ScopeID $_.ScopeID | where {$_.HostName -like "Polycom*"} | select IPAddress
} > dhcp_polycomlist.txt
```

This will put all IPs into a text file called `dhcp_polycomlist.txt`. 

Remove the first two lines and you've got a list of IPs to give to polyboot!

## Bonus:

If you reconfigure 350 phones pointing to a single server simultaneously, fun things happen!  
I implemented the pacing shortly after.

![danger](http://i.imgur.com/myH8Brf.png)

# polyboot Unique Passwords
Some PBXes have unique passwords for each phone.  In that case, you can use the bulk scripts to handle this scenario.

## IP List:

Create a file 'iplist.txt' with each phone's IP and unique password.

```
127.0.0.1,"password"
192.168.10.1,"password2"
192.168.10.2,"password3"
10.81.11.22,"password4"
```

## Usage:
```
./polyboot_bulk_factory.py

```

