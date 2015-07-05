# PlatoCDP Instance
#
# Version 0.1
#

FROM kagesenshi/platocdp-base
MAINTAINER Izhar Firdaus <izhar@kagesenshi.org>

# base system
USER root
RUN  yum -y update; yum clean all
RUN  yum -y install supervisor

# update buildout
RUN rm -rf /opt/platocdp/
RUN git clone https://github.com/koslab/PlatoCDP.git /opt/platocdp
ADD http://downloads.buildout.org/2/bootstrap.py /opt/platocdp/bootstrap.py
RUN chown -R plone:plone /opt/platocdp/

# build development eggs
USER plone
WORKDIR /opt/platocdp/
RUN virtualenv venv;./venv/bin/python bootstrap.py
RUN ./bin/buildout -vvvv install utils devreleaser;./bin/devreleaser
RUN rm -rf dev/*

# construct buildout
ADD instance.cfg /opt/platocdp/instance.cfg
RUN ./bin/buildout -vvvv -c instance.cfg

USER root
VOLUME /logs

ADD supervisord.conf /etc/supervisord.d/platocdp.conf
ADD start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

EXPOSE 8080
CMD start.sh
