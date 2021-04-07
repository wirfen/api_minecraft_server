#!/bin/bash
sudo apt update
sudo apt install -y openjdk-14-jdk python3-pip
pip3 install flask mcstatus
cp funciones/server.properties .
cd api_minecraft_server
python3 app.py