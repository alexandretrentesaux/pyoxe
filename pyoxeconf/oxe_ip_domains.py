# -*- encoding: utf-8 -*-

"""OXE IP domains configuration methods 
"""
from pprint import pprint
from requests import put, exceptions, packages
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_ip_domain_deactivate_compression_default_ip_domain(host, token):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Intra_Domain_Coding_Algorithm': 'No_Compression',
        'Extra_Domain_Coding_Algorithm': 'No_Compression'
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put('https://' + host + '/api/mgt/1.0/Node/1/IP/1/IP_Domain/0',
                           json=payload,
                           headers=oxe_set_headers(token, 'PUT'),
                           verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code
