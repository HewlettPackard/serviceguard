# Ansible Playbooks for HPE Serviceguard for Linux.

This collection provides a series of Ansible roles for performing actions on HPE Serviceguard for Linux Clusters.

Actions for HPE Serviceguard for Linux Clusters currently include 

	a) Installing HPE Serviceguard for Linux 15.00.00 or later.

	b) Configuring HPE Serviceguard for Linux clusters 15.00.00 or later.

	c) Deploying Oracle and MSSQL solutions using respective Add-ons 15.00.00 or later.

## Requirements

 - Ansible >= 2.9
 - python >= 3.4.2

## Usage

Clone the repository on ansible control node.

```bash
git clone https://github.com/HewlettPackard/serviceguard.git
cd serviceguard/ansible-sglx
```

To upgrade to the latest version of the playbooks:

```bash
git pull https://github.com/HewlettPackard/serviceguard.git
```
### Install, Configure and Deploy HPE Serviceguard Clusters.

Master playbook [site.yml](site.yml) contains the roles which will be executed for the
inventory defined in [hosts](hosts).

When the master playbook is run
 - Version specified in the parameters file will be installed
 - Cluster will be configured on the set of nodes with default parameters.
   For defaults of Serviceguard cluster values, refer to [Concepts guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sd00002308en_us&docLocale=en_US).
 - Application deployed on the clusters will be configured under purview of the Serviceguard
   cluster using corresponding Serviceguard Add-on.

Users have the option of creating a playbook by importing specific roles defined in the
[roles](roles) directory.

The parameters for the master playbook, roles are configured in [group_vars/all.yml](group_vars/all.yml).

### Parameters for playbooks
This section contains description of parameters under [group_vars/all.yml](group_vars/all.yml) that can help users to
start using the playbooks.

Configuring version of Serviceguard to be installed.
```yaml
sglx_version : 15.00.00
```
Mode of the installation. If ISO mode is specified then ISO file path is specified under iso_params section
below.
```yaml
sglx_inst_upg_mode: iso
sglx_inst_upg_additional_params:
    ..
    iso_params:
        iso_location: <absolute path of the iso>
```

Some users prefer a method of mounting Serviceguard ISO on a node and export it as a NFS share in their
environment. In case NFS server is configured then it can be specified as
```yaml
sglx_inst_upg_mode: iso
sglx_inst_upg_additional_params:
    ..
    iso_params:
        iso_location: nfs://<NFS_server_hostname>/<exported_share_path>
```
##### Note: Ensure that exported share is accessible to all the hosts specified in the inventory file.

Serviceguard supports multiple add-ons, installation for specific add-on can be configured under

```yaml
sglx_add_on_inst_upg_params:
    sglx_addon: oracle
```
Serviceguard requires an arbitration mechanism for configuring a cluster. Arbitration mechanism
can be configured under

```yaml
sglx_arbitation_method: qs
```

Serviceguard installation mandates a replicated user configuration. As part of the installation,
a replicated user for Serviceguard Manager (sgmgr) is created on the hosts and the password for
the same can be configured under the below parameter.

```yaml
sglx_sgmgr_password: "{{ vault_sglx_sgmgr_password }}"
```

### Encrypting the Passwords using Ansible vault
Create a file in your home directory. Example: “vault_password.txt”.
Key specified as part of "vault_password.txt" will be used to create the ansible vault secret.
    
More information on generating ansible vault secrets can be found
[here](https://docs.ansible.com/ansible/latest/user_guide/vault.html#managing-vault-passwords)

```bash
ansible-vault encrypt_string 'some_string' --name 'vault_sglx_sgmgr_password'
```
The generated output must be substituted in
```yaml
vault_sglx_sgmgr_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          34363834323266326237363636613833396665333061653138623431626261343064373363656165
          6639383863383633643035656336336639373161323663380a303331306337396435366535313663
          31336636333862303462346234336138393135393363323739633661653534306162323565646561
          6662396366333534350a663033303862646331613765306433353632316435306630343761623237
          3863
```
Similar substitution is required for the parameters that vault enabled password.

### Running the playbook

When the parameters specified above are configured, playbook [site.yml](site.yml) can be run
from the directory where the repository is cloned on the ansible control node.

```bash
cd serviceguard/ansible-sglx
ansible-playbook -i hosts -v --vault-password-file <path_to_vault_password_file> site.yml
```

## License

This project is licensed under the Apache 2.0 license. Please see the [LICENSE](LICENSE) for more information.

## Issues
Please report issues or problems using the Issues section of Github.

## Contributing and feature requests

**Contributing:** We welcome your contributions to the Ansible roles for HPE Serviceguard for Linux.
See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought
of everything, because we assure you that is not the case.

## Features

The ansible deliverables includes
[roles](roles)


## Copyright

© Copyright 2023 Hewlett Packard Enterprise Development LP
