%bcond_without  qt
%bcond_with     gjdoc
%bcond_without  info

%define javaver 1.5.0
%define libname %mklibname %{name}

Name:           classpath
Version:        0.95
Release:        %mkrel 2
Epoch:          0
Summary:        GNU Classpath, Essential Libraries for Java
Group:          Development/Java
#Vendor:        JPackage Project
#Distribution:  JPackage
License:        GPL-like
URL:            http://www.classpath.org/
Source0:        ftp://ftp.gnu.org/pub/gnu/classpath/classpath-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/pub/gnu/classpath/classpath-%{version}.tar.gz.sig
Patch0:         classpath-with-jay.patch
Patch1:         classpath-enable-examples.patch
%if %with info
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%endif
Requires:       jamvm
BuildRequires:  atk-devel
BuildRequires:  autoconf2.5
BuildRequires:  automake1.8
BuildRequires:  cairo-devel
BuildRequires:  dssi-devel
BuildRequires:  eclipse-ecj
BuildRequires:  freetype2-devel
BuildRequires:  gcc-java
BuildRequires:  gcj-tools
%if %with gjdoc
# Need to use gjdoc because of the -licensetext option
BuildRequires:  gjdoc
%else
Obsoletes:      classpath-javadoc
%endif
BuildRequires:  jpackage-utils
BuildRequires:  libalsa-devel
BuildRequires:  libGConf2-devel
BuildRequires:  libgdk_pixbuf2.0-devel
BuildRequires:  libgtk+2.0-devel
BuildRequires:  libglib2.0-devel
BuildRequires:  libjack-devel
BuildRequires:  libpango-devel
#BuildRequires: libxml2-devel
#BuildRequires: libxslt-devel
BuildRequires:  libxtst-devel
BuildRequires:  mozilla-firefox-devel
BuildRequires:  pkgconfig
%if %with qt
BuildRequires:  qt4-devel >= 0:4.1.0
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
GNU Classpath, Essential Libraries for Java, is a GNU project to
create free core class libraries for use with virtual machines and
compilers for the java programming language.

%package        devel
Summary:        Devlopment headers and examples for GNU Classpath
Group:          Development/Java
Requires:       classpath = %{epoch}:%{version}-%{release}

%description    devel
%{summary}.

%if %with gjdoc
%package        javadoc
Summary:        API documentation for GNU Classpath
Group:          Development/Java
Provides:       java-javadoc = 0:%{javaver}
Provides:       java-%{javaver}-javadoc = 0:%{javaver}

%description    javadoc
%{summary}.
%endif

%if %with qt
%package        qt
Summary:        QT4 peer for GNU Classpath
Group:          Development/Java

%description    qt
%{summary}.
%endif

%package -n     mozilla-plugin-gcjwebplugin
Summary:        A plugin to execute Java (tm) applets in Mozilla and compatible browsers
Group:          Development/Java
Requires:       mozilla-firefox
Provides:       mozilla-plugin-gcj = %{epoch}:%{version}-%{release}
Provides:       gcjwebplugin = %{epoch}:%{version}-%{release}
Provides:       java-plugin = %{epoch}:%{javaver}
Provides:       java-%{javaver}-plugin = %{epoch}:%{version}
Requires:       classpath = %{epoch}:%{version}-%{release}

%description -n mozilla-plugin-gcjwebplugin
gcjwebplugin is a plugin to execute Java (tm) applets in Mozilla and
compatible browsers. It uses the JVM provided by GCJ and adds a
SecurityManager suitable for applets.

WARNING: The current version does not provide a security manager capable
of handling Java (tm) applets. Applets have UNRESTRICTED access to your
computer. This means they can do anything you can do, like deleting all
your important data.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%ifarch x86_64
%endif
%{__perl} -pi -e 's|^tools_cp=.*|tools_cp="%{_datadir}/%{name}/glibj.zip:%{_datadir}/%{name}/tools.zip"|' tools/g*.in

%build
%if %with qt
export MOC=%{_prefix}/lib/qt4/bin/moc
%endif
%configure2_5x --disable-Werror \
               --enable-plugin \
%if %with qt
               --enable-qt-peer \
%else
               --disable-qt-peer \
%endif
               --enable-regen-headers \
               --disable-rpath \
               --with-vm=%{_bindir}/jamvm \
               --with-ecj \
%if %with gjdoc
               --with-gjdoc
%else
               --without-gjdoc
%endif
%{__make}

%install
%{__rm} -rf %{buildroot}
%makeinstall
(cd native/plugin && %makeinstall)
%if 0
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/plugins
%{__mv} %{buildroot}%{_libdir}/%{name}/libgcjwebplugin.so %{buildroot}%{_libdir}/mozilla/plugins
%endif
%{__rm} %{buildroot}%{_libdir}/%{name}/libgcjwebplugin.la
# XXX: Shared with libgcj
%{__rm} %{buildroot}%{_prefix}/lib/logging.properties
%{__rm} %{buildroot}%{_prefix}/lib/security/classpath.security

%if %with gjdoc
%{__mkdir_p} 755 %{buildroot}%{_javadocdir}
%{__cp} -a doc/api/html %{buildroot}%{_javadocdir}/%{name}-%{version}
touch %{buildroot}%{_javadocdir}/{%{name},java}
%endif

%clean
%{__rm} -rf %{buildroot}

%if %with info
%post
%_install_info cp-hacking.info
%_install_info cp-tools.info
%_install_info cp-vmintegration.info

%preun
%_remove_install_info cp-hacking.info
%_remove_install_info cp-tools.info
%_remove_install_info cp-vmintegration.info
%endif

%if %with gjdoc
%post javadoc
%{__rm} -rf %{_javadocdir}/java
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/java
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS COPYING HACKING INSTALL LICENSE NEWS README THANKYOU TODO
%exclude %{_datadir}/%{name}/examples
%attr(0755,root,root) %{_bindir}/gappletviewer
%attr(0755,root,root) %{_bindir}/gjar
%attr(0755,root,root) %{_bindir}/gjarsigner
%attr(0755,root,root) %{_bindir}/gjavah
%attr(0755,root,root) %{_bindir}/gkeytool
%attr(0755,root,root) %{_bindir}/gnative2ascii
%attr(0755,root,root) %{_bindir}/gorbd
# FIXME: conflicts with gcj-tools
%exclude %attr(0755,root,root) %{_bindir}/grmic
%attr(0755,root,root) %{_bindir}/grmid
%exclude %attr(0755,root,root) %{_bindir}/grmiregistry
%attr(0755,root,root) %{_bindir}/gserialver
%attr(0755,root,root) %{_bindir}/gtnameserv
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
#%{_libdir}/%{name}/libxmlj.*
%{_mandir}/man1/gappletviewer.1*
%exclude %{_mandir}/man1/gcjh.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%exclude %{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*

%files devel
%defattr(0644,root,root,0755)
%doc ChangeLog* 
%{_includedir}/*.h
%{_datadir}/%{name}/examples

%if %with gjdoc
%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
%ghost %doc %{_javadocdir}/java
%endif

%if %with qt
%files qt
%defattr(-,root,root)
%{_libdir}/%{name}/libqtpeer.*
%endif

%files -n mozilla-plugin-gcjwebplugin
%defattr(-,root,root)
%if 0
%{_libdir}/mozilla/plugins
%endif
%{_libdir}/classpath/libgcjwebplugin.so


