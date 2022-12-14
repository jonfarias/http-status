"""Adding tasks on app."""

import os, sys
# Fix ImportError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from http_check.extensions import scheduler
import time, calendar

#Import for database
from http_check.app import db
from http_check.models import Site, Ssl

# Import Functions HTTP
from http_check.functions import http
from http_check.functions import ssl


@scheduler.task(
    "interval",
    id="job_sync",
    minutes=1440,
    max_instances=1,
    start_date="2022-01-01 00:00:00",
)
def cron_ssl():
    """
    Added when cron task when app starts.
    """

    # oh, do you need something from config?
    with scheduler.app.app_context():
        ssls = db.session.execute(db.select(Ssl).order_by(Ssl.id)).scalars().all()
        if ssls:
            for i_ssl in ssls:
                url = i_ssl.domain
                days, organization, info = ssl.get_ssl_status(url)
                i_ssl.days = days
                i_ssl.organization = organization
                i_ssl.info = info
                db.session.commit()
        else:
            print("Database is Empty", file=sys.stderr) 


def add_http_task(cron_time):
    """Add a task for http.
    id_job: cron_14545465
    cron_time: 1|2|3|4|5
    """

    cron_id = 'cron_' + str(calendar.timegm(time.gmtime()))

    job = scheduler.add_job(
        func=cron_sites,
        trigger="interval",
        minutes=cron_time,
        id=cron_id,
        name=cron_id,
        args=[cron_id, cron_time],
        replace_existing=True,
    )
    return job.id
    

def cron_sites(*args):
    """Cron Sites Task.

    Added when new site is add.
    """

    cron_id = args[0]
    cron_time = args[1]

    with scheduler.app.app_context():   
        sites = db.session.execute(db.select(Site).filter_by(cron_id=cron_id)).scalars().one()

        time_now, next_run = http.get_http_time(cron_time)

        http_status = http.get_http_status(sites.url)

        #print(sites.name, file=sys.stderr)
        #print(sites.url, file=sys.stderr)
        #print(sites.cron_id, file=sys.stderr)
        #print(sites.http_status, file=sys.stderr)
        #print(sites.last_run, file=sys.stderr)
        #print(sites.next_run, file=sys.stderr)
        
        sites.last_run = time_now
        sites.next_run = next_run
        sites.http_status = http_status
        db.session.commit()

        #print(f"running cron_sites task with id {cron_id} in {cron_time} minutes with status {sites.http_status}!", file=sys.stderr)  # noqa: T001

def remove_http_task(cron_id):
    """Remove a task for http.
    cron_id: cron_14545465
    """

    job = scheduler.remove_job(cron_id)

    return job