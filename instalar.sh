#!/bin/bash
sudo apt update
sudo apt install -y openjdk-14-jdk python3-pip
pip3 install flask flask_cors mcstatus
cd api_minecraft_server
python3 app.py
