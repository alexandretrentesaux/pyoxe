# -*- encoding: utf-8 -*-

"""OXE infos methods 
"""
from pprint import pprint
from requests import get, packages
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_get_json_model(host, token):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    response = get('https://' + host + '/api/mgt/1.0/model',
                   headers=oxe_set_headers(token),
                   verify=False,
                   stream=True)
    result = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            result += chunk.decode('utf-8')
    # todo: transcode false to 'false'
    # todo: transcode true to 'true'
    return result


def oxe_get_rainbow_agent_version(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    command = 'rainbowagent -v'
    stdin, stdout, stderr = client.exec_command(command)
    version = {'rainbowagent version': stdout.readlines()[0].split()[2]}
    pprint(version)
    client.close()
    return version


def oxe_get_oxe_version(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    # connect OXE through SSH and execute 'rainbowagent -v'
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    command = 'siteid'
    stdin, stdout, stderr = client.exec_command(command)
    tmp = stdout.readlines()

    # pprint.pprint(tmp)
    # todo test string patch static/dynamic
    major = tmp[2].split()[4].upper()
    static = tmp[3].split()[3]
    dynamic = tmp[4].split()[4]
    version = {'OXE version': major + '.' + static + dynamic}
    pprint(version)
    client.close()
    return version
