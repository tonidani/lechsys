import uuid

from flask import url_for

from app import db
from app import ma
from flask_login import UserMixin
from marshmallow import fields
from config import Config
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

import pandas as pd

from time import time
import json



from app import login, app_path
from werkzeug.security import generate_password_hash , check_password_hash
import datetime
import os
import shutil
import random


# ORM for DB models
class BaseModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# UserMixin is needed for authentication and login process (flask-login)
class User(db.Model, UserMixin, BaseModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True , unique=True)
    username = db.Column(db.String(64), index=True , unique=True)
    password = db.Column(db.String(256))

    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.now(Config.APP_TIMEZONE))
    confirmed_at = db.Column(db.DateTime())
    birth_date = db.Column(db.Date())
    state = db.Column(db.String(64), default="HEALTHY")

    nationality = db.Column(db.Integer, db.ForeignKey('nationalities.id'))




    last_seen = db.Column(db.DateTime, default=datetime.datetime.now(Config.APP_TIMEZONE))
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    roles = db.relationship('Role', secondary='user_roles')
    teams = db.relationship('Team', secondary='user_teams')
    events = db.relationship('Event', secondary='user_events')

    #Messages part

    last_message_read_time = db.Column(db.DateTime)

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')


    #notification PART

    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    #User conf

    language = db.Column(db.Text, default='pl')

    avatar = db.Column(db.Text)

    folder = db.Column(db.Text)


    motoric = db.relationship('Motoric', secondary='user_motoric')

    wellness = db.relationship('Wellness', secondary='user_wellness')

    rpe = db.relationship('RPE', secondary='user_rpe')

    kinase = db.relationship('Kinase', secondary='user_kinase')

    contusion = db.relationship('Contusion', secondary='user_contusion')

    basic_info = db.relationship("UserBasicInfo",
                           backref=db.backref('user'))


    def __init__(self, first_name, last_name, email, uuid=str(uuid.uuid4()), birth_date=None, confirmed_at=None, active=False, username=None,
                 avatar=None, nationality=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.confirmed_at = confirmed_at
        self.active = active
        self.uuid = uuid
        self.folder = os.path.join("user_data/",uuid)
        self.avatar = avatar
        self.birth_date = birth_date
        self.nationality = nationality
        #self.folder = '{}/user_data/{}/'.format(app_path, self.email)




    def _set_password(self, password):
        self.password = generate_password_hash(password)

    def _check_password(self, password):
        return check_password_hash(self.password, password)

    def validate_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return False
        return True

    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return False
        return True

    def show_role(self):
        return ' '.join([role.name for role in self.roles])

    def show_team(self):
        return ' '.join([team.name for team in self.teams])

    def is_active(self):
        return self.active

    def create_user_data_folder(self):
        try:
            os.umask(0)
            os.makedirs(os.path.join(app_path,self.folder))
            os.makedirs(os.path.join(app_path,self.folder+"/avatars/"), mode=0o777)
            os.makedirs(os.path.join(app_path,self.folder+"/files/"), mode=0o777)
            os.makedirs(os.path.join(app_path,self.folder+"/photos/"), mode=0o777)
            return True
        except:
            return False

    def delete_user_data_folder(self):
        pass

#        try: #if path exist, it will be deleted
#            return shutil.rmtree(os.path.join(app_path,self.folder))
#        except:
#            return False


    def generate_confirmation_mail_token(self):
        mail_serializer=URLSafeTimedSerializer(Config.MAIL_SERIALIZER_SECRET)
        return mail_serializer.dumps(self.email , salt=Config.MAIL_SALT)

    @staticmethod
    def confirm_mail_token(token , expiration=Config.EXPIRATION_TOKEN_TIME) :
        serializer=URLSafeTimedSerializer(Config.MAIL_SERIALIZER_SECRET)
        try :
            email=serializer.loads(
                token ,
                salt=Config.MAIL_SALT ,
                max_age=expiration
            )
        except SignatureExpired :
            return None
        return email

    def create_username(self):
       # first_letter = self.first_name[0][0].lower()
       # full_name = '{}{}'.format(self.first_name, self.last_name.lower())
      #  three_letters_surname = full_name[-1][:3].rjust(3 , 'x')
       # three_letters_surname = full_name[-1][:3].rjust(3 , 'x')

        number = '{:03d}'.format(random.randrange(1 , 999))
        self.username ='{}{}{}'.format(self.first_name[:3].lower() , self.last_name[:3].lower() , number)
        return self.username

    def get_basic_info(self):
        return UserBasicInfo.query.filter_by(user_id=self.id).first()

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime.datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, notification):
        #self.notifications.filter_by(name=name).delete()
        notification.user_id = self.id

        notification.save()
        return notification

    def checked_notification(self, link):
        notification = Notification.query.filter_by(user_id=self.id, link=link).one()

        notification.checked = True
        notification.save()
        return notification




    def user_active_events(self):
        return [i for i in self.events if i.state == "ACTIVE"]


    def user_inactive_events(self):
        return [i for i in self.events if i.state == "PAST"]

    def get_user_info(self):
        return UserBasicInfo.query.filter_by(user_id=self.id).first()


    def get_motoric_of_event(self, event_id):
        return [i for i in self.motoric if i.event_id == event_id]

    def get_kinase_of_event(self, event_id):
        return [i for i in self.kinase if i.event_id == event_id]

class Message(db.Model, BaseModelMixin):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now(Config.APP_TIMEZONE))

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Role(db.Model, BaseModelMixin):

    __tablename__ = "roles"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)


class Team(db.Model, BaseModelMixin):

    __tablename__ = "teams"

    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(64) , unique=True)

    events = db.relationship('Event' , secondary='team_events')

class TeamEvents(db.Model, BaseModelMixin):
    __tablename__ = "team_events"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))

class UserMotoric(db.Model, BaseModelMixin):
    __tablename__ = "user_motoric"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    motoric_id = db.Column(db.Integer, db.ForeignKey('motoric.id', ondelete='CASCADE'))

class UserWellness(db.Model, BaseModelMixin):
    __tablename__ = "user_wellness"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    wellness_id = db.Column(db.Integer, db.ForeignKey('wellness.id', ondelete='CASCADE'))

class UserRpe(db.Model, BaseModelMixin):
    __tablename__ = "user_rpe"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    rpe_id = db.Column(db.Integer, db.ForeignKey('rpe.id', ondelete='CASCADE'))


class UserKinase(db.Model, BaseModelMixin):
    __tablename__ = "user_kinase"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    kinase_id = db.Column(db.Integer, db.ForeignKey('kinase.id', ondelete='CASCADE'))

class UserContusion(db.Model, BaseModelMixin):
    __tablename__ = "user_contusion"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    contusion_id = db.Column(db.Integer, db.ForeignKey('contusion.id', ondelete='CASCADE'))

class Contusion(db.Model, BaseModelMixin):

    __tablename__ = "contusion"
    id = db.Column(db.Integer, primary_key=True)
    body_part_id = db.Column(db.Integer, db.ForeignKey('body_parts.id'))
    tissue_id = db.Column(db.Integer, db.ForeignKey('tissues.id'))
    trauma_id = db.Column(db.Integer, db.ForeignKey('traumas.id'))

    start = db.Column(db.Date)
    end = db.Column(db.Date)
    details = db.Column(db.String(128))
    state = db.Column(db.String(128), default="ACTIVE")

    def __repr__(self, lang):
        body_part = BodyPart.query.filter_by(id=self.body_part_id).first()
        tissue = Tissue.query.filter_by(id=self.tissue_id).first()
        trauma = Trauma.query.filter_by(id=self.trauma_id).first()

        if lang == "pl":
            return f"Kontuzja: Część ciała - {body_part.name_pl}, Rodzaj tkanki - {tissue.name_pl}, Rodzaj kontuzji - {trauma.name_pl}"
        else:
            return f"Contusion: Part - {body_part.name_eng}, Tissue - {tissue.name_eng}, Trauma - {trauma.name_eng}"

    def check_state_if_contusion_past(self):
        now_date = datetime.datetime.now(Config.APP_TIMEZONE)
        naive_now_date = now_date.replace(tzinfo=None)


        if self.end < datetime.datetime.now().date():
            # TODO - CHECK IF GOOD LOGIC
            # I CHECK EVENT IS PAST AND USER HAS CONTUSION STATE
            self.state = "PAST"
            user_tmp = UserContusion.query.filter_by(id=self.id).first()
            user = User.query.filter_by(id=user_tmp.user_id).first()
            if user.state in "CONTUSION":
                user.state = "HEALTHY"
            self.save()



class BodyPart(db.Model, BaseModelMixin):
    __tablename__ = "body_parts"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_eng = db.Column(db.String(128))
    name_pl = db.Column(db.String(128, collation='utf8_unicode_ci'))

    def __init__(self, name_eng, name_pl):
        self.name_eng = name_eng
        self.name_pl = name_pl

    @staticmethod
    def get_body_part_lang_label(user):
        body_part_list = BodyPart.query.all()
        if user.language == "pl":
            body_part_label = [i.name_pl for i in body_part_list]
            return body_part_label
        if user.language == "en":
            body_part_label = [i.name_eng for i in body_part_list]
            return body_part_label



    @staticmethod
    def set_body_part(user, data):
        if user.language == "en":
            body_part = BodyPart.query.filter_by(name_eng=data).one()
        if user.language == "pl":
            body_part = BodyPart.query.filter_by(name_pl=data).one()

        return body_part.id

    @staticmethod
    def get_body_part_name_by_lang(user, contusion):
        body_part_qr = BodyPart.query.filter_by(id=contusion.body_part_id).first()
        if user.language == 'pl':
            return body_part_qr.name_pl
        if user.language == 'en':
            return body_part_qr.name_eng

class Tissue(db.Model, BaseModelMixin):
    __tablename__ = "tissues"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_eng = db.Column(db.String(128))
    name_pl = db.Column(db.String(128, collation='utf8_unicode_ci'))

    def __init__(self, name_eng, name_pl):
        self.name_eng = name_eng
        self.name_pl = name_pl

    @staticmethod
    def get_tissue_lang_label(user):
        tissue_list = Tissue.query.all()
        if user.language == "pl":
            tissue_label = [i.name_pl for i in tissue_list]
            return tissue_label
        if user.language == "en":
            tissue_label = [i.name_eng for i in tissue_list]
            return tissue_label



    @staticmethod
    def set_tissue_part(user, data):
        if user.language == "en":
            tissue = Tissue.query.filter_by(name_eng=data).one()
        if user.language == "pl":
            tissue = Tissue.query.filter_by(name_pl=data).one()

        return tissue.id

    @staticmethod
    def get_tissue_name_by_lang(user, contusion):
        tissue_qr = Tissue.query.filter_by(id=contusion.tissue_id).first()
        if user.language == 'pl':
            return tissue_qr.name_pl
        if user.language == 'en':
            return tissue_qr.name_eng

class Trauma(db.Model, BaseModelMixin):
    __tablename__ = "traumas"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_eng = db.Column(db.String(128))
    name_pl = db.Column(db.String(128, collation='utf8_unicode_ci'))

    def __init__(self, name_eng, name_pl):
        self.name_eng = name_eng
        self.name_pl = name_pl

    @staticmethod
    def get_trauma_lang_label(user):
        trauma_list = Tissue.query.all()
        if user.language == "pl":
            trauma_label = [i.name_pl for i in trauma_list]
            return trauma_label
        if user.language == "en":
            trauma_label = [i.name_eng for i in trauma_list]
            return trauma_label



    @staticmethod
    def set_trauma_part(user, data):
        if user.language == "en":
            trauma = Trauma.query.filter_by(name_eng=data).one()
        if user.language == "pl":
            trauma = Trauma.query.filter_by(name_pl=data).one()

        return trauma.id

    @staticmethod
    def get_tissue_name_by_lang(user, contusion):
        trauma_qr = Tissue.query.filter_by(id=contusion.trauma_id).first()
        if user.language == 'pl':
            return trauma_qr.name_pl
        if user.language == 'en':
            return trauma_qr.name_eng

class Event(db.Model, BaseModelMixin):

    __tablename__ = "events"

    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(128))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    details = db.Column(db.String(128))
    type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'))
    description = db.Column(db.String(1024))
    color = db.Column(db.String(128))
    has_kinase = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(100))


    def __init__(self, name, start, end, type_id, has_kinase=False, color=None, latitude=None, longitude=None, details=None, description=None, state="ACTIVE"):
        self.name = name
        self.start = start
        self.end = end
        self.color = color
        self.latitude = latitude
        self.longitude = longitude
        self.has_kinase = has_kinase
        self.type_id = type_id
        self.details = details
        self.description = description
        self.state = state


    def get_event(id):
        return Event.query.filter_by(id=id).first()




    def get_users_of_event(self):
        users = UserEvents.query.filter_by(event_id=self.id).all()
        return users


#    def get_players_of_event(self):
#        users = self.get_users_of_event()
#        return [players for players in users if User.query.filter_by(id == players.user_id, Role.name == "player").first()]

    def get_id_of_users_in_event(self):
        users = User.query.filter(User.events.any(id = self.id)).all()
        return users

    @staticmethod
    def get_events_without_motorics():
        events = Event.query.filter_by(state="PAST").all()

        return [event for event in events if len(event.get_motorics_of_event()) == 0]

    @staticmethod
    def get_events_without_wellness():
        events = Event.query.filter_by(state="PAST").all()

        return [event for event in events if len(event.get_wellness_of_event()) == 0]

    def get_motorics_of_event(self):
        return Motoric.query.filter_by(event_id=self.id).all()

    def get_wellness_of_event(self):
        return Wellness.query.filter_by(event_id=self.id).all()

    def get_rpe_of_event(self):
        return RPE.query.filter_by(event_id=self.id).all()

    def get_kinase_of_event(self):
        return Kinase.query.filter_by(event_id=self.id).all()

    @staticmethod
    def get_living_events():
        return Event.query.filter((Event.state == "ACTIVE") | (Event.state == "WELLNESS")).all()

    @staticmethod
    def check_if_is_not_in_past(end_date: str):
        # count the time before start of event

        date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - datetime.datetime.today()
        if date.seconds > 0:
            return False
        return True

    @staticmethod
    def check_if_today(start_date: str):
        # count the time before start of event
        date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

        # return True if is today
        return date.day == datetime.date.today().day


    def create_motorics_of_event(self):

        users = self.get_users_of_event()

        if self.type_id in [1, 2, 3, 4]:
            # send notification about survey to people subscribed to the event
            for i in users:
                player = User.query.filter_by(id=i.user_id).one()

                if "player" in player.show_role():

                    if player.state == "HEALTHY":
                        motoric_to_add = Motoric(event_id=self.id,
                                                 date=self.start, state="TO-COMPLETE")

                        player.motoric.append(motoric_to_add)
                        motoric_to_add.save()

                    else:

                        motoric_contusion = Motoric(event_id=self.id,
                                                    date=self.start, state="CONTUSION")

                        player.motoric.append(motoric_contusion)
                        motoric_contusion.save()

    def create_kinase_of_event(self):

        users = self.get_users_of_event()

        if self.has_kinase == True:
            for i in users:
                player = User.query.filter_by(id=i.user_id).one()

                if "player" in player.show_role():

                    if player.state == "HEALTHY":
                        kinase_to_add = Kinase(event_id=self.id,
                                                 date=self.start, state="TO-COMPLETE")

                        player.kinase.append(kinase_to_add)
                        kinase_to_add.save()

                    else:

                        kinase_contusion = Kinase(event_id=self.id,
                                                    date=self.start, state="CONTUSION")

                        player.kinase.append(kinase_contusion)
                        kinase_contusion.save()



    def send_motoric_notification_to_admins(self):

        self.create_motorics_of_event()


        admins = UserRoles.query.filter_by(role_id=1).all()
        link = '/{}/motoric-import'.format(self.id)
        for z in admins:
            n2 = Notification(name="Add Motoric Data {} - {}".format(self.end, self.name),name_pl="Dodaj dane motoryczne {} - {}".format(self.end, self.name), type="Motoric-import", details_pl= "Masz podsumowanie motoryczne do dodania.",  details="You have motoric data to add",
                                  link=link)
            user_admin = User.query.filter_by(id=z.user_id).first()
            user_admin.add_notification(n2)

            Notification.MOTORIC_PUSH(user_admin, link, self)



    def send_wellness_notification_to_users(self):
        # send wellness notification to users of event
        users = self.get_users_of_event()

        if self.type_id in [1,2,3,4]:
            # send notification about survey to people subscribed to the event
            for i in users:
                player = User.query.filter_by(id=i.user_id).one()

                if "player" in player.show_role():

                    if player.state == "HEALTHY":
                        wellness_to_complete = Wellness(event_id=self.id,
                                                        date=self.start, state="TO-COMPLETE")

                        player.wellness.append(wellness_to_complete)
                        wellness_to_complete.save()

                        link = '/{}/wellness-survey'.format(self.id)
                        n = Notification(name="Wellness {} - {}".format(self.end, self.name), name_pl="Wellness {} - {}".format(self.end, self.name), type="Wellness-survey", details_pl="Masz ankietę do wypełnienia!", details="You have a survey to complete!",
                                         link=link)



                        player.add_notification(n)

                        Notification.WELLNESS_PUSH(player, link, self)

                    else:

                        wellness_contusion = Wellness(event_id=self.id,
                                                        date=self.start, state="CONTUSION")

                        player.wellness.append(wellness_contusion)
                        wellness_contusion.save()







    def send_rpe_notification_to_users(self):
        # send RPE notification to users of event

        users = self.get_users_of_event()


        if self.type_id in [1, 2, 3, 4]:
            # send notification about survey to people subscribed to the event
            for i in users:
                player = User.query.filter_by(id=i.user_id).one()

                if "player" in player.show_role():

                    if player.state == "HEALTHY":
                        rpe_to_complete = RPE(event_id=self.id,
                                                        date=self.end, state="TO-COMPLETE")
                        rpe_to_complete.save()
                        player.rpe.append(rpe_to_complete)


                        link = '/{}/rpe-survey'.format(self.id)
                        n = Notification(name="RPE Borge {} - {}".format(self.end, self.name),name_pl="RPE Borge {} - {}".format(self.end, self.name), type="RPE-survey",
                                         details="You have a survey to complete!", details_pl="Masz ankietę do wypełnienia!",
                                         link=link)

                        player.add_notification(n)

                        #WEBPUSH

                        Notification.RPE_PUSH(player, link, self)


                    else:
                        rpe_contusion = RPE(event_id=self.id,
                                                      date=self.end, state="CONTUSION")

                        player.rpe.append(rpe_contusion)
                        rpe_contusion.save()

    def send_kinase_notification_to_admins(self):

        self.create_kinase_of_event()

        # send kinase notification to admins
        admins = UserRoles.query.filter_by(role_id=1).all()
        link = '/{}/kinase-import'.format(self.id)
        for z in admins:
            n2 = Notification(name="Add kinase Data {} - {}".format(self.end, self.name),name_pl="Dodaj dane kinazy {} - {}".format(self.end, self.name), type="Kinase-import",
                              details="You have Kinase data to add",details_pl="Masz podsumowanie kinazy do dodania.",
                              link=link)
            user_admin = User.query.filter_by(id=z.user_id).one()
            user_admin.add_notification(n2)
            Notification.KINASIS_PUSH(user_admin, link, self)


    def check_state_if_event_past(self):
        now_date = datetime.datetime.now(Config.APP_TIMEZONE)
        naive_now_date = now_date.replace(tzinfo=None)

        #If event past -> send notifications about RPE and MOTORIC DATA, set the training as KINASE for waiting

        if self.end < naive_now_date:
            # TODO - CHECK IF GOOD LOGIC
            # If event is Match (some type) wait for Motoric Data
            if self.type_id in [1,2,3,4]:
                self.state = "MOTORIC"

            # If is Medical put it as past
            else:
                self.state = "PAST"

            self.save()
            self.send_motoric_notification_to_admins()
            self.send_rpe_notification_to_users()


    def check_state_if_event_wellness(self):
        now_date = datetime.datetime.now(Config.APP_TIMEZONE)
        naive_now_date = now_date.replace(tzinfo=None)

        #If event past -> send notifications about RPE and MOTORIC DATA, set the training as KINASE for waiting

        if self.start.day ==  naive_now_date.day or self.start < naive_now_date:
            self.state = "WELLNESS"
            self.save()
            self.send_wellness_notification_to_users()

    def generate_past_surveys(self):
        pass



    @staticmethod
    def convert_to_date(date):
        #API METHOD to convert string into Date object form db
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


    def add_event_by_teams(self, by_teams):
        try:
            for team in by_teams:
                users = User.query.filter(User.teams.any(name=team)).all()
                teamEvent = Team.query.filter_by(name=team).first()
                teamEvent.events.append(self)
                for user in users:
                    user.events.append(self)
        except:
            print("some error")

    def add_event_by_user(self, by_users):
        try:
            for user in by_users:
                users_by_id=User.query.filter_by(id=user).first()
                users_by_id.events.append(self)
        except:
            print('error while adding')

    @staticmethod
    def get_events_past():
        return Event.query.filter((Event.state.like("PAST") | Event.state.like("WELLNESS") | Event.state.like("MOTORIC") | Event.state.like("KINASIS"))).all()


'''
class Files(db.Model, BaseModelMixin):
     
     __tablename__ = "files"

     id = db.Column(db.Integer, primary_key=True, unique=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
     uuid = db.Column(db.String(128))
     real_name = db.Column(db.String(128, collation='utf8_unicode_ci'))
     path = db.Column(db.String(128, collation='utf8_unicode_ci'))
     type = db.Column(db.String(128)) #IMPORT-FILE , PHOTO, AVATAR, DOC
     
'''




class UserRoles(db.Model):

    __tablename__ = "user_roles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))


class UserTeams(db.Model):

    __tablename__ = "user_teams"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))


class UserEvents(db.Model):

    __tablename__ = "user_events"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))


class Motoric(db.Model, BaseModelMixin):

    __tablename__ = "motoric"

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    date = db.Column(db.Date)

    total_distance = db.Column(db.Float(), default=0)
    sprint = db.Column(db.Float, default=0)

    total_player_load = db.Column(db.Float, default=0)
    hsr = db.Column(db.Float, default=0)

    acceleration = db.Column(db.Float, default=0)
    deceleration = db.Column(db.Float, default=0)
    field_time = db.Column(db.Integer, default=0)

    maximum_velocity = db.Column(db.Float, default=0)
    meterage_per_minute = db.Column(db.Float, default=0)
    max_vel_per_max = db.Column(db.Float, default=0)

    running = db.Column(db.Float, default=0)
    state = db.Column(db.Text, default="TO-COMPLETE")



    @staticmethod
    def get_user_motoric_of_event(user, event_id):

        list_of_motoric = [i for i in user.motoric if i.event_id == event_id]

        if list_of_motoric is None:
            return None
        return Motoric.query.filter_by(id=list_of_motoric [0].id).one()

    def __repr__(self):
        return "{}".format(self.__dict__)


'''    
    exertion_index = db.Column(db.Float)
    exertion_index_per_minute = db.Column(db.Float)

    total_distance = db.Column(db.Float)
    standing = db.Column(db.Float)
    walking = db.Column(db.Float)
    jogging = db.Column(db.Float)


    sprint = db.Column(db.Float)


    date = db.Column(db.Date())
'''




class UserBasicInfo(db.Model, BaseModelMixin):

    __tablename__ = "user_basic_info"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    shirt = db.Column(db.Integer)

    def __init__(self, shirt, height, weight, position_id, user_id):
        self.height = height
        self.weight = weight
        self.position_id = position_id
        self.shirt = shirt
        self.user_id = user_id



class Nationality(db.Model, BaseModelMixin):

    __tablename__ = "nationalities"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_eng = db.Column(db.String(128))
    name_pl = db.Column(db.String(128, collation='utf8_unicode_ci'))

    def __init__(self, name_eng, name_pl):
        self.name_eng = name_eng
        self.name_pl = name_pl

    @staticmethod
    def get_nationality_lang_label(user):
        nationalities_list = Nationality.query.all()
        if user.language == "pl":
            return [i.name_pl for i in nationalities_list]
        if user.language == "en":
            return [i.name_eng for i in nationalities_list]



    @staticmethod
    def set_nationality(user, data):
        if user.language == "en":
            nationality = Nationality.query.filter_by(name_eng=data).one()
        if user.language == "pl":
            nationality = Nationality.query.filter_by(name_pl=data).one()

        return nationality.id

    @staticmethod
    def get_nationality_name_by_lang(user):
        nationality_qr = Nationality.query.filter_by(id=user.nationality).first()

        if user.language == 'pl':
            return nationality_qr.name_pl
        if user.language == 'en':
            return nationality_qr.name_eng





class Position(db.Model, BaseModelMixin):
    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_eng = db.Column(db.String(128))
    name_pl = db.Column(db.String(128, collation='utf8_unicode_ci'))

    def __init__(self, name_eng, name_pl):
        self.name_eng = name_eng
        self.name_pl = name_pl

    @staticmethod
    def get_position_lang_label(user):
        position_list = Position.query.all()
        if user.language == "pl":
            position_label = [i.name_pl for i in position_list]
            return position_label
        if user.language == "en":
            position_label = [i.name_eng for i in position_list]
            return position_label



    @staticmethod
    def set_position(user, data):
        if user.language == "en":
            position = Position.query.filter_by(name_eng=data).one()
        if user.language == "pl":
            position = Position.query.filter_by(name_pl=data).one()

        return position.id

    @staticmethod
    def get_position_name_by_lang(user, user_info):
        position_qr = Position.query.filter_by(id=user_info.position_id).first()
        if user.language == 'pl':
            return position_qr.name_pl
        if user.language == 'en':
            return position_qr.name_eng


class Notification(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    name_pl = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(128))
    timestamp = db.Column(db.Float, index=True, default=time)
    details = db.Column(db.Text)
    details_pl = db.Column(db.Text)
    checked = db.Column(db.Boolean)
    link = db.Column(db.Text)

    @staticmethod
    def checked_notification_admins(link):

        notifications = Notification.query.filter_by(link=link).all()
        for notification in notifications:
            notification.checked = True
            notification.save()
        return notifications

    @staticmethod
    def send_web_push(subscription_information, message_body):
        from pywebpush import webpush

        return webpush(
            subscription_info=subscription_information,
            data=message_body,
            vapid_private_key=Config.WEBPUSH_VAPID_PRIVATE_KEY,
            vapid_claims=Config.VAPID_CLAIMS
        )

    @staticmethod
    def RPE_PUSH(player, link, event):

        subscribtions = Subscriber.query.filter_by(user_id=player.id).all()

        if subscribtions:
            from pywebpush import WebPushException
            for _sub in subscribtions:
                try:
                    if player.language == 'pl':
                        data = {'body' : "Masz ankietę RPE do wypełnienia! - {} {} {}".format(event.name, event.start, event.end), 'link' : link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)
                    else:
                        data = {'body': "You have a RPE survey to complete! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)
                except WebPushException as ex:
                    print(ex)

    @staticmethod
    def WELLNESS_PUSH(player, link, event):

        subscribtions = Subscriber.query.filter_by(user_id=player.id).all()

        if subscribtions:
            from pywebpush import WebPushException
            for _sub in subscribtions:
                try:
                    if player.language == 'pl':
                        data = {'body': "Masz ankietę Wellness do wypełnienia! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)
                    else:
                        data = {'body': "You have a Wellness survey to complete! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)
                except WebPushException as ex:
                    print(ex)

    @staticmethod
    def KINASIS_PUSH(admin, link, event):

        subscribtions = Subscriber.query.filter_by(user_id=admin.id).all()

        if subscribtions:
            from pywebpush import WebPushException
            for _sub in subscribtions:
                try:
                    if admin.language == 'pl':
                        data = {'body': "Masz dane Kinazy do wypełnienia! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)
                    else:
                        data = {'body': "You have a Kinase data to add! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json,data_js)
                except WebPushException as ex:
                    print(ex)

    @staticmethod
    def MOTORIC_PUSH(admin, link, event):

        subscribtions = Subscriber.query.filter_by(user_id=admin.id).all()

        if subscribtions:
            from pywebpush import WebPushException
            for _sub in subscribtions:
                try:
                    if admin.language == 'pl':
                        data = {'body': "Masz dane Motoryczne do wypełnienia! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)

                    else:
                        data = {'body': "You have Motoric data to add! - {} {} {}".format(event.name, event.start, event.end), 'link': link}
                        data_js = json.dumps(data)
                        Notification.send_web_push(_sub.subscription_info_json, data_js)

                except WebPushException as ex:
                    print(ex)


'''

    @staticmethod
    def send_wellness_notification(event):
        n = Notification(name="Wellness {}".format(self.end), type="Wellness", details="You have a survey to complete!",
                         link=link)

    @staticmethod
    def send_rpe_notification(event):
        n = Notification(name="Wellness {}".format(self.end), type="RPE", details="You have a survey to complete!",
                         link=link)

    @staticmethod
    def send_kinase_notification(event):
        n = Notification(name="Wellness {}".format(self.end), type="Kinase", details="You have a survey to complete!",
                         link=link)

'''




#types part
class EventType(db.Model, BaseModelMixin):

    __tablename__ = "event_types"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)



#SUERVEY PART

class Wellness(db.Model, BaseModelMixin):

    __tablename__ = "wellness"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    sleep_duration = db.Column(db.Integer, default=0)
    sleep_quality = db.Column(db.Integer, default=0)
    muscle_soreness = db.Column(db.Integer, default=0)
    energy = db.Column(db.Integer, default=0)
    mood = db.Column(db.Integer, default=0)
    stress = db.Column(db.Integer, default=0)
    fatigue = db.Column(db.Integer, default=0)
    mental_focus = db.Column(db.Integer, default=0)
    nutrional_amount = db.Column(db.Integer, default=0)
    nutrional_quality = db.Column(db.Integer, default=0)
    hydration = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text, default="")

    total_time = db.Column(db.Time)
    state = db.Column(db.Text, default="TO-COMPLETE")

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date = db.Column(db.Date)

    @staticmethod
    def get_user_welless_of_event(user, event_id):
        list_of_wellness = [i for i in user.wellness if i.event_id == event_id]
        if len(list_of_wellness) == 0:
            return None
        return Wellness.query.filter_by(id=list_of_wellness[0].id).one()



class RPE(db.Model, BaseModelMixin):
    __tablename__ = "rpe"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.Integer, default=0)

    total_time = db.Column(db.Time, default=0)

    state = db.Column(db.Text, default="TO-COMPLETE")
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date = db.Column(db.Date)

    @staticmethod
    def get_user_rpe_of_event(user, event_id):
        list_of_rpe = [i for i in user.rpe if i.event_id == event_id]
        if list_of_rpe is None:
            return None
        return RPE.query.filter_by(id=list_of_rpe[0].id).one()

class Kinase(db.Model, BaseModelMixin):
    __tablename__ = "kinase"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.Float, default=0)

    state = db.Column(db.Text, default="TO-COMPLETE")
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date = db.Column(db.Date)

    @staticmethod
    def get_user_kinase_of_event(user, event_id):
        list_of_kinase = [i for i in user.rpe if i.event_id == event_id]
        if list_of_kinase is None:
            return None
        return RPE.query.filter_by(id=list_of_kinase[0].id).one()


#WEBPUSH
class Subscriber(db.Model, BaseModelMixin):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer(), primary_key=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    subscription_info = db.Column(db.Text())
    is_active = db.Column(db.Boolean(), default=True)

    @property
    def subscription_info_json(self):
        return json.loads(self.subscription_info)

    @subscription_info_json.setter
    def subscription_info_json(self, value):
        self.subscription_info = json.dumps(value)



class UsersSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    active = fields.String()
    teams = fields.Nested('TeamsSchema', many=True)
    roles = fields.Nested('RolesSchema', many=True)
    state = fields.String()


# Schemas for API calls



class EventsSchema(ma.Schema):
    model = Event
    class Meta:
        fields = ('id', 'name', 'start', 'end', 'type_id', 'latitude', 'longitude', 'details', 'description', 'color', 'has_kinase')

'''
class EventsSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    start = fields.Date()
    end = fields.Date()
    type_id = fields.NestedSchema('EventsTypeSchema')
    latitude = fields.Float()
    longitude = fields.Float()
    details = fields.String()
    description = fields.String()
    color = fields.String()
'''



class MotoricSchema(ma.Schema):
    model = Motoric
    class Meta:
        fields = (
            'id', 'event_id', 'field_time', 'exertion_index', 'exertion_index_per_minute', 'total_player_load',
            'total_distance', 'standing', 'walking', 'jogging', 'running', 'hsr', 'sprint',
         'meterage_per_minute', 'acceleration', 'deceleration', 'date', 'state')

class WellnessSchema(ma.Schema):
    model = Motoric
    class Meta:
        fields = (
            'id', 'event_id', 'sleep_quality', 'muscle_soreness', 'mood', 'fatigue',
            'energy', 'state', 'date')





class RPESchema(ma.Schema) :
    class Meta :
        fields=('id' , 'value', 'event_id', 'total_time' , 'state', 'date')


class KinaseSchema(ma.Schema) :
    class Meta :
        fields=('id' , 'value', 'event_id', 'value' , 'state', 'date')



class MessageSchema(ma.Schema) :
    class Meta :
        fields=('id' , 'sender_id', 'recipient_id', 'body' , 'timestamp', 'date')





'''
class MotoricSchema(ma.Schema):
    id = fields.Integer()
    event_id = fields.Integer()
    field_time = fields.Integer()
    exertion_index = fields.Float()
    exertion_index_per_minute = fields.Float()
    total_player_load = fields.Float()
    total_distance = fields.Float()
    standing = fields.Float()
    walking = fields.Float()
    jogging = fields.Float()
    running = fields.Float()
    hsr = fields.Float()
    sprint = fields.Float()

    meterage_per_minute = fields.Float()
    acceleration = fields.Float()
    deceleration = fields.Float()
    date = fields.Date()
    events = fields.Nested('EventsSchema', many=True)
'''

class NotificationSchema(ma.Schema):
    class Meta:
        fields = ('name','name_pl', 'details' , 'details_pl', 'link', 'checked', 'timestamp' )

'''
class EventsSchema(ma.Schema):
    class Meta:
        id=fields.Integer(dump_only=True)
        name=fields.String()
        start=fields.String()
        hour=fields.String()
        type=fields.String()
        latitude=fields.String()
        longitude= fields.String()
        address=fields.String()
        participants=fields.Nested('UsersSchema' , many=True)

'''

class TeamsSchema(ma.Schema) :
    class Meta :
        fields=('id' , 'name')

class RolesSchema(ma.Schema) :
    class Meta :
        fields=('id' , 'name')

user_schema=UsersSchema()
users_schema=UsersSchema(many=True)
event_schema=EventsSchema()
events_schema=EventsSchema(many=True)
team_schema=TeamsSchema()
teams_schema=TeamsSchema(many=True)
role_schema=RolesSchema()
roles_schema=RolesSchema(many=True)

notification_schema=NotificationSchema(many=True)

motoric_schema = MotoricSchema()
motorics_schema = MotoricSchema(many=True)

wellness_schema = WellnessSchema()
wellness_schemas = WellnessSchema(many=True)

kinase_schema = KinaseSchema()
kinases_schema = KinaseSchema(many=True)

rpe_schema = RPESchema()
rpes_schema = RPESchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)













class Survey(db.Model, BaseModelMixin):

    __tablename__ = "surveys"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

class Question(db.Model, BaseModelMixin):

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    text = db.Column(db.Text)
    type = db.Column(db.Text)



class PredefinedAnswer(db.Model, BaseModelMixin):

    __tablename__ = "predefined_answers"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    value = db.Column(db.Text)
    placeholder = db.Column(db.Text)

class UserAnswers(db.Model, BaseModelMixin):

    __tablename__ = "user_answers"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    value = db.Column(db.Text)


class QuestionSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'text', 'type'
        )

class MotoricSchema(ma.Schema):
    class Meta:
        fields = ('total_distance', 'sprint', 'total_player_load', 'hsr', 'acceleration', 'deceleration', 'field_time', 'maximum_velocity', 'meterage_per_minute', 'max_vel_per_max', 'running')


class SuerveySchema(ma.Schema):
     class Meta:
        fields = (
            'id', 'name', 'desciption'
        )

class PredefinedAnswerSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'value', 'placeholder'
        )


class UserAnswerSchema(ma.Schema):
    class Meta:
        fields = (
           'user_id' ,'question_id', 'value'
        )

'''
# Schemas for API calls
'''
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'active')




question_schema=QuestionSchema(many = True)
predefined_answer_schema = PredefinedAnswerSchema(many = True)
user_answer_schema = UserAnswerSchema(many = True)


# create USERs and send to databse if they are not created
db.create_all()

@login.user_loader
def load_user(id) :
    user=User.query.get(id)
    return user
