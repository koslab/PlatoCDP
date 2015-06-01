=========================================
PlatoCDP : Plato Content & Data Platform
=========================================

Introduction
============

PlatoCDP is a system for knowledge management, data management, and data visualization platform.
Built on top of Plone, it provides full featured CMS capabilities provided by Plone such as its powerful 
content type system, search engine, various integration capabilities, alongside additional functionalities 
as listed below:

* Data Visualization dashboards (TBD)
* Data Visualization maps (TBD)
* Data Management system ala CKAN (TBD)
* Document Preview powered by collective.documentviewer (WIP)
* Pluggable component to register new visualizations (TBD)
* Responsive design theme powered by DevOOPS (WIP)
* JWT Authentication Provider (TBD)
* OAuth Authentication Provider (Wishlist)
* Integration with Hadoop ecosystem for ELT/ETL (Wishlist)

The end goal is to have an easy to use, easy to customize, flexible platform for building Enterprise Data Portal 
with integration with various Big Data backend technologies.

Bundled Add-ons
----------------

Following are the bundled add-ons in this distribution. WIP (Work-in-Progress) add-ons are still undergoing 
integration and compatibility fixes as PlatoCDP uses JQuery 1.9.1 and Bootstrap 3.3.1. Assistance on fixing
them is really appreciated.

* Dexterity Content Types 
* Diazo Theming Engine
* Unslider Portlet 
* Portlet Page 
* LDAP Integration
* Document Viewer (WIP)
* Solgema Fullcalendar (WIP)
* EEA Faceted Navigation (WIP)
* Content Well Portlets (WIP)
* Plone True Gallery (WIP)
* Quick Upload (WIP)


Deploying development Buildout
===============================

You will need these to be installed for some dependencies to build properly:

* python-virtualenv 
* python-devel 
* python-setuptools
* libxslt-devel 
* libxml2-devel
* libjpeg-turbo-devel 
* libpng-devel 
* zlib-devel 
* bzip2-devel 
* tk-devel
* freetype-devel 
* rubygems 
* ghostscript 
* openldap-devel

To get documentviewer to work properly, follow the instructions to prepare docsplit on this url:

  https://github.com/collective/collective.documentviewer/blob/master/CENTOS-INSTALL.rst

Afterwards checkout the repository and build it using virtualenv::

  git clone https://github.com/koslab/PlatoCDP.git
  cd PlatoCDP/
  virtualenv venv/
  ./venv/bin/python bootstrap.py
  ./bin/buildout -vvvv
  
To start the instance, run::

  ./bin/instance fg
  
Releasing the development eggs
===============================

There is a helper releaser script installed in ``./bin/`` directory, which can be used to automatically
release all development eggs in the buildout. To use it, you'll need ``zest.releaser`` to be installed
in your global python.

As root, run::

  pip install zest.releaser
  
Then you can run the releaser as normal user::

  ./bin/releaser.py
  
Building the RPM
=================

PlatoCDP includes a RPM Specfile that can be used to build the distribution for CentOS6 and CentOS7. To build
you will need a CentOS machine with ``rpmdevtools`` installed. Then the package can be built through::

  # replace ${version} with the package version from platocdp.spec
  git clone  https://github.com/koslab/PlatoCDP.git PlatoCDP
  tar cvjf platocdp-${version}.tar.bz2 PlatoCDP
  rpmbuild -ta platocdp-${version}.tar.bz2
  
**NOTE:** The RPM can only handle production build

Using the (almost) nightly RPM
-------------------------------

Latest RPM builds for CentOS6 and CentOS7 are available at http://nightly.koslab.org/nightly/

To setup repository, create ``/etc/yum.repos.d/koslab.repo``::

    [koslab-nightly]
    name=KOSLAB Nightly Repository
    baseurl=http://nightly.koslab.org/nightly/EL$releasever/
    enabled=1
    gpgcheck=0

Install packages::

    yum install platocdp-nightly

Initialize buildout::

    platocdp-nightly rebuild

Start instances::

    platocdp-nightly start



Credits
========

PlatoCDP Team

* Izhar Firdaus <kagesenshi.87@gmail.com>
* Your Name Here

PlatoCDP is built on top of the awesome work done by Plone contributors worldwide. Check out the CMS here:

* http://www.plone.org
