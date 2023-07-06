%define module_name mxser
%define _srcdir %{_prefix}/src
%{?systemd_requires}

Name:           dkms-%{module_name}
Version:        5
Release:        6%{?dist}
Summary:        Kernel module for Moxa serial controllers

Group:          System Environment/Kernel
License:        Proprietary
URL:            https://moxa.com
Source0:        https://moxa.com/getmedia/03ca2468-f62a-4c7e-ac1e-c9c9d8c62895/moxa-linux-kernel-5.x.x-driver-v%{version}.0.tgz
Source1:        dkms.conf
Source2:        disable-fifo-moxa.sh
Source3:        mxser-disable-fifo.service
Patch1:         mxser_include_fix.patch
Patch2:         mxser_fix_incorrect_returns.patch
Patch3:         mxser_local_tty_flags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       dkms kernel-devel gcc make systemd bash
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
Kernel module driver source for Moxa serial controllers

%prep
%setup -q -n %{module_name}
%patch1 -p1 -b .includes-patch
%patch2 -p1 -b .incorrect-returns
%patch3 -p1 -b .local_tty_flags

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_srcdir}
mkdir -p $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp -r %{_builddir}/%{module_name}/driver/* $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/
cp %{_builddir}/%{module_name}/mx_ver.h $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/kernel5.x/
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/dkms.conf
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/disable-fifo-moxa.sh
install -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/mxser-disable-fifo.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_srcdir}/%{module_name}-%{version}/*
%{_bindir}/disable-fifo-moxa.sh
%{_unitdir}/mxser-disable-fifo.service
%doc readme.txt

%post
occurrences=/usr/sbin/dkms status | grep "%{module_name}" | grep "%{version}" | wc -l
if [ ! occurrences > 0 ];
then
    /usr/sbin/dkms add -m %{module_name} -v %{version}
fi
/usr/sbin/dkms build -m %{module_name} -v %{version}
/usr/sbin/dkms install -m %{module_name} -v %{version}
%systemd_post mxser-disable-fifo.service
exit 0

%preun
/usr/sbin/dkms remove -m %{module_name} -v %{version} --all
%systemd_preun mxser-disable-fifo.service
exit 0

%postun
%systemd_postun_with_restart mxser-disable-fifo.service

%changelog
* Thu Jul  6 2023 Alexei Panov <alexei@panov.email> - 5-6
- changed remake_initrd option to yes in dkms.conf

* Thu May 27 2021 Alexei Panov <alexei@panov.email> - 5-5
- changed preun and postin scripts

* Thu May 27 2021 Alexei Panov <alexei@panov.email> - 5-4
- added local TTY flags header file

* Wed May 26 2021 Alexei Panov <alexei@panov.email> - 5-3
- fixed incorrect returns

* Fri Oct 23 2020 Alexei Panov <alexei@panov.email> - 5-2
- added unit and script for disablt FIFO buffer on serial ports

* Wed Oct 21 2020 Alexei Panov <alexei@panov.email> - 5-1
- Initial build
