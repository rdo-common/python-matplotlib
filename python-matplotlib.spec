%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-matplotlib
Version:        0.87.7
Release:        1%{?dist}
Summary:        Python plotting library

Group:          Development/Libraries
License:        Python Software Foundation License 
URL:            http://sourceforge.net/projects/matplotlib
Source0:        http://dl.sf.net/matplotlib/matplotlib-%{version}.tar.gz
Patch0:         matplotlib-0.87.7-matplotlibrc.patch
Patch1:         matplotlib-0.87.7-tkagg-check.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, freetype-devel, libpng-devel, zlib-devel
BuildRequires:  pygtk2-devel, gtk2-devel, tkinter, tk-devel
BuildRequires:  python-numeric, pytz, python-dateutil, numpy, python-numarray
Requires:       python-numeric, pytz, python-dateutil
Requires:       pycairo >= 1.2.0


%description
Matplotlib is a pure python plotting library with the goal of making
publication quality plots using a syntax familiar to matlab users. The
library uses Numeric for handling large data sets and supports a variety
of output backends


%package        tk
Summary:        Tk backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       tkinter

%description    tk
%{summary}


%prep
%setup -q -n matplotlib-%{version}
%patch0 -p1 -b .matplotlibrc
%patch1 -p1 -b setup.py 
chmod -x images/*.svg

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/dates.py

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
%exclude %{python_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/_tkagg.so

%files tk
%{python_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python_sitearch}/matplotlib/backends/tkagg.py*
%{python_sitearch}/matplotlib/backends/_tkagg.so


%changelog
* Tue Nov  21 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-1
- Update to 0.87.7 and fix up the defaults to use numpy
- Force build of tkagg backend without X server
- Use src.rpm from Jef Spaleta, closes bug 216578

* Fri Oct  6 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.6-1
- Update to 0.87.6

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.5-1
- Update to 0.87.5

* Thu Jul 27 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.4-1
- Update to 0.87.4

* Wed Jun  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.3-1
- Update to 0.87.3

* Mon May 15 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-2
- Rebuild for new numpy

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-1
- Update to 0.87.2

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.1-1
- Update to 0.87.1
- Add pycairo >= 1.0.2 requires (FC5+ only)

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.87-1
- Update to 0.87
- Add BR numpy and python-numarray
- Add patch to keep Numeric as the default numerix package
- Add BR tkinter and tk-devel for TkInter backend
- Make separate package for Tk backend

* Tue Jan 10 2006 Orion Poplawski <orion@cora.nwra.com> 0.86-1
- Update to 0.86

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-2
- Rebuild

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-1
- New upstream version 0.85

* Mon Sep 19 2005 Orion Poplawski <orion@cora.nwra.com> 0.84-1
- New upstream version 0.84

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-3
- bump release 

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-2
- Add Requires: python-numeric, pytz, python-dateutil

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
