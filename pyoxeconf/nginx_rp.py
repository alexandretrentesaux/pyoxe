# -*- encoding: utf-8 -*-

"""Summary

Attributes:
    rp_template (str): Description
"""
from os.path import join
from tempfile import gettempdir


rp_template = """server {{
        listen 443;

        server_name {}wbm {}wbm.{};

        access_log    /var/log/nginx/{}.{}-access.log;
        error_log     /var/log/nginx/{}.{}-error.log;

        ssl on;
        ssl_certificate /etc/nginx/cert/{};
        ssl_certificate_key /etc/nginx/cert/{};

        ssl_session_timeout 5m;
        ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv3:+EXP;

        location / {{
                proxy_bind {};
                proxy_pass https://{}.{};
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                add_header              Front-End-Https   on;
        }}
}}"""


def nginx_rp_oxe_config(host, domain, cert, key, bind_ip):
    """Create NGINX RP config file for accessing OXE WBM
    
    Args:
        host (str): OXE FQDN host part
        domain (str): OXE domain part
        cert (str): Certificate filename
        key (str): Key filename
        bind_ip (str): NGINX internal IP address
    """
    with open(join(gettempdir(), host + 'wbm.' + domain + '.conf'), 'w') as fh:
        fh.write(rp_template.format(host, host, domain, host, domain, host, domain, cert, key, bind_ip, host, domain))
