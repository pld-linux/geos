Summary:	Geometry Engine - Open Source
Summary(pl):	GEOS - silnik geometryczny z otwartymi ¼ród³ami
Name:		geos
Version:	2.1.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://geos.refractions.net/%{name}-%{version}.tar.bz2
# Source0-md5:	076f1bfb17e13d4075b0345f5ca525ca
Patch0:		%{name}-config.patch
URL:		http://geos.refractions.net/
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java
Topology Suite (JTS). As such, it aims to contain the complete
functionality of JTS in C++. This includes all the OpenGIS "Simple
Features for SQL" spatial predicate functions and spatial operators,
as well as specific JTS topology functions such as IsValid().

%description -l pl
GEOS (Geometry Engine - Open Source, czyli silnik geometryczny z
otwartymi ¼ród³ami) to port C++ biblioteki Java Topology Suite (JTS).
Celem biblioteki jako takiej jest implementacja pe³nej funkcjonalno¶ci
JTS w C++. Obejmuje to wszystkie funkcje predykatów przestrzennych
wg "Simple Features for SQL" OpenGIS oraz operatory przestrzenne, a
tak¿e specyficzne dla JTS funkcje topologiczne takie jak IsValid().

%package devel
Summary:	Header files for GEOS library
Summary(pl):	Pliki nag³ówkowe biblioteki GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for GEOS library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GEOS.

%package static
Summary:	Static GEOS library
Summary(pl):	Statyczna biblioteka GEOS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GEOS library.

%description static -l pl
Statyczna biblioteka GEOS.

%prep
%setup -q
%patch0 -p1

%build
cp -f /usr/share/automake/config.* .
%configure
%{__make} \
	pkglibdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkglibdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/geos-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/geos
%{_includedir}/geos.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
