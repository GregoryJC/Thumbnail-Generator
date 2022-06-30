#!/bin/bash

cd /thumbnail_generator
pip3 install --upgrade pip
pip3 install -r requirements.txt
mkdir -p ./logs
chmod 777 ./logs
touch ./logs/run.log
touch ./logs/server_gunicorn.log
touch ./logs/thumbnail_generator.log
/usr/local/bin/gunicorn server:app -k gevent --access-logfile=logs/thumbnail_generator.log --error-logfile=logs/server_gunicorn.log --timeout 120  -b :630 -w 3