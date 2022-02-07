import os
from datetime import timedelta
import pytz
class Config():
    SECRET_KEY = "some-kerearewrewrwerwerweey" or os.environ.get('SECRET_KEY')

    #DOCKER: ""mysql://lech:S0M3p*ssword@127.0.0.1/lechsys?charset=utf8"


    #FLASK SESSION
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1/lechsys?charset=utf8" or os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'lechsysbot@gmail.com'
    MAIL_PASSWORD = 'WartaLezyWp0znaniu'
    MAIL_DEFAULT_SENDER = '"LechSys" <lechsysbot@gmail.com>'
    MAIL_SENDER = "Lechsysbot@gmail.com"

    #MAIL TOKEN TIME
    EXPIRATION_TOKEN_TIME = 365 * 24 * 3600

    MAIL_SERIALIZER_SECRET = "mail_utilities-token-serializer-secret" or os.environ.get('MAIL_SERIALIZER_SECRET')

    MAIL_SALT = "email-confirm" or os.environ.get('MAIL_SALT')


    # Files max lenght (avatars, pictures, RTG or other type of files)
    MAX_CONTENT_LENGTH= 5 * 1024*1024

    #UPLOAD_PATH = 'static/uploads/user_data/'
    UPLOAD_PATH = 'instance/user_data/'


    #Languages
    LANGUAGES = {'english': 'en', 'spanish': 'es', 'polish': 'pl'}

    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_ACCESS_TOKEN_EXPIRES = 3600 * 24 # This is in seconds

    #for develop
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"

    #CORS 500 ERROR
    PROPAGATE_EXCEPTIONS = False

    #PUSH SERVICE PART
    NOTIFICATION_KEY = 'BJg3NW4PZ1fC60Bg02SLFIk-lAUz9T5LQTLSacBBav4rmNKMLZ0bjw94W7Igc2pac9nR8Yteonv9pkpFGcou3L4'

    WEBPUSH_VAPID_PRIVATE_KEY = 'ZL8SjMaRpdVZYbVXNCNDApW3JZhMh1ta97dYxBhcng8'
    VAPID_CLAIMS = {
        "sub": "mailto:lechsysbot@gmail.com"
    }


    #timezone of app
    APP_TIMEZONE = pytz.timezone('Europe/Berlin')