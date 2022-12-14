"""Init app."""

import os, sys, logging
# Fix ImportError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from flask import Flask
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from http_check.extensions import scheduler, db, talisman, ma, login_manager, session

csp = {
    'default-src': ['\'self\''],
    'object-src': '\'none\'',
}

def create_app():
    app = Flask(__name__)

    #secret = python3 -c 'import secrets; print(secrets.token_hex())'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/databases/http-check.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SCHEDULER_TIMEZONE'] = 'America/Sao_Paulo'
    app.config['SCHEDULER_JOBSTORES'] = { "default": SQLAlchemyJobStore(url="sqlite:////usr/src/databases/scheduler.db") }


    # Init Extensions in App
    db.init_app(app)
    ma.init_app(app)
    scheduler.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    session.init_app(app)

    # Logs
    logging.basicConfig()
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    # Import db models
    from http_check.models import Ssl, Site, User
    from http_check.functions import tasks

    with app.app_context():
        db.create_all()
        scheduler.start()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from pages.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from pages.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from pages.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #@app.errorhandler(404)
    #def page_not_found(error):
    #    return render_template('errors/404.html', title='Page Not Found'), 404
#
    #@app.errorhandler(500)
    #def internal_server_error(error):
    #    return render_template('errors/500.html', title='Server Error'), 500

    return app

if __name__ == "__main__":
   app = create_app()
   app.run(host='0.0.0.0', ssl_context=('./keys/cert.pem', './keys/key.pem'))