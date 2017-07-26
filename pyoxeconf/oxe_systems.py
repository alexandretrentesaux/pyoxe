""" OXE Systems configuration methods """
import pprint
import requests
import requests.packages
from pyoxeconf.oxe_access import oxe_set_headers


# Compression_type value 'G_729'/'G_723'
def oxe_system_compression_type(host, token, compression_type):
    payload = {
        'Compression_Type': compression_type
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/Compression_Parameters/Compression_Type',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


# law value "Law_A"/"Law_Mu"
def oxe_system_law(host, token, law):
    payload = {
        'Law': law
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/Law',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


# mode value 'true'/'false'
def oxe_system_alaw_to_mulaw(host, token, mode):
    payload = {
        'T0_Mu_Law': mode
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/T0_Mu_Law',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


def oxe_system_accept_mu_a_laws_in_sip(host, token, mode):
    payload = {
        'T0_Mu_Law': mode
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/System_/Accept_Mu_A_Laws_In_SIP',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


def oxe_system_csta_sessions_monitored(host, token, max_session):
    payload = {
        'CSTA_Requests_monitored': max_session
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host +
            '/api/mgt/1.0/Node/1/System_Parameters/1/System_Parameters_2/1/RTU_Parameters/CSTA_Requests_monitored',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


def oxe_system_network_number(host, token, net_number):
    payload = {
        'Network_Number': net_number
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code


def oxe_system_node_number(host, token, node_number):
    payload = {
        'Node_Number': node_number
    }
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        modification = requests.put(
            'https://' + host + '/api/mgt/1.0/Node/1/System_Parameters/1',
            json=payload,
            headers=oxe_set_headers(token, 'PUT'),
            verify=False)
    except requests.exceptions.RequestException as e:
        pprint.pprint(e)
    return modification.status_code
