Name:           vdo
Version:        6.2.6.14
Release:        4
Summary:        Management tools for Virtual Data Optimizer
License:        GPLv2
URL:            http://github.com/dm-vdo/vdo
Source0:        https://github.com/dm-vdo/vdo/archive/refs/tags/%{version}.tar.gz
Patch0002:      0002-Ignore-misaligned-pointers.patch
Patch0003:      0001-Add-loongarch64-support.patch
Patch0004:      0003-RISC-V-support.patch
Patch0005:      0004-fix-build-errors-for-the-clang-compiler.patch

BuildRequires:  gcc libuuid-devel device-mapper-devel device-mapper-event-devel
BuildRequires:  valgrind-devel python3 python3-devel zlib-devel systemd
%{?systemd_requires}
Requires:       lvm2 >= 2.02 python3-PyYAML >= 3.10 libuuid >= 2.23 kmod-kvdo >= 6.2 util-linux >= 2.32.1
Provides:       kvdo-kmod-common = %{version}

%define __requires_exclude perl

%description
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.
This package provides the user-space management tools for VDO.

%package_help

%prep
%setup -q
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1

%build
%make_build

%install
%make_install DESTDIR=%{buildroot} INSTALLOWNER= bindir=%{_bindir} \
  defaultdocdir=%{_defaultdocdir} name=%{name} \
  python3_sitelib=%{python3_sitelib} mandir=%{_mandir} \
  unitdir=%{_unitdir} presetdir=%{_presetdir}

# Fix the python3 shebangs
for file in %{_bindir}/vdo \
            %{_bindir}/vdostats
do
  pathfix.py -pni "%{__python3}" %{buildroot}${file}
done

%post
%systemd_post vdo.service

%preun
%systemd_preun vdo.service

%postun
%systemd_postun_with_restart vdo.service

%files
%defattr(-,root,root)
%dir %{_defaultdocdir}/%{name}
%doc CONTRIBUTORS.txt README.md 
%doc %{_defaultdocdir}/%{name}/examples/*
%license %{_defaultdocdir}/%{name}/COPYING
%{_bindir}/*
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/__init__.py
%{python3_sitelib}/%{name}/__pycache__/__init__.cpython-*.pyc
%{python3_sitelib}/%{name}/__pycache__/__init__.cpython-*.opt-1.pyc
%dir %{python3_sitelib}/%{name}/vdomgmnt/
%{python3_sitelib}/%{name}/vdomgmnt/*
%dir %{python3_sitelib}/%{name}/statistics/
%{python3_sitelib}/%{name}/statistics/*
%dir %{python3_sitelib}/%{name}/utils/
%{python3_sitelib}/%{name}/utils/*
%{_unitdir}/vdo.service
%{_presetdir}/97-vdo.preset
/bash_completion.d/vdo
/bash_completion.d/vdostats
/etc/udev/rules.d/69-vdo-start-by-dev.rules
/usr/lib/systemd/system/vdo-start-by-dev@.service
/usr/libexec/vdoprepareforlvm

%files help
%defattr(-,root,root)
%{_mandir}/man8/*

%changelog
* Mon Jun 19 2023 Xiaoya Huang <huangxiaoya@iscas.ac.cn> - 6.2.6.14-4
- Add conditionals for the function that only the GCC compiler support
- Add warning options to suppress errors

* Fri Mar 17 2023 laokz <zhangkai@iscas.ac.cn> - 6.2.6.14-3
- Add RISC-V support (Patch by YukariChiba<i@0x7f.cc>)
- Source of fence commands: RISC-V ISA Spec from riscv.org
- Remove -Wcast-align flag, since it causes error in RISC-V gcc
- Remove error-prone patch isolation macro

* Tue Mar 7 2023 doupengda <doupengda@loongson.cn> - 6.2.6.14-2
- Add loongarch64 support

* Fri May 20 2022 houyingchao <houyingchao@h-partners.com> - 6.2.6.14-1
- Upgrade to 6.2.6.14

* Fri Jun  5 2020 leiju<leiju4@huawei.com> - 6.2.0.298-13
- Fix null string and misaligned pointers

* Tue Feb 18 2019 cangyi<cangyi@huawei.com> - 6.2.0.298-12
- Package init
