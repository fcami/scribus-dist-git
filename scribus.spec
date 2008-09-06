Name:           scribus
Version:        1.3.5
Release:	0.4.12516svn%{?dist}

Summary:        DeskTop Publishing application written in Qt

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://www.scribus.net/
# obtained via svn co -r 12516 svn://scribus.info/Scribus/trunk/Scribus
Source0:        scribus-svn-12516.tar.bz2
Source1:        scribus.xml
Source2:	scribus.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  lcms-devel
BuildRequires:  libart_lgpl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  python-devel >= 2.3
BuildRequires:  python-imaging-devel
BuildRequires:  qt-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  gnutls-devel
BuildRequires:  cairo-devel
Requires:       ghostscript >= 7.07
Requires:       python >= 2.3
Requires:       python-imaging
Requires:       tkinter
Requires(post): shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): shared-mime-info
Requires(postun): desktop-file-utils

Obsoletes:     scribus-i18n-en
Obsoletes:     scribus-svg
Obsoletes:     scribus-scripting
Obsoletes:     scribus-short-words
Obsoletes:     scribus-vnla
Obsoletes:     scribus-i18en
Obsoletes:     scribus-i18de
Obsoletes:     scribus-i18fr
Obsoletes:     scribus-templates

Provides:      scribus-i18n-en
Provides:      scribus-svg
Provides:      scribus-scripting
Provides:      scribus-short-words
Provides:      scribus-vnla
Provides:      scribus-i18en
Provides:      scribus-i18de
Provides:      scribus-i18fr
Provides:      scribus-templates

%description
Scribus is an desktop open source page layout program with
the aim of producing commercial grade output in PDF and
Postscript, primarily, though not exclusively for Linux.

While the goals of the program are for ease of use and simple easy to
understand tools, Scribus offers support for professional publishing
features, such as CMYK color, easy PDF creation, Encapsulated Postscript
import/export and creation of color separations.


%package        devel
Summary:        Header files for Scribus
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files for Scribus.

%package        doc
Summary:        Documentation files for Scribus
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    doc
%{summary}

%prep
%setup -q -n Scribus


%build
mkdir build
cd build
%cmake -DOPENSYNC_LIBEXEC_DIR=%{_libexecdir} \
    -DCMAKE_SKIP_RPATH=YES  ../
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
cd build
make install DESTDIR=$RPM_BUILD_ROOT

install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribusicon.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/scribusicon.png
install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribusdoc.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/x-scribus.png

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}


%post
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%postun
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLogSVN COPYING README TODO
%{_bindir}/scribus
#%{_datadir}/applications/fedora-scribus.desktop
%{_datadir}/mime/packages/scribus.xml
%{_datadir}/mimelnk/application/*scribus.desktop
%{_datadir}/pixmaps/*
%{_datadir}/scribus/
%{_libdir}/scribus/
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
%{_mandir}/de/man1/*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_includedir}/scribus/

%files doc
%defattr(-,root,root,-)
%lang(cd) %{_datadir}/doc/%{name}-1.3.5svn/cs/*
%lang(de) %{_datadir}/doc/%{name}-1.3.5svn/de/*
%lang(en) %{_datadir}/doc/%{name}-1.3.5svn/en/*
%lang(fr) %{_datadir}/doc/%{name}-1.3.5svn/fr/*
%lang(pl) %{_datadir}/doc/%{name}-1.3.5svn/pl/*
%{_datadir}/doc/%{name}-1.3.5svn/AUTHORS
%{_datadir}/doc/%{name}-1.3.5svn/BUILDING
%{_datadir}/doc/%{name}-1.3.5svn/ChangeLog
%{_datadir}/doc/%{name}-1.3.5svn/ChangeLogSVN
%{_datadir}/doc/%{name}-1.3.5svn/COPYING
%{_datadir}/doc/%{name}-1.3.5svn/NEWS
%{_datadir}/doc/%{name}-1.3.5svn/README*
%{_datadir}/doc/%{name}-1.3.5svn/TODO
%{_datadir}/doc/%{name}-1.3.5svn/PACKAGING

 

%changelog
* Fri Sep 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.4.12516svn
- new svn snapshot

* Sun Jul 27 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.3.12419svn
- new svn snapshot

* Mon Jul 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.2.12404svn
- svn snapshot

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.4-5
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.3.4-4
- Rebuilt for gcc43

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-3
- fix inclusion of python scripts as proposed by Todd Zullinger (#312091)
- fix desktop file

* Thu Aug 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-2
- rebuild for buildid
- new license tag

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.4
- version upgrade

* Mon Dec 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.6-1
- version upgrade

* Sat Nov 11 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.5-1
- version upgrade

* Wed Oct 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.4-1
- version upgrade

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.3-1
- version upgrade (#205962)

* Sun Jun 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.2-2
- bump

* Tue May 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.2-1
- version upgrade

* Sat Apr 22 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.1-1
- version upgrade

* Tue Mar 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3-1
- version upgrade
- add BR gnutls-devel

* Sat Mar 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.2-1
- upgrade to beta version

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-4
- Rebuild for Fedora Extras 5

* Wed Feb 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-3
- add missing requires python-imaging

* Sat Jan 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-2
- rebuild (#178494)

* Wed Jan 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-1
- version upgrade

* Thu Jul 7 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.2.1-2
- use dist tag for sanity between branches

* Tue Jul 5 2005 P Linnell <mrdocs AT scribus.info> - 1.2.2.1-1
- 1.2.2.1 released to fix crash on open with certain 1.2.1 docs

* Sun Jul 3 2005 P Linnell <mrdocs AT scribus.info> - 1.2.2-0.fc4
- 1.2.2 final

* Tue Jun 28 2005 P Linnell <mrdocs AT scribus.info>- 1.2.2cvs-0
- test build for 1.2.2cvs
- Add freetype2 explicit build requirement
- Add obsoletes. See PACKAGING in the source tarball
- Change the description per PACKAGING
- Bump required python. 2.2 is no longer supported.


* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.1-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 06 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-3
- Bumped BR on qt-devel to 3.3.

* Thu Feb  3 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.1-2
- Fix x86_64 build and summary.

* Sun Jan 09 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-1
- 1.2.1.

* Sat Dec 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-0.1.cvs20041118
- cvs snapshot.

* Wed Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2-0.fdr.3
- Redirect output in post/postun, to avoid failure.

* Wed Nov 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2-0.fdr.2
- Mime-type corrections for FC3.
- Dropped redundent BR XFree86-devel.

* Thu Aug 26 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.2-0.fdr.1
- 1.2.
- Dropping old obsoletes/provides (don't know of anyone using them).

* Thu Aug 19 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.2-0.fdr.0.RC1
- 1.2RC1.

* Sat Aug 07 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.4
- mime info/icon for .sla files.

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
