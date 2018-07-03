#!/usr/bin/env python3
#
# Python Installer / Uninstaller
#
import subprocess
import sys
import os
import platform
import time

from Client import connect

# if nix or Mac then run installer
if platform.system() == "Linux" or platform.system() == "Darwin":
    # give installer and uninstaller a null value
    installer = False
    uninstaller = False

    # Check user ID
    if os.getuid() != 0:
        print("Are you root? Please execute as root")
        exit()

    try:
        # if our command option is true then install dependencies
        if sys.argv[1] == "install":
            installer = True

        # if our command option is true then install dependencies
        if sys.argv[1] == "uninstall":
            uninstaller = True

    # if index is out of range then flag options
    except IndexError:
        print("** Auto SSH Dependency Installer by Facerecog Asia **")
        print("** Written by: Muhammad Amrullah (Facerecog Asia) **")
        print("** Visit: https://github.com/facerecog **")
        print("\nTo install: setup.py install")

    # if user specified install then lets proceed to the installation
    if installer is True:

        # install openssh-server with apt for Debian systems
        if platform.system() == "Linux":
            # if we trigger on sources.list then we know its Debian
            if os.path.isfile("/etc/apt/sources.list"):

                print("[*] Installing dependencies..")
                # force install of debian packages
                subprocess.Popen("apt-get -y --allow-change-held-packages install openssh-server", shell=True).wait()
            # if sources.list is not available then we're running something offset
            else:
                print("[!] You're not running a Debian variant. Installer not finished for this type of Linux distro.")
                print("[!] Install open-ssh server manually for all of autossh dependencies.")
                sys.exit()

        print("[*] Updating 'Alive' parameters in ssh_config and sshd_config...")
        if 'ServerAliveInterval' not in open('/etc/ssh/ssh_config').read():
            writetoSSH = open('/etc/ssh/ssh_config','a')
            writetoSSH.write("    ServerAliveInterval 30\n    ServerAliveCountMax 4")
            writetoSSH.close()

        if 'ClientAliveInterval' not in open('/etc/ssh/sshd_config').read():
            writetoSSH = open('/etc/ssh/sshd_config','a')
            writetoSSH.write("ClientAliveInterval 30\nClientAliveCountMax 4")
            writetoSSH.close()


        # if installation is done on client, the autossh automatically kicks in the daemon
        try:
            rootname = connect.username_ipaddress
            if rootname == "":
                print("Please run configure.py first.")
                sys.exit()

            print("[*] Installing autossh client...")

            print("[*] Setting up autossh client as startup application...")
            subprocess.Popen("cd && mkdir .ssh -p", shell=True)

            if platform.system() == "Linux":
                subprocess.Popen("mkdir /etc/auto-ssh-tunnel && yes | cp Client/connect.py /etc/auto-ssh-tunnel", shell=True).wait()
                subprocess.Popen("chmod +x /etc/auto-ssh-tunnel/connect.py", shell=True).wait()
                subprocess.Popen("yes | cp Client/auto-ssh-tunnel.service /etc/systemd/system/", shell=True).wait()
                subprocess.Popen("systemctl enable auto-ssh-tunnel.service", shell=True).wait()
            elif platform.system() == "Darwin":
                subprocess.Popen("mkdir /System/Library/StartupItems/auto-ssh-tunnel", shell=True)
                subprocess.Popen("yes | cp mac/StartupParameters.plist /System/Library/StartupItems/auto-ssh-tunnel/", shell=True)
                subprocess.Popen("yes | cp Client/connect.py /System/Library/StartupItems/auto-ssh-tunnel/", shell=True)
                subprocess.Popen("chmod +x /System/Library/StartupItems/auto-ssh-tunnel/connect.py", shell=True).wait()

            print("[*] Copying SSH-Keys file over to server...")
            subprocess.call("printf 'priv_key\n\n' | ssh-keygen -t rsa -b 2048 -v -P ''", shell=True)

            print("[*] Installing private keys inside protected folder...")
            if platform.system() == "Linux":
                subprocess.call(['ssh-copy-id', '-i', 'priv_key.pub', rootname])
            elif platform.system() == "Darwin":
                subprocess.Popen("cat priv_key.pub | ssh " + rootname + " 'cat >> ~/.ssh/authorized_keys'", shell=True).wait()

#            print("[*] Moving autossh client into the /usr/local/bin/ directory...")
#            subprocess.Popen("yes | cp Client/connect.py /usr/local/bin/", shell=True)
#            subprocess.Popen("chmod +x /usr/local/bin/connect.py", shell=True).wait()

            print("[*] Moving private key to /etc/auto-ssh-tunnel/")
            subprocess.Popen("rm priv_key.pub", shell=True)
            subprocess.Popen("mv priv_key /etc/auto-ssh-tunnel/priv_key", shell=True)
        except subprocess.CalledProcessError as e:
            pass

        # Start the service and check if the installation has been successful
        subprocess.Popen("systemctl restart auto-ssh-tunnel.service", shell=True).wait()
        auto_ssh_service_not_started = subprocess.Popen("systemctl status auto-ssh-tunnel.service --no-pager", shell=True).wait()
        if auto_ssh_service_not_started:
            time.sleep(1)
            auto_ssh_service_not_started = subprocess.Popen("systemctl restart auto-ssh-tunnel.service --no-pager", shell=True).wait()
            if auto_ssh_service_not_started:
                print("[!] Installation has failed. Please ensure that connect.py and .pub file is installed")
                exit(1)
        print("________________________________________________________________________")
        print("[*] We are now finished! Restart the client to complete the installation.")
        print("[*] To check the status of the auto-ssh-tunnel service enter on the terminal:\n")
        print("  systemctl status auto-ssh-tunnel.service --no-pager\n")

    # if user specified uninstall then proceed to uninstallation
    if uninstaller is True:
        subprocess.Popen("sudo systemctl stop auto-ssh-tunnel.service", shell=True).wait()
        subprocess.Popen("sudo systemctl disable auto-ssh-tunnel.service", shell=True).wait()
        subprocess.Popen("sudo rm -rf /etc/systemd/system/auto-ssh-tunnel.service /etc/auto-ssh-tunnel /usr/local/bin/connect.py /System/Library/StartupItems/auto-ssh-tunnel/", shell=True).wait()
        print("[*] Uninstallation successful.")

# if the platform is running on a MAC, a version will be ready soon
# if platform.system() == 'Darwin':
    # print("[!] A version for Mac will be ready soon")

if platform.system() != "Linux" and platform.system() != "Darwin":
        print("[!] Sorry this installer is not designed for any other system other than Linux or Mac. Please install the python dependencies manually.")
