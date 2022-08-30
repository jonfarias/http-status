from ..extensions import scheduler
from .tasks import task2
import time, calendar

# Database
from ..app import db
from ..models import Site

# Http Status
import requests

# Debug
import sys


def add_http_db(url, name, time, cron_name, code):

    # Adiciona um novo site ao banco de dados de HTTP Status
    new_site_status = Site(url=url, name=name, time=time, cron_name=cron_name, status=code)
    db.session.add(new_site_status)
    db.session.commit()

def get_http_status(url):
    try:
        r = requests.get(url)
        return r.status_code
    except requests.ConnectionError:
        return 000



def add_http_task(cron_time):
    """Add a task for http.
    :url: /add/
    :returns: job
    """

    id_job = 'cron_' + str(calendar.timegm(time.gmtime()))

    job = scheduler.add_job(
        func=cron_sites,
        trigger="interval",
        minutes=cron_time,
        id=id_job,
        name=id_job,
        args=[id_job, cron_time],
        replace_existing=True,
    )
    return job.id


def cron_sites(*args):
    """Sample task 2.

    Added when /add url is visited.
    """
    textit = args[1]

    print(f"running task {textit}!", file=sys.stderr)  # noqa: T001
