Role Name
=========

Role to configure a cluster on group of hosts.

Requirements
------------

Serviceguard is installed on the servers where the cluster needs to be configured

Role Variables
--------------
sglx_cmd_path                        - Defined in "os_*.yml" that point to Serviceguard binaries for a OS distribution.

cluster_cmd_exec:                     - Defined in defaults/main.yml that store the result of command exection. Values can be  
   exec_result: "cluster_cmd_result"    "passed" or "failed".                                        
op                                     - Operation to be performed on the cluster. Values can be "create" or "edit"
   
Dependencies
------------
None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: config/cluster, vars: { op: "create" }

License
-------

HPE

Author Information
------------------

