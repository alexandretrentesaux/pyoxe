""" OXE connection methods """
import paramiko
import time


# set DNS
def oxe_netadmin_dns(host, dns1, dns2, port=22, password='mtcl', root_password='letacla'):
    dns_config = 'DNSPRIMADDR=' + dns1 + '\nDNSSECADDR=' + dns2
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
    channel.send('cat >> /usr/netadm/data/netdata << EOF\n' + dns_config + '\nEOF\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    channel.send('netadmin -c\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


# set http/https proxy
# proxy data
# {'address': proxy IP@, 'port': proxy port, 'login': login, }
def oxe_netadmin_proxies(host, proxy, port=22, password='mtcl', root_password='letacla'):
    proxy_config = 'PROXYADDR=' + proxy['address'] + '\nPROXYPORT=' + proxy['port']
    if proxy['login'] is not None:
        proxy_config += '\nPROXYUSER=' + proxy['login']
    if proxy['password'] is not None:
        proxy_config += '\nPROXYPASSWD=' + proxy['password']
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
    channel.send('cat >> /usr/netadm/data/netdata << EOF\n' + proxy_config + '\nEOF\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    channel.send('netadmin -c\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


# enable SSHv2
def oxe_netadmin_sshv2_enable():
    # update /usr/netadm/data/netdata
    # load modification with netdata -c
    print('todo\n')
