#! /bin/bash

# AUTHOR: Remy Tomasetto

#############################################
#### Mofication #############################
#############################################

# Modify the Path for logs storage
LOG_REPOSITORY=/DHS3bin/mtcl/tests/

# Modify OXE's IP 
OXE_IP=127.0.0.1

#############################################
##### No modification beyond this line ######
#############################################

while getopts :h OPT; do
    case $OPT in
        h|+h)
            echo "That's some help !"
            ;;
        *)
            echo "usage: ${0##*/} [+-h} [--] ARGS..."
            exit 2
    esac
done
shift $(( OPTIND - 1 ))
OPTIND=1



function set-log ()
{
    echo "set-log : $1"
	echo "LOG_REPOSITORY : $LOG_REPOSITORY"
	echo "OXE_IP : $OXE_IP"
    mkdir -p $LOG_REPOSITORY/$1
    actdbg all=off sip=on abcf=on fct=on isdn=on
    tuner all=off cpl cpu at tr s hybrid=on
    mtracer -ag -d -1 $LOG_REPOSITORY/$1/$1-sip -s 1000000 -f2
    motortrace 3
    traced -d -1 $LOG_REPOSITORY/$1/$1-motor -s 1000000 -f2
    tcpdump -w$LOG_REPOSITORY/$1/$1.pcap -s1500 ip host $OXE_IP &
}


function stop-log ()
{
    actdbg all=off
    tuner all=off
    tuner km
    killall traced
    killall tcpdump
}

