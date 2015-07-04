# PlatoCDP Base
#
# Version 0.1
#

FROM centos:centos7
MAINTAINER Izhar Firdaus <izhar@kagesenshi.org>

# base system
RUN  yum -y update; yum clean all
RUN  yum -y install epel-release

# core platocdp dependencies
RUN  yum -y install git python-devel python python-virtualenv python-setuptools
RUN  yum -y install gcc gcc-c++ libxslt-devel libxml2-devel
RUN  yum -y install libjpeg-turbo-devel libpng-devel zlib-devel bzip2-devel tk-devel
RUN  yum -y install freetype-devel rubygems ghostscript wget openldap-devel
RUN  yum -y install java-1.7.0-openjdk java-1.7.0-openjdk-devel chrpath
RUN  yum -y install libreoffice-headless libreoffice-impress libreoffice-writer libreoffice-calc
RUN  yum -y install libreoffice-draw GraphicsMagick poppler-utils haproxy varnish ghostscript
RUN  yum -y install python-virtualenv wv
RUN  yum -y install java-1.7.0-openjdk tkinter libtidy
RUN  yum -y install postgresql-devel postgresql

# documentviewer dependencies
RUN  gem install docsplit -v 0.7.5

# create user
RUN  /usr/sbin/groupadd -r plone; /usr/sbin/useradd -r -g plone -d /var/lib/platocdp -s /bin/false plone
RUN mkdir -p /var/lib/platocdp/.buildout; chown -R plone:plone /var/lib/platocdp

# default.cfg
RUN mkdir -p /var/platocdp/{cache,eggs}; chown -R plone:plone /var/platocdp
ADD buildout-default.cfg /var/lib/platocdp/.buildout/default.cfg

# create buildoutdir
RUN git clone https://github.com/koslab/PlatoCDP.git /opt/platocdp
ADD http://downloads.buildout.org/2/bootstrap.py /opt/platocdp/bootstrap.py
ADD eggcache.cfg /opt/platocdp/eggcache.cfg
ADD build.sh /tmp/build.sh
RUN chown -R plone:plone /opt/platocdp

# build cache
USER plone
RUN sh /tmp/build.sh
