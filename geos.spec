#
# Conditional build:
%bcond_without	php	# PHP binding
%bcond_without	ruby	# ruby binding
#
Summary:	Geometry Engine - Open Source
Summary(pl.UTF-8):	GEOS - silnik geometryczny z otwartymi źródłami
Name:		geos
Version:	3.4.2
Release:	3
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
# Source0-md5:	fc5df2d926eb7e67f988a43a92683bae
Patch0:		%{name}-ruby1.9.patch
Patch1:		rubydir.patch
URL:		http://trac.osgeo.org/geos/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libstdc++-devel
%{?with_php:BuildRequires:	php-devel}
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
JTS w C++. Obejmuje to wszystkie funkcje predykatów przestrzennych
wg "Simple Features for SQL" OpenGIS oraz operatory przestrzenne, a
także specyficzne dla JTS funkcje topologiczne takie jak IsValid().

%package devel
Summary:	Header files for GEOS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

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

%package -n php-geos
Summary:	PHP bindings for Geometry Engine - Open Source
Summary(pl.UTF-8):	Wiązania PHP do biblioteki GEOS
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n php-geos
PHP bindings for Geometry Engine - Open Source.

%description -n php-geos -l pl.UTF-8
Wiązania PHP do biblioteki GEOS.

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
	%{?with_php:--enable-php} \
	--enable-python \
	%{?with_ruby:--enable-ruby}

%{__make} \
	pkglibdir=%{_libdir}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with php}
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/geos.ini
; Enable geos extension module
extension=geos.so
EOF
%endif

%{?with_ruby:%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/*.{la,a}}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/geos/*.{la,a}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeos-*.so
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

%if %{with php}
%files -n php-geos
%defattr(644,root,root,755)
%doc php/{README,TODO}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/geos.ini
%attr(755,root,root) %{php_extensiondir}/geos.so
%endif

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
