%bcond_with ecj
%bcond_without qt
%bcond_with gjdoc
%bcond_with plugin

%define javaver 1.5.0
%define libname %mklibname %{name}

Name:		classpath
Version:	0.99
Release:	1
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
BuildRequires:	gcc-java
BuildRequires:	gcj-tools
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel
BuildRequires:	antlr
%if %with ecj
BuildRequires:	eclipse-ecj
%endif
%if %with gjdoc
# Need to use gjdoc because of the -licensetext option
BuildRequires:	gjdoc
%else
Obsoletes:		classpath-javadoc
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
perl -pi -e 's|^tools_cp=.*|tools_cp="%{_datadir}/%{name}/glibj.zip:%{_datadir}/%{name}/tools.zip"|' tools/g*.in

# freetype2 fix Sflo
perl -pi -e "s|<freetype/|<freetype2/|" native/jni/gtk-peer/gnu_java_awt_peer_gtk_FreetypeGlyphVector.c
perl -pi -e "s|<freetype/|<freetype2/|" native/jni/gtk-peer/gnu_java_awt_peer_gtk_GdkFontPeer.c
#

%build
%if %with qt
export MOC=%{_prefix}/lib/qt4/bin/moc
%endif

%configure \
		--disable-Werror \
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

%make

%install
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
%if %with gjdoc
%{_libdir}/%{name}/libgjsmdssi.*
%endif
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

