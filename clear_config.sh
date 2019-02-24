#!/bin/bash

rm -f Client/auto-ssh-tunnel-*
rm -f Client/connect_*
rm -f Client/verify_auto_ssh_tunnel_*
truncate -s 0 Client/server
echo Config cleared.
