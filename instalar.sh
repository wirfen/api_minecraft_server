#!/bin/bash
sudo apt update
sudo apt install -y openjdk-14-jdk python3-pip
pip3 install flask mcstatus
python3 app.py
