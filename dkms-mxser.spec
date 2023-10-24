%define module_name mxser
%define _srcdir %{_prefix}/src
%{?systemd_requires}

Name:           dkms-%{module_name}
Version:        4
Release:        5%{?dist}
Summary:        Kernel module for Moxa serial controllers

Group:          System Environment/Kernel
License:        Proprietary
URL:            https://moxa.com
Source0:        https://cdn-cms.azureedge.net/getmedia/c93cf256-4b6d-442d-b18c-297902e370a1/moxa-msb-pci-express-universal-pci-boards-linux-kernel-4.x.x-driver-v4.2.tgz
Source1:        dkms.conf
Source2:        disable-fifo-moxa.sh
Source3:        mxser-disable-fifo.service
Source6:        moxa_unbind
Source7:        moxa_unbind.service
Source8:        mxupcie.conf
Patch1:         mxser_include_ver_fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       dkms kernel-devel gcc make systemd bash
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
Kernel module driver source for Moxa serial controllers

%prep
%setup -q -n %{module_name}
%patch 1 -p1 -b .access_ok_and_include_fix
# %patch2 -p1 -b .fix_new_kernel_state_naming.patch

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_srcdir}
mkdir -p $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/moxa
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{_modprobedir}
cp -r %{_builddir}/%{module_name}/driver/* $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/
cp %{_builddir}/%{module_name}/mx_ver.h $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/kernel4.x/
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/dkms.conf
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/disable-fifo-moxa.sh
install -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/mxser-disable-fifo.service
install -D -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/moxa/moxa_unbind
install -D -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}/mxser_unbind.service
install -D -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_modprobedir}/mxupcie.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_srcdir}/%{module_name}-%{version}/*
%{_bindir}/disable-fifo-moxa.sh
%{_unitdir}/mxser-disable-fifo.service
%{_sysconfdir}/moxa/moxa_unbind
%{_unitdir}/moxa_unbind.service
%{_modprobedir}/mxupcie.conf
%doc readme.txt

%post
#occurrences=/usr/sbin/dkms status | grep "%{module_name}" | grep "%{version}" | wc -l
#if [ ! occurrences > 0 ];
#then
    
#fi
/usr/sbin/dkms add -m %{module_name} -v %{version}
#/usr/sbin/dkms build -m %{module_name} -v %{version}
#/usr/sbin/dkms install -m %{module_name} -v %{version}
%systemd_post mxser-disable-fifo.service
%systemd_post mxser_unbind.service
#exit 0

%preun
%systemd_preun mxser-disable-fifo.service
/usr/sbin/dkms remove -m %{module_name} -v %{version} --all

%postun
%systemd_postun_with_restart mxser-disable-fifo.service
%systemd_postun_with_restart moxa_unbind.service
/usr/sbin/dkms uninstall -m %{module_name} -v %{version}
/usr/sbin/dkms remove -m %{module_name} -v %{version} --all

%changelog
* Tue Oct 24 2023 Alexei Panov <alexei@panov.email> - 4-5
- added second kernel module

* Thu Jul  6 2023 Alexei Panov <alexei@panov.email> - 4-4
- changed post and preun ections

* Thu Jul  6 2023 Alexei Panov <alexei@panov.email> - 4-3
- changed option "remake_initrd" to "yes" in dkms.conf file

* Thu Jun 30 2022 Alexei Panov <alexei@panov.email> - 4-2
- added patch to fix rename state field

* Mon Mar 14 2022 Alexei Panov <alexei@panov.email> - 4-1
- initial build for EPEL (version 8)

