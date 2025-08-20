#/bin/bash
#@file
#@author wenkelx
#@date 2025-07-01
#@description:Automatically install docker scriptinstall

export https_proxy=
export http_proxy=
export no_proxy=
export all_proxy=
export socks_proxy=
export ftp_proxy=

## Install official package
sudo apt-get -y remove docker docker-engine docker.io containerd runc
sudo apt-get -y update
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common vim
wget https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg 
sudo apt-key add ./gpg
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce
sudo docker -v

## config docker 
echo '{ "exec-opts": [ "native.cgroupdriver=systemd" ],"insecure-registries": ["DOCKER_SERVER_IP"] }' | sudo tee  /etc/docker/daemon.json
sudo systemctl daemon-reload
sudo systemctl restart docker

## Config intel proxy
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\n#Environment=\"HTTP_PROXY=$SYSTEM_PROXY\"" | sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$SYSTEM_PROXY\"" | sudo tee /etc/systemd/system/docker.service.d/https-proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
systemctl show --property=Environment docker

## Verify installation
#sudo docker run hello-world

#move docker default direcoty
sudo systemctl stop docker
sudo cp  -r /var/lib/docker /home/
sudo sed -i '13s#$# --data-root=/home/docker/#g' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl restart docker

