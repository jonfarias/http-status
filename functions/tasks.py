"""Adding tasks on app."""

from ..extensions import scheduler
import sys
import time, calendar

#Import for database
from ..app import db
from ..models import Site

# Import Functions HTTP
from ..functions import http 

#@scheduler.task(
#    "interval",
#    id="job_sync",
#    seconds=30,
#    max_instances=1,
#    start_date="2000-01-01 12:19:00",
#)
#
#def task1():
#    """Sample task 1.
#
#    Added when app starts.
#    """
#    print("running task 1!", file=sys.stderr)  # noqa: T001
#
#    # oh, do you need something from config?
#    #with scheduler.app.app_context():
#    #    print(scheduler.app.config)  # noqa: T001

def add_http_task(cron_time):
    """Add a task for http.
    id_job: cron_14545465
    cron_time: 1|2|3|4|5
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
    """Cron Sites Task.

    Added when new site is add.
    """
    cron_id = args[0]
    cron_time = args[1]

    with scheduler.app.app_context():   
        sites = Site.query.filter_by(cron_id=cron_id).first()

        http_status = http.get_http_status(sites.url)


        print(sites.name, file=sys.stderr)
        print(sites.url, file=sys.stderr)
        print(sites.cron_id, file=sys.stderr)
        print(sites.http_status, file=sys.stderr)

        sites.http_status = http_status
        db.session.commit()


        print(f"running cron_sites task with id {cron_id} in {cron_time} minutes with status {sites.http_status}!", file=sys.stderr)  # noqa: T001
