"Initialize any app extensions."

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

scheduler = APScheduler()
db = SQLAlchemy()

