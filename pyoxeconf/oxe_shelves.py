# -*- encoding: utf-8 -*-

"""OXE Shelves configuration methods 
"""
from pprint import pprint
from requests import packages, put, post, exceptions
from pyoxeconf.oxe_access import oxe_set_headers


# Create shelves
def oxe_create_shelf(host, token, shelf_id, rack_size):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        shelf_id (TYPE): Description
        rack_size (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'MediaServer': 'Yes',
        'Rack_Size': rack_size
    }
    if id == 0 or id == 18 or id ==19:
        print('Error can\'t proceed to create shelf with reserved id : {}'.format(id))
        exit(-1)
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        creation = post('https://' + host + '/api/mgt/1.0/Node/1/Rack/' + str(shelf_id),
                        json=payload,
                        headers=oxe_set_headers(token, 'POST'),
                        verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return creation.status_code


# Update shelf ethernet parameters
def oxe_shelf_ethernet_parameters(host, token, shelf_id, mac_address):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        shelf_id (TYPE): Description
        mac_address (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Board_Ethernet_Address': mac_address
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put('https://' + host + '/api/mgt/1.0/Node/1/Rack/' + str(shelf_id)
                           + '/Board/0/Ethernet_Parameters/' + str(shelf_id) + '-0',
                           json=payload,
                           headers=oxe_set_headers(token, 'PUT'),
                           verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code


# Update compressors number
def oxe_shelf_board_compressors_for_ip_devices(host, token, shelf_id, compressors):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        shelf_id (TYPE): Description
        compressors (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'IP_Nb_Used_Compressors': compressors
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = put('https://' + host + '/api/mgt/1.0/Node/1/Rack/' + shelf_id + '/Board/0',
                           json=payload,
                           headers=oxe_set_headers(token, 'PUT'),
                           verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return modification.status_code
