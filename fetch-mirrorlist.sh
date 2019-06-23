#!/bin/bash

curl -s "https://www.archlinux.org/mirrorlist/?country=US&protocol=https&user_mirror_status=on" > /etc/pacman.d/mirrorlist.pacnew
