# -*- encoding: utf-8 -*-

"""Rainbow settings methods
"""
from configparser import ConfigParser
from pprint import pprint
from requests import packages, put, exceptions
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from os.path import join, exists
from tempfile import gettempdir
from pyoxeconf.oxe_access import oxe_set_headers
from sys import exit
from time import sleep


def oxe_get_rainbow_config(filename=None):
    """Retrieve Rainbow configuration from ini file
    
    Args:
        filename (STR): config file name
    
    Returns:
        TYPE: Description
    """

    config = ConfigParser()

    if filename is None:
        full_path = join(gettempdir() + 'oxe.ini')
    else:
        full_path = join(gettempdir(), filename)

    print('DEBUG: trying to open ini file: {}'.format(full_path))

    if exists(full_path):
        config.read(full_path)
        if config.has_section('default'):
            rainbow_domain = config.get('default', 'rainbow_domain', raw=False)
            pbx_id = config.get('default', 'pbx_id', raw=False)
            rainbow_temp_password = config.get('default', 'rainbow_temp_password', raw=False)
            rainbow_host = config.get('default', 'rainbow_host', raw=False)
            return rainbow_domain, pbx_id, rainbow_temp_password, rainbow_host
        else:
            print('Corrupted rainbow config file')
            exit(-1)
    elif IOError:
        print('Rainbow config file does not exists')
        exit(-1)


def oxe_rainbow_connect(host, token, rainbow_domain, pbx_id, temp_password, phone_book):
    """Set settings for Rainbow connection.
    
    Not sufficient for AIO: updateCccaCfg must used in addition to this command
    
    Args:
        host (STR): OmniPCX Enterprise IP address / FQDN
        token (STR): Authentication token
        rainbow_domain (STR): Rainbow domain
        pbx_id (STR): PBX ID
        temp_password (STR): Activation code
        phone_book (STR): YES/NO Phone book processing
    
    Returns:
        INT: API request status code
    """

    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Rainbow_Agent_Enable': 'Yes',
        'Rainbow_Domain': rainbow_domain,
        'Rainbow_Pbx_Id': pbx_id,
        'Rainbow_Temp_Password': temp_password,
        'Rainbow_Use_PhoneBook': phone_book.capitalize()
    }

    try:
        response = put('https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1',
                       headers=oxe_set_headers(token, 'PUT'),
                       json=payload,
                       verify=False
                       )
    except exceptions.RequestException as e:
        pprint(e)
    return response.status_code


def oxe_rainbow_disconnect(host, token):
    """Disconnect OXE from Rainbow
    
    Args:
        host (STR): OmniPCX Enterprise IP address / FQDN
        token (STR): Authentication token
    
    Returns:
        INT: API request status code
    """

    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    # Pay attention in M1.403.15.h disabling rainbow agent also restore Rainbow domain to default value
    payload = {'Rainbow_Agent_Enable': 'No'}
    url = 'https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1'

    try:
        response = put(url, headers=oxe_set_headers(token, 'PUT'), json=payload, verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return response.status_code


def oxe_rainbow_reconnect(host, token, pbx_id, rainbow_domain):
    """Reconnect OXE to rainbow
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        pbx_id (TYPE): Description
        rainbow_domain (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Rainbow_Agent_Enable': 'Yes',
        'Rainbow_Pbx_Id': pbx_id,
        'Rainbow_Domain': rainbow_domain
    }
    try:
        response = put('https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1',
                       headers=oxe_set_headers(token, 'PUT'),
                       json=payload,
                       verify=False
                       )
    except exceptions.RequestException as e:
        pprint(e)
    return response.status_code


def oxe_update_ccca_cfg_dev_all_in_one(host, port, password, api_server):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        api_server (TYPE): Description
    """
    # update ccca.cfg for all-in-one connection
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    command = "cat >> /usr3/mao/ccca.cfg << EOF\nRAINBOW_HOST={}\nEOF\n".format(api_server)
    # print(command)
    client.exec_command(command)
    client.close()


def oxe_purge_ccca_cfg(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    # sed -re 's/PASSWORD=.*/PASSWORD=/g' /usr3/mao/ccca.cfg
    # sed -re 's/STATE=./STATE=0/g' /usr3/mao/ccca.cfg
    # sed '/^RAINBOW_HOST/d' /usr3/mao/ccca.cfg
    client = SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command("sed -i -re \'s/PASSWORD=.*/PASSWORD=/g\' /usr3/mao/ccca.cfg\n")
    client.exec_command("sed -i -re \'s/STATE=./STATE=0/g\' /usr3/mao/ccca.cfg\n")
    client.exec_command("sed -i -e \'/^RAINBOW_HOST/d\' /usr3/mao/ccca.cfg\n")
    client.close()


def oxe_purge_rainbowagent_logs(host, port=22, password='mtcl', root_password='letacla'):
    """Summary
    
    Args:
        host (TYPE): Description
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
    channel.send('rm -f /var/log/rainbowagent.log.*\n')
    while channel.recv_ready() is False:
        sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()

# todo enable phonebook use
# todo disable phonebook use
# todo clean rainbowagent log files
