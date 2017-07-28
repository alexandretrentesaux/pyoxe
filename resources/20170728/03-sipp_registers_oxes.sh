#!/bin/sh

sipp 10.100.8.11 -sf /home/alexantr/Workspace/pyoxeconf/resources/sipp_uac_register.xml -inf /tmp/zsh-1000/10.100.8.11_2000users -m 2000
sipp 10.100.8.16 -sf /home/alexantr/Workspace/pyoxeconf/resources/sipp_uac_register.xml -inf /tmp/zsh-1000/10.100.8.16_5000users -m 5000
sipp 10.100.8.15 -sf /home/alexantr/Workspace/pyoxeconf/resources/sipp_uac_register.xml -inf /tmp/zsh-1000/10.100.8.15_500users -m 500
sipp 10.100.8.18 -sf /home/alexantr/Workspace/pyoxeconf/resources/sipp_uac_register.xml -inf /tmp/zsh-1000/10.100.8.18_10000users -m 10000

