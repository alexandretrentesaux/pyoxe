"""Summary"""
import pprint
import scp
import os
import tempfile


def oxe_log_sh(host, password):
    with open('resources/oxe-log.sh', 'r+', encoding='utf-8') as template:
        with open(os.path.join(tempfile.gettempdir(), 'oxe-log.sh'), 'w+', encoding='utf-8') as result:
            for line in template:
                if '127.0.0.1' in line:
                    result.write(line.replace('127.0.0.1', host))
                else:
                    result.write(line)
    client = scp.Client(host=host, user='mtcl', password=password)
    client.transfer(os.path.join(tempfile.gettempdir(), 'oxe-log.sh'), '/DHS3bin/mtcl/oxe-log.sh')
    if os.path.exists(os.path.join(tempfile.gettempdir(), 'oxe-log.sh')):
        os.remove(os.path.join(tempfile.gettempdir(), 'oxe-log.sh'))
    # sur l'OXE pour
    #   mkdir -p /DHS3bin/mtcl/tests
    #   su -
    #   chmod a+x /usr/sbin/tcpdump
    #   logout
    #   logout


def start_log(host, password, test_name):
    pprint.pprint('todo\n')
    # connect OXE
    # source /DHS3bin/mtcl/oxe-log.sh
    # set-log <test_name>


def stop_log(host, password, test_name):
    pprint.pprint('todo\n')
    # stop-log