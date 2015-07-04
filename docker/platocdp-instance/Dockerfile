# PlatoCDP Instance
#
# Version 0.1
#

FROM kagesenshi/platocdp-base
MAINTAINER Izhar Firdaus <izhar@kagesenshi.org>

# base system
USER root
RUN  yum -y update; yum clean all

WORKDIR /opt/platocdp/
RUN git pull

USER plone
ADD instance.cfg /opt/platocdp/instance.cfg
RUN ./bin/buildout -vvvv -c instance.cfg

EXPOSE 8080

CMD /opt/platocdp/bin/instance console
