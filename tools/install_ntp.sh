#!/bin/bash
sudo apt install ntp ntpdate -y
sudo sed -i 's/^pool/#&/' /etc/ntp.conf |grep "pool 0.ubuntu.pool.ntp.org iburst"
sudo sed -i 's/^pool/#&/' /etc/ntp.conf |grep "pool 1.ubuntu.pool.ntp.org iburst"
sudo sed -i 's/^pool/#&/' /etc/ntp.conf |grep "pool 2.ubuntu.pool.ntp.org iburst"
sudo sed -i 's/^pool/#&/' /etc/ntp.conf |grep "pool 3.ubuntu.pool.ntp.org iburst"
sudo sed -i '/#pool 3.ubuntu.pool.ntp.org iburst/a\server 10.67.108.202' /etc/ntp.conf
sudo cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo systemctl restart ntp
sudo systemctl enable ntp
sudo ntpdate -u NTP_SERVER_IP