%define module_name mxser
%define _srcdir %{_prefix}/src
%{?systemd_requires}

Name:           dkms-%{module_name}
Version:        4
Release:        2%{?dist}
Summary:        Kernel module for Moxa serial controllers

Group:          System Environment/Kernel
License:        Proprietary
URL:            https://moxa.com
Source0:	    https://cdn-cms.azureedge.net/getmedia/c7c46cba-df8c-4645-92f5-47092b8906c0/moxa-msb-linux-kernel-4.x.x-driver-v4.1.tgz
Source1:        dkms.conf
Source2:        disable-fifo-moxa.sh
Source3:        mxser-disable-fifo.service
Patch1:		    mxser_access_ok_fix_and_include_fix.patch
Patch2:         fix_new_kernel_state_naming.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       dkms kernel-devel gcc make systemd bash
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
Kernel module driver source for Moxa serial controllers

%prep
%setup -q -n %{module_name}
%patch1 -p1 -b .access_ok_and_include_fix
%patch2 -p1 -b .fix_new_kernel_state_naming.patch

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_srcdir}
mkdir -p $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp -r %{_builddir}/%{module_name}/driver/* $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/
cp %{_builddir}/%{module_name}/mx_ver.h $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/kernel4.x/
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
* Thu Jun 30 2022 Alexei Panov <alexei@panov.email> - 4-2
- added patch to fix rename state field

* Mon Mar 14 2022 Alexei Panov <alexei@panov.email> - 4-1
- initial build for EPEL (version 8)

