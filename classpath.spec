%define javaver 1.5.0

Name:		classpath
Version:	0.93
Release:	1
Summary:	An old implementation of the Java standard class library
Group:		Development/Java
License:	GPL-like
URL:		http://www.classpath.org/
Source0:	ftp://ftp.gnu.org/gnu/classpath/classpath-%{version}.tar.gz
Source1:	classpath.rpmlintrc
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
#BuildRequires:	pkgconfig(dssi)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	magic-devel
BuildRequires:	jikes
BuildRequires:	jamvm
BuildRequires:	fastjar

%description
GNU Classpath was a project to create a free reimplementation of the Java
standard class library before OpenJDK was released under an acceptable
license.

These days, it is obsoleted by OpenJDK - but it is still useful for
bootstrapping OpenJDK (which usually requires itself to build).

%package devel
Summary:	Devlopment headers and examples for GNU Classpath
Group:		Development/Java
Requires:	classpath = %{EVRD}

%description devel
%{summary}.

%prep
%autosetup -p1
%configure \
	--with-jikes=%{_bindir}/jikes \
	--with-fastjar=%{_bindir}/fastjar \
	--with-vm=%{_bindir}/jamvm \
	--disable-Werror \
	--disable-gtk-peer \
	--disable-gconf-peer \
	--enable-default-preferences-peer=file \
	--disable-plugin

%build
# Not SMP safe
make

%install
%make_install

%files
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS COPYING HACKING INSTALL LICENSE NEWS README THANKYOU TODO
%{_bindir}/gappletviewer
%{_bindir}/gjar
%{_bindir}/gjarsigner
%{_bindir}/gkeytool
%{_bindir}/gnative2ascii
%{_bindir}/gorbd
%{_bindir}/grmid
%{_bindir}/grmiregistry
%{_bindir}/gserialver
%{_bindir}/gtnameserv
%{_prefix}/lib/logging.properties
%{_prefix}/lib/security/classpath.security
%{_infodir}/hacking.info*
%{_infodir}/tools.info*
%{_infodir}/vmintegration.info*
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%defattr(-,root,root)
%{_libdir}/%{name}/libgjsmalsa.*
%if %{with gjdoc}
%{_libdir}/%{name}/libgjsmdssi.*
%endif
%{_libdir}/%{name}/libjavaio.*
%{_libdir}/%{name}/libjavalang.*
%{_libdir}/%{name}/libjavalangreflect.*
%{_libdir}/%{name}/libjavanet.*
%{_libdir}/%{name}/libjavanio.*
%{_libdir}/%{name}/libjavautil.*

%files devel
%defattr(0644,root,root,0755)
%doc ChangeLog*
%{_includedir}/*.h
