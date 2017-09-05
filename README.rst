=========
Pyoxeconf
=========

Automation tool managing ALE OmniPCX Enterprise configuration. This tools is using OXE REST API (only available for OXE version >= M1.403.15)

Installation
============

::

    pip install git+https://github.com/alexandretrentesaux/pyoxeconf#egg=pyoxeconf

Or in a develop mode after downloading a zip or cloning the git repository ::

    git clone https://github.com/alexandretrentesaux/pyoxeconf
    cd pyoxeconf
    pip install -e .

Or in a develop mode from a git repository ::

    pip install -e git+https://github.com/alexandretrentesaux/pyoxeconf#egg=pyoxeconf

Once installed you can run ::

 pyoxeconf_cli --help



Examples
========

Access methods
--------------

* configure : store configuration in ini file (WBM)

    + pyoxeconf_cli configure --host 10.100.8.10 --password mtcl
    + pyoxeconf_cli configure --host oxe02wbm.rainbow.tech-systems.fr --password mtcl
    + pyoxeconf_cli configure --host 10.100.8.10


* connect : (WBM)

    + pyoxeconf_cli connect --host oxe02wbm.rainbow.tech-systems.fr --password mtcl
    + pyoxeconf_cli connect --host 10.100.8.11 --password 'mtcl'
    + pyoxeconf_cli connect --host 10.100.8.11 --ini


* logout : (WBM)

    + pyoxeconf_cli logout --host 10.100.8.11
    + pyoxeconf_cli logout --host oxe02wbm.rainbow.tech-systems.fr

* change WBM requests quota (SSH)

    + pyoxeconf_cli wbmRequestsLimit --host 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd
    + pyoxeconf_cli wbmRequestsLimit --host oxe05wbm.rainbow.tech-systems.fr --port 22 --password mtcl --rootPassword myrootpasswd



Users methods
-------------

* create users (WBM)

    + pyoxeconf_cli createUsers --host 10.100.8.10 --rangeSize=15000 --rangeStart=80000 --setType "SIP_Extension"
    + pyoxeconf_cli createUsers --host 10.100.8.10 --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension"
    + pyoxeconf_cli createUsers --host 10.100.8.10 --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension" --sipp
    + pyoxeconf_cli createUsers --host 10.100.8.10 --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL"
    + *pyoxeconf_cli createUsers --host 10.100.8.10 --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL" --voicemail=6000*

* delete users (WBM)

    + pyoxeconf_cli deleteUsers --host 10.100.8.10 --rangeSize=100 --rangeStart=8000

* provision phonebook (WBM)

    + pyoxeconf_cli createPhonebookEntries --host 10.100.8.10 --rangeSize 1 --rangeStart 618001 --alias 255



Licensing methods
-----------------

* set external flex server (WBM)

    + pyoxeconf_cli setFlexServer --host 10.100.8.10 --flexip 10.100.8.3
    + pyoxeconf_cli setFlexServer --host oxe01wbm.rainbow.tech-systems.fr --flexip 10.100.8.3 --reboot



JSON model management
---------------------

* get OXE JSON data model (WBM)

    + pyoxeconf_cli getJsonModel --host 10.100.8.10
    + pyoxeconf_cli getJsonModel --host oxe01wbm.rainbow.tech-systems.fr



Collect Information
-------------------

* get OXE Version (SSH)

    + pyoxeconf_cli getOxeVersion --host 10.100.8.10
    + pyoxeconf_cli getOxeVersion --host oxe01wbm.rainbow.tech-systems.fr



Rainbow connection methods
--------------------------

* get rainbow agent version running on OXE (SSH)

    + pyoxeconf_cli getRainbowAgentVersion --host 10.100.8.10
    + pyoxeconf_cli getRainbowAgentVersion --host oxe01wbm.rainbow.tech-systems.fr


* enable Rainbow connection (WBM)

    + pyoxeconf_cli rainbowConnect --host 10.100.8.10 --rainbowDomain 'alexantr-all-in-one-dev-1.opentouch.cloud' --pbxId 'PBXd513-58ac-2d51-4737-a3a8-6b1e-6926-9e14' --activationCode 4567 --phoneBook Yes
    + pyoxeconf_cli rainbowConnect --host 10.100.8.10 --ini --filename OXE1.ini


* disable Rainbow connection (WBM)

    + pyoxeconf_cli rainbowDisconnect --host 10.100.8.10


* Rainbow reconnection (WBM)

    + pyoxeconf_cli rainbowReconnect --host 10.100.8.10 --pbxId 'PBXd513-58ac-2d51-4737-a3a8-6b1e-6926-9e14'
    + pyoxeconf_cli rainbowReconnect --host 10.100.8.10 --ini --filename OXE1.ini


* update ccca.cfg specific for rainbow test environment ALL-IN-ONE (SSH)

    + pyoxeconf_cli updateCccaCfg --host 10.100.8.14 --port 22 --password mtcl --apiServer alexantr-agent.openrainbow.org



OMS configuration methods
-------------------------

* Set main Call Server & cristal number to auto-discovery (SSH)

    + pyoxeconf_cli omsConfig --host 10.100.8.40 --port 22 --login admin --password myadminpasswd --rootpassword myrootpassword



Shelves methods
---------------

* Create shelf (WBM)

    + pyoxeconf_cli createShelf --host 10.100.8.10
    + pyoxeconf_cli createShelf --host 10.100.8.10 --shelfId 22

* Update ethernet parameters (WBM)

    + pyoxeconf_cli shelfEthernetParameters --host 10.100.8.10  --shelfId 10 --mac 00:50:56:3c:86:9f

* Update compressors for IP devices (WBM)

    * pyoxeconf_cli setOmsCompressors --host 10.100.8.10  --shelfId 20
    * pyoxeconf_cli setOmsCompressors --host 10.100.8.10  --shelfId 20 --compressors 64



SIP management
--------------

* Default configuration to enable SIP (default trunk groups + SIP GW + SIP Proxy + disable default IP Domain compression + set A Law on system + allow convert A Law to Mu Law + accept A/Mu Law in SIP) (WBM)

    + pyoxeconf_cli enableSip --host 10.100.8.10
    + pyoxeconf_cli enableSip --host 10.100.8.10 --trkId 15



Translator
----------

* Create DPNSS prefix (WBM)

    + pyoxeconf_cli createDpnssPrefix --host 10.100.8.10
    + pyoxeconf_cli createDpnssPrefix --host 10.100.8.10 --dpnss A1000



System Parameters
-----------------

* enable UcaasCstaMonitored (WBM)

    + pyoxeconf_cli enableUcaasCstaMonitored --host 10.100.8.10 (by default set session to max=20000)
    + pyoxeconf_cli enableUcaasCstaMonitored --host 10.100.8.10 --sessions 1000

* set system law

    + pyoxeconf_cli systemLaw --host 10.100.8.10 (by default set A_LAW)
    + pyoxeconf_cli systemLaw --host 10.100.8.10 --law A_LAW
    + pyoxeconf_cli systemLaw --host 10.100.8.10 --law MU_LAW

* set system compression

    + pyoxeconf_cli systemCompression --host 10.100.8.10 (by default set G_729)
    + pyoxeconf_cli systemCompression --host 10.100.8.10 --compression G729
    + pyoxeconf_cli systemCompression --host 10.100.8.10 --compression G723

* report node number from netadmin settings

    + pyoxeconf_cli reportNodeNumber --host 10.100.8.10

* report network number from netadmin settings

    + pyoxeconf_cli reportNetNumber --host 10.100.8.10



4645 voicemail
--------------

* Enable 4645

    + *On going*

* Add voicemail to existing users

    + *On going*



Netadmin management
-------------------

* Set proxies

    + pyoxeconf_cli setProxy --host 10.100.8.19 --proxyAddr 10.100.8.2 --proxyPort 8080
    + pyoxeconf_cli setProxy --host 10.100.8.19 --proxyAddr 10.100.8.2 --proxyPort 8080 --proxyUser Alexandre --proxyPassword Test

* Set DNS

    + pyoxeconf_cli setDns --host 10.100.8.19 --dns1 10.100.0.70 --dns2 10.100.0.71
    + pyoxeconf_cli setDns --host 10.100.8.19 --dns1 10.100.0.70


Swinst management
-----------------

* Install OPS

    + *On Going*

* Start Telephone

    + *On Going*

* Stop Telephone

    + *On Going*

* Set Autostart

    + *On Going*

* Install delivery from network

    + *On Going*



Commands
--------

* reboot OXE (SSH)

    + pyoxeconf_cli oxeReboot --host 10.100.8.10


* kill rainbow agent (SSH)

    + pyoxeconf_cli killRainbowAgent --host 10.100.8.10



Log Utilities
-------------

* Install and configure oxe-log.sh on OXE CallServer (SCP)

    + pyoxeconf_cli oxeLogSh --host 10.100.8.10 *(not completed)*


NGINX
-----

* Create config file for accessing WBM through reverse proxy

    + pyoxeconf_cli nginxRpConfig --host oxe09 --domain rainbow.tech-systems.fr


SIPp
----

* Create UAC dictionary (csv) for SIPp scripts

    + pyoxeconf_cli sippCreateCsv --rangeSize 2000 --rangeStart 70000 --callServer 10.100.8.11

* Customize registration timer in SIPp UAC register script

    + pyoxeconf_cli sippCustomizeUacRegisterXml --filename unregister.xml --registrationTimer 0



ToDo List
---------

    * Mevo 4645 management (to test)
    * Swinst:
        + stop/start telephone
        + set autostart
        + install delivery from network
        + install OPS
    * build URL outside API requests to allow customization (for example http or https scheme, ...)



Rainbow Tests Env Prep
======================

* Prepare OXE for first use

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli wbmRequestsLimit --host 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd *(reboot needed)*
    + pyoxeconf_cli setFlexServer --host 10.100.8.14 --flexip 10.100.8.3 --reboot *(reboot needed)*
    + pyoxeconf_cli logout --host 10.100.8.14
    + *Wait OXE system is back, and telephony is MAIN, and WBM is available again*
    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli createShelf --host 10.100.8.14
    + pyoxeconf_cli shelfEthernetParameters --host 10.100.8.14 --shelfId 10 --mac 00:50:56:3c:86:9f
    + pyoxeconf_cli setOmsCompressors
    + pyoxeconf_cli wbmRequestsLimit --host 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd *(reboot needed)*
    + pyoxeconf_cli enableSip --host 10.100.8.14
    + pyoxeconf_cli createDpnssPrefix --host 10.100.8.14
    + pyoxeconf_cli enableUcaasCstaMonitored --host 10.100.8.14
    + pyoxeconf_cli logout --host 10.100.8.14


* Connect OXE for the first time to Rainbow

    + pyoxeconf_cli connect --host 10.100.8.14
    + *start data collect if test 1st connection scenario*
    + pyoxeconf_cli updateCccaCfg --host 10.100.8.14 --apiServer agent-fabien.openrainbow.org
    + pyoxeconf_cli rainbowConnect  --host 10.100.8.14 --ini --filename oxe5.ini
    + pyoxeconf_cli logout --host 10.100.8.14


* Connect OXE already connected to Rainbow solution as a new Rainbow system

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli rainbowDisconnect --host 10.100.8.14
    + pyoxeconf_cli purgeCccaCfg --host 10.100.8.14
    + Update OXE directory *pyoxeconf_cli deleteUsers or pyoxeconf_cli createUsers*
    + *start data collect if test 1st connection scenario*
    + pyoxeconf_cli updateCccaCfg --host 10.100.8.14 --apiServer agent-fabien.openrainbow.org
    + pyoxeconf_cli rainbowConnect --host 10.100.8.14 --ini --filename oxe6.ini
    + pyoxeconf_cli logout --host 10.100.8.14


* Disconnect OXE from Rainbow solution

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli rainbowDisconnect --host 10.100.8.14
    + pyoxeconf_cli logout --host 10.100.8.14


* Reconnect an OXE to Rainbow Solution

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli rainbowReconnect --host 10.100.8.14 --pbxId PBX4867-d7dc-fe11-4445-8dc8-743b-4d31-ca4b --rainbowDomain fabien-all-in-one-dev-1.opentouch.cloud
    + pyoxeconf_cli logout --host 10.100.8.14


* Example of simultaneous 1st connection to Rainbow on multiple OXE
    + pyoxeconf_cli connect --host 10.100.8.10
    + pyoxeconf_cli connect --host 10.100.8.11
    + pyoxeconf_cli connect --host 10.100.8.12
    + *start data collect if test 1st connection scenario*
    + pyoxeconf_cli updateCccaCfg --host 10.100.8.10 --apiServer agent-fabien.openrainbow.org
    + pyoxeconf_cli updateCccaCfg --host 10.100.8.11 --apiServer agent-fabien.openrainbow.org
    + pyoxeconf_cli updateCccaCfg --host 10.100.8.12 --apiServer agent-fabien.openrainbow.org
    + pyoxeconf_cli rainbowConnect  --host 10.100.8.10 --ini --filename oxe1.ini
    + pyoxeconf_cli rainbowConnect  --host 10.100.8.11 --ini --filename oxe2.ini
    + pyoxeconf_cli rainbowConnect  --host 10.100.8.12 --ini --filename oxe3.ini
    + pyoxeconf_cli logout --host 10.100.8.10
    + pyoxeconf_cli logout --host 10.100.8.11
    + pyoxeconf_cli logout --host 10.100.8.12


Development
===========

To run the all tests run ::

    py.test

