#!/bin/sh

for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	echo "begin config OXE"$i
	pyoxeconf_cli connect --host 10.100.8.$i
	echo "--> create shelf"
	pyoxeconf_cli createShelf --host 10.100.8.$i
	pyoxeconf_cli setOmsCompressors --host 10.100.8.$i
	echo "--> enable sip"
	pyoxeconf_cli enableSip --host 10.100.8.$i
	echo "--> create DPNSS"
	pyoxeconf_cli createDpnssPrefix --host 10.100.8.$i
	echo "--> enable UCAAS csta monitored session"
	pyoxeconf_cli enableUcaasCstaMonitored --host 10.100.8.$i
	pyoxeconf_cli logout --host 10.100.8.$i
done
