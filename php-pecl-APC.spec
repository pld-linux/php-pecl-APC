# TODO
# - maybe related:
#  - http://pecl.php.net/bugs/bug.php?id=7141
%define		php_name	php%{?php_suffix}
%define		modname	APC
%define		status		beta
Summary:	%{modname} - Alternative PHP Cache
Summary(pl.UTF-8):	%{modname} - alternatywne cache PHP
Name:		%{php_name}-pecl-%{modname}
Version:	3.1.13
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	c9e47002e3a67ebde3a6f81437c7b6e0
URL:		http://pecl.php.net/package/APC/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
APC is the Alternative PHP Cache. It was conceived of to provide a
free, open, and robust framework for caching and optimizing PHP
intermediate code.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
APC to alternatywne cache PHP. W wyobrażeniach miało dostarczać
wolnodostępny, otwarty i potężny szkielet do buforowania i
optymalizowania kodu pośredniego PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

cat <<'EOF' > %{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
apc.enabled=1
;apc.optimization=0
;apc.shm_segments=1
;apc.shm_size=32
;apc.cache_by_default=1
;apc.max_file_size=1M
;apc.num_files_hint=1024
;apc.gc_ttl=3600
;apc.ttl=0
;apc.mmap_file_mask=/tmp/apc.XXXXXX
;apc.filters=
;apc.stat=1
;apc.enable_cli=0
EOF

%build
phpize
%configure \
	--%{!?debug:dis}%{?debug:en}able-apc-debug \
	--enable-apc-mmap
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D modules/apc.so $RPM_BUILD_ROOT%{php_extensiondir}/%{modname}.so
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL NOTICE apc.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
