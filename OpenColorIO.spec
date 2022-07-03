# TODO (proprietary?):
# - truelight http://www.filmlight.ltd.uk/products/truelight/overview_tl.php
# - nuke: http://docs.thefoundry.co.uk/products/nuke/
#
# Conditional build:
%bcond_without	oiio	# OpenImageIO-dependent apps (ocioconvert,ociodisplay)
%bcond_without	opengl	# OpenGL-dependent app (ociodisplay)
%bcond_with	java	# JNI glue
%bcond_with	doc	# documentation
%bcond_with	sse2	# use SSE2 instructions
#
%ifarch %{x8664} pentrium4
%define	with_sse2	1
%endif
Summary:	Complete color management solution
Summary(pl.UTF-8):	Kompletny pakiet do zarządzania kolorami
Name:		OpenColorIO
Version:	2.1.1
Release:	3.1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/imageworks/OpenColorIO/releases
Source0:	https://github.com/imageworks/OpenColorIO/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	604f562e073f23d88ce89ed4f7f709ba
URL:		http://opencolorio.org/
BuildRequires:	Imath-devel >= 3.1.2
BuildRequires:	cmake >= 2.8
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	pystring-devel
BuildRequires:	python3-devel
BuildRequires:	python3-pybind11 >= 2.6.1
%if %{with doc}
BuildRequires:	python3-recommonmark
BuildRequires:	python3-testresources
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
BuildRequires:	rpmbuild(macros) >= 1.742
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

%package -n java-OpenColorIO
Summary:	Java binding for OpenColorIO library
Summary(pl.UTF-8):	Wiązanie Javy do biblioteki OpenColorIO
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-OpenColorIO
Java binding for OpenColorIO library.

%description -n java-OpenColorIO -l pl.UTF-8
Wiązanie Javy do biblioteki OpenColorIO.

%package -n python3-OpenColorIO
Summary:	Python binding for OpenColorIO library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki OpenColorIO
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-OpenColorIO
Python binding for OpenColorIO library.

%description -n python3-OpenColorIO -l pl.UTF-8
Wiązanie Pythona do biblioteki OpenColorIO.

%prep
%setup -q

%build
# required for cmake to find JNI headers/libs when lib64 is in use
%{?with_java:export JAVA_HOME=%{_jvmlibdir}/java}

install -d build
cd build
%cmake .. \
	-DCMAKE_CONFIGURATION_TYPES=PLD \
	-DCMAKE_CXX_STANDARD=14 \
	%cmake_on_off doc OCIO_BUILD_DOCS \
	%cmake_on_off java OCIO_BUILD_JAVA \
	%{!?with_oiio:-DDISABLE_OIIO=ON} \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-OpenColorIO -p /sbin/ldconfig
%postun	-n java-OpenColorIO -p /sbin/ldconfig

%post	-n python3-OpenColorIO -p /sbin/ldconfig
%postun	-n python3-OpenColorIO -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/ociobakelut
%attr(755,root,root) %{_bindir}/ociocheck
%attr(755,root,root) %{_bindir}/ociochecklut
%attr(755,root,root) %{_bindir}/ociomakeclf
%attr(755,root,root) %{_bindir}/ociowrite
%attr(755,root,root) %{_libdir}/libOpenColorIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO.so.2.1

%if %{with oiio}
%files convert
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocioconvert
%attr(755,root,root) %{_bindir}/ociolutimage
%attr(755,root,root) %{_bindir}/ocioperf
%endif

%if %{with oiio} && %{with opengl}
%files display
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ociodisplay
%endif

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc build/docs/build-html/*}
%attr(755,root,root) %{_libdir}/libOpenColorIO.so
%{_libdir}/libOpenColorIOoglapphelpers.a
%{?with_oiio:%{_libdir}/libOpenColorIOoiiohelpers.a}
%{_includedir}/OpenColorIO
%{_pkgconfigdir}/OpenColorIO.pc
%{_libdir}/cmake/OpenColorIO

%if %{with java}
%files -n java-OpenColorIO
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenColorIO-JNI.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO-JNI.so.1
%attr(755,root,root) %{_libdir}/libOpenColorIO-JNI.so
%dir %{_datadir}/ocio
%{_datadir}/ocio/OpenColorIO-%{version}.jar
%endif

%files -n python3-OpenColorIO
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/PyOpenColorIO.so
