#
%bcond_without	static_libs # don't build static libraries
#
%define	_oname	fox
%define _suffix	14
#
Summary:	The FOX C++ GUI Toolkit
Summary(pl.UTF-8):   FOX - toolkit graficzny w C++
Name:		%{_oname}%{_suffix}
Version:	1.4.27
Release:	0.1
License:	LGPL
Group:		X11/Libraries
Source0:	ftp://ftp.fox-toolkit.com/pub/%{_oname}-%{version}.tar.gz
# Source0-md5:	0f2925b1d595a889640b4222ab1c6a15
Patch0:		%{name}-opt.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-Makefile.patch
URL:		http://www.fox-toolkit.org/fox.html
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cups-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	xcursor-devel
Requires:	OpenGL
Provides:	%{_oname} = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%description
FOX is a C++-Based Library for Graphical User Interface Development
FOX supports modern GUI features, such as Drag-and-Drop, Tooltips, Tab
Books, Tree Lists, Icons, Multiple-Document Interfaces (MDI), timers,
idle processing, automatic GUI updating, as well as OpenGL/Mesa for 3D
graphics. Subclassing of basic FOX widgets allows for easy extension
beyond the built-in widgets by application writers.

%description -l pl.UTF-8
FOX jest biblioteką bazującą na C++ do projektowania graficznych
interfejsów użytkownika. Obsługuje wiele właściwości współczesnych
GUI: Drag-and-Drop, listy, ikony, interfejsy wielodokumentowe (MDI),
liczniki, przetwarzanie w tle, automatyczne uaktualnianie GUI, obsługę
grafiki OpenGL. Bazowe klasy widgetów FOX pozwalają na łatwe
rozszerzanie.

%package progs
Summary:	FOX example applications
Summary(pl.UTF-8):   Przykłady aplikacji w FOX
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Provides:	%{_oname}-progs = %{version}-%{release}
Obsoletes:	%{name}-example-apps

%description progs
Editor and file browser, written with FOX.

%description progs -l pl.UTF-8
Edytor i przeglądarka plików napisane z użyciem toolkitu FOX.

%package devel
Summary:	Header files for FOX library
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki FOX
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-devel
Requires:	bzip2-devel
Requires:	libjpeg-devel
Requires:	libpng-devel
Requires:	libstdc++-devel
Requires:	libtiff-devel
Requires:	xcursor-devel
Provides:	%{_oname}-devel = %{version}-%{release}

%description devel
Header files for FOX library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FOX.

%package static
Summary:	FOX static libraries
Summary(pl.UTF-8):   Biblioteki statyczne FOX
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	%{_oname}-static = %{version}-%{release}

%description static
FOX static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne FOX.

%package doc
Summary:	Development documentation for FOX library
Summary(pl.UTF-8):   Dokumentacja programisty do biblioteki FOX
Group:		X11/Development/Libraries

%description doc
Development documentation for FOX library.

%description doc -l pl.UTF-8
Dokumentacja programisty do biblioteki FOX.

%prep
%setup -q -n %{_oname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
LDFLAGS="%{rpmldflags} -L/usr/X11R6/%{_lib}"
%configure \
	--enable-cups \
	--enable-release \
	--enable-threadsafe \
	--with-xcursor \
	--with-xrandr \
	--with-opengl \
	--with-shape \
	--with-xshm \
	--with-xft \
	%{?debug:--enable-debug}%{!?_debug:--enable-release} \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f doc/Makefile* doc/*/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE_ADDENDUM README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/adie
%attr(755,root,root) %{_bindir}/calculator
%attr(755,root,root) %{_bindir}/PathFinder
%attr(755,root,root) %{_bindir}/shutterbug
%attr(755,root,root) %{_bindir}/Adie.stx
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc ADDITIONS TRACING
%attr(755,root,root) %{_bindir}/fox-config
%attr(755,root,root) %{_bindir}/reswrap
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/fox-1.4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/*
