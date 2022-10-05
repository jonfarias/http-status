"""SSL Functions."""

# Debug
import sys

# SSL
import datetime, socket, ssl

# Database
from ..app import db
from ..models import Ssl


def add_ssl_db(name, url, days, organization, info):

    # Adiciona um novo site ao banco de dados de SSL Status
    new_site_ssl = Ssl(name=name, domain=url, days=days, organization=organization, status=info)
    db.session.add(new_site_ssl)
    db.session.commit()

def get_ssl_status(hostname: str, port: int = 443):
    try:
        if 'https://' in hostname:
            hostname = hostname[8:]
            if '/' in hostname:
                hostname = hostname[:len(hostname)-1]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssl_info = ssock.getpeercert()
                expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
                delta = expiry_date - datetime.datetime.utcnow()
                print(f'{hostname} expires in {delta.days} day(s)', file=sys.stderr)

                # Days
                days = delta.days

                # Organization Name
                for organization_name in ssl_info['issuer'][1]:
                    organization = organization_name[1]

                # Status
                if delta.days <= 30:
                    info = 'Attention'
                else:
                    info = 'OK'                

                return days, organization, info

    except Exception as e:
        days = 0
        organization = 'Fail'
        info = 'Fail'
        print("{} in {}".format(e, hostname), file=sys.stderr)
        return days, organization, info