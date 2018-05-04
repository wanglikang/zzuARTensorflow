#!/usr/bin/env bash
apt-get update
apt-get upgrade
apt-get install screen
apt-get install python3-dev
apt-get install python3-pip

pip3 install tensorflow-gpu==1.5.0