%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg libcarddav
%define tde_prefix /opt/trinity

%define libname %mklibname carddav
%define devname %mklibname carddav -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.2
Release:	%{?tde_version:%{tde_version}_}5
Summary:	A portable CardDAV client implementation
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DWITH_ALL_OPTIONS=ON 
BuildOption:    -DBUILD_ALL=ON -DBUILD_DOC=ON -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	libtool

# CURL support
BuildRequires:  pkgconfig(libcurl)

# GTK2 support
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)

%description
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

##########

%package -n %{libname}0
Summary:	A portable CardDAV client implementation
Group:		System/Libraries

%description -n %{libname}0
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

%files -n %{libname}0
%defattr(-,root,root,-)
%{_libdir}/libcarddav.so.0
%{_libdir}/libcarddav.so.0.0.6
%{_docdir}/libcarddav/

##########

%package -n %{devname}
Summary:	A portable CardDAV client implementation (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libname}0 = %{EVRD}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	pkgconfig(glib-2.0)

%description -n %{devname}
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

This package contains the development files.

%files -n %{devname}
%defattr(-,root,root,-)
%{_includedir}/libcarddav/
%{_libdir}/libcarddav.la
%{_libdir}/libcarddav.so
%{_libdir}/pkgconfig/libcarddav.pc


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a 
# Fix doc directory
%if "%{_docdir}" != "%{_datadir}/doc"
%__mkdir_p "%{?buildroot}/%{_docdir}"
%__mv -f "%{?buildroot}/%{_datadir}/doc/libcarddav" "%{?buildroot}/%{_docdir}/libcarddav"
%endif

