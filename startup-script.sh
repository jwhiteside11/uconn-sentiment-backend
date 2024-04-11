#!/use/bin/env bash

name=$(uname -n)

gcloud write production_log "${name}: New VM Created"

cd /
mkdir startup

cd startup/