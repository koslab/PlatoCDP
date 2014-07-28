#!/bin/bash


BUILDOUT_ROOT=%%BUILDOUT_ROOT%%

if [ `whoami` != "root" ];then
   echo "This script have to be run as root"
   exit
fi

case "$1" in 
   rebuild)
        cd $BUILDOUT_ROOT
        sudo -u plone virtualenv venv
        sudo -u plone wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py -o /dev/null
        sudo -u plone ./venv/bin/python bootstrap.py
        sudo -u plone ./bin/buildout -c buildout.cfg
   ;;
   start)
       echo "Starting ZEO Replication Service"
       $BUILDOUT_ROOT/bin/zrsreplicator start
   ;;
   stop)
       echo "Stopping ZEO Replication Service"
       $BUILDOUT_ROOT/bin/zrsreplicator stop
   ;;
   restart)
       echo "Stopping ZEO Replication Service"
       $BUILDOUT_ROOT/bin/zrsreplicator stop
       echo "Starting ZEO Replication Service"
       $BUILDOUT_ROOT/bin/zrsreplicator start
   ;;
   status)
       echo "Status of ZEO Replication Service"
       $BUILDOUT_ROOT/bin/zrsreplicator status
   ;;
esac
