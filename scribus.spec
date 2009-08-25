Name:           scribus
Version:        1.3.5.1
Release:        3%{?dist}

Summary:        DeskTop Publishing application written in Qt

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://www.scribus.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-1.3.5-system-hyphen.patch
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
BuildRequires:  python-devel
BuildRequires:  python-imaging-devel
BuildRequires:  qt-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  gnutls-devel
BuildRequires:  cairo-devel
BuildRequires:  aspell-devel
BuildRequires:  boost-devel
BuildRequires:  podofo-devel
BuildRequires:  hyphen-devel
Requires:       ghostscript
Requires:       python
Requires:       python-imaging
Requires:       tkinter
Requires:       shared-mime-info
Requires:       %{name}-doc = %{version}-%{release}


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
%if 0%{?fedora} > 9
BuildArch:      noarch
Obsoletes:      %{name}-doc < 1.3.5-0.12.beta
%endif


%description    doc
%{summary}

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .system-hyphen

# recode man page to UTF-8
pushd scribus/manpages
iconv -f ISO8859-2 -t UTF-8 scribus.1.pl > tmp
touch -r scribus.1.pl tmp
mv tmp scribus.1.pl
popd

# fix permissions
chmod a-x scribus/pageitem_latexframe.h

# drop shebang lines from python scripts
for f in scribus/plugins/scriptplugin/{samples,scripts}/*.py
do
    sed '1{/#!\/usr\/bin\/env\|#!\/usr\/bin\/python/d}' $f > $f.new
    touch -r $f $f.new
    mv $f.new $f
done


%build
mkdir build
pushd build
%cmake ..

%ifnarch s390x
make VERBOSE=1 %{?_smp_mflags}
%else
# we can't use parallel build on s390x, because g++ eats almost all memory
# in the builder (2+0.5 GB) when compiling scribus134format.cpp
make VERBOSE=1
%endif
popd


%install
rm -rf ${RPM_BUILD_ROOT}
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribus.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/scribus.png
install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribusdoc.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/x-scribus.png

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

# install the global desktop file
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mimelnk/application/*scribus.desktop
desktop-file-install --vendor="fedora"                      \
    --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
    scribus.desktop


%clean
rm -rf ${RPM_BUILD_ROOT}


%post
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :


%postun
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :


%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-%{version}/AUTHORS
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLogSVN
%doc %{_datadir}/doc/%{name}-%{version}/COPYING
%doc %{_datadir}/doc/%{name}-%{version}/README
%doc %{_datadir}/doc/%{name}-%{version}/TODO
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/samples/*.py[co]
%exclude %{_datadir}/%{name}/scripts/*.py[co]
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
%{_mandir}/de/man1/*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_includedir}/%{name}

%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/doc/%{name}-%{version}
%lang(cs) %{_datadir}/doc/%{name}-%{version}/cs
%lang(de) %{_datadir}/doc/%{name}-%{version}/de
%lang(en) %{_datadir}/doc/%{name}-%{version}/en
%lang(fr) %{_datadir}/doc/%{name}-%{version}/fr
%lang(pl) %{_datadir}/doc/%{name}-%{version}/pl
%{_datadir}/doc/%{name}-%{version}/BUILDING
%{_datadir}/doc/%{name}-%{version}/NEWS
%{_datadir}/doc/%{name}-%{version}/README*
%{_datadir}/doc/%{name}-%{version}/PACKAGING
%{_datadir}/doc/%{name}-%{version}/LINKS
%{_datadir}/doc/%{name}-%{version}/TRANSLATION


%changelog
* Tue Aug 25 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5.1-3
- drop shebang line from python scripts
- don't package precompiled python scripts

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.5.1-2
- rebuilt with new openssl

* Thu Aug 20 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5.1-1
- update to final 1.3.5.1
- drop the upstreamed "install-headers" patch
- always install doc subpackage (#446148)
- full changelog: http://www.scribus.net/?q=node/193

* Wed Jul 29 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.17.rc3
- don't use parallel build on s390x

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-0.16.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.15.rc3
- update to 1.3.5-rc3
- use system hyphen library (#506074)
- fix update path for the doc subpackage (#512498)
- preserve directories when installing headers (#511800)

* Thu Jun  4 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.14.rc2
- update to 1.3.5-rc2

* Mon May 18 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.13.beta
- rebuilt with podofo enabled

* Wed Apr 22 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.12.beta
- update to 1.3.5.beta
- make docs subpackage noarch
- drop outdated Obsoletes/Provides

* Sun Mar 29 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.11.20090329svn13359
- update to revision 13359
- add aspell-devel and boost-devel as BR
- update release tag to conform to the pre-release versioning guideline

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-0.10.12516svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.4-0.9.12516svn
- rebuild with new openssl

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.5-0.8.12516svn
- Rebuild for Python 2.6

* Tue Dec  2 2008 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.7.12516svn
- fix directory ownership in doc subpackage (#474041)

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.5-0.6.12516svn
- Rebuild for Python 2.6

* Mon Oct 13 2008 Dan Horák <dan[AT]danny.cz> 1.3.5-0.5.12516svn
- install global desktop file instead of KDE-only one (#461124)
- little cleanup

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
