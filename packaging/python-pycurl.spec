%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.0
Release:        4
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Patch0:		python-pycurl-no-static-libs.patch
Patch1:		python-pycurl-lcrypto.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  curl-devel >= 7.19.0
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libcares)

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%define libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%define curlver_h /usr/include/curl/curlver.h
%define libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:	libcurl >= %{libcurl_ver}

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup0 -q -n pycurl-%{version}
%patch0 -p0
%patch1 -p1 -b .lcrypto

chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" %{__python} setup.py build

%check
export PYTHONPATH=$PWD/build/lib*
%{__python} tests/test_internals.py -q

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}  --prefix %{_prefix}
 
%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc %{_prefix}/share/doc/pycurl/*
/%{python_sitearch}/curl/*
/%{python_sitearch}/pycurl*
