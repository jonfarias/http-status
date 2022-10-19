from .app import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 0
    name = db.Column(db.String(24), index=True, unique=True) # Google
    url = db.Column(db.String(24)) # https://google.com.br
    cron_time = db.Column(db.Integer) # 1|2|3|4|5 minutes
    cron_id = db.Column(db.String(24), unique=True) # cron_321456567
    http_status = db.Column(db.Integer) # 200 | 300 | 400 | 500
    next_run = db.Column(db.Integer) # NEXT_RUN
    last_run = db.Column(db.Integer) # LAST_RUN

class Ssl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True)
    domain = db.Column(db.String(24))
    days = db.Column(db.Integer)
    organization = db.Column(db.String(24))
    status = db.Column(db.String(24))
