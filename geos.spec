%define		_rc	rc4
Summary:	Geometry Engine - Open Source
Summary(pl):	GEOS - silnik geometryczny z otwartymi �r�d�ami
Name:		geos
Version:	3.0.0
Release:	0.%{_rc}.1
License:	LGPL
Group:		Libraries
Source0:	http://geos.refractions.net/%{name}-%{version}%{_rc}.tar.bz2
# Source0-md5:	90d4dba51dd75f8f1f12378e0f910d76
URL:		http://geos.refractions.net/
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	ruby-devel
BuildRequires:	swig-python >= 1.3.29
BuildRequires:	swig-ruby >= 1.3.29
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java
Topology Suite (JTS). As such, it aims to contain the complete
functionality of JTS in C++. This includes all the OpenGIS "Simple
Features for SQL" spatial predicate functions and spatial operators,
as well as specific JTS topology functions such as IsValid().

%description -l pl
GEOS (Geometry Engine - Open Source, czyli silnik geometryczny z
otwartymi �r�d�ami) to port C++ biblioteki Java Topology Suite (JTS).
Celem biblioteki jako takiej jest implementacja pe�nej funkcjonalno�ci
JTS w C++. Obejmuje to wszystkie funkcje predykat�w przestrzennych
wg "Simple Features for SQL" OpenGIS oraz operatory przestrzenne, a
tak�e specyficzne dla JTS funkcje topologiczne takie jak IsValid().

%package devel
Summary:	Header files for GEOS library
Summary(pl):	Pliki nag��wkowe biblioteki GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for GEOS library.

%description devel -l pl
Pliki nag��wkowe biblioteki GEOS.

%package static
Summary:	Static GEOS library
Summary(pl):	Statyczna biblioteka GEOS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GEOS library.

%description static -l pl
Statyczna biblioteka GEOS.

%package -n python-geos
Summary:	Python bindings for Geometry Engine - Open Source
Summary(pl):	Wi�zania Pythona do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-geos
Python bindings for Geometry Engine - Open Source.

%description -n python-geos -l pl
Wi�zania Pythona do biblioteki GEOS.

%package -n ruby-geos
Summary:	Ruby bindings for Geometry Engine - Open Source
Summary(pl):	Wi�zania j�zyka Ruby do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n ruby-geos
Ruby bindings for Geometry Engine - Open Source.

%description -n ruby-geos -l pl
Wi�zania j�zyka Ruby do biblioteki GEOS.

%prep
%setup -q -n %{name}-%{version}%{_rc}

%build
cp -f /usr/share/automake/config.* .
%configure \
	--enable-python \
	--enable-ruby
%{__make} \
	pkglibdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkglibdir=%{_libdir}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeos-*.*.*.so
%attr(755,root,root) %{_libdir}/libgeos_c.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/geos-config
%attr(755,root,root) %{_libdir}/libgeos.so
%attr(755,root,root) %{_libdir}/libgeos_c.so
%{_libdir}/libgeos.la
%{_libdir}/libgeos_c.la
%{_includedir}/geos
%{_includedir}/geos.h
%{_includedir}/geos_c.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libgeos.a
%{_libdir}/libgeos_c.a

%files -n python-geos
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/geos/_geos.so
%{py_sitescriptdir}/geos/geos.py[co]

%files -n ruby-geos
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_sitearchdir}/geos.so
