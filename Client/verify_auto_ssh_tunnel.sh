#!/bin/bash

ssh_failed=$(systemctl status auto-ssh-tunnel.service --no-pager | grep failed -c)

if [ $ssh_failed -eq "1" ]
then
 echo Restarting Auto SSH Tunnel Service
 sudo systemctl restart auto-ssh-tunnel.service;
else
 echo Auto SSH Tunnel is running;
fi
