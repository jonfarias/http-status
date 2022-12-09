"""Init app."""

# Fix ImportError
import os
import sys  
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
import os

from flask import Flask
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from http_check.extensions import scheduler, db, talisman, ma

csp = {
    'default-src': ['\'self\''],
    'object-src': '\'none\'',
}

def create_app():
    app = Flask(__name__)

    secret = os.urandom(24).hex()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/databases/http-check.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret
    app.config['SCHEDULER_TIMEZONE'] = "America/Sao_Paulo"
    app.config['SCHEDULER_JOBSTORES'] = { "default": SQLAlchemyJobStore(url="sqlite:////usr/src/databases/scheduler.db") }

    #print(secret)

    # Init Extensions in App
    db.init_app(app)
    ma.init_app(app)
    scheduler.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    # Logs
    logging.basicConfig()
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    # Import db models
    from http_check.models import Ssl, Site
    from http_check.functions import tasks

    with app.app_context():
        db.create_all()
        scheduler.start()

    from http_check.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from http_check.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

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
   app.run(host='0.0.0.0')