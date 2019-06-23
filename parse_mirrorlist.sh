#!/bin/bash

awk 'f{print} /^## United States$/{f=1}' /etc/pacman.d/mirrorlist.pacnew > /etc/pacman.d/mirrorlist.working
sed -i 's/^#Server/Server/' mirrorlist.working
rankmirrors -n 6 /etc/pacman.d/mirrorlist.working > /etc/pacman.d/mirrorlist
