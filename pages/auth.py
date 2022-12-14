"""Auth Configuration"""

import os, sys
# Fix ImportError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from http_check.models import User
from http_check.app import db



auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')

@auth.route('/', methods=['POST'])
def login_post():
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']

        session['email'] = email
        session['password'] = password

        try:
            user = db.session.execute(db.select(User).filter_by(email=email)).scalars().one()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login feito com sucesso.')
                return redirect(url_for('main.new_site'))
            else: 
                flash('Ops algo deu errado, email ou senha estão incorretos.')
                return redirect(url_for('auth.login')) 
        except:
            flash('Nenhum usuário foi cadastrado ainda.')
            return redirect(url_for('auth.login')) 

    return render_template('login.html')

@auth.route('/signup/', methods=['GET'])
def signup():
    if (request.method == 'GET'):
        return render_template('signup.html')

@auth.route('/signup/', methods=['POST'])
def signup_post():
    if (request.method == 'POST'):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        if not name or name.isdigit():
            flash('É obrigatório inserir um nome.')
        elif not email or not '@gmail.com' in email and not '@apiki.com' in email and not '@outlook.com' in email or email == '@apiki.com' and email == '@outlook.com' and email == '@gmail.com':
            flash('É necessário inserir um email válido. Domínios válidos @gmail.com, @outlook.com, @apiki.com')
        elif not password and len(password) <= 6:
            flash('É necessário inserir uma senha válida e maior que 6 caracteres.')
        else:
            try:
                user_email = db.session.execute(db.select(User).filter_by(email=email)).scalars().one()

                if user_email: 
                    flash('O email inserido já existe')
                    return redirect(url_for('auth.signup'))

            except: 
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

                # Adiciona um novo usuário ao banco de dados
                db.session.add(new_user)
                db.session.commit()

                flash('Usuário Cadastrado com Sucesso.')
                return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/logout/')
@login_required
def logout():
    session.pop('email', None)
    session.pop('password', None)
    logout_user()
    flash('Logout realizado com sucesso.')
    return redirect(url_for('auth.login'))