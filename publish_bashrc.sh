#!/bin/bash

homerc=$HOME/.bashrc

if [[ -L $homerc ]]; then
	echo "removing existing symlink..."
	unlink $homerc
fi

if [[ -f $homerc ]]; then
	echo "deleting exiting .bashrc..."
	mv $homerc $homerc.orig
fi

ln -s $HOME/.scripts/bashrc $homerc
source $homerc
