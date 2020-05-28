#!/bin/sh

PART_STATUS=$(sgdisk -A 4:get:2 /dev/mmcblk0)
if test "${PART_STATUS}" = "4:2:1" ; then
	NEXT_ROOTFS=/dev/mmcblk0p5
else
	NEXT_ROOTFS=/dev/mmcblk0p4
fi

# Add update marker
mount ${NEXT_ROOTFS} /mnt
touch /mnt/update-ok
umount /mnt

sgdisk -A 4:toggle:2 -A 5:toggle:2 /dev/mmcblk0
reboot
