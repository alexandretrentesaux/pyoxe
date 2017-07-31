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
from pyoxeconf.oxe_data_model import oxe_model


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
@click.option('-V',
              '--version',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


# OXE access methods

@cli.command('configure')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_oxe_access_configure(host, password, proxies):
    if host is None:
        print('--host option is mandatory')
        exit(-1)
    oxe_configure(host, 'mtcl', password, proxies)


@cli.command('connect')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
@click.option('--ini', help='Config File', is_flag=True)
def cli_oxe_access_connect(host, password, proxies, ini):
    if ini is False:
        if host is None:
            print('--host option is mandatory')
            exit(-1)
    else:
        host, login, password, proxies = oxe_get_config()
    oxe_authenticate(host, 'mtcl', password, proxies)


@cli.command('logout')
def cli_oxe_access_logout():
    oxe_logout()


@cli.command('wbmRequestsLimit')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
def cli_oxe_access_wbm_requests_limit(ip, port, password, rootpassword):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_wbm_update_requests_quota(ip, port, password, rootpassword)


@cli.command('wbmRestart')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_wbm_restart(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_wbm_restart(ip, port, password)


# JSON model

@cli.command('getJsonModel')
def cli_get_json_model():
    token, host = oxe_get_auth_from_cache()
    json_model = json.loads(oxe_get_json_model(host, token))
    horodating = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open(os.path.join(tempfile.gettempdir(), 'OXE_' + host + '_' + horodating + '.json'), 'w') as fh:
        fh.write(json.dumps(json_model, indent=2, sort_keys=True))


# Users management

@cli.command('createUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--setType',
              help='set type',
              type=click.Choice(oxe_model['definitions']['Station_Type']['values']),
              default='SIP_Extension')
@click.option('--companyId', help='Company Index', default=1)
@click.option('--sipp', help='Generate SIPp csv file', is_flag=True)
def cli_create_users(rangesize, rangestart, settype, companyid, sipp):
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(int(rangestart), int(rangestart) + int(rangesize))):
        if companyid < 10:
            last_name = 'LC0' + str(companyid) + 'U' + str(extension_number)
            first_name = 'FC0' + str(companyid) + 'U' + str(extension_number)
        else:
            last_name = 'LC0' + str(companyid) + 'U' + str(extension_number)
            first_name = 'FC0' + str(companyid) + 'U' + str(extension_number)
        oxe_create_user(host, token, extension_number, last_name, first_name, settype, 10)
    if settype == 'SIP_Extension' and sipp is True:
        sipp_csv_generator(host + '_' + str(rangesize) + 'users', host, rangestart, rangesize, '0000')


@cli.command('deleteUsers')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
def cli_delete_users(rangesize, rangestart):
    token, host = oxe_get_auth_from_cache()
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(int(rangestart), int(rangestart) + int(rangesize))):
        oxe_delete_user(host, token, extension_number, 10)


@cli.command('createPhonebookEntries')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--alias', help='directory alias', default=255)
def cli_create_phonebook_entries(**kwargs):
    print('Debug ongoing, OXE API is not working properly with the following request\n')
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
@click.option('--ip', help='External Flex server IP address', default=None)
@click.option('--port', help='External Flex port', default=27000)
@click.option('--reboot', help='Reboot CS to apply settings', is_flag=True)
@click.option('--sshPort', help='OXE SSH port / needed if --reboot', default=22)
@click.option('--password', help='mtcl password / needed if --reboot', default='mtcl')
@click.option('--swinstPassword', help='swinst password / needed if --reboot', default='SoftInst')
def cli_oxe_licensing_set_flex_server(ip, port, reboot, sshport, password, swinstpassword):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    token, host = oxe_get_auth_from_cache()
    oxe_set_flex(host, token, ip, port)
    print('WARNING: OXE must be rebooted')
    if reboot is True:
        oxe_reboot(host, sshport, password, swinstpassword)


# Rainbow connection management

@cli.command('rainbowConnect')
@click.option('--rainbowDomain', help='Rainbow Domain', default=None)
@click.option('--pbxId', help='PBX Rainbow ID', default=None)
@click.option('--phoneBook', help='Send OXE phone book to Rainbow', default='Yes')
@click.option('--activationCode', help='PBX activation code', default=None)
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_oxe_rainbow_rainbow_connect(rainbowdomain, pbxid, phonebook, activationcode, ini, filename):
    token, host = oxe_get_auth_from_cache()
    if ini is False:
        if rainbowdomain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit(-1)
        if pbxid is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit(-1)
        if activationcode is None:
            print('--activationCode option is mandatory. Exiting ...')
            exit(-1)
    else:
        rainbowdomain, pbxid, activationcode, rainbowhost = oxe_get_rainbow_config(filename)
    oxe_rainbow_connect(host, token, rainbowdomain, pbxid, activationcode, phonebook)


@cli.command('rainbowDisconnect')
def cli_oxe_rainbow_rainbow_disconnect():
    token, host = oxe_get_auth_from_cache()
    oxe_rainbow_disconnect(host, token)


@cli.command('rainbowReconnect')
@click.option('--pbxId', help='PBX Rainbow ID', default=None)
@click.option('--rainbowDomain', help='Rainbow Domain', default=None)
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_oxe_rainbow_rainbow_reconnect(pbxid, rainbowdomain, ini, filename):
    token, host = oxe_get_auth_from_cache()
    if ini is False:
        if pbxid is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit(-1)
        if rainbowdomain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit(-1)
    else:
        rainbow_domain, pbx_id, activation_code, rainbow_host = oxe_get_rainbow_config(filename)
    oxe_rainbow_reconnect(host, token, pbx_id, rainbow_domain)


@cli.command('updateCccaCfg')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--apiServer', help='API server FQDN', default=None)
def cli_oxe_rainbow_update_ccca_cfg(ip, port, password, apiserver):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    if apiserver is None:
        print('--apiServer option is mandatory. Exiting ...')
        exit(-1)
    oxe_update_ccca_cfg_dev_all_in_one(ip, port, password, apiserver)


@cli.command('purgeCccaCfg')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_rainbow_purge_ccca_cfg(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_purge_ccca_cfg(ip, port, password)


# OXE information

@cli.command('getRainbowAgentVersion')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_info_get_rainbow_agent_version(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_get_rainbow_agent_version(ip, port, password)


@cli.command('getOxeVersion')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_version(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_get_oxe_version(ip, port, password)


# OXE commands

@cli.command('oxeReboot')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--swinstPassword', help='swinst password', default='SoftInst')
def cli_oxe_reboot(ip, port, password, swinstpassword):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_reboot(ip, port, password, swinstpassword)


@cli.command('killRainbowAgent')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='swinst password', default='letacla')
def cli_kill_rainbow_agent(ip, port, password, rootpassword):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_kill_rainbow_agent(ip, port, password, rootpassword)


@cli.command('runmao')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runmao(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_runmao(ip, port, password)


@cli.command('runtel')
@click.option('--ip', help='OXE IP address')
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runtel(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
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
    oxe_system_compression_type(host, token)
    oxe_system_law(host, token)
    oxe_system_accept_mu_a_laws_in_sip(host, token, 'true')
    oxe_system_alaw_to_mulaw(host, token, 'true')


# System options

@cli.command('enableUcaasCstaMonitored')
@click.option('--sessions', help='CSTA sessions monitored', default=20000)
def cli_enable_ucaas_csta_sessions_monitored(sessions):
    token, host = oxe_get_auth_from_cache()
    oxe_system_csta_sessions_monitored(host, token, sessions)


@cli.command('systemLaw')
@click.option('--law',
              help='System law',
              type=click.Choice(oxe_model['definitions']['Law_MG']['values']),
              default='Law_A')
def cli_system_law(law):
    token, host = oxe_get_auth_from_cache()
    oxe_system_law(host, token, law)


@cli.command('systemCompression')
@click.option('--compression',
              help='System compression',
              type=click.Choice(oxe_model['definitions']['Compression_Type']['values']),
              default='G_729')
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
@click.option('--rackSize', help='shelf rack size',
              type=click.Choice(oxe_model['definitions']['Rack_Type_Media_Gateway']['values']),
              default=oxe_model['definitions']['Rack_Type_Media_Gateway']['defaultValue'])
def cli_oxe_shelf_create(shelfid, racksize):
    token, host = oxe_get_auth_from_cache()
    oxe_create_shelf(host, token, shelfid, racksize)


@cli.command('shelfEthernetParameters')
@click.option('--shelfId', help='shelf id', default=None)
@click.option('--mac', help='shelf MAC address', default=None)
def cli_oxe_shelf_ethernet_parameters(shelfid, mac):
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
def cli_oxe_shelf_board_compressors_for_ip_devices(shelfid, compressors):
    token, host = oxe_get_auth_from_cache()
    oxe_shelf_board_compressors_for_ip_devices(host, token, shelfid, compressors)


@cli.command('omsConfig')
@click.option('--ip', help='OMS IP address', default=None)
@click.option('--port', help='OMS SSH port', default=22)
@click.option('--login', help='User login', default='admin')
@click.option('--password', help='User password', default='letacla1')
@click.option('--rootPassword', help='root password', default='letacla1')
@click.option('--callServer', help='main CallServer', default=None)
def cli_oms_config(ip, port, login, password, rootpassword, callserver):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    if callserver is None:
        print('--callServer option is mandatory. Exiting ...')
        exit(-1)
    oms_omsconfig(ip, port, login, password, rootpassword, callserver)


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
    print('test on going on this feature\n')
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
    print('test on going on this feature\n')
    token, host = oxe_get_auth_from_cache()
    vm_create(host, token, vm_number='')


# netadmin management

@cli.command('setDns')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--dns1', help='DNS1 IP address', default=None)
@click.option('--dns2', help='DNS2 IP address', default='127.0.0.1')
def cli_netadmin_dns(ip, port, password, rootpassword, dns1, dns2):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    if dns1 is None:
        print('--dns1 option is mandatory. Exiting ...')
        exit(-1)
    oxe_netdata_update(ip, 'DNSPRIMADDR=' + dns1 + '\nDNSSECADDR=' + dns2, port, password, rootpassword)


@cli.command('setProxy')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--proxyAddr', help='Proxy IP address', default=None)
@click.option('--proxyPort', help='Proxy port', default=None)
@click.option('--proxyUser', help='Proxy login', default='')
@click.option('--proxyPassword', help='Proxy port', default='')
def cli_netadmin_proxy(ip, port, password, rootpassword, proxyaddr, proxyport, proxyuser, proxypassword):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    if proxyaddr is None:
        print('--proxyAddr option is mandatory. Exiting ...')
        exit(-1)
    if proxyport is None:
        print('--proxyPort option is mandatory. Exiting ...')
        exit(-1)
    proxy_data = 'PROXYADDR=' + proxyaddr + '\nPROXYPORT=' + proxyport
    if proxyuser != '':
        proxy_data += '\nPROXYUSER=' + proxyuser
    proxy_data += '\nPROXYPASSWD=' + proxypassword
    oxe_netdata_update(ip, proxy_data, port, password, rootpassword)


# Logs utilities

@cli.command('oxeLogSh')
@click.option('--ip', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_log_sh(ip, port, password):
    if ip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    oxe_log_sh(ip, port, password)


# SIPp management
@cli.command('sippCreateCsv')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--callserver', help='OXE IP address', default=None)
@click.option('--sippassword', help='SIP password', default='0000')
def cli_create_sipp_csv(rangesize, rangestart, callserver, sippassword):
    if callserver is None:
        print('--callServer option is mandatory. Exiting ...')
        exit(-1)
    sipp_csv_generator(callserver + '_' + str(rangesize) + 'users', callserver, rangestart, rangesize, sippassword)


@cli.command('sippCustomizeUacRegisterXml')
@click.option('--filename', help='destination', default='sipp_uac_register.xml')
@click.option('--registrationTimer', help='first internal number', default=1800)
def cli_customize_sipp_uac_register_xml(filename, registrationtimer):
    sipp_register_uac_xml_customize(filename, registrationtimer)


# pilot2a management
#  todo: manage all prerequistes for pilot2a use


# nginx rp management
@cli.command('nginxRpConfig')
@click.option('--host', help='OXE hostname', default=None)
@click.option('--domain', help='OXE domain part', default='rainbow.tech-systems.fr')
@click.option('--cert', help='certificate', default='01-tech-systems.crt')
@click.option('--key', help='key', default='01-tech-systems.key')
@click.option('--bindIp', help='nginx bind ip', default='10.100.0.90')
def cli_create_nginx_rp_config(host, domain, cert, key, bindip):
    if host is None:
        print('--host option is mandatory. Exiting ...')
        exit(-1)
    nginx_rp_oxe_config(host, domain, cert, key, bindip))


# # test on OmniPCX Data Model
# @cli.command('dataModel')
# @click.option('--pattern', help='search pattern')
# def cli_data_model(pattern):
#     print(json.dumps(oxe_model['definitions']['Station_Type']['values'], indent=2))
#     if pattern in oxe_model['definitions']['Station_Type']['values']:
#         print('Valid Set Type: ' + pattern)
#     else:
#         print('Unknown Set Type: ' + pattern)
