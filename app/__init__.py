from flask import Flask
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from flask_cors import CORS
from flask_babel import Babel
from flask_jwt_extended import JWTManager
#from flask_crontab import Crontab
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) #database
migrate = Migrate(app,  db) #UPGRADE database Models
ma = Marshmallow(app) # API Serializer
login = LoginManager(app) #Login Module
login.login_view = 'auth_bp.login' #this set the logn view = redirect everytime when someone want to go to pages
jwt = JWTManager(app)
babel = Babel(app)
# without
# being auth
mail = Mail(app) #mail_utilities module
cors = CORS(app) #for api calls

#for cron jobs
#cron = Crontab(app)

app_path = app.instance_path

#Blueprint must be initialized here bellow
from app.api.api import api_bp
from app.auth.auth import auth_bp
from app.mail_utilities.mail_utilities import mail_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp)
app.register_blueprint(mail_bp)

from app import cli

@babel.localeselector
def get_locale():
    if current_user.is_authenticated:
        if current_user.language != 'pl' or current_user.language is not None:
            return current_user.language
    return 'pl'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()



from app import routes, models

