#!/bin/bash

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

pip install psutil

USERNAME="monit-man"

useradd -m -s /bin/bash "$USERNAME"

mkdir /etc/monit/
chown "$USERNAME:$USERNAME" /etc/monit/
chmod 700 /etc/monit/

mkdir /var/monit/
chown "$USERNAME:$USERNAME" /var/monit/
chmod 700 /var/monit/

mkdir /var/log/monit/
chown "$USERNAME:$USERNAME" /var/log/monit/
chmod 700 /var/log/monit/

touch /var/log/monit/monit.log
chown "$USERNAME:$USERNAME" /var/log/monit/monit.log
chmod 600 /var/log/monit/monit.log

touch /etc/monit/monit.conf
cp conf/monit.conf /etc/monit/monit.conf
chown "$USERNAME:$USERNAME" /etc/monit/monit.conf
chmod 600 /etc/monit/monit.conf

cp app/monit.py /usr/bin/monit.py
chown "$USERNAME:$USERNAME" /usr/bin/monit.py
chmod 700 /usr/bin/monit.py

cp service/monit.service /etc/systemd/system/monit.service
cp service/monit.timer /etc/systemd/system/monit.timer

systemctl daemon-reload
systemctl start monit.timer
systemctl enable monit.timer

echo "User $USERNAME created with folders and permissions"

echo "Script execution complete."
echo "You can start using the monit.py monitoring tool"