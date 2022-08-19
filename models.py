from .app import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(64))
    cron = db.Column(db.String(64))
    status = db.Column(db.Integer)

class Ssl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    domain = db.Column(db.String(64))
    days = db.Column(db.Integer)
    organization = db.Column(db.String(64))
    status = db.Column(db.String(64))
