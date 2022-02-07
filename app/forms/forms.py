import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField, RadioField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField, IntegerField, DecimalRangeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, Optional
from app.models.models import User, Role, Team, Event, Nationality, Position, Motoric
from wtforms.widgets import html5
from flask_babel import lazy_gettext as _l
import pandas as pd
def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(_l("File size must be less than %d MB"  %  max_size_in_mb))
    
    return file_length_check


MAX_AVATAR = 1024*1024

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sign In'))


class AddUserForm(FlaskForm):

    first_name = StringField(_l("First name"),  validators=[DataRequired()])
    last_name = StringField(_l("Last name"),  validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label='name',blank_text=(_l('Select a role')),
                            allow_blank=False, get_pk=lambda x: x.id)
    team = QuerySelectField(query_factory=lambda: Team.query.all(), get_label='name',blank_text=(_l('Select a team')),
                            allow_blank=False, get_pk=lambda x: x.id)

    nationality = SelectField(_l('Select nationality'), choices=[("1", "Class 1"), ("2", "Class 2")],
                              validators=[DataRequired()])

    birth_date = DateField(_l("Birth date", format='%d/%m/%Y'), validators=[DataRequired()])



    height = IntegerField(_l("Height (in cm)"), widget=html5.NumberInput(min = 100, max = 250), validators=[Optional(), NumberRange(min=100, max=250, message=_l("Please, select a number between 100 cm and 250 cm")) ])
    weight = IntegerField(_l("Weight (in kg)"), widget=html5.NumberInput(min = 40, max = 500), validators=[Optional(), NumberRange(min=40, max=300, message=_l("Please, select a number between 40 kg and 200 kg"))])
    #position = QuerySelectField(query_factory=lambda: Position.query.all(), get_label=db_language_check(), blank_text=(_l('Select position')),
                           # allow_blank=False, get_pk=lambda x: x.id)

    position = SelectField(_l('Select position'), choices= [("1", "Class 1"), ("2","Class 2")])

    #nationality = QuerySelectField(query_factory=lambda: Nationality.query.all(), get_label=label_lang, blank_text=(_l('Select nationality')),
                           # allow_blank=False, get_pk=lambda x: x.id)
    shirt = IntegerField(_l('Shirt number'), widget=html5.NumberInput(min = 0, max = 99), validators=[Optional(), NumberRange(min=0, max=99, message=_l("Please, select a shirt number between 0 and 100"))])

    submit = SubmitField(_l('Add Basic Info!'))




    submit = SubmitField(_l('Add User'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))


    def validate_first_name(self, first_name):
        if not first_name.data.isalpha():
            raise ValidationError(_l('Name should contain ony letters.'))

    def validate_last_name(self, last_name):
        if not last_name.data.isalpha():
            raise ValidationError(_l('Last name should contain ony letters.'))

    def validate_birth_date(self, birth_date):
        diff = datetime.date.today() - birth_date.data
        if diff.days / 365.25 > 100:
            raise ValidationError(_l('Please use a different date because you can not live more than 100 years!'))
        if datetime.date.today() < birth_date.data:
            raise ValidationError(_l('Select a date in the past'))
        if diff.days / 365.25 < 3:
            raise ValidationError(_l('Minimum 3 years'))






class EditBasicInfoAdminUserForm(FlaskForm):
    height = IntegerField(_l("Height (in cm)"))
    weight = StringField(_l("Weight (in kg)"))
    position = QuerySelectField(query_factory=lambda: Position.query.all(), get_label='position',blank_text=(_l('Select position')),
                            allow_blank=False, get_pk=lambda x: x.id)
    birth_date = DateField(_l("Birth date", format='%d/%m/%Y'))
    nationality = QuerySelectField(query_factory=lambda: Nationality.query.all(), get_label='nationality',blank_text=(_l('Select nationality')),
                            allow_blank=False, get_pk=lambda x: x.id)
    shirt = IntegerField(_l('Shirt number'))

    submit_basic_info = SubmitField(_l('Add Basic Info!'))

    def validate_birth_date(self, birth_date):
        if datetime.date - birth_date > 100:
            raise ValidationError(_l('Please use a different date because you can not live more than 100 years!'))
        if datetime.date < birth_date:
            raise ValidationError(_l('Select a date in the past'))
        if datetime.date - birth_date < 3:
            raise ValidationError(_l('Minimum 3 years'))



class ImportPlayersForm(FlaskForm):

    players_file = FileField(_l('Add players file'), validators=[FileAllowed(['xlsx']), FileRequired()] )
    team = QuerySelectField(query_factory=lambda: Team.query.all(), get_label='name',blank_text=(_l('Select a team')),
                            allow_blank=False, get_pk=lambda x: x.id)

    submit = SubmitField(_l('Import players'))

class AddTeamForm(FlaskForm):
    name = StringField(_l('Team name'), validators=[DataRequired(), Length(min=6, max=25)])
    submit=SubmitField(_l('Add Team to the system'))


class ImportMotoricResumeForm(FlaskForm):

    motoric_players_resume_file = FileField(_l('Import motoric resume'), validators=[FileAllowed(['xlsx', 'csv'])])
    event = QuerySelectField(
        query_factory=lambda: Event.query.filter(Event.type =="training").all(), get_label='name', blank_text=(
            _l('Select a Event')),
        allow_blank=False, get_pk=lambda x: x.id)

    submit = SubmitField('Import Motoric')


class SetUserPasswordForm(FlaskForm):
    avatar = FileField(_l('Image'), validators=[FileRequired(), FileAllowed(['jpg', 'png']), FileSizeLimit(max_size_in_mb=10)])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Set user and password'))


    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))

    def validate_password(self, password):
        if len(password.data) < 10:
            raise ValidationError(_l('You password should contain at least 10 characters!'))

    def validate_avatar(self, avatar):
        if len(avatar.data.read()) > 1000:
            raise ValidationError(_l("File size must be less than 1 MB"))



class EditAdminUserForm(FlaskForm):
    username = StringField(_l('Username') , validators=[DataRequired()])
    first_name = StringField(_l("First name"), validators=[DataRequired()])
    last_name = StringField(_l("Last name"), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired()])
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label='name',blank_text=(_l('Select a role')),
                            allow_blank=False, get_pk=lambda x: x.id)
    team = QuerySelectField(query_factory=lambda: Team.query.all(), get_label='name',blank_text=(_l('Select a team')),
                            allow_blank=True, get_pk=lambda x: x.id)
    active = BooleanField(_l('Active'))

    submit = SubmitField(_l('Save User'))

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(_l('No match for account with this email!'))

class RequestResetPasswordUserForm(FlaskForm):
    email=StringField(_l('Email') , validators=[DataRequired(), Email()])
    submit=SubmitField(_l('Request password'))

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(_l('No match for account with this email!'))

class ResetPasswordUserForm(FlaskForm):
    password=PasswordField(_l('Password') , validators=[DataRequired()])
    password2=PasswordField(
        _l('Repeat Password') , validators=[DataRequired() , EqualTo('password')])
    submit=SubmitField(_l('Set new password!'))

    def validate_password(self, password):
        if len(password.data) < 10:
            raise ValidationError(_l('You password should contain at least 10 characters!'))

class ChangeAvatarUserForm(FlaskForm):
    avatar = FileField(_l('Image'), validators=[FileRequired(), FileAllowed(['jpg', 'png']), FileSizeLimit(max_size_in_mb=10)])
    submitAvatar=SubmitField(_l('Set new avatar!'))



class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=1024)])
    submit = SubmitField(_l('Submit'))


class WellnessForm(FlaskForm):
    # TODO zmniejszyć ankietę, zmienić w modelu też oraz dodać state do nich aby się nie generowały przy kontuzjach

    '''
    sleep_duration = DecimalRangeField(_l('Sleep duration'), validators=[DataRequired()])



    sleep_duration = RadioField(_l('Sleep duration'), choices=[('1', _l('Less than 4hrs.')),
                                                              ('2', _l('Less than 5hrs.')),
                                                              ('3', _l('Less than 6hrs.')),
                                                              ('4', _l('Less than 7hrs.')),
                                                              ('5', _l('8hrs. or more'))], validators=[DataRequired()])
   '''
    sleep_quality = RadioField(_l('Sleep quality'), choices=[('1', _l('Insomnia')),
                                                              ('2', _l('Restless sleep')),
                                                              ('3', _l('Difficulty falling asleep')),
                                                              ('4', _l('Good')),
                                                              ('5', _l('Very restful'))], validators=[DataRequired()])

    muscle_soreness = RadioField(_l('Muscle soreness'), choices=[('1', _l('Very sore')),
                                                             ('2', _l('Increase in soreness / tightness')),
                                                             ('3', _l('Normal')),
                                                             ('4', _l('Feeling good')),
                                                             ('5', _l('Feeling great'))], validators=[DataRequired()])
    '''
    energy = RadioField(_l('Energy level'), choices=[('1', _l('Very low')),
                                                             ('2', _l('Low')),
                                                             ('3', _l('Moderate')),
                                                             ('4', _l('High')),
                                                             ('5', _l('Very high'))], validators=[DataRequired()])
   '''
    mood = RadioField(_l('Mood'), choices=[('1', _l('Highly irritable / annoyed / down')),
                                                     ('2', _l('Snappy with team-mates, family and friends')),
                                                     ('3', _l('Less interested in others / activities')),
                                                     ('4', _l('Generally good mood')),
                                                     ('5', _l('Very positive mood'))], validators=[DataRequired()])

    stress = RadioField(_l('Stress'), choices=[('1', _l('Highly stressed')),
                                                     ('2', _l('Feeling stressed')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Relaxed')),
                                                     ('5', _l('Very Relaxed'))], validators=[DataRequired()])

    fatigue = RadioField(_l('Fatigue'), choices=[('1', _l('Always tired')),
                                                     ('2', _l('More tired than normal')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Fresh')),
                                                     ('5', _l('Very fresh'))], validators=[DataRequired()])

    mental_focus = RadioField(_l('Mental focus'), choices=[('1', _l('Distracted')),
                                                     ('2', _l('More distracted than normal')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Focused')),
                                                     ('5', _l('Very focused'))], validators=[DataRequired()])
    '''
    nutrional_amount = RadioField(_l('Nutrional amount'), choices=[('1', _l('Always hungry')),
                                                     ('2', _l('More hungry than normal')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Satisfied')),
                                                     ('5', _l('Very satisfied'))], validators=[DataRequired()])

    nutrional_quality = RadioField(_l('Nutrional quality'), choices=[('1', _l('Poor')),
                                                     ('2', _l('Poorer than normal')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Satisfied')),
                                                     ('5', _l('High'))], validators=[DataRequired()])

    hydration = RadioField(_l('Hydration'), choices=[('1', _l('Always thirsty')),
                                                     ('2', _l('More thirsty than normal')),
                                                     ('3', _l('Normal')),
                                                     ('4', _l('Hydrated')),
                                                     ('5', _l('Well hydrated'))], validators=[DataRequired()])

   '''   '''
    comment = TextAreaField(_l('Additional comment'))

    '''
    submit = SubmitField(_l('Save'))


class AddMotoricDataForm(FlaskForm):
    motoric_data = FileField(_l('Motoric file'), validators=[FileRequired(), FileAllowed(['csv']), FileSizeLimit(max_size_in_mb=15)])
    submit=SubmitField(_l('Import data'))


class AddMotoricDataManually(FlaskForm):
    total_distance = FloatField(_l("total_distance"))
    sprint = FloatField(_l("Sprint"))

    total_player_load = FloatField(_l("total_player_load"))
    hsr = FloatField(_l("hsr"))

    acceleration = FloatField(_l("acceleration"))
    deceleration = FloatField(_l("deceleration"))
    field_time = IntegerField(_l("field_time"))

    maximum_velocity = FloatField(_l("maximum_velocity"))
    meterage_per_minute =FloatField(_l("meterage_per_minute"))
    max_vel_per_max = FloatField(_l("max_vel_per_max"))

    running = FloatField(_l("running"))

    submitManually = SubmitField(_l('Submit'))


class EditMotoricDataForm(FlaskForm):
    total_distance = FloatField(_l("Total distance (m)"), widget=html5.NumberInput(min = 0, max = 20000, step=0.001), validators=[DataRequired()])
    sprint = FloatField(_l("Sprint (m)"),widget=html5.NumberInput(min = 0, max = 10000, step=0.001), validators=[DataRequired()])

    total_player_load = FloatField(_l("Total player load"),widget=html5.NumberInput(min = 0, max = 10000, step=0.001), validators=[DataRequired()])
    hsr = FloatField(_l("HSR"),widget=html5.NumberInput(min = 0, max = 10000, step=0.001), validators=[DataRequired()])

    acceleration = FloatField(_l("Acceleration"),widget=html5.NumberInput(min = 0, max = 10000, step=0.001), validators=[DataRequired()])
    deceleration = FloatField(_l("Deceleration"),widget=html5.NumberInput(min = 0, max = 10000, step=0.001), validators=[DataRequired()])
    field_time = FloatField(_l("Field time"),widget=html5.NumberInput(min = 0, max = 200), validators=[DataRequired()])

    maximum_velocity = FloatField(_l("Max. velocity"),widget=html5.NumberInput(min = 0, max = 100, step=0.001), validators=[DataRequired()])
    meterage_per_minute =FloatField(_l("M. per minute"),widget=html5.NumberInput(min = 0, max = 100, step=0.001), validators=[DataRequired()])
    max_vel_per_max = FloatField(_l("Max. vel. per. max"),widget=html5.NumberInput(min = 0, max = 100, step=0.001), validators=[DataRequired()])

    running = FloatField(_l("Running"),widget=html5.NumberInput(min = 0, max = 100000, step=0.001), validators=[DataRequired()])

    submitMotoric = SubmitField(_l('Edit motoric data'))

    def validate_total_distance(self, total_distance):
        if total_distance.data < 0 or total_distance.data > 20000:
            raise ValidationError(_l('The value of total distance cannot be less than 0 or greater than 20000'))

    def validate_sprint(self, sprint):
        if sprint.data < 0 or sprint.data > 10000:
            raise ValidationError(_l('The value of sprint cannot be less than 0 or greater than 10000'))

    def validate_total_player_load(self, total_player_load):
        if total_player_load.data < 0 or total_player_load.data > 10000:
            raise ValidationError(_l('The value of total player load cannot be less than 0 or greater than 10000'))

    def validate_hsr(self, hsr):
        if hsr.data < 0 or hsr.data > 10000:
            raise ValidationError(_l('The value of hsr cannot be less than 0 or greater than 10000'))

    def validate_acceleration(self, acceleration):
        if acceleration.data < 0 or acceleration.data > 10000:
            raise ValidationError(_l('The value of acceleration cannot be less than 0 or greater than 10000'))

    def validate_deceleration(self, deceleration):
        if deceleration.data < 0 or deceleration.data > 10000:
            raise ValidationError(_l('The value of deceleration cannot be less than 0 or greater than 10000'))

    def validate_field_time(self, field_time):
        if field_time.data < 0 or field_time.data > 200:
            raise ValidationError(_l('The value of deceleration cannot be less than 0 or greater than 200 minutes'))

    def validate_maximum_velocity(self, maximum_velocity):
        if maximum_velocity.data < 0 or maximum_velocity.data > 100:
            raise ValidationError(_l('The value of maximum valocity cannot be less than 0 or greater than 100'))

    def validate_meterage_per_minute(self, meterage_per_minute):
        if meterage_per_minute.data < 0 or meterage_per_minute.data > 100:
            raise ValidationError(_l('The value of meterage per minute cannot be less than 0 or greater than 100'))

    def validate_max_vel_per_max(self, max_vel_per_max):
        if max_vel_per_max.data < 0 or max_vel_per_max.data > 100:
            raise ValidationError(_l('The value of maximum velocity per maximum cannot be less than 0 or greater than 100'))

    def validate_running(self, running):
        if running.data < 0 or running.data > 100000:
            raise ValidationError(
                _l('The value of running cannot be less than 0 or greater than 100000'))


class EditKinaseDataForm(FlaskForm):
    value = FloatField(_l("Kinase"), widget=html5.NumberInput(min = 0, max = 100, step=0.001), validators=[DataRequired()])
    submitKinase=SubmitField(_l('Edit kinase'))

    def validate_value(self, value):
        if value.data < 0 or value.data > 100:
            raise ValidationError(_l('The value of kinase cannot be less than 0 or greater than 100'))



class RPEForm(FlaskForm):
    training_note = RadioField(_l('Rate of preceived exertion'), choices=[('1', _l('Very light activity')),
                                                               ('2', _l('Light activity')),
                                                               ('3', _l('Light activity')),
                                                               ('4', _l('Moderate activity')),
                                                               ('5', _l('Moderate')),
                                                             ('6', _l('Moderate')),
                                                             ('7', _l('Vigorous activiy')),
                                                             ('8', _l('Vigorous')),
                                                             ('9', _l('Very hard activity')),
                                                             ('10', _l('Max effort activity'))
                                                             ], validators=[DataRequired()])
    submit=SubmitField(_l('Give RPE answer'))





class AddContusionForm(FlaskForm):

    body_part = RadioField(_l('Select injuried partq'), choices=[('1', _l('Head')),
                                                               ('2', _l('Left Shoulder')),
                                                               ('3', _l('Right shoulder')),
                                                               ('4', _l('Left arm')),
                                                               ('5', _l('Right arm')),
                                                             ('6', _l('Left elbow')),
                                                             ('7', _l('Right elbow')),
                                                             ('8', _l('Left forearm')),
                                                             ('9', _l('Right forearm')),
                                                             ('10', _l('Left wrist')),
                                                            ('11', _l('Left hip')),
                                                            ('12', _l('Right hip')),
                                                            ('13', _l('Right wrist')),
                                                            ('14', _l('Left hand')),
                                                            ('15', _l('Right hand')),
                                                             ('16', _l('Left thigh')),
                                                             ('17', _l('Right thigh')),
                                                             ('18', _l('Left knee')),
                                                             ('19', _l('Right knee')),
                                                             ('20', _l('Left Tibia')),
                                                            ('21', _l('Right Tibia')),
                                                            ('22', _l('Left ankle')),
                                                            ('23', _l('Right ankle')),
                                                            ('24', _l('Left foot')),
                                                            ('25', _l('Right foot'))], validators=[DataRequired()])

    tissue = SelectField(_l('Tissue'), choices=[("1", _l("Bone")), ("2", _l("Tendon")), ("3", _l("Muscle")), ("4", _l("Joint / Articulation"))],
                              validators=[DataRequired()])

    trauma = SelectField(_l('Trauma'), choices=[("1", _l("Contusion")), ("2", _l("Wound")), ("3", _l("Fracture")),
                                                ("4", _l("Sprain")), ("5", _l("Dislocation"))],
                         validators=[DataRequired()])


    start = DateField(_l("start of injury", format='%d/%m/%Y'), validators=[DataRequired()])
    end = DateField(_l("End of injury (prediction)", format='%d/%m/%Y'), validators=[DataRequired()])
    details = TextAreaField(_l('Add some details'), validators=[DataRequired(), Length(min=0, max=1024)])
    submit= SubmitField(_l('Add Injury to player'))

    def validate_end(self, end):
        if (self.start.data > end.data):
            raise ValidationError(_l('You can not End a Injury before it Start!'))

    def validate_start(self, start):
        if (start.data > datetime.date.today()):
            raise ValidationError(_l('You can not Start a Injury in the future!'))


class EditContusionForm(FlaskForm):

    edit_body_part = SelectField(_l('Select injuried part'), choices=[('1', _l('Head')),
                                                               ('2', _l('Left Shoulder')),
                                                               ('3', _l('Right shoulder')),
                                                               ('4', _l('Left arm')),
                                                               ('5', _l('Right arm')),
                                                             ('6', _l('Left elbow')),
                                                             ('7', _l('Right elbow')),
                                                             ('8', _l('Left forearm')),
                                                             ('9', _l('Right forearm')),
                                                             ('10', _l('Left wrist')),
                                                            ('11', _l('Left hip')),
                                                            ('12', _l('Right hip')),
                                                            ('13', _l('Right wrist')),
                                                            ('14', _l('Left hand')),
                                                            ('15', _l('Right hand')),
                                                             ('16', _l('Left thigh')),
                                                             ('17', _l('Right thigh')),
                                                             ('18', _l('Left knee')),
                                                             ('19', _l('Right knee')),
                                                             ('20', _l('Left Tibia')),
                                                            ('21', _l('Right Tibia')),
                                                            ('22', _l('Left ankle')),
                                                            ('23', _l('Right ankle')),
                                                            ('24', _l('Left foot')),
                                                            ('25', _l('Right foot'))], validators=[DataRequired()])

    edit_tissue = SelectField(_l('Tissue'), choices=[("1", _l("Bone")), ("2", _l("Tendon")), ("3", _l("Muscle")), ("4", _l("Joint / Articulation"))],
                              validators=[DataRequired()])

    edit_trauma = SelectField(_l('Trauma'), choices=[("1", _l("Contusion")), ("2", _l("Wound")), ("3", _l("Fracture")),
                                                ("4", _l("Sprain")), ("5", _l("Dislocation"))],
                         validators=[DataRequired()])


    edit_start = DateField(_l("start of injury", format='%d/%m/%Y'), validators=[DataRequired()])
    edit_end = DateField(_l("End of injury (prediction)", format='%d/%m/%Y'), validators=[DataRequired()])
    edit_details = TextAreaField(_l('Add some details'), validators=[DataRequired(), Length(min=0, max=1024)])
    edit_submit= SubmitField(_l('Edit Injury to player'))

    def validate_edit_end(self, edit_end):
        if (self.edit_start.data > edit_end.data):
            raise ValidationError(_l('You can not End a Injury before it Start!'))

    def validate_edit_start(self, edit_start):
        if (edit_start.data > datetime.date.today()):
            raise ValidationError(_l('You can not Start a Injury in the future!'))

