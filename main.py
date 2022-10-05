# Flask Dependencies
from flask import render_template, Blueprint, jsonify, request, url_for, flash, redirect
from json2html import *

# Database
from .app import db
from .models import Site, Ssl

# Import some functions
from .functions import http
from .functions import ssl
from .functions import tasks

main = Blueprint('main', __name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 } 
]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/http')
def http_check():
    sites = Site.query.all()
    return render_template('http.html', sites=sites)

@main.route('/ssl')
def ssl_check():
    ssls = Ssl.query.all()
    return render_template('ssl.html', ssls=ssls)

@main.route('/new', methods=('GET', 'POST'))
def new_site():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['name']
        cron_time = request.form['cron_time']

        if not name or name.isdigit():
            flash('É obrigatório inserir um nome.')
        elif not url or url.isdigit() or not 'https://' in url or 'http://' in url:
            flash('É obrigatório inserir uma url.')
        elif not cron_time or not cron_time.isdigit() or int(cron_time)<=0 and int(cron_time)>=6:
            flash('É obrigatório inserir um tempo entre 1 e 5 minutos.')
        else:
            sites = Site.query.filter_by(name=name).first()
            if sites:
                flash('O site já existe no banco de dados.')
            else:
                # Get the HTTP Status
                http_status = http.get_http_status(url)

                # Create new task
                cron_id = tasks.add_http_task(int(cron_time))

                # Adiciona um novo site ao banco de dados de HTTP Status
                http.add_http_db(name, url, int(cron_time), cron_id, http_status)

                # Get SSL Status
                days, organization, info = ssl.get_ssl_status(url)

                # Adiciona um novo site ao banco de dados de SSL Status
                ssl.add_ssl_db(name, url, days, organization, info)

                flash('Site adicionado com sucesso.')


    return render_template('new.html')


@main.route('/checks.json', methods=['GET'])
def chat():
  #return jsonify(incomes)
  return render_template('cron.html')



