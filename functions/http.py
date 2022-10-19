"""HTTP Functions."""

# HTTP Status
import requests

# Database
from ..app import db
from ..models import Site

# TIME
from datetime import datetime, timedelta
from pytz import timezone



def add_http_db(name, url, cron_time, cron_id, http_status, ):
    """Adiciona um novo site ao banco de dados de HTTP Status."""

    # Pega o tempo da próxima verificação de Status 
    time_now, next_run = get_http_time(cron_time)

    # Adiciona no banco as informações
    new_site_status = Site(name=name, url=url, cron_time=cron_time, cron_id=cron_id, http_status=http_status, last_run=time_now, next_run=next_run)
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

def get_http_time(cron_time):

    time_now = str(datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S"))

    next_run = datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=cron_time)

    return time_now, next_run
