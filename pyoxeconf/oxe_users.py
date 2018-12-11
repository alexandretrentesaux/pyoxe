# -*- encoding: utf-8 -*-

"""Summary
"""
from requests import packages, exceptions, post, put, delete, utils
from time import sleep
from pprint import pprint
from pyoxeconf.oxe_access import oxe_set_headers


def oxe_create_user(host, token, extension, last_name, first_name, station_type, max_retries):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        extension (TYPE): Description
        last_name (TYPE): Description
        first_name (TYPE): Description
        station_type (TYPE): Description
        max_retries (TYPE): Description
    """
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        "Annu_Name": last_name,
        "Annu_First_Name": first_name,
        "Station_Type": station_type
    }
    for i in range(max_retries):
        response = post('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                        headers=oxe_set_headers(token, 'POST'),
                        json=payload,
                        verify=False)
        # code status 201: CREATED
        if response.status_code in (201, 401):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            sleep(.500)
            # return response.status_code
        elif response.status_code == 403:
            print('Connection error, please reconnect first! mass provisioning ended on extension {}'.format(
                str(extension - 1)))
            exit(-1)


def oxe_delete_user(host, token, extension, max_retries):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        extension (TYPE): Description
        max_retries (TYPE): Description
    """
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    for i in range(max_retries):
        response = delete('https://' + host + '/api/mgt/1.0/Node/1/Subscriber/' + str(extension),
                          headers=oxe_set_headers(token, 'DELETE'),
                          verify=False)
        # code status 200: OK
        if response.status_code in (200, 404):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            sleep(.500)


def oxe_create_phonebook_entry(host, token, extension, last_name, first_name, alias, max_retries):
    """Summary
    
    Args:
        host (TYPE): Description
        token (TYPE): Description
        extension (TYPE): Description
        last_name (TYPE): Description
        first_name (TYPE): Description
        alias (TYPE): Description
        max_retries (TYPE): Description
    """
    packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)
    payload = {
        'Annu_First_Name': first_name,
        'Annu_Name': last_name,
        'Phone_Book_First_Name': first_name,
        'Phone_Book_Name': last_name,
        'Phone_Book_Type': 'PB_Service_Number',
        'UTF8_Phone_Book_First_Name': first_name,
        'UTF8_Phone_Book_Name': last_name
    }
    for i in range(max_retries):
        response = post('https://' + host + '/api/mgt/1.0/Node/1/Phone_Book/' + str(extension) +
                        utils.quote(',') + str(alias),
                        oxe_set_headers(token, 'POST'),
                        json=payload,
                        verify=False)
        if response.status_code in (201, 404, 401):
            break
        # code status 503: retry with same requests + wait 500ms (oxe max 2r/s)
        elif response.status_code == 503:
            sleep(.500)
    pprint('\n' + str(response.status_code))
