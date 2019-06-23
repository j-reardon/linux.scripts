#!/bin/bash

if [[ -f $HOME/.bashrc ]]; then
	rm $HOME/.bashrc
fi

ln -s $HOME/.scripts/bashrc $HOME/.bashrc
source $HOME/.bashrc
