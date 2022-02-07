from flask import Blueprint, url_for
from app import Config, mail
from flask_mail import Message
from flask_babel import _
from flask_babel import lazy_gettext as _l

mail_bp = Blueprint('mail_bp', __name__)


def send_activation_mail(subject, token, email):

    msg = Message(subject , sender=Config.MAIL_SENDER, recipients=[email])

    link = url_for('confirm_email' , token=token , _external=True)

    msg.body = _l("Your activation link is: %s" %(link))

    mail.send(msg)

def send_reset_password__mail(subject, token, email):

    msg = Message(subject , sender=Config.MAIL_SENDER, recipients=[email])

    link = url_for('reset_password' , token=token , _external=True)

    msg.body = _l("Your link for reset password is: %s" %(link))

    mail.send(msg)