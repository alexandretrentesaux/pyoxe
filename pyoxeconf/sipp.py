# -*- encoding: utf-8 -*-

"""SIPp methods for OXE

Attributes:
    register_template (TYPE): Description
"""

import os
import tempfile

register_template="""<?xml version="1.0" encoding="ISO-8859-1" ?>
<!DOCTYPE scenario SYSTEM "sipp.dtd">

<scenario name="registration">

<send retrans="500">
<![CDATA[
REGISTER sip:[field1] SIP/2.0
Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]
Max-Forwards: 70
From: "sipp" <sip:[field0]@[field1]>;tag=[call_number]
To: "sipp" <sip:[field0]@[field1]>
Call-ID: reg///[call_id]
CSeq: 7 REGISTER
Contact: <sip:sipp@[local_ip]:[local_port]>
Expires: {}
Content-Length: 0
User-Agent: SIPp
]]>
</send>

<recv response="100" optional="true">
</recv>

<recv response="401" auth="true" rtd="true">
</recv>

<send retrans="500">
<![CDATA[
REGISTER sip:[field1] SIP/2.0
Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]
Max-Forwards: 70
From: "sipp" <sip:[field0]@[field1]>;tag=[call_number]
To: "sipp" <sip:[field0]@[field1]>
Call-ID: reg///[call_id]
CSeq: 8 REGISTER
Contact: <sip:sipp@[local_ip]:[local_port]>
Expires: {}
Content-Length: 0
User-Agent: SIPp
[field2]
]]>
</send>

<recv response="100" optional="true">
</recv>

<recv response="200">
</recv>

<ResponseTimeRepartition value="10, 20"/>
<CallLengthRepartition value="10"/>
</scenario>
"""


def sipp_csv_generator(file, pbx, range_start, range_size, sip_password):
    """Create CSV describing UAC for SIPp scripts
    
    Args:
        file (str): destination file
        pbx (str): OXE IP address
        range_start (int): first extension number
        range_size (str): extension range size
        sip_password (str): UAC SIP password
    """
    with open(os.path.join(tempfile.gettempdir(), file), 'w+') as fh:
        fh.write('SEQUENTIAL\n')
        for i in range(range_start, range_start + range_size):
            fh.write(str(i) + ';' + pbx + ';[authentication username=' + str(i) + ' password=' + sip_password + ']\n')


def sipp_register_uac_xml_customize(file, registration_timer):
    """Customize registration script with custom registration timer
    
    Args:
        file (str): destination file
        registration_timer (int): SIP REGISTER registration timer
    
    """
    with open(os.join(tempfile.gettempdir(), file), 'w+') as fh:
        fh.write(register_template.format(registration_timer, registration_timer))
