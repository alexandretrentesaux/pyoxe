# -*- encoding: utf-8 -*-

"""Summary
"""
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from time import sleep


def oxe_reboot(host, port, password, swinst_password):
    """Reboot OXE Call Server
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        swinst_password (TYPE): Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
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
    channel.send('reboot\n')
    while channel.recv_ready() is False:
        sleep(1)
    stdout += channel.recv(1024)
    channel.send(swinst_password + '\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    # pprint.pprint(stdout)
    channel.close()
    client.close()


def oxe_kill_rainbow_agent(host, port, password, root_password):
    """Kill rainbow agent
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        root_password (TYPE): Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
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
    channel.send('rainbowagent -k\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    # pprint.pprint(stdout)
    channel.close()
    client.close()


def oxe_runmao(host, port, password):
    """RUNMAO to provision configuration without starting telephone
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command('RUNMAO\n')
    client.close()


def oxe_runtel(host, port, password):
    """RUNTEL start telephone
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command('RUNTEL\n')
    client.close()
