# -*- encoding: utf-8 -*-

"""OXE 4645 configuration methods 
"""
import paramiko
import time
import requests
import pprint
from pyoxeconf.oxe_access import oxe_set_headers


# work only for standalone server
# todo: add callserver2 option
# todo: add option for eva_access
def vm_create_eva_cfg(host, port=22, password='mtcl', accesses=15):
    """Summary
    
    Args:
        host (TYPE): Description
        port (int, optional): Description
        password (str, optional): Description
        accesses (int, optional): Description
    """
    data = 'callserver1=' + host +'\ncallserver2=' + '\neva=' + host + '\eva_access=' + accesses
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
    channel.send('cat >> /usr3/mao/eva.cfg << EOF\n' + data + '\nEOF\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


# todo : add option to customize nb_lines
def vm_create_eva_access(host, port=22, password='mtcl', accesses=15):
    """Summary
    
    Args:
        host (TYPE): Description
        port (int, optional): Description
        password (str, optional): Description
        accesses (int, optional): Description
    """
    data = 'NB_LINES=' + accesses
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
    channel.send('cat >> /usr3/mao/eva.access << EOF\n' + data + '\nEOF\n')
    while channel.recv_ready() is False:
        time.sleep(0.5)
    stdout += channel.recv(1024)
    # print(stdout.decode(encoding='UTF-8'))
    channel.close()
    client.close()


def vm_create(host, token, voice_mail_number, number_accesses, voice_mail_directory_name='voicemail',
                                 voice_mail_server_index=1, voice_mail_type='embedded'):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        voice_mail_number (TYPE): Description
        number_accesses (TYPE): Description
        voice_mail_directory_name (str, optional): Description
        voice_mail_server_index (int, optional): Description
        voice_mail_type (str, optional): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Directory_Name': voice_mail_directory_name,
        'Number_Of_Accesses': number_accesses,
        'Voice_Mail_CPU_Name': host,
        'Voice_Mail_Directory_Number': voice_mail_number,
        'Voice_Mail_Server_Number': voice_mail_server_index,
        'Voice_Mail_Type': voice_mail_type
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host + '/api/mgt/1.0/Node/101/Application_Configuration/1/Voice_Mail/' + voice_mail_server_index,
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False
            )
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code
