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

    + pyoxeconf_cli configure --host='10.100.8.10' --password='mtcl'


* connect : (WBM)

    + pyoxeconf_cli connect --host 'oxe02wbm.rainbow.tech-systems.fr' --password 'mtcl'
    + pyoxeconf_cli connect --ini


* logout : (WBM)

    + pyoxeconf_cli logout

* change WBM requests quota (SSH)

    + pyoxeconf_cli wbmRequestsLimit --ip 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd



Users methods
-------------

* create users (WBM)

    + pyoxeconf_cli createUsers --rangeSize=15000 --rangeStart=80000 --setType "SIP_Extension"
    + pyoxeconf_cli createUsers --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension"
    + pyoxeconf_cli createUsers --rangeSize=100 --rangeStart=8000 --setType "SIP_Extension" --sipp
    + pyoxeconf_cli createUsers --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL"
    + *pyoxeconf_cli createUsers --rangeSize=10 --rangeStart=6000 --setType "UA_VIRTUAL" --voicemail=6000*

* delete users (WBM)

    + pyoxeconf_cli deleteUsers --rangeSize=100 --rangeStart=8000

* provision phonebook (WBM)

    + pyoxeconf_cli createPhonebookEntries --rangeSize 1 --rangeStart 618001 --alias 255



Licensing methods
-----------------

* set external flex server (WBM)

    + pyoxeconf_cli setFlexServer --ip 10.100.8.3
    + pyoxeconf_cli setFlexServer --ip 10.100.8.3 --reboot



JSON model management
---------------------

* get OXE JSON data model (WBM)

    + pyoxeconf_cli getJsonModel --ip 10.100.8.10



Collect Information
-------------------

* get OXE Version (SSH)

    + pyoxeconf_cli getOxeVersion --ip 10.100.8.10



Rainbow connection methods
--------------------------

* get rainbow agent version running on OXE (SSH)

    + pyoxeconf_cli getRainbowAgentVersion --ip 10.100.8.10


* enable Rainbow connection (WBM)

    + pyoxeconf_cli rainbowConnect --rainbowDomain 'alexantr-all-in-one-dev-1.opentouch.cloud' --pbxId 'PBXd513-58ac-2d51-4737-a3a8-6b1e-6926-9e14' --activationCode 4567 --phoneBook Yes
    + pyoxeconf_cli rainbowConnect --ini --filename OXE1.ini


* disable Rainbow connection (WBM)

    + pyoxeconf_cli rainbowDisconnect


* Rainbow reconnection (WBM)

    + pyoxeconf_cli rainbowReconnect --pbxId 'PBXd513-58ac-2d51-4737-a3a8-6b1e-6926-9e14'
    + pyoxeconf_cli rainbowReconnect --ini --filename OXE1.ini

* update ccca.cfg for rainbow test environment ALL-IN-ONE (SSH)

    + pyoxeconf_cli updateCccaCfg --ip 10.100.8.14 --port 22 --password mtcl --apiserver alexantr-agent.openrainbow.org



OMS configuration methods
-------------------------

* Set main Call Server & cristal number to auto-discovery (SSH)

    + pyoxeconf_cli omsConfig --ip 10.100.8.40 --port 22 --login admin --password myadminpasswd --rootpassword myrootpassword



Shelves methods
---------------

* Create shelf (WBM)

    + pyoxeconf_cli createShelf


* Update ethernet parameters (WBM)

    + pyoxeconf_cli shelfEthernetParameters --shelfId 10 --mac 00:50:56:3c:86:9f

* Update compressors for IP devices (WBM)

    * pyoxeconf_cli setOmsCompressors --shelfId 20
    * pyoxeconf_cli setOmsCompressors --shelfId 20 --compressors 64



SIP management
--------------

* Default configuration to enable SIP (default trunk groups + SIP GW + SIP Proxy + disable default IP Domain compression + set A Law on system + allow convert A Law to Mu Law + accept A/Mu Law in SIP) (WBM)

    + pyoxeconf_cli enableSip --trkId 15



Translator
----------

* Create DPNSS prefix (WBM)

    + pyoxeconf_cli createDpnssPrefix
    + pyoxeconf_cli createDpnssPrefix --dpnss A1000



4645 voicemail
--------------

* Enable 4645

    + *On going*

* Add voicemail to existing users

    + *On going*



Netadmin management
-------------------

* Set proxies

    + *On Going*

* Set DNS

    + *On Going*



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

    + pyoxeconf_cli oxeReboot --ip 10.100.8.10


* kill rainbow agent (SSH)

    + pyoxeconf_cli killRainbowAgent --ip 10.100.8.10



Log Utilities
-------------

* Install and configure oxe-log.sh on OXE CallServer (SCP)

    + pyoxeconf_cli oxeLogSh --ip 10.100.8.10 *(not completed)*


NGINX
-----

* Create config file for accessing WBM through reverse proxy

    + pyoxeconf_cli nginxRpConfig --host oxe09 --domain rainbow.tech-systems.fr


SIPp
----

* Create UAC dictionary (csv) for SIPp scripts

    + pyoxeconf_cli sippCreateCsv --rangeSize 2000 --rangeStart 70000 --ip 10.100.8.11

* Customize registration timer in SIPp UAC register script

    + pyoxeconf_cli sippCustomizeUacRegisterXml --filename unregister.xml --registrationTimer 0



ToDo List
---------

    * netadmin DNS (mandatory for Rainbow)
    * netadmin Proxy (mandatory for Rainbow)
    * proxy management for API based command
    * Mevo 4645 management
    * Swinst:
        + stop/start telephone
        + set autostart
        + install delivery from network
        + install OPS



Rainbow Tests Env Prep
======================

* Prepare OXE for first use

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli wbmRequestsLimit --ip 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd *(reboot needed)*
    + pyoxeconf_cli setFlexServer --ip 10.100.8.3 --reboot *(reboot needed)*
    + pyoxeconf_cli logout
    + *Wait OXE system is back, and telephony is MAIN, and WBM is available again*
    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli createShelf
    + pyoxeconf_cli shelfEthernetParameters --shelfId 10 --mac 00:50:56:3c:86:9f
    + pyoxeconf_cli setOmsCompressors
    + pyoxeconf_cli wbmQuota --ip 10.100.8.14 --port 22 --password mtcl --rootPassword myrootpasswd *(reboot needed)*
    + pyoxeconf_cli enableSip
    + pyoxeconf_cli createDpnssPrefix
    + pyoxeconf_cli enableUcaasCstaMonitored
    + pyoxeconf_cli logout


* Connect OXE for the first time to Rainbow

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli rainbowConnect --ini --filename oxe5.ini
    + *start data collect*
    + pyoxeconf_cli updateCccaCfg --ip 10.100.8.14 --apiserver agent-fabien.openrainbow.org
    + pyoxeconf_cli logout


* Connect OXE as a new Rainbow system

    + pyoxeconf_cli connect --host 10.100.8.14
    + pyoxeconf_cli rainbowDisconnect
    + pyoxeconf_cli purgeCccaCfg --ip 10.100.8.14
    + Update OXE directory *pyoxeconf_cli deleteUsers or pyoxeconf_cli createUsers*
    + pyoxeconf_cli rainbowConnect --ini --filename oxe6.ini
    + *start data collect*
    + pyoxeconf_cli updateCccaCfg --ip 10.100.8.14 --apiserver agent-fabien.openrainbow.org
    + pyoxeconf_cli logout


Development
===========

To run the all tests run ::

    py.test

