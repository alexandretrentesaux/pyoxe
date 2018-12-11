# -*- encoding: utf-8 -*-

"""OXE Systems configuration methods 
"""
from pprint import pprint
from requests import packages, exceptions, post, put
from pyoxeconf.oxe_access import oxe_set_headers


# Compression_type value 'G_729'/'G_723'
def oxe_system_compression_type(host, token, compression_type):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        compression_type (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Compression_Type': compression_type
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/Compression_Parameters/Compression_Type',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


# law value "Law_A"/"Law_Mu"
def oxe_system_law(host, token, law):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        law (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Law': law
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/Law',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


# mode value 'true'/'false'
def oxe_system_alaw_to_mulaw(host, token, mode):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        mode (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'T0_Mu_Law': mode
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/T0_Mu_Law',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


def oxe_system_accept_mu_a_laws_in_sip(host, token, mode):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        mode (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'T0_Mu_Law': mode
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/Accept_Mu_A_Laws_In_SIP',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


def oxe_system_ucaas_csta_sessions_monitored(host, token, max_session):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        max_session (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'CSTA_Requests_monitored': max_session
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/RTU_Parameters/CSTA_Requests_monitored',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


def oxe_system_network_number(host, token, net_number):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        net_number (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Network_Number': net_number
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


def oxe_system_node_number(host, token, node_number):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        node_number (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Node_Number': node_number
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put(
            'https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code
