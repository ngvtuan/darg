#!/bin/bash

source ../.ve/bin/activate

git pull
pip install -r requirements.txt
python ../minify_static.py
../site/manage.py migrate 
../site/manage.py collectstatic --noinput
