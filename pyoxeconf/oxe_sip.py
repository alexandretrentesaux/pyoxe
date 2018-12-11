# -*- encoding: utf-8 -*-

"""OXE SIP configuration methods 
"""
from pprint import pprint
from requests import packages, exceptions, post, put
from pyoxeconf.oxe_access import oxe_set_headers


# create default trunk groups
def oxe_sip_create_default_trunk_groups(host, token, trunk_id):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        trunk_id (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Homo_Net_For_Direct_RTP': 'Yes',
        'Number_Of_Digits_To_Send': '4',
        'Public_Network_Category_Id': '31',
        'Remote_Network': '15',
        'Signalization_Variation': 'ABC_F_VARIANT',
        'T2_Specificity': 'SIP',
        'Trunk_Group_Name': 'SIP'
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        creation = post('https://' + host + '/api/mgt/1.0/Node/1/Trunk_Group_Overview/' + str(trunk_id),
                        json=payload,
                        headers=oxe_set_headers(token, 'POST'),
                        verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return creation.status_code


# configure sip gateway
def oxe_sip_gateway(host, token, trunk_id):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        trunk_id (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'SIP_Subnetwork': '15',
        'SIP_Trunk_Group': trunk_id
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put('https://' + host + '/api/mgt/1.0/Node/1/SIP/1/SIP_Gateway/1',
                           json=payload,
                           headers=oxe_set_headers(token, 'PUT'),
                           verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


# configure sip proxy
def oxe_sip_proxy(host, token):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'SIP_min_auth_method': 'SIP_None',
        'SIP_Move_To_TCP': 'false',
        'ReTransNo_Invite': '4'
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put('https://' + host + '/api/mgt/1.0/Node/1/SIP/1/SIP_Proxy/1',
                           json=payload,
                           headers=oxe_set_headers(token, 'PUT'),
                           verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code

