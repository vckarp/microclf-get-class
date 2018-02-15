#!/bin/bash

# A shell script to install all of the requirements and run the server in a background
# Requires port 5001 to be open

sudo apt-get update -y
sudo apt-get install -y python3-dev python3-pip build-essentials
sudo pip3 install --upgrade pip setuptools
sudo pip3 install -r ./requirements.txt
sudo python3 -m nltk.downloader averaged_perceptron_tagger wordnet
sudo gunicorn get_class:app -b "0.0.0.0:5001" --workers 5 --timeout 120 --daemon
