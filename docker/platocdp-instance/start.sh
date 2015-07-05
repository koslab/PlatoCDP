#!/bin/bash

chmod a+rwx /logs
su plone -c "/opt/platocdp/bin/buildout -o -c /opt/platocdp/instance.cfg"
supervisord -c /etc/supervisord.d/platocdp.conf
