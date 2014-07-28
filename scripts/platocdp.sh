#!/bin/bash


BUILDOUT_ROOT=@@BUILDOUT_ROOT@@

if [ `whoami` != "root" ];then
   echo "This script have to be run as root"
   exit
fi

case "$1" in 
   rebuild)
        cd $BUILDOUT_ROOT
        if [ ! -e ./venv/bin/python ];then
           sudo -u plone virtualenv venv
        fi
        sudo -u plone wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py -o /dev/null
        sudo -u plone ./venv/bin/python bootstrap.py
        sudo -u plone ./bin/buildout -c deployment.cfg
   ;;
   rebuild-zrs)
        cd $ZRS_BUILDOUT_ROOT
        sudo -u plone virtualenv venv
        sudo -u plone wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py -o /dev/null
        sudo -u plone ./venv/bin/python bootstrap.py
        sudo -u plone ./bin/buildout -c buildout.cfg
   ;;
   start)
       echo "Starting ZEO server"
       $BUILDOUT_ROOT/bin/zeoserver start
       echo "Starting instance 1"
       $BUILDOUT_ROOT/bin/instance1 start
       echo "Starting instance 2"
       $BUILDOUT_ROOT/bin/instance2 start
       echo "Starting instanceworker 1"
       $BUILDOUT_ROOT/bin/instanceworker1 start
   ;;
   start-zrs)
       echo "Starting ZEO Replication Service"
       $ZRS_BUILDOUT_ROOT/bin/zrsreplicator start
   ;;
   stop)
       echo "Stopping instanceworker 1"
       $BUILDOUT_ROOT/bin/instanceworker1 stop
       echo "Stopping instance 2"
       $BUILDOUT_ROOT/bin/instance2 stop
       echo "Stopping instance 1"
       $BUILDOUT_ROOT/bin/instance1 stop
       echo "Stopping ZEO server"
       $BUILDOUT_ROOT/bin/zeoserver stop
   ;;
   stop-zrs)
       echo "Stopping ZEO Replication Service"
       $ZRS_BUILDOUT_ROOT/bin/zrsreplicator stop
   ;;
   restart)
       echo "Stopping instanceworker 1"
       $BUILDOUT_ROOT/bin/instanceworker1 stop
       echo "Stopping instance 2"
       $BUILDOUT_ROOT/bin/instance2 stop
       echo "Stopping instance 1"
       $BUILDOUT_ROOT/bin/instance1 stop
       echo "Stopping ZEO server"
       $BUILDOUT_ROOT/bin/zeoserver stop
       echo "Starting ZEO server"
       $BUILDOUT_ROOT/bin/zeoserver start
       echo "Starting instance 1"
       $BUILDOUT_ROOT/bin/instance1 start
       echo "Starting instance 2"
       $BUILDOUT_ROOT/bin/instance2 start
       echo "Starting instanceworker 1"
       $BUILDOUT_ROOT/bin/instanceworker1 start
   ;;
   restart-zrs)
       echo "Stopping ZEO Replication Service"
       $ZRS_BUILDOUT_ROOT/bin/zrsreplicator stop
       echo "Starting ZEO Replication Service"
       $ZRS_BUILDOUT_ROOT/bin/zrsreplicator start
   ;;
   status)
       echo "Status of ZEO server"
       $BUILDOUT_ROOT/bin/zeoserver status
       echo "Status of instance 1"
       $BUILDOUT_ROOT/bin/instance1 status
       echo "Status of instance 2"
       $BUILDOUT_ROOT/bin/instance2 status
       echo "Status of instanceworker 1"
       $BUILDOUT_ROOT/bin/instanceworker1 status
   ;;
   status-zrs)
       echo "Status of ZEO Replication Service"
       $ZRS_BUILDOUT_ROOT/bin/zrsreplicator status
   ;;
esac
