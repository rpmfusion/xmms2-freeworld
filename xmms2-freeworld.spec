%define codename DrLecter

Name:			xmms2-freeworld
Summary: 		Plugins for XMMS2 that cannot be included in Fedora
Version:		0.5
Release:		6%{?dist}
License:		LGPLv2+ and GPL+ and BSD
Group:			Applications/Multimedia
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		http://downloads.sourceforge.net/xmms2/xmms2-%{version}%{codename}.tar.bz2
# From upstream git (Compilation fixes)
Patch0:			xmms2-devel.git-37578b59f5d7376213da74b3bf6b7c7f430d0bc9.patch
# Use libdir properly for Fedora multilib
Patch1:			xmms2-0.5DrLecter-use-libdir.patch

# Don't add extra CFLAGS, we're smart enough, thanks.
Patch4: 		xmms2-0.5DrLecter-no-O0.patch
# More sane versioning
Patch5:			xmms2-0.5DrLecter-moresaneversioning.patch

# From upstream git (fix avcodec compilation and bugs)
Patch10:		xmms2-devel.git-fae1d0cfd643e999d419162979b9c90d12a30002.patch
Patch11:		xmms2-devel.git-be6f8e111913433a0fee1ddfa3d234067695aadf.patch
Patch12:		xmms2-devel.git-a63d0f80f384ffd15c921af74f036d785d3b72df.patch
Patch13:		xmms2-devel.git-6f06f3409dfa82b7a3e7fdd682567d46fd65e262.patch
Patch14:		xmms2-devel.git-93aab85319fcc168db2d35058e996826a5c6a034.patch
Patch15:		xmms2-devel.git-d09c0d8a971c0333a0c8387113f744f0b9899fe4.patch
Patch16:		xmms2-devel.git-a42762549126b8facdab90cf01a17fa106bc8dce.patch
Patch17:		xmms2-devel.git-fccc583328ca58110a8b6e00ccb8c0bb1f6923ad.patch

URL:			http://wiki.xmms2.xmms.se/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		sqlite-devel
BuildRequires:		glib2-devel
BuildRequires:		python-devel
# RPMFusion only BuildRequires
BuildRequires:		faad2-devel, libmad-devel, ffmpeg-devel, libmms-devel
# Keep the mac plugin disabled until mac goes to free repo
#BuildRequires:		mac-devel

Requires:		xmms2-avcodec = %{version}-%{release}
Requires:		xmms2-faad = %{version}-%{release}
Requires:		xmms2-mad = %{version}-%{release}
Requires:		xmms2-mms = %{version}-%{release}
Requires:		xmms2-mp4 = %{version}-%{release}
#Requires:		xmms2-mac = %%{version}-%%{release}


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
Group:		Applications/Multimedia
Requires:	xmms2 = %{version}

%description -n xmms2-avcodec
An XMMS2 Plugin which provides support for audio formats provided by
FFMPEG's libavcodec.


%package -n xmms2-faad
Summary:	XMMS2 Plugin for AAC and MP4 audio formats
License:	GPLv2+
Group:		Applications/Multimedia
Requires:	xmms2 = %{version}

%description -n xmms2-faad
An XMMS2 Plugin which provides support for audio formats provided by FAAD 
(AAC and MP4).

#%%package -n xmms2-mac
#Summary:	XMMS2 Plugin for APE audio format
#License:	GPLv2+
#Group:		Applications/Multimedia
#Requires:	xmms2 = %%{version}

#%%description -n xmms2-mac
#An XMMS2 Plugin for listening to Monkey's Audio files.

%package -n xmms2-mad
Summary:	XMMS2 Plugin for MPEG Audio files
License:	GPLv2+
Group:		Applications/Multimedia
Requires:	xmms2 = %{version}

%description -n xmms2-mad
An XMMS2 Plugin for listening to MPEG files (MPEG 1 & 2 layers I, II and III 
- includes MP3).

%package -n xmms2-mms
Summary:	XMMS2 Plugin for MMS audio streams
License:	LGPLv2+
Group:		Applications/Multimedia
Requires:	xmms2 = %{version}

%description -n xmms2-mms
An XMMS2 Plugin for listening to Microsoft Media Services (MMS) audio streams.

%package -n xmms2-mp4
Summary:	XMMS2 Plugin for MP4 audio
License:	GPLv2+
Group:		Applications/Multimedia
Requires:	xmms2 = %{version}

%description -n xmms2-mp4
An XMMS2 Plugin for listening to MP4 audio files.

%prep
%setup -q -n xmms2-%{version}%{codename}
%patch0 -p1 -b .compilefix
%patch1 -p1 -b .plugins-use-libdir

%patch4 -p1 -b .noO0
%patch5 -p1 -b .versionsanity

%patch10 -p1 -b .avcodec10
%patch11 -p1 -b .avcodec11
%patch12 -p1 -b .avcodec12
%patch13 -p1 -b .avcodec13
%patch14 -p1 -b .avcodec14
%patch15 -p1 -b .avcodec15
%patch16 -p1 -b .avcodec16
%patch17 -p1 -b .avcodec17


# Clean up paths in wafadmin
WAFADMIN_FILES=`find wafadmin/ -type f`
for i in $WAFADMIN_FILES; do
	 sed -i 's|/usr/lib|%{_libdir}|g' $i
done

%build
export CFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
		--with-libdir=%{_libdir} \
		--with-pkgconfigdir=%{_libdir}/pkgconfig \
		--without-optionals=avahi \
		--without-optionals=cli \
		--without-optionals=dns_sd \
		--without-optionals=et \
		--without-optionals=launcher \
		--without-optionals=medialib-updater \
		--without-optionals=perl \
		--without-optionals=pixmaps \
		--without-optionals=python \
		--without-optionals=ruby \
		--without-optionals=xmmsclient-ecore \
		--without-optionals=xmmsclient++ \
		--without-optionals=xmmsclient++-glib \
		--without-plugins=airplay \
		--without-plugins=alsa \
		--without-plugins=ao \
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
		--without-plugins=gme \
		--without-plugins=gvfs \
		--without-plugins=ices \
		--without-plugins=icymetaint \
		--without-plugins=id3v2 \
		--without-plugins=jack \
		--without-plugins=karaoke \
		--without-plugins=lastfm \
		--without-plugins=lastfmeta \
		--without-plugins=m3u \
		--without-plugins=modplug \
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
		--without-plugins=speex \
		--without-plugins=vocoder \
		--without-plugins=vorbis \
		--without-plugins=wave \
		--without-plugins=xml \
		--without-plugins=xspf 

./waf build -v %{?_smp_mflags}

%install
rm -rf %{buildroot}
./waf install --destdir=%{buildroot} --prefix=%{_prefix} --with-libdir=%{_libdir} --with-pkgconfigdir=%{_libdir}/pkgconfig

# There are lots of things that get built that we don't need to package, because they're in the Fedora xmms2 package.
rm -rf %{buildroot}%{_bindir} %{buildroot}%{_libdir}/libxmmsclient* %{buildroot}%{_mandir} %{buildroot}%{_datadir} %{buildroot}%{_includedir} %{buildroot}%{_libdir}/pkgconfig 

# exec flags for debuginfo
chmod +x %{buildroot}%{_libdir}/xmms2/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL COPYING.LGPL

%files -n xmms2-avcodec
%defattr(-,root,root,-)
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_avcodec.so

%files -n xmms2-faad
%defattr(-,root,root,-)
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_faad.so

#%%files -n xmms2-mac
#%%defattr(-,root,root,-)
#%%doc COPYING.GPL
#%%{_libdir}/xmms2/libxmms_mac.so

%files -n xmms2-mad
%defattr(-,root,root,-)
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_mad.so

%files -n xmms2-mms
%defattr(-,root,root,-)
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_mms.so

%files -n xmms2-mp4
%defattr(-,root,root,-)
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_mp4.so

%changelog
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
