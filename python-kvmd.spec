# Created by pyp2rpm-3.3.8
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

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

Requires:       python3dist(pyotp)
Requires:       python3dist(qrcode)
Requires:       python3dist(ustreamer)
Requires:       tesseract

%description
%{summary}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(setuptools)
%description -n python3-%{pypi_name}
%{summary}

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/kvmd
%{_bindir}/kvmd-cleanup
%{_bindir}/kvmd-edidconf
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
%{_bindir}/kvmd-vnc
%{_bindir}/kvmd-watchdog
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sun Apr 16 2023 trix - 3.212-1
- Initial package.
