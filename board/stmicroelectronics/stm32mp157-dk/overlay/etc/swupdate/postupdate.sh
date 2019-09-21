#!/bin/sh
sgdisk -A 4:toggle:2 -A 5:toggle:2 /dev/mmcblk0
reboot
