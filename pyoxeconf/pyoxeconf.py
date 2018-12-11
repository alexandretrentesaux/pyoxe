#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Summary

Attributes:
    CONTEXT_SETTINGS (TYPE): Description
    MAX_COLUMN_WIDTHS (TYPE): Description
    STYLES (TYPE): Description
    TITLES (TYPE): Description
"""

# Here go you application specific code.

import click
import progressbar
from _datetime import datetime
from json import loads, dumps
from pkg_resources import require
from pprint import pprint
from sys import exit
from os.path import exists, join
from tempfile import gettempdir
from clickclick import AliasedGroup
from pyoxeconf.__init__ import __version__
from pyoxeconf.oxe_commands import *
from pyoxeconf.oxe_access import oxe_get_auth_from_cache, oxe_logout, oxe_logout_all, oxe_configure, oxe_get_config, \
    oxe_authenticate, oxe_wbm_update_requests_quota, oxe_wbm_restart
from pyoxeconf.oxe_info import oxe_get_json_model, oxe_get_oxe_version, oxe_get_rainbow_agent_version
from pyoxeconf.oxe_users import oxe_create_phonebook_entry, oxe_create_user, oxe_delete_user
from pyoxeconf.oxe_rainbow import oxe_get_rainbow_config, oxe_purge_ccca_cfg, oxe_purge_rainbowagent_logs, \
    oxe_rainbow_connect, oxe_rainbow_disconnect, oxe_rainbow_reconnect, oxe_update_ccca_cfg_dev_all_in_one
from pyoxeconf.oxe_licensing import oxe_set_flex
from pyoxeconf.oxe_sip import oxe_sip_create_default_trunk_groups, oxe_sip_gateway, oxe_sip_proxy
from pyoxeconf.oxe_shelves import oxe_create_shelf, oxe_shelf_board_compressors_for_ip_devices, \
    oxe_shelf_ethernet_parameters
from pyoxeconf.oxe_systems import oxe_system_accept_mu_a_laws_in_sip, oxe_system_alaw_to_mulaw, \
    oxe_system_compression_type, oxe_system_law, oxe_system_network_number, oxe_system_node_number, \
    oxe_system_ucaas_csta_sessions_monitored
from pyoxeconf.oxe_ip_domains import oxe_ip_domain_deactivate_compression_default_ip_domain
from pyoxeconf.oxe_translator import oxe_translator_prefix_create_dpnss
from pyoxeconf.oxe_netadmin import oxe_netdata_get, oxe_netdata_update
from pyoxeconf.oms_config import oms_omsconfig
from pyoxeconf.sipp import sipp_csv_generator, sipp_register_uac_xml_customize
from pyoxeconf.oxe_log import oxe_log_sh
from pyoxeconf.nginx_rp import nginx_rp_oxe_config
from pyoxeconf.oxe_data_model import oxe_data_model
from pyoxeconf.oxe_voicemail import vm_create, vm_create_eva_access, vm_create_eva_cfg


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
    """Summary
    
    Args:
        ctx (TYPE): Description
        param (TYPE): Description
        value (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    if not value or ctx.resilient_parsing:
        return
    pprint(require("pyoxeconf")[0])
    click.echo('pyoxeconf_cli version: {}'.format(__version__))
    ctx.exit()


def check_host_option(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    if host is None:
        print('--host option is mandatory')
        exit(-1)


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
    """Summary
    """
    pass


# OXE access methods

@cli.command('configure')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
def cli_oxe_access_configure(host, password, proxies):
    """Summary
    
    Args:
        host (TYPE): Description
        password (TYPE): Description
        proxies (TYPE): Description
    """
    check_host_option(host)
    oxe_configure(host, 'mtcl', password, proxies)


@cli.command('connect')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--proxies', help='API server FQDN', default=None)
@click.option('--ini', help='Config File', is_flag=True)
def cli_oxe_access_connect(host, password, proxies, ini):
    """Summary
    
    Args:
        host (TYPE): Description
        password (TYPE): Description
        proxies (TYPE): Description
        ini (TYPE): Description
    """
    check_host_option(host)
    if ini is True:
        password, proxies = oxe_get_config(str(host))
    oxe_authenticate(host, 'mtcl', password, proxies)


@cli.command('logout')
@click.option('--host', help='OXE IP address / FQDN', default=None)
def cli_oxe_access_logout(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    if host is not None:
        oxe_logout(host)
    else:
        oxe_logout_all()


@cli.command('wbmRequestsLimit')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
def cli_oxe_access_wbm_requests_limit(host, port, password, rootpassword):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        rootpassword (TYPE): Description
    """
    check_host_option(host)
    oxe_wbm_update_requests_quota(host, port, password, rootpassword)


@cli.command('wbmRestart')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_wbm_restart(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_wbm_restart(host, port, password)


# JSON model

@cli.command('getJsonModel')
@click.option('--host', help='OXE IP address / FQDN', default=None)
def cli_get_json_model(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(str(host))
    json_model = loads(oxe_get_json_model(host, token))
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    with open(join(gettempdir(), 'OXE_' + host + '_' + timestamp + '.json'), 'w') as fh:
        fh.write(dumps(json_model, indent=2, sort_keys=True))


# Users management

@cli.command('createUsers')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--setType',
              help='set type',
              type=click.Choice(oxe_data_model()['definitions']['Station_Type']['values']),
              default='SIP_Extension')
@click.option('--companyId', help='Company Index', default=1)
@click.option('--sipp', help='Generate SIPp csv file', is_flag=True)
def cli_create_users(host, rangesize, rangestart, settype, companyid, sipp):
    """Summary
    
    Args:
        host (TYPE): Description
        rangesize (TYPE): Description
        rangestart (TYPE): Description
        settype (TYPE): Description
        companyid (TYPE): Description
        sipp (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(int(rangestart), int(rangestart) + int(rangesize))):
        last_name = 'LC' + '{:02}'.format(companyid) + 'U' + str(extension_number)
        first_name = 'FC' + '{:02}'.format(companyid) + 'U' + str(extension_number)
        oxe_create_user(host, token, extension_number, last_name, first_name, settype, 10)
    if settype == 'SIP_Extension' and sipp is True:
        sipp_csv_generator(host + '_' + str(rangesize) + 'users', host, rangestart, rangesize, '0000')


@cli.command('deleteUsers')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
def cli_delete_users(host, rangesize, rangestart):
    """Summary
    
    Args:
        host (TYPE): Description
        rangesize (TYPE): Description
        rangestart (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    bar = progressbar.ProgressBar()
    for extension_number in bar(range(int(rangestart), int(rangestart) + int(rangesize))):
        oxe_delete_user(host, token, extension_number, 10)


@cli.command('createPhonebookEntries')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--alias', help='directory alias', default=255)
def cli_create_phonebook_entries(host, rangesize, rangestart, alias):
    """Summary
    
    Args:
        host (TYPE): Description
        rangesize (TYPE): Description
        rangestart (TYPE): Description
        alias (TYPE): Description
    """
    print('Debug ongoing, OXE API is not working properly with the following request\n')
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    bar = progressbar.ProgressBar()
    if 0 <= alias <= 15 or alias == 255:
        for extension_number in bar(range(rangestart, rangestart + rangesize)):
            oxe_create_phonebook_entry(host, token, extension_number, 'pb_ln' + str(extension_number),
                                       'pb_fn' + str(extension_number), alias, 10)
    else:
        print('--alias value must be in following ranges 0 to 15, 255')
        exit(-1)


# Licenses management

@cli.command('setFlexServer')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--flexIp', help='External Flex server IP address', default=None)
@click.option('--port', help='External Flex port', default=27000)
@click.option('--reboot', help='Reboot CS to apply settings', is_flag=True)
@click.option('--sshPort', help='OXE SSH port / needed if --reboot', default=22)
@click.option('--password', help='mtcl password / needed if --reboot', default='mtcl')
@click.option('--swinstPassword', help='swinst password / needed if --reboot', default='SoftInst')
def cli_oxe_licensing_set_flex_server(host, flexip, port, reboot, sshport, password, swinstpassword):
    """Summary
    
    Args:
        host (TYPE): Description
        flexip (TYPE): Description
        port (TYPE): Description
        reboot (TYPE): Description
        sshport (TYPE): Description
        password (TYPE): Description
        swinstpassword (TYPE): Description
    """
    check_host_option(host)
    if flexip is None:
        print('--ip option is mandatory. Exiting ...')
        exit(-1)
    token = oxe_get_auth_from_cache(host)
    oxe_set_flex(host, token, flexip, port)
    print('WARNING: OXE must be rebooted')
    if reboot is True:
        oxe_reboot(host, sshport, password, swinstpassword)


# Rainbow connection management

@cli.command('rainbowConnect')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--rainbowDomain', help='Rainbow Domain', default=None)
@click.option('--pbxId', help='PBX Rainbow ID', default=None)
@click.option('--phoneBook', help='Send OXE phone book to Rainbow', default='Yes')
@click.option('--activationCode', help='PBX activation code', default=None)
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_oxe_rainbow_rainbow_connect(host, rainbowdomain, pbxid, phonebook, activationcode, ini, filename):
    """Summary
    
    Args:
        host (TYPE): Description
        rainbowdomain (TYPE): Description
        pbxid (TYPE): Description
        phonebook (TYPE): Description
        activationcode (TYPE): Description
        ini (TYPE): Description
        filename (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
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
@click.option('--host', help='OXE IP address / FQDN', default=None)
def cli_oxe_rainbow_rainbow_disconnect(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    token = oxe_get_auth_from_cache(host)
    oxe_rainbow_disconnect(host, token)


@cli.command('rainbowReconnect')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--pbxId', help='PBX Rainbow ID', default=None)
@click.option('--rainbowDomain', help='Rainbow Domain', default=None)
@click.option('--ini', help='config file use', is_flag=True)
@click.option('--filename', help='config file name', default=None)
def cli_oxe_rainbow_rainbow_reconnect(host, pbxid, rainbowdomain, ini, filename):
    """Summary
    
    Args:
        host (TYPE): Description
        pbxid (TYPE): Description
        rainbowdomain (TYPE): Description
        ini (TYPE): Description
        filename (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    if ini is False:
        if pbxid is None:
            print('--pbxId option is mandatory. Exiting ...')
            exit(-1)
        if rainbowdomain is None:
            print('--rainbowDomain option is mandatory. Exiting ...')
            exit(-1)
    else:
        rainbowdomain, pbxid, activation_code, rainbow_host = oxe_get_rainbow_config(filename)
    oxe_rainbow_reconnect(host, token, pbxid, rainbowdomain)


@cli.command('updateCccaCfg')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--apiServer', help='API server FQDN', default=None)
def cli_oxe_rainbow_update_ccca_cfg(host, port, password, apiserver):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        apiserver (TYPE): Description
    """
    check_host_option(host)
    if apiserver is None:
        print('--apiServer option is mandatory. Exiting ...')
        exit(-1)
    oxe_update_ccca_cfg_dev_all_in_one(host, port, password, apiserver)


@cli.command('purgeCccaCfg')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_rainbow_purge_ccca_cfg(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_purge_ccca_cfg(host, port, password)


@cli.command('purgeRainbowagentLogs')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
def cli_purge_rainbowagent_logs(host, port, password, rootpassword):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_purge_rainbowagent_logs(host, port, password, rootpassword)


# OXE information

@cli.command('getRainbowAgentVersion')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_info_get_rainbow_agent_version(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_get_rainbow_agent_version(host, port, password)


@cli.command('getOxeVersion')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_version(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_get_oxe_version(host, port, password)


# OXE commands

@cli.command('oxeReboot')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--swinstPassword', help='swinst password', default='SoftInst')
def cli_oxe_reboot(host, port, password, swinstpassword):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        swinstpassword (TYPE): Description
    """
    check_host_option(host)
    oxe_reboot(host, port, password, swinstpassword)


@cli.command('killRainbowAgent')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='swinst password', default='letacla')
def cli_kill_rainbow_agent(host, port, password, rootpassword):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        rootpassword (TYPE): Description
    """
    check_host_option(host)
    oxe_kill_rainbow_agent(host, port, password, rootpassword)


@cli.command('runmao')
@click.option('--host', help='OXE IP address', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runmao(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_runmao(host, port, password)


@cli.command('runtel')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_runtel(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_runtel(host, port, password)


# SIP management

@cli.command('enableSip')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--trkId', help='Trunk ID for SIP', default=15)
def cli_enable_sip(host, trkid):
    """Summary
    
    Args:
        host (TYPE): Description
        trkid (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
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
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--sessions', help='CSTA sessions monitored', default=20000)
def cli_enable_ucaas_csta_sessions_monitored(host, sessions):
    """Summary
    
    Args:
        host (TYPE): Description
        sessions (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_system_ucaas_csta_sessions_monitored(host, token, sessions)


@cli.command('systemLaw')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--law',
              help='System law',
              type=click.Choice(oxe_data_model()['definitions']['Law_MG']['values']),
              default='Law_A')
def cli_system_law(host, law):
    """Summary
    
    Args:
        host (TYPE): Description
        law (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_system_law(host, token, law)


@cli.command('systemCompression')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--compression',
              help='System compression',
              type=click.Choice(oxe_data_model()['Node']['subClasses']['System_Parameters']['subClasses']
                                ['System_Parameters_2']['subClasses']['Compression_Parameters']['attributes']
                                ['Compression_Type']['type']['values']),
              default='G_729')
def cli_system_compression(host, compression):
    """Summary
    
    Args:
        host (TYPE): Description
        compression (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_system_compression_type(host, token, compression)


@cli.command('reportNodeNumber')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_report_node_number(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    node_number = oxe_netdata_get(host, 'NODE_NBER', port, password)
    oxe_system_node_number(host, token, node_number)


@cli.command('reportNetNumber')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_report_node_number(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    net_number = oxe_netdata_get(host, 'NET_NBER', port, password)
    oxe_system_network_number(host, token, net_number)


# OMS management

@cli.command('createShelf')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--shelfId', help='shelf id', default=10)
@click.option('--rackSize', help='shelf rack size',
              type=click.Choice(oxe_data_model()['definitions']['Rack_Type_Media_Gateway']['values']),
              default=oxe_data_model()['definitions']['Rack_Type_Media_Gateway']['defaultValue'])
def cli_oxe_shelf_create(host, shelfid, racksize):
    """Summary
    
    Args:
        host (TYPE): Description
        shelfid (TYPE): Description
        racksize (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_create_shelf(host, token, shelfid, racksize)


@cli.command('shelfEthernetParameters')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--shelfId', help='shelf id', default=None)
@click.option('--mac', help='shelf MAC address', default=None)
def cli_oxe_shelf_ethernet_parameters(host, shelfid, mac):
    """Summary
    
    Args:
        host (TYPE): Description
        shelfid (TYPE): Description
        mac (TYPE): Description
    """
    check_host_option(host)
    if shelfid is None:
        print('--shelfId option is mandatory. Exiting ...')
        exit(-1)
    if mac is None:
        print('--mac option is mandatory. Exiting ...')
        exit(-1)
    token = oxe_get_auth_from_cache(host)
    oxe_shelf_ethernet_parameters(host, token, shelfid, mac)


@cli.command('setOmsCompressors')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--shelfId', help='shelf id', default=10)
@click.option('--compressors', help='number of compressors for IP devices', default=120)
def cli_oxe_shelf_board_compressors_for_ip_devices(host, shelfid, compressors):
    """Summary
    
    Args:
        host (TYPE): Description
        shelfid (TYPE): Description
        compressors (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_shelf_board_compressors_for_ip_devices(host, token, shelfid, compressors)


@cli.command('omsConfig')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OMS SSH port', default=22)
@click.option('--login', help='User login', default='admin')
@click.option('--password', help='User password', default='letacla1')
@click.option('--rootPassword', help='root password', default='letacla1')
@click.option('--callServer', help='main CallServer', default=None)
def cli_oms_config(host, port, login, password, rootpassword, callserver):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        login (TYPE): Description
        password (TYPE): Description
        rootpassword (TYPE): Description
        callserver (TYPE): Description
    """
    check_host_option(host)
    if callserver is None:
        print('--callServer option is mandatory. Exiting ...')
        exit(-1)
    oms_omsconfig(host, port, login, password, rootpassword, callserver)


# Translator management

@cli.command('createDpnssPrefix')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--dpnss', help='DPNSS prefix number', default='A1000')
def cli_oxe_translator_prefix_create_dpnss(host, dpnss):
    """Summary
    
    Args:
        host (TYPE): Description
        dpnss (TYPE): Description
    """
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    oxe_translator_prefix_create_dpnss(host, token, dpnss)


# 4645 management

@cli.command('create4645')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--number', help='Voice mail number', default=6000)
@click.option('--accesses', help='Voice mail accesses', default=15)
@click.option('--directory', help='Voice mail directory name', default='voicemail')
@click.option('--index', help='Voice mail index', default=1)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_create_voice_mail(**kwargs):
    """Summary
    
    Args:
        **kwargs: Description
    """
    print('test on going on this feature\n')
    host = kwargs.get('host')
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    vm_number = kwargs.get('number')
    vm_accesses = kwargs.get('accesses')
    vm_name = kwargs.get('directory')
    vm_index = kwargs.get('index')
    port = kwargs.get('port')
    password = kwargs.get('password')
    vm_create_eva_cfg(host, port, password, vm_accesses)
    vm_create_eva_access(host, port, password, vm_accesses)
    vm_create(host, token, vm_accesses, vm_number, vm_name, vm_index, 'embedded')


@cli.command('delete4645')
@click.option('--host', help='OXE IP address / FQDN', default=None)
def cli_oxe_delete_voice_mail(host):
    """Summary
    
    Args:
        host (TYPE): Description
    """
    print('test on going on this feature\n')
    check_host_option(host)
    token = oxe_get_auth_from_cache(host)
    vm_create(host, token, vm_number='')


# netadmin management

@cli.command('setDns')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--dns1', help='DNS1 IP address', default=None)
@click.option('--dns2', help='DNS2 IP address', default='127.0.0.1')
def cli_netadmin_dns(host, port, password, rootpassword, dns1, dns2):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        rootpassword (TYPE): Description
        dns1 (TYPE): Description
        dns2 (TYPE): Description
    """
    check_host_option(host)
    if dns1 is None:
        print('--dns1 option is mandatory. Exiting ...')
        exit(-1)
    oxe_netdata_update(host, 'DNSPRIMADDR=' + dns1 + '\nDNSSECADDR=' + dns2, port, password, rootpassword)


@cli.command('setProxy')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
@click.option('--rootPassword', help='root password', default='letacla')
@click.option('--proxyAddr', help='Proxy IP address', default=None)
@click.option('--proxyPort', help='Proxy port', default=None)
@click.option('--proxyUser', help='Proxy login', default='')
@click.option('--proxyPassword', help='Proxy port', default='')
def cli_netadmin_proxy(host, port, password, rootpassword, proxyaddr, proxyport, proxyuser, proxypassword):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
        rootpassword (TYPE): Description
        proxyaddr (TYPE): Description
        proxyport (TYPE): Description
        proxyuser (TYPE): Description
        proxypassword (TYPE): Description
    """
    check_host_option(host)
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
    oxe_netdata_update(host, proxy_data, port, password, rootpassword)


# Logs utilities

@cli.command('oxeLogSh')
@click.option('--host', help='OXE IP address / FQDN', default=None)
@click.option('--port', help='OXE SSH port', default=22)
@click.option('--password', help='mtcl password', default='mtcl')
def cli_oxe_log_sh(host, port, password):
    """Summary
    
    Args:
        host (TYPE): Description
        port (TYPE): Description
        password (TYPE): Description
    """
    check_host_option(host)
    oxe_log_sh(host, port, password)


# SIPp management
@cli.command('sippCreateCsv')
@click.option('--rangeSize', help='range of users to create', default=1)
@click.option('--rangeStart', help='first internal number', default=8000)
@click.option('--callserver', help='OXE IP address', default=None)
@click.option('--sippassword', help='SIP password', default='0000')
def cli_create_sipp_csv(rangesize, rangestart, callserver, sippassword):
    """Summary
    
    Args:
        rangesize (TYPE): Description
        rangestart (TYPE): Description
        callserver (TYPE): Description
        sippassword (TYPE): Description
    """
    if callserver is None:
        print('--callServer option is mandatory. Exiting ...')
        exit(-1)
    sipp_csv_generator(callserver + '_' + str(rangesize) + 'users', callserver, rangestart, rangesize, sippassword)


@cli.command('sippCustomizeUacRegisterXml')
@click.option('--filename', help='destination', default='sipp_uac_register.xml')
@click.option('--registrationTimer', help='first internal number', default=1800)
def cli_customize_sipp_uac_register_xml(filename, registrationtimer):
    """Summary
    
    Args:
        filename (TYPE): Description
        registrationtimer (TYPE): Description
    """
    sipp_register_uac_xml_customize(filename, registrationtimer)


# pilot2a management
# todo: manage all prerequistes for pilot2a use


# nginx rp management
@cli.command('nginxRpConfig')
@click.option('--host', help='OXE hostname', default=None)
@click.option('--domain', help='OXE domain part', default='rainbow.tech-systems.fr')
@click.option('--cert', help='certificate', default='01-tech-systems.crt')
@click.option('--key', help='key', default='01-tech-systems.key')
@click.option('--bindIp', help='nginx bind ip', default='10.100.0.90')
def cli_create_nginx_rp_config(host, domain, cert, key, bindip):
    """Summary
    
    Args:
        host (TYPE): Description
        domain (TYPE): Description
        cert (TYPE): Description
        key (TYPE): Description
        bindip (TYPE): Description
    """
    check_host_option(host)
    nginx_rp_oxe_config(host, domain, cert, key, bindip)
