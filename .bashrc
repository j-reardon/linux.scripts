#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias ll='ls -l'
alias la='ll -a'
PS1='[\u@\h \W]\$ '

alias grepps='ps aux | grep'
alias catbash='cat ~/.bashrc'

alias shutdown='shutdown -h now'

# sudo aliases and functions
alias scp='sudo cp'
svim()
{
	if [ ! -f "$1.orig" ]; then
		scp $1 "$1.orig"
	fi
	sudo vim $1
}

# pacman aliases
alias pac-update='sudo pacman -Su'
alias pac-install='sudo pacman -S'
alias pac-uninstall='sudo pacman -Rs'
alias pac-search='pacman -Qs'
alias pac-list='pacman -Qe'
alias pac-listorphans='pacman -Qtdq'
alias pac-removeorphans='pacman -Rns $(pacman -Qtdq)'
alias aur-sync='python ~/.scripts/aur/aur-update-checker.py'

aur-install()
{
	aur="$HOME/.scripts/aur"
	python -c "import sys; sys.path.append('$aur'); import aur; aur.install('$1')" 
}

aur-update()
{
	aur="$HOME/.scripts/aur"
	python -c "import sys; sys.path.append('$aur'); import aur; aur.update('$1')"
}

aur-get()
{
	aur="$HOME/.scripts/aur"
	python -c "import sys; sys.path.append('$aur'); import aur; aur.clone('$1')"
}

pac-sync()
{
	sudo pacman -Syy
	pacman -Qu
	python ~/.scripts/aur/aur-update-checker.py
}

pac-listsize()
{
    pacman -Qi | awk '/^Name/{name=$3} /^Installed Size/{print $4$5, name}' | sort -h
}

edit-rc()
{
	vim ~/.bashrc
	source ~/.bashrc
}
