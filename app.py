from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import os

db = SQLAlchemy()
scheduler = APScheduler()
#load_dotenv()

def create_app():
    app = Flask(__name__)

    secret = os.urandom(24).hex()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret

    print(secret)

    db.init_app(app)
    scheduler.init_app(app)

    from .models import Site

    with app.app_context():
        db.create_all()
        scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #@app.errorhandler(404)
    #def page_not_found(error):
    #    return render_template('errors/404.html', title='Page Not Found'), 404
#
    #@app.errorhandler(500)
    #def internal_server_error(error):
    #    return render_template('errors/500.html', title='Server Error'), 500


    return app