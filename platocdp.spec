# How to build it
# QA_RPATHS=$[ 0x0001|0x0002 ] rpmbuild -bb platocdp.spec

%global _python_bytecompile_errors_terminate_build 0
%global _build_development_rpm 1

Name:		platocdp
Version:	4.3.4
Release:	%(date +%%Y%%m%%d)%{?dist}
Summary:	A Plone distribution for intranet use-cases

Group:		Applications/Internet
License:	GPLv2+
URL:		http://www.koslab.org
Source0:	%{name}-%{version}.tar.bz2

BuildRequires:	git python-devel python python-virtualenv python-setuptools
BuildRequires:  gcc gcc-c++ libxslt-devel libxml2-devel
BuildRequires:  libjpeg-turbo-devel libpng-devel zlib-devel bzip2-devel tk-devel
BuildRequires:  freetype-devel rubygems ghostscript wget openldap-devel
BuildRequires:  java-1.7.0-openjdk java-1.7.0-openjdk-devel chrpath
Requires:       %{name}-libs = %{version}
Requires:       libreoffice-headless libreoffice-impress libreoffice-writer libreoffice-calc
Requires:       libreoffice-draw 
Requires:       GraphicsMagick poppler-utils haproxy varnish 
Requires:       ghostscript
Requires:       rubygem-docsplit = 0.7.5
Requires:       python-virtualenv wv
Requires:       java-1.7.0-openjdk tkinter libtidy
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

%package eggbasket

Summary: Downloaded source tarballs used by PlatoCDP
Group: System Environment/Libraries

%description eggbasket
Source tarballs and config files used for building PlatoCDP

%package zrs

Summary: Replication service for PlatoCDP
Group: Applications/Databases
Requires: %{name}-libs rsync python-virtualenv
Requires(post): chkconfig
Requires(postun) : chkconfig


%description zrs
Provide a ZEO Replication Server to replicate existing ZEO database

%prep
%setup -q -n PlatoCDP

%build
# build eggs
virtualenv --no-site-packages .
wget http://downloads.buildout.org/2/bootstrap.py -O bootstrap.py
./bin/python bootstrap.py
cat site.cfg.sample | sed 's|/var/lib/platocdp/data|var|g' \
    | sed 's|/var/log/platocdp/|var/log|' \
    | sed 's|sites = defaultsite|sites =|' >  site.cfg 

%if 0%{?rhel} >= 7
    cp templates/varnish.vcl.in-varnish4 templates/varnish.vcl.in
%endif

%if 0%{?rhel} == 6
    cp templates/varnish.vcl.in-varnish3 templates/varnish.vcl.in
%endif

%if 0%{?_build_development_rpm} == 1
    # release eggs
    ./bin/buildout -vvvv install utils devreleaser
    ./bin/devreleaser
    if [ $? -ne 0 ];then
        exit 1    
    fi
%endif

cat << EOF > build.cfg
[buildout]
extends=deployment.cfg
eggs-directory=eggs
download-cache=downloads
extends-cache=downloads
EOF
mkdir downloads/
I=1
C=0
while [ "x$I" != "x0" ];do
    ./bin/buildout -vvvv -U -c build.cfg
    I=$?
    C=$(($C + 1))
    if [ $C -gt 10 ];then
        exit 1
    fi
done
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
mkdir -p %{buildroot}/%{_datadir}/%{name}/template/

# copy sources
tar xvf %{SOURCE0}
cp -r PlatoCDP/* %{buildroot}/%{_datadir}/%{name}/template/

%if 0%{?_build_development_rpm} == 1
    cp releaseversions.cfg %{buildroot}/%{_datadir}/%{name}/template/
%endif

# copy built eggs
cp -r eggs/* %{buildroot}/%{_var}/lib/%{name}/eggs/

# clean up paths

%if 0%{?rhel} >= 7
    find %{buildroot}/%{_var}/lib/%{name}/eggs/ -type f -exec sed -i "s|`pwd`/bin/python|/bin/python|g" '{}' ';'
    find %{buildroot}/%{_var}/lib/%{name}/eggs/ -type f -exec sed -i "s|/opt/local/bin/python2.4|/bin/python|g" '{}' ';'
%endif

%if 0%{?rhel} == 6
    find %{buildroot}/%{_var}/lib/%{name}/eggs/ -type f -exec sed -i "s|`pwd`/bin/python|/usr/bin/python|g" '{}' ';'
    find %{buildroot}/%{_var}/lib/%{name}/eggs/ -type f -exec sed -i "s|/opt/local/bin/python2.4|/usr/bin/python|g" '{}' ';'
%endif


# copy tarballs
cp -r downloads/* %{buildroot}/%{_var}/cache/%{name}

# create deployment buildout 
rm -f %{buildroot}/%{_datadir}/%{name}/template/site.cfg
cp -r %{buildroot}/%{_datadir}/%{name}/template/* %{buildroot}/%{_var}/www/%{name}/

%if 0%{?rhel} >= 7
    cp %{buildroot}/%{_var}/www/%{name}/templates/varnish.vcl.in-varnish4 %{buildroot}/%{_var}/www/%{name}/templates/varnish.vcl.in
%endif

%if 0%{?rhel} == 6
    cp %{buildroot}/%{_var}/www/%{name}/templates/varnish.vcl.in-varnish3 %{buildroot}/%{_var}/www/%{name}/templates/varnish.vcl.in
%endif

sed -i "s|platocdp/|%{name}/|g" %{buildroot}/%{_var}/www/%{name}/site.cfg.sample
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

sed 's|@@BUILDOUT_ROOT@@|%{_var}/www/%{name}|g' scripts/platocdp.sh > %{buildroot}/%{_bindir}/%{name}

cat << EOF > %{buildroot}/%{_sysconfdir}/init.d/%{name}
#! /bin/bash
#
# platocdp       Bring up/down platocdp
#
# chkconfig: 345 99 01
# description: init script for platocdp

. /etc/init.d/functions

case "\$1" in 
   start)
       %{_bindir}/%{name} start
   ;;
   stop)
       %{_bindir}/%{name} stop
   ;;
   restart)
       %{_bindir}/%{name} restart
   ;;
   status)
       %{_bindir}/%{name} status
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

sed 's|@@BUILDOUT_ROOT@@|%{_var}/www/%{name}-zrs|g' scripts/platocdp-zrs.sh > %{buildroot}/%{_bindir}/%{name}-zrs

cat << EOF > %{buildroot}/%{_sysconfdir}/init.d/%{name}-zrs
#! /bin/bash
#
# platocdp-zrs       Bring up/down platocdp-zrs
#
# chkconfig: 345 99 01
# description: init script for platocdp-zrs

. /etc/init.d/functions

case "\$1" in 
   start)
      %{_bindir}/%{name}-zrs start
   ;;
   stop)
      %{_bindir}/%{name}-zrs stop
   ;;
   status)
       %{_bindir}/%{name}-zrs status
   ;;
esac

EOF

rm -f %{buildroot}/%{_sysconfdir}/%{name}/site.cfg

%files
%defattr(-, plone, plone, -)
%{_datadir}/%{name}/template
%{_var}/www/%{name}
%config %{_sysconfdir}/%{name}/platocdp.cfg
%attr(755, root, root) %{_bindir}/%{name}
%attr(755, root, root) %{_sysconfdir}/init.d/%{name}


%files libs
%defattr(-, plone, plone, -)
%{_var}/lib/%{name}
%dir %{_var}/cache/%{name}
%{_var}/log/%{name}

%files eggbasket
%defattr(-, plone, plone, -)
%{_var}/cache/%{name}

%files zrs
%defattr(-, plone, plone, -)
%{_var}/www/%{name}-zrs
%attr(755, root, root) %{_sysconfdir}/init.d/%{name}-zrs
%config %{_sysconfdir}/%{name}/zrs.cfg
%attr(755, root, root) %{_bindir}/%{name}-zrs

%pre
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%pre libs
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%pre zrs
getent group plone >/dev/null || /usr/sbin/groupadd -r plone
getent passwd plone >/dev/null || /usr/sbin/useradd -r -g plone -d %{_var}/lib/%{name}/ -s /bin/false plone

%post
chkconfig --add %{name}

%post zrs
chkconfig --add %{name}-zrs

%postun 
chkconfig --del %{name} >/dev/null 2>&1 || :

%postun zrs
chkconfig --del %{name}-zrs >/dev/null 2>&1 || :

%postun libs 
userdel plone >/dev/null 2>&1 || :

%changelog
* Mon Mar 23 2015 Izhar Firdaus <izhar@kagesenshi.org> 4.3.4-5
- add support for both centos6 and centos7

* Thu Dec 25 2014 Izhar Firdaus <izhar@kagesenshi.org> 4.3.4-1
- update rebuild for plone 4.3.4

