#!/bin/bash

cd /
pip3 install --upgrade pip
pip3 install -r requirements.txt --no-cache-dir
mkdir logs
mv thumbnail_generator.log /logs/
touch /logs/run.log
chmod 777 logs
/usr/local/python3/bin/gunicorn server:app -k gevent --access-logfile=logs/thumbnail_generator.log --error-logfile=logs/server_gunicorn.log --timeout 120  -b :630 -w 3