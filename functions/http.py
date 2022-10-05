"""HTTP Functions."""

# HTTP Status
import requests

# Database
from ..app import db
from ..models import Site


def add_http_db(name, url, cron_time, cron_id, http_status):
    """Adiciona um novo site ao banco de dados de HTTP Status."""

    new_site_status = Site(name=name, url=url, cron_time=cron_time, cron_id=cron_id, http_status=http_status)
    db.session.add(new_site_status)
    db.session.commit()


def get_http_status(url):
    """Verifica o status HTTP.
    Retorna o Status HTTP e se falhar retorna 000.
    """

    try:
        r = requests.get(url)
        return r.status_code
    except requests.ConnectionError:
        return 000
