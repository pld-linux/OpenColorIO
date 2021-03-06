# TODO (proprietary?):
# - truelight http://www.filmlight.ltd.uk/products/truelight/overview_tl.php
# - nuke: http://docs.thefoundry.co.uk/products/nuke/
#
# Conditional build:
%bcond_without	oiio	# OpenImageIO-dependent apps (ocioconvert,ociodisplay)
%bcond_without	opengl	# OpenGL-dependent app (ociodisplay)
%bcond_without	java	# JNI glue
%bcond_without	doc	# documentation
%bcond_with	sse2	# use SSE2 instructions
#
%ifarch %{x8664} pentrium4
%define	with_sse2	1
%endif
Summary:	Complete color management solution
Summary(pl.UTF-8):	Kompletny pakiet do zarządzania kolorami
Name:		OpenColorIO
Version:	1.1.1
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/imageworks/OpenColorIO/releases
Source0:	https://github.com/imageworks/OpenColorIO/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	23d8b9ac81599305539a5a8674b94a3d
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-java.patch
Patch2:		%{name}-libsuffix.patch
Patch3:		%{name}-missing.patch
Patch4:		%{name}-yaml-cpp.patch
Patch5:		%{name}-no-Werror.patch
Patch6:		%{name}-oiio.patch
Patch7:		%{name}-cmake-dir.patch
Patch8:		%{name}-disable-latex.patch
URL:		http://opencolorio.org/
BuildRequires:	cmake >= 2.8
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	python-devel
%if %{with doc}
BuildRequires:	sphinx-pdg >= 1.1
%endif
BuildRequires:	tinyxml-devel >= 2.6.1
BuildRequires:	yaml-cpp-devel >= 0.3.0
%if %{with opengl}
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	glew-devel >= 1.5.1
%endif
%if %{with oiio}
BuildRequires:	OpenImageIO-devel
BuildRequires:	lcms2-devel >= 2.1
%endif
Requires:	tinyxml >= 2.6.1
Requires:	yaml-cpp >= 0.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenColorIO (OCIO) is a complete color management solution geared
towards motion picture production with an emphasis on visual effects
and computer animation. OCIO provides a straightforward and consistent
user experience across all supporting applications while allowing for
sophisticated back-end configuration options suitable for high-end
production usage. OCIO is compatible with the Academy Color Encoding
Specification (ACES) and is LUT-format agnostic, supporting many
popular formats.

%description -l pl.UTF-8
OpenColorIO (OCIO) to kompletne rozwiązanie zarządzania kolorami
przeznaczone do tworzenia obrazów ruchomych, w szczególności efektów
wizualnych i animacji komputerowej. OCIO zapewnia proste i spójne
elementy we wszystkich współpracujących aplikacjach, pozwalając na
wyszukane opcje konfiguracyjne backendu, nadające się do zastosowań
produkcyjnych wysokiej jakości. OCIO jest zgodne ze specyfikacją ACES
(Academy Color Encoding Specification) i jest niezależne od formatu
LUT dzięki obsłudze wielu popularnych formatów.

%package convert
Summary:	OpenColorIO convert tool
Summary(pl.UTF-8):	Narzędzie OpenColorIO do konwersji
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	lcms2 >= 2.1

%description convert
OpenColorIO convert tool.

%description convert -l pl.UTF-8
Narzędzie OpenColorIO do konwersji.

%package display
Summary:	OpenColorIO viewer based on OpenGL
Summary(pl.UTF-8):	Przeglądarka OpenColorIO oparta na OpenGL-u
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description display
OpenColorIO viewer based on OpenGL.

%description display -l pl.UTF-8
Przeglądarka OpenColorIO oparta na OpenGL-u.

%package devel
Summary:	Header files for OpenColorIO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenColorIO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for OpenColorIO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenColorIO.

%package static
Summary:	Static OpenColorIO library
Summary(pl.UTF-8):	Statyczna biblioteka OpenColorIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenColorIO library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenColorIO.

%package -n java-OpenColorIO
Summary:	Java binding for OpenColorIO library
Summary(pl.UTF-8):	Wiązanie Javy do biblioteki OpenColorIO
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-OpenColorIO
Java binding for OpenColorIO library.

%description -n java-OpenColorIO -l pl.UTF-8
Wiązanie Javy do biblioteki OpenColorIO.

%package -n python-OpenColorIO
Summary:	Python binding for OpenColorIO library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki OpenColorIO
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-OpenColorIO
Python binding for OpenColorIO library.

%description -n python-OpenColorIO -l pl.UTF-8
Wiązanie Pythona do biblioteki OpenColorIO.

%package -n python-OpenColorIO-devel
Summary:	Header file for PyOpenColorIO API
Summary(pl.UTF-8):	Plik nagłówkowy API PyOpenColorIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-OpenColorIO = %{version}-%{release}

%description -n python-OpenColorIO-devel
Header file for PyOpenColorIO API.

%description -n python-OpenColorIO-devel -l pl.UTF-8
Plik nagłówkowy API PyOpenColorIO.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
# required for cmake to find JNI headers/libs when lib64 is in use
%{?with_java:export JAVA_HOME=%{_jvmlibdir}/java}

install -d build
cd build
# yaml-cpp 0.6.x requires C++11
CXXFLAGS="%{rpmcxxflags} -std=c++11"
%cmake .. \
	%{!?with_oiio:-DDISABLE_OIIO=ON} \
	-DOCIO_BUILD_DOCS=ON \
%if %{with java}
	-DOCIO_BUILD_JNIGLUE=ON \
	-DOCIO_STATIC_JNIGLUE=OFF \
%endif
	%{!?with_sse2:-DOCIO_USE_SSE=OFF} \
	-DUSE_EXTERNAL_LCMS=ON \
	-DUSE_EXTERNAL_TINYXML=ON \
	-DUSE_EXTERNAL_YAML=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# not needed when installing to /usr
%{__rm} $RPM_BUILD_ROOT%{_datadir}/ocio/setup_ocio.sh
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/OpenColorIO

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-OpenColorIO -p /sbin/ldconfig
%postun	-n java-OpenColorIO -p /sbin/ldconfig

%post	-n python-OpenColorIO -p /sbin/ldconfig
%postun	-n python-OpenColorIO -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%attr(755,root,root) %{_bindir}/ociobakelut
%attr(755,root,root) %{_bindir}/ociocheck
%attr(755,root,root) %{_libdir}/libOpenColorIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO.so.1

%if %{with oiio}
%files convert
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocioconvert
%attr(755,root,root) %{_bindir}/ociolutimage
%endif

%if %{with oiio} && %{with opengl}
%files display
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ociodisplay
%endif

%files devel
%defattr(644,root,root,755)
%doc build/docs/build-html/*
%attr(755,root,root) %{_libdir}/libOpenColorIO.so
%{_includedir}/OpenColorIO
%{_pkgconfigdir}/OpenColorIO.pc
%{_libdir}/cmake/OpenColorIO

%files static
%defattr(644,root,root,755)
%{_libdir}/libOpenColorIO.a

%if %{with java}
%files -n java-OpenColorIO
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenColorIO-JNI.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO-JNI.so.1
%attr(755,root,root) %{_libdir}/libOpenColorIO-JNI.so
%dir %{_datadir}/ocio
%{_datadir}/ocio/OpenColorIO-%{version}.jar
%endif

%files -n python-OpenColorIO
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/PyOpenColorIO.so

%files -n python-OpenColorIO-devel
%defattr(644,root,root,755)
%{_includedir}/PyOpenColorIO
