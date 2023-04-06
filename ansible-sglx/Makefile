# Makefile to build Ansible RPM
DISTRO := $(shell if [ -f /etc/os-release ]; \
         then cat /etc/os-release|grep -qi SLES; \
         if [[ $$? -eq 0 ]]; \
         then echo sles; \
         fi; \
         cat /etc/os-release|grep -qi -e RedHat -e Centos; \
         if [[ $$? -eq 0 ]]; \
         then echo redhat; \
         fi;\
         else if [ -f /etc/redhat-release ]; \
         then echo redhat; \
         else if [ -f /etc/SuSE-release ]; \
         then echo sles; fi; fi; \
         fi)
ifeq ($(BUILD_OS), ol)
	DISTRO := ol
endif
DISTRO := linux
ANSIBLE_BASE_DIR := $(CURDIR)
ANSIBLE_OBJ_DIR := $(CURDIR)/objs
ANSIBLE_BUILD_DIR := $(CURDIR)/build
ANSIBLE_INSTALL_DIR := /opt/hpe/
ANSIBLE_RPM_IMG_DIR = ${ANSIBLE_OBJ_DIR}/rpmimage/$(DISTRO)/ansible

RPM_ARCH := noarch
RPM_X86_ARCH := x86_64
ANSIBLE_MC_VERSION = 15.99.01
ENDPOINT_API_VERSION = v1
RPMCMD=$(shell if [ -f /usr/bin/rpmbuild ]; then echo rpmbuild; else echo rpm; fi)
 
ANSIBLE_RPM_DEFINES = --define 'ansible_base ${ANSIBLE_INSTALL_DIR}' --define 'ansible_version $(ANSIBLE_MC_VERSION)' --define '_topdir $(CURDIR)' --define 'buildobjdir objs' \
                   --define 'distro $(DISTRO)' --define 'buildroot ${ANSIBLE_RPM_IMG_DIR}' --define 'ansible_release $(DISTRO)'
 
sglx-ansible-rpm := Serviceguard-Ansible-$(ANSIBLE_MC_VERSION)-linux.$(RPM_X86_ARCH).rpm

ansible_rpm: $(sglx-ansible-rpm)
$(sglx-ansible-rpm): $(ANSIBLE_BASE_DIR)/build/ansible.spec clean_ansible build_ansible
	${RPMCMD}  -bb --quiet --target=${RPM_X86_ARCH} ${ANSIBLE_RPM_DEFINES} $< ;
	@rm -Rf BUILD BUILDROOT RPMS SOURCES SPECS SRPMS
	@mv ${ANSIBLE_OBJ_DIR}/$(RPM_X86_ARCH)/$(sglx-ansible-rpm) ${ANSIBLE_BASE_DIR} ;


clean_ansible:
	@rm -Rf ${ANSIBLE_OBJ_DIR}/objs/ansible;


build_ansible:
	@echo "Building ANSIBLE project...."
	mkdir -p ${ANSIBLE_BASE_DIR}/objs/ansible;
	cp -r ${ANSIBLE_BASE_DIR}/build ${ANSIBLE_BASE_DIR}/objs/ansible; 
	cp -r ${ANSIBLE_BASE_DIR}/group_vars ${ANSIBLE_BASE_DIR}/objs/ansible;
	cp -r ${ANSIBLE_BASE_DIR}/roles ${ANSIBLE_BASE_DIR}/objs/ansible;
	cp -r ${ANSIBLE_BASE_DIR}/main ${ANSIBLE_BASE_DIR}/objs/ansible;
	cp ${ANSIBLE_BASE_DIR}/hosts ${ANSIBLE_BASE_DIR}/objs/ansible;
	cp ${ANSIBLE_BASE_DIR}/site.yml ${ANSIBLE_BASE_DIR}/objs/ansible;

