#!/bin/bash
set -e

# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3 python3-dev

# Install python dependencies
pip3 install -r /scripts/requirements.txt