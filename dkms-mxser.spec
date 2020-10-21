%define module_name mxser
%define _srcdir %{_prefix}/src

Name:		dkms-%{module_name}
Version:  	5
Release:	1%{?dist}
Summary:	Kernel module for Moxa serial controllers

Group:		System Environment/Kernel
License:	Proprietary
URL:		https://moxa.com
Source0:	https://moxa.com/getmedia/03ca2468-f62a-4c7e-ac1e-c9c9d8c62895/moxa-linux-kernel-5.x.x-driver-v%{version}.0.tgz
Source1:	dkms.conf
Patch1:     mxser_include_fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	dkms kernel-devel gcc make
BuildArch:	noarch

%description
Kernel module driver source for Moxa serial controllers

%prep
%setup -q -n %{module_name}
%patch1 -p1 -b .includes-patch

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_srcdir}
mkdir -p $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}
cp -r %{_builddir}/%{module_name}/driver/* $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/
cp %{_builddir}/%{module_name}/mx_ver.h $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/kernel5.x/
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/dkms.conf


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_srcdir}/%{module_name}-%{version}/*
%doc readme.txt

%post
/usr/sbin/dkms add -m %{module_name} -v %{version}

%preun
/usr/sbin/dkms uninstall -m %{module_name} -v %{version}
/usr/sbin/dkms remove -m %{module_name} -v %{version} --all

%changelog
* Wed Oct 21 2020 Alexei Panov <alexei@panov.email> - 5-1
- Initial build