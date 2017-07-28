#!/bin/sh

pyoxeconf_cli connect --host 10.100.8.11
pyoxeconf_cli rainbowReconnect --ini --filename OXE1.ini
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.16
pyoxeconf_cli rainbowReconnect --ini --filename OXE2.ini
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.18
pyoxeconf_cli rainbowReconnect --ini --filename OXE3.ini
pyoxeconf_cli logout

pyoxeconf_cli connect --host 10.100.8.15
pyoxeconf_cli rainbowReconnect --ini --filename OXE4.ini
pyoxeconf_cli logout
