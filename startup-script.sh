#! /bin/bash

name=$(uname -n)

gcloud logging write production_log "${name}: New VM Created"

cd /
mkdir sentiment-data

cd sentiment-data/

curl -H 'Cache-Control: no-cache, no-store' -o taskmanager.py https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/taskmanager.py
gcloud logging write production_log "${name}: Downloaded taskmanager"

gcloud logging write production_log "${name}: taskmanager:" + $(python3 taskquerier.py get-task)