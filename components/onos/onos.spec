%define __jar_repack 0

Name: onos
Summary: Open Network Operating System
Version: 1.1
Release: 1
Source0: http://downloads.onosproject.org/release/onos-1.1.0.tar.gz
Source1: onos.service
Group: Applications/Communications
License: ASL 2.0
URL: http://www.onosproject.org
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: java-1.7.0-openjdk-devel >= 1.7.0
Requires(pre): shadow-utils, glibc-common
Requires(postun): shadow-utils
BuildRequires: systemd

%pre
%global onos_user onos
%global onos_home /opt/onos

# Create onos user/group
getent passwd %{onos_user} > /dev/null \
    || useradd --system --home-dir %{onos_home} %{onos_user}
getent group %{onos_user} > /dev/null \
    || groupadd --system %{onos_user}

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
OpenDaylight is an open platform for network programmability to enable SDN and create a solid foundation for NFV for networks at any size and scale.

%prep
%autosetup -N -c -n %{name}

%build

%install
install -d %{buildroot}/%{onos_home}
cp -R %{_builddir}/%{name} %{buildroot}/%{onos_home}
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service

%clean
rm -rf %
 
%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

# remove installed files
rm -rf %{onos_home}/%{name}

# remove onos user/group
userdel %{onos_user} && groupdel %{onos_user}

%files
# ONOS uses systemd to run as user:group onos:onos
%attr(0775,onos,onos) %{onos_home}/%{name}
%attr(0644,-,-) %{_unitdir}/%{name}.service

%changelog
* Thu Apr 09 2015 David Jorm - 1.1-1
- Initial creation