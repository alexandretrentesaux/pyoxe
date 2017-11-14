# -*- encoding: utf-8 -*-

"""OXE translator configuration methods 
"""
import pprint
import requests
import requests.packages
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
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        creation = requests.post('https://' + host + '/api/mgt/1.0/Node/1/Services_Access_Code/1/Prefix_Plan/'
                                 + dpnss_prefix,
                                 json=payload,
                                 headers=oxe_set_headers(token, 'POST'),
                                 verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return creation.status_code
