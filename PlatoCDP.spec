# How to build it
# QA_RPATHS=$[ 0x0001|0x0002 ] rpmbuild -bb PlatoCDP.spec

Name:		PlatoCDP
Version:	4.0b1
Release:	1%{?dist}
Summary:	A Plone distribution for intranet use-cases

Group:		Applications/Internet
License:	GPLv2+
URL:		http://www.koslab.org
Source0:	%{name}-%{version}.tar.bz2

BuildRequires:	git python-devel python python-virtualenv python-setuptools
BuildRequires:  gcc gcc-c++ libxslt-devel libxml2-devel
BuildRequires:  libjpeg-turbo-devel libpng-devel zlib-devel bzip2-devel tk-devel
BuildRequires:  freetype-devel rubygems ghostscript wget openldap-devel
Requires:       %{name}-libs
Requires:       libreoffice-headless libreoffice-impress libreoffice-writer libreoffice-calc
Requires:       libreoffice-draw 
Requires:       GraphicsMagick poppler-utils haproxy varnish 
Requires:       ghostscript = 8.71
Requires:       rubygem-docsplit = 0.7.5
Requires:       python-virtualenv
Requires(post): chkconfig
Requires(postun) : chkconfig

%description
A Plone distribution for intranet use-cases

%package libs

Summary: Libraries and eggs for PlatoCDP
Group:  System Environment/Libraries
Requires(pre): shadow-utils glibc-common
Requires(postun): shadow-utils


%description libs
Precompiled libraries and eggs for PlatoCDP

%package ZRS

Summary: Replication service for PlatoCDP
Group: Applications/Databases
Requires: %{name}-libs rsync python-virtualenv
Requires(post): chkconfig
Requires(postun) : chkconfig


%description ZRS
Provide a ZEO Replication Server to replicate existing ZEO database

%prep
%setup -q

%build
mkdir -p %{buildroot}/%{_datadir}/%{name}/template/
cp -r * %{buildroot}/%{_datadir}/%{name}/template/

# build eggs
virtualenv --no-site-packages .
wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py
./bin/python bootstrap.py
cat site.cfg.sample | sed 's|/var/lib/PlatoCDP/data|`pwd`/var|g' \
    | sed 's|/var/log/PlatoCDP/|`pwd`/var/log|' >  site.cfg 
./bin/buildout -vvvv -c deployment.cfg
rm site.cfg

%install

# create directories
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/eggs/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/data/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/backups/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/zrs/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/zrs/data/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/zrs/data/filestorage/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/zrs/data/blobstorage/
mkdir -p %{buildroot}/%{_var}/lib/%{name}/zrs/backups/
mkdir -p %{buildroot}/%{_var}/cache/%{name}/
mkdir -p %{buildroot}/%{_var}/www/%{name}/
mkdir -p %{buildroot}/%{_sysconfdir}/init.d/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}/%{_var}/log/%{name}

# copy built eggs
cp -r eggs/* %{buildroot}/%{_var}/lib/%{name}/eggs/

# create deployment buildout 
rm -f %{buildroot}/%{_datadir}/%{name}/template/site.cfg
cp -r %{buildroot}/%{_datadir}/%{name}/template/* %{buildroot}/%{_var}/www/%{name}/
cp %{buildroot}/%{_var}/www/%{name}/site.cfg.sample %{buildroot}/%{_sysconfdir}/%{name}/platocdp.cfg
rm -f %{buildroot}/%{_var}/www/%{name}/site.cfg
ln -s %{_sysconfdir}/%{name}/platocdp.cfg %{buildroot}/%{_var}/www/%{name}/site.cfg 

# create buildout default.cfg
mkdir -p %{buildroot}/%{_var}/lib/%{name}/.buildout/
cat << EOF > %{buildroot}/%{_var}/lib/%{name}/.buildout/default.cfg 
[buildout]
download-cache = %{_var}/cache/%{name}/
eggs-directory = %{_var}/lib/%{name}/eggs/
extends-cache = %{_var}/cache/%{name}/
EOF

# create buildscript
cat << EOF > %{buildroot}/%{_bindir}/platocdp-rebuild
#!/bin/bash

if [ \`whoami\` != "root" ];then 
   echo "This script have to be run as root"
   exit
fi

cd %{_var}/www/%{name}
sudo -u plone virtualenv venv
sudo -u plone wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py -o /dev/null
sudo -u plone ./venv/bin/python bootstrap.py
sudo -u plone ./bin/buildout -c deployment.cfg
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/init.d/platocdp
#! /bin/bash
#
# platocdp       Bring up/down platocdp
#
# chkconfig: 345 99 01
# description: init script for platocdp

. /etc/init.d/functions

case "\$1" in 
   start)
       echo "Starting ZEO server"
       %{_var}/www/%{name}/bin/zeoserver start
       echo "Starting instance 1"
       %{_var}/www/%{name}/bin/instance1 start
       echo "Starting instance 2"
       %{_var}/www/%{name}/bin/instance2 start
       echo "Starting instanceworker 1"
       %{_var}/www/%{name}/bin/instanceworker1 start
   ;;
   stop)
       echo "Stopping instanceworker 1"
       %{_var}/www/%{name}/bin/instanceworker1 stop
       echo "Stopping instance 2"
       %{_var}/www/%{name}/bin/instance2 stop
       echo "Stopping instance 1"
       %{_var}/www/%{name}/bin/instance1 stop
       echo "Stopping ZEO server"
       %{_var}/www/%{name}/bin/zeoserver stop
   ;;
   restart)
       echo "Stopping instanceworker 1"
       %{_var}/www/%{name}/bin/instanceworker1 stop
       echo "Stopping instance 2"
       %{_var}/www/%{name}/bin/instance2 stop
       echo "Stopping instance 1"
       %{_var}/www/%{name}/bin/instance1 stop
       echo "Stopping ZEO server"
       %{_var}/www/%{name}/bin/zeoserver stop
       echo "Starting ZEO server"
       %{_var}/www/%{name}/bin/zeoserver start
       echo "Starting instance 1"
       %{_var}/www/%{name}/bin/instance1 start
       echo "Starting instance 2"
       %{_var}/www/%{name}/bin/instance2 start
       echo "Starting instanceworker 1"
       %{_var}/www/%{name}/bin/instanceworker1 start
   ;;
   status)
       echo "Status of ZEO server"
       %{_var}/www/%{name}/bin/zeoserver status
       echo "Status of instance 1"
       %{_var}/www/%{name}/bin/instance1 status
       echo "Status of instance 2"
       %{_var}/www/%{name}/bin/instance2 status
       echo "Status of instanceworker 1"
       %{_var}/www/%{name}/bin/instanceworker1 status
   ;;
esac

EOF

#################### ZRS ###########################

# create deployment buildout 
mkdir -p %{buildroot}/%{_var}/www/%{name}-zrs/
cp -r %{buildroot}/%{_datadir}/%{name}/template/zrs/* %{buildroot}/%{_var}/www/%{name}-zrs/
cp %{buildroot}/%{_var}/www/%{name}-zrs/site.cfg.sample %{buildroot}/%{_sysconfdir}/%{name}/zrs.cfg
rm -f %{buildroot}/%{_var}/www/%{name}-zrs/site.cfg
ln -s %{_sysconfdir}/%{name}/zrs.cfg %{buildroot}/%{_var}/www/%{name}-zrs/site.cfg 

# create buildscript
cat << EOF > %{buildroot}/%{_bindir}/platocdp-zrs-rebuild
#!/bin/bash

if [ \`whoami\` != "root" ];then 
   echo "This script have to be run as root"
   exit
fi

cd %{_var}/www/%{name}-zrs
sudo -u plone virtualenv venv
sudo -u plone wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py -o /dev/null
sudo -u plone ./venv/bin/python bootstrap.py
sudo -u plone ./bin/buildout -c buildout.cfg
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/init.d/platocdp-zrs
#! /bin/bash
#
# platocdp-zrs       Bring up/down platocdp-zrs
#
# chkconfig: 345 99 01
# description: init script for platocdp-zrs

. /etc/init.d/functions

case "\$1" in 
   start)
       echo "Starting ZEO Replication Service"
       %{_var}/www/%{name}-zrs/bin/zrsreplicator start
   ;;
   stop)
       echo "Stopping ZEO Replication Service"
       %{_var}/www/%{name}-zrs/bin/zrsreplicator stop
   ;;
   status)
       %{_var}/www/%{name}-zrs/bin/zrsreplicator status
   ;;
esac

EOF

rm -f %{buildroot}/%{_sysconfdir}/%{name}/site.cfg

%files
%defattr(-, plone, plone, -)
%{_datadir}/%{name}/template
%{_var}/www/%{name}
%config %{_sysconfdir}/%{name}/platocdp.cfg
%attr(755, root, root) %{_bindir}/platocdp-rebuild
%attr(755, root, root) %{_sysconfdir}/init.d/platocdp


%files libs
%defattr(-, plone, plone, -)
%{_var}/lib/%{name}
%{_var}/cache/%{name}
%{_var}/log/%{name}

%files ZRS
%defattr(-, plone, plone, -)
%{_var}/www/%{name}-zrs
%attr(755, root, root) %{_sysconfdir}/init.d/platocdp-zrs
%config %{_sysconfdir}/%{name}/zrs.cfg
%attr(755, root, root) %{_bindir}/platocdp-zrs-rebuild

%pre
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%pre libs
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%pre ZRS
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%post
chkconfig --add platocdp

%post ZRS
chkconfig --add platocdp-zrs

%postun 
chkconfig --del platocdp >/dev/null 2>&1 || :

%postun ZRS
chkconfig --del platocdp-zrs >/dev/null 2>&1 || :

%postun libs 
userdel plone >/dev/null 2>&1 || :

%changelog

