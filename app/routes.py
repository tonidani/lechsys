import json

from flask import render_template, flash, redirect, request, send_from_directory, jsonify, session
from flask.helpers import url_for
from app import app, db, app_path
from app.models.models import User, Role, Team, Nationality, Position, UserBasicInfo, Message, Wellness, Event, \
    Notification, notification_schema, Motoric, RPE, Contusion, BodyPart, Tissue, Trauma
from app.forms.forms import (AddUserForm, SetUserPasswordForm, EditAdminUserForm, RequestResetPasswordUserForm,
                             ResetPasswordUserForm, ImportPlayersForm, ChangeAvatarUserForm, WellnessForm,
                             AddMotoricDataForm, RPEForm, AddMotoricDataManually, AddContusionForm, AddTeamForm,
                             EditContusionForm, EditMotoricDataForm, EditKinaseDataForm)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid
import os.path


from app import Config

from flask import Markup
from flask_babel import lazy_gettext as _l
from flask_babel import _
from app.decorators import blocked_access, is_logged

from app.mail_utilities.mail_utilities import send_activation_mail, send_reset_password__mail
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
from datetime import date

import numpy as np
import pandas as pd
'''
def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
'''
#TODO
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(Config.APP_TIMEZONE)
        current_user.save()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
@login_required
def home():
    '''
    query=db.session.query(Event).join(UserEvents).join(User).filter(Event.id == UserEvents.event_id , User.id ==
                                                                     UserEvents.user_id).filter(User.id == current_user.id)
    Events=query.all()
    '''

    user = User.query.filter_by(id=current_user.id).first()

    user_info = user.get_basic_info()
    nationality = Nationality.get_nationality_name_by_lang(user)
    if 'player' in current_user.show_role():
        position = Position.get_position_name_by_lang(user, user_info)

        wellness_to_complete = [ i for i in current_user.wellness if i.state == 'TO-COMPLETE']
        rpe_to_complete = [i for i in current_user.rpe if i.state == 'TO-COMPLETE']
        event_wellness = [event for event in user.events for wellness in wellness_to_complete if event.id == wellness.event_id ]
        event_rpe = [event for event in user.events for rpe in rpe_to_complete if event.id == rpe.event_id ]






        return render_template("home.html", title="Home Page", user=current_user, events=user.user_active_events(), event_wellness=event_wellness, event_rpe=event_rpe , user_info=user_info,
                               nationality=nationality, position=position)

    if 'admin' in current_user.show_role():


        return render_template("home.html", title="Home Page", user=current_user, events=Event.get_living_events(), events_kinase=Event.query.filter_by(state="KINASIS").all(), events_motoric =Event.query.filter_by(state="MOTORIC").all())

    return render_template("home.html", title="Home Page", user=current_user)


@app.route('/users')
@login_required
@blocked_access('player')
def users():

    page = request.args.get('page' , 1 , type=int)


    if current_user.show_role() in 'admin':
        users = User.query.paginate(page ,10, False)
        next_url=url_for('users' , page=users.next_num) if users.has_next else None
        prev_url=url_for('users' , page=users.prev_num) if users.has_prev else None
        return render_template("users.html" , title="Search Players" , users=users.items , next_url=next_url ,
                               prev_url=prev_url , page=page)

    else: #staff only see people from his team
        users = User.query.filter(User.teams.any(name=current_user.show_team())).all()
        return render_template("users.html", title="Search Players", users=users)



@app.route('/users/add', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def add_users():
    user = User.query.filter_by(id=current_user.id).first()

    form = AddUserForm()
    form.position.choices = Position.get_position_lang_label(user)
    form.nationality.choices = Nationality.get_nationality_lang_label(user=user)

    if form.validate_on_submit():

        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        birth_date=form.birth_date.data,
                        nationality=Nationality.set_nationality(user, form.nationality.data))

        token = new_user.generate_confirmation_mail_token()

        role = form.role.data
        team = form.team.data

        new_user.roles.append(role)
        new_user.teams.append(team)


        new_user.create_username()

        try:
            subject=_("You Have to confirm mail!")
            send_activation_mail(subject, token, new_user.email)
            new_user.create_user_data_folder()


            new_user.save()
            basic_user_info = UserBasicInfo(user_id=new_user.id, height=form.height.data, weight=form.weight.data, shirt=form.shirt.data, position_id=Position.set_position(user, form.position.data))

            basic_user_info.save()

            flash(_(" Added user %s and sent activation link" %(new_user.first_name)))
            return redirect(url_for('users'))

        except:
            flash(_("bad mail"))
            return render_template("adduser.html" , title="Users - Add user" , form=form)

    return render_template("adduser.html", title="Users - Add user", form=form)


@app.route('/teams/add', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def add_team():
    teams = Team.query.all()
    form = AddTeamForm()

    if form.validate_on_submit():
        new_team = Team(name=form.name.data)
        new_team.save()
        flash(_("New team %s added!")%(new_team.name))
        return redirect(url_for('users'))

    return render_template('add_team.html', form=form, teams=teams)

@app.route('/users/import', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def import_users():
    #TODO send activation link

    form = ImportPlayersForm()
    if form.validate_on_submit():

        import_file=form.players_file.data

        filename=secure_filename(import_file.filename)

        #TODO create /imports/ folder if not exist
        #TODO create validation of columns in file
        #TODO

        path = app_path + '/' + current_user.folder + "/files/"

        extension = os.path.splitext(filename)[1]
        image_id = str(uuid.uuid4())

        filename = image_id + extension

        import_file.save(os.path.join(path, filename))

        file = pd.read_excel(os.path.join(path, filename))

        df = pd.DataFrame(file, columns=['Name', 'Birth date',
                                         'Height', 'Weight',
                                         'Position', 'Nation',
                                         'Shirt', 'Mail'])

        try:
            for i, row in df.iterrows():
                first_name, last_name = row[0].split(" ")[0], row[0].split(" ")[1]

                user = User.query.filter(User.first_name==first_name , User.last_name==last_name).first()

                if user is None:
                    nationality = Nationality.query.filter_by(name_eng = str(row[5]).capitalize()).one()
                    position = Position.query.filter_by(name_eng = str(row[4]).capitalize()).one()
                    #birth_date=datetime.strptime(row[1], '%d/%m/%Y')
                    new_user = User(first_name, last_name, email=row[7], nationality=nationality.id, birth_date=row[1])
                    new_user.create_username()
                    #new_user.create_user_data_folder()
                    team=form.team.data
                    role = Role.query.filter(Role.name == "player").first()



                    new_user.roles.append(role)
                    new_user.teams.append(team)
                    new_user.save()
                    basic_user_info = UserBasicInfo(user_id=new_user.id, height=row[2], weight=row[3],
                                                    shirt=row[6],
                                                    position_id=position.id)

                    basic_user_info.save()
                    flash(_l('User %s %s added' %(new_user.first_name, new_user.last_name)))

                else:
                    flash('user exist!')

        except:
            flash(_("you have some errors in your file, please see If the names not contain spaces before and after!"))

        return redirect(url_for('users'))

    return render_template("import_users.html", title="Users - Import Users", form=form)


@app.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    #TODO not delete, deactivate
    if current_user.id == user.id:
        flash(_l("You can not delete yourself!"))
    else:
        user.delete_user_data_folder()
        user.delete()
        flash(_l("User %d deleted" %id))

    return redirect(url_for('users'))

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if user.show_role() in 'admin' and user != current_user:
        flash(_("You can not edit other admins :>!"))
        return redirect(url_for("users"))
    form = EditAdminUserForm()
    if form.validate_on_submit():
        user.username=form.username.data
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        #user.email = form.email.data #TODO:  can  not change the email)
        role = form.role.data

        user.active = form.active.data

        user.roles = []
        if form.team.data is not None:
            team = form.team.data
            user.teams = []
            user.teams.append(team)
        #TODO: WHEN CHANGE THE TEAM, REFRESH THE EVENTS (TEAM_EVENTS TABLE)

        user.roles.append(role)


        user.save()

        flash(_("User edited!"), "success")

    elif request.method == 'GET':
        form.username.data=user.username
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.role.data = Role.query.filter_by(id = user.roles[0].id).first()
        if 'admin' not in user.show_role():
            form.team.data = Team.query.filter_by(id = user.teams[0].id).first()
        form.active.data = user.active


    return render_template("edituser.html", title="{} - Edit user".format(user.username), form=form, user=user)



def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(_l(u"Error in the %s field - %s") % (
                getattr(form, field).label.text,
                error
            ), 'error')

#users pages
@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
@blocked_access('player')
def people_page(id):
    user = User.query.filter_by(id=id).first()
    # TODO ZMIANA LOGIKI BO COS SIE PSUJE

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    elif ('staff' in user.show_role()) or ('admin' in user.show_role()):
        flash(_('Staff and admins do not have pages!'))
        return redirect(url_for("home"))

    elif (current_user.show_team() in user.show_team()) or (current_user.show_role() in 'admin'):
        user_info = user.get_basic_info()
        position = Position.get_position_name_by_lang(current_user, user_info)

        nationality = Nationality.get_nationality_name_by_lang(current_user)

        form = AddContusionForm()
        if user.state == "CONTUSION":
            contusions = [i for i in user.contusion if i.state == "ACTIVE"]
            if not contusions:

                pass
            else:
                contusion = contusions[0]
                editForm = EditContusionForm()
                if request.method == 'GET':
                    editForm.edit_start.data = contusion.start
                    editForm.edit_end.data = contusion.end
                    editForm.edit_details.data = contusion.details

                if editForm.validate_on_submit():
                    edit_body_part = editForm.edit_body_part.data
                    edit_tissue = editForm.edit_tissue.data
                    edit_trauma = editForm.edit_trauma.data
                    edit_start = editForm.edit_start.data
                    edit_end = editForm.edit_end.data
                    edit_details = editForm.edit_details.data
                    flash('{} {} {} {} {} {}'.format(edit_body_part, edit_tissue, edit_trauma, edit_start, edit_end, edit_details))

                    now = date.today()

                    contusion.body_part_id, contusion.tissue_id, contusion.trauma_id, contusion.start, contusion.end, contusion.details = edit_body_part, edit_tissue, edit_trauma, edit_start, edit_end, edit_details

                    if now < edit_end:
                        user.state = "CONTUSION"
                        contusion.state = "ACTIVE"
                    else:
                        #TODO jezeli nie ma innej kontuzji to dopiero aktive
                        user.state = "HEALTHY"
                        contusion.state = "PAST"

                    contusion.save()


                else:
                    flash_errors(editForm)




                return render_template("user_page.html", user=user, user_info=user_info, nationality=nationality,
                                   position=position, user_page="{} - User Page".format(user.username), form=form, editform=editForm,
                                   contusion=user.contusion)




        if form.validate_on_submit():
            new_contusion = Contusion(body_part_id=form.body_part.data,
                                      start=form.start.data,
                                      end=form.end.data,
                                      tissue_id = form.tissue.data,
                                      trauma_id=form.trauma.data,
                                      details=form.details.data)

            now = date.today()


            if now < new_contusion.end:
                user.state = "CONTUSION"
                new_contusion.state = "ACTIVE"
            else:
                new_contusion.state = "PAST"

            new_contusion.save()
            user.contusion.append(new_contusion)
            user.save()


            flash(new_contusion.__repr__(current_user.language))
            return redirect(url_for('people_page', id=id))
        else:
            flash_errors(form)


        return render_template("user_page.html" , user=user, user_info=user_info, nationality=nationality, position=position, user_page="{} - User Page".format(user.username), form=form, contusion=user.contusion)

    else:
        flash(_('You can not see people who are not in your team!'))
        return redirect(url_for("home"))


#users pages
@app.route('/users/<int:id>/motoric', methods=['GET'])
@login_required
@blocked_access('player')
def people_page_motoric(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    elif ('staff' in user.show_role()) or ('admin' in user.show_role()):
        flash(_('Staff and admins dont have pages!'))
        return redirect(url_for("home"))

    elif (current_user.show_team() in user.show_team()) or (current_user.show_role() in 'admin'):
        #same_team = True
        #flash("{} ----- {} \n same team: {}".format(user.show_team(), current_user.show_team(), same_team))

        user_info = user.get_basic_info()
        position = Position.get_position_name_by_lang(user, user_info)

        nationality = Nationality.get_nationality_name_by_lang(user)

        return render_template("user_page_motoric.html" , user=user, user_info=user_info, nationality=nationality, position=position, user_page="{} - User Page".format(user.username))

    else:
        flash(_('You can not see people who are not in your team!'))
        return redirect(url_for("home"))

        return render_template("user_page_motoric.html")

#user medical 
@app.route('/users/<int:id>/medical', methods=['GET'])
@login_required
@blocked_access('player')
def people_page_medical(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    elif ('staff' in user.show_role()) or ('admin' in user.show_role()):
        flash(_('Staff and admins dont have pages!'))
        return redirect(url_for("home"))

    elif (current_user.show_team() in user.show_team()) or (current_user.show_role() in 'admin'):
        #same_team = True
        #flash("{} ----- {} \n same team: {}".format(user.show_team(), current_user.show_team(), same_team))

        user_info = user.get_basic_info()
        position = Position.get_position_name_by_lang(user, user_info)

        nationality = Nationality.get_nationality_name_by_lang(user)

        return render_template("user_page_medical.html" , user=user, user_info=user_info, nationality=nationality, position=position, user_page="{} - User Page".format(user.username))

    else:
        flash(_('You can not see people who are not in your team!'))
        return redirect(url_for("home"))

        return render_template("user_page_medical.html")

#user survey
@app.route('/users/<int:id>/surveys', methods=['GET'])
@login_required
@blocked_access('player')
def people_page_survey(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    elif ('staff' in user.show_role()) or ('admin' in user.show_role()):
        flash(_('Staff and admins dont have pages!'))
        return redirect(url_for("home"))

    elif (current_user.show_team() in user.show_team()) or (current_user.show_role() in 'admin'):
        #same_team = True
        #flash("{} ----- {} \n same team: {}".format(user.show_team(), current_user.show_team(), same_team))

        user_info = user.get_basic_info()
        position = Position.get_position_name_by_lang(user, user_info)

        nationality = Nationality.get_nationality_name_by_lang(user)

        return render_template("user_page_survey.html" , user=user, user_info=user_info, nationality=nationality, position=position, user_page="{} - User Page".format(user.username))

    else:
        flash(_('You can not see people who are not in your team!'))
        return redirect(url_for("home"))

        return render_template("user_page_survey.html")

#user summary
@app.route('/users/<int:id>/resume', methods=['GET'])
@login_required
@blocked_access('player')
def people_page_summary(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    elif ('staff' in user.show_role()) or ('admin' in user.show_role()):
        flash(_('Staff and admins dont have pages!'))
        return redirect(url_for("home"))

    elif (current_user.show_team() in user.show_team()) or (current_user.show_role() in 'admin'):
        #same_team = True
        #flash("{} ----- {} \n same team: {}".format(user.show_team(), current_user.show_team(), same_team))

        user_info = user.get_basic_info()
        position = Position.get_position_name_by_lang(user, user_info)

        nationality = Nationality.get_nationality_name_by_lang(user)

        return render_template("user_summary.html" , user=user, user_info=user_info, nationality=nationality, position=position, user_page="{} - User Page".format(user.username))

    else:
        flash(_('You can not see people who are not in your team!'))
        return redirect(url_for("home"))

        return render_template("user_summary.html")

@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
@is_logged
def confirm_email(token):
    if not User.confirm_mail_token(token):
        # TODO Create refresh for email if lost time
        flash(_('The link has expired, do you want to get a new one?'))
        return _("The link has expired, do you want to get a new one?")

    email=User.confirm_mail_token(token)
    user=User.query.filter_by(email=email).first()
    if user is None:
        flash(_("No user with this mail in the system!"))
        return redirect(url_for('auth_bp.login'))

    if user.is_active() is True:

        flash(_("Your account has been activated!"))
        return redirect(url_for('auth_bp.login'))



    form = SetUserPasswordForm()



    if form.validate_on_submit():

        #TODO CHECK THE VALIDATION IF WORKS

        avatar = form.avatar.data
        avatar.seek(0)
        '''
        if len(avatar.read()) > 1000:
            flash(_("Your file is too large! Max size for avatar is 1MB"))
            return url_for(confirm_email(token))
        '''

        filename = secure_filename(avatar.filename)

        path = app_path+'/'+user.folder+"/avatars/"

        extension = os.path.splitext(filename)[1]
        image_id = str(uuid.uuid4())

        filename = image_id + extension

        avatar.save(os.path.join(path, filename))

        user.avatar = filename

        user._set_password(form.password.data)
        user.confirmed_at = datetime.now(Config.APP_TIMEZONE)
        user.active = True
        user.save()
        flash(_("Your account has been activated! Please log in"), 'success')
        return redirect(url_for('auth_bp.login'))



    return render_template('confirmmail.html', form=form, email=email, user=user)



@app.route('/reset_password', methods=['GET', 'POST'])
@is_logged
def reset_request():
    form = RequestResetPasswordUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        subject=_("You can reset your password!!")
        token = user.generate_confirmation_mail_token()
        send_reset_password__mail(subject, token, user.email)
        flash(_("Reset link sent to %s" %(form.email.data)), 'info')
        return redirect(url_for('auth_bp.login'))

    return render_template('reset_request.html', title="Request a set Password", form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
@is_logged
def reset_password(token):
    email = User.confirm_mail_token(token)
    if not email:
        flash(_('Invalid or expired token'), 'error')
        return redirect(url_for('reset_request'))


    form = ResetPasswordUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        user._set_password(form.password.data)
        user.save()
        flash(_("Your new password has been updated!"), 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('reset_password_g.html', title="Reset Password", form=form)



@app.get('/calendar')
@login_required
def calendar():
    if 'player' in current_user.show_role():
        events = current_user.events
        return render_template("calendar.html", title="Calendar", events= events)
    return render_template("calendar.html", title="Calendar")

@app.get('/surveys')
@blocked_access('staff')
@login_required
def survey():
    if current_user.show_role() in 'admin':
        events = Event.get_events_past()

        return render_template("surveys.html", title="Surveys", events=events )

    if current_user.show_role() in 'player':
        events = current_user.events

        return render_template("surveys.html", title="Surveys", events=events )


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def profile_settings():

    form = ResetPasswordUserForm()
    form2 = ChangeAvatarUserForm()
    user = User.query.filter_by(id=current_user.id).first()

    if form.submit.data and form.validate():
        user._set_password(form.password.data)
        user.save()
        flash(_("Your new password has been updated!"), 'success')


    if form2.submitAvatar.data and form2.validate():
        avatar = form2.avatar.data
        avatar.seek(0)

        filename = secure_filename(avatar.filename)

        extension = os.path.splitext(filename)[1]
        image_id = str(uuid.uuid4())

        filename = image_id + extension

        path = app_path+'/'+user.folder+"/avatars/"

        avatar.save(os.path.join(path, filename))
        user.avatar = filename
        user.save()
        flash(_("Your new Avatar has been set!"),'success')

    return render_template("profile_settings.html", title="Profile Settings", form=form, form2=form2)










@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')



'''
@app.route('/files/<int:id>/avatars')
def avatar_photo(id):
    user = User.query.filter_by(id=id).first()
    return app.send_static_file('uploads/user_data/{}/avatars/{}'.format(id, user.avatar))
   # return redirect(url_for('static', filename='uploads/user_data/{}/avatars/{}'.format(id, user.avatar)))
'''

@app.route('/files/<int:id>/avatars/')
@login_required
def avatar_photo(id):
    user = User.query.filter_by(id=id).first()


    if user.avatar is not None:
        filename=user.avatar
        path = '{}/{}/avatars/'.format(app_path, user.folder)
        path2 = os.path.join(app_path,user.folder+"/avatars/")

        path2i = path2


        resp = send_from_directory(path2, filename)
        return resp
    else:
        return  app.send_static_file('images/blank_avatar.jpg')


@app.route('/language/<language>')
@login_required
def set_language(language=None):
    user = current_user
    user.language = language
    user.save()
    return redirect(url_for('home'))


@app.route('/language')
@login_required
def language():
    return current_user.language


@app.context_processor
def inject_conf_var():
    LANGUAGES = Config.LANGUAGES
    return LANGUAGES


@app.route('/messages')
@login_required
def messages():
    users = User.query.filter(User.teams.any(name=current_user.show_team())).all()
    if current_user.show_role() in 'admin':
        users = User.query.all()



    return render_template("messages.html", title="Messages Settings", users=users)




@app.route('/<int:event_id>/wellness-survey/', methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'admin')
def wellness_survey(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash(_("This event does not exist!"), 'error')
        return redirect(url_for("home"))

    link = '/{}/wellness-survey'.format(event.id)
    wellness = Wellness.get_user_welless_of_event(current_user, event.id)
    if (event.type_id in [1,2,3,4]) and event in current_user.events and wellness.state == "TO-COMPLETE":
        wellness_form = WellnessForm()
        survey_start = datetime.utcnow()

        if wellness_form.validate_on_submit():

            wellness.name=""
            #wellness.sleep_duration=wellness_form.sleep_duration.data
            wellness.sleep_quality=wellness_form.sleep_quality.data
            wellness.muscle_soreness=wellness_form.muscle_soreness.data
            #wellness.energy=wellness_form.energy.data
            wellness.mood=wellness_form.mood.data
            wellness.stress=wellness_form.stress.data
            wellness.fatigue=wellness_form.fatigue.data
            wellness.mental_focus=wellness_form.mental_focus.data
            #wellness.nutrional_amount=wellness_form.nutrional_amount.data
            #wellness.nutrional_quality=wellness_form.nutrional_quality.data
            #wellness.hydration=wellness_form.hydration.data
            #wellness.comment=wellness_form.comment.data
            wellness.total_time=datetime.utcnow() - survey_start
            wellness.state = "COMPLETED"

            wellness.save()
            current_user.checked_notification(link)

            flash(_("Survey completed!"), 'success')
            return redirect(url_for("home"))
        else:
            flash(_("Fill all inputs"))
        return render_template("wellness_survey.html", title="Complete Survey", event=event, form=wellness_form)
    elif wellness.state == "COMPLETED":
        flash(_("You have completed this survey!"), 'info')
        return redirect(url_for("home"))

    else:
        flash(_("survey is not ready to be completed!"), 'error')
        return redirect(url_for("home"))



@app.route('/<int:event_id>/rpe-survey/', methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'admin')
def rpe_survey(event_id):

    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash(_("This event does not exist!"), 'error')
        return redirect(url_for("home"))


    link = '/{}/rpe-survey'.format(event.id)
    w_link ='/{}/wellness-survey'.format(event.id)
    rpe = RPE.get_user_rpe_of_event(current_user, event.id)
    wellness = Wellness.get_user_welless_of_event(current_user, event.id)
    if (rpe is not None and wellness is not None) and (event.type_id in [1,2,3,4]) and (event.state == "MOTORIC" or event.state == "KINASIS" or event.state == "PAST") and (event in current_user.events and rpe.state == "TO-COMPLETE" and wellness.state == "COMPLETED"):
        rpe_form = RPEForm()
        survey_start = datetime.utcnow()

        if rpe_form.validate_on_submit():
            rpe.value=rpe_form.training_note.data
            rpe.state = "COMPLETED"
            rpe.total_time=datetime.utcnow() - survey_start

            rpe.save()

            current_user.checked_notification(link)

            flash(_("Survey completed!"), 'success')
            return redirect(url_for("home"))
        else:
            flash(_("Fill all inputs"))
        return render_template("rpe-survey.html", title="Complete Survey", event=event, form=rpe_form)

    elif wellness.state == "TO-COMPLETE":
        flash(Markup(_("You have not completed your Wellness survey! Do it before here: <a href='%s'>Complete Wellness</a>" %(w_link))), 'info')
        return redirect(url_for("home"))

    elif rpe is None or wellness is None:
        flash(_("No rpe or wellness created obj"))
        return redirect(url_for("home"))

    else:
        flash(_("You have completed this survey!") , "error")
        return redirect(url_for("home"))

@app.route('/<int:event_id>/motoric-import/', methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'player')
def import_motoric(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash(_("This event does not exist!"), 'error')
        return redirect(url_for("home"))
    link = '/{}/motoric-import'.format(event.id)
    participants = event.get_id_of_users_in_event()
    motorics = event.get_motorics_of_event()
    motorics_completed = [completed for completed in event.get_motorics_of_event() if completed.state == "COMPLETED"]
    message = []
    #TODO dawalo błedy <- trzeba sprawdzić czy wszystkie motoriki byly wykonana, jezeli tak, to zablokuj i zapomnij
    '''
    if motorics == motorics_completed:
        Notification.checked_notification_admins(link)
        if event.has_kinase == True:
            event.state = "KINASIS"
            flash(_("This kinase import has been completed"))
        else:
            event.state = "PAST"
            flash(_("This kinase import has been completed"))
    '''
    if (event is not None) and (event.state == "MOTORIC"):
        form = AddMotoricDataForm()


        if form.validate_on_submit():

            uploaded_file = form.motoric_data.data
            uploaded_file.seek(0)
            file = pd.read_csv(uploaded_file)

            df = pd.DataFrame(file, columns=['Name', 'Date',
                                             'Total Distance (m)', 'Sprint (m)',
                                             'Total Player Load', 'HSR (m)',
                                             'Acceleration', 'Deceleration', 'Field Time',
                                             'Maximum Velocity (km/h)', 'Meterage Per Minute', 'Max Vel (% Max)',
                                             'Running (m)'])
            participants_added = []
            #users_planed_in_event = event.get_users_of_event()
            try:
                for i, row in df.iterrows():
                    first_name, last_name = row[0].split(" ")[0], row[0].split(" ")[1]
                    user = User.query.filter(User.first_name == first_name, User.last_name == last_name).first()
                    if user is not None and user in participants:

                        motoric = user.get_motoric_of_event(event.id)[0]
                        if motoric.state == "TO-COMPLETE":
                            # minutes to time = int() ->  if field.type == intdatetime.timedelta(minutes=72)datetime.timedelta(minutes=row[8])
                            motoric.date=datetime.strptime(row[1], '%d/%m/%Y')
                            motoric.total_distance=row[2]
                            motoric.sprint=row[3]
                            motoric.total_player_load=row[4]
                            motoric.hsr=row[5]
                            motoric.acceleration=row[6]
                            motoric.deceleration=row[7]
                            motoric.field_time=row[8]
                            motoric.maximum_velocity=row[9]
                            motoric.meterage_per_minute=row[10]
                            motoric.max_vel_per_max=row[11]
                            motoric.running=row[12]
                            motoric.state = "COMPLETED"

                            participants_added.append(user)




                            txt = '{} {} motoric!'.format(user, motoric)
                            message.append(txt)
                            motoric.save()










                    else:
                        txt = 'No user {} {} in the system !'.format(first_name, last_name)
                        message.append(txt)

                for user in participants:
                    user = User.query.filter_by(id=user.id).first()
                    if user is not None and len(user.motoric) != 0:
                        motoric = user.get_motoric_of_event(event.id)[0]
                        if motoric.state == "TO-COMPLETE":
                            motoric.total_distance = 0
                            motoric.sprint = 0
                            motoric.total_player_load = 0
                            motoric.hsr = 0
                            motoric.acceleration = 0
                            motoric.deceleration = 0
                            motoric.field_time = 0
                            motoric.maximum_velocity = 0
                            motoric.meterage_per_minute = 0
                            motoric.max_vel_per_max = 0
                            motoric.running = 0
                            motoric.state = "COMPLETED"
                            motoric.save()


                return redirect(url_for('import_motoric_lock' ,event_id=event_id))
            except:
                flash('file have errors')



        return render_template("import_motoric.html", title="Add data for event", participants=participants,
                               event=event, form=form, message=message)

    else:
        #TODO usunać to do debugingu bardziej
        notification = Notification.query.filter_by(link=link).all()
        for i in notification:
            i.checked = True
            i.save()
        flash(_("This import has been already completed!"))
        return redirect(url_for("home"))


@app.post('/<int:event_id>/motoric-import/manually')
@login_required
@blocked_access('staff', 'player')
def import_motoric_by_api(event_id):
    data = request.get_json()
    event = Event.query.filter_by(id=event_id).first()
    participants = event.get_id_of_users_in_event()
    if event is None:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}

    participants_added = []
    for i in data:
        user = User.query.filter_by(id=i.get('id')).first()
        if user is not None:
            motoric = user.get_motoric_of_event(event.id)[0]
            if user in participants and motoric.state == "TO-COMPLETE":
                motoric.total_distance = i.get('total_distance')
                motoric.sprint = i.get('sprint')
                motoric.total_player_load = i.get('total_player_load')
                motoric.hsr = i.get('hsr')
                motoric.acceleration = i.get('acceleration')
                motoric.deceleration = i.get('deceleration')
                motoric.field_time = i.get('field_time')
                motoric.maximum_velocity = i.get('maximum_velocity')
                motoric.meterage_per_minute = i.get('meterage_per_minute')
                motoric.max_vel_per_max = i.get('max_vel_per_max')
                motoric.running = i.get('running')
                motoric.state = "COMPLETED"
                motoric.save()

                participants_added.append(user)



    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.motoric) != 0:
            motoric = user.get_motoric_of_event(event.id)[0]
            if motoric.state == "TO-COMPLETE":
                motoric.total_distance = 0
                motoric.sprint = 0
                motoric.total_player_load = 0
                motoric.hsr = 0
                motoric.acceleration = 0
                motoric.deceleration = 0
                motoric.field_time = 0
                motoric.maximum_velocity = 0
                motoric.meterage_per_minute = 0
                motoric.max_vel_per_max = 0
                motoric.running = 0
                motoric.state = "COMPLETED"
                motoric.save()

    not_added = [{'name': user.first_name, 'second_name': user.last_name, 'added': _("Not added")} for user in participants if user not in participants_added]
    added = [{'name': user.first_name, 'second_name': user.last_name, 'added': _("Added")} for user in participants_added]
    result = added + not_added



    return jsonify(result)



@app.route('/<int:event_id>/motoric-import/lock',  methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'player')
def import_motoric_lock(event_id):
    event = Event.query.filter_by(id=event_id).first()
    link = '/{}/motoric-import'.format(event.id)
    if (event is not None) and (event.state != "MOTORIC"):
        flash(_("Data to this event has been added before"))
        return redirect(url_for("home"))


    if event.has_kinase == True:
        event.state = "KINASIS"
        event.send_kinase_notification_to_admins()
    else:
        event.state = "PAST"

    event.save()
    Notification.checked_notification_admins(link)
    flash(_("This Motoric import has been completed"))
    return redirect(url_for("home"))






@app.route('/<int:event_id>/kinase-import/', methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'player')
def import_kinasis(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash("No event with this id!")
        return redirect(url_for("home"))

    link = '/{}/kinase-import'.format(event.id)
    motoric = Motoric.query.filter_by(event_id=event_id).all()
    participants = event.get_id_of_users_in_event()
    if event is not None and event.state == "KINASIS":
        if len(motoric) == 0: #TODO NOT LEN MOTORIC - every MOTORIC MUST BE COMPLETED
            flash(Markup(_("this event dont have motric data added! do it before here: <a href='%s'>Add motoric data</a>" %(link))))
            return redirect(url_for("home"))

    return render_template("import_kinase.html", title="Add data for event", participants=participants,
                               event=event)






@app.post('/<int:event_id>/kinase-import/manually')
@login_required
@blocked_access('staff', 'player')
def import_kinase_by_api(event_id):
    data = request.get_json()
    event = Event.query.filter_by(id=event_id).first()
    participants = event.get_id_of_users_in_event()
    if event is None:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}

    participants_added = []
    for i in data:
        user = User.query.filter_by(id=i.get('id')).first()
        if user is not None:
            kinase = user.get_kinase_of_event(event.id)[0]
            if user in participants: #and kinase.state == "TO-COMPLETE":
                kinase.value = i.get('kinase')
                kinase.state = "COMPLETED"
                kinase.save()

                participants_added.append(user)

    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.motoric) != 0:
            kinase = user.get_kinase_of_event(event.id)[0]
            if kinase.state == "TO-COMPLETE":
                kinase.value = 0
                kinase.state = "COMPLETED"
                kinase.save()

    not_added = [{'name': user.first_name, 'second_name': user.last_name, 'added': _("Not added")} for user in participants if user not in participants_added]
    added = [{'name': user.first_name, 'second_name': user.last_name, 'added': _("Added")} for user in participants_added]
    result = added + not_added

    return jsonify(result)



@app.route('/<int:event_id>/kinase-import/lock',  methods=['GET', 'POST'])
@login_required
@blocked_access('staff', 'player')
def import_kinase_lock(event_id):
    event = Event.query.filter_by(id=event_id).first()
    link = '/{}/kinase-import'.format(event.id)
    if (event is None) and (event.state != "KINASIS"):
        flash(_("Data to this event has been added before"))
        return redirect(url_for("home"))

    event.state = "PAST"
    event.save()
    Notification.checked_notification_admins(link)
    flash(_("This import has been completed"))
    return redirect(url_for("home"))





@app.route('/messages/<recipient>')
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    pass

@app.get('/support')
@login_required
def support():
    return render_template("support.html", title="Support")

@app.get('/notifications')
@login_required
def notifications():

    notifications = current_user.notifications

    return notification_schema.jsonify(notifications)


@app.get('/refresh')
@login_required
def refresh():
    events = Event.query.filter_by(state="WELLNESS").all()
    print("Checking")
    for event in events:
        event.check_state_if_event_past()

    flash(_("event id past checked!!"))

    return redirect(url_for('home'))

@app.get('/w-refresh')
@login_required
def w_refresh():
    events = Event.query.filter_by(state="ACTIVE").all()
    print("Checking if wellness")
    for event in events:
        event.check_state_if_event_wellness()

    flash(_("event wellness past checked!!"))

    return redirect(url_for('home'))

@app.get('/p-refresh')
@login_required
def p_refresh():
    events = Event.query.filter_by(state="MOTORIC").all()
    print("Checking if PAST")
    for event in events:
        event.state = "PAST"
        event.save()

    flash(("event past checked!!"))

    return redirect(url_for('home'))

@app.get('/k-refresh')
@login_required
def k_refresh():
    events = Event.query.filter_by(state="KINASIS").all()
    print("Checking if PAST")
    for event in events:
        event.state = "PAST"
        event.save()

    flash(("event past checked!!"))

    return redirect(url_for('home'))


@app.route('/users/<int:id>/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@blocked_access('player', 'staff')
def edit_event_data(id, event_id):
    #TODO NAPRAWIC TE GLUPIE BLEDY
    user = User.query.filter_by(id=id).first()
    event = Event.get_event(event_id)

    if user is None:
        flash(_('This person does not exist in the system!'))
        return redirect(url_for("home"))

    if event not in user.events:
        flash(_('This person is not part of this event!'))
        return redirect(url_for("home"))

    if event is None:
        flash(_('This event does not exist in the system!'))
        return redirect(url_for("home"))

    if event.state != "PAST":
        flash(_('This event does not have completed data!'))
        return redirect(url_for("home"))

    motoricForm = EditMotoricDataForm(obj=user.get_motoric_of_event(event_id)[0])

    if event.has_kinase is True:
        kinaseForm = EditKinaseDataForm(obj=user.get_kinase_of_event(event_id)[0])

        if motoricForm.validate_on_submit() and motoricForm.submitMotoric.data:
            motoric = user.get_motoric_of_event(event_id)[0]

            motoric.total_distance = motoricForm.total_distance.data
            motoric.hsr = motoricForm.hsr.data
            motoric.acceleration = motoricForm.acceleration.data
            motoric.sprint = motoricForm.sprint.data
            motoric.total_player_load = motoricForm.total_player_load.data
            motoric.deceleration = motoricForm.deceleration.data
            motoric.field_time = motoricForm.field_time.data
            motoric.maximum_velocity = motoricForm.maximum_velocity.data
            motoric.max_vel_per_max = motoricForm.max_vel_per_max.data
            motoric.meterage_per_minute = motoricForm.meterage_per_minute.data
            motoric.running = motoricForm.running.data

            motoric.save()
            flash(_("Motoric data edited"), 'success')
        else:
            flash_errors(motoricForm)

        if request.method == 'GET':
            motoric = user.get_motoric_of_event(event_id)[0]
            kinase = user.get_kinase_of_event(event_id)[0]

            motoricForm.total_distance.data = motoric.total_distance
            motoricForm.hsr.data = motoric.hsr
            motoricForm.acceleration.data = motoric.acceleration
            motoricForm.sprint.data = motoric.sprint
            motoricForm.total_player_load.data = motoric.total_player_load
            motoricForm.deceleration.data = motoric.deceleration
            motoricForm.field_time.data = motoric.field_time
            motoricForm.maximum_velocity.data = motoric.maximum_velocity
            motoricForm.max_vel_per_max.data = motoric.max_vel_per_max
            motoricForm.meterage_per_minute.data = motoric.meterage_per_minute
            motoricForm.running.data = motoric.running

            kinaseForm.value.data = kinase.value



        if kinaseForm.validate_on_submit() and kinaseForm.submitKinase.data:
            kinase = user.get_kinase_of_event(event_id)[0]

            kinase.value = kinaseForm.value.data
            print(kinase.value)


            kinase.save()
            flash(_("Kinase data edited"), 'success')
            redirect(url_for('edit_event_data', id=id, event_id=event_id))
        else:
            flash_errors(kinaseForm)


        return render_template('edit_data.html', event=event, player=user, form=motoricForm, kform = kinaseForm)

    else:
        motoric = user.get_motoric_of_event(event_id)[0]
        if request.method == 'GET':


            motoricForm.total_distance.data = motoric.total_distance
            motoricForm.hsr.data = motoric.hsr
            motoricForm.acceleration.data = motoric.acceleration
            motoricForm.sprint.data = motoric.sprint
            motoricForm.total_player_load.data = motoric.total_player_load
            motoricForm.deceleration.data = motoric.deceleration
            motoricForm.field_time.data = motoric.field_time
            motoricForm.maximum_velocity.data = motoric.maximum_velocity
            motoricForm.max_vel_per_max.data = motoric.max_vel_per_max
            motoricForm.meterage_per_minute.data = motoric.meterage_per_minute
            motoricForm.running.data = motoric.running


        elif motoricForm.validate_on_submit() and motoricForm.submitMotoric.data and request.method== 'POST':

            motoric.total_distance = float(motoricForm.total_distance.data)
            motoric.hsr = float(motoricForm.hsr.data)
            motoric.acceleration = float(motoricForm.acceleration.data)
            motoric.sprint = float(motoricForm.sprint.data)
            motoric.total_player_load = float(motoricForm.total_player_load.data)
            motoric.total_player_load = float(motoricForm.total_player_load.data)
            motoric.deceleration = motoricForm.deceleration.data
            motoric.field_time = motoricForm.field_time.data
            motoric.maximum_velocity = motoricForm.maximum_velocity.data
            motoric.max_vel_per_max = motoricForm.max_vel_per_max.data
            motoric.meterage_per_minute = motoricForm.meterage_per_minute.data
            motoric.running = motoricForm.running.data

            motoric.save()

            flash(_("Motoric data edited"), 'success')
        else:
            flash_errors(motoricForm)


        return render_template('edit_data.html', event=event, player=user, form=motoricForm)






@app.get('/player-file')
@login_required
@blocked_access('player', 'staff')
def download_player_file():
    return app.send_static_file('docs/player_import_demonstration.xlsx')

@app.get('/motoric-file')
@login_required
@blocked_access('player', 'staff')
def download_motoric_file():
    return app.send_static_file('docs/export1.csv')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def handle_400_error(e):
    return render_template('400.html'), 400

@app.errorhandler(401)
def custom_401(error):
    return render_template('401_403_405.html'), 401

@app.errorhandler(403)
def handle_403_error(e):
    return render_template('401_403_405.html'), 403

@app.errorhandler(405)
def handle_405_error(e):
    return render_template('401_403_405.html'), 405

@app.errorhandler(406)
def handle_406_error(e):
    return render_template('40x.html'), 406

def handle_408_error(e):
    return render_template('40x.html'), 408

@app.errorhandler(409)
def handle_409_error(e):
    return render_template('40x.html'), 409

@app.errorhandler(410)
def handle_410_error(e):
    return render_template('40x.html'), 410

@app.errorhandler(411)
def handle_411_error(e):
    return render_template('411_413_414.html'), 411

@app.errorhandler(412)
def handle_412_error(e):
    return render_template('40x.html'), 412

@app.errorhandler(413)
def handle_413_error(e):
    return render_template('411_413_414.html'), 413

@app.errorhandler(414)
def handle_414_error(e):
    return render_template('411_413_414.html'), 414

@app.errorhandler(415)
def handle_415_error(e):
    return render_template('40x.html'), 415

@app.errorhandler(416)
def handle_416_error(e):
    return render_template('40x.html'), 416

@app.errorhandler(417)
def handle_417_error(e):
    return render_template('40x.html'), 417

@app.errorhandler(500)
def internal_error(error):
    return render_template('40x.html'), 500

@app.errorhandler(501)
def internal_error(error):
    return render_template('40x.html'), 501

@app.errorhandler(502)
def internal_error(error):
    return render_template('40x.html'), 502

@app.errorhandler(503)
def internal_error(error):
    return render_template('40x.html'), 503

@app.errorhandler(504)
def internal_error(error):
    return render_template('40x.html'), 504

@app.errorhandler(505)
def internal_error(error):
    return render_template('40x.html'), 505

