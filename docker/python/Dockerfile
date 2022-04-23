#!/bin/sh

FROM python:3
EXPOSE 8443 

RUN apt-get update && \
     apt-get install python3-pip -y
RUN pip3 install --no-cache-dir --upgrade pip

WORKDIR /var/www/app
COPY . .

RUN pip3 install --no-cache-dir  -r /var/www/app/requirements.txt

# RUN python3 ./manage.py migrate
# RUN python3 ./manage.py createsuperuser

ENTRYPOINT python3 ./manage.py runserver 0.0.0.0:8443
