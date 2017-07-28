#!/bin/sh

pyoxeconf_cli connect --host 10.100.8.11
pyoxeconf_cli sippCreateCsv --rangeStart 70000 --rangeSize 2000 --ip 10.100.8.11
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.16
pyoxeconf_cli sippCreateCsv --rangeStart 70000 --rangeSize 5000 --ip 10.100.8.16
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.18
pyoxeconf_cli sippCreateCsv --rangeStart 70000 --rangeSize 10000 --ip 10.100.8.18
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.15
pyoxeconf_cli sippCreateCsv --rangeStart 70000 --rangeSize 500 --ip 10.100.8.15
pyoxeconf_cli logout
