# TODO
# - maybe related:
#  - http://pecl.php.net/bugs/bug.php?id=7141
%define		_modname	APC
%define		_status		beta
Summary:	%{_modname} - Alternative PHP Cache
Summary(pl.UTF-8):	%{_modname} - alternatywne cache PHP
Name:		php-pecl-%{_modname}
Version:	3.1.10
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	f4a6b91903d6ba9dce89fc87bb6f26c9
URL:		http://pecl.php.net/package/APC/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
APC is the Alternative PHP Cache. It was conceived of to provide a
free, open, and robust framework for caching and optimizing PHP
intermediate code.

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
APC to alternatywne cache PHP. W wyobrażeniach miało dostarczać
wolnodostępny, otwarty i potężny szkielet do buforowania i
optymalizowania kodu pośredniego PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

cat <<'EOF' > %{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
cd %{_modname}-%{version}
phpize
%configure \
	--%{!?debug:dis}%{?debug:en}able-apc-debug \
	--enable-apc-mmap
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D %{_modname}-%{version}/modules/apc.so $RPM_BUILD_ROOT%{php_extensiondir}/%{_modname}.so

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

cp -a %{_modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini

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
%doc %{_modname}-%{version}/{CHANGELOG,INSTALL,NOTICE,apc.php}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
