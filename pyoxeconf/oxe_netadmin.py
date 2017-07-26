""" OXE connection methods """
import paramiko
import time
import re
import pprint


def oxe_netdata_update(host, data, port=22, password='mtcl', root_password='letacla'):
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        time.sleep(3)  # OXE is really slow on mtcl connexion
    stdout = channel.recv(4096)
    channel.send('su -\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.send(root_password + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.send('cat >> /usr/netadm/data/netdata << EOF\n' + data + '\nEOF\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.send('netadmin -c\n')
    while channel.recv_ready() is False:
        time.sleep(2)
    stdout += channel.recv(1024)
    channel.send('chmod 664 /usr/netadm/data/netdata\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


def oxe_netdata_get(host, pattern, port=22, password='mtcl'):
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    # stdout, stdin, stderr = client.exec_command('sed -n -e \'s/^' + pattern + '=\([^;][^;]*\).*/\\1/p\'  -e \'s/.*;' +
    #                                            pattern + '=\([^;][^;]*\).*/\\1/p\' /usr/netadm/data/netdata\n')
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        time.sleep(3)  # OXE is really slow on mtcl connexion
    stdout = channel.recv(4096)
    channel.send('cat /usr/netadm/data/netdata\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout = channel.recv(4096)
    channel.close()
    client.close()
    find = re.compile(pattern + '=.*').findall(stdout.decode('utf-8'))[0].split('=')[1]
    return find
