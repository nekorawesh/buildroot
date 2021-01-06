#!/bin/sh

PART_STATUS=$(sgdisk -A 2:get:2 /dev/mmcblk1)
if test "${PART_STATUS}" = "2:2:1" ; then
	NEXT_ROOTFS=/dev/mmcblk1p3
else
	NEXT_ROOTFS=/dev/mmcblk1p2
fi

# Add update marker
mount ${NEXT_ROOTFS} /mnt
touch /mnt/update-ok
umount /mnt

sgdisk -A 2:toggle:2 -A 3:toggle:2 /dev/mmcblk1
reboot