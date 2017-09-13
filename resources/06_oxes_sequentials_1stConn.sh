#!/usr/bin/env bash

#!/bin/sh

for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	echo 'proceeding oxe ip 10.100.8.'$i
	pyoxeconf_cli connect --host 10.100.8.$i
	pyoxeconf_cli updateCccaCfg --host 10.100.8.$i --apiServer agent-fabien.openrainbow.org
	j=$((i-9))
	pyoxeconf_cli rainbowConnect --host 10.100.8.$i --ini --filename 'OXE'$j'.ini'
	pyoxeconf_cli logout --host 10.100.8.$i
	sleep 300
    pyoxeconf_cli connect --host 10.100.8.$i
	pyoxeconf_cli rainbowDisconnect --host 10.100.8.$i
	pyoxeconf_cli purgeCccaCfg --host 10.100.8.$i
	pyoxeconf_cli purgeRainbowagentLogs --host 10.100.8.$i
	pyoxeconf_cli logout --host 10.100.8.$i
done

