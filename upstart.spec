Name:           upstart
Version:        0.6.5
Release:        6.1%{?dist}
Summary:        An event-driven init system

Group:          System Environment/Base
License:        GPLv2 and LGPLv2+
URL:            http://upstart.ubuntu.com
Source0:        http://upstart.ubuntu.com/download/0.6/upstart-%{version}.tar.gz
Source1:        init-system-dbus.conf
Patch1:         upstart-telinit.patch
Patch2:         upstart-audit-events.patch
# set DEAD_PROCESS for died proccess with pid in utmp table (#556731)
Patch3:         upstart-utmp.patch
# SIGTERM handler re-execs init (#588929)
Patch4:         upstart-reexec.patch
# shutdown exits with nonzero exitcode when fails (#608569)
Patch5:         upstart-shutdown-exitcode.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: SysVinit < 2.86-24, sysvinit < 2.86-24
Provides: SysVinit = 2.86-24, sysvinit = 2.86-24
BuildRequires:  gettext, audit-libs-devel, expat-devel 
BuildRequires:  dbus-devel >= 1:1.2.16, libnih-devel >= 1.0.1

%description
Upstart is an event-based replacement for the /sbin/init daemon which
handles starting of tasks and services during boot, stopping them
during shutdown and supervising them while the system is running.

%prep
%setup -q
%patch1 -p1 -b .u
%patch2 -p1 -b .audit
%patch3 -p1 -b .utmp
%patch4 -p1 -b .reexec
%patch5 -p1 -b .exitcode

%build
%configure --sbindir=/sbin --libdir=/%{_lib}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# don't ship default jobs
rm -f %{buildroot}/%{_sysconfdir}/init/*
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/init/

%find_lang %{name}

%check
#some tests fail in koji while pass in mock and local build
#to run make check use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
  make check
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc COPYING
%doc NEWS
%doc README
%doc TODO
%doc HACKING
%{_sysconfdir}/init/
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/Upstart.conf
/sbin/halt
/sbin/init
/sbin/initctl
/sbin/poweroff
/sbin/reboot
/sbin/runlevel
/sbin/shutdown
/sbin/start
/sbin/status
/sbin/stop
/sbin/restart
/sbin/telinit
/sbin/reload
%{_mandir}/man5/init.5.gz
%{_mandir}/man5/inittab.5.gz
%{_mandir}/man7/control-alt-delete.7.gz
%{_mandir}/man7/keyboard-request.7.gz
%{_mandir}/man7/power-status-changed.7.gz
%{_mandir}/man7/runlevel.7.gz
%{_mandir}/man7/started.7.gz
%{_mandir}/man7/starting.7.gz
%{_mandir}/man7/startup.7.gz
%{_mandir}/man7/stopped.7.gz
%{_mandir}/man7/stopping.7.gz
%{_mandir}/man7/upstart.7.gz
%{_mandir}/man8/restart.8.gz
%{_mandir}/man8/halt.8.gz
%{_mandir}/man8/init.8.gz
%{_mandir}/man8/initctl.8.gz
%{_mandir}/man8/poweroff.8.gz
%{_mandir}/man8/reboot.8.gz
%{_mandir}/man8/runlevel.8.gz
%{_mandir}/man8/shutdown.8.gz
%{_mandir}/man8/start.8.gz
%{_mandir}/man8/status.8.gz
%{_mandir}/man8/stop.8.gz
%{_mandir}/man8/telinit.8.gz
%{_mandir}/man8/reload.8.gz

%changelog
* Wed Jun 30 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-6.1
- print error message and remove /etc/nologin when sysvinit shutdown fails

* Wed Jun 30 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-6
- shutdown exits with nonzero exitcode when sysvinit shutdown fails (#608569)

* Fri May 07 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-5
- re-add SIGTERM handler so restart on shutdown works, avoiding dirty inodes (#588929)

* Tue May 04 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-4
- set DEAD_PROCESS for died proccess with pid in utmp table (#556731)

* Tue Mar 23 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-3.2
- removed upstart-dont-close-console.patch (#568418)

* Fri Mar 12 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-3.1
- don't reopen std* from /dev/console to /dev/null (#568418)

* Wed Feb 24 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-3
- run "make check" only with --with check

* Fri Feb 19 2010 Casey Dahlin <cdahlin@redhat.com> 0.6.5-2
- be more specific about which libnih we need.

* Wed Feb 17 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.5-1
- upgrade to 0.6.5

* Fri Jan 29 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.3-7
- add SIGUSR1 handler and init-system-dbus.conf (#559660)

* Sun Jan 17 2010 Dennis Gilmore <dennis@ausil.us> - 0.6.3-6
- add patch from upstream fixing sparc alignment issues

* Mon Jan 11 2010 Petr Lautrbach <plautrba@redhat.com> 0.6.3-5
- License changed to GPLv2 and LGPLv2+

* Wed Dec 16 2009 Petr Lautrbach <plautrba@redhat.com> 0.6.3-4
- audit events patch rebased for 0.6 (#470661, #554474)

* Thu Dec  3 2009 Bill Nottingham <notting@redhat.com> 0.6.3-3
- make 'telinit u' a no-op, temporarily

* Fri Nov 27 2009 Petr Lautrbach <plautrba@redhat.com> 0.6.3-2
- Removed tests which fail in koji

* Fri Nov 20 2009 Casey Dahlin <cdahlin@redhat.com> - 0.6.3-1
- Upgrade to 0.6.3

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.11-3
- rebuilt with new audit

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Petr Lautrbach <plautrba@redhat.com> - 0.3.11-1
- Update to 0.3.11

* Mon Apr 27 2009 Bill Nottingham <notting@redhat.com> - 0.3.9-24
- Apply the audit patch correctly (#470661)

* Fri Apr 3 2009 Casey Dahlin <cdahlin@redhat.com> - 0.3.9-23
- Add audit events patch from Steve Grubb <sgrubb@redhat.com> (Bug #470661)

* Fri Jan 23 2009 Casey Dahlin <cdahlin@redhat.com> - 0.3.9-22
- Re-add 'telinit u' support along with patch to fix it (#450488). Patch due to
  <pspencer@fields.utoronto.ca>

* Mon Jan 12 2009 Bill Nottingham <notting@redhat.com> - 0.3.9-21
- Remove 'telinit u' support as it is broken (#450488, <cjdahlin@ncsu.edu>)

* Fri Apr 25 2008 Bill Nottingham <notting@redhat.com> - 0.3.9-19
- with the merge of event-compat-sysv, move the sysvinit obsoletes/provides here

* Thu Apr 24 2008 Bill Nottingham <notting@redhat.com> - 0.3.9-18
- fix some man page typos (#444008, <archimerged@gmail.com>)

* Wed Apr 09 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-17
- Added list of stock events to events(5)

* Tue Apr 08 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-16
- Add telinit u support

* Fri Apr 04 2008 Bill Nottingham <notting@redhat.com> - 0.3.9-15
- Add a events(5) manpage that describes event syntax

* Thu Apr 03 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-14
- Change bug report email address to fedora-devel-list@redhat.com

* Thu Mar 14 2008 Bill Nottingham <notting@redhat.com> - 0.3.9-13
- Ignore rpm temporary files of the foo;<somehex> format
- Make ignores of .rpm{new,orig,save} match only at the end of the name

* Wed Mar 13 2008 Bill Nottingham <notting@redhat.com> - 0.3.9-12
- forgot about rpmorig too (ugh)

* Wed Mar 13 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-11
- Make logd a noreplace

* Wed Mar 13 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-10
- Add patch to ignore .rpm{new,save} files

* Sun Mar 03 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-9
- Remove automake dependency, build Makefile.in changes into patch

* Sun Mar 03 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-8
- Run automake after patching

* Sun Mar 03 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-7
- Added BuildRequires: automake

* Sun Mar 03 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-6
- Added patch to allow runtime tty changes

* Fri Feb 15 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-5
- Added patch to imply --force on runlevels 0 and 6

* Wed Feb 06 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-4
- Patched for GCC 4.3

* Thu Jan 31 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-3
- Added AUTHORS, COPYING, etc.
- Made config --libdir option relative

* Mon Jan 21 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-2
- Remove libnih and libupstart

* Sun Jan 13 2008 Casey Dahlin <cjdahlin@ncsu.edu> - 0.3.9-1
- Initial packaging
