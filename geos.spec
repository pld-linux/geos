#
# Conditional build:
%bcond_without	ruby	# ruby binding

Summary:	Geometry Engine - Open Source
Summary(pl.UTF-8):	GEOS - silnik geometryczny z otwartymi źródłami
Name:		geos
Version:	3.8.3
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
# Source0-md5:	57e4bde34a4f8aabed096e06a2002c4d
Patch0:		rubydir.patch
Patch1:		%{name}-x32.patch
URL:		https://trac.osgeo.org/geos/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.519
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	swig-python >= 1.3.29
%{?with_ruby:BuildRequires:	swig-ruby >= 1.3.40-3}
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

%package static
Summary:	Static GEOS library
Summary(pl.UTF-8):	Statyczna biblioteka GEOS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GEOS library.

%description static -l pl.UTF-8
Statyczna biblioteka GEOS.

%package -n python-geos
Summary:	Python bindings for Geometry Engine - Open Source
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-geos
Python bindings for Geometry Engine - Open Source.

%description -n python-geos -l pl.UTF-8
Wiązania Pythona do biblioteki GEOS.

%package -n ruby-geos
Summary:	Ruby bindings for Geometry Engine - Open Source
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki GEOS
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n ruby-geos
Ruby bindings for Geometry Engine - Open Source.

%description -n ruby-geos -l pl.UTF-8
Wiązania języka Ruby do biblioteki GEOS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-python \
	%{?with_ruby:--enable-ruby}

%{__make} \
	pkglibdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitescriptdir}

%{?with_ruby:%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/*.{la,a}}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/geos/*.{la,a}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libgeos-%{version}.so
%attr(755,root,root) %{_libdir}/libgeos_c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeos_c.so.1

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
%dir %{py_sitedir}/geos
%attr(755,root,root) %{py_sitedir}/geos/_geos.so
%{py_sitescriptdir}/geos
%{py_sitescriptdir}/geos.pth

%if %{with ruby}
%files -n ruby-geos
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/geos.so
%endif
