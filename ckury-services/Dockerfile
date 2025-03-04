FROM --platform=linux/amd64 python:3.9-buster
 
# install dependencies

COPY . .

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
COPY . /opt/app
 
# start flask server

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5200"]