#!/bin/bash

# Install requirements
apt-get update
apt-get install -y ceph git python-pip python3-setuptools
apt-get install -y python-coverage python3-coverage python-nose python3-nose

cd  /vagrant
python setup.py develop
python3 setup.py develop

py3ver=$(python3 --version 2>&1 | awk '{print $2}')
python3-coverage run --source crushsim setup.py test &> tests-$py3ver.txt
python3-coverage report -m &> coverage-$py3ver.txt

py2ver=$(python2 --version 2>&1 | awk '{print $2}')
python2-coverage run --source crushsim setup.py test &> tests-$py2ver.txt
python2-coverage report -m &> coverage-$py2ver.txt
