#
# Conditional build:
%bcond_with	apidocs		# API documentation (files missing in tarball)
%bcond_without	static_libs	# static libraries
#
Summary:	Implementation of HTTP/3 mapping over QUIC and QPACK in C
Summary(pl.UTF-8):	Implementacja w C odwzorowania HTTP/3 w oparciu o QUIC i QPACK
Name:		nghttp3
Version:	1.3.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ngtcp2/nghttp3/releases
Source0:	https://github.com/ngtcp2/nghttp3/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	7bb5c4e3c39e76931c64ea94d6f8cda8
URL:		https://github.com/ngtcp2/nghttp3
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	sphinx-pdg
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nghttp3 is an implementation of HTTP/3 mapping over QUIC and QPACK in
C.

It does not depend on any particular QUIC transport implementation.

%description -l pl.UTF-8
nghttp3 to implementacja w C odwzorowania HTTP/3 w oparciu o QUIC i
QPACK.

%package devel
Summary:	Header files for nghttp3 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki nghttp3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for nghttp3 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki nghttp3.

%package static
Summary:	Static nghttp3 library
Summary(pl.UTF-8):	Statyczna biblioteka nghttp3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static nghttp3 library.

%description static -l pl.UTF-8
Statyczna biblioteka nghttp3.

%package apidocs
Summary:	API documentation for nghttp3 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki nghttp3
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for nghttp3 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki nghttp3.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies, obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnghttp3.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/nghttp3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README.rst
%attr(755,root,root) %{_libdir}/libnghttp3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnghttp3.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnghttp3.so
%{_includedir}/nghttp3
%{_pkgconfigdir}/libnghttp3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnghttp3.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/*
%endif
