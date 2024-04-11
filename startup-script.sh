#!/use/bin/env bash

cd /
mkdir startup

cd startup/

# Download ops agent used for logging
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
# Install ops agent
sudo bash add-google-cloud-ops-agent-repo.sh --also-install
