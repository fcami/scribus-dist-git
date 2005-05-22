Name:           scribus
Version:        1.2.1
Release: 5

Summary:        DeskTop Publishing application written in Qt

Group:          Applications/Productivity
License:        GPL
URL:            http://www.scribus.net/
Source0:        http://www.scribus.org.uk/downloads/1.2.1/scribus-1.2.1.tar.bz2
Source1:        scribus.xml
Patch0:         scribus-x86_64.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  lcms-devel
BuildRequires:  libart_lgpl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  python-devel >= 2.2
BuildRequires:  qt-devel >= 1:3.3
BuildRequires:  zlib-devel
Requires:       ghostscript >= 7.07
Requires:       python >= 2.2
Requires:       tkinter
Requires(post): shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): shared-mime-info
Requires(postun): desktop-file-utils

Obsoletes:      scribus-i18n-en


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
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files for Scribus.


%prep
%setup -q
%patch -p1 -b .x86_64


%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
%configure  \
   --with-pythondir=%{_prefix}
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

install -p -D -m0644 scribus/icons/scribusicon.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/scribusicon.png
install -p -D -m0644 scribus/icons/scribusdoc.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/x-scribus.png
install -p -D -m0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/scribus.xml

desktop-file-install --vendor fedora                \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications   \
  --add-category X-Fedora                           \
 scribus.desktop

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
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/scribus
%{_datadir}/applications/fedora-scribus.desktop
%{_datadir}/mime/packages/scribus.xml
%{_datadir}/pixmaps/*
%{_datadir}/scribus/
%{_libdir}/scribus/
%{_mandir}/man1/*
%{_mandir}/pl/man1/*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_includedir}/scribus/


%changelog
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
