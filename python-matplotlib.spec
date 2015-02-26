%if 0%{?fedora} >= 18
%global with_python3            1
%global basepy3dir              %(echo ../`basename %{py3dir}`)
%else
%global with_python3            0
%endif
%global __provides_exclude_from	.*/site-packages/.*\\.so$
%global with_html               1
%global run_tests               0

# On RHEL 7 onwards, don't build with wx:
%if 0%{?rhel} >= 7
%global with_wx 0
%else
%global with_wx 1
%endif

# On Fedora 21 onwards, enable Qt5 backend:
%if 0%{?fedora} >= 21
%global with_qt5 1
%else
%global with_qt5 0
%endif

# the default backend; one of GTK GTKAgg GTKCairo GTK3Agg GTK3Cairo
# CocoaAgg MacOSX Qt4Agg Qt5Agg TkAgg WX WXAgg Agg Cairo GDK PS PDF SVG
%global backend                 TkAgg

%if "%{backend}" == "TkAgg"
%global backend_subpackage tk
%else
%  if "%{backend}" == "Qt4Agg"
%global backend_subpackage qt4
%  else
%    if "%{backend}" == "Qt5Agg"
%global backend_subpackage qt5
%    endif
%  endif
%endif

# https://fedorahosted.org/fpc/ticket/381
%global with_bundled_fonts      1

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:           python-matplotlib
Version:        1.4.3
Release:        4%{?dist}
Summary:        Python 2D plotting library
Group:          Development/Libraries
# qt4_editor backend is MIT
License:        Python and MIT
URL:            http://matplotlib.org
#Modified Sources to remove the bundled libraries
Source0:        matplotlib-%{version}-without-extern.tar.xz
Source1:        setup.cfg

Patch0:         %{name}-noagg.patch
Patch1:         %{name}-system-cxx.patch
Patch2:         20_matplotlibrc_path_search_fix.patch
Patch3:         40_bts608939_draw_markers_description.patch
Patch4:         50_bts608942_spaces_in_param_args.patch
Patch5:         70_bts720549_try_StayPuft_for_xkcd.patch

BuildRequires:  agg-devel
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  qhull-devel
BuildRequires:  python-six
BuildRequires:  numpy
BuildRequires:  pyparsing
BuildRequires:  python-pycxx-devel
BuildRequires:  python-dateutil
BuildRequires:  python-setuptools
%if %{with_html}
BuildRequires:  python-numpydoc
BuildRequires:  python-scikit-image
%endif
%if %{run_tests}
BuildRequires:  python-nose
%if %{with_python3}
BuildRequires:  python3-nose
%endif
%endif
BuildRequires:  python2-devel
BuildRequires:  pytz
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  zlib-devel
Requires:       dejavu-sans-fonts
Requires:       dvipng
Requires:       python-six
Requires:       numpy
Requires:       pyparsing
Requires:       python-dateutil
Requires:       pytz
%if 0%{?fedora} >= 18
Requires:	stix-math-fonts
%else
Requires:	stix-fonts
%endif
Requires:       %{name}-data = %{version}-%{release}

%{?backend_subpackage:Requires: %{name}-%{backend_subpackage}%{?_isa} = %{version}-%{release}}

%description
Matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell, web application servers, and
six graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%package        qt4
Summary:        Qt4 backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  PyQt4-devel
Requires:       PyQt4

%description    qt4
%{summary}

%if %{with_qt5}
%package        qt5
Summary:        Qt5 backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python-qt5
Requires:       python-qt5

%description    qt5
%{summary}
%endif # with_qt5

%package        gtk
Summary:        GTK backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  gtk2-devel
BuildRequires:  pygtk2-devel
BuildRequires:  pycairo-devel
Requires:       pycairo
Requires:       pygtk2

%description    gtk
%{summary}

%package        gtk3
Summary:        GTK3 backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This should be converted to typelib(Gtk) when supported
BuildRequires:  gtk3
BuildRequires:  pygobject3-base
Requires:       gtk3%{?_isa}
Requires:       pygobject3-base%{?_isa}

%description    gtk3
%{summary}

%package        tk
Summary:        Tk backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  tcl-devel
BuildRequires:  tkinter
BuildRequires:  tk-devel
Requires:       tkinter

%description    tk
%{summary}

%if %{with_wx}
%package        wx
Summary:        wxPython backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  wxPython-devel
Requires:       wxPython

%description    wx
%{summary}
%endif # with_wx

%package        doc
Summary:        Documentation files for python-matplotlib
Group:          Documentation
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{with_html}
BuildRequires:  python-sphinx
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  dvipng
BuildRequires:  graphviz
%endif

%description    doc
%{summary}

%package        data
Summary:        Data used by python-matplotlib
%if %{with_bundled_fonts}
Requires:       %{name}-data-fonts = %{version}-%{release}
%endif
BuildArch:      noarch

%description    data
%{summary}

%if %{with_bundled_fonts}
%package        data-fonts
Summary:        Fonts used by python-matplotlib
Requires:       %{name}-data = %{version}-%{release}
BuildArch:      noarch

%description    data-fonts
%{summary}
%endif

%if %{with_python3}
%package -n     python3-matplotlib
Summary:        Python 2D plotting library
Group:          Development/Libraries
BuildRequires:  python3-cairo
BuildRequires:  python3-dateutil
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-gobject
BuildRequires:  python3-numpy
BuildRequires:  python3-pycxx-devel
BuildRequires:  python3-pyparsing
BuildRequires:  python3-pytz
BuildRequires:  python3-six
Requires:       python3-six
Requires:       python3-numpy
Requires:       python3-cairo
Requires:       python3-pyparsing
Requires:       python3-dateutil
Requires:       python3-pytz
%if 0%{?fedora} >= 18
Requires:	stix-math-fonts
%else
Requires:	stix-fonts
%endif
Requires:       %{name}-data = %{version}-%{release}

Requires: python3-matplotlib-%{?backend_subpackage}%{!?backend_subpackage:tk}%{?_isa} = %{version}-%{release}

%description -n python3-matplotlib
Matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell, web application servers, and
six graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%package -n     python3-matplotlib-qt4
Summary:        Qt4 backend for python3-matplotlib
Group:          Development/Libraries
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
BuildRequires:  python3-PyQt4-devel
Requires:       python3-PyQt4

%description -n python3-matplotlib-qt4
%{summary}

%if %{with_qt5}
%package -n     python3-matplotlib-qt5
Summary:        Qt5 backend for python3-matplotlib
Group:          Development/Libraries
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
BuildRequires:  python3-qt5
Requires:       python3-qt5

%description -n python3-matplotlib-qt5
%{summary}
%endif # with_qt5

# gtk2 never worked in Python 3 afaict, so no need for -gtk subpackage
%package -n     python3-matplotlib-gtk3
Summary:        GTK3 backend for python3-matplotlib
Group:          Development/Libraries
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
# This should be converted to typelib(Gtk) when supported
BuildRequires:  gtk3
BuildRequires:  python3-gobject
Requires:       gtk3%{?_isa}
Requires:       python3-gobject%{?_isa}

%description -n python3-matplotlib-gtk3
%{summary}

%package -n     python3-matplotlib-tk
Summary:        Tk backend for python3-matplotlib
Group:          Development/Libraries
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
BuildRequires:  python3-tkinter
Requires:       python3-tkinter

%description -n python3-matplotlib-tk
%{summary}
%endif

%prep
%setup -q -n matplotlib-%{version}

# Copy setup.cfg to the builddir
cp %{SOURCE1} .
sed -i 's/\(backend = \).*/\1%{backend}/' setup.cfg

# Keep this until next version, and increment if changing from
# USE_FONTCONFIG to False or True so that cache is regenerated
# if updated from a version enabling fontconfig to one not
# enabling it, or vice versa
if [ %{version} = 1.4.3 ]; then
    sed -i 's/\(__version__ = 101\)/\1.1/' lib/matplotlib/font_manager.py
fi

%if !%{with_bundled_fonts}
# Use fontconfig by default
sed -i 's/\(USE_FONTCONFIG = \)False/\1True/' lib/matplotlib/font_manager.py
%endif

# Remove references to bundled libraries
%patch0 -b .noagg
%patch1 -b .cxx
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

chmod -x lib/matplotlib/mpl-data/images/*.svg

%if %{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
  xvfb-run %{__python2} setup.py build
%if %{with_html}
# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
    MPLCONFIGDIR=$PWD/.. \
    MATPLOTLIBDATA=$PWD/../lib/matplotlib/mpl-data \
    PYTHONPATH=`realpath ../build/lib.linux*` \
        %{__python2} make.py html
popd
%endif
# Ensure all example files are non-executable so that the -doc
# package doesn't drag in dependencies
find examples -name '*.py' -exec chmod a-x '{}' \;

%if %{with_python3}
pushd %{py3dir}
    MPLCONFIGDIR=$PWD \
    MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
      xvfb-run %{__python3} setup.py build
    # documentation cannot be built with python3 due to syntax errors
    # and building with python 2 exits with cryptic error messages
popd
%endif

%install
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data/ \
  %{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/dates.py
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir} $RPM_BUILD_ROOT%{_datadir}/matplotlib
mv $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/mpl-data/matplotlibrc \
   $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/mpl-data \
   $RPM_BUILD_ROOT%{_datadir}/matplotlib
%if !%{with_bundled_fonts}
rm -rf $RPM_BUILD_ROOT%{_datadir}/matplotlib/mpl-data/fonts
%endif

%if %{with_python3}
pushd %{py3dir}
    MPLCONFIGDIR=$PWD/.. \
    MATPLOTLIBDATA=$PWD/../lib/matplotlib/mpl-data/ \
        %{__python3} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
    chmod +x $RPM_BUILD_ROOT%{python3_sitearch}/matplotlib/dates.py
    rm -fr $RPM_BUILD_ROOT%{python3_sitearch}/matplotlib/mpl-data
    rm -f $RPM_BUILD_ROOT%{python3_sitearch}/six.py
popd
%endif

%if %{run_tests}
%check
# This should match the default backend
echo "backend      : %{backend}" > matplotlibrc
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$RPM_BUILD_ROOT%{_datadir}/matplotlib/mpl-data \
PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch} \
     xvfb-run %{__python} -c "import matplotlib; matplotlib.test()"

%if %{with_python3}
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$RPM_BUILD_ROOT%{_datadir}/matplotlib/mpl-data \
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} \
     xvfb-run %{__python3} -c "import matplotlib; matplotlib.test()"
%endif
%endif # run_tests

%files
%license LICENSE/
%doc README.rst
%doc CHANGELOG
%doc PKG-INFO
%{python_sitearch}/*egg-info
%{python_sitearch}/matplotlib-*-nspkg.pth
%{python_sitearch}/matplotlib/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%exclude %{python_sitearch}/matplotlib/backends/backend_qt4*
%exclude %{python_sitearch}/matplotlib/backends/backend_qt5*
%exclude %{python_sitearch}/matplotlib/backends/backend_gtk*
%exclude %{python_sitearch}/matplotlib/backends/_gtkagg.*
%exclude %{python_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/_tkagg.so
%exclude %{python_sitearch}/matplotlib/backends/backend_wx.*
%exclude %{python_sitearch}/matplotlib/backends/backend_wxagg.*
%exclude %{_pkgdocdir}/*/

%files qt4
%{python_sitearch}/matplotlib/backends/backend_qt4.*
%{python_sitearch}/matplotlib/backends/backend_qt4agg.*

%if %{with_qt5}
%files qt5
%{python_sitearch}/matplotlib/backends/backend_qt5.*
%{python_sitearch}/matplotlib/backends/backend_qt5agg.*
%endif # with_qt5

%files gtk
%{python_sitearch}/matplotlib/backends/backend_gtk.py*
%{python_sitearch}/matplotlib/backends/backend_gtkagg.py*
%{python_sitearch}/matplotlib/backends/backend_gtkcairo.py*
%{python_sitearch}/matplotlib/backends/_gtkagg.so

%files gtk3
%{python_sitearch}/matplotlib/backends/backend_gtk3*.py*

%files tk
%{python_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python_sitearch}/matplotlib/backends/tkagg.py*
%{python_sitearch}/matplotlib/backends/_tkagg.so

%if %{with_wx}
%files wx
%{python_sitearch}/matplotlib/backends/backend_wx.*
%{python_sitearch}/matplotlib/backends/backend_wxagg.*
%endif # with_wx

%files doc
%doc examples
%if %{with_html}
%doc doc/build/html/*
%endif

%files data
%{_sysconfdir}/matplotlibrc
%{_datadir}/matplotlib/mpl-data/
%if %{with_bundled_fonts}
%exclude %{_datadir}/matplotlib/mpl-data/fonts/
%endif

%if %{with_bundled_fonts}
%files data-fonts
%{_datadir}/matplotlib/mpl-data/fonts/
%endif

%if %{with_python3}
%files -n python3-matplotlib
%license %{basepy3dir}/LICENSE/
%doc %{basepy3dir}/README.rst
%doc %{basepy3dir}/CHANGELOG
%doc %{basepy3dir}/PKG-INFO
%{python3_sitearch}/*egg-info
%{python3_sitearch}/matplotlib-*-nspkg.pth
%{python3_sitearch}/matplotlib/
%{python3_sitearch}/mpl_toolkits/
%{python3_sitearch}/pylab.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/matplotlib/backends/backend_qt4*
%exclude %{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt4*
%exclude %{python3_sitearch}/matplotlib/backends/backend_qt5*
%exclude %{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt5*
%exclude %{python3_sitearch}/matplotlib/backends/backend_gtk*
%exclude %{python3_sitearch}/matplotlib/backends/__pycache__/backend_gtk*
%exclude %{python3_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/__pycache__/backend_tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/__pycache__/tkagg.*
%exclude %{python3_sitearch}/matplotlib/backends/_tkagg.*
%exclude %{_pkgdocdir}/*/

%files -n python3-matplotlib-qt4
%{python3_sitearch}/matplotlib/backends/backend_qt4.*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt4.*
%{python3_sitearch}/matplotlib/backends/backend_qt4agg.*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt4agg.*

%if %{with_qt5}
%files -n python3-matplotlib-qt5
%{python3_sitearch}/matplotlib/backends/backend_qt5.*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt5.*
%{python3_sitearch}/matplotlib/backends/backend_qt5agg.*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_qt5agg.*
%endif # with_qt5

%files -n python3-matplotlib-gtk3
%{python3_sitearch}/matplotlib/backends/backend_gtk*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_gtk*

%files -n python3-matplotlib-tk
%{python3_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python3_sitearch}/matplotlib/backends/__pycache__/backend_tkagg.*
%{python3_sitearch}/matplotlib/backends/tkagg.*
%{python3_sitearch}/matplotlib/backends/__pycache__/tkagg.*
%{python3_sitearch}/matplotlib/backends/_tkagg.*
%endif

%changelog
* Wed Feb 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.3-4
- Split out python-matplotlib-gtk, python-matplotlib-gtk3,
  python3-matplotlib-gtk3 subpackages (#1067373)
- Add missing requirements on gtk

* Tue Feb 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.3-3
- Use %%license, add skimage to build requirements

* Tue Feb 17 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.3-2
- Disable Qt5 backend on Fedora <21 and RHEL

* Tue Feb 17 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.3-1
- New upstream release (#1134007)
- Add Qt5 backend

* Tue Jan 13 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.2-1
- Bump to new upstream release
- Add qhull-devel to BR
- Add six to Requires

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 11 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.1-3
- Make TkAgg the default backend
- Remove python2 dependency from -data subpackage

* Mon Jan 27 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.1-2
- Correct environment for and enable %%check
- Install system wide matplotlibrc under /etc
- Do not duplicate mpl-data for python2 and python3 packages
- Conditionally bundle data fonts (https://fedorahosted.org/fpc/ticket/381)

* Sat Jan 25 2014 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-1
- update to 1.3.1
- use GTKAgg as backend (#1030396, #982793, #1049624)
- use fontconfig
- add %%check for local testing (testing requires a display)

* Wed Aug  7 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.3.0-1
- update to new version
- use xz to compress sources
- drop fontconfig patch (upstream)
- drop tk patch (upstream solved build issue differently)
- redo use system agg patch
- delete bundled python-pycxx headers
- fix requires of python3-matplotlib-qt (fixes #988412)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jon Ciesla <limburgher@gmail.com> - 1.2.0-14
- agg rebuild.

* Wed Apr 10 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.2.0-13
- use python3 version in python3-matplotlib-qt4 (#915727)
- include __pycache__ files in correct subpackages on python3

* Wed Apr  3 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.2.0-12
- Decode output of subprocess to utf-8 or regex will fail (#928326)

* Tue Apr  2 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-11
- Make stix-fonts a requires of matplotlib (#928326)

* Thu Mar 28 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-10
- Use stix fonts avoid problems with missing cm fonts (#908717)
- Correct type mismatch in python3 font_manager (#912843, #928326)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-8
- Update fontconfig patch to apply issue found by upstream
- Update fontconfig patch to apply issue with missing afm fonts (#896182)

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-7
- Use fontconfig by default (#885307)

* Thu Jan  3 2013 David Malcolm <dmalcolm@redhat.com> - 1.2.0-6
- remove wx support for rhel >= 7

* Tue Dec 04 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-5
- Reinstantiate wx backend for python2.x.
- Run setup.py under xvfb-run to detect and default to gtk backend (#883502)
- Split qt4 backend subpackage and add proper requires for it.
- Correct wrong regex in tcl libdir patch.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-4
- Obsolete python-matplotlib-wx for clean updates.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-3
- Enable python 3 in fc18 as build requires are now available (#879731)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-2
- Build python3 only on f19 or newer (#837156)
- Build requires python3-six if building python3 support (#837156)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-1
- Update to version 1.2.0
- Revert to regenerate tarball with generate-tarball.sh (#837156)
- Assume update to 1.2.0 is for recent releases
- Remove %%defattr
- Remove %%clean
- Use simpler approach to build html documentation
- Do not use custom/outdated setup.cfg
- Put one BuildRequires per line
- Enable python3 support
- Cleanup spec as wx backend is no longer supported
- Use default agg backend
- Fix bogus dates in changelog by assuming only week day was wrong

* Fri Aug 17 2012 Jerry James <loganjerry@gmail.com> - 1.1.1-1
- Update to version 1.1.1.
- Remove obsolete spec file elements
- Fix sourceforge URLs
- Allow sample data to have a different version number than the sources
- Don't bother removing problematic file since we remove entire agg24 directory
- Fix building with pygtk in the absence of an X server
- Don't install license text for bundled software that we don't bundle

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 3 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1.0-1
- Update to version 1.1.0.
- Do not regenerate upstream tarball but remove problematic file in %%prep.
- Remove non longer applicable/required patch0.
- Rediff/rename -noagg patch.
- Remove propagate-timezone-info-in-plot_date-xaxis_da patch already applied.
- Remove tkinter patch now with critical code in a try block.
- Remove png 1.5 patch as upstream is now png 1.5 aware.
- Update file list.

* Wed Apr 18 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.1-20
- remove wx support for rhel >= 7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-19
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-17
- fix the build against libpng 1.5

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-16
- fix egg-info conditional for RHEL

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-15
- Rebuild for new libpng

* Mon Oct 31 2011 Dan Horák <dan[at]danny.cz> - 1.0.1-14
- fix build with new Tkinter which doesn't return an expected value in __version__

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.0.1-13
- apply upstream bugfix for timezone formatting (Bug 735677) 

* Fri May 20 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-12
- Add Requires dvipng (Bug 684836)
- Build against system agg (Bug 612807)
- Use system pyparsing (Bug 702160)

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-11
- Set PYTHONPATH during html doc building using find to prevent broken builds

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-10
- Spec file cleanups for readability

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-9
- Bump and rebuild

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-8
- Fix spec file typos so package builds

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-7
- Remove a debugging echo statement from the spec file
- Fix some line endings and permissions in -doc sub-package

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-6
- Spec file cleanups to silence some rpmlint warnings

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-5
- Add default attr to doc sub-package file list
- No longer designate -doc subpackage as noarch
- Add arch specific Requires for tk, wx and doc sub-packages

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-4
- Enable wxPython backend
- Make -doc sub-package noarch

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-3
- Add conditional for optionally building doc sub-package
- Add flag to build low res images for documentation
- Add matplotlib-1.0.1-plot_directive.patch to fix build of low res images
- Remove unused patches

* Sat Feb 19 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-2
- Build and package HTML documentation in -doc sub-package
- Move examples to -doc sub-package
- Make examples non-executable

* Fri Feb 18 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.0.1-1
- update to new bugfix version (#678489)
- set file attributes in tk subpackage
- filter private *.so

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 8 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.0.0-1
- New upstream release  
- Remove undistributable file from bundled agg library 

* Thu Jul 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.3-1
- New upstream release  

* Thu May 27 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-4
- Upstream patch to fix deprecated gtk tooltip warning.  

* Mon Apr 12 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-2
- Bump to rebuild against numpy 1.3  

* Thu Apr 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-1
- Bump to rebuild against numpy 1.4.0  

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.1.2
- Update to 0.99.1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-4
- Fixed font dep after font guideline change

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-2
- Add dep on DejaVu Sans font for default font support

* Mon Dec 22 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-1
- Latest upstream release
- Strip out included fonts

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.98.3-2
- Rebuild for Python 2.6

* Wed Aug  6 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.3-1
- Latest upstream release

* Tue Jul  1 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.1-1
- Latest upstream release

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-2
- gcc43 cleanups

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-1
- New upstream version
- Adding Fedora specific setup.cfg from included template
- removed numarry and numerics build requirements

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.90.1-6
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-5
- Fixed typo in spec.

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-4
- Support for Python Eggs for F9+

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-3
- Rebuild for new Tcl 8.5

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-2
- Update license tag to Python
- Rebuild for BuildID

* Mon Jun 04 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-1
- Update to 0.90.1

* Wed Feb 14 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-2
- Rebuild for Tcl/Tk downgrade

* Sat Feb 10 2007 Jef Spaleta <jspaleta@gmail.com> 0.90.0-2
- Release bump for rebuild against new tk 

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-1
- Update to 0.90.0

* Fri Jan  5 2007 Orion Poplawski <orion@cora.nwra.com> 0.87.7-4
- Add examples to %%docs

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 0.87.7-3
- Release bump for rebuild against python 2.5 in devel tree

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-2
- Force build of gtk/gtkagg backends in mock (bug #218153)
- Change Requires from python-numeric to numpy (bug #218154)

* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-1
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
- Add private directories to %%files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras
