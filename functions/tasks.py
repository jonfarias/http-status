"""Adding tasks on app."""

from ..extensions import scheduler
import datetime
import sys


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=30,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)

def task1():
    """Sample task 1.

    Added when app starts.
    """
    print("running task 1!", file=sys.stderr)  # noqa: T001

    # oh, do you need something from config?
    #with scheduler.app.app_context():
    #    print(scheduler.app.config)  # noqa: T001


def task2(*args):
    """Sample task 2.

    Added when /add url is visited.
    """
    textit = args[1]

    print(f"running task {textit}!", file=sys.stderr)  # noqa: T001
