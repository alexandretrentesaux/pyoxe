# -*- encoding: utf-8 -*-

"""OXE licensing methods
"""
import pprint
import requests
import requests.packages
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_set_flex(host, token, flex_ip_address, flex_port):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        flex_ip_address (TYPE): Description
        flex_port (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        "Flex_Licensing_Enable": "Yes",
        "Flex_Server_Address": flex_ip_address,
        "Flex_Server_Port": flex_port,
        "Flex_ProductId_Discovery": "Yes"
    }
    try:
        response = requests.put('https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1/Flex_Server/1',
                                headers=oxe_set_headers(token, 'PUT'),
                                json=payload,
                                verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    # todo: manage errors
    return response.status_code


def oxe_create_offerid(host, password):
    """Summary
    
    Args:
        host (TYPE): Description
        password (TYPE): Description
    """
    pprint.pprint('todo\n')
    # todo: connect CS through SSH and create empty file /usr3/mao/offerid.zip
