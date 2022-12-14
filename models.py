"""Database Models"""

import os, sys
# Fix ImportError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from http_check.app import db
from http_check.app import ma
from flask_login import UserMixin

class Site(db.Model):

    __tablename__ = "site"

    id = db.Column(db.Integer, primary_key=True) # 0
    name = db.Column(db.String(24), index=True, unique=True, nullable=False) # Google
    url = db.Column(db.String(24), unique=True, nullable=False) # https://google.com.br
    cron_time = db.Column(db.Integer, nullable=False) # 1|2|3|4|5 minutes
    cron_id = db.Column(db.String(24), unique=True, nullable=False) # cron_321456567
    http_status = db.Column(db.Integer, nullable=False) # 200 | 300 | 400 | 500
    next_run = db.Column(db.Integer, nullable=False) # NEXT_RUN
    last_run = db.Column(db.Integer, nullable=False) # LAST_RUN

class SiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "url", "cron_time", "cron_id", "http_status", "next_run", "last_run")

class Ssl(db.Model):

    __tablename__ = "ssl"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True, nullable=False)
    domain = db.Column(db.String(24), unique=True, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    organization = db.Column(db.String(24), nullable=False)
    status = db.Column(db.String(24), nullable=False)

class SslSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "domain", "days", "organization", "status")

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
