"""API pages"""

# Fix ImportError
import os
import sys  
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Flask Dependencies
from flask import Blueprint, jsonify, request
import sys

# Database
from http_check.models import Site, Ssl, SiteSchema, SslSchema
from http_check.app import db



api = Blueprint('api', __name__, url_prefix='/api')

site_schema = SiteSchema()
site_schema = SiteSchema(many=True)
ssl_schema = SslSchema()
ssl_schema = SslSchema(many=True)

@api.route('/', methods = ['GET', 'POST'])
def api_root():
    if (request.method == 'GET'):
        all_sites = db.session.execute(db.select(Site).order_by(Site.id)).scalars().all()
        all_ssls = db.session.execute(db.select(Ssl).order_by(Ssl.id)).scalars().all()
        if all_sites and all_ssls:
            status = "online"
        else:
            status = "offline"
        return jsonify({'status': status})


@api.route('/http/', methods = ['GET'])
def api_all_http():
    if (request.method == 'GET'):
        all_sites = db.session.execute(db.select(Site).order_by(Site.id)).scalars().all()
        if all_sites:
            return site_schema.dump(all_sites)
        else:
            return "No results find.", 404


@api.route('/http/<name_site>', methods = ['GET'])
def api_http(name_http):
    if (request.method == 'GET'):
        try:
            single_site = db.session.execute(db.select(Site).filter_by(name=name_http)).one()
            return site_schema.dump(single_site)
        except:
            return f"Cannot find {name_http} in search.", 404


@api.route('/ssl/', methods = ['GET'])
def api_all_ssl():
    if (request.method == 'GET'):
        all_ssls = db.session.execute(db.select(Ssl).order_by(Ssl.id)).scalars().all()
        if all_ssls:
            return ssl_schema.dump(all_ssls)
        else:
            return "No results find.", 404


@api.route('/ssl/<name_ssl>', methods = ['GET'])
def api_ssl(name_ssl):
    if (request.method == 'GET'):
        try:
            single_ssl = db.session.execute(db.select(Ssl).filter_by(name=name_ssl)).one()
            return ssl_schema.dump(single_ssl)
        except:
            return f"Cannot find {name_ssl} in search.", 404
