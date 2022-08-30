from flask import current_app, Blueprint, render_template
from .extensions import scheduler
from .functions.tasks import task2
import time, calendar

cron = Blueprint("cron", __name__, url_prefix='/cron')

@cron.route("/add")
def add_task():
    """Add a task.
    :url: /add/
    :returns: job
    """
    id_job = 'cron_' + str(calendar.timegm(time.gmtime()))
    an = 'one' + str(calendar.timegm(time.gmtime()))

    job = scheduler.add_job(
        func=task2,
        trigger="interval",
        minutes=1,
        id=id_job,
        name=id_job,
        args=[id_job, an],
        replace_existing=True,
    )
    return "%s added!" % job.name