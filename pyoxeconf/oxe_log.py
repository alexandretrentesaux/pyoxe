# -*- encoding: utf-8 -*-

"""Summary
"""
from pprint import pprint
import scp
from os.path import join, exists
from os import remove
from tempfile import gettempdir


def oxe_log_sh(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    with open('resources/oxe-log.sh', 'r+', encoding='utf-8') as template:
        with open(join(gettempdir(), 'oxe-log.sh'), 'w+', encoding='utf-8') as result:
            for line in template:
                if '127.0.0.1' in line:
                    result.write(line.replace('127.0.0.1', host))
                else:
                    result.write(line)
    client = scp.Client(host=host, port=port, user='mtcl', password=password)
    client.transfer(join(gettempdir(), 'oxe-log.sh'), '/DHS3bin/mtcl/oxe-log.sh')
    if exists(join(gettempdir(), 'oxe-log.sh')):
        remove(join(gettempdir(), 'oxe-log.sh'))
    # sur l'OXE pour
    #   mkdir -p /DHS3bin/mtcl/tests
    #   su -
    #   chmod a+x /usr/sbin/tcpdump
    #   exit
    #   exit


def start_log(host, password, test_name):
    """Summary
    
    Args:
        host (TYPE): Description
        password (TYPE): Description
        test_name (TYPE): Description
    """
    pprint('todo\n')
    # connect OXE
    # source /DHS3bin/mtcl/oxe-log.sh
    # set-log <test_name>


def stop_log(host, password, test_name):
    """Summary
    
    Args:
        host (TYPE): Description
        password (TYPE): Description
        test_name (TYPE): Description
    """
    pprint('todo\n')
    # stop-log
