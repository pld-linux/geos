Summary:	Geometry Engine - Open Source
Summary(pl.UTF-8):	GEOS - silnik geometryczny z otwartymi źródłami
Name:		geos
Version:	3.13.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
# Source0-md5:	7dda2ea78f394c7d460f6e81a215087c
URL:		https://libgeos.org/
BuildRequires:	cmake
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.519
Obsoletes:	geos-static < 3.13.0
Obsoletes:	python-geos < 3.13.0
Obsoletes:	ruby-geos < 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java
Topology Suite (JTS). As such, it aims to contain the complete
functionality of JTS in C++. This includes all the OpenGIS "Simple
Features for SQL" spatial predicate functions and spatial operators,
as well as specific JTS topology functions such as IsValid().

%description -l pl.UTF-8
GEOS (Geometry Engine - Open Source, czyli silnik geometryczny z
otwartymi źródłami) to port C++ biblioteki Java Topology Suite (JTS).
Celem biblioteki jako takiej jest implementacja pełnej funkcjonalności
JTS w C++. Obejmuje to wszystkie funkcje predykatów przestrzennych wg
"Simple Features for SQL" OpenGIS oraz operatory przestrzenne, a także
specyficzne dla JTS funkcje topologiczne takie jak IsValid().

%package devel
Summary:	Header files for GEOS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for GEOS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GEOS.

%prep
%setup -q

%build
mkdir -p build
cd build
%cmake ../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS.md README.md
%attr(755,root,root) %{_bindir}/geosop
%attr(755,root,root) %{_libdir}/libgeos.so.%{version}
%attr(755,root,root) %{_libdir}/libgeos_c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeos_c.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/geos-config
%attr(755,root,root) %{_libdir}/libgeos.so
%attr(755,root,root) %{_libdir}/libgeos_c.so
%{_includedir}/geos
%{_includedir}/geos.h
%{_includedir}/geos_c.h
%{_libdir}/cmake/GEOS
%{_pkgconfigdir}/geos.pc
