#! /bin/bash

name=$(uname -n)

gcloud logging write production_log "${name}: New VM Created"

cd /
mkdir sentiment-data

cd sentiment-data/

apt install -y python3-pip
gcloud logging write production_log "${name}: Installed pip"

curl -H 'Cache-Control: no-cache, no-store' -o requirements.txt https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/requirements.txt
gcloud logging write production_log "${name}: Downloaded requirements.txt"

python3 -m pip install -r requirements.txt --break-system-packages

curl -H 'Cache-Control: no-cache, no-store' -o taskmanager.py https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/taskmanager.py
gcloud logging write production_log "${name}: Downloaded taskmanager"

gcloud logging write production_log "${name}: taskmanager: "$(python3 taskmanager.py get-task)