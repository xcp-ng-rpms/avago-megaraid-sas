%global package_speccommit 07a7e44b3e7f7ce03d5fc0ff6d632bb57c479170
%global package_srccommit 07.713.01.00+rc1
%define vendor_name Avago
%define vendor_label avago
%define driver_name megaraid-sas

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 07.713.01.00+rc1
Release: 3%{?xsrel}%{?dist}
License: GPL
Source0: avago-megaraid-sas.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 07.713.01.00+rc1-3
- CP-38416: Enable static analysis

* Thu Jun 04 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 07.713.01.00+rc1-2
- CA-340752: Remove unnessary nested source tarball

* Wed May 20 2020 Tim Smith <tim.smith@citrix.com> - 07.713.01.00+rc1-1
- CP-34009 Update avago-megaraid_sas driver to 07.713.01.00+rc1

* Mon Feb 25 2019 Thomas Mckelvey <thomas.mckelvey@citrix.com> - 07.707.50.00+rc1-1
- BRO-229: Update driver version to 07.707.50.00+rc1
