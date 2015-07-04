#!/bin/bash

cd /opt/
git clone https://github.com/koslab/PlatoCDP.git platocdp

cd /opt/platocdp/
wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py
cat << EOF > eggcache.cfg
[buildout]
extends = buildout.cfg
parts = eggcache

[eggcache]
recipe = zc.recipe.egg
eggs = \${instance1:eggs}
EOF

chown -R plone:plone /opt/platocdp/
