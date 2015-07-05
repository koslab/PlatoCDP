#!/bin/bash

DBNAME=${PLATOCDP_DB_NAME:-platocdp}
DBUSER=${PLATOCDP_DB_USER:-platocdp}
DBPASS=${PLATOCDP_DB_PASS:-platocdp}
DBASYNC=${PLATOCDP_DB_ASYNC:-platocdp_async}

SUNAME=${PGSQL_SU_NAME:-pgadmin}
SUPASS=${PGSQL_SU_PASS:-pgadmin}

function pg_createsu {
    su postgres -c "postgres --single -D /var/lib/pgsql/data <<< \"CREATE USER $1 WITH SUPERUSER PASSWORD '$2'\""
}

function pg_createuser {
    su postgres -c "postgres --single -D /var/lib/pgsql/data <<< \"CREATE USER $1 WITH PASSWORD '$2'\""
}

function pg_createdb {
    su postgres -c "postgres --single -D /var/lib/pgsql/data <<< \"CREATE DATABASE $1 OWNER $2\""
}

chmod a+rw /logs
if [ ! -f /var/lib/pgsql/data/pg_hba.conf ];then
    chown postgres:postgres /var/lib/pgsql/data
    su postgres -c "initdb /var/lib/pgsql/data"
    pg_createsu $SUNAME $SUPASS
    pg_createuser $DBUSER $DBPASS
    pg_createdb $DBNAME $DBUSER
    pg_createdb $DBASYNC $DBUSER
    echo "host all all 0.0.0.0/0 md5" >> /var/lib/pgsql/data/pg_hba.conf
    echo "listen_addresses='*'" >> /var/lib/pgsql/data/postgresql.conf
fi

supervisord -c /etc/supervisord.d/pgsql.conf
