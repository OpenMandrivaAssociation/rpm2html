Name:           rpm2html
Version:        1.11.2
Release:        %mkrel 2
Summary:        Translates rpm database into HTML and RDF info
License:        MIT
Group:          Networking/WWW
URL:            http://www.nongnu.org/rpm2html/
Source0:        http://savannah.nongnu.org/download/rpm2html/rpm2html-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/rpm2html/rpm2html-%{version}.tar.gz.sig
# cvs -z3 -d:pserver:anonymous@cvs.savannah.nongnu.org:/sources/rpm2html co -rRPM2HTML_1_9_5 rpm2html
# tar xf rpm2html-mysql-1.9.5.tar.bz2
# for i in rpm2html/*; do if test -f rpm2html-mysql/$i; then cp $i -avf ../rpm2html-mysql/$i; fi; done
# tar cjf rpm2html-mysql-1.9.5.tar.bz2 rpm2html-mysql
Source2:        rpm2html-mysql-1.9.5.tar.bz2
Source3:        rpm2html.bashrc
Source4:        rpm2html.sql
Patch0:         rpm2html-1.8.2-no_db.patch
Patch1:         rpm2html-1.8.1-mysql.patch
Patch2:         rpm2html-1.9.2-rpm2html_config.patch
Patch3:         rpm2html-1.9.2-mysql-release.patch
Patch4:		rpm2html-1.11.2-rpm5.patch
Requires:       gnupg
BuildRequires:  autoconf2.5
BuildRequires:  automake1.7
BuildRequires:  bzip2-devel
BuildRequires:  gnupg
BuildRequires:  libintl
BuildRequires:  libpopt-devel
BuildRequires:  librpm-devel
BuildRequires:  libxml2-devel
BuildRequires:  libz-devel
BuildRequires:  mysql-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The rpm2html utility automatically generates web pages that describe a
set of RPM packages.  The goals of rpm2html are to identify the
dependencies between various packages, and to find the package(s) that
will provide the resources needed to install a given package.
Rpm2html analyzes the provides and requires of the given set of RPMs,
and then shows the dependency cross-references using hypertext links.
Rpm2html can now dump the metadata associated with RPM files into
standard RDF files.

Install rpm2html if you want a utility for translating information
from an RPM database into HTML.

%package mysql
Summary:        Translates rpm database into HTML and RDF info
Group:          Networking/WWW
Requires:       %{name} = %{version}
Requires:       apache
Requires:       mod_php
Requires:       php-common
Requires:       php-mysql

%description mysql
The rpm2html-mysql utility automatically generates web pages that describe a
set of RPM packages.  The goals of rpm2html are to identify the
dependencies between various packages, and to find the package(s) that
will provide the resources needed to install a given package.
Rpm2html analyzes the provides and requires of the given set of RPMs,
and then shows the dependency cross-references using hypertext links.
Rpm2html can now dump the metadata associated with RPM files into
standard RDF files.

Install rpm2html-mysql if you want a utility for translating information
from an RPM database into HTML.

This package contains the nessesary files to enable MySQL support.

%prep
%setup -q -a2
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p1 -b .rpm5~
rm -f configure Makefile
autoreconf -fi

# tag it with the correct version (duh!, at what point did this work?)
%{__perl} -pi -e "s|^#define RPM2HTML_VER.*|#define RPM2HTML_VER \"%{version}-%{release}\"|g" rpm2html.h

# fix tag
%{__perl} -pi -e "s|RPMTAG_COPYRIGHT|RPMTAG_LICENSE|" rpmopen.c

%build
export WANT_AUTOCONF_2_5=1
%{__libtoolize} --copy --force
%{_bindir}/aclocal-1.7
%{__autoconf}
%{_bindir}/automake-1.7 --add-missing

# first build without MySQL support
%configure2_5x --sysconfdir=%{_sysconfdir} --with-gpg
%make
%{__mv} %{name} %{name}-bin-std

# build with MySQL support
%make clean
%configure2_5x --sysconfdir=%{_sysconfdir} --with-gpg --with-sql
%make
%{__mv} %{name} %{name}-bin-mysql

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}/var/www/html/%{name}-mysql

%{__install} -m 755 %{name}-bin-std %{buildroot}%{_bindir}/%{name}
%{__install} -m 755 %{name}-bin-mysql %{buildroot}%{_bindir}/%{name}-mysql
%{__install} -m 755 sqltools %{buildroot}%{_bindir}/

%{__install} -m 644 msg.* %{buildroot}%{_datadir}/%{name}/
%{__install} -m 644 %{name}.config %{buildroot}%{_sysconfdir}
%{__install} -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/rpm2html.1

%{__install} -m 644 rpm2html-mysql/*.html %{buildroot}/var/www/html/%{name}-mysql/
%{__install} -m 644 rpm2html-mysql/*.gif %{buildroot}/var/www/html/%{name}-mysql/
%{__install} -m 644 rpm2html-mysql/*.php %{buildroot}/var/www/html/%{name}-mysql/

%{__cat} %{SOURCE3} > rpm2html.bashrc
%{__chmod} 755 rpm2html.bashrc
%{__cat} %{SOURCE4} > rpm2html.sql

%post                mysql
echo "%{_bindir}/%{name}-mysql and %{_bindir}/sqltools will segfault if environment"
echo "variables outlined in %{_docdir}/%{name}-mysql-%{version}/rpm2html.bashrc is unset."

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc BUGS CHANGES ChangeLog Copyright INSTALL PRINCIPLES README TODO
%doc %{name}*.config* rpm2html-mysql/rpm2html.config.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.config
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0644,root,root) %{_datadir}/%{name}/msg.*
%attr(0644,root,root) %{_mandir}/man1/%{name}.1*

%files mysql
%defattr(0644,root,root,0755)
%doc rpm2html-mysql/rpm2html-mysql-setup.txt rpm2html.bashrc rpm2html.sql
%doc rpm2html-mysql/*.py
%attr(0755,root,root) %{_bindir}/%{name}-mysql
%attr(0755,root,root) %{_bindir}/sqltools
%attr(0644,root,root) /var/www/html/%{name}-mysql/*
