#!/bin/sh

pyoxeconf_cli connect --host 10.100.8.16
pyoxeconf_cli rainbowDisconnect
pyoxeconf_cli updateCccaCfg --ip 10.100.8.16 --apiserver agent-fabien.openrainbow.org
pyoxeconf_cli rainbowConnect --ini --filename OXE2.ini
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.18
pyoxeconf_cli rainbowDisconnect
pyoxeconf_cli updateCccaCfg --ip 10.100.8.18 --apiserver agent-fabien.openrainbow.org
pyoxeconf_cli rainbowConnect --ini --filename OXE3.ini
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.15
pyoxeconf_cli rainbowDisconnect
pyoxeconf_cli updateCccaCfg --ip 10.100.8.18 --apiserver agent-fabien.openrainbow.org
pyoxeconf_cli rainbowConnect --ini --filename OXE4.ini
pyoxeconf_cli logout


