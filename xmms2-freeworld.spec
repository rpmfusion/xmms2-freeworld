%define codename DrO_o

Name:			xmms2-freeworld
Summary:		Plugins for XMMS2 that cannot be included in Fedora
Version:		0.8
Release:		25%{?dist}
License:		LGPLv2+ and GPL+ and BSD
URL:			http://wiki.xmms2.xmms.se/
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		http://downloads.sourceforge.net/xmms2/xmms2-%{version}%{codename}.tar.bz2
# Use libdir properly for Fedora multilib
Patch0:			xmms2-0.8DrO_o-use-libdir.patch
# Don't add extra CFLAGS, we're smart enough, thanks.
Patch1:			xmms2-0.8DrO_o-no-O0.patch
# Fix compilation against newer ffmpeg (patches from debian)
Patch2:                 bp-fix-avcodec-init.patch
Patch3:                 bp-fix-alloc-context.patch
Patch4:                 bp-fix-missing-include.patch
Patch5:                 libav10.patch

BuildRequires:		gcc
BuildRequires:		sqlite-devel
BuildRequires:		glib2-devel
BuildRequires:		python2-devel
# RPMFusion only BuildRequires
BuildRequires:		faad2-devel, libmad-devel, ffmpeg-devel, libmms-devel

Requires:		xmms2-avcodec = %{version}-%{release}
Requires:		xmms2-faad = %{version}-%{release}
Requires:		xmms2-mad = %{version}-%{release}
Requires:		xmms2-mms = %{version}-%{release}
Requires:		xmms2-mp4 = %{version}-%{release}


%description
XMMS2 is an audio framework, but it is not a general multimedia player - it 
will not play videos. It has a modular framework and plugin architecture for 
audio processing, visualisation and output, but this framework has not been 
designed to support video. Also the client-server design of XMMS2 (and the 
daemon being independent of any graphics output) practically prevents direct 
video output being implemented. It has support for a wide range of audio 
formats, which is expandable via plugins. It includes a basic CLI interface 
to the XMMS2 framework, but most users will want to install a graphical XMMS2 
client (such as gxmms2 or esperanza).

%package -n xmms2-avcodec
Summary:	XMMS2 Plugin for avcodec supported formats
License:	LGPLv2+
Requires:	xmms2 = %{version}

%description -n xmms2-avcodec
An XMMS2 Plugin which provides support for audio formats provided by
FFMPEG's libavcodec.


%package -n xmms2-faad
Summary:	XMMS2 Plugin for AAC and MP4 audio formats
License:	GPLv2+
Requires:	xmms2 = %{version}

%description -n xmms2-faad
An XMMS2 Plugin which provides support for audio formats provided by FAAD 
(AAC and MP4).

%package -n xmms2-mad
Summary:	XMMS2 Plugin for MPEG Audio files
License:	GPLv2+
Requires:	xmms2 = %{version}

%description -n xmms2-mad
An XMMS2 Plugin for listening to MPEG files (MPEG 1 & 2 layers I, II and III 
- includes MP3).

%package -n xmms2-mms
Summary:	XMMS2 Plugin for MMS audio streams
License:	LGPLv2+
Requires:	xmms2 = %{version}

%description -n xmms2-mms
An XMMS2 Plugin for listening to Microsoft Media Services (MMS) audio streams.

%package -n xmms2-mp4
Summary:	XMMS2 Plugin for MP4 audio
License:	GPLv2+
Requires:	xmms2 = %{version}

%description -n xmms2-mp4
An XMMS2 Plugin for listening to MP4 audio files.

%prep
%setup -q -n xmms2-%{version}%{codename}

%patch0 -p1 -b .plugins-use-libdir
%patch1 -p1 -b .noO0
%patch2 -p1
%patch3 -p1 
%patch4 -p1
%patch5 -p1

for i in doc/tutorial/python/tut1.py doc/tutorial/python/tut2.py doc/tutorial/python/tut3.py doc/tutorial/python/tut4.py doc/tutorial/python/tut5.py doc/tutorial/python/tut6.py utils/gen-tree-hashes.py utils/gen-wiki-release-bugs.py utils/gen-tarball.py utils/gen-wiki-release-authors.py waf waftools/podselect.py waftools/genipc.py waftools/genipc_server.py waftools/cython.py; do
	sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python2|g' $i
done


%build
export CFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
		--libdir=%{_libdir} \
		--with-pkgconfigdir=%{_libdir}/pkgconfig \
		--without-optionals=et \
		--without-optionals=launcher \
		--without-optionals=medialib-updater \
		--without-optionals=nycli \
		--without-optionals=perl \
		--without-optionals=pixmaps \
		--without-optionals=python \
		--without-optionals=ruby \
		--without-optionals=vistest \
		--without-optionals=xmmsclient-ecore \
		--without-optionals=xmmsclient++ \
		--without-optionals=xmmsclient++-glib \
		--without-plugins=airplay \
		--without-plugins=alsa \
		--without-plugins=ao \
		--without-plugins=apefile \
		--without-plugins=asf \
		--without-plugins=asx \
		--without-plugins=cdda \
		--without-plugins=cue \
		--without-plugins=curl \
		--without-plugins=daap \
		--without-plugins=diskwrite \
		--without-plugins=equalizer \
		--without-plugins=curl \
		--without-plugins=file \
		--without-plugins=flac \
		--without-plugins=flv \
		--without-plugins=gme \
		--without-plugins=gvfs \
		--without-plugins=html \
		--without-plugins=ices \
		--without-plugins=icymetaint \
		--without-plugins=id3v2 \
		--without-plugins=jack \
		--without-plugins=karaoke \
		--without-plugins=m3u \
		--without-plugins=modplug \
		--without-plugins=mpg123 \
		--without-plugins=musepack \
		--without-plugins=normalize \
		--without-plugins=null \
		--without-plugins=nulstripper \
		--without-plugins=ofa \
		--without-plugins=oss \
		--without-plugins=pls \
		--without-plugins=pulse \
		--without-plugins=replaygain \
		--without-plugins=rss \
		--without-plugins=samba \
		--without-plugins=sndfile \
		--without-plugins=speex \
		--without-plugins=tta \
		--without-plugins=vocoder \
		--without-plugins=vorbis \
		--without-plugins=wave \
		--without-plugins=wavpack \
		--without-plugins=xml \
		--without-plugins=xspf 

./waf build -v %{?_smp_mflags}

%install
./waf install --destdir=%{buildroot} --prefix=%{_prefix} --libdir=%{_libdir} --with-pkgconfigdir=%{_libdir}/pkgconfig

# There are lots of things that get built that we don't need to package, because they're in the Fedora xmms2 package.
rm -rf %{buildroot}%{_bindir} %{buildroot}%{_libdir}/libxmmsclient* %{buildroot}%{_mandir} %{buildroot}%{_datadir} %{buildroot}%{_includedir} %{buildroot}%{_libdir}/pkgconfig 

# exec flags for debuginfo
chmod +x %{buildroot}%{_libdir}/xmms2/*

%files
%doc COPYING COPYING.GPL COPYING.LGPL

%files -n xmms2-avcodec
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_avcodec.so

%files -n xmms2-faad
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_faad.so

%files -n xmms2-mad
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_mad.so

%files -n xmms2-mms
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_mms.so

%files -n xmms2-mp4
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_mp4.so

%changelog
* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
- Spec file clean up

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.8-24
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8-22
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.8-20
- Rebuilt for ffmpeg-3.5 git

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.8-18
- Rebuild for ffmpeg update

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.8-16
- Rebuilt for ffmpeg-3.1.1

* Wed Jul 06 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.8-15
- Patch for newer ffmpeg

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.8-14
- Rebuilt for FFmpeg 2.4.3

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.8-13
- Rebuilt for ffmpeg-2.3

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 0.8-12
- Rebuilt for ffmpeg-2.2

* Mon Dec 09 2013 Leigh Scott <leigh123linux@googlemail.com> - 0.8-11
- fix ffmpeg compile error

* Sun Dec 08 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-10
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-9
- Rebuilt for FFmpeg 2.0.x

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-8
- Rebuilt for x264/FFmpeg

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-7
- Rebuilt for ffmpeg

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-6
- Rebuilt for FFmpeg 1.0

* Thu Nov 01 2012 John Doe <anonymous@american.us> 0.8-5
- Patch for new ffmpeg

* Thu Nov 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-4
- Rebuilt for ffmpeg

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-3
- Rebuilt for FFmpeg

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-2
- Rebuilt for F-17

* Mon Dec 05 2011 John Doe <anonymous@american.us> 0.8-1
- Update to 0.8

* Wed Oct 05 2011 John Doe <anonymous@american.us> 0.7-3
- Patch for new ffmpeg thanks to rathann!

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7-2
- Rebuilt for FFmpeg-0.8

* Thu Jul 01 2010 John Doe <anonymous@american.us> 0.7-1
- Update to 0.7

* Wed Aug 12 2009 John Doe <anonymous@american.us> 0.6-1
- Update to 0.6

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5-6
- rebuild for new F11 features

* Mon Dec 16 2008 John Doe <anonymous@american.us> 0.5-5
- Fix typo in the SPEC file

* Mon Dec 15 2008 John Doe <anonymous@american.us> 0.5-4
- Disable building of everything possible that do not go to the freeworld plugins
- Add bits for mac plugin, but keep it disabled until mac becomes free

* Fri Dec 12 2008 John Doe <anonymous@american.us> 0.5-3
- Add meta package
- Include more upstream patches for avcodec plugin compilation and fixes
- Drop BR's and patches that are irrelevant for compiling freeworld plugins

* Wed Dec 10 2008 John Doe <anonymous@american.us> 0.5-2
- Do the same cleanups as is done to the main package,
  see rh-bz #474908

* Fri Dec 05 2008 John Doe <anonymous@american.us> 0.5-1
- Initial package for RPMFusion
