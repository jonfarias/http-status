"""Web Pages"""

import os, sys
# Fix ImportError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Flask Dependencies
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required

# Database
from http_check.app import db
from http_check.models import Site, Ssl

# Import some functions
from http_check.functions import http
from http_check.functions import ssl
from http_check.functions import tasks

main = Blueprint('main', __name__)

@main.route('/http/', methods=['GET'])
@login_required
def http_check():
    if request.method == 'GET':
        # Get all sites in Site table
        sites = db.session.execute(db.select(Site).order_by(Site.id)).scalars().all()
        return render_template('http.html', sites=sites)

@main.route('/http/', methods=['POST'])
@login_required
def http_delete():
    if request.method == 'POST':
        id = request.form['id']

        # Search ID in site and ssl db
        search_id_http = db.session.execute(db.select(Site).filter_by(id=id)).scalars().one()
        search_id_ssl = db.session.execute(db.select(Ssl).filter_by(id=id)).scalars().one()

        # Remove http task for cron
        tasks.remove_http_task(search_id_http.cron_id)

        # Catch removed site
        removed = search_id_http.name

        # Remove site and ssl from db
        db.session.delete(search_id_http)
        db.session.delete(search_id_ssl)
        db.session.commit()

        # Return all sites in db
        sites = db.session.execute(db.select(Site).order_by(Site.id)).scalars().all()
        flash(f'Site {removed} removido com sucesso.')
        return render_template('http.html', sites=sites)

@main.route('/ssl/', methods=['GET'])
@login_required
def ssl_check():
    if request.method == 'GET':
        ssls = db.session.execute(db.select(Ssl).order_by(Ssl.id)).scalars().all()
        return render_template('ssl.html', ssls=ssls)

@main.route('/new/', methods=['GET'])
@login_required
def new_site():
    if request.method == 'GET':
        return render_template('new.html')

@main.route('/new/', methods=['POST'])
@login_required
def new_site_post():
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
            try:
                sites = db.session.execute(db.select(Site).filter_by(name=name)).scalars().one()
                if sites:
                    flash('O site já existe no banco de dados.')
            except:
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

                return redirect(url_for('main.new_site'))


    return render_template('new.html')




