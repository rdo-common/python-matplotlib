%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-matplotlib
Version:        0.83.2
Release:        1%{?dist}
Summary:        Python plotting library

Group:          Development/Libraries
License:        Python Software Foundation License 
URL:            http://sourceforge.net/projects/matplotlib
Source0:        http://dl.sf.net/matplotlib/matplotlib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, freetype-devel, libpng-devel, zlib-devel
BuildRequires:  python-numeric, pygtk2-devel, gtk2-devel
BuildRequires:  pytz, python-dateutil

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
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/dates.py
chmod -x $RPM_BUILD_ROOT%{_datadir}/matplotlib/*.svg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README license/LICENSE license/LICENSE_enthought.txt
%doc license/LICENSE_PAINT license/LICENSE_PIL
%doc API_CHANGES CHANGELOG CXX INSTALL INTERACTIVE KNOWN_BUGS
%doc NUMARRAY_ISSUES PKG-INFO TODO
%{python_sitearch}/matplotlib/
%{python_sitearch}/pylab.py*
%{_datadir}/matplotlib/

%changelog
* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-1
- New upstream version matplotlib 0.83.2

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-2
- Bump rel to fix botched tag

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-1
- New upstream version matplotlib 0.83.1

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-4
- BuildRequires: pytz, python-dateutil - use upstream
- Don't use INSTALLED_FILES, list dirs
- Fix execute permissions

* Fri Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-3
- Use %%{python_sitearch}

* Thu Jun 30 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-2
- Rename to python-matplotlib
- Remove unneeded Requires: python
- Add private directories to %files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras
