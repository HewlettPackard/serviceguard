Summary: Serviceguard-Ansible
Name: Serviceguard-Ansible
Version: %{ansible_version}
Release: %{ansible_release}
Group: System
License: Hewlett Packard Enterprise
Packager: %{user}
URL: http://www.hpe.com/servers/sglx
Source: unavailable

%define _builddir %{_topdir}
%define objdir  %{_builddir}/objs
%define _buildroot     %{objdir}/rpmimage/%{distro}/ansible
BuildRoot: %{_buildroot}
%define _rpmdir       %{objdir}


# turn off man page compressing and binary stripping
%define __spec_install_post /bin/true

%description
Serviceguard Ansible.

%pre


%install

rm -rf $RPM_BUILD_ROOT
%define installroot %{_buildroot}
%define _builddir %{_topdir}

mkdir -p %{_rpmdir}
mkdir -p %{installroot}%{ansible_base}/ansible/group_vars
mkdir -p %{installroot}%{ansible_base}/ansible/playbooks
mkdir -p %{installroot}%{ansible_base}/ansible/roles
mkdir -p %{installroot}%{ansible_base}/ansible/roles/add-on
mkdir -p %{installroot}%{ansible_base}/ansible/roles/add-on/storage-flex/install/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/add-on/storage-flex/install/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/add-on/storage-flex/install/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/common
mkdir -p %{installroot}%{ansible_base}/ansible/roles/common/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/common/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/common/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/common/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/cluster
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/cluster/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/cluster/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/cluster/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/cluster/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/extns/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/extns/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/extns/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/config/extns/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/custom/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/custom/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/custom/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/custom/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aoai
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aofi
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aoai/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aoai/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aoai/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aoai/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aofi/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aofi/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aofi/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/mssql/aofi/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/dg
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/si
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/dg/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/dg/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/dg/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/dg/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/si/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/si/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/si/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/oracle/si/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/hana
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/hana/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/hana/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/hana/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/hana/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/sap-app
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/sap-app/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/sap-app/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/sap-app/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/deploy/sap/sap-app/vars
mkdir -p %{installroot}%{ansible_base}/ansible/roles/install/defaults
mkdir -p %{installroot}%{ansible_base}/ansible/roles/install/handlers
mkdir -p %{installroot}%{ansible_base}/ansible/roles/install/tasks
mkdir -p %{installroot}%{ansible_base}/ansible/roles/install/vars

install -m 755 %{objdir}/ansible/group_vars/all.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/custom-app-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/mssql-aoai-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/mssql-aofi-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/oracle-dg-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/oracle-si-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/os_RedHat.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/os_SLES.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/sap-app-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/sap-hana-hosts.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/sglx-add-on-items.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/group_vars/sglx-workload-items.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/group_vars/
install -m 755 %{objdir}/ansible/hosts $RPM_BUILD_ROOT/%{ansible_base}/ansible/
install -m 755 %{objdir}/ansible/site.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/defaults/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/handlers/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/tasks/iso_install.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/tasks/repo_install.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/
install -m 755 %{objdir}/ansible/roles/add-on/storage-flex/install/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/add-on/storage-flex/install/vars/
install -m 755 %{objdir}/ansible/roles/common/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/defaults/
install -m 755 %{objdir}/ansible/roles/common/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/handlers/
install -m 755 %{objdir}/ansible/roles/common/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/
install -m 755 %{objdir}/ansible/roles/common/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/tasks/
install -m 755 %{objdir}/ansible/roles/common/tasks/set_passwordless_ssh.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/tasks/
install -m 755 %{objdir}/ansible/roles/common/tasks/unset_passwordless_ssh.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/tasks/

install -m 755 %{objdir}/ansible/roles/common/tasks/setup_lvm_config.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/tasks/
install -m 755 %{objdir}/ansible/roles/common/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/common/vars/
install -m 755 %{objdir}/ansible/roles/config/cluster/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/defaults/
install -m 755 %{objdir}/ansible/roles/config/cluster/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/handlers/
install -m 755 %{objdir}/ansible/roles/config/cluster/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/
install -m 755 %{objdir}/ansible/roles/config/cluster/tasks/create_cluster.yml  $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/tasks/
install -m 755 %{objdir}/ansible/roles/config/cluster/tasks/easy_deploy_cl.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/tasks/
install -m 755 %{objdir}/ansible/roles/config/cluster/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/tasks/
install -m 755 %{objdir}/ansible/roles/config/cluster/tasks/view_cluster.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/tasks/
install -m 755 %{objdir}/ansible/roles/config/cluster/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/cluster/vars/
install -m 755 %{objdir}/ansible/roles/config/extns/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/extns/defaults/
install -m 755 %{objdir}/ansible/roles/config/extns/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/extns/handlers/
install -m 755 %{objdir}/ansible/roles/config/extns/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/extns/
install -m 755 %{objdir}/ansible/roles/config/extns/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/extns/tasks/
install -m 755 %{objdir}/ansible/roles/config/extns/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/config/extns/vars/
install -m 755 %{objdir}/ansible/roles/deploy/custom/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/custom/defaults
install -m 755 %{objdir}/ansible/roles/deploy/custom/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/custom/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/custom/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/custom/
install -m 755 %{objdir}/ansible/roles/deploy/custom/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/custom/tasks
install -m 755 %{objdir}/ansible/roles/deploy/custom/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/custom/vars/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aoai/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aoai/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aoai/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aoai/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aoai/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aoai/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aoai/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aoai/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aoai/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aoai/vars/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aofi/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aofi/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aofi/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aofi/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aofi/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aofi/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aofi/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aofi/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/mssql/aofi/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/mssql/aofi/vars/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/dg/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/dg/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/dg/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/dg/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/dg/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/dg/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/dg/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/dg/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/dg/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/dg/vars/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/vars/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/vars/os_RedHat.yml  $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/vars/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/vars/os_sles.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/vars/
install -m 755 %{objdir}/ansible/roles/deploy/oracle/si/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/oracle/si/
install -m 755 %{objdir}/ansible/roles/deploy/sap/hana/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/hana/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/sap/hana/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/hana/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/sap/hana/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/hana/
install -m 755 %{objdir}/ansible/roles/deploy/sap/hana/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/hana/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/sap/hana/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/hana/vars/
install -m 755 %{objdir}/ansible/roles/deploy/sap/sap-app/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/sap-app/defaults/
install -m 755 %{objdir}/ansible/roles/deploy/sap/sap-app/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/sap-app/handlers/
install -m 755 %{objdir}/ansible/roles/deploy/sap/sap-app/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/sap-app/
install -m 755 %{objdir}/ansible/roles/deploy/sap/sap-app/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/sap-app/tasks/
install -m 755 %{objdir}/ansible/roles/deploy/sap/sap-app/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/deploy/sap/sap-app/vars/
install -m 755 %{objdir}/ansible/roles/install/defaults/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/defaults/
install -m 755 %{objdir}/ansible/roles/install/handlers/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/handlers/
install -m 755 %{objdir}/ansible/roles/install/README.md $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/
install -m 755 %{objdir}/ansible/roles/install/tasks/iso_install.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/tasks/
install -m 755 %{objdir}/ansible/roles/install/tasks/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/tasks/
install -m 755 %{objdir}/ansible/roles/install/tasks/repo_install.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/tasks/
install -m 755 %{objdir}/ansible/roles/install/vars/main.yml $RPM_BUILD_ROOT/%{ansible_base}/ansible/roles/install/vars/

%postun
rm -Rf %{ansible_base}

%clean
rm -Rf %{ansible_base}

%files
%defattr(-,root,root)
%dir %{ansible_base}

%attr(-,root,root) %{ansible_base}/ansible/group_vars/all.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/custom-app-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/mssql-aoai-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/mssql-aofi-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/oracle-dg-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/oracle-si-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/os_RedHat.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/os_SLES.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/sap-app-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/sap-hana-hosts.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/sglx-add-on-items.yml
%attr(-,root,root) %{ansible_base}/ansible/group_vars/sglx-workload-items.yml
%attr(-,root,root) %{ansible_base}/ansible/hosts
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/iso_install.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/tasks/repo_install.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/add-on/storage-flex/install/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/common/tasks/set_passwordless_ssh.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/tasks/unset_passwordless_ssh.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/tasks/setup_lvm_config.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/common/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/tasks/create_cluster.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/tasks/easy_deploy_cl.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/tasks/view_cluster.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/cluster/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/extns/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/extns/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/extns/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/config/extns/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/config/extns/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/custom/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/custom/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/custom/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/custom/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/custom/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aoai/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aoai/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aoai/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aoai/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aoai/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aofi/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aofi/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aofi/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aofi/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/mssql/aofi/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/dg/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/dg/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/dg/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/dg/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/dg/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/vars/os_RedHat.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/oracle/si/vars/os_sles.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/hana/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/hana/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/hana/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/hana/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/hana/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/sap-app/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/sap-app/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/sap-app/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/sap-app/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/deploy/sap/sap-app/README.md
%attr(-,root,root) %{ansible_base}/ansible/roles/install/defaults/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/tasks/iso_install.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/vars/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/handlers/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/tasks/repo_install.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/tasks/main.yml
%attr(-,root,root) %{ansible_base}/ansible/roles/install/README.md
%attr(-,root,root) %{ansible_base}/ansible/site.yml
