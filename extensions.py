"Initialize any app extensions."

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

scheduler = APScheduler()
db = SQLAlchemy()
talisman = Talisman()
