#!/bin/bash

rm -f Client/auto-ssh-tunnel-*
rm -f Client/connect_*
rm -f Client/verify_auto_ssh_tunnel_*
rm -f Client/services.list
truncate -s 0 Client/server.py
echo Config cleared.
