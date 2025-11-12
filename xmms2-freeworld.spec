Name:			xmms2-freeworld
Summary:		Plugins for XMMS2 that cannot be included in Fedora
Version:		0.9.5
Release:		3%{?dist}
License:		LGPL-2.1-or-later AND GPL-2.0-or-later AND BSD-3-Clause
URL:			http://wiki.xmms2.xmms.se/
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		https://github.com/xmms2/xmms2-devel/releases/download/%{version}/xmms2-%{version}.tar.xz
Patch0:         ffmpeg-8.patch

BuildRequires:		gcc-c++
BuildRequires:		sqlite-devel
BuildRequires:		glib2-devel
BuildRequires:		python3
# RPMFusion only BuildRequires
BuildRequires:		faad2-devel
BuildRequires:		ffmpeg-devel

Requires:		xmms2-avcodec%{?_isa} = %{version}-%{release}
Requires:		xmms2-faad%{?_isa} = %{version}-%{release}
Requires:		xmms2-mp4%{?_isa} = %{version}-%{release}


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
Requires:	xmms2%{?_isa} = %{version}

%description -n xmms2-avcodec
An XMMS2 Plugin which provides support for audio formats provided by
FFMPEG's libavcodec.


%package -n xmms2-faad
Summary:	XMMS2 Plugin for AAC and MP4 audio formats
License:	GPLv2+
Requires:	xmms2%{?_isa} = %{version}

%description -n xmms2-faad
An XMMS2 Plugin which provides support for audio formats provided by FAAD
(AAC and MP4).

%package -n xmms2-mp4
Summary:	XMMS2 Plugin for MP4 audio
License:	GPLv2+
Requires:	xmms2%{?_isa} = %{version}

%description -n xmms2-mp4
An XMMS2 Plugin for listening to MP4 audio files.

%prep
%autosetup -p1 -n xmms2-%{version}

for i in doc/tutorial/python/tut1.py doc/tutorial/python/tut2.py doc/tutorial/python/tut3.py doc/tutorial/python/tut4.py doc/tutorial/python/tut5.py doc/tutorial/python/tut6.py utils/gen-tree-hashes.py utils/gen-wiki-release-bugs.py utils/gen-tarball.py utils/gen-wiki-release-authors.py waf waftools/podselect.py waftools/genipc.py waftools/genipc_server.py waftools/cython.py; do
	sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' $i
done


%build
export CFLAGS="%{optflags}"
export CPPFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
 --libdir=%{_libdir} \
 --without-optionals="launcher,xmmsclient++,xmmsclient++-glib,perl,ruby,nycli,pixmaps,et,mdns, \
 medialib-updater,migrate-collections,vistest,sqlite2s4" \
 --without-plugins="airplay,alsa,ao,apefile,asf,asx,cdda,cue,curl,daap,diskwrite,equalizer,curl,file,flac, \
 flv,gme,gvfs,html,ices,icymetaint,id3v2,jack,karaoke,mad,m3u,mid1,midsquash,mms,modplug,mpg123,musepack,normalize, \
 null,nulstripper,ofa,oss,pls,pulse,replaygain,rss,samba,sndfile,speex,tta,vocoder,vorbis,wave,wavpack,xml,xspf"

./waf build -v %{?_smp_mflags}

%install
./waf install --destdir=%{buildroot} --prefix=%{_prefix} --libdir=%{_libdir} --with-pkgconfigdir=%{_libdir}/pkgconfig

# There are lots of things that get built that we don't need to package, because they're in the Fedora xmms2 package.
rm -rf %{buildroot}%{_bindir} %{buildroot}%{_libdir}/libxmmsclient* %{buildroot}%{_mandir} %{buildroot}%{_datadir} %{buildroot}%{_includedir} %{buildroot}%{_libdir}/pkgconfig

# exec flags for debuginfo
chmod +x %{buildroot}%{_libdir}/xmms2/*

%files
%license COPYING COPYING.GPL COPYING.LGPL

%files -n xmms2-avcodec
%license COPYING.LGPL
%{_libdir}/xmms2/libxmms_avcodec.so

%files -n xmms2-faad
%license COPYING.GPL
%{_libdir}/xmms2/libxmms_faad.so

%files -n xmms2-mp4
%license COPYING.GPL
%{_libdir}/xmms2/libxmms_mp4.so

%changelog
* Wed Nov 05 2025 Leigh Scott <leigh123linux@gmail.com> - 0.9.5-3
- Rebuild for ffmpeg-8.0

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 20 2025 Leigh Scott <leigh123linux@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Sat Feb 01 2025 Leigh Scott <leigh123linux@gmail.com> - 0.9.4-1
- Update to 0.9.4

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 19 2023 Leigh Scott <leigh123linux@gmail.com> - 0.9.3-2
- Drop mms plugin, fedora xmms2 provides it

* Sat Nov 18 2023 Leigh Scott <leigh123linux@gmail.com> - 0.9.3-1
- update to 0.9.3

* Wed Nov 08 2023 Leigh Scott <leigh123linux@gmail.com> - 0.8-38
- Rebuild for new faad2 version

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.8-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.8-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.8-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8-34
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8-31
- Rebuilt for new ffmpeg snapshot

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8-29
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.8-27
- Rebuild for new ffmpeg version

* Mon Apr 15 2019 Xavier Bachelot <xavier@bachelot.org> - 0.8-26
- Drop mad sub-package, libmad is now in Fedora.

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
