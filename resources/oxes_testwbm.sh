for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
do
	echo "--> test wbm OXE 10.100.8."$i
	curl "https://10.100.8."$i"/api/mgt/1.0/login" --insecure
done