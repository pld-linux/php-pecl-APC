%define		_modname	APC
%define		_status		stable

Summary:	%{_modname} - Alternative PHP Cache
Summary(pl):	%{_modname} - alternatywne cache PHP
Name:		php-pecl-%{_modname}
Version:	2.0.3
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	06d27f39d2e0fe9b31c319996b7b6cad
URL:		http://pecl.php.net/package/APC/
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
APC is the Alternative PHP Cache. It was conceived of to provide a
free, open, and robust framework for caching and optimizing PHP
intermediate code.

This extension has in PEAR status: %{_status}.

%description -l pl
APC to alternatywne cache PHP. W wyobra¿eniach mia³o dostarczaæ
wolnodostêpny, otwarty i potê¿ny szkielet do buforowania i
optymalizowania kodu po¶redniego PHP.

To rozszerzenie ma w PEAR status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/apc.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CHANGELOG,INSTALL,NOTICE}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
