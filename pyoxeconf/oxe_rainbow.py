"""Summary"""
import configparser
import pprint
import requests
import requests.packages
import paramiko
import os
import tempfile
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_get_rainbow_config(filename=None):
    """Summary

    Returns:
        TYPE: Description
    """
    config = configparser.ConfigParser()
    if filename is None:
        config.read(tempfile.gettempdir() + 'oxe.ini')
    else:
        config.read(os.path.join(tempfile.gettempdir(), filename))
    rainbow_domain = config.get('default', 'rainbow_domain', raw=False)
    pbx_id = config.get('default', 'pbx_id', raw=False)
    rainbow_temp_password = config.get('default', 'rainbow_temp_password', raw=False)
    rainbow_host = config.get('default', 'rainbow_host', raw=False)
    return rainbow_domain, pbx_id, rainbow_temp_password, rainbow_host


def oxe_rainbow_connect(host, token, rainbow_domain, pbx_id, temp_password, phone_book):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description
        rainbow_domain (TYPE): Description
        pbx_id (TYPE): Description
        temp_password (TYPE): Description
        phone_book (TYPE): Description

    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Rainbow_Agent_Enable': 'Yes',
        'Rainbow_Domain': rainbow_domain,
        'Rainbow_Pbx_Id': pbx_id,
        'Rainbow_Temp_Password': temp_password,
        'Rainbow_Use_PhoneBook': phone_book.capitalize()
    }
    try:
        response = requests.put('https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1',
                                headers=oxe_set_headers(token, 'PUT'),
                                json=payload,
                                verify=False
                                )
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return response.status_code


def oxe_rainbow_disconnect(host, token):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description

    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Rainbow_Agent_Enable': 'No'
    }
    try:
        response = requests.put('https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1',
                                headers=oxe_set_headers(token, 'PUT'),
                                json=payload,
                                verify=False
                                )
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return response.status_code


def oxe_rainbow_reconnect(host, token, pbx_id, rainbow_domain):
    """Summary

    Args:
        host (TYPE): Description
        token (TYPE): Description
        pbx_id (TYPE): Description
        rainbow_domain (TYPE): Description

    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Rainbow_Agent_Enable': 'Yes',
        'Rainbow_Pbx_Id': pbx_id,
        'Rainbow_Domain': rainbow_domain
    }
    try:
        response = requests.put('https://' + host + '/api/mgt/1.0/Node/1/RAINBOW/1',
                                headers=oxe_set_headers(token, 'PUT'),
                                json=payload,
                                verify=False
                                )
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
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
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    command = "cat >> /usr3/mao/ccca.cfg << EOF\nRAINBOW_HOST={}\nEOF\n".format(api_server)
    # print(command)
    client.exec_command(command)
    client.close()


def oxe_purge_ccca_cfg(host, port, password):
    # sed -re 's/PASSWORD=.*/PASSWORD=/g' /usr3/mao/ccca.cfg
    # sed -re 's/STATE=./STATE=0/g' /usr3/mao/ccca.cfg
    # sed '/^RAINBOW_HOST/d' /usr3/mao/ccca.cfg
    client = paramiko.SSHClient()  # use the paramiko SSHClient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add SSH key
    try:
        client.connect(host, port, username='mtcl', password=password)
    except paramiko.AuthenticationException:
        print('*** Failed to connect to {}:{}'.format(host, port))
    client.exec_command("sed -i -re \'s/PASSWORD=.*/PASSWORD=/g\' /usr3/mao/ccca.cfg\n")
    client.exec_command("sed -i -re \'s/STATE=./STATE=0/g\' /usr3/mao/ccca.cfg\n")
    client.exec_command("sed -i -e \'/^RAINBOW_HOST/d\' /usr3/mao/ccca.cfg\n")
    client.close()


# todo enable phonebook use
# todo disable phonebook use
# todo clean rainbowagent log files
