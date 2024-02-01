#!/bin/bash

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

pip install psutil flask

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

cp -r app/* /usr/share/monit/
chown "$USERNAME:$USERNAME" /usr/share/monit/
chmod -R 600 /usr/share/monit/
chmod 700 /usr/share/monit/

cp app/monit.py /usr/bin/monit.py
chown "$USERNAME:$USERNAME" /usr/bin/monit.py
chmod 700 /usr/bin/monit.py

cp app/monit-api.py /usr/bin/monit-api.py
chown "$USERNAME:$USERNAME" /usr/bin/monit-api.py
chmod 700 /usr/bin/monit-api.py

cp service/monit.service /etc/systemd/system/monit.service
cp service/monit.timer /etc/systemd/system/monit.timer

cp service/monit-api.service /etc/systemd/system/monit-api.service

systemctl daemon-reload
systemctl start monit.timer
systemctl enable monit.timer
systemctl start monit-api.service
systemctl enable monit-api.service

echo "User $USERNAME created with folders and permissions"

echo "Script execution complete."
echo "To access the API at 127.0.0.1:8000/reports/<report_id>, don't forget to open port 8000/tcp in your firewall !"
echo "You can start using the monit.py monitoring tool"

