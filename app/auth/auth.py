from datetime import timedelta , datetime



from flask import Blueprint , redirect , flash , render_template , make_response , session
from flask.helpers import url_for

from app.models.models import User
from app.forms.forms import LoginForm
from flask_login import logout_user, login_user

from flask_jwt_extended import create_access_token , decode_token , get_jwt , get_jwt_identity , unset_jwt_cookies
from flask_babel import _


from app.decorators import is_logged


auth_bp = Blueprint('auth_bp', __name__)



@auth_bp.route('/login', methods=['GET', 'POST'])
@is_logged
def login():

    Loginform = LoginForm()

    if Loginform.validate_on_submit():
        user = User.query.filter_by(username=Loginform.username.data).first()

        if user is None:
            user = User.query.filter_by(email=Loginform.username.data).first()

        if user is None:
            flash(_('Invalid username or password'), 'error')
            return redirect(url_for('auth_bp.login'))


        if (user.is_active() is False):
            flash(_('Your account is innactive') , 'error')
            return redirect(url_for('auth_bp.login'))

        if  (not user._check_password(Loginform.password.data)):
            flash(_('Invalid username or password'), 'error')
            return redirect(url_for('auth_bp.login'))





        payload = {
            'role': '{}'.format(user.show_role()),
            'teams' : '{}'.format(user.show_team()),
            'first_name' : '{}'.format(user.first_name),
            'last_name' : '{}'.format(user.last_name)

        }

        token = create_access_token(identity=user.username, additional_claims=payload)
        decoded = decode_token(token) # TESTING IF GOOD DECODE

        #flash('Login requested for user {}, remember_me={},\n Token : {}\n:decoded {}'.format(
        #    Loginform.username.data, Loginform.remember_me.data, token, decoded), 'success')
        login_user(user, remember=Loginform.remember_me.data)

        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('access_token_cookie', token, httponly=True)

        session.permanent = True

        return resp
    return render_template('login.html', title='Sign In', form=Loginform)


@auth_bp.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect(url_for('auth_bp.login')))
    #resp.set_cookie('access_token_cookie' , '' , expires=0)
    unset_jwt_cookies(resp)
    return resp


#TODO
@auth_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=59))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            response.set_cookie('new_access_token_cookie' , access_token , httponly=True)
        return response



    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response