#!/bin/bash

# Build the frontend
cd oa_frontend
npm run build

# Migrate database models
cd ../oa_server
python3 manage.py makemigrations
python3 manage.py migrate