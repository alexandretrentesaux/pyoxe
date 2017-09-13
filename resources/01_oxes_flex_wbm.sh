#!/bin/sh

for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	echo "begin config OXE"$i
	pyoxeconf_cli connect --host 10.100.8.$i
	sleep 0.5
	echo "--> wbm limits"
	pyoxeconf_cli wbmRequestsLimit --host 10.100.8.$i
	echo "--> set flex"
	pyoxeconf_cli setFlexServer --host 10.100.8.$i --flexIp 10.100.8.3 --reboot
	pyoxeconf_cli logout --host 10.100.8.$i
done