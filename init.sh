#!/bin/bash

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

pip install psutil

USERNAME="monit-man"

useradd -m --disable-login -s /bin/bash "$USERNAME"

mkdir /etc/monit/
chown "$USERNAME:$USERNAME" /etc/monit/
chmod 755 /etc/monit/

mkdir /var/monit/
chown "$USERNAME:$USERNAME" /var/monit/
chmod 755 /var/monit/

mkdir /var/log/monit/
chown "$USERNAME:$USERNAME" /var/log/monit/
chmod 755 /var/log/monit/

touch /var/log/monit/monit.log
chown "$USERNAME:$USERNAME" /var/log/monit/monit.log
chmod 766 /var/log/monit/monit.log

touch /etc/monit/monit.conf
cp conf/monit.conf /etc/monit/monit.conf
chown "$USERNAME:$USERNAME" /etc/monit/monit.conf
chmod 766 /etc/monit/monit.conf

cp app/monit.py /home/monit-man/monit.py
chown "$USERNAME:$USERNAME" /home/monit-man/monit.py
chmod 766 /home/monit-man/monit.py

cp service/monit.service /etc/systemd/system/monit.service
cp service/monit.target /etc/systemd/system/monit.target

systemctl daemon-reload
systemctl start monit.timer
systemctl enable monit.timer

echo "User $USERNAME created with folders and permissions"

echo "Script execution complete."
echo "You can start using the monit.py monitoring tool"