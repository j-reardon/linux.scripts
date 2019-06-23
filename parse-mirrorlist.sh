#!/bin/bash

base_dir=/etc/pacman.d
mirrorlist=$basdir/mirrorlist
working=$mirrorlist.working
pacnew=$mirrorlist.pacnew

country="US"

pacman -Qs pacman-contrib > /dev/null
if [[ $? -eq 1 ]]; then
	pacman -S pacman-contrib
fi

if [[ ! -f /etc/pacman.d/mirrorlist.pacnew ]]; then
	curl -s "https://www.archlinux.org/mirrorlist/?country=$country&protocol=https&user_mirror_status=on" > $working
else 
	awk 'f{print} /^## United States$/{f=1}' $pacnew > $working
fi

sed -i 's/^#Server/Server/' $working
rankmirrors -n 6 $working > $mirrorlist

if [[ $? -eq 1 ]]; then
	cp $working $mirrorlist
fi
