#!/bin/bash
tsundere_word="butiluvu"

echo "FUCK YOU TOO!!!"

if [ $# -ne 0 ] ; then
	if [ $1$2$3$4 = $tsundere_word ] ; then
	echo "..."
	sudo shutdown -r now
	fi
else
	sudo shutdown -h now
fi

