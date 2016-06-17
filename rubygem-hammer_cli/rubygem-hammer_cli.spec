%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name hammer_cli
%global confdir hammer

%{!?_root_bindir:%global _root_bindir %{_bindir}}
%{!?_root_sysconfdir:%global _root_sysconfdir %{_sysconfdir}}

Summary: Universal command-line interface for Foreman
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.7.0
Release: 1%{?dist}
Group: Development/Languages
License: GPLv3
URL: http://github.com/theforeman/hammer-cli
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(clamp) >= 1.0.0
Requires: %{?scl_prefix}rubygem(logging)
Requires: %{?scl_prefix}rubygem(awesome_print)
Requires: %{?scl_prefix}rubygem(table_print) >= 1.5.0
Requires: %{?scl_prefix}rubygem(highline)
Requires: %{?scl_prefix}rubygem(fast_gettext)
Requires: %{?scl_prefix}rubygem(locale) >= 2.0.6
Requires: %{?scl_prefix}rubygem(apipie-bindings) >= 0.0.14
Requires: %{?scl_prefix}rubygem(apipie-bindings) < 0.1.0
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}}
%if 0%{?scl:1}
Obsoletes: rubygem-%{gem_name} < 0.3.0-2
%endif

%description
Hammer cli provides universal extendable CLI interface for ruby apps

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}-doc}
BuildArch: noarch
%if 0%{?scl:1}
Obsoletes: rubygem-%{gem_name}-doc < 0.3.0-2
%endif

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - <<EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

sed -i '1s@/.*@/usr/bin/%{?scl_prefix}ruby@' .%{_bindir}/*
mkdir -p %{buildroot}%{_root_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_root_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

mkdir -p %{buildroot}%{_root_sysconfdir}/bash_completion.d
mv %{buildroot}%{gem_instdir}/hammer_cli_complete %{buildroot}%{_root_sysconfdir}/bash_completion.d/%{gem_name}

mkdir -p %{buildroot}%{_root_sysconfdir}/%{confdir}/cli.modules.d
install -m 755 .%{gem_instdir}/config/cli_config.template.yml \
               %{buildroot}%{_root_sysconfdir}/%{confdir}/cli_config.yml

%files
%dir %{gem_instdir}
%{_root_bindir}/hammer
%{_root_sysconfdir}/bash_completion.d/%{gem_name}
%{_root_sysconfdir}/%{confdir}/cli.modules.d
%config(noreplace) %{_root_sysconfdir}/%{confdir}/cli_config.yml
%{gem_instdir}/bin
%{gem_instdir}/lib
%{gem_instdir}/locale
%{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/test
%doc %{gem_docdir}
%doc %{gem_instdir}/config
%doc %{gem_instdir}/doc
%doc %{gem_instdir}/README.md

%changelog
* Fri May 27 2016 Dominic Cleal <dominic@cleal.org> 0.6.1-2
- Use gem_install macro (dominic@cleal.org)

* Tue Mar 15 2016 Dominic Cleal <dominic@cleal.org> 0.6.1-1
- Update hammer_cli to 0.6.1 (dominic@cleal.org)

* Tue Dec 22 2015 Dominic Cleal <dcleal@redhat.com> 0.5.1-2
- Replace ruby(abi) for ruby22 rebuild (dcleal@redhat.com)

* Tue Dec 15 2015 Tomas Strachota <tstrachota@redhat.com> 0.5.1-1
- Update hammer_cli to 0.5.1 (tstrachota@redhat.com)

* Wed Oct 07 2015 Dominic Cleal <dcleal@redhat.com> 0.4.0-1
- Update hammer_cli to 0.4.0 (dcleal@redhat.com)

* Tue Aug 25 2015 Dominic Cleal <dcleal@redhat.com> 0.3.0-2
- Use tfm-ruby in shebang line (dcleal@redhat.com)
- Converted to tfm SCL (dcleal@redhat.com)
- Increase range of non-SCL obsoletes to cover 1.9 versions (dcleal@redhat.com)

* Tue Aug 04 2015 Dominic Cleal <dcleal@redhat.com> 0.3.0-1
- Update hammer_cli to 0.3.0 (dcleal@redhat.com)
- fixes #8979 - convert hammer packages to SCL (dcleal@redhat.com)
- Require clamp >=1.0.0 (dcleal@redhat.com)

* Mon Apr 27 2015 Dominic Cleal <dcleal@redhat.com> 0.2.0-1
- Update hammer_cli to 0.2.0 (dcleal@redhat.com)
- refs #10154 - require locale 2.0.6 (dcleal@redhat.com)
- Refresh hammer-cli dep versions (dcleal@redhat.com)
- refs #8829 - use config/ template from gem (dcleal@redhat.com)

* Fri Dec 12 2014 Dominic Cleal <dcleal@redhat.com> 0.1.4-1
- Update hammer_cli to 0.1.4 (martin.bacovsky@gmail.com)
- Added rb-readline dependency to rubygem-hammer_cli
  (martin.bacovsky@gmail.com)
- Refresh Hammer cli_config file (dcleal@redhat.com)

* Thu Aug 21 2014 Dominic Cleal <dcleal@redhat.com> 0.1.3-1
- Update rubygem-hammer_cli to 0.1.3 (martin.bacovsky@gmail.com)

* Thu Aug 14 2014 Dominic Cleal <dcleal@redhat.com> 0.1.2-1
- Update rubygem-hammer_cli to 0.1.2 (martin.bacovsky@gmail.com)

* Tue May 20 2014 Martin Bačovský <martin.bacovsky@gmail.com> 0.1.1-1
- Rebased hammer_cli to 0.1.1 (martin.bacovsky@gmail.com)

* Wed Mar 26 2014 Martin Bačovský <martin.bacovsky@gmail.com> 0.1.0-1
- Bump to 0.1.0 (martin.bacovsky@gmail.com)
- hammer_cli - new config location and dependencies (tstrachota@redhat.com)

* Wed Jan 29 2014 Martin Bačovský <mbacovsk@redhat.com> 0.0.18-1
- Bump to 0.0.18 (mbacovsk@redhat.com)

* Thu Jan 23 2014 Martin Bačovský <mbacovsk@redhat.com> 0.0.16-1
- Bump to 0.0.16 (mbacovsk@redhat.com)

* Tue Jan 21 2014 Martin Bačovský <mbacovsk@redhat.com> 0.0.15-1
- Bump to 0.0.15 (mbacovsk@redhat.com)

* Tue Jan 07 2014 Dominic Cleal <dcleal@redhat.com> 0.0.14-2
- Require fastercsv and mime-types on Fedora to avoid gemspec conflict
  (dcleal@redhat.com)

* Thu Dec 19 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.14-1
- Bump to 0.0.14 (mbacovsk@redhat.com)

* Wed Dec 18 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.13-1
- Bump to 0.0.13 (mbacovsk@redhat.com)

* Thu Dec 05 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.12-1
- Bump to 0.0.12 (mbacovsk@redhat.com)

* Tue Nov 26 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.11-1
- Bump to 0.0.11 (mbacovsk@redhat.com)

* Fri Nov 08 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.9-1
- Bumped to 0.0.9 (mbacovsk@redhat.com)

* Tue Oct 29 2013 Tomas Strachota <tstrachota@redhat.com> 0.0.8-1
- Update to Hammer CLI Foreman 0.0.8

* Wed Oct 09 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.7-1
- Bumped to 0.0.7 (mbacovsk@redhat.com)
- fixed error handling while loading hammer modules

* Tue Oct 08 2013 Martin Bačovský <mbacovsk@redhat.com> 0.0.6-2
- Added depenedency on fastercsv on ruby 1.8 (mbacovsk@redhat.com)

* Tue Oct 08 2013 Tomas Strachota <tstrachota@redhat.com> 0.0.6-1
- fixes #3184 - update hammer dependencies

* Thu Sep 26 2013 Sam Kottler <shk@redhat.com> 0.0.5-1
- Cherry pick hammer_cli version bump (shk@redhat.com)

* Tue Aug 27 2013 Dominic Cleal <dcleal@redhat.com> 0.0.3-4
- Install bash completion extension (dcleal@redhat.com)

* Mon Aug 26 2013 Sam Kottler <shk@redhat.com> 0.0.3-3
- Fix typo in macro (shk@redhat.com)
- Use macros provided by rubygems-devel on Fedora (shk@redhat.com)

* Mon Aug 26 2013 Sam Kottler <shk@redhat.com> 0.0.3-2
- Add configuration example to packaged files (shk@redhat.com)
- Fix readme path (shk@redhat.com)
- Add docs and other files that are new in the 0.0.3 release (shk@redhat.com)
- Add docs and other files that are new in the 0.0.3 release (shk@redhat.com)
- Bump hammer_cli version to 0.0.3 (shk@redhat.com)

* Thu Aug 15 2013 Sam Kottler <shk@redhat.com> 0.0.2-15
- Remove SCL conditional (shk@redhat.com)

* Thu Aug 15 2013 Sam Kottler <shk@redhat.com> 0.0.2-14
- Add multi_json dependency to hammer and fix gem_dir (shk@redhat.com)
- Fix changelog (shk@redhat.com)

* Tue Aug 13 2013 Sam Kottler <shk@redhat.com> 0.0.2-13
- Add logging requirement (shk@redhat.com)

* Tue Aug 13 2013 Sam Kottler <shk@redhat.com> 0.0.2-10
- Rebuilding on RHEL

* Mon Aug 12 2013 Sam Kottler <shk@redhat.com> 0.0.2-9
- Bump version

* Mon Aug 12 2013 Sam Kottler <shk@redhat.com> 0.0.2-8
- Bump hammer version (shk@redhat.com)

* Tue Aug 06 2013 Sam Kottler <shk@redhat.com> 0.0.1-7
- Add a missing %% (shk@redhat.com)
- Remove ruby(abi) for f19 (shk@redhat.com)

* Tue Aug 06 2013 Sam Kottler <shk@redhat.com> 0.0.1-6
- Fix bindir (shk@redhat.com)

* Tue Aug 06 2013 Sam Kottler <shk@redhat.com> 0.0.1-5
- Don't require ruby-abi on F19+ (shk@redhat.com)

* Thu Aug 01 2013 Sam Kottler <shk@redhat.com> 0.0.1-4
- Rebuild

* Thu Aug 01 2013 Sam Kottler <shk@redhat.com> 0.0.1-3
- Removed abi version for hammer_cli deps (shk@redhat.com)

* Thu Aug 01 2013 Sam Kottler <shk@redhat.com> 0.0.1-2
- Initial package with tito
* Wed Jul 31 2013  <shk@redhat.com> - 0.0.1-1
- Initial package
