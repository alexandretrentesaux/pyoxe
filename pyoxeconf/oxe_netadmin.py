# -*- encoding: utf-8 -*-

"""OXE connection methods 
"""
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from time import sleep
from re import compile



def oxe_netdata_update(host, data, port=22, password='mtcl', root_password='letacla'):
    """Summary
    
    Args:
        host (TYPE): Description
        data (TYPE): Description
        port (int, optional): Description
        password (str, optional): Description
        root_password (str, optional): Description
    """
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        sleep(3)  # OXE is really slow on mtcl connexion
    stdout = channel.recv(4096)
    channel.send('su -\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    channel.send(root_password + '\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    channel.send('cat >> /usr/netadm/data/netdata << EOF\n' + data + '\nEOF\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    channel.send('netadmin -c\n')
    while channel.recv_ready() is False:
        sleep(2)
    stdout += channel.recv(1024)
    channel.send('chmod 664 /usr/netadm/data/netdata\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


def oxe_netdata_get(host, pattern, port=22, password='mtcl'):
    """Summary
    
    Args:
        host (TYPE): Description
        pattern (TYPE): Description
        port (int, optional): Description
        password (str, optional): Description
    
    Returns:
        TYPE: Description
    """
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    # stdout, stdin, stderr = client.exec_command('sed -n -e \'s/^' + pattern + '=\([^;][^;]*\).*/\\1/p\'  -e \'s/.*;' +
    #                                            pattern + '=\([^;][^;]*\).*/\\1/p\' /usr/netadm/data/netdata\n')
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        sleep(3)  # OXE is really slow on mtcl connexion
    stdout = channel.recv(4096)
    channel.send('cat /usr/netadm/data/netdata\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout = channel.recv(4096)
    channel.close()
    client.close()
    find = compile(pattern + '=.*').findall(stdout.decode('utf-8'))[0].split('=')[1]
    return find
