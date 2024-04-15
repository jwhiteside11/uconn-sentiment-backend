#! /bin/bash

machinename=$(uname -n)

gcloud logging write production_log "${machinename}: New VM Created"

cd /
mkdir sentiment-data

cd sentiment-data/

apt install -y python3-pip
gcloud logging write production_log "${machinename}: Installed pip"

curl -H 'Cache-Control: no-cache, no-store' -o requirements.txt https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/requirements.txt
gcloud logging write production_log "${machinename}: Downloaded requirements.txt"

python3 -m pip install -r requirements.txt --break-system-packages

curl -H 'Cache-Control: no-cache, no-store' -o taskmanager.py https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/taskmanager.py
gcloud logging write production_log "${machinename}: Downloaded taskmanager"

gcloud logging write production_log "${machinename}: taskmanager: $(python3 taskmanager.py get-task)"

mkdir input_files/
gcloud storage cp gs://production_upload_data_sentiment-analysis-379200/Raw_CC/$(python3 taskmanager.py task-inputfile)/* input_files/

gcloud logging write production_log "${machinename}: Downloaded inputs ${input_file}"

keywordlocations=$(python3 taskmanager.py task-keywordlocations)
ticker=$(python3 taskmanager.py task-ticker)
datetime=$(python3 taskmanager.py task-datetime)

curl -H 'Cache-Control: no-cache, no-store' -o keywordcollector.py https://raw.githubusercontent.com/ckury/uconn-sentiment-automation/main/keywordcollector.py
gcloud logging write production_log "${machinename}: Downloaded keywordcollector"

gcloud logging write production_log "${machinename}: Downloaded keywords as csv file $(python3 keywordcollector.py ${keywordlocations} keywords.csv)"

# PROTOTYPE Below

python3 scoring.py input_files/ keywords.csv scored_files/

python3 weighting.py scored_files/ keywords.csv weighted_files/

python3 summarizing.py scored_files/ scored_summarized_files/

python3 summarizing.py weighted_files/ weighted_summarized_files/

python3 uploading.py scored_files/ weighted_files/ Detailed ${keywordlocations} ${ticker} ${datetime}
python3 uploading.py scored_summarized_files/ weighted_summarized_files/ Summary ${keywordlocations} ${ticker} ${datetime}