%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-matplotlib
Version:        0.82
Release:        3%{?dist}
Summary:        Python plotting library

Group:          Development/Libraries
License:        Python Software Foundation License 
URL:            http://sourceforge.net/projects/matplotlib
Source0:        http://dl.sf.net/matplotlib/matplotlib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, freetype-devel, libpng-devel, zlib-devel
BuildRequires:  python-numeric, pygtk2-devel, gtk2-devel

%description
Matplotlib is a pure python plotting library with the goal of making
publication quality plots using a syntax familiar to matlab users. The
library uses Numeric for handling large data sets and supports a variety
of output backends

%prep
%setup -q -n matplotlib-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%doc README license/LICENSE license/LICENSE_enthought.txt
%doc license/LICENSE_PAINT license/LICENSE_PIL license/PYTZ_LICENSE.txt
%doc API_CHANGES CHANGELOG CXX INSTALL INTERACTIVE KNOWN_BUGS
%doc NUMARRAY_ISSUES PKG-INFO TODO
%dir %{python_sitearch}/matplotlib
%dir %{_datadir}/matplotlib

%changelog
* Fri Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-3
- Use %{python_sitearch}

* Thu Jun 30 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-2
- Rename to python-matplotlib
- Remove unneeded Requires: python
- Add private directories to %files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras
