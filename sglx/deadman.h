/*
 * (c) Copyright 2009-2019 Hewlett Packard Enterprise Development LP. 
 *      http://www.hpe.com
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version
 * 2 of the License, or (at your option) any later version.
 * 
 * Neither Eric Soderberg or Hewlett-Packard Enterprise admit 
 * liability nor provide warranty for any of this software. This 
 * material is provided "AS-IS" and at no charge.
 *
 */

#ifndef _DEADMAN_INCLUDED /* allows multiple inclusion */
#define _DEADMAN_INCLUDED 

#ifdef __KERNEL__
#include <linux/ioctl.h>
#include <linux/time.h>
#else
#include <sys/ioctl.h>
#include <time.h>
#endif

/*
 * DEADMAN_ROOT_DISK_QUERY returns the root_disk_info structure.
 */

struct root_disk_info {
    unsigned int polling_interval;
    unsigned int root_disk_status;
    unsigned int root_disk_enabled;
};


#define CHUNK  512

#define DEADMAN_IOCTL_BASE  'W'

/*
 * DEADMAN_QUERY_CURRENT returns the amount of time that has elapsed
 * since the system was booted (converts jiffies to timespec).
 * Any user can call this.
 */
#define DEADMAN_QUERY_CURRENT _IOR(DEADMAN_IOCTL_BASE, 0x30, struct timespec)
/*
 * DEADMAN_ENABLE turns on the deadman timer which will expire at the
 * specified time.
 * The process calling this must be owned by root.
 * EBUSY is reported if it is already enabled.
 * EPERM is reported if the caller is not the root user.
 */
#define DEADMAN_ENABLE _IOW(DEADMAN_IOCTL_BASE, 0x31, struct timespec)
/*
 * DEADMAN_DISABLE turns off the deadman timer.
 * The process calling this must be owned by root.
 * EINVAL is reported if it is not enabled.
 * EPERM is reported if the caller is not the root user.
 */
#define DEADMAN_DISABLE _IO(DEADMAN_IOCTL_BASE, 0x32)

/*
 * DEADMAN_UPDATE advances the expiration time of the deadman timer.
 * The process calling this must be owned by root.
 * EINVAL is reported and no action is taken if the deadman timer is
 * not enabled.
 * EPERM is reported if the caller is not the root user.
 */
#define DEADMAN_UPDATE _IOW(DEADMAN_IOCTL_BASE, 0x33, struct timespec)

/*
 * DEADMAN_SYSTEM_REBOOT & DEADMAN_SYSTEM_PANIC flags allow system either to
 * reboot or to halt when its safety time expires.
 */
#define DEADMAN_SYSTEM_REBOOT _IOW(DEADMAN_IOCTL_BASE, 0x34, struct timespec)
#define DEADMAN_SYSTEM_PANIC _IOW(DEADMAN_IOCTL_BASE, 0x35, struct timespec)

/*
 * DEADMAN_ROOT_DISK_QUERY queries the root disk status.
 * DEADMAN_ROOT_DISK_ENABLE enables the root disk monitoring.
 * DEADMAN_ROOT_DISK_DISABLE disables the root disk monitoring.
  */
#define DEADMAN_ROOT_DISK_QUERY   _IOR(DEADMAN_IOCTL_BASE, 0x36, struct root_disk_info)
#define DEADMAN_ROOT_DISK_ENABLE  _IOW(DEADMAN_IOCTL_BASE, 0x37, uint)
#define DEADMAN_ROOT_DISK_DISABLE _IO(DEADMAN_IOCTL_BASE, 0x38)

#define DEADMAN_VERSION "2.28"

#endif /* _DEADMAN_INCLUDED */
