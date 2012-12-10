%bcond_with     ecj
%bcond_without  qt
%bcond_with     gjdoc
%bcond_with     plugin

%define javaver 1.5.0
%define libname %mklibname %{name}

Name:		classpath
Version:	0.97.2
Release:	7
Epoch:		0
Summary:	GNU Classpath, Essential Libraries for Java
Group:		Development/Java
License:	GPL-like
URL:		http://www.classpath.org/
Source0:	http://builder.classpath.org/dist/classpath-%{version}.tar.gz
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(dssi)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	magic-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	gcc-java
BuildRequires:	gcj-tools
BuildRequires:	java-rpmbuild
%if %with ecj
BuildRequires:	eclipse-ecj
%endif
%if %with gjdoc
# Need to use gjdoc because of the -licensetext option
BuildRequires:	gjdoc
%else
Obsoletes:	classpath-javadoc
%endif
%if %with plugin
BuildRequires:	mozilla-firefox-devel
%endif
%if %with qt
BuildRequires:	qt4-devel >= 0:4.1.0
%endif

%description
GNU Classpath, Essential Libraries for Java, is a GNU project to
create free core class libraries for use with virtual machines and
compilers for the java programming language.

%package devel
Summary:	Devlopment headers and examples for GNU Classpath
Group:		Development/Java
Requires:	classpath = %{EVRD}

%description devel
%{summary}.

%if %with gjdoc
%package javadoc
Summary:	API documentation for GNU Classpath
Group:		Development/Java
Provides:	java-javadoc = 0:%{javaver}
Provides:	java-%{javaver}-javadoc = 0:%{javaver}

%description javadoc
%{summary}.
%endif

%if %with qt
%package qt
Summary:	QT4 peer for GNU Classpath
Group:		Development/Java

%description qt
%{summary}.
%endif

%if %with plugin
%package -n mozilla-plugin-gcjwebplugin
Summary:	Plugin to execute Java (tm) applets in Mozilla and compatible browsers
Group:		Development/Java
Requires:	mozilla-firefox
Provides:	mozilla-plugin-gcj = %{EVRD}
Provides:	gcjwebplugin = %{EVRD}
Provides:	java-plugin = %{epoch}:%{javaver}
Provides:	java-%{javaver}-plugin = %{EVRD}
Requires:	classpath = %{EVRD}

%description -n mozilla-plugin-gcjwebplugin
gcjwebplugin is a plugin to execute Java (tm) applets in Mozilla and
compatible browsers. It uses the JVM provided by GCJ and adds a
SecurityManager suitable for applets.

WARNING: The current version does not provide a security manager capable
of handling Java (tm) applets. Applets have UNRESTRICTED access to your
computer. This means they can do anything you can do, like deleting all
your important data.
%endif

%prep
%setup -q
%__perl -pi -e 's|^tools_cp=.*|tools_cp="%{_datadir}/%{name}/glibj.zip:%{_datadir}/%{name}/tools.zip"|' tools/g*.in

%build
%if %with qt
export MOC=%{_prefix}/lib/qt4/bin/moc
%endif
%configure2_5x --disable-Werror \
%if %with plugin
               --enable-plugin \
%else
               --disable-plugin \
%endif
%if %with qt
               --enable-qt-peer \
%else
               --disable-qt-peer \
%endif
               --enable-regen-headers \
               --disable-rpath \
               --with-vm=%{java} \
%if %with ecj
               --with-ecj \
%else
               --without-ecj \
%endif
%if %with gjdoc
               --with-gjdoc
%else
               --without-gjdoc
%endif

%__make

%install
%__rm -rf %{buildroot}
%makeinstall_std
%if %with plugin
(cd native/plugin && %{makeinstall_std})
%__rm %{buildroot}%{_libdir}/%{name}/libgcjwebplugin.la
%endif
%if 0
%__mkdir_p %{buildroot}%{_libdir}/mozilla/plugins
%__mv %{buildroot}%{_libdir}/%{name}/libgcjwebplugin.so %{buildroot}%{_libdir}/mozilla/plugins
%endif
# FIXME: Shared with libgcj
%__rm %{buildroot}%{_prefix}/lib/logging.properties
%__rm %{buildroot}%{_prefix}/lib/security/classpath.security

%if %with gjdoc
%__mkdir_p 755 %{buildroot}%{_javadocdir}
cp -a doc/api/html %{buildroot}%{_javadocdir}/%{name}-%{version}
touch %{buildroot}%{_javadocdir}/{%{name},java}
%endif

# FIXME: conflicts with gcj-tools
%__rm -f %{buildroot}%{_bindir}/gappletviewer
%__rm -f %{buildroot}%{_bindir}/gjar
%__rm -f %{buildroot}%{_bindir}/gjarsigner
%__rm -f %{buildroot}%{_bindir}/gjavah
%__rm -f %{buildroot}%{_bindir}/gkeytool
%__rm -f %{buildroot}%{_bindir}/gnative2ascii
%__rm -f %{buildroot}%{_bindir}/gorbd
%__rm -f %{buildroot}%{_bindir}/grmic
%__rm -f %{buildroot}%{_bindir}/grmid
%__rm -f %{buildroot}%{_bindir}/grmiregistry
%__rm -f %{buildroot}%{_bindir}/gserialver
%__rm -f %{buildroot}%{_bindir}/gtnameserv
%__rm -rf %{buildroot}%{_datadir}/%{name}/examples
%__rm -f %{buildroot}%{_mandir}/man1/gappletviewer.1*
%__rm -f %{buildroot}%{_mandir}/man1/gcjh.1*
%__rm -f %{buildroot}%{_mandir}/man1/gjar.1*
%__rm -f %{buildroot}%{_mandir}/man1/gjarsigner.1*
%__rm -f %{buildroot}%{_mandir}/man1/gjavah.1*
%__rm -f %{buildroot}%{_mandir}/man1/gkeytool.1*
%__rm -f %{buildroot}%{_mandir}/man1/gnative2ascii.1*
%__rm -f %{buildroot}%{_mandir}/man1/gorbd.1*
%__rm -f %{buildroot}%{_mandir}/man1/grmid.1*
%__rm -f %{buildroot}%{_mandir}/man1/grmiregistry.1*
%__rm -f %{buildroot}%{_mandir}/man1/gserialver.1*
%__rm -f %{buildroot}%{_mandir}/man1/gtnameserv.1*

%clean
%__rm -rf %{buildroot}

%if %with gjdoc
%post javadoc
%__rm -rf %{_javadocdir}/java
%__rm -f %{_javadocdir}/%{name}
%__ln_s %{name}-%{version} %{_javadocdir}/%{name}
%__ln_s %{name}-%{version} %{_javadocdir}/java
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS COPYING HACKING INSTALL LICENSE NEWS README THANKYOU TODO
%{_datadir}/%{name}
%{_infodir}/cp-hacking.info*
%{_infodir}/cp-tools.info*
%{_infodir}/cp-vmintegration.info*
%dir %{_libdir}/%{name}
%defattr(-,root,root)
%{_libdir}/%{name}/libgconfpeer.*
%{_libdir}/%{name}/libgjsmalsa.*
%{_libdir}/%{name}/libgjsmdssi.*
%{_libdir}/%{name}/libgtkpeer.*
%{_libdir}/%{name}/libjavaio.*
%{_libdir}/%{name}/libjavalang.*
%{_libdir}/%{name}/libjavalangmanagement.*
%{_libdir}/%{name}/libjavalangreflect.*
%{_libdir}/%{name}/libjavanet.*
%{_libdir}/%{name}/libjavanio.*
%{_libdir}/%{name}/libjavautil.*
%{_libdir}/%{name}/libjawt.*

%files devel
%defattr(0644,root,root,0755)
%doc ChangeLog*
%{_includedir}/*.h

%if %with gjdoc
%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
%ghost %doc %{_javadocdir}/java
%endif

%if %with qt
%files qt
%{_libdir}/%{name}/libqtpeer.*
%endif

%if %with plugin
%files -n mozilla-plugin-gcjwebplugin
%{_libdir}/classpath/libgcjwebplugin.so
%endif


%changelog
* Sat Jun 02 2012 Andrey Bondrov <abondrov@mandriva.org> 0:0.97.2-7
+ Revision: 802014
- Update BuildRequires
- Drop some legacy junk

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix %%exclude abuse

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0:0.97.2-5mdv2010.0
+ Revision: 437054
- rebuild

* Sun Mar 01 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0:0.97.2-4mdv2009.1
+ Revision: 346289
- rebuild for missing binaries

* Sat Aug 09 2008 David Walluck <walluck@mandriva.org> 0:0.97.2-3mdv2009.0
+ Revision: 270005
- make plugin optional
- conditionalize ecj
- don't Requires: jamvm
- BuildRequires: magic-devel
- sync sources
- 0.97.2

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Tue Apr 15 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.97.1-1mdv2009.0
+ Revision: 193740
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.96.1-2mdv2008.1
+ Revision: 120850
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Tue Oct 16 2007 David Walluck <walluck@mandriva.org> 0:0.96.1-1mdv2008.1
+ Revision: 99254
- 0.96.1

* Tue Oct 16 2007 David Walluck <walluck@mandriva.org> 0:0.96-1mdv2008.1
+ Revision: 98885
- 0.96

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 0:0.95-3mdv2008.0
+ Revision: 70154
- kill file require on info-install

* Wed Apr 25 2007 David Walluck <walluck@mandriva.org> 0:0.95-2mdv2008.0
+ Revision: 18116
- fix bug #30439

* Tue Apr 24 2007 David Walluck <walluck@mandriva.org> 0:0.95-1mdv2008.0
+ Revision: 17725
- 0.95


* Sat Mar 10 2007 Anssi Hannula <anssi@mandriva.org> 0.93-3mdv2007.1
+ Revision: 140785
- patch2: fix build with recent firefox (from upstream)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - bump release
    - move huge (5Mb!) ChangeLog in devel package

* Sat Dec 09 2006 David Walluck <walluck@mandriva.org> 0:0.93-1mdv2007.1
+ Revision: 93930
- 0.93

* Sat Nov 11 2006 David Walluck <walluck@mandriva.org> 0:0.93-0.20061109.1mdv2007.1
+ Revision: 81410
- 20061109

* Fri Oct 27 2006 David Walluck <walluck@mandriva.org> 0:0.93-0.20061026.1mdv2007.1
+ Revision: 72947
- update

* Tue Oct 24 2006 David Walluck <walluck@mandriva.org> 0:0.93-0.20061019.2mdv2007.0
+ Revision: 71984
- exclude %%{_bindir}/grmiregistry
- bump release
- /usr/bin/grmiregistry conflicts with gcj-tools
- 0.93-pre
- Import classpath

* Tue Aug 15 2006 David Walluck <walluck@mandriva.org> 0:0.92-3mdv2007.0
- BuildRequires: libjack-devel

* Sun Aug 13 2006 David Walluck <walluck@mandriva.org> 0:0.92-2mdv2007.0
- don't require java-devel
- plugin requires mozilla-firefox
- use jamvm as default vm
- drop mozilla-firefox workaround
- drop securitydir workaround
- drop double workaround
- add glibj.zip to classpath of each tool

* Fri Aug 11 2006 David Walluck <walluck@mandriva.org> 0:0.92-1mdv2007.0
- 0.92-generics
- disable javadoc because gjdoc has no generics support

* Thu Aug 10 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060803.2mdv2007.0
- BuildRequires: libxtst-devel

* Mon Jul 31 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060803.1mdv2007.0
- 0.93-pre (20060803)
- BuildRequires: libGConf2-devel

* Mon Jun 19 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060618.1mdv2007.0
- 0.92-pre (20060618)
- use java-functions to set jvm binary for tools
- make qt optional and turn it off until qt4-devel installs

* Tue Jun 06 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060605.2mdv2007.0
- use less configure options
- fix devel package permissions
- add mozilla-plugin-gcjwebplugin package

* Tue Jun 06 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060605.1mdv2007.0
- 0.92-pre (20060605)
- split the qt peer into its own package
- fix library permissions
- remove rebuild-security-providers requirement
- don't (un)install infopages as they are broken
- remove unused %%check

* Thu Jun 01 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060601.1mdv20072007.0
- 0.92-pre (20060601)
- rebuild to remove libgcj6-base dependency

* Sat May 13 2006 David Walluck <walluck@mandriva.org> 0:0.92-0.20060512.1mdk
- 0.92-pre (20060512)

* Sun May 07 2006 Giuseppe Ghib� <ghibo@mandriva.com> 0:0.91-0.20060426.2mdk
- Don't call %%{_bindir}/rebuild-security-providers if doesn't exists. Breaks
  uninstalling.

* Thu Apr 27 2006 David Walluck <walluck@mandriva.org> 0:0.91-0.20060426.1mdk
- 0.91-pre (20060426)
- apply some small fixes
- fix jarsigner script

* Sun Apr 23 2006 David Walluck <walluck@mandriva.org> 0:0.91-0.20060424.1mdk
-  0.91-pre (20060424)

* Wed Apr 19 2006 David Walluck <walluck@mandriva.org> 0:0.91-0.20060417.1mdk
- 0.91-pre (20060417)
- install gjarsigner script

* Fri Apr 14 2006 David Walluck <walluck@mandriva.org> 0:0.91-0.20060413.1mdk
- 0.91-pre (20060413)

* Wed Apr 12 2006 David Walluck <walluck@mandriva.org> 0:0.91-0.20060411.1mdk
- 0.91-pre (20060411)

* Wed Apr 12 2006 David Walluck <walluck@mandriva.org> 0:0.90-1mdk
- 0.90

* Wed Feb 01 2006 David Walluck <walluck@mandriva.org> 0:0.21-0.20060204.1mdk
- 0.21-pre (20060204)

* Wed Jan 25 2006 David Walluck <walluck@mandriva.org> 0:0.20-4mdk
- add autotools BuildRequires
- use %%configure2_5x

* Wed Jan 18 2006 David Walluck <walluck@mandriva.org> 0:0.20-3mdk
- BuildRequires gtk 2.0, not gtk

* Sat Jan 14 2006 David Walluck <walluck@mandriva.org> 0:0.20-2mdk
- fix file conflicts

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:0.20-1mdk
- 0.20
- rename hacking.info to %%{name}-hacking.info

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:0.19-0.0.5mdk
- fix gtk BuildRequires

* Sat Dec 03 2005 David Walluck <walluck@mandriva.org> 0:0.19-0.0.4mdk
- really fix build on x86_64

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:0.19-0.0.3mdk
- fix build on x86_64

* Fri Nov 04 2005 David Walluck <walluck@mandriva.org> 0:0.19-0.0.2mdk
- fix location of classpath.security, but remove it as it is already
  in libgcj6-base

* Fri Nov 04 2005 David Walluck <walluck@mandriva.org> 0.19-0.0.1mdk
- 0.19

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:0.18-0.0.3mdk
- BuildRequires: gtk+-devel (neoclust)

* Tue Nov 01 2005 David Walluck <walluck@mandriva.org> 0:0.18-0.0.2mdk
- workaround (but don't fix) difference in classpath.security location

* Sat Oct 29 2005 David Walluck <walluck@mandriva.org> 0:0.18-0.0.1mdk
- 0.18

* Thu Aug 18 2005 David Walluck <walluck@mandriva.org> 0:0.17-1.1mdk
- release

* Wed Aug 03 2005 Ville Skyttä <scop at jpackage.org> - 0:0.17-1jpp
- 0.17.

* Thu Jun 30 2005 Ville Skyttä <scop at jpackage.org> - 0:0.15-1jpp
- First build (javadocs only)

