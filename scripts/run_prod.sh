#!/bin/bash

# Serve frontend
#cd oa_frontend/dist
# TODO: INSERT LINE FOR RUNNING NGINX SERVER

# NOT SUITABLE FOR PUBLIC INTERNET ACCESS
# Temporary frontend until NGINX is configured:
cd oa_frontend
sudo npm run serve -- --port 80 --mode production &

# Serve backend
#cd ../..
cd ../oa_server
python3 manage.py qcluster &
python3 manage.py runserver 0.0.0.0:8080