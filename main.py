from flask import render_template, Blueprint, jsonify, request, url_for, flash, redirect
from json2html import *

# Database
from .app import db
from .models import Site, Ssl

from .functions.http import get_http_status, add_http_db, add_http_task
from .functions.ssl import get_ssl_status, add_ssl_db

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
        time = request.form['time']

        if not name:
            flash('É obrigatório inserir um nome.')
        elif not url:
            flash('É obrigatório inserir uma url.')
        elif not time:
            flash('É obrigatório inserir um tempo.')
        else:
            sites = Site.query.filter_by(name=name).first()
            if sites:
                flash('O site já existe no banco de dados.')
            else:
                # Get the HTTP Status
                code = get_http_status(url)

                # Create new task
                cron_name = add_http_task(int(time))

                # Adiciona um novo site ao banco de dados de HTTP Status
                add_http_db(url, name, int(time), cron_name, code)

                # Get SSL Status
                days, organization, info = get_ssl_status(url)

                # Adiciona um novo site ao banco de dados de SSL Status
                add_ssl_db(name, url, days, organization, info)

                flash('Site adicionado com sucesso')


    return render_template('new.html')


@main.route('/checks.json', methods=['GET'])
def chat():
  #return jsonify(incomes)
  return render_template('cron.html')



