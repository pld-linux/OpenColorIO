# TODO:
# - OpenFX plugin (OpenFX >= 1.4, https://github.com/ofxa/openfx)
# - truelight http://www.filmlight.ltd.uk/products/truelight/overview_tl.php (proprietary?)
# - nuke: http://docs.thefoundry.co.uk/products/nuke/ (proprietary)
#
# Conditional build:
%bcond_without	opengl	# OpenGL-dependent app (ociodisplay)
%bcond_with	java	# JNI glue (outdated as of 2.2.1)
%bcond_without	doc	# documentation
%bcond_with	sse2	# use SSE2 instructions
%bcond_with	sse3	# use SSE3 instructions
%bcond_with	ssse3	# use SSSE3 instructions
%bcond_with	sse4	# use SSE4 instructions
%bcond_with	sse42	# use SSE4.2 instructions
%bcond_with	avx	# use AVX instructions
%bcond_with	avx2	# use AVX2 instructions
%bcond_with	avx512	# use AVX512 instructions
%bcond_with	f16c	# use F16C instructions
#
%ifarch %{x8664} pentium4 x32
%define	with_sse2	1
%endif
Summary:	Complete color management solution
Summary(pl.UTF-8):	Kompletny pakiet do zarządzania kolorami
Name:		OpenColorIO
Version:	2.3.2
Release:	
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/imageworks/OpenColorIO/releases
Source0:	https://github.com/imageworks/OpenColorIO/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8af74fcb8c4820ab21204463a06ba490
Patch0:		%{name}-java.patch
URL:		http://opencolorio.org/
BuildRequires:	Imath-devel >= 3.1.6
BuildRequires:	OpenEXR-devel >= 3.0.5
BuildRequires:	cmake >= 3.13
BuildRequires:	expat-devel >= 1:2.5.0
%{?with_java:BuildRequires:	jdk}
BuildRequires:	lcms2-devel >= 2.2
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	minizip-ng-devel >= 3.0.7
BuildRequires:	pkgconfig
BuildRequires:	pystring-devel >= 1.1.3
BuildRequires:	python3-devel
BuildRequires:	python3-pybind11 >= 2.9.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	tinyxml-devel >= 2.6.1
BuildRequires:	yaml-cpp-devel >= 0.8.0
BuildRequires:	zlib-devel >= 1.2.13
%if %{with doc}
BuildRequires:	python3-breathe
BuildRequires:	python3-recommonmark
BuildRequires:	python3-six
BuildRequires:	python3-sphinx_press_theme
BuildRequires:	python3-sphinx_tabs
BuildRequires:	python3-testresources
BuildRequires:	sphinx-pdg >= 1.1
%endif
%if %{with opengl}
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	glew-devel >= 1.5.1
%endif
Requires:	Imath >= 3.1.6
Requires:	expat >= 1:2.5.0
Requires:	minizip-ng >= 3.0.7
Requires:	tinyxml >= 2.6.1
Requires:	yaml-cpp >= 0.8.0
Requires:	zlib >= 1.2.13
%if %{without java}
Obsoletes:	java-OpenColorIO < 2
%endif
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
Requires:	OpenEXR >= 3.0.5
Requires:	lcms2 >= 2.2

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
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for OpenColorIO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenColorIO.

%package apidocs
Summary:	API documentation for OpenColorIO library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenColorIO
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for OpenColorIO library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OpenColorIO.

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
%patch0 -p1

%build
# required for cmake to find JNI headers/libs when lib64 is in use
%{?with_java:export JAVA_HOME=%{_jvmlibdir}/java}

%cmake -B build \
	-DCMAKE_CONFIGURATION_TYPES=PLD \
	-DCMAKE_CXX_STANDARD=14 \
	%{cmake_on_off doc OCIO_BUILD_DOCS} \
	%{cmake_on_off java OCIO_BUILD_JAVA} \
	%{!?with_sse2:-DOCIO_USE_SSE2=OFF} \
	%{!?with_sse3:-DOCIO_USE_SSE3=OFF} \
	%{!?with_ssse3:-DOCIO_USE_SSSE3=OFF} \
	%{!?with_sse4:-DOCIO_USE_SSE4=OFF} \
	%{!?with_sse42:-DOCIO_USE_SSE42=OFF} \
	%{!?with_avx:-DOCIO_USE_AVX=OFF} \
	%{!?with_avx2:-DOCIO_USE_AVX2=OFF} \
	%{!?with_avx512:-DOCIO_USE_AVX512=OFF} \
	%{!?with_f16c:-DOCIO_USE_F16C=OFF}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

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

%post	-n python3-OpenColorIO -p /sbin/ldconfig
%postun	-n python3-OpenColorIO -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/ocioarchive
%attr(755,root,root) %{_bindir}/ociobakelut
%attr(755,root,root) %{_bindir}/ociocheck
%attr(755,root,root) %{_bindir}/ociochecklut
%attr(755,root,root) %{_bindir}/ociomakeclf
%attr(755,root,root) %{_bindir}/ocioperf
%attr(755,root,root) %{_bindir}/ociowrite
%attr(755,root,root) %{_libdir}/libOpenColorIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenColorIO.so.2.3

%files convert
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocioconvert
%attr(755,root,root) %{_bindir}/ociolutimage

%if %{with opengl}
%files display
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ociodisplay
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenColorIO.so
%{_libdir}/libOpenColorIOimageioapphelpers.a
%{_libdir}/libOpenColorIOoglapphelpers.a
%{_includedir}/OpenColorIO
%{_pkgconfigdir}/OpenColorIO.pc
%{_libdir}/cmake/OpenColorIO

%files apidocs
%defattr(644,root,root,755)
%doc build/docs/build-html/{_images,_static,api,aswf,concepts,configurations,guides,quick_start,releases,tutorials,*.html,*.js}

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
%dir %{py3_sitedir}/PyOpenColorIO
%attr(755,root,root) %{py3_sitedir}/PyOpenColorIO/PyOpenColorIO.so
%{py3_sitedir}/PyOpenColorIO/__init__.py
%{py3_sitedir}/PyOpenColorIO/__pycache__
