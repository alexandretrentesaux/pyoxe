for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	echo "begin users provisioning OXE"$i
	pyoxeconf_cli connect --host 10.100.8.$i
	pyoxeconf_cli createUsers --host 10.100.8.$i --rangeSize=250 --rangeStart=70000 --setType "SIP_Extension"
	pyoxeconf_cli createUsers --host 10.100.8.$i --rangeSize=250 --rangeStart=80000 --setType "UA_VIRTUAL"
	pyoxeconf_cli createUsers --host 10.100.8.$i --rangeSize=2 --rangeStart=65000 --setType "NOE_C_IP"
	pyoxeconf_cli logout --host 10.100.8.$i
done
