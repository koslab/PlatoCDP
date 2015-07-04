# CentOS based PgSQL for PlatoCDP

FROM centos:centos7
MAINTAINER Izhar Firdaus <izhar@kagesenshi.org>

# base system
RUN  yum -y update; yum clean all
RUN  yum -y install epel-release
RUN  yum -y install postgresql-server
RUN  yum -y install supervisor

ADD supervisord.conf /etc/supervisord.d/pgsql.conf

ADD start.sh /usr/local/bin/start.sh
RUN chmod a+x /usr/local/bin/start.sh

VOLUME /var/lib/pgsql/data/
VOLUME /logs

CMD start.sh
