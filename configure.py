#!/usr/bin/env python3

import os.path
from shutil import copyfile
import argparse

parser = argparse.ArgumentParser(description="Configure auto-ssh-tunnel")
parser.add_argument("name", metavar="name", type=str, nargs=1, help="Name of the forwarded service")
parser.add_argument("port_open", metavar="port_open", type=int, nargs=1, help="Port number of the ssh server")
parser.add_argument("port_forward", metavar="port_forward", type=int, nargs=1, help="Port number to forward to the ssh server")
parser.add_argument("username", metavar="username", type=str, nargs=1, help="Username with which log in to the server")
parser.add_argument("server", metavar="server", type=str, nargs=1, help="Server IP address")
args = parser.parse_args()

name = args.name[0]
port_open = args.port_open[0]
port_forward = args.port_forward[0]
username = args.username[0]
server = args.server[0]

server_str = username + "@" + server

port_open_str = "port_open"
port_forward_str = "port_forward"
username_ipaddress_str = "username_ipaddress"



if os.stat("Client/server.py").st_size == 0:
    with open("Client/server.py", "w+") as services_file:
        print("Writing to server.py...")
        services_file.write("username_ipaddress = \"" + server_str +"\"\n")
else:
    with open("Client/server.py", "a+") as services_file:
        services_file.seek(0)
        lines = services_file.readlines()
        if "username_ipaddress = \"" + server_str +"\"\n" not in lines:
            print("Server" + lines[0].split('=')[1].rstrip() + " should be consistent for the different services.")
            exit()



connect_file = open("Client/connect.py", "r")
lines = connect_file.readlines()

port_open_line = None
port_forward_line = None
username_ipaddress_line = None
i = 1
for line in lines:
    if line.startswith(port_open_str):
        port_open_line = i
    if line.startswith(port_forward_str):
        port_forward_line = i
    if line.startswith(username_ipaddress_str):
        username_ipaddress_line = i

    i += 1

lines[port_open_line - 1] = "port_open = \"" + str(port_open) +"\"\n"
lines[port_forward_line - 1] = "port_forward = \"" + str(port_forward) +"\"\n"
lines[username_ipaddress_line - 1] = "username_ipaddress = \"" + str(server_str) +"\"\n"

edited_lines = ""
for line in lines:
    edited_lines += line

connect_file.close()

print("Writing to connect_" + name + ".py...")
connect_file = open("Client/connect_" + name + ".py", "w+")
connect_file.write("".join(edited_lines))
connect_file.close()





connect_file = open("Client/auto-ssh-tunnel.service", "r")
lines = connect_file.readlines()

exec_start_str = "ExecStart="
description_str = "Description="

exec_start_line = None
description_line = None
i = 1

for line in lines:
    if line.startswith(exec_start_str):
        exec_start_line = i
    if line.startswith(description_str):
        description_line = i
    i += 1

lines[exec_start_line - 1] = "ExecStart=/etc/auto-ssh-tunnel/connect_" + name + ".py\n"
lines[description_line - 1] = "Description=Auto SSH Tunnel " + name.upper() + " service\n"

edited_lines = ""
for line in lines:
    edited_lines += line

connect_file.close()

print("Writing to auto-ssh-tunnel-" + name + ".service...")
connect_file = open("Client/auto-ssh-tunnel-" + name + ".service", "w+")
connect_file.write("".join(edited_lines))
connect_file.close()




connect_file = open("Client/verify_auto_ssh_tunnel.sh", "r")
lines = connect_file.readlines()

failed_str = "ssh_failed="
message_str = " echo Restarting Auto SSH Tunnel"
restart_str = " sudo systemctl restart auto-ssh-tunnel"

failed_line = None
message_line = None
restart_line = None
i = 1

for line in lines:
    if line.startswith(failed_str):
        failed_line = i
    if line.startswith(message_str):
        message_line = i
    if line.startswith(restart_str):
        restart_line = i
    i += 1

lines[failed_line - 1] = "ssh_failed=$(systemctl status auto-ssh-tunnel-" + name + ".service --no-pager | grep failed -c)\n"
lines[message_line - 1] = " echo Restarting Auto SSH Tunnel " + name.upper() + " Service\n"
lines[restart_line - 1] = " sudo systemctl restart auto-ssh-tunnel-" + name + ".service;\n"

edited_lines = ""
for line in lines:
    edited_lines += line

connect_file.close()

print("Writing to verify_auto_ssh_tunnel_" + name + ".service...")
connect_file = open("Client/verify_auto_ssh_tunnel_" + name + ".sh", "w+")
connect_file.write("".join(edited_lines))
connect_file.close()





with open("Client/services.list", "a+") as services_file:
    services_file.seek(0)
    lines = services_file.readlines()
    if name+"\n" not in lines:
        print("Writing to services.list...")
        services_file.write(name + "\n")


print("Configuration successful.")
