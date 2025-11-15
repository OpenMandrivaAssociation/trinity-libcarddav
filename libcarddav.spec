#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg libcarddav
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libcarddav %{_lib}carddav
%else
%define libcarddav libcarddav
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.2
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	A portable CardDAV client implementation
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Deskio
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:    cmake make

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
#BuildRequires:	make
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

%package -n %{libcarddav}0
Summary:	A portable CardDAV client implementation
Group:		System/Libraries

Obsoletes:	trinity-libcarddav < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcarddav = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcarddav = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcarddav}0
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

%files -n %{libcarddav}0
%defattr(-,root,root,-)
%{_libdir}/libcarddav.so.0
%{_libdir}/libcarddav.so.0.0.6
%{_docdir}/libcarddav/

%post -n %{libcarddav}0
/sbin/ldconfig

%postun -n %{libcarddav}0
/sbin/ldconfig


##########

%package -n %{libcarddav}-devel
Summary:	A portable CardDAV client implementation (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libcarddav}0 = %{?epoch:%{epoch}:}%{version}-%{release}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	pkgconfig(glib-2.0)

Obsoletes:	trinity-libcarddav-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcarddav-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcarddav-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcarddav}-devel
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

This package contains the development files.

%files -n %{libcarddav}-devel
%defattr(-,root,root,-)
%{_includedir}/libcarddav/
%{_libdir}/libcarddav.la
%{_libdir}/libcarddav.so
%{_libdir}/pkgconfig/libcarddav.pc

%post -n %{libcarddav}-devel
/sbin/ldconfig

%postun -n %{libcarddav}-devel
/sbin/ldconfig

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DLIB_INSTALL_DIR="%{_libdir}" \
  -DSHARE_INSTALL_PREFIX="%{_datadir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR=%{buildroot} -C build

# Fix doc directory
%if "%{_docdir}" != "%{_datadir}/doc"
%__mkdir_p "%{?buildroot}/%{_docdir}"
%__mv -f "%{?buildroot}/%{_datadir}/doc/libcarddav" "%{?buildroot}/%{_docdir}/libcarddav"
%endif

