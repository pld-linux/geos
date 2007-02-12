Summary:	Geometry Engine - Open Source
Summary(pl.UTF-8):   GEOS - silnik geometryczny z otwartymi źródłami
Name:		geos
Version:	2.2.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://geos.refractions.net/%{name}-%{version}.tar.bz2
# Source0-md5:	440be2b11fd3d711e950a47ea6f1b424
Patch0:		%{name}-swig.patch
URL:		http://geos.refractions.net/
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	python >= 1:2.5
BuildRequires:	python-devel >= 1:2.5
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

%description -l pl.UTF-8
GEOS (Geometry Engine - Open Source, czyli silnik geometryczny z
otwartymi źródłami) to port C++ biblioteki Java Topology Suite (JTS).
Celem biblioteki jako takiej jest implementacja pełnej funkcjonalności
JTS w C++. Obejmuje to wszystkie funkcje predykatów przestrzennych
wg "Simple Features for SQL" OpenGIS oraz operatory przestrzenne, a
także specyficzne dla JTS funkcje topologiczne takie jak IsValid().

%package devel
Summary:	Header files for GEOS library
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for GEOS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GEOS.

%package static
Summary:	Static GEOS library
Summary(pl.UTF-8):   Statyczna biblioteka GEOS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GEOS library.

%description static -l pl.UTF-8
Statyczna biblioteka GEOS.

%package -n python-geos
Summary:	Python bindings for Geometry Engine - Open Source
Summary(pl.UTF-8):   Wiązania Pythona do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-geos
Python bindings for Geometry Engine - Open Source.

%description -n python-geos -l pl.UTF-8
Wiązania Pythona do biblioteki GEOS.

%package -n ruby-geos
Summary:	Ruby bindings for Geometry Engine - Open Source
Summary(pl.UTF-8):   Wiązania języka Ruby do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n ruby-geos
Ruby bindings for Geometry Engine - Open Source.

%description -n ruby-geos -l pl.UTF-8
Wiązania języka Ruby do biblioteki GEOS.

%prep
%setup -q
%patch0 -p1

%build
cp -f /usr/share/automake/config.* .
%configure
%{__make} \
	pkglibdir=%{_libdir}

cd swig/python
swig -c++ -python -modern -o geos_wrap.cxx ../geos.i
python setup.py build

cd ../ruby
swig -c++ -ruby -autorename -o geos_wrap.cxx ../geos.i
%{__cxx} %{rpmcxxflags} -I../../source/headers -I%{ruby_archdir} -c geos_wrap.cxx
%{__cxx} -shared -o geos.so geos_wrap.o -lruby -L../../source/geom/.libs -lgeos

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkglibdir=%{_libdir}

cd swig
install -D ruby/geos.so $RPM_BUILD_ROOT%{ruby_archdir}/geos.so

cd python
python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeos.so.*.*.*
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
%attr(755,root,root) %{py_sitedir}/_geos.so
%{py_sitedir}/geos.py[co]
%{py_sitedir}/PyGEOS-*.egg-info

%files -n ruby-geos
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_archdir}/geos.so
