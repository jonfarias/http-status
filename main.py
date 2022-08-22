from flask import render_template, Blueprint, jsonify, request, url_for, flash, redirect
from json2html import *

# Database
from .app import db
from .models import Site
from .models import Ssl

# Http Status
import requests

# Debug
import sys

# SSL
import datetime
import socket
import ssl

main = Blueprint('main', __name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 } 
]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/http')
def http_check():
    sites = Site.query
    return render_template('http.html', sites=sites)

@main.route('/ssl')
def ssl_check():
    ssls = Ssl.query.all()
    return render_template('ssl.html', ssls=ssls)

@main.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['name']
        cron = request.form['cron']

        if not name:
            flash('É obrigatório inserir um nome.')
        elif not url:
            flash('É obrigatório inserir uma url.')
        elif not cron:
            flash('É obrigatório inserir um cron.')
        else:
            sites = Site.query.filter_by(name=name).first()
            if sites:
                flash('O site já existe no banco de dados.')
            else:
                # Get the HTTP Status
                code = get_status(url)

                # Adiciona um novo site ao banco de dados de HTTP Status
                add_status_db(url, name, cron, code)

                # Get SSL Status
                days, organization, info = get_ssl(url)

                # Adiciona um novo site ao banco de dados de SSL Status
                add_ssl_db(name, url, days, organization, info)

                flash('Site adicionado com sucesso')


    return render_template('new.html')


@main.route('/checks.json', methods=['GET'])
def chat():
  #return jsonify(incomes)
  return render_template('cron.html')


@main.route('/cron', methods=('GET', 'POST'))
def run_http_status():
  sites = Site.query.all()

  try:
    for site in sites:
        r = requests.get("https://google.com.br/")
        print(r.status_code)
        print(site.url, file=sys.stderr)
        incomes.append({'title': sites, 'content': sites})
        return render_template('cron.html', incomes=incomes)

  except requests.ConnectionError:
   return render_template('index.html')


##################
def add_status_db(url, name, cron, code):

    # Adiciona um novo site ao banco de dados de HTTP Status
    new_site_status = Site(url=url, name=name, cron=cron, status=code)
    db.session.add(new_site_status)
    db.session.commit()

def add_ssl_db(name, url, days, organization, info):

    # Adiciona um novo site ao banco de dados de SSL Status
    new_site_ssl = Ssl(name=name, domain=url, days=days, organization=organization, status=info)
    db.session.add(new_site_ssl)
    db.session.commit()



def get_status(url):
    try:
        r = requests.get(url)
        return r.status_code
    except requests.ConnectionError:
        return 000


def get_ssl(hostname: str, port: int = 443):
    try:
        if 'https://' in hostname:
            hostname = hostname[8:]
            if '/' in hostname:
                hostname = hostname[:len(hostname)-1]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssl_info = ssock.getpeercert()
                expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
                delta = expiry_date - datetime.datetime.utcnow()
                print(f'{hostname} expires in {delta.days} day(s)', file=sys.stderr)

                # Days
                days = delta.days

                # Organization Name
                for organization_name in ssl_info['issuer'][1]:
                    organization = organization_name[1]

                # Status
                if delta.days <= 30:
                    info = 'Attention'
                else:
                    info = 'OK'                

                return days, organization, info

    except Exception as e:
        days = 0
        organization = 'Fail'
        info = 'Fail'
        print("{} in {}".format(e, hostname), file=sys.stderr)
        return days, organization, info

