#! /bin/bash

name=$(uname -n)

gcloud logging write production_log "${name}: New VM Created"

cd /
mkdir startup

cd startup/