# Created by pyp2rpm-3.3.8
# Based on https://github.com/tao-j/copr/blob/main/kvmd/kvmd.spec

%global pypi_name kvmd
%global pypi_version 3.212
%global debug_package %{nil}

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        The main PiKVM daemon
ExclusiveArch:  aarch64

License:        GPLv3
URL:            https://github.com/pikvm/kvmd
Source0:        %{url}/archive/v%{pypi_version}.tar.gz
Patch1:         kvmd-01.patch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

Requires:       iproute
Requires:       openssl
Requires:       python3dist(pyotp)
Requires:       python3dist(qrcode)
Requires:       python3dist(setuptools)
Requires:       python3dist(ustreamer)
Requires:       tesseract

%description
%{summary}

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
%description -n python3-%{pypi_name}
%{summary}

%prep
%autosetup -p1 -n %{pypi_name}-%{pypi_version}

%build
%py3_build

%install
%py3_install
%{__cp} scripts/* %{buildroot}%{_bindir}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/kvmd/nginx/ssl
%{__mkdir_p} %{buildroot}%{_sysconfdir}/kvmd/override.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/kvmd/vnc/ssl
%{__cp} configs/kvmd/*.yaml %{buildroot}%{_sysconfdir}/kvmd/
%{__cp} configs/kvmd/edid/*.hex %{buildroot}%{_sysconfdir}/kvmd/
%{__cp} configs/kvmd/*passwd %{buildroot}%{_sysconfdir}/kvmd/
%{__cp} configs/kvmd/totp.secret %{buildroot}%{_sysconfdir}/kvmd/

%{__mkdir_p} %{buildroot}%{_datadir}/kvmd/configs.default
%{__cp} -r configs/* %{buildroot}%{_datadir}/kvmd/configs.default/
%{__cp} -r contrib/keymaps %{buildroot}%{_datadir}/kvmd/
%{__cp} -r extras %{buildroot}%{_datadir}/kvmd/

# # % dir %{_sysconfdir}/kvmd
# # % dir %{_datadir}/kvmd

%pre  -n python3-%{pypi_name}
%{_sbindir}/groupadd gpio

%{_bindir}/getent passwd kvmd >/dev/null || \
%{_sbindir}/useradd -r -U -G gpio,dialout,video,systemd-journal \
                    -d %{_datadir}/kvmd -s %{_sbindir}/nologin \
                    -c 'kvmd - The main daemon' kvmd

%{_bindir}/getent passwd kvmd-ipmi >/dev/null || \
%{_sbindir}/useradd -r -U -G kvmd \
                    -d %{_datadir}/kvmd -s %{_sbindir}/nologin \
                    -c 'kvmd - IPMI to KVMD proxy' kvmd-ipmi

%{_bindir}/getent passwd kvmd-vnc >/dev/null || \
%{_sbindir}/useradd -r -U -G kvmd \
                    -d %{_datadir}/kvmd -s %{_sbindir}/nologin \
                    -c 'kvmd - VNC to KVMD/Streamer proxy' kvmd-vnc

%post  -n python3-%{pypi_name}
%{_bindir}/kvmd-gencert --do-the-thing
%{_bindir}/kvmd-gencert --do-the-thing --vnc

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/kvmd
%{_bindir}/kvmd-bootconfig
%{_bindir}/kvmd-certbot
%{_bindir}/kvmd-cleanup
%{_bindir}/kvmd-edidconf
%{_bindir}/kvmd-gencert
%{_bindir}/kvmd-helper-otgmsd-remount
%{_bindir}/kvmd-helper-pst-remount
%{_bindir}/kvmd-helper-swapfiles
%{_bindir}/kvmd-htpasswd
%{_bindir}/kvmd-ipmi
%{_bindir}/kvmd-janus
%{_bindir}/kvmd-otg
%{_bindir}/kvmd-otgconf
%{_bindir}/kvmd-otgmsd
%{_bindir}/kvmd-otgnet
%{_bindir}/kvmd-pst
%{_bindir}/kvmd-pstrun
%{_bindir}/kvmd-totp
%{_bindir}/kvmd-udev-hdmiusb-check
%{_bindir}/kvmd-vnc
%{_bindir}/kvmd-watchdog
%{_datadir}/kvmd/
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info
%{_sysconfdir}/kvmd/
%attr(0600,kvmd,kvmd) %{_sysconfdir}/kvmd/htpasswd
%attr(0600,kvmd-ipmi,kvmd-ipmi) %{_sysconfdir}/kvmd/ipmipasswd
%attr(0600,kvmd-vnc,kvmd-vnc) %{_sysconfdir}/kvmd/vncpasswd

%global hw_name python3-%{pypi_name}-v3-rpi4

%package -n %{hw_name}
Summary:        PiKVM RPI4 Version 3 hardware
Requires:       python3dist(%{pypi_name})

%description -n %{hw_name}
%{summary}

%files -n %{hw_name}

%post -n %{hw_name}
cp %{_datadir}/kvmd/configs.default/kvmd/main/v3-hdmi-rpi4.yaml %{_sysconfdir}/kvmd/main.yaml

%postun -n %{hw_name}
rm %{_sysconfdir}/kvmd/main.yaml

%changelog
* Sun Apr 16 2023 trix - 3.212-1
- Initial package.
