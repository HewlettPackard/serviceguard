KERNEL_SOURCE := /lib/modules/`uname -r`/source
KERNEL_BUILD  := /lib/modules/`uname -r`/build

# Module will be installed into /lib/modules/`uname -r`/kernel/extra

obj-m           := deadman.o

# Do not print "Entering directory ..."
MAKEFLAGS += --no-print-directory

# Targets for running make directly in the external module directory:
modules modules_install clean:
	@$(MAKE) -C $(KERNEL_SOURCE) $@ O=$(KERNEL_BUILD) M=$(CURDIR)
