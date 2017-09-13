for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	pyoxeconf_cli connect --host 10.100.8.$i
	pyoxeconf_cli rainbowDisconnect --host 10.100.8.$i
	pyoxeconf_cli purgeCccaCfg --host 10.100.8.$i
	pyoxeconf_cli purgeRainbowagentLogs --host 10.100.8.$i
	pyoxeconf_cli logout --host 10.100.8.$i
done
