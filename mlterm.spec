%define name mlterm
%define version 3.0.5
%define release 1
%define prefix /usr
%define bindir /usr/bin
%define libdir /usr/lib
%define mandir /usr/share/man
%define datadir /usr/share
%define sysconfdir /etc
%define libexecdir /usr/libexec/mlterm
%define pixmapdir  /usr/share/pixmaps

Summary:     Multi Lingual TERMinal emulator on X
Name:	     %{name}
Version:     %{version}
Release:     %{release}
License:     Modified BSD-style license
Group:	     User Interface/X
URL:         http://mlterm.sourceforge.net/
Source0:     http://prdownloads.sourceforge.net/mlterm/mlterm-%{version}.tar.gz
Packager:    The mlterm team
Requires:    gtk+
BuildRoot:   /var/tmp/%{name}-%{version}-root
BuildPreReq: gtk+-devel

%description
mlterm is a multi-lingual terminal emulator written from
scratch, which supports various character sets and encodings
in the world.  It also supports various unique feature such as
anti-alias using FreeType, multiple windows, scrollbar API,
scroll by mouse wheel, automatic selection of encoding,
and so on. Multiple xims are also supported. 
You can dynamically change various xims.

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=%{prefix} \
	    --bindir=%{bindir} \
	    --libdir=%{libdir} \
	    --mandir=%{mandir} \
	    --libexecdir=%{libexecdir} \
	    --datadir=%{datadir} \
	    --sysconfdir=%{sysconfdir} \
	    # --with-imagelib=gdk-pixbuf \
	    # --enable-anti-alias
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{pixmapdir}
install -m 644 $RPM_BUILD_DIR/%{name}-%{version}/doc/icon/mlterm* \
               $RPM_BUILD_ROOT%{pixmapdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog LICENCE README doc/{en,ja}
%{bindir}/mlterm
%{bindir}/mlclient
%{bindir}/mlclientx
%{bindir}/mlcc
%{libdir}/libkik.*
%{libdir}/libmkf.*
%{libdir}/mkf/
%{libdir}/mlterm/
%{libexecdir}/
%{sysconfdir}/mlterm/
%{mandir}/man1/mlterm.1*
%{mandir}/man1/mlclient.1*
%{pixmapdir}/mlterm*
%{datadir}/locale/*/LC_MESSAGES/mlconfig.mo

%changelog
* Sat Jun 04 2011 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.5

* Sat May 29 2011 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.4

* Sun Mar 20 2011 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.3

* Sun Jan 02 2011 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.2
 
* Mon Jun 07 2010 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.1

* Sat Apr 10 2010 Araki Ken <arakiken@users.sf.net>
- Source version 3.0.0

* Fri Nov 30 2007 Seiichi SATO <me@seiichisato.jp>
- Source version 2.9.4

* Sun May 07 2006 Seiichi SATO <me@seiichisato.jp>
- Source version 2.9.3

* Sat Mar 04 2005 Seiichi SATO <ssato@sh.rim.or.jp>
- Source version 2.9.2

* Sun Nov 28 2004 Seiichi SATO <ssato@sh.rim.or.jp>
- Source version 2.9.1

* Thu Nov 25 2004 Seiichi SATO <ssato@sh.rim.or.jp>
- Fixed #1072304
- FHS compliance

* Sun Oct 24 2004 Seiichi SATO <ssato@sh.rim.or.jp>
- Source version 2.9.0

* Sun Oct 05 2003 Araki Ken <arakiken@users.sf.net>
- Source version 2.8.0

* Sat Jun 14 2003 Araki Ken <arakiken@users.sf.net>
- Source version 2.7.0

* Sun Jan 12 2003 Araki Ken <arakiken@users.sf.net>
- Source version 2.6.3

* Thu Oct 1 2002 Araki Ken <arakiken@users.sf.net>
- Source version 2.6.2

* Thu Sep 12 2002 Araki Ken <arakiken@users.sf.net>
- Source version 2.6.1

* Sat Sep 7 2002 Araki Ken <arakiken@users.sf.net>
- Source version 2.6.0

* Sun Jun 16 2002 Araki Ken <arakiken@users.sourceforge.net>
- Source version 2.5.0

* Sun Apr 14 2002 Araki Ken <arakiken@users.sourceforge.net>
- Source version 2.4.0

* Mon Feb 25 2002 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.3.1

* Sat Feb 23 2002 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.3.0

* Tue Jan 29 2002 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.2.0

* Wed Jan 2 2002 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.1.2

* Sun Dec 30 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.1.1

* Sat Dec 29 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.1.0

* Thu Nov 29 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 2.0.0

* Mon Nov 26 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.47

* Sat Nov 24 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.46

* Fri Nov 23 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.45

* Sat Nov 17 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.44

* Wed Nov 14 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.43

* Tue Nov 13 2001 Araki Ken <j00v0113@ip.media.kyoto-u.ac.jp>
- Source version 1.9.42pl6
