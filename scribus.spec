Name:           scribus
Version:        1.1.7
Release:        0.fdr.3.1
Epoch:          0
Summary:        DeskTop Publishing app in QT.

Group:          Applications/Productivity
License:        GPL
URL:            http://www.scribus.net/
#Link from site does not allow direct download.
#Source0:       http://ahnews.music.salford.ac.uk/scribus/scribus-1.1.7.tar.bz2
Source0:        http://web2.altmuehlnet.de/fschmid/scribus-1.1.7.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt-devel >= 1:3.0.5
BuildRequires:  XFree86-devel
BuildRequires:  zlib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  cups-devel
BuildRequires:  lcms-devel
BuildRequires:  libart_lgpl-devel
BuildRequires:  openssl-devel
BuildRequires:  libtool
BuildRequires:  python-devel >= 0:2.2
BuildRequires:  desktop-file-utils
Requires:       python >= 0:2.2
Requires:       ghostscript >= 0:7.07
Requires:       tkinter

Obsoletes:      scribus-svg
Obsoletes:      scribus-scripting
Provides:       scribus-scripting

%description
Scribus is a Layout program for GNU/Linux®, similar to Adobe® PageMaker™,
QuarkXPress™ or Adobe® InDesign™, except that it is published under the
GNU GPL.

While the goals of the program are for ease of use and simple easy to
understand tools, Scribus offers support for professional publishing
features, such as CMYK color, easy PDF creation, Encapsulated Postscript
import/export and creation of color separations.


%package        devel
Summary:        Header files for Scribus.
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
Header files for Scribus.



%prep
%setup -q



%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
%configure  \
   --with-pythondir=%{_prefix}
make %{?_smp_mflags}



%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

install -p -D -m0644 scribus/icons/scribusicon.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/scribusicon.png
desktop-file-install --vendor fedora                   \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications      \
  --add-category Application                           \
  --add-category X-Fedora                              \
  scribus.desktop

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'



%clean
rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/scribus
%{_libdir}/scribus/
%{_datadir}/scribus/
%{_datadir}/pixmaps/scribusicon.png
%{_datadir}/applications/fedora-%{name}.desktop

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_includedir}/scribus/



%changelog
* Fri Jul 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.3
- BuildReq openssl-devel (#1727).

* Thu Jun 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.2
- Source0 allows direct download (#1727).
- Req tkinter (#1727).

* Sun Jun 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.1
- Updated to 1.1.7.
- Re-added _smp_mflags.

* Mon May 24 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.3
- Add Application Category to desktop entry.

* Sun Apr 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.2
- Bump ghostscript Req to 7.07.
- URL scribus.net.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.1
- Updated to 1.1.6.
- Using upstream desktop entry.

* Sat Feb 14 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.5-0.fdr.1
- Updated to 1.1.5.

* Sun Dec 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.4-0.fdr.1
- Updated to 1.1.4.

* Thu Dec 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.3-0.fdr.2
- Dropped LDFLAGS="-lm"
- Added --with-pythondir=%%{_prefix}
- Req ghostscript.

* Sun Nov 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.3-0.fdr.1
- Updated to 1.1.3.
- Removed _smp_mflags.

* Tue Nov 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.2-0.fdr.2
- Req python.
- Provides scribus-scripting.

* Sun Nov 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.2-0.fdr.1
- Updated to 1.1.2.
- Obsoletes scribus-scripting.

* Sat Oct 11 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.1-0.fdr.2
- BuildReq littlecms-devel -> lcms-devel.

* Thu Oct 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.1-0.fdr.1
- Updated to 1.1.1.
- BuildReq littlecms-devel.
- BuildReq libart_lgpl-devel.

* Wed Sep 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0.1-0.fdr.1
- Updated to 1.0.1.
- Split off devel package for headers.
- No longer Obsoletes scribus-i18n-en

* Thu Jul 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.3
- desktop entry terminal=0 -> false.

* Tue Jul 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.2
- Added Obsoletes scribus-i18n-en.

* Tue Jul 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.1
- Updated to 1.0.

* Tue Jul 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.0.1.rc1
- Updated to 1.0RC1.

* Fri Jun 20 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.11.1-0.fdr.1
- Updated to 0.9.11.1.
- Added obsoletes scribus-svg.

* Sun May 25 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.3
- Using make DESTDIR= workaround for plugin issue.
- Removed post/postun ldconfig.
- Removed devel subpackage.

* Mon May 19 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.2
- Explicitly set file permission on icon.
- Created devel package.
- Removed .la files.
- Added ChangeLog to Documentation.

* Sun May 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.1
- Updated to 0.9.10.
- buildroot -> RPM_BUILD_ROOT.

* Sat Apr 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.3
- Added BuildRequires for cups-devel.

* Thu Apr 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.2
- Added BuildRequires for libtiff-devel.
- Added line to help package find tiff.

* Sun Apr 20 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.1
- Updated to 0.9.9.
- Added line for QT.

* Thu Apr 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.8-0.fdr.3.rh90
- Added missing BuildRequires.
- Corrected Group.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.8-0.fdr.2
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.
- Added Epoch:0.

* Thu Mar 27 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.9.8-0.fdr.1
- Initial RPM release.
