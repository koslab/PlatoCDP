# CentOS based PgSQL for PlatoCDP

FROM centos:centos7
MAINTAINER Izhar Firdaus <izhar@kagesenshi.org>

# base system
RUN  yum -y update; yum clean all
RUN  yum -y install epel-release
RUN  yum -y install haproxy
RUN  yum -y install supervisor
RUN  yum -y install python-genshi

ADD supervisord.conf /etc/supervisord.d/haproxy.conf

ADD haproxy_config.py /usr/local/bin/haproxy_config.py
RUN chmod a+x /usr/local/bin/haproxy_config.py
ADD start.sh /usr/local/bin/start.sh
RUN chmod a+x /usr/local/bin/start.sh

VOLUME /logs

EXPOSE 80
CMD start.sh
