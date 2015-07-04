#!/bin/bash -x

cd /opt/platocdp
virtualenv venv 
./venv/bin/python bootstrap.py 
./bin/buildout -vvv -c eggcache.cfg

