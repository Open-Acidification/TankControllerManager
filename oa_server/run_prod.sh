#!/bin/bash

# Serve frontend
cd oa_frontend/dist
sudo python3 -m http.server 80 &

# Serve backend
cd ../..
python3 manage.py qcluster &
python3 manage.py runserver 0.0.0.0:8080