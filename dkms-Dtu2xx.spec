%define modname Dtu2xx
%define version 3.1.0.30
%define release %mkrel 2
%define modversion %{version}-%{release}

Name:     dkms-%{modname}
Version:  %{version}
Release:  %{release}
Summary:  Kernel driver for Dektec Dtu2xx
# Actually it's a very permissive license, but it tells the kernel it is GPL
# so let's distribute it as GPLv2
License:  GPLv2
# Extracted from http://www.dektec.com/Products/SDK/LinuxSDK/Downloads/LinuxSDK.zip
# which contains several drivers and some non free libraries
Source0:  %{modname}.tar.gz
Url:      http://www.dektec.com/downloads/Drivers.asp
Group:    Development/Kernel
Requires(post):  dkms
Requires(preun): dkms
Buildroot:  %{_tmppath}/%{modname}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
The Dtu2xx driver is a char driver for DekTec's DTU-2XX series of USB devices.
Currently the driver provides support for the following devices:
 - DTU-205 (FantASI USB-2 ASI/SDI Output Adapter)
 - DTU-225 (FantASI USB-2 ASI/SDI Input Adapter)
 - DTU-234 (USB-2 8-VSB/QAM-B Receiver)
 - DTU-235 (USB-2 DVB-T Receiver)
 - DTU-245 (FantASI USB-2 ASI/SDI Input + Output Adapter)

%prep
%setup -q -n %{modname}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{modversion}
cp -a * %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/
cat > %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/dkms.conf <<EOF

PACKAGE_VERSION="%{modversion}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
CLEAN="make clean"
MAKE[0]="export KERNELDIR=/lib/modules/\${kernelver}/build; make all"
BUILT_MODULE_NAME[0]="%{modname}"
BUILT_MODULE_LOCATION[0]="Source"
DEST_MODULE_LOCATION[0]="/kernel/drivers/misc/dektec"
REMAKE_INITRD="no"
AUTOINSTALL="yes"
EOF

%post
dkms add -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms build -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms install -m %{modname} -v %{modversion} --rpm_safe_upgrade --force

cat > /etc/udev/rules.d/10-%{modname}.rules << DEK
BUS=="usb", SYSFS{manufacturer}=="DEKTEC", NAME="usb/DekTec/\%k", MODE="0666"
DEK

%preun
dkms remove -m %{modname} -v %{modversion} --rpm_safe_upgrade --all

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc Readme
/usr/src/%{modname}-%{modversion}

