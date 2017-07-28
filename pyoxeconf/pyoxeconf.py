#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Here go you application specific code.

import click
import progressbar
import datetime
import json
import pkg_resources
from clickclick import AliasedGroup
from pyoxeconf.__init__ import __version__
from pyoxeconf.oxe_commands import *
from pyoxeconf.oxe_access import oxe_get_auth_from_cache, oxe_logout, oxe_configure, oxe_get_config, \
    oxe_authenticate, oxe_wbm_update_requests_quota, oxe_wbm_restart
from pyoxeconf.oxe_info import *
from pyoxeconf.oxe_users import *
from pyoxeconf.oxe_rainbow import *
from pyoxeconf.oxe_licensing import *
from pyoxeconf.oxe_sip import *
from pyoxeconf.oxe_shelves import *
from pyoxeconf.oxe_systems import *
from pyoxeconf.oxe_ip_domains import *
from pyoxeconf.oxe_translator import *
from pyoxeconf.oxe_voicemail import *
from pyoxeconf.oxe_netadmin import *
# from pyoxeconf.oxe_swinst import *
from pyoxeconf.oms_config import *
from pyoxeconf.sipp import *
from pyoxeconf.oxe_log import *
from pyoxeconf.nginx_rp import *


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

STYLES = {
    'FINE': {'fg': 'green'},
    'ERROR': {'fg': 'red'},
    'WARNING': {'fg': 'yellow', 'bold': True},
}

TITLES = {
    'state': 'Status',
    'creation_time': 'Creation Date',
    'id': 'Identifier',
    'desc': 'Description',
    'name': 'Name',
}

MAX_COLUMN_WIDTHS = {
    'desc': 50,
    'name': 20,
}


# Version
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    pprint.pprint(pkg_resources.require("pyoxeconf")[0])
    click.echo('pyoxeconfgen_cli version: {}'.format(__version__))
    ctx.exit()


# CLI
@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


# OXE access methods

@cli.command('configure')
@click.option('--host', help='OXE IP address / FQDN')
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_configure(**kwargs):
    oxe_ip = kwargs.get('host', None)
    if oxe_ip is None:
        print('--host option is mandatory')
        exit(-1)
    password = kwargs.get('password', 'mtcl')
    proxies = kwargs.get('proxies', None)
    oxe_configure(oxe_ip, 'mtcl', password, proxies)


@cli.command('connect')
@click.option('--host', help='OXE IP address / FQDN')
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
@click.option('--ini', help='Config File', is_flag=True)
def cli_connect(**kwargs):
    ini = kwargs.get('ini', False)
    if ini is False:
        host = kwargs.get('host', None)
        if host is None:
            print('--host option is mandatory')
            exit(-1)
        password = kwargs.get('password', 'mtcl')
        proxies = kwargs.get('proxies', None)
    else:
        host, login, password, proxies = oxe_get_config()
    oxe_authenticate(host, 'mtcl', password, proxies)


@cli.command('logout')
def cli_logout():
    oxe_logout()


@cli.command('wbmRequestsLimit')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
def cli_wbm_requests_limit(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    root_password = kwargs.get('rootpassword')
    oxe_wbm_update_requests_quota(ip, port, password, root_password)


@cli.command('wbmRestart')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_wbm_restart(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_wbm_restart(ip, port, password)


# JSON model

@cli.command('getJsonModel')
def cli_get_json_model():
    token, host = oxe_get_auth_from_cache()
    json_model = json.loads(oxe_get_json_model(host, token))
    horodating = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open(os.path.join(tempfile.gettempdir(), 'OXE_' + host + '_' + horodating + '.json'), 'w') as fh:
        fh.write(json.dumps(json_model, indent=4, sort_keys=True))


# Users management

@cli.command('createUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--setType', help='set type', default='SIP_Extension')
@click.option('--companyId', help='Company Index', default=1)
@click.option('--sipp', help='Generate SIPp csv file', is_flag=True)
def cli_create_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    set_type = kwargs.get('settype', 'SIP_Extension')
    company_id = kwargs.get('companyid', 1)
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    # json_model['definitions']['Station_Type']['values'] # to control set type with OXE dictionary
    for extension_number in bar(range(range_start, range_start + range_size)):
        if company_id < 10:
            last_name = 'LC0' + str(company_id) + 'U' + str(extension_number)
            first_name = 'FC0' + str(company_id) + 'U' + str(extension_number)
        else:
            last_name = 'LC0' + str(company_id) + 'U' + str(extension_number)
            first_name = 'FC0' + str(company_id) + 'U' + str(extension_number)
        oxe_create_user(host, token, extension_number, last_name, first_name, set_type, 10)
    if set_type == 'SIP_Extension' and kwargs.get('sipp') is True:
        sipp_csv_generator(host + '_' + str(range_size) + 'users', host, range_start, range_size, '0000')


@cli.command('deleteUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
def cli_delete_users(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(range_start, range_start + range_size)):
        oxe_delete_user(host, token, extension_number, 10)


@cli.command('createPhonebookEntries')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--alias', help='directory alias', default=255)
def cli_create_phonebook_entries(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    alias = int(kwargs.get('alias', 0))
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    if 0 <= alias <= 15 or alias == 255:
        for extension_number in bar(range(range_start, range_start + range_size)):
            oxe_create_phonebook_entry(host, token, extension_number, 'pb_ln' + str(extension_number),
                                       'pb_fn' + str(extension_number), alias, 10)
    else:
        print('--alias value must be in following ranges 0 to 15, 255')
        exit(-1)


# Licenses management

@cli.command('setFlexServer')
@click.option('--ip', help='External Flex server IP address')
@click.option('--port', help='External Flex port', default=27000)
@click.option('--reboot', help='Reboot CS to apply settings', is_flag=True)
@click.option('--sshPort', help='OXE SSH port / needed if --reboot', default=22)
@click.option('--password', help='mtcl password / needed if --reboot', default='mtcl')
@click.option('--swinstPassword', help='swinst password / needed if --reboot', default='SoftInst')
def cli_set_flex_server(**kwargs):
    flex_ip_address = kwargs.get('ip', None)
    if flex_ip_address is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    flex_port = kwargs.get('port', 27000)
    token, host = oxe_get_auth_from_cache()
    oxe_set_flex(host, token, flex_ip_address, flex_port)
    print('WARNING: OXE must be rebooted')
    if kwargs.get('reboot') is True:
        port = kwargs.get('sshport')
        mtcl_password = kwargs.get('password')
        swinst_password = kwargs.get('swinstpassword')
        oxe_reboot(host, port, mtcl_password, swinst_password)


# Rainbow connection management

@cli.command('rainbowConnect')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--pbxId', help='PBX Rainbow ID')
@click.option('--phoneBook', help='Send OXE phone book to Rainbow', default='Yes')
@click.option('--activationCode', help='PBX activation code')
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_enable_rainbow_connection(**kwargs):
    token, host = oxe_get_auth_from_cache()
    phone_book = kwargs.get('phonebook', 'Yes')
    if kwargs.get('ini') is False:
        rainbow_domain = kwargs.get('rainbowdomain', None)
        if rainbow_domain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit(-1)
        pbx_id = kwargs.get('pbxid', None)
        if pbx_id is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit(-1)
        activation_code = kwargs.get('activationcode', None)
        if activation_code is None:
            print('--activationCode option is mandatory. Exiting ...')
            exit(-1)
    else:
        rainbow_domain, pbx_id, activation_code, rainbow_host = oxe_get_rainbow_config(kwargs.get('filename'))
    oxe_rainbow_connect(host, token, rainbow_domain, pbx_id, activation_code, phone_book)


@cli.command('rainbowDisconnect')
def cli_disable_rainbow_connection():
    token, host = oxe_get_auth_from_cache()
    oxe_rainbow_disconnect(host, token)


@cli.command('rainbowReconnect')
@click.option('--pbxId', help='PBX Rainbow ID')
@click.option('--rainbowDomain', help='Rainbow Domain')
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_enable_rainbow_connection(**kwargs):
    token, host = oxe_get_auth_from_cache()
    if kwargs.get('ini') is False:
        pbx_id = kwargs.get('pbxid', None)
        if pbx_id is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit(-1)
        rainbow_domain = kwargs.get('rainbowdomain', None)
        if rainbow_domain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit(-1)
    else:
        rainbow_domain, pbx_id, activation_code, rainbow_host = oxe_get_rainbow_config(kwargs.get('filename'))
    oxe_rainbow_reconnect(host, token, pbx_id, rainbow_domain)


@cli.command('updateCccaCfg')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--apiserver', help='API server FQDN')
def cli_update_ccca_cfg(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    api_server = kwargs.get('apiserver')
    if api_server is None:
        print('--api_server option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_update_ccca_cfg_dev_all_in_one(ip, port, password, api_server)


@cli.command('purgeCccaCfg')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--apiserver', help='API server FQDN')
def cli_purge_ccca_cfg(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_purge_ccca_cfg(ip, port, password)


# OXE information

@cli.command('getRainbowAgentVersion')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='mtcl password', default='letacla')
def cli_get_rainbow_agent_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_get_rainbow_agent_version(ip, port, password)


@cli.command('getOxeVersion')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_version(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_get_oxe_version(ip, port, password)


# OXE commands

@cli.command('oxeReboot')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--swinstPassword', help='swinst password', default='SoftInst')
def cli_oxe_reboot(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    swinst_password = kwargs.get('swinstpassword')
    oxe_reboot(ip, port, password, swinst_password)


@cli.command('killRainbowAgent')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='swinst password', default='letacla')
def cli_kill_rainbow_agent(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    root_password = kwargs.get('rootpassword')
    oxe_kill_rainbow_agent(ip, port, password, root_password)


@cli.command('runmao')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runmao(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_runmao(ip, port, password)


@cli.command('runtel')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runtel(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    password = kwargs.get('password')
    oxe_runtel(ip, port, password)


# SIP management

@cli.command('enableSip')
@click.option('--trkId', help='Trunk ID for SIP', default=15)
def cli_enable_sip(trkid):
    token, host = oxe_get_auth_from_cache()
    oxe_sip_create_default_trunk_groups(host, token, trkid)
    oxe_sip_gateway(host, token, trkid)
    oxe_sip_proxy(host, token)
    oxe_ip_domain_deactivate_compression_default_ip_domain(host, token)
    oxe_system_compression_type(host, token, 'G_729')
    oxe_system_law(host, token, 'Law_A')
    oxe_system_accept_mu_a_laws_in_sip(host, token, 'true')
    oxe_system_alaw_to_mulaw(host, token, 'true')


# System options

@cli.command('enableUcaasCstaMonitored')
@click.option('--sessions', help='CSTA sessions monitored', default=20000)
def cli_enable_ucaas_csta_sessions_monitored(sessions):
    token, host = oxe_get_auth_from_cache()
    oxe_system_csta_sessions_monitored(host, token, sessions)


@cli.command('systemLaw')
@click.option('--law', help='System law', type=click.Choice(['Law_A', 'Law_Mu']), default='Law_A')
def cli_system_law(law):
    token, host = oxe_get_auth_from_cache()
    oxe_system_law(host, token, law)


@cli.command('systemCompression')
@click.option('--compression', help='System compression', type=click.Choice(['G_729', 'G_723']), default='G_729')
def cli_system_compression(compression):
    token, host = oxe_get_auth_from_cache()
    oxe_system_compression_type(host, token, compression)


@cli.command('reportNodeNumber')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_report_node_number(ip, port, password):
    token, host = oxe_get_auth_from_cache()
    if ip is not None:
        node_number = oxe_netdata_get(ip, 'NODE_NBER', port, password)
    else:
        node_number = oxe_netdata_get(host, 'NODE_NBER', port, password)
    oxe_system_node_number(host, token, node_number)


@cli.command('reportNetNumber')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_report_node_number(ip, port, password):
    token, host = oxe_get_auth_from_cache()
    if ip is not None:
        net_number = oxe_netdata_get(ip, 'NET_NBER', port, password)
    else:
        net_number = oxe_netdata_get(host, 'NET_NBER', port, password)
    oxe_system_network_number(host, token, net_number)


# OMS management

@cli.command('createShelf')
@click.option('--shelfId', help='shelf id', default=10)
# @click.option('--rackSize', help='shelf rack size', default='MediaGateway_Large')
def cli_shelf_create(shelfid, racksize=None):
    token, host = oxe_get_auth_from_cache()
    oxe_create_shelf(host, token, shelfid, 'MediaGateway_Large')


@cli.command('shelfEthernetParameters')
@click.option('--shelfId', help='shelf id', default=None)
@click.option('--mac', help='shelf MAC address', default=None)
def cli_shelf_ethernet_parameters(shelfid, mac):
    if shelfid is None:
        print('--shelfId option is mandatory. Exiting ...')
        exit(-1)
    if mac is None:
        print('--mac option is mandatory. Exiting ...')
        exit(-1)
    token, host = oxe_get_auth_from_cache()
    oxe_shelf_ethernet_parameters(host, token, shelfid, mac)


@cli.command('setOmsCompressors')
@click.option('--shelfId', help='shelf id', default=10)
@click.option('--compressors', help='number of compressors for IP devices', default=120)
def cli_shelf_ethernet_parameters(shelfid, compressors):
    token, host = oxe_get_auth_from_cache()
    oxe_shelf_ethernet_parameters(host, token, shelfid, compressors)


@cli.command('omsConfig')
@click.option('--ip', help='OMS IP address')
@click.option('--port', help='OMS SSH port', default=22)
@click.option('--login', help='User login', default='admin')
@click.option('--password', help='User password', default='letacla1')
@click.option('--rootPassword', help='root password', default='letacla1')
@click.option('--callServer', help='main CallServer')
def cli_oms_config(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    call_server = kwargs.get('callserver')
    if call_server is None:
        print('--callServer option is mandatory. Exiting ...')
        exit(-1)
    port = kwargs.get('port')
    login = kwargs.get('login')
    password = kwargs.get('password')
    swinst_password = kwargs.get('rootpassword')
    oms_omsconfig(ip, port, login, password, swinst_password, call_server)


# Translator management

@cli.command('createDpnssPrefix')
@click.option('--dpnss', help='DPNSS prefix number', default='A1000')
def cli_oxe_translator_prefix_create_dpnss(dpnss):
    token, host = oxe_get_auth_from_cache()
    oxe_translator_prefix_create_dpnss(host, token, dpnss)


# 4645 management

@cli.command('create4645')
@click.option('--number', help='Voice mail number', default=6000)
@click.option('--accesses', help='Voice mail accesses', default=15)
@click.option('--directory', help='Voice mail directory name', default='voicemail')
@click.option('--index', help='Voice mail index', default=1)
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_create_voice_mail(**kwargs):
    token, host = oxe_get_auth_from_cache()
    vm_number = kwargs.get('number')
    vm_accesses = kwargs.get('accesses')
    vm_name = kwargs.get('directory')
    vm_index = kwargs.get('index')
    ip = kwargs.get('ip')
    if ip is None:
        ip = host
    port = kwargs.get('port')
    password = kwargs.get('password')
    vm_create_eva_cfg(host, port, password, vm_accesses)
    vm_create_eva_access(host, port, password, vm_accesses)
    vm_create(host, token, vm_accesses, vm_number, vm_name, vm_index, 'embedded')


@cli.command('delete4645')
def cli_oxe_delete_voice_mail():
    token, host = oxe_get_auth_from_cache()
    vm_create(host, token, vm_number='')


# netadmin management

@cli.command('setDns')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--dns1', help='DNS1 IP address', default=None)
@click.option('--dns2', help='DNS2 IP address', default='127.0.0.1')
def cli_netadmin_dns(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    dns1 = kwargs.get('dns1')
    if dns1 is None:
        print('--dns1 option is mandatory. Exiting ...')
        exit(-1)
    oxe_netdata_update(ip,
                       'DNSPRIMADDR=' + kwargs.get('dns1') + '\nDNSSECADDR=' + kwargs.get('dns2'),
                       kwargs.get('port'),
                       kwargs.get('password'),
                       kwargs.get('rootpassword'))


@cli.command('setProxy')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--proxyAddr', help='Proxy IP address', default=None)
@click.option('--proxyPort', help='Proxy port', default=None)
@click.option('--proxyUser', help='Proxy login', default='')
@click.option('--proxyPassword', help='Proxy port', default='')
def cli_netadmin_proxy(**kwargs):
    ip = kwargs.get('ip')
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    proxy_address = kwargs.get('proxyaddr')
    if proxy_address is None:
        print('--proxyAddr option is mandatory. Exiting ...')
        exit(-1)
    proxy_port = kwargs.get('proxyport')
    if proxy_port is None:
        print('--proxyPort option is mandatory. Exiting ...')
        exit(-1)
    proxy_data = 'PROXYADDR=' + proxy_address + '\nPROXYPORT=' + proxy_port
    proxy_user = kwargs.get('proxyuser')
    if proxy_user != '':
        proxy_data += '\nPROXYUSER=' + proxy_user
    proxy_data += '\nPROXYPASSWD=' + kwargs.get('proxypassword')
    oxe_netdata_update(ip, proxy_data, kwargs.get('port'), kwargs.get('password'), kwargs.get('rootpassword'))


# Logs utilities

@cli.command('oxeLogSh')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_log_sh(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_log_sh(ip, password)


# SIPp management
@cli.command('sippCreateCsv')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--ip', help='OXE IP address')
def cli_create_sipp_csv(**kwargs):
    range_size = int(kwargs.get('rangesize', 1))
    range_start = int(kwargs.get('rangestart', 8000))
    ip_address = kwargs.get('ip')
    sipp_csv_generator(ip_address + '_' + str(range_size) + 'users', ip_address, range_start, range_size, '0000')


@cli.command('sippCustomizeUacRegisterXml')
@click.option('--filename', help='destination', default='sipp_uac_register.xml')
@click.option('--registrationTimer', help='first internal number', default=1800)
def cli_customize_sipp_uac_register_xml(**kwargs):
    registration_timer = int(kwargs.get('registrationtimer', 1800))
    filename = kwargs.get('filename')
    sipp_register_uac_xml_customize(filename, registration_timer)


# pilot2a management


# nginx rp management
@cli.command('nginxRpConfig')
@click.option('--host', help='OXE hostname')
@click.option('--domain', help='OXE domain part', default='rainbow.tech-systems.fr')
@click.option('--cert', help='certificate', default='01-tech-systems.crt')
@click.option('--key', help='key', default='01-tech-systems.key')
@click.option('--bindIp', help='nginx bind ip', default='10.100.0.90')
def cli_create_nginx_rp_config(**kwargs):
    host = kwargs.get('host', None)
    if host is None:
        print('--host option is mandatory. Exiting ...')
        exit(-1)
    nginx_rp_oxe_config(host, kwargs.get('domain'), kwargs.get('cert'), kwargs.get('key'), kwargs.get('bindip'))
