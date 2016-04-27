#!/bin/bash

# Install requirements
apt-get update
apt-get install -y ceph git python-pip

cd  /vagrant
python setup.py develop
