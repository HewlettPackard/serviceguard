/*
 * Deadman: A Software Deadman Device
 *
 *  (c) Copyright 2007-2019 Hewlett Packard Enterprise Development LP. 
 *              http://www.hpe.com
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version
 *  2 of the License, or (at your option) any later version.
 *
 *  Hewlett-Packard Enterprise admits no liability nor provides
 *  warranty for any of this software. This material is provided 
 *  "AS-IS" and at no charge.
 *
 *      Fixes
 *      Release 2.28
 *             Murali L R              Changed:
 *                                     Replaced the call to spin_lock() and
 *                                     spin_unlock() with spin_lock_irqsave()
 *                                     and spin_unlock_irqrestore() routines 
 *                                     for Oracle Linux.
 *                                     On OL with UEK5 Update2 kernel version
 *                                     (v4.14.35-1902.6.1) we were not able to
 *                                     acquire the lock with prior routines.
 *      Release 2.27
 *             Prabhanjan Gururaj      Modified to support changes in kernel   
 *                                     version 4.18 and RHEL8.

 *      Release 2.26
 *             Sharath K G             Added root disk name and size to interface into
 *                                     the /proc filesystem for user to query.
 *      Release 2.25                   
 *             Saurabh Kadiyali        Changed:
 *                                     Modified to support on 4.14 kernel version 
 *                                     or higher as vfs_read() does not work on 
 *                                     these kernel versions.
 *      Release 2.24
 *             Ravi Mishra             Changed: 
 *                                     Modified to build on SLES15.
 *      Release 2.23
 *             Sharath K G             Changed: 
 *                                     Compliance for Spectre V 2.
 *      Release 2.22 
 *             Hari S Tiwari           Changed: 
 *                                     Corrected the typecast for copy_to_user call.
 *      Release 2.21 
 *             Sayed M Mujtaba         Changed: 
 *                                     Added code to include root disk monitoring.
 *
 *      Release 2.20
 *             Sarvameet Yadav          Changed:
 *                                      Modified code to pass platform information 
 *                                      to do conditional compilation for ACPI symbols
 *      Release 2.19
 *             Vaishnavi R              Changed:
 *                                      Resolved acpi headers error for 3.17.xx
 *                                      and later kernels.
 *      Release 2.18
 *             Hari S Tiwari            Changed:
 *                                      Log the process ID which disables the 
 *                                      safety timer.
 *      Release 2.17
 *             Deepa M Kini             Changed:
 *                                      In RedHat 7, Kernel 3.10.0 onwards,  
 *                                      1. There is a new function uid_valid() to  
 *                                      be used to validate euid and uid. 
 *                                      check_user_ids().
 *                                      2. init_timer_key() function requires a 
 *                                      new timer_flag parameter to be passed.
 *                                      __init deadman_init().
 *      Release 2.16
 *             Hari S Tiwari            Changed:
 *                                      Removed strcpy call, which tries to modify 
 *                                      the read-only page and panics the system. 
 *      Release 2.15
 *             Hari S Tiwari            Changed:
 *                                      Modified static buffer to stack buffer in
 *                                      ioctl call. Static buffer can be corrupted
 *                                      by different processes, trying to access it
 *                                      simultaneously.
 *      Release 2.14
 *             Manish R K               Added:
 *                                      Added code to pass platform information 
 *                                      when loading the module. Also, calling 
 *                                      emergency_restart() on some HP shipped 
 *                                      platforms was causing panic due to missing
 *                                      ACPI reset register mapping. Code is added
 *                                      fix this issue. 
 *      Release 2.13
 *             Hari S Tiwari            Added:
 *                                      Added code to pass HZ value while loading   
 *                                      the module. The preprocessor directives
 *                                      related to USER_HZ and HZ has been changed 
 *                                      to calculate these at run time. 
 *      Release 2.12
 *             Hari S Tiwari            Changed:
 *             Shashank Admane          Replaced the call create_proc_read_entry()
 *                                      with proc_create()/proc_create_data().
 *                                      Use init_timer_key() call with 2.6.32 kernel
 *                                      onwards.
 *      Release 2.11
 *             Amol Sanglikar           Added:
 *                                      Added code to access global variables
 *                                      in function current_jiffies_to_tsb()
 *                                      in safe way using lock , thus preventing
 *                                      corruption.
 *      Release 2.10
 *             Hari S Tiwari            Added:
 *                                      In compliance to GPL, added MODULE_AUTHOR
 *                                      and MODULE_DESCRIPTION fields.
 *      Release 2.9
 *             Sreedharamurthy K        Changed:
 *                                      -Modified ioctl structure changes as per
 *                                        new kernel 2.6.36 (and higher) and 
 *                                        function signature accordingly.
 *      Release 2.8
 *             Srinivas K Shapur        Changed:
 *                                      The way we access euid & uid has been changed 
 *                                      in RedHat 6. Kernel 2.6.32 onwards, added 
 *                                      check_user_ids().
 *                                    
 *      Release 2.7
 *             Don Cleland              Changed:
 *                                      1. linux/calc64.h to asm/div64.h
 *                                         (64 bit functions moved).
 *                                      2. create_proc_info_entry() to
 *                                         create_proc_read_entry()
 *                                         (previous call removed).
 *                                      Added:
 *                                      1. linux/jiffies.h
 *                                      2. linux/timer.h
 *                                      3. linux/kthread.h
 *
 *      Release 2.6
 *             John DeFranco            When building on 2.6.18 kernels
 *                                      don't include linux/config.h.
 *      Release 2.5
 *             John DeFranco            2.6.16 kernels set kernel
 *             Eric Soderberg           HZ values that break the
 *             Jayesh Patel             current conversions of 
 *             Chuck Carlino            jiffies <-> tsb. Added code to
 *                                      calculate jiffies <-> tsb correctly
 *                                      for HZ:250 and USER_HZ:100.
 *      Release 2.4                     2.6.14 kernels don't export
 *             John DeFranco            machine_restart() anymore. Instead
 *                                      they use emergency_restart();
 *                                      2.6.14 kernels changed MODULE_PARM()
 *                                      to module_param().
 *      Release 2.3                     Added use of safety_time directly.
 *             Eric Soderberg           With 2.6 RH 4, kernel HZ on IA32
 *             John DeFranco            is 1000 while user space (cmcld)
 *             Jayesh Patel             HZ remains 100. Before 2.6 kernel
 *                                      HZ was also 100. On IPF both HZ
 *                                      are 1024.
 *                                      Added code to convert jiffies to
 *                                      user space by saving pervious jiffies
 *                                      and pervious tsb
 *                                      
 *      Release 2.2
 *              John DeFranco:          Removed obsolete MOD_DEC_USE_COUNT and
 *                                      MOD_INC_USE_COUNT macros. Also modified
 *                                      the creating of the /proc/deadman
 *                                      directory so that it would be removed
 *                                      correctly on a rmmod.
 *      Release 2.1
 *              Jayesh Patel  :         If value specified for set timer is
 *                                      less than or eqaul to current timer
 *                                      then reset the system immediately.
 *
 *      Release 2.0
 *              Paul W. Chang :         Added feature to allow the system either
 *                                      reboot or panic when its safety time expires.
 *                                      Added also deadman_get_info to interface into
 *                                      the /proc filesystem for user to query.
 *
 *      Release 1.01
 *              Chad N. Tindel :        Use KERN_EMERG instead of KERN_CRIT
 *
 *      Release 1.0
 *              John DeFranco :         Set dynamic minor number.
 *                                      Added GPL licence hook for
 *                                      2.4.18 support.
 *      Release 0.02.
 *              Chad N. Tindel :        Port to 2.4.0-test7 kernel,
 *                                      added DEADMAN_MINOR as 185
 *      Release 0.01
 *              Eric Soderberg :        Initial Version for 2.2.16 kernel
 */

#include <linux/module.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/miscdevice.h>
#include <linux/reboot.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>
#include <linux/random.h>
#include "deadman.h"
#include <linux/version.h>
#include <linux/jiffies.h>
#include <linux/timer.h>
#include <linux/kthread.h>
#include <linux/seq_file.h>
#if LINUX_VERSION_CODE >= KERNEL_VERSION(3,17,0)
#define BUILDING_ACPICA
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
#include <acpi/platform/acenv.h>
#include <acpi/platform/aclinux.h>
#include <acpi/actypes.h>
#include <acpi/actbl.h>
#include <acpi/acpixf.h>
#include <acpi/acpiosxf.h>
#include <acpi/acexcep.h>
#endif

/* calc64.h includes do_div() */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,14)
#include <asm/div64.h>
#endif

/* This is just a hack for being able to build on kernels
 * <2.4.10 since they don't define MODULE_LICENSE().
 */
#ifndef _DO_NOT_INCLUDE_SG_GPL_
/* Add to avoid 'taining' kernel. Only valid on kernels >2.4.9 */
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Eric Soderberg");
MODULE_DESCRIPTION("Deadman Timer");
#ifndef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif
MODULE_INFO(supported, "external");
#endif

/* #define DEADMAN_TESTING 1 */

/* This should be defined identical to SG safety time in h/safety_time.h */
struct safety_tsb {
    unsigned long tsb_hi;
    unsigned long tsb_low;
};


/* Deadman version has to be bumped up, every time there is change in
 * this file
 */
static const char *current_version = DEADMAN_VERSION;

/* 
 * Static variables to be used for jiffies rollover. In RH4 IA32, jiffies 
 * are set MAX jiffies minus 5 minutes so rollover would happen after 
 * 5 minutes and problems with that would be caught earlier. Eventhough 
 * jiffies rollover happens on RH4 IA32 due to difference between 
 * USER_HZ (100) and HZ(1000), deadman would not rollover tsb at the same
 * time.
 */
static struct safety_tsb previous = {0,0};
static unsigned long previous_jiffies = 0;
static unsigned long left_over_jiffies = 0;
static spinlock_t deadman_tsb_lock;

static int userhz = USER_HZ;
static int systemhz = HZ;
static int confighz = 0;
static int platform_info = 0;
static unsigned long disk_size;
static char root_disk_name[512]={0};
static char *root_disk = root_disk_name;
static unsigned int polling_interval=30;
static int root_disk_enabled = 0;

#define DH_SYS_TRUE 1
#define ROOT_DISK_HEALTHY 1
#define ROOT_DISK_FAILED  0
#ifdef DEADMAN_ACPI
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
#define ACPI_RESET_REG_SIZE	((acpi_size)1)	/* ACPI 5.0 section 4.8.3.6 */
static int acpi_reset_init(void);
volatile void *virt_acpi_reset_register=NULL;
#endif
#endif

static struct task_struct *task;
static struct timer_list timer_root_disk;
static struct file *fd;
static struct root_disk_info root_disk_query;
static int flag=0;
static unsigned int root_disk_status = ROOT_DISK_HEALTHY;


static struct file*
file_open(const char* path, int flags, int rights)
{
    struct file* filp = NULL;
    mm_segment_t oldfs = get_fs();
    set_fs(get_ds());
    filp = filp_open(path, flags, rights);
    if (IS_ERR(filp)) {
        printk("ROOT DISK: File open error\n");
        return 0;
    } 
    set_fs(oldfs);
    return filp;
}

static int
file_read(struct file* file, unsigned char* data, unsigned int size, unsigned long offset)
{
    int ret;
#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,14,0)
    ret = kernel_read(file, data, size, (loff_t *)&offset);
#else
    mm_segment_t oldfs = get_fs();
    set_fs(get_ds());
    ret = vfs_read(file, data, size, (loff_t *)&offset);
    set_fs(oldfs);
#endif
    return ret;
}

static void
file_close(struct file* file)
{
   filp_close(file, NULL);
}

/*Getting Random Offset to make sure that read is from the disk each time */
static void
get_random_offset(unsigned long *offset)
{
    int random_byte, positive_random_byte;
    get_random_bytes(&random_byte, 4);
    positive_random_byte = random_byte&0x7FFFFFFF;
    *offset=positive_random_byte % disk_size;
 }
 
static int
root_disk_thread_function(void *data)
{
    char buf[512];
    char filename[512];
    unsigned long offset=0;
    unsigned long aligned_offset;
    int retry_count=0;
    
    strcpy(filename, root_disk);
    fd = file_open(filename,O_RDONLY, 0); /*Open the file*/
    if( fd != 0 ) {
        printk("RDM: Root Disk %s, Disk size %lu\n",root_disk, disk_size );
        while(!kthread_should_stop()) {
            get_random_offset(&offset);
            if ( disk_size > CHUNK ) {
               aligned_offset = offset % (disk_size - CHUNK);
               aligned_offset = (aligned_offset / CHUNK) * CHUNK;
            } else {
               aligned_offset = 0;
            }
            if (file_read(fd, buf, CHUNK, aligned_offset) < 0) {  /*Call the read function*/
                retry_count++;
            } else {
                retry_count=0; 
                /* Advance the timer.*/
                mod_timer(&timer_root_disk, jiffies + ((polling_interval * 3) + (polling_interval / 10)) * confighz);
            }            
            if (retry_count == 3) {
                printk("RDM: Exiting kernel thread \n");
                flag=1;
                file_close(fd);
                do_exit(0);
            } else {
                set_current_state(TASK_INTERRUPTIBLE);
                schedule_timeout(polling_interval*confighz);
            }
        }
    } else {
               flag=1;
               printk(KERN_INFO"RDM: Stopping the thread \n");
                              
    }
    del_timer_sync(&timer_root_disk); /* Deleting the timer */
    file_close(fd);
    do_exit(0);
    return 0;
}

static void
#if LINUX_VERSION_CODE < KERNEL_VERSION(4,18,0)
root_disk_timer_routine(unsigned long data)
#else
root_disk_timer_routine(struct timer_list *t)
#endif
{
    printk(KERN_ALERT"RDM: Timer Expired\n");
    if (root_disk_enabled != 0 ) {
        root_disk_status = ROOT_DISK_FAILED;
    }
}

static void
current_jiffies_to_tsb(struct safety_tsb *tmp)
{
    unsigned long current_jiffies;
    unsigned long delta_jiffies;
    unsigned long delta_ticks;
    unsigned long flags;

#ifdef DEADMAN_SPINLOCK_IRQ_SAVE
    spin_lock_irqsave(&deadman_tsb_lock, flags);
#else
    spin_lock(&deadman_tsb_lock);
#endif

    current_jiffies = jiffies;
    if (current_jiffies >= previous_jiffies) {
        delta_jiffies = (current_jiffies - previous_jiffies) + 
                left_over_jiffies ;
    } else {
        delta_jiffies = current_jiffies + 
            (((unsigned long)-1) - previous_jiffies) +
            left_over_jiffies;
    }

    if (systemhz == userhz) {
        delta_ticks = delta_jiffies;
        left_over_jiffies = 0;
    } else {
        delta_ticks = (delta_jiffies / systemhz) * userhz;
        left_over_jiffies = delta_jiffies % systemhz;
    }

    tmp->tsb_low = previous.tsb_low + delta_ticks;
    tmp->tsb_hi = previous.tsb_hi;
    if (previous.tsb_low > tmp->tsb_low) {
        tmp->tsb_hi++;
    }

    previous_jiffies = current_jiffies;
    previous.tsb_low = tmp->tsb_low;
    previous.tsb_hi = tmp->tsb_hi;
#ifdef DEADMAN_SPINLOCK_IRQ_SAVE
    spin_unlock_irqrestore(&deadman_tsb_lock, flags);
#else
    spin_unlock(&deadman_tsb_lock);
#endif

}

/*
 * deadman_timer is THE kernel timer.
 */

static struct timer_list deadman_timer;

#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    static struct lock_class_key __key;
#endif

/*
 * deadman_enabled is 1 when enabled and 0 when disabled.
 */
static int deadman_enabled = 0;

/*
 * set default value to reboot system when the safety time expires
 */

static char *mode = "reboot";
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,9)
    module_param(mode, charp, 0);
#else
    MODULE_PARM(mode, "s");
#endif
MODULE_PARM_DESC(mode, "Mode for system operation when safety time expires : reboot or panic");

module_param(systemhz, int, 0);
MODULE_PARM_DESC(systemhz, "Kernel HZ Value to be passed while loading the module.");

module_param(platform_info, int, 0);
MODULE_PARM_DESC(platform_info, "Platform specific information to be passed while loading the module.");

module_param(root_disk, charp, 0644);
MODULE_PARM_DESC(root_disk, "Root Disk value to be passed while loading the module.");

module_param(disk_size, ulong, 0644);
MODULE_PARM_DESC(disk_size, "Disk Size value to be passed while loading the module.");

struct proc_dir_entry *deadman_proc_dir = NULL;
struct proc_dir_entry *deadman_proc_info_file = NULL;

static int deadman_get_info(struct seq_file *m, void *v);

static int get_hcf_hz(int firsthz, int secondhz);

/*
 * If the timer expires..
 */
#if LINUX_VERSION_CODE < KERNEL_VERSION(4,18,0)
static void deadman_timer_fire(unsigned long data)
#else
static void deadman_timer_fire(struct timer_list *t)
#endif
{
#ifdef DEADMAN_TESTING
    printk(KERN_EMERG "DEADMAN: Time expired, would restart machine.\n");
    (void)del_timer(&deadman_timer);
    deadman_enabled = 0;
#else

        if (!strcmp(mode, "panic")) {
            printk(KERN_EMERG "DEADMAN: Time expired, initiating system panic.\n");
            panic("PANIC: Timer expired!");
        }
        else {
            printk(KERN_EMERG "DEADMAN: Time expired, initiating system restart.\n");
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,14)
            emergency_restart();
#else
            machine_restart(NULL);
#endif
            printk(KERN_EMERG "DEADMAN: Restart failed!!!\n");
        }

#endif
}

static int deadman_open(struct inode *inode, struct file *file)
{
    return 0;
}

static int deadman_release(struct inode *inode, struct file *file)
{
    return 0;
}


static void deadman_set(struct safety_tsb fire_time)
{

    unsigned long jiffies_fire_time;
    struct safety_tsb current_tsb;
    u64 jif;

    if (systemhz == userhz) {
        jiffies_fire_time = fire_time.tsb_low;
    } else {
         jif = fire_time.tsb_low * (u64) systemhz;
         do_div(jif, userhz);
         jiffies_fire_time = jif;
    }

    current_jiffies_to_tsb(&current_tsb);

    /*
     *      If value if from past then fire deadman timer immediately
     */
    if ((current_tsb.tsb_hi > fire_time.tsb_hi) || 
        ((current_tsb.tsb_hi == fire_time.tsb_hi) && 
         (current_tsb.tsb_low >= fire_time.tsb_low))) {
        printk(KERN_CRIT "DEADMAN: Firing deadman timer. Attempt to set "
               "deadman timer to a time in the past.\n Current time is "
               "(%lu:%lu), attempt to set (%lu:%lu)\n",
               current_tsb.tsb_hi, current_tsb.tsb_low, 
               fire_time.tsb_hi, fire_time.tsb_low);
       deadman_timer_fire(NULL);
    }

    /*
     * Refresh the timer.
     */
    mod_timer(&deadman_timer, jiffies_fire_time);

#ifdef DEADMAN_TESTING
    printk(KERN_CRIT "DEADMAN: Set to %llu\n", 
           (unsigned long long)jiffies_fire_time);
#endif
    return;
}

static int check_user_ids(void)
{
#if LINUX_VERSION_CODE >= KERNEL_VERSION(3,10,0)
    if (!uid_valid(current->cred->uid) && !uid_valid(current->cred->euid)) {
        return -1;
    }
#elif LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    if (current->cred->uid != 0 && current->cred->euid != 0) {
        return -1;
    }
#else
    if (current->uid != 0 && current->euid != 0) {
        return -1;
    }
#endif
    return 0;
}

static void
update_root_disk_info(void)
{
    root_disk_query.polling_interval=polling_interval;
    root_disk_query.root_disk_status=root_disk_status;
    root_disk_query.root_disk_enabled=root_disk_enabled;
 } 
 
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,36)
static long deadman_ioctl(struct file *file,  unsigned int cmd,
                          unsigned long arg)
#else
static int deadman_ioctl(struct inode *inode, struct file *file,
                         unsigned int cmd, unsigned long arg)
#endif
{
    struct safety_tsb tmp;
    
    switch(cmd) {

        case DEADMAN_SYSTEM_REBOOT:
            printk("DEADMAN: Set system to reboot when the safety time expires\n");
            mode = "reboot";
            return 0;

        case DEADMAN_SYSTEM_PANIC:
            printk("DEADMAN: Set system to panic when the safety time expires\n");
            mode = "panic"; 
            return 0;

        case DEADMAN_QUERY_CURRENT:
            current_jiffies_to_tsb(&tmp);
            if (copy_to_user((struct safety_tsb *)arg, &tmp, sizeof(tmp))) {
                return -EFAULT;
            }
            return 0;

        case DEADMAN_ENABLE:
            if (check_user_ids() != 0) {
                return -EPERM;
            }
            
            if (deadman_enabled != 0) {
                printk(KERN_NOTICE "DEADMAN: Attempt to enable while "
                       "already enabled\n"); 
                return -EBUSY;
            }
			
            if (copy_from_user(&tmp, (struct safety_tsb *)arg, sizeof(tmp))) {
                return -EFAULT;
            }
            printk("DEADMAN: Enabled\n");
            deadman_set(tmp);
            deadman_enabled = 1;
            /*
             * Add an additional module reference count to prevent
             * unloading this module while the timer is running even if
             * the caller closes the device
             */
            printk("DEADMAN: Enabled by process %d\n", current->pid);
            return 0;
            
        case DEADMAN_DISABLE:
            if (check_user_ids() != 0) {
                return -EPERM;
            }
            if (deadman_enabled == 0) {
                printk(KERN_NOTICE "DEADMAN: Attempt to disable while "
                       "already disabled\n"); 
                return -EINVAL;
            }
            del_timer(&deadman_timer);
            deadman_enabled = 0;

            printk("DEADMAN: Disabled by process %d\n", current->pid);
            return 0; 

        case DEADMAN_UPDATE:
            if (check_user_ids() != 0) {
                return -EPERM;
            }
            if (deadman_enabled == 0) {
                printk(KERN_NOTICE "DEADMAN: Attempt to update while "
                       "disabled\n"); 
                return -EINVAL;
            }
            if (copy_from_user(&tmp, (struct safety_tsb *) arg, sizeof(tmp))) {
                return -EFAULT;
            }
            deadman_set(tmp);
            return 0;    
            
        case DEADMAN_ROOT_DISK_ENABLE:
            if (check_user_ids() != 0) {
                return -EPERM;
            }
            
            if (root_disk_enabled != 0) {
                printk(KERN_NOTICE "RDM: Attempt to enable while "
                       "already enabled\n"); 
                return -EBUSY;
            }
			
			if( root_disk[0] == '\0' ||  !disk_size) {
                printk("RDM: Invalid root disk parameters, Cannot be enabled. \n");
                return -EINVAL;
            }
			
            if (copy_from_user(&polling_interval, (unsigned int *)arg, sizeof(polling_interval))) {
                return -EFAULT;
            }
#if LINUX_VERSION_CODE < KERNEL_VERSION(4,18,0)
            init_timer(&timer_root_disk);
            timer_root_disk.function = root_disk_timer_routine;
            timer_root_disk.expires = jiffies + ((polling_interval * 3) + (polling_interval / 10)) * confighz;
#else
            timer_root_disk.expires = jiffies + ((polling_interval * 3) + (polling_interval / 10)) * confighz;
            timer_setup(&timer_root_disk, root_disk_timer_routine, 0);
#endif
            add_timer(&timer_root_disk); /* Starting the timer */
            task = kthread_run(root_disk_thread_function,NULL,"rootdisk_thread"); /*creation of thread */
            if (task) {
                printk("RDM: Kernel Thread %s created successfully.\n", task->comm);
                root_disk_enabled = 1;
                printk("RDM: Enabled by process %d\n", current->pid);
                flag=0;
            } else {
                printk(KERN_ERR "RDM: Kernel Thread Creation failed\n");
                root_disk_enabled = 0;
                del_timer_sync(&timer_root_disk); /* Deleting the timer */
                return -EFAULT;
            }
			return 0;
                    
        case DEADMAN_ROOT_DISK_DISABLE:
            if (check_user_ids() != 0) {
                return -EPERM;
            }
            if (root_disk_enabled == 0) {
                printk("RDM: Attempt to disable while "
                       "already disabled\n"); 
                return -EINVAL;
            }
            root_disk_enabled = 0;
            if (flag != 1) {
                if (task) {
                    kthread_stop(task);
                    printk("RDM: Thread stopped successfully by process %d\n",current->pid);
                }
            } else {
                printk("RDM: Thread is already stopped\n");
            }
            return 0;    
       
         case DEADMAN_ROOT_DISK_QUERY:
            update_root_disk_info();
            if (copy_to_user((struct root_disk_info *)arg, &root_disk_query, sizeof(root_disk_query))) {
                return -EFAULT;
            }
            return 0;
            
        default:
            return -ENOIOCTLCMD;
    } /* switch on command */
} /* deadman_ioctl() */

static struct file_operations deadman_fops =
{
    owner:          THIS_MODULE,
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,36)
    unlocked_ioctl: deadman_ioctl,
#else
    ioctl:          deadman_ioctl,
#endif
    open:           deadman_open,
    release:        deadman_release
};

static struct miscdevice deadman_miscdev =
{
     MISC_DYNAMIC_MINOR,
    "deadman",
    &deadman_fops
};

static int deadman_info_open(struct inode *inode, struct file *file)
{
    return single_open(file, deadman_get_info, NULL);
}

static const struct file_operations deadman_info_fops = {
        .owner          = THIS_MODULE,
        .open           = deadman_info_open,
	.read		= seq_read,
	.llseek		= seq_lseek,
	.release	= seq_release,
};

static int deadman_get_info(struct seq_file *m, void *v)
{
   seq_printf(m, "Deadman Enabled: ");
   if (deadman_enabled) {
        seq_printf(m, "Yes\n");
    } else {
        seq_printf(m, "No\n");
    }
    seq_printf(m, "Deadman Mode: %s\n", mode);
    seq_printf(m, "CONFIG_HZ: %d\n", confighz);
    seq_printf(m, "Root Disk Name: %s\nRoot Disk Size: %lu(bytes)\n", root_disk,
                                                               disk_size);
    return 0;
}

static int get_hcf_hz(int firsthz, int secondhz)
{
   int temp;
   while (secondhz != 0) {
       temp = secondhz;
       secondhz = firsthz % secondhz;
       firsthz = temp;
   }
   return firsthz;
}
 
int __init deadman_init(void)
{
    int hcf;

    if (userhz > systemhz) {
        printk(KERN_NOTICE "DEADMAN: Cannot insert the module when USER_HZ "
               "value is greater than kernel HZ.\n");
        return -EPERM;
    } else if (systemhz > 1000 ) {
        printk(KERN_NOTICE "DEADMAN: Cannot insert the module for untested "
               "frequencies of kernel HZ.\n");
        return -EPERM;
    }

    misc_register(&deadman_miscdev);
#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,18,0)
    init_timer_key(&deadman_timer, NULL, 0, "deadman_timer", &__key);
#elif LINUX_VERSION_CODE >= KERNEL_VERSION(3,10,0)
    init_timer_key(&deadman_timer, 0, "deadman_timer", &__key);
#elif LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    init_timer_key(&deadman_timer, "deadman_timer", &__key);
#else
    init_timer(&deadman_timer);
#endif
    deadman_timer.function = deadman_timer_fire;

    /* Calculate the HCF of USER_HZ and HZ values. 
     * Divide USER_HZ and HZ values with their HCF, which will be used for
     * delta_ticks and left_over_jiffies calculation.
     */
    confighz = systemhz;
    hcf = get_hcf_hz(systemhz, userhz);
    systemhz = systemhz/hcf;
    userhz = userhz/hcf;
    spin_lock_init(&deadman_tsb_lock);
    printk("Deadman: %s minor: %i\n", current_version,
            deadman_miscdev.minor);
        if (mode) {
            if (!(strcmp(mode, "panic"))) {
                printk("DEADMAN: System is set to panic when the safety time expires\n");
            } else {
                printk("DEADMAN: System is set to reboot when the safety time expires\n");
            }
        }

#ifdef CONFIG_PROC_FS
    deadman_proc_dir = proc_mkdir("deadman", NULL);
    if (deadman_proc_dir == NULL) {
        printk(KERN_ERR 
            "DEADMAN: Cannot init /proc/deadman directory\n");
        return -ENOMEM;
    }

#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    deadman_proc_info_file =
        proc_create_data("info", 0, deadman_proc_dir,
                      &deadman_info_fops, NULL);
#else
    deadman_proc_info_file =
        proc_create("info", 0, deadman_proc_dir,
                      &deadman_info_fops);
#endif
 
    if (deadman_proc_info_file == NULL) {
        printk(KERN_ERR "DEADMAN: Cannot init /proc/deadman/info\n");
        remove_proc_entry("deadman", NULL);
        return -ENOMEM;
    }
#endif /* CONFIG_PROC_FS */
#ifdef DEADMAN_ACPI
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    if (DH_SYS_TRUE == platform_info) 
    {
        /* When loading deadman module, we ignore errors other than 
         * AE_NO_MEMORY because other errors mainly indicate that
         * either is ACPI register is already mapped or ACPI reset
         * register is not supported. Assumptions is on platforms
         * which return errors other than AE_MEMORY would not 
         * face the issue due calling emergency_restart() function 
         * from interrupt context.
         */ 

        if (AE_NO_MEMORY == acpi_reset_init())
        {
            remove_proc_entry("deadman", NULL);
            return -ENOMEM;
        }
    }
#endif
#endif
    return 0;
}

void deadman_cleanup(void)
{
#ifdef CONFIG_PROC_FS
        remove_proc_entry("info", deadman_proc_dir);
        remove_proc_entry("deadman", NULL);
#endif /* CONFIG_PROC_FS */
#ifdef DEADMAN_ACPI
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
    if ((DH_SYS_TRUE == platform_info) && NULL != virt_acpi_reset_register) 
    {
        acpi_os_unmap_memory((void *)virt_acpi_reset_register,
                             ACPI_RESET_REG_SIZE);
    }
#endif
#endif
    misc_deregister(&deadman_miscdev);
    if (root_disk_enabled) {
       if (task) {
           kthread_stop(task);
           printk("RDM: Thread stopped successfully \n");
        }  
       del_timer_sync(&timer_root_disk); /* Deleting the timer */       
    }    
    
}
#ifdef DEADMAN_ACPI
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,32)
static int acpi_reset_init(void) 
{
    struct acpi_generic_address *reset_reg;
    acpi_physical_address phys_addr;
    acpi_size size;
    volatile void *virt_addr;
        
    printk("DEADMAN: ACPI reset init called\n");

    reset_reg = &acpi_gbl_FADT.reset_register;

    /* Check if the reset register is supported */

    if (!(acpi_gbl_FADT.flags & ACPI_FADT_RESET_REGISTER) ||
          !reset_reg->address) {
        printk("DEADMAN: no reset register\n");
        return AE_SUPPORT;
    }

    if (reset_reg->space_id != ACPI_ADR_SPACE_SYSTEM_MEMORY) {
        printk("DEADMAN: reset register not in system_memory\n");
        return AE_ALREADY_ACQUIRED;
    }

    phys_addr =  (acpi_physical_address)reset_reg->address;
    size = reset_reg->access_width;
    WARN_ON(size != ACPI_RESET_REG_SIZE);

    virt_addr = acpi_os_map_memory(phys_addr, size);
    if (!virt_addr) {
        printk("DEADMAN: acpi_os_map_memory failed\n");
        return AE_NO_MEMORY;
    }
    virt_acpi_reset_register = virt_addr;

    return AE_OK;

}
#endif
#endif
module_init(deadman_init);
module_exit(deadman_cleanup);

