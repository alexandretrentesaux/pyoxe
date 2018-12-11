# -*- encoding: utf-8 -*-

"""OXE translator configuration methods 
"""
from pprint import pprint
from requests import packages, exceptions, post
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_translator_prefix_create_dpnss(host, token, dpnss_prefix):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        dpnss_prefix (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    payload = {
        'Prefix_Meaning': 'Local_Facilities',
        'Local_Facility_Type': 'Pabx_address_in_network'
    }
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        creation = post('https://' + host + '/api/mgt/1.0/Node/1/Services_Access_Code/1/Prefix_Plan/'
                        + dpnss_prefix,
                        json=payload,
                        headers=oxe_set_headers(token, 'POST'),
                        verify=False)
    except exceptions.RequestException as e:
        pprint(e)
    return creation.status_code
