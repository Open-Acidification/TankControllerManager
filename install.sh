#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get -y install python3 python3-pip postgresql postgresql-contrib nodejs npm redis
sudo npm install -g @vue/cli

cd oa_server
pip3 install -r requirements.txt

# Set up database
sudo su postgres -c "psql -c \"CREATE USER oa_server_user WITH PASSWORD 'password';\""
sudo su postgres -c "psql -c \"CREATE DATABASE oa_server WITH OWNER oa_server_user;\""