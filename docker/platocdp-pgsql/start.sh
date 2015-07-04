#!/bin/bash

cat << EOF > /tmp/init.sql
CREATE USER platocdp WITH SUPERUSER PASSWORD 'platocdp';
CREATE DATABASE platocdp OWNER platocdp;
EOF

chmod a+rw /logs
if [ ! -f /var/lib/pgsql/data/pg_hba.conf ];then
    chown postgres:postgres /var/lib/pgsql/data
    su postgres -c "initdb /var/lib/pgsql/data"
    su postgres -c "postgres --single -D /var/lib/pgsql/data <<< \"CREATE USER platocdp WITH SUPERUSER PASSWORD 'platocdp'\""
    su postgres -c "postgres --single -D /var/lib/pgsql/data <<< \"CREATE DATABASE platocdp OWNER platocdp;\""
    echo "host all all 0.0.0.0/0 md5" >> /var/lib/pgsql/data/pg_hba.conf
    echo "listen_addresses='*'" >> /var/lib/pgsql/data/postgresql.conf
fi

supervisord -c /etc/supervisord.d/pgsql.conf
