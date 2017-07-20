""" OXE IP domains configuration methods """
import pprint
import requests
import requests.packages
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_ip_domain_deactivate_compression_default_ip_domain(host, token):
    payload = {
        'Intra_Domain_Coding_Algorithm': 'No_Compression',
        'Extra_Domain_Coding_Algorithm': 'No_Compression'
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put('https://' + host + '/api/mgt/1.0/Node/1/IP/1/IP_Domain/0',
                                    json=payload,
                                    headers=oxe_set_headers(token, 'PUT'),
                                    verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code
