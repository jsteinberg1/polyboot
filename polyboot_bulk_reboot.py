#!/usr/bin/env python3.8
# ----------------------------------------------------------------------------------------------------------------------
# Polyboot FACTORY RESET
# ========
# A simple program to reboot Polycom phones using CURL commands to interact with the phone's web UI.
#
#
# Usage
# ~~~~~
# ./polyboot_bulk_reset.py
# Create a csv file called iplist.txt like below - if your password is not just digits then surround it by single quotes
# 10.10.10.117,123456
# 10.10.10.118,'Z$$M2*#00'
# ----------------------------------------------------------------------------------------------------------------------

from subprocess import Popen
from sys import argv
from base64 import b64encode
from time import sleep
import csv

# --[ Configure these to your liking ] ---------------------------------------------------------------------------------
# Timeout between connections for a list of addresses
timeout = 0.5

# Number of phones in a list to process before pausing (to allow server to catch up with registrations etc)
batch_size = 40

# Pause duration after each batch
batch_timeout = 60
# -----------------------------------------------------------------------------------------------------------------------

# Auth string glued in front of password
auth_string = "Polycom:"

# Rebooting the phone
def reboot(ip,admin_password):
    reboot_curl = ['curl',
                   '-k',
                   'https://' + str(ip) + '/form-submit/Reboot',
                   '-X',
                   'POST',
                   '-H',
                   'Authorization: Basic ' + b64encode(admin_password.encode('UTF-8')).decode('ascii'),
                   '-H',
                   'Content-Length: 0',
                   '-H',
                   'Content-Type: application/x-www-form-urlencoded',
                   '-H',
                   'Cookie: Authorization=Basic ' + b64encode(admin_password.encode('UTF-8')).decode('ascii')]
    Popen(reboot_curl, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    return


# BULK REBOOT
with open('iplist.txt') as f:
    reader = csv.reader(f)
    for IP_ADDR, Password in reader:
        ip = IP_ADDR
        Passwd = Password
        admin_password = auth_string + Passwd
        reboot(ip,admin_password)
        print(f'Reboot instruction sent to address: {ip} using password {Passwd}')
