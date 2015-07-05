#!/bin/bash

INSTANCE_COUNT=${PLATOCDP_INSTANCE_COUNT:-1}

haproxy_config.py > /etc/haproxy.cfg
chmod a+rw /logs
haproxy -f /etc/haproxy.cfg
#supervisord -c /etc/supervisord.d/haproxy.conf
