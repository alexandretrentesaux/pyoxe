""" OXE connection methods """
import configparser
import pprint
import requests
import requests.packages
import sys
import os
import json
import paramiko
import time
import tempfile


# create connection config file
def oxe_configure(host, login, password, proxies):
    """Create config file with OXE connection parameters

    Args:
        host (str): OXE IP or FQDN
        login (str): mtcl user
        password (str): Description
        proxies (json): Description
    """
    config = configparser.RawConfigParser()
    config.add_section('default')
    config.set('default', 'host', str(host))
    config.set('default', 'login', str(login))
    config.set('default', 'password', str(password))
    if proxies is not None:
        config.add_section('proxies')
        config.set('proxies', 'proxies', proxies)
    with open(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_oxe.ini'), 'w+') as config_file:
        config.write(config_file)
    os.chmod(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_oxe.ini'), 0o600)


# get connection info from config file
def oxe_get_config():
    """Summary

    Returns:
        TYPE: Description
    """
    config = configparser.ConfigParser()
    config.read(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_oxe.ini'))
    oxe_ip = config.get('default', 'host', raw=False)
    login = config.get('default', 'login', raw=False)
    password = config.get('default', 'password', raw=False)
    if config.has_section('proxies'):
        proxies = config.get('proxies', 'proxies', raw=True)
    else:
        proxies = None
    return oxe_ip, login, password, proxies


# store authentication token
def oxe_get_auth_from_cache():
    """Summary

    Returns:
        TYPE: Description
    """
    try:
        with open(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_auth')) as fh:
            tmp = json.loads(fh.read())
            token = tmp['token']
            ip_address = tmp['oxe_ip']
            return token, ip_address
        os.chmod(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_auth', 0o600))
    except IOError:
        print('Please login to go on !!!')
        exit(1)


# build header
def oxe_set_headers(token, method=None):
    """Summary

    Args:
        token (TYPE): Description
        method (None, optional): Description

    Returns:
        TYPE: Description
    """
    # basic method GET
    headers = {
        'Authorization': 'Bearer ' + token,
        'accept': 'application/json'
    }
    # addition for POST & PUT
    if method in ('POST', 'PUT'):
        headers.update({'Content-Type': 'application/json'})
    elif method == 'DELETE':
        headers.update({'Content-Type': 'text/plain'})
    return headers


# OXE WBM authentication + JWT cache creation
def oxe_authenticate(host, login, password, proxies=None):
    """Summary

    Args:
        host (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description
        proxies (None, optional): Description

    Returns:sed -i -e 's/zone=two\:1m rate\=2r\/s/zone=two\:1m rate\=50r\/s/g' /usr/local/openresty/nginx/conf/wbm.conf
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    authentication = requests.get('https://' + host + '/api/mgt/1.0/login',
                                  timeout=10,
                                  auth=(login, password),
                                  verify=False,
                                  proxies=proxies)
    if authentication.status_code == 401:
        print('Error {} - {}'.format(authentication.json()['errorCode'],
                                     authentication.json()['errorMsg']))
        sys.exit(-1)
    elif authentication.status_code == 000:
        print('Error {} - telephony is not running on OXE / WBM not available'.format(authentication.status_code))
        sys.exit(-1)
    data = {'oxe_ip': host, 'token': authentication.json()['token']}
    with open(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_auth'), 'w') as fh:
        fh.write(json.dumps(data))
    return authentication.json()


# OXE WBM logout + clear JWT cache
def oxe_logout():
    """Summary

    Args:

    Returns:
    """
    # clear cache
    try:
        os.remove(os.path.join(tempfile.gettempdir(), '.pyoxeconfgen_auth'))
    except IOError:
        print('JWT cache already purged')


# OXE WBM change requests quota
def oxe_wbm_update_requests_quota(host, port, password, root_password):
    # execute as root following command
    # sed -i -e 's/zone=two\:1m rate\=2r\/s/zone=two\:1m rate\=50r\/s/g' /usr/local/openresty/nginx/conf/wbm.conf
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
        time.sleep(1)
    stdout += channel.recv(1024)
    channel.send(root_password + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.send('sed -i -e \'s/zone=two\:1m rate\=2r\/s/zone=two\:1m rate\=50r\/s/g\' /usr/local/openresty/nginx/conf/wbm.conf\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode('utf-8'))
    channel.close()
    client.close()


def oxe_wbm_restart(host, port, password):
    """RUNTEL start telephone

    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        root_password (TYPE): Description

    Returns:
        TYPE: Description
    """
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command('dhs3_init -R openresty')
    client.close()
