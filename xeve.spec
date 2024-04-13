#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	eXtra-fast Essential Video Encoder (MPEG-5 EVC)
Summary(pl.UTF-8):	eXtra-fast Essential Video Encoder - szybki koder obrazu MPEG-5 EVC
Name:		xeve
Version:	0.4.3
%define	gitref	%{version}-3890dae6
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/mpeg5/xeve/releases
Source0:	https://github.com/mpeg5/xeve/archive/v%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	17e7dc3ba36f43e8311d8a88734aeeca
Patch0:		%{name}-string.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-dynamic.patch
URL:		https://github.com/mpeg5/xeve
BuildRequires:	cmake >= 3.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The eXtra-fast Essential Video Encoder (XEVE) is an opensource and
fast MPEG-5 EVC encoder.

MPEG-5 Essential Video Coding (EVC) is a video compression standard of
ISO/IEC Moving Picture Experts Group (MPEG). The main goal of the EVC
is to provide a significantly improved compression capability over
existing video coding standards with timely publication of terms.

This package contains the library with Main Profile (with additional
tools).

%description -l pl.UTF-8
XEVE (eXtra-fast Essential Video Encoder - bardzo szybki koder obrazu
zasadniczego) to szybki, mający otwarte źródła koder MPEG-5 EVC.

MPEG-5 Essential Video Coding (EVC) to standard kompresji obrazu
tworzony przez ISO/IEC Moving Picture Experts Group (MPEG). Głównym
celem EVC jest zapewnienie znacząco lepszych mozliwości kompresji niż
istniejące standardy kodowania obrazu.

Ten pakiet zawiera bibliotekę o profilu Main (z dodatkowymi
narzędziami).

%package devel
Summary:	Header files for XEVE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki XEVE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for XEVE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki XEVE.

%package static
Summary:	Static XEVE library
Summary(pl.UTF-8):	Statyczna biblioteka XEVE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static XEVE library.

%description static -l pl.UTF-8
Statyczna biblioteka XEVE.

%package base
Summary:	eXtra-fast Essential Video Encoder (MPEG-5 EVC) - Baseline Profile
Summary(pl.UTF-8):	eXtra-fast Essential Video Encoder - szybki koder obrazu MPEG-5 EVC - profil Baseline
Group:		Libraries

%description base
The eXtra-fast Essential Video Encoder (XEVE) is an opensource and
fast MPEG-5 EVC encoder.

MPEG-5 Essential Video Coding (EVC) is a video compression standard of
ISO/IEC Moving Picture Experts Group (MPEG). The main goal of the EVC
is to provide a significantly improved compression capability over
existing video coding standards with timely publication of terms.

This package contains the library with Baseline Profile (which contain
only technologies that are older than 20 years or otherwise freely
available for use in the standard).

%description base -l pl.UTF-8
XEVE (eXtra-fast Essential Video Encoder - bardzo szybki koder
obrazu zasadniczego) to szybki, mający otwarte źródła dekoder MPEG-5
EVC.

MPEG-5 Essential Video Coding (EVC) to standard kompresji obrazu
tworzony przez ISO/IEC Moving Picture Experts Group (MPEG). Głównym
celem EVC jest zapewnienie znacząco lepszych mozliwości kompresji niż
istniejące standardy kodowania obrazu.

Ten pakiet zawiera bibliotekę o profilu Baseline (zawierający jedynie
technologie starsze niż 20 lat albo w inny sposób wolnodostępne do
użycia w standardzie).

%package base-devel
Summary:	Header files for XEVE library (Baseline Profile)
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki XEVE (profil Baseline)
Group:		Development/Libraries
Requires:	%{name}-base = %{version}-%{release}

%description base-devel
Header files for XEVE library (Baseline Profile).

%description base-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki XEVE (profil Baseline).

%package base-static
Summary:	Static XEVE library (Baseline Profile)
Summary(pl.UTF-8):	Statyczna biblioteka XEVE (profil Baseline)
Group:		Development/Libraries
Requires:	%{name}-base-devel = %{version}-%{release}

%description base-static
Static XEVE library (Baseline Profile).

%description base-static -l pl.UTF-8
Statyczna biblioteka XEVE (profil Baseline).

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1
%patch2 -p1

echo "v%{version}" > version.txt

%build
install -d build-main
cd build-main
%cmake ..

%{__make}
cd ..

install -d build-base
cd build-base
%cmake .. \
	-DSET_PROF=BASE

%{__make}
%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-main install \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_libdir}/xeve/lib*.a $RPM_BUILD_ROOT%{_libdir}

%{__make} -C build-base install \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_libdir}/xeveb/lib*.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	base -p /sbin/ldconfig
%postun	base -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/xeve_app
%attr(755,root,root) %{_libdir}/libxeve.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxeve.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxeve.so
%{_includedir}/xeve
%{_pkgconfigdir}/xeve.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxeve.a
%endif

%files base
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/xeveb_app
%attr(755,root,root) %{_libdir}/libxeveb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxeveb.so.0

%files base-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxeveb.so
%{_includedir}/xeveb
%{_pkgconfigdir}/xeveb.pc

%if %{with static_libs}
%files base-static
%defattr(644,root,root,755)
%{_libdir}/libxeveb.a
%endif
