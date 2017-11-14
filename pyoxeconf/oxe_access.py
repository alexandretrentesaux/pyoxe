# -*- encoding: utf-8 -*-

"""OXE connection methods 
"""
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
        password (str): mtcl password
        proxies (json): proxies
    """

    config = configparser.ConfigParser()
    full_path = os.path.join(tempfile.gettempdir(), 'pyoxeconf.ini')

    if os.path.exists(full_path):
        config.read(full_path)

    if config.has_section('default') is False:
        config.add_section('default')

    if config.has_section(str(host)) is False:
        config.add_section(str(host))
    config.set(str(host), 'host', str(host))
    config.set(str(host), 'login', str(login))
    config.set(str(host), 'password', str(password))

    if proxies is not None:
        if config.has_section('proxies') is False:
            config.add_section('proxies')
        config.set('proxies', 'proxies', proxies)

    with open(full_path, 'w+') as file:
        try:
            config.write(file)
            os.chmod(full_path, 0o600)
        except configparser.Error as e:
            print('Error creating config file: {}'.format(full_path))
            exit(-1)


# get connection info from config file
def oxe_get_config(host=None):
    """Summary
    
    Returns:
        TYPE: Description
    
    Args:
        host (None, optional): Description
    """

    config = configparser.ConfigParser()
    full_path = os.path.join(tempfile.gettempdir(), 'pyoxeconf.ini')

    if os.path.exists(full_path):
        config.read(full_path)
        if config.has_section(str(host)):
            # oxe_ip = config.get(str(host), 'host', raw=False)
            # login = config.get(str(host), 'login', raw=False)
            password = config.get(str(host), 'password', raw=False)
        else:
            print('Inconsistent config file: {}'.format(full_path))
            exit(-1)
        if config.has_section('proxies'):
            proxies = config.get('proxies', 'proxies', raw=True)
        else:
            proxies = None
        return password, proxies
    elif IOError:
        print('error opening file: {}'.format(full_path))
        exit(-1)


# store authentication token
def oxe_get_auth_from_cache(host):
    """Summary
    
    Returns:
        TYPE: Description
    
    Args:
        host (TYPE): Description
    """
    config = configparser.ConfigParser()
    full_path = os.path.join(tempfile.gettempdir(), '.pyoxeconf')

    if os.path.exists(full_path):
        config.read(full_path)
        if config.has_section(str(host)):
            return config.get(str(host), 'token', raw=False)
    elif IOError:
        print('error opening file: {}'.format(full_path))
        exit(-1)


# build header
def oxe_set_headers(token, method=None):
    """Builder for requests headers depending on request method
    
    Args:
        token (STR): Authentication token
        method (None, optional): GET (not mandatory), PUT, POST, DELETE
    
    Returns:
        JSON: headers
    """

    # basic method GET
    headers = {
        'Authorization': 'Bearer ' + token,
        'accept': 'application/json'
    }

    # addition for POST & PUT
    if method in ('POST', 'PUT'):
        headers.update({'Content-Type': 'application/json'})
    # addtion for DELETE
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
    
    Returns:
        TYPE: Description
    """

    # Authentication through WBM API
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    url = 'https://' + host + '/api/mgt/1.0/login'
    full_path = os.path.join(tempfile.gettempdir(), '.pyoxeconf')

    authentication = requests.get(url, timeout=10, auth=(login, password), verify=False, proxies=proxies)
    if authentication.status_code == 401:
        print('Error {} - {}'.format(authentication.json()['errorCode'],
                                     authentication.json()['errorMsg']))
        sys.exit(-1)
    elif authentication.status_code == 000:
        print('Error {} - telephony is not running on OXE / WBM not available'.format(authentication.status_code))
        sys.exit(-1)

    # Cache authentication data for later use in other CLI commands
    config = configparser.ConfigParser()

    if os.path.exists(full_path):
        config.read(full_path)

    if config.has_section('default') is False:
        config.add_section('default')

    if config.has_section(str(host)) is False:
        config.add_section(str(host))
    config.set(str(host), 'token', str(authentication.json()['token']))

    auth_write_cache(full_path, config)

    return authentication.json()


# OXE WBM logout
def oxe_logout(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    config = configparser.ConfigParser()
    full_path = os.path.join(tempfile.gettempdir(), '.pyoxeconf')

    if os.path.exists(full_path):
        config.read(full_path)

    if config.has_section(str(host)):
        config.remove_section(str(host))
        auth_write_cache(full_path, config)
    else:
        print('You\'re already logout from OXE {}'.format(str(host)))


def auth_write_cache(path, config):
    """Summary
    
    Args:
        path (TYPE): Description
        config (TYPE): Description
    """
    with open(path, 'w+') as file:
        try:
            config.write(file)
            os.chmod(path, 0o600)
        except configparser.Error as e:
            print('Error writing config file: {}'.format(path))
            exit(-1)


# All OXE WBM logout
def oxe_logout_all():
    """Logout from WBM
    """

    # clear cache
    try:
        os.remove(os.path.join(tempfile.gettempdir(), '.pyoxeconf'))
    except IOError:
        print('JWT cache already purged')


# OXE WBM change requests quota
def oxe_wbm_update_requests_quota(host, port, password, root_password, new_limit=50):
    """Update WBM requests limit for configuration zone (not authentication zone)
    
    Args:
        host (STR): OmniPCX Enterprise IP address
        port (INT): SSH port
        password (STR): mtcl password
        root_password (TYPE): root password
        new_limit (int, optional): Description
    """

    # Build OXE sed command
    cmd = 'sed -i -e \'s/zone=two\:1m rate\=2r\/s/zone=two\:1m rate\=' + new_limit + \
          'r\/s/g\' /usr/local/openresty/nginx/conf/wbm.conf\n'

    # SSH connection
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    channel = client.invoke_shell()
    while channel.recv_ready() is False:
        time.sleep(3)  # OXE is really slow on mtcl connexion (Update this timer on physical servers)
    stdout = channel.recv(4096)
    channel.send('su -\n')
    while channel.recv_ready() is False:
        time.sleep(1)
    stdout += channel.recv(1024)
    channel.send(root_password + '\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    # channel.send('sed -i -e \'s/zone=two\:1m rate\=2r\/s/zone=two\:1m rate\=50r\/s/g\' /usr/local/openresty/nginx/conf/wbm.conf\n')
    channel.send(cmd)
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    channel.close()
    client.close()


def oxe_wbm_restart(host, port, password):
    """restart WBM
    
    Args:
        host (STR): OmniPCX Enterprise IP address
        port (INT): SSH port
        password (STR): mtcl password
    """

    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command('dhs3_init -R openresty')
    client.close()
