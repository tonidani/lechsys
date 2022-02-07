import datetime
import json

from flask import Blueprint, request, jsonify

from flask_login import login_required, current_user
from app import db
from app import Config

from app.models.models import (
    PredefinedAnswer, Question, Survey, User, Team, Event, Role, UserAnswers, team_schema,
    teams_schema, user_schema, users_schema, event_schema, events_schema, UserEvents, question_schema,
    predefined_answer_schema, user_answer_schema
, Notification, motoric_schema, UserMotoric, Motoric, motorics_schema, wellness_schema, rpe_schema, kinase_schema,
    rpes_schema, wellness_schemas, kinases_schema, messages_schema)

from app.decorators import token_admin_required, token_player_blocked, blocked_access
from flask_jwt_extended import jwt_required
from flask_babel import _
from flask_cors import cross_origin

api_bp = Blueprint('api_bp', __name__)



# API

@api_bp.post('/users')
@jwt_required()
@token_admin_required()
@cross_origin()
def add_user():
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email=request.json['email']
    active = request.json['active']
    role = request.json['role']
    team = request.json['team']

    new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, active=active)
    if new_user.validate_email(email) and new_user.validate_username(username):
        new_user._set_password('lol')
        role_in_db = Role.query.filter(Role.name == role).first()
        new_user.roles.append(role_in_db)
        team_in_db=Team.query.filter(Team.name == team).first()
        new_user.teams.append(team_in_db)


        new_user.save()

        return user_schema.jsonify(new_user)
    return jsonify({"error" : "email or username in the db"})

@api_bp.get('/users/<int:id>')
@jwt_required()
@token_player_blocked()
@cross_origin()
def get_user_id(id):

    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"error" : "No user with id = {}!".format(id)})

    return user_schema.jsonify(user)



@api_bp.get('/users')
@jwt_required()
@token_player_blocked()
@cross_origin()
def get_user():
    data = User.query.all()
    if data is None:
        return jsonify({"error" : "No users!"})
    return users_schema.jsonify(data)


@api_bp.get('/users/q')
@jwt_required()
#token_player_blocked()
@cross_origin()
@login_required
@blocked_access('player')
def get_user_by_query():
    if request.args.get('role', type=str):
        role = request.args.get('role', type=str)
        data = User.query.filter(User.roles.any(name=role)).all()

    elif request.args.get('name', type=str):
        name = request.args.get('name', type=str)
        data = User.query.filter(User.first_name.like('%'+name+'%') | (User.last_name.like('%'+name+'%'))).all()

        return users_schema.jsonify([players for players in data if current_user.show_team() in players.show_team()])



    elif request.args.get('id', type=int) :
        id = request.args.get('id' , type=int)
        data = User.query.filter_by(id=id).all()

    elif request.args.get('team', type=str):
        team = request.args.get('team', type=str)
        data = User.query.filter(User.teams.any(name=team)).all()

    else:
        return jsonify({'error': 'Bad request!'})
    return users_schema.jsonify(data)



@api_bp.post('/events')
@jwt_required()
@token_admin_required()
@cross_origin()
@blocked_access('player', 'staff')
def add_event():
    name = request.json['name']
    start = request.json['start']
    end = request.json['end']
    type_id = request.json['type']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    by_teams = request.json['by_team']
    by_users = request.json['by_users']
    details = request.json['details']
    color = request.json['color']
    kinase = request.json['kinase']

    if (by_users is None or not len(by_users)) and (by_teams is None or not len(by_teams)):
        return jsonify({'error': _('You can not add event without participants!')})

    if (type_id is None):
        return jsonify({'error': _('You can not add event without type!')})
    
    if (type_id != 1 ) and (type_id != 2 ) and (type_id != 3) and (type_id != 4) and (type_id != 5):
         return jsonify({'error': _('Type of event do not match with "Match, Medical or Training"')})

    if Event.check_if_is_not_in_past(end):
        return jsonify({'error': _('You can not add event ending in the past!"')})

    #TODO if end date or astar date in past -> ustaw automatycznie na PAST

    new_event = Event(name=name, start=Event.convert_to_date(start), end=Event.convert_to_date(end) , type_id=int(type_id) , latitude=latitude , longitude=longitude , details=details, color=color, has_kinase=kinase)


    if by_teams is not None:
        new_event.add_event_by_teams(by_teams)

    if by_users is not None:
        new_event.add_event_by_user(by_users)

    new_event.save()


    return event_schema.jsonify(new_event)

@api_bp.patch('/events/<int:id>')
@jwt_required()
@token_admin_required()
@cross_origin()
@blocked_access('player', 'staff')
def edit_event(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({"error": "No events!"})

    elif (event.state in "PAST") or (event.state in "WELLNESS") or (event.state in "MOTORIC") or (event.state in "KINASIS"):
        return jsonify({"error": _("You can not edit a past event")})

    else:
        name = request.json['name']
        start = request.json['start']
        end = request.json['end']
        type_id = request.json['type']
        by_teams = request.json['by_team']
        by_users = request.json['by_users']
        details = request.json['details']
        color = request.json['color']
        kinase = request.json['kinase']

        event.name, event.start, event.end, event.type_id, event.by_teams , event.by_users, event.details, event.color, event.kinase = name, start, end, type_id, by_teams, by_users, details, color, kinase


        pass


@api_bp.delete('/events/<int:id>')
#@jwt_required()
#@token_admin_required()
#@cross_origin()
#@blocked_access('player', 'staff')
def delete_event(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({"error": _("No event with this id!")})

    elif (event.state in "PAST") or (event.state in "WELLNESS") or (event.state in "MOTORIC") or (
            event.state in "KINASIS"):
        return jsonify({"error": _("You can not delete a past event")})

    else:
        event.delete()
        return jsonify({"ok": _("Event deleted!")})





@api_bp.get('/events')
@jwt_required()
@token_admin_required()
@cross_origin()
def get_event():

    events = Event.query.all()

    if events is None:
        return jsonify({"error" : "No events!"})

    return events_schema.jsonify(events)


@api_bp.get('/my_events')
@jwt_required()
@blocked_access('admin')
def my_events():

    events = current_user.events

    if events is None:
        return jsonify({"error" : "No events!"})

    return events_schema.jsonify(events)


#NOWE API
@api_bp.get('/users/<int:id>/events')
@login_required
@blocked_access('player')
def get_user_all_events(id):

    user = User.query.filter_by(id=id).first()
    if user is not None:

       events = sorted(user.user_inactive_events(), key=lambda x: x.end, reverse=True)
    else:
        return jsonify({"error" : "No user with this id!"})
    return events_schema.jsonify(events)



@api_bp.get('/users/<int:id>/events/type/<int:event_type>')
@login_required
@blocked_access('player')
def get_user_all_events_by_type(id, event_type):

    user = User.query.filter_by(id=id).first()
    if user is not None:
        user_events_by_type = [i for i in user.user_inactive_events() if i.type_id == event_type]
        events = sorted(user_events_by_type, key=lambda x: x.end, reverse=True)
    else:
        return jsonify({"error" : "No user with this id!"})

    return events_schema.jsonify(events)


'''
@api_bp.get('/users/<int:id>/events/<int:event_id>')
@jwt_required()
def get_user_events_by_event_id(id, event_id):

    user = User.query.filter_by(id=id).first()
    events = user.events.filter(id==event_id).first()

    return events_schema.jsonify(events)
'''




@api_bp.get('/events/q')
@login_required
@blocked_access('player')
def get_event_by_query():
    if request.args.get('date' , type=str):
        date=request.args.get('date' , type=str)
        data=Event.query.filter_by(date=date).all()

    elif request.args.get('name' , type=str):
        name=request.args.get('name' , type=str)
        data=Event.query.filter(Event.name.like('%' + name +'%')).all()

    elif request.args.get('hour' , type=str) :
        hour=request.args.get('hour' , type=str)
        data=Event.query.filter_by(hour=hour).all()

    elif request.args.get('type' , type=str) :
        type=request.args.get('type' , type=str)
        data=Event.query.filter_by(type=type).all()

    elif request.args.get('user_id' , type=int) :
        user_id=request.args.get('user_id' , type=int)
        query = db.session.query(Event).join(UserEvents).join(User).filter(Event.id == UserEvents.event_id, User.id ==
                                                                   UserEvents.user_id).filter(User.id == user_id)
        data = query.all()
    else:
        return jsonify({"error" : "No data!! Bad endpoint?"})

    return events_schema.jsonify(data)

@api_bp.get('/events/<int:id>')
@login_required
def get_event_id(id):

    events = Event.query.filter_by(id=id).first()

    if events is None:
        return jsonify({"error" : "No event with id = {}!".format(id)})

    return event_schema.jsonify(events)


@api_bp.get('/teams/<int:id>')
@jwt_required()
@cross_origin()
def get_team_by(id):

    team = Team.query.filter_by(id=id).first()

    if team is None:
        return jsonify({"error" : "No team with id = {}!".format(id)})
    return team_schema.jsonify(team)



@api_bp.get('/teams')
@jwt_required()
@cross_origin()
def get_teams():

    teams = Team.query.all()
    if teams is None:
        return jsonify({"error" : "No teams!"})

    return teams_schema.jsonify(teams)

'''
@api_bp.get('/surveys/<int:id>')
@jwt_required()
def get_surveys(id):

    surveys = Survey.query.filter_by(id=id).first()
    if surveys is None:
        return jsonify({"error" : "No survey!"})

    return jsonify({"id": surveys.id , "name" : surveys.name, "description" : surveys.description})



@api_bp.get('/surveys/<int:id>/questions')
@jwt_required()
@cross_origin()
def get_questions(id):

    questions = Question.query.filter_by(survey_id=id).all()

    return question_schema.jsonify(questions)


@api_bp.get('/questions/<int:id>/predefined-answers')
@jwt_required()
@cross_origin()
def get_predefined_answers(id):

    pre_answer = PredefinedAnswer.query.filter_by(question_id=id).all()

    return predefined_answer_schema.jsonify(pre_answer)


@api_bp.get('/answers/user/<int:id>')
#@jwt_required()
#@cross_origin()
def get_user_answers_by_id(id):

    user_answer = UserAnswers.query.filter_by(user_id=id).all()

    return user_answer_schema.jsonify(user_answer)

@api_bp.get('/questions/predefined-answers')
@jwt_required()
@cross_origin()
def get_predefined_answers_all():



    pre_answer = PredefinedAnswer.query.all()

    return predefined_answer_schema.jsonify(pre_answer)


'''
#MOTORIC
@api_bp.get('users/<int:user_id>/motoric')
@login_required
@blocked_access('player')
def get_user_motoric_all(user_id):


    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_motoric = user.motoric

    return motorics_schema.jsonify(user_motoric)



@api_bp.get('users/<int:user_id>/motoric/<int:event_id>')
@login_required
@blocked_access('player')
def get_user_motoric(user_id, event_id):

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_motoric = user.motoric

    for i in user_motoric:
        if i.event_id == event_id:
            return motoric_schema.jsonify(i)




    return motoric_schema.jsonify(user_motoric)


@api_bp.get('events/<int:event_id>/motoric')
@login_required
@blocked_access('player')
def get_event_motoric_all(event_id):
    event = Event.get_event(event_id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    return motorics_schema.jsonify(event.get_motorics_of_event())


@api_bp.get('events/<int:event_id>/participants')
def get_event_partcipants(event_id):
    event = Event.get_event(event_id)
    if event is None:
        return jsonify({'error': "no event with this id!"})

    users = event.get_id_of_users_in_event()
    return users_schema.jsonify(users)



#WELLNESS
@api_bp.get('users/<int:user_id>/wellness')
@login_required
@blocked_access('player')
def get_user_wellness_all(user_id):


    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_wellness = user.wellness

    return wellness_schemas.jsonify(user_wellness)


@api_bp.get('users/<int:user_id>/wellness/<int:event_id>')
@login_required
@blocked_access('player')
def get_user_wellness(user_id, event_id):

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_wellness = user.wellness

    for i in user_wellness:
        if i.event_id == event_id:
            return wellness_schema.jsonify(i)




    return wellness_schema.jsonify(user_wellness)


@api_bp.get('events/<int:event_id>/wellness')
@login_required
@blocked_access('player')
def get_event_wellness_all(event_id):
    event = Event.get_event(event_id)
    if event is None:
        return jsonify({'error': "no event with this id!"})

    return wellness_schemas.jsonify(event.get_wellness_of_event())


#RPE
@api_bp.get('users/<int:user_id>/rpe')
@login_required
@blocked_access('player')
def get_user_rpe_all(user_id):


    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_rpe = user.rpe

    return rpes_schema.jsonify(user_rpe)


@api_bp.get('users/<int:user_id>/rpe/<int:event_id>')
@login_required
@blocked_access('player')
def get_user_rpe(user_id, event_id):

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_rpe = user.rpe

    for i in user_rpe:
        if i.event_id == event_id:
            return rpe_schema.jsonify(i)




    return rpe_schema.jsonify(user_rpe)


@api_bp.get('events/<int:event_id>/rpe')
@login_required
@blocked_access('player')
def get_event_rpe_all(event_id):
    event = Event.get_event(event_id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    return rpes_schema.jsonify(event.get_rpe_of_event())


#KINASE
@api_bp.get('users/<int:user_id>/kinase')
@login_required
@blocked_access('player')
def get_user_kinase_all(user_id):


    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_kinase = user.kinase

    return kinases_schema.jsonify(user_kinase)


@api_bp.get('users/<int:user_id>/kinase/<int:event_id>')
@login_required
@blocked_access('player')
def get_user_kinase(user_id, event_id):

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': "no user with this id!"})

    user_kinase = user.kinase

    for i in user_kinase:
        if i.event_id == event_id:
            return kinase_schema.jsonify(i)




    return kinase_schema.jsonify(user_kinase)

@api_bp.get('events/<int:event_id>/kinase')
@login_required
@blocked_access('player')
def get_event_kinase_all(event_id):
    event = Event.get_event(event_id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    return kinases_schema.jsonify(event.get_kinase_of_event())




@api_bp.get('/messages/<int:user_id>')
@login_required
def messages_with_this_person(user_id):
    messages = Messages.query.filter(Mesa)
    if messages is not None:
        messages_with_this_person = [i for i in messages if i.sender_id == user_id]

        return messages_schema.jsonify(messages)






@api_bp.get('/events/<int:id>/wellness-result')
@login_required
@blocked_access('staff', 'player')
def surveys_wellness_control(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    participants = event.get_id_of_users_in_event()

    wellness_of_event = []
    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.wellness) != 0:
            user_wellness = user.wellness

            for wellness in user_wellness:
                if wellness.event_id == event.id:
                    wellness_of_event.append({'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'state': wellness.state})

    return jsonify(wellness_of_event)

@api_bp.get('/events/<int:id>/rpe-result')
@login_required
@blocked_access('staff', 'player')
def surveys_rpe_control(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    participants = event.get_id_of_users_in_event()

    rpe_of_event = []
    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.wellness) != 0:
            user_rpe = user.rpe

            for rpe in user_rpe:
                if rpe.event_id == event.id:
                    rpe_of_event.append({'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'state': rpe.state})

    return jsonify(rpe_of_event)


@api_bp.get('/events/<int:id>/motoric-result')
@login_required
@blocked_access('staff', 'player')
def surveys_motoric_control(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    participants = event.get_id_of_users_in_event()

    motoric_of_event = []
    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.motoric) != 0:
            user_motoric = user.motoric

            for motoric in user_motoric:
                if motoric.event_id == event.id:
                    motoric_of_event.append({'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'state': motoric.state})

    return jsonify(motoric_of_event)



@api_bp.get('/events/<int:id>/kinase-result')
@login_required
@blocked_access('staff', 'player')
def surveys_kinase_control(id):
    event = Event.get_event(id)
    if event is None:
        return jsonify({'error': "no event with this id!"})
    participants = event.get_id_of_users_in_event()

    kinase_of_event = []
    for user in participants:
        user = User.query.filter_by(id=user.id).first()
        if user is not None and len(user.kinase) != 0:
            user_kinase = user.kinase

            for kinase in user_kinase:
                if kinase.event_id == event.id:
                    kinase_of_event.append({'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'state': kinase.state})

    return jsonify(kinase_of_event)



@api_bp.get('/wellness/<int:event_id>')
@login_required
@blocked_access('staff', 'admin')
def get_player_wellness(event_id):

    user = current_user
    user_wellness = user.wellness

    for i in user_wellness:
        if i.event_id == event_id:
            return wellness_schema.jsonify(i)




    return wellness_schema.jsonify(user_wellness)


@api_bp.get('/rpe/<int:event_id>')
@login_required
@blocked_access('staff', 'admin')
def get_player_rpe(event_id):

    user = current_user
    user_rpe = user.rpe

    for i in user_rpe:
        if i.event_id == event_id:
            return rpe_schema.jsonify(i)




    return rpes_schema.jsonify(user_rpe)





'''
@api_bp.get('user/<int:user_id>/motoric_resume/')
def get_event_motoric_all(user_id):



    events = Event.query.filter_by(event_.id)


    return motorics_schema.jsonify(event.get_motorics_of_event())
'''


'''
@api_bp.post('send_message')
@jwt_required()
def send_message():
    recipient = request.json['recipient']
    message = request.json['message']
    to_who = User.query.filter_by(username=recipient)

    msg = Message(author=current_user, recipient=to_who, body=message)

    msg.save()

    return jsonify({""})
'''


#WEBPUSH

import datetime
from app.models.models import Subscriber




@api_bp.post('/subscribe')
@login_required
def subscribe():
    subscription_info = request.json.get('subscription_info')
    #is_active = request.json.get('is_active')

    # we assume subscription_info shall be the same
    item = Subscriber.query.filter(Subscriber.subscription_info == subscription_info).first()

    if not item:
        item = Subscriber()
        item.user_id = current_user.id
        item.created = datetime.datetime.utcnow()
        item.subscription_info = subscription_info

    #item.is_active = is_active
    item.modified = datetime.datetime.utcnow()
    item.save()


    return jsonify({ "id": item.id }), 200


@api_bp.get('/unsubscribe')
@login_required
def unsubscribe():
    item = Subscriber.query.filter_by(user_id=current_user.id).all()

    if not item:
        return jsonify({"error": 'This user is not subscribed'}), 200
    else:
        for i in item:
            i.delete()


        return jsonify({ "ok": 'subscription deleted' }), 200



@api_bp.route('/notify')
def notify():
    from pywebpush import WebPushException

    items = Subscriber.query.filter(Subscriber.is_active == True).all()
    count = 0
    data = {"body" : "testujemydsdsds", "link" :"jakis link"}

    data_js = json.dumps(data)

    for _item in items:
        try:
            Notification.send_web_push(_item.subscription_info_json, data_js)

            count += 1
        except WebPushException as ex:
            print(ex)


    return "{} notification(s) sent".format(count)

