# TODO: truelight, nuke
#
# Conditional build:
%bcond_without	oiio	# OpenImageIO-dependent apps (ocioconvert,ociodisplay)
%bcond_without	opengl	# OpenGL-dependent app (ociodisplay)
%bcond_without	java	# JNI glue
%bcond_without	docs	# documentation
%bcond_with	sse2	# use SSE2 instructions
#
%ifarch %{x8664} pentrium4
%define	with_sse2	1
%endif
Summary:	Complete color management solution
Summary(pl.UTF-8):	Kompletny pakiet do zarządzania kolorami
Name:		OpenColorIO
Version:	1.0.6
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/imageworks/OpenColorIO/tarball/v%{version}#/%{name}-%{version}.tar.gz
# Source0-md5:	7bd5521d8671be9f9f92339b32497908
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-java.patch
URL:		http://opencolorio.org/
# g++ with tr1 support or...
#BuildRequires:	boost-devel >= 1.34
BuildRequires:	cmake >= 2.8
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
%{?with_docs:BuildRequires:	sphinx-pdg >= 1.1}
BuildRequires:	tinyxml-devel >= 2.6.1
BuildRequires:	yaml-cpp-devel >= 0.2.6
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
Requires:	yaml-cpp >= 0.2.6
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
%setup -q -n imageworks-OpenColorIO-a16d9ac
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DOCIO_BUILD_DOCS=ON \
%if %{with java}
	-DOCIO_BUILD_JNIGLUE=ON \
	-DOCIO_STATIC_JNIGLUE=OFF \
%endif
	%{!?with_sse2:-DOCIO_USE_SSE=OFF} \
	-DPYTHON_INCLUDE_LIB_PREFIX=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# we use PYTHON_INCLUDE_LIB_PREFIX=ON so library is useful as C++ API
# but allow it to be loaded without lib prefix
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libPyOpenColorIO.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/PyOpenColorIO.so

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
%doc ChangeLog LICENSE README
%attr(755,root,root) %{_bindir}/ociobakelut
%attr(755,root,root) %{_bindir}/ociocheck
%attr(755,root,root) %{_libdir}/libOpenColorIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO.so.1

%if %{with oiio}
%files convert
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocioconvert
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
%{_datadir}/ocio/OpenColorIO-1.0.6.jar
%endif

%files -n python-OpenColorIO
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPyOpenColorIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libPyOpenColorIO.so.1
%attr(755,root,root) %{_libdir}/PyOpenColorIO.so

%files -n python-OpenColorIO-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPyOpenColorIO.so
%{_includedir}/PyOpenColorIO
