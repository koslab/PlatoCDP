#!/bin/bash

chmod a+rw /logs
if [ ! -f /var/lib/pgsql/data/pg_hba.conf ];then
    chown postgres:postgres /var/lib/pgsql/data
    su postgres -c "initdb /var/lib/pgsql/data"
fi

supervisord -c /etc/supervisord.d/pgsql.conf
