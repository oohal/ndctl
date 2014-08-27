%global gitcommit %(git log --pretty=format:"%h" -n 1)

# (hack stolen from systemd.spec)
# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

Name:           ndctl
Version:        1
Release:        1%{?gitcommit:.git%{gitcommit}}%{?dist}
Summary:	Manage "nd" subsystem devices (Non-volatile Memory)
License:        LGPLv2.1 and BSD and MIT
URL:            http://01.org/linux-nvdimm/

%if %{defined gitcommit}
# Snapshot tarball can be created using: ./make-git-shapshot.sh [gitcommit]
Source0:        %{name}-git%{gitcommit}.tar.xz
%else
Source0:        https://github.com/01org/nd/archive/%{name}-%{version}.tar.gz
%endif

BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake

%description
Utility library for managing the "nd" subsystem.  The "nd" subsystem
defines a device model and control message interface for NFIT (NVDIMM
Firmware Interface Table) defined devices.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q %{?gitcommit:-n %{name}-git%{gitcommit}}


%build
%if %{defined gitcommit}
    ./autogen.sh
%endif
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libndctl.pc

%changelog
* Wed Aug 27 2014 Dan Williams
- 