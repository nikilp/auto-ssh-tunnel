#!/usr/bin/env python

import re
import subprocess

location_of_pem_file = "/etc/auto-ssh-tunnel/priv_key"
# configure.py will automatically edit port_open and username_ipaddress
port_open = "50000"
username_ipaddress = ""

# A function that checks if there is an existing ssh process running in the backgroun:
def ssh_running():
    try:	
        out = subprocess.check_output("pgrep -x ssh", shell=True)
        print(out)
    except subprocess.CalledProcessError as e:
        print("Running and activating ssh. Please wait for 1 minute...")
	run_ssh()

# A	function that runs the ssh reverse tunnel
def run_ssh():
    try:
        full_ssh_command= "ssh -i %s -N -R %s:localhost:22 %s" % (location_of_pem_file, port_open, username_ipaddress)
        ssh_output = subprocess.check_output(full_ssh_command, shell=True)
        if not ssh_output:
            print("Successful")
    except subprocess.CalledProcessError as e:
        print("Failed. Please check your config file.")

#Main Command

if __name__ == "__main__":
    ssh_running()
