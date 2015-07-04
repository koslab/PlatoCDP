#!/bin/bash

cd /opt/
git clone https://github.com/koslab/PlatoCDP.git platocdp

cd /opt/platocdp/
wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py
chown -R plone:plone /opt/platocdp/
