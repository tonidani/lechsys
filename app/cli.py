from app import app
import click
from flask.cli import with_appcontext
from app.models.models import *
from datetime import datetime


import numpy as np
import pandas as pd


now = datetime.now()
@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('../messages.pot')

@click.command(name="create_basic_users")
@with_appcontext
def create_basic_users():
    if not Role.query.filter(Role.name == "player").first() :
        player_role=Role(id=2 , name="player")
        db.session.add(player_role)
        db.session.commit()
        print("Player role added!")

    if not Role.query.filter(Role.name == "admin").first() :
        admin_role=Role(id=1 , name="admin")
        db.session.add(admin_role)
        db.session.commit()
        print("admin Role added!")

    if not Role.query.filter(Role.name == "staff").first() :
        staff_role=Role(id=3 , name="staff")
        db.session.add(staff_role)
        db.session.commit()
        print("staff role added!")

    if not Team.query.filter(Team.name == "KKS LECH 1").first() :
        kks1=Team(id=1 , name="KKS LECH 1")
        db.session.add(kks1)
        db.session.commit()
        print("team KKS1 lech added!")

    if not Team.query.filter(Team.name == "KKS LECH 2").first() :
        kks2=Team(id=2 , name="KKS LECH 2")
        db.session.add(kks2)
        db.session.commit()
        print("team KKS2 lech added!")


    if not User.query.filter(User.username == "player").first() :
        player_user=User(
            username="player" ,
            first_name="playerName" ,
            last_name="playerLastName" ,
            email="player@mail_utilities.com" ,
            active=1,
            birth_date="1999-11-03"
        )
        player_user._set_password('lol')
        player_user.create_user_data_folder()
        player_user.nationality = 5
        player_user.roles.append(player_role)
        player_user.teams.append(kks1)

        basic_user_info1 = UserBasicInfo(height=180, weight=90, shirt=10,
                                        position_id=4, user_id=1)
        player_user.save()
        basic_user_info1.save()
        print("Player1 added with team ksk1")


    if not User.query.filter(User.username == "player2").first() :
        player_user2=User(
            username="player2" ,
            first_name="playerName" ,
            last_name="playerLastName" ,
            email="player2@mail_utilities.com" ,
            active=1,
            birth_date="1999-05-03"
        )
        player_user2._set_password('lol')
        player_user2.create_user_data_folder()
        player_user2.roles.append(player_role)
        player_user2.nationality = 140
        player_user2.teams.append(kks2)
        basic_user_info2 = UserBasicInfo(height= 150, weight=87, shirt=4,
                                        position_id=1, user_id=2)



        player_user2.save()
        basic_user_info2.save()
        print("Player2 added with team ksk2")

    if not User.query.filter(User.username == "staff").first():
        staff_user=User(
            username="staff" ,
            first_name="staffName" ,
            last_name="staffLastName" ,
            email="staff@mail_utilities.com" ,
            active=1,
            birth_date="1950-05-02"
        )
        staff_user._set_password('lol')
        staff_user.create_user_data_folder()
        staff_user.roles.append(staff_role)
        staff_user.teams.append(kks1)
        staff_user.nationality = 123
        staff_user.save()
        print("Staff user added !")

    if not User.query.filter(User.username == "admin").first() :
        admin_user=User(
            username="admin" ,
            first_name="adminName" ,
            last_name="adminLastName" ,
            email="admin@mail_utilities.com" ,
            active=1,
            birth_date="1988-05-03"
        )
        admin_user._set_password('lol')
        admin_user.create_user_data_folder()
        admin_user.roles.append(admin_role)
        admin_user.nationality = 122
        admin_user.save()
        print("admin added !")


    # create Roles and send to databse if they are not created

@click.command(name="create_basic_survey")
@with_appcontext
def create_basic_survey():
    if not Survey.query.filter(Survey.id == 1).first() :
        survey_1=Survey(id=1 , name="testowa ankieta" , description="opis asdasda")
        survey_1.save()
        print("survey_1 added !")
    if not Question.query.filter(Question.id == 1).first() :
        question_1=Question(id=1 , survey_id=1 , text="pytanie 1" , type_id="input")
        question_1.save()
        print("question_1 added !")
    if not PredefinedAnswer.query.filter(PredefinedAnswer.id == 1).first() :
        pre_ans=PredefinedAnswer(id=1 , question_id=1 , value=None , placeholder="Dodaj odp do inputa")
        pre_ans.save()
        print("pre_ans added !")
    if not UserAnswers.query.filter(UserAnswers.id == 1).first() :
        user_answ_1=UserAnswers(id=1 , user_id=1 , question_id=1 , value="odpowiedz do question 1")
        user_answ_1.save()
        print("user_answ_1 added !")

@click.command(name="create_nationalities")
@with_appcontext
def create_nationalities():
    nationalities_tuple = [('Andorra', 'Andora'), ('United Arab Emirates', 'Zjednoczone Emiraty Arabskie'), ('Afghanistan', 'Afganistan'), ('Antigua & Barbuda', 'Antigua i Barbuda'), ('Anguilla', 'Anguilla'), ('Albania', 'Albania'), ('Armenia', 'Armenia'), ('Netherlands Antilles', 'Antyle Holenderskie'), ('Angola', 'Angola'), ('Antarctica', 'Antarktyda'), ('Argentina', 'Argentyna'), ('American Samoa', 'Samoa Amerykańskie'), ('Austria', 'Austria'), ('Australia', 'Australia'), ('Aruba', 'Aruba'), ('Azerbaijan', 'Azerbejdżan'), ('Bosnia and Herzegovina', 'Bośnia i Hercegowina'), ('Barbados', 'Barbados'), ('Bangladesh', 'Bangladesz'), ('Belgium', 'Belgia'), ('Burkina Faso', 'Burkina Faso'), ('Bulgaria', 'Bułgaria'), ('Bahrain', 'Bahrajn'), ('Burundi', 'Burundi'), ('Benin', 'Benin'), ('Bermuda', 'Bermudy'), ('Brunei Darussalam', 'Brunei Darussalam'), ('Bolivia', 'Boliwia'), ('Brazil', 'Brazylia'), ('Bahama', 'Bahama'), ('Bhutan', 'Bhutan'), ('Burma (no longer exists)', 'Birma (już nie istnieje)'), ('Bouvet Island', 'Wyspa Bouveta'), ('Botswana', 'Botswana'), ('Belarus', 'Białoruś'), ('Belize', 'Belize'), ('Canada', 'Kanada'), ('Cocos (Keeling) Islands', 'Wyspy Kokosowe (Keelinga)'), ('Central African Republic', 'Republika Środkowoafrykańska'), ('Congo', 'Kongo'), ('Switzerland', 'Szwajcaria'), ("Côte D'ivoire (Ivory Coast)", 'Wybrzeże Kości Słoniowej (Ivory Coast)'), ('Cook Iislands', 'Wyspy Cooka'), ('Chile', 'Chile'), ('Cameroon', 'Kamerun'), ('China', 'Chiny'), ('Colombia', 'Kolumbia'), ('Costa Rica', 'Kostaryka'), ('Czechoslovakia (no longer exists)', 'Czechosłowacja (już nie istnieje)'), ('Cuba', 'Kuba'), ('Cape Verde', 'Wyspy Zielonego Przylądka'), ('Christmas Island', 'Wyspa Bożego Narodzenia'), ('Cyprus', 'Cypr'), ('Czech Republic', 'Republika Czeska'), ('German Democratic Republic (no longer exists)', 'Niemiecka Republika Demokratyczna (już nie istnieje)'), ('Germany', 'Niemcy'), ('Djibouti', 'Dżibuti'), ('Denmark', 'Dania'), ('Dominica', 'Dominika'), ('Dominican Republic', 'Republika Dominikańska'), ('Algeria', 'Algieria'), ('Ecuador', 'Ekwador'), ('Estonia', 'Estonia'), ('Egypt', 'Egipt'), ('Western Sahara', 'Sahara Zachodnia'), ('Eritrea', 'Erytrea'), ('Spain', 'Hiszpania'), ('Ethiopia', 'Etiopia'), ('Finland', 'Finlandia'), ('Fiji', 'Fidżi'), ('Falkland Islands (Malvinas)', 'Falklandy (Malwiny)'), ('Micronesia', 'Mikronezja'), ('Faroe Islands', 'Wyspy Owcze'), ('France', 'Francja'), ('France, Metropolitan', 'Francja, metropolia'), ('Gabon', 'Gabon'), ('United Kingdom (Great Britain)', 'Zjednoczone Królestwo (Wielka Brytania)'), ('Grenada', 'Grenada'), ('Georgia', 'Gruzja'), ('French Guiana', 'Gujana Francuska'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greenland', 'Grenlandia'), ('Gambia', 'Gambia'), ('Guinea', 'Gwinea'), ('Guadeloupe', 'Gwadelupa'), ('Equatorial Guinea', 'Gwinea Równikowa'), ('Greece', 'Grecja'), ('South Georgia and the South Sandwich Islands', 'Południowa Georgia i Południowe Wyspy Sandwich'), ('Guatemala', 'Gwatemala'), ('Guam', 'Guam'), ('Guinea-Bissau', 'Gwinea Bissau'), ('Guyana', 'Gujana'), ('Hong Kong', 'Hongkong'), ('Heard & McDonald Islands', 'Wyspy Heard i McDonald'), ('Honduras', 'Honduras'), ('Croatia', 'Chorwacja'), ('Haiti', 'Haiti'), ('Hungary', 'Węgry'), ('Indonesia', 'Indonezja'), ('Ireland', 'Irlandia'), ('Israel', 'Izrael'), ('India', 'Indie'), ('British Indian Ocean Territory', 'Brytyjskie Terytorium Oceanu Indyjskiego'), ('Iraq', 'Irak'), ('Islamic Republic of Iran', 'Islamska Republika Iranu'), ('Iceland', 'Islandia'), ('Italy', 'Włochy'), ('Jamaica', 'Jamajka'), ('Jordan', 'Jordania'), ('Japan', 'Japonia'), ('Kenya', 'Kenia'), ('Kyrgyzstan', 'Kirgistan'), ('Cambodia', 'Kambodża'), ('Kiribati', 'Kiribati'), ('Comoros', 'Komory'), ('St. Kitts and Nevis', 'St. Kitts i Nevis'), ("Korea, Democratic People's Republic of", 'Koreańska Republika Ludowo-Demokratyczna'), ('Korea, Republic of', 'Korea, Republika Korei'), ('Kuwait', 'Kuwejt'), ('Cayman Islands', 'Kajmany'), ('Kazakhstan', 'Kazachstan'), ("Lao People's Democratic Republic", 'Laotańska Republika Ludowo-Demokratyczna'), ('Lebanon', 'Liban'), ('Saint Lucia', 'Saint Lucia'), ('Liechtenstein', 'Liechtenstein'), ('Sri Lanka', 'Sri Lanka'), ('Liberia', 'Liberia'), ('Lesotho', 'Lesotho'), ('Lithuania', 'Litwa'), ('Luxembourg', 'Luksemburg'), ('Latvia', 'Łotwa'), ('Libyan Arab Jamahiriya', 'Libijska Arabska Dżamahirija'), ('Morocco', 'Maroko'), ('Monaco', 'Monako'), ('Moldova, Republic of', 'Mołdawia, Republika Mołdowy'), ('Madagascar', 'Madagaskaru'), ('Marshall Islands', 'Wyspy Marshalla'), ('Mali', 'Mali'), ('Mongolia', 'Mongolia'), ('Myanmar', 'Myanmar'), ('Macau', 'Makau'), ('Northern Mariana Islands', 'Mariany Północne'), ('Martinique', 'Martynika'), ('Mauritania', 'Mauretania'), ('Monserrat', 'Monserrat'), ('Malta', 'Malta'), ('Mauritius', 'Mauritius'), ('Maldives', 'Malediwy'), ('Malawi', 'Malawi'), ('Mexico', 'Meksyk'), ('Malaysia', 'Malezja'), ('Mozambique', 'Mozambik'), ('Namibia', 'Namibia'), ('New Caledonia', 'Nowa Kaledonia'), ('Niger', 'Niger'), ('Norfolk Island', 'Wyspa Norfolk'), ('Nigeria', 'Nigeria'), ('Nicaragua', 'Nikaragua'), ('Netherlands', 'Niderlandy'), ('Norway', 'Norwegia'), ('Nepal', 'Nepal'), ('Nauru', 'Nauru'), ('Neutral Zone (no longer exists)', 'Strefa Neutralna (już nie istnieje)'), ('Niue', 'Niue'), ('New Zealand', 'Nowa Zelandia'), ('Oman', 'Oman'), ('Panama', 'Panama'), ('Peru', 'Peru'), ('French Polynesia', 'Polinezja Francuska'), ('Papua New Guinea', 'Papua-Nowa Gwinea'), ('Philippines', 'Filipiny'), ('Pakistan', 'Pakistan'), ('Poland', 'Polska'), ('St. Pierre & Miquelon', 'St. Pierre i Miquelon'), ('Pitcairn', 'Pitcairn'), ('Puerto Rico', 'Puerto Rico'), ('Portugal', 'Portugalia'), ('Palau', 'Palau'), ('Paraguay', 'Paragwaj'), ('Qatar', 'Katar'), ('Réunion', 'Reunion'), ('Romania', 'Rumunia'), ('Russian Federation', 'Federacja Rosyjska'), ('Rwanda', 'Rwanda'), ('Saudi Arabia', 'Arabia Saudyjska'), ('Solomon Islands', 'Wyspy Salomona'), ('Seychelles', 'Seszele'), ('Sudan', 'Sudan'), ('Sweden', 'Szwecja'), ('Singapore', 'Singapur'), ('St. Helena', 'Święta Helena'), ('Slovenia', 'Słowenia'), ('Svalbard & Jan Mayen Islands', 'Svalbard i Wyspy Jan Mayen'), ('Slovakia', 'Słowacja'), ('Sierra Leone', 'Sierra Leone'), ('San Marino', 'San Marino'), ('Senegal', 'Senegal'), ('Somalia', 'Somalia'), ('Suriname', 'Surinam'), ('Sao Tome & Principe', 'Wyspy Świętego Tomasza i Książęca (Sao Tome & Principe)'), ('Union of Soviet Socialist Republics (no longer exists)', 'Związek Socjalistycznych Republik Radzieckich (już nie istnieje)'), ('El Salvador', 'Salwador'), ('Syrian Arab Republic', 'Syryjska Republika Arabska'), ('Swaziland', 'Suazi'), ('Turks & Caicos Islands', 'Wyspy Turks i Caicos'), ('Chad', 'Czad'), ('French Southern Territories', 'Francuskie Terytoria Południowe'), ('Togo', 'Togo'), ('Thailand', 'Tajlandia'), ('Tajikistan', 'Tadżykistan'), ('Tokelau', 'Tokelau'), ('Turkmenistan', 'Turkmenistan'), ('Tunisia', 'Tunezja'), ('Tonga', 'Tonga'), ('East Timor', 'Timor Wschodni'), ('Turkey', 'Turcja'), ('Trinidad & Tobago', 'Trynidad i Tobago'), ('Tuvalu', 'Tuvalu'), ('Taiwan, Province of China', 'Tajwan, Prowincja Chin'), ('Tanzania, United Republic of', 'Tanzania, Zjednoczona Republika'), ('Ukraine', 'Ukraina'), ('Uganda', 'Uganda'), ('United States Minor Outlying Islands', 'Mniejsze Wyspy Przybrzeżne Stanów Zjednoczonych'), ('United States of America', 'Stany Zjednoczone Ameryki'), ('Uruguay', 'Urugwaj'), ('Uzbekistan', 'Uzbekistan'), ('Vatican City State (Holy See)', 'Państwo Watykańskie (Stolica Apostolska)'), ('St. Vincent & the Grenadines', 'St. Vincent i Grenadyny'), ('Venezuela', 'Wenezuela'), ('British Virgin Islands', 'Brytyjskie Wyspy Dziewicze'), ('United States Virgin Islands', 'Wyspy Dziewicze Stanów Zjednoczonych'), ('Viet Nam', 'Wietnam'), ('Vanuatu', 'Vanuatu'), ('Wallis & Futuna Islands', 'Wyspy Wallis i Futuna'), ('Samoa', 'Samoa'), ('Democratic Yemen (no longer exists)', 'Demokratyczny Jemen (już nie istnieje)'), ('Yemen', 'Jemen'), ('Mayotte', 'Majotta'), ('Yugoslavia', 'Jugosławia'), ('South Africa', 'Republika Południowej Afryki'), ('Zambia', 'Zambia'), ('Zaire', 'Zair'), ('Zimbabwe', 'Zimbabwe'), ('Unknown or unspecified country', 'Kraj nieznany lub nieokreślony')]

    for i in nationalities_tuple:
        nationalities_to_db = Nationality(i[0], i[1])
        nationalities_to_db.save()
        print("{} i {} added!".format(i[0], i[1]))

@click.command(name="create_medic_contusion")
@with_appcontext
def create_medic_contusion():
    body_parts_list = [('Head', 'Głowa'),
                           ('Left Shoulder', 'Lewy bark'),
                           ('Right shoulder', 'Prawy bark'),
                           ('Left arm', 'Lewe ramie'),
                            ('Right arm', 'Prawe ramie'),
                       ('Left elbow', 'Lewy łokieć'),
                       ('Right elbow', 'Prawy łokieć'),
                       ('Left forearm', 'Lewe przedramie'),
                       ('Right forearm', 'Prawe przedramie'),
                       ('Left wrist', 'Lewy nadgarstek'),
                       ('Left hip', 'Lewe biodro'),
                       ('Right hip', 'Prawe biodro'),
                       ('Right wrist', 'Prawy nadgarstek'),
                       ('Left hand', 'Lewa ręka'),
                       ('Right hand', 'Prawa ręka'),
                       ('Left thigh', 'Lewe udo'),
                       ('Right thigh', 'Prawe udo'),
                       ('Left knee', 'Lewe kolano'),
                       ('Right knee', 'Prawe kolano'),
                       ('Left Tibia', 'Lewy piszczel'),
                       ('Right Tibia', 'Prawy piszczel'),
                       ('Left ankle', 'Lewa kostka'),
                       ('Right ankle', 'Prawa kostka'),
                       ('Left foot', 'Lewa noga'),
                       ('Right foot', 'Prawa noga')]

    tissues_list = [('Bone', 'Kość'),
                    ('Tendon', 'Ścięgno'),
                    ('Muscle', 'Mięsień'),
                    ('Joint / Articulation', 'Wiązanie / Artykulacja')]

    traumas_list = [("Contusion", 'Stłuczenie'), ("Wound", 'Rana'), ("Fracture", "Złamanie"),
                                                ("Sprain", 'Skręcenie'), ("Dislocation" , 'Zwichnięcie')]


    for i in body_parts_list:
        body_parts_to_db = BodyPart(i[0], i[1])
        body_parts_to_db.save()
        print("{} i {} added!".format(i[0], i[1]))

    for i in tissues_list:
        tissues_list_to_db = Tissue(i[0], i[1])
        tissues_list_to_db.save()
        print("{} i {} added!".format(i[0], i[1]))

    for i in traumas_list:
        traumas_list_to_db = Trauma(i[0], i[1])
        traumas_list_to_db.save()
        print("{} i {} added!".format(i[0], i[1]))


@click.command(name="create_positions")
@with_appcontext
def create_positions():
    positions_list = [('Goalkeeper', 'Bramkarz'),
                           ('Defender', 'Obrońca'),
                           ('Midfielder', 'Pomocnik'),
                           ('Striker', 'Napastnik')]

    for i in positions_list:
        positions_to_db = Position(i[0], i[1])
        positions_to_db.save()
        print("{} i {} added!".format(i[0], i[1]))


@click.command(name="create_events")
@with_appcontext
def create_events():
    "Add some events and type"
    decision = input("do you want to create event types? (y/n): ")
    if decision == "y":
        event_type1 = EventType(id = 1, name="Match league")
        event_type1.save()

        event_type2 = EventType(id = 2, name="Match Cup")
        event_type2.save()

        event_type3 = EventType(id = 3, name="Match international")
        event_type3.save()

        event_type4 = EventType(id = 4, name="Training")
        event_type4.save()

        event_type5 = EventType(id = 5, name="Medical")
        event_type5.save()


    new_event1 = Event(name="Event 1", details="Bułgarska 17", latitude=52.400, longitude=16.888,
                       start=Event.convert_to_date("2021-11-01 10:48:10"), end=Event.convert_to_date("2021-11-01 10:48:10"), type_id=1, description="Match Lechia", color="blue")


    new_event2 = Event(name="Event 2", details="Jasielska 14", latitude=52.444, longitude=16.896,
                       start=Event.convert_to_date("2021-11-05 10:48:10"), end=Event.convert_to_date("2021-11-06 3:48:10"), type_id=5, description="Medical Overview 1", color="blue")

    new_event3 = Event(name="Event 3", details="Bułgarska 17", latitude=52.400, longitude=16.888,
                       start=Event.convert_to_date("2021-11-07 10:48:10"), end=Event.convert_to_date("2021-11-07 5:00:10"), type_id=4, description="Training 1 kks 1", color="blue")

    new_event4 = Event(name="Event 4", details="Łanzienkowska 3", latitude=52.629, longitude=19.274,
                       start=Event.convert_to_date("2021-11-08 10:48:10"), end=Event.convert_to_date("2021-11-08 9:00:00"), type_id=1, description="Match Legia", color="blue")

    new_event9 = Event(name="Event 9", details="Av. de Suècia", latitude=39.474, longitude=-0.361,
                       start=Event.convert_to_date("2021-11-11 10:48:10"), end=Event.convert_to_date("2021-11-11 9:00:00"), type_id=3,
                       description="Match Valencia", color="blue")


    new_event1.add_event_by_teams(['KKS LECH 1'])
    new_event1.save()
    print("new_event 1 added")

    new_event2.add_event_by_teams(['KKS LECH 1'])
    new_event2.save()
    print("new_event 2 added")

    new_event3.add_event_by_teams(['KKS LECH 1'])
    new_event3.save()
    print("new_event 3 added")

    new_event4.add_event_by_teams(['KKS LECH 1'])
    new_event4.save()
    print("new_event 4 added")

    new_event9.add_event_by_teams(['KKS LECH 1'])
    new_event9.save()

    print("new_event 9 added")


    new_event5 = Event(name="Event 5", details="Bułgarska 17", latitude=52.400, longitude=16.888,
                       start=Event.convert_to_date("2021-11-05 10:48:10"), end=Event.convert_to_date("2021-11-05 10:00:00"), type_id=3,
                       description="Match Valencia kks 2", color="blue")

    new_event6 = Event(name="Event 6", details="Jasielska 14", latitude=52.444, longitude=16.896,
                       start=Event.convert_to_date("2021-11-05 10:48:10"), end=Event.convert_to_date("2021-11-06 3:48:10"), type_id=5,
                       description="Medical Overview 1 kks 2", color="blue")

    new_event7 = Event(name="Event 7", details="Bułgarska 17", latitude=52.400, longitude=16.888,
                       start=Event.convert_to_date("2021-11-07 10:48:10"), end=Event.convert_to_date("2021-11-07 5:00:10"), type_id=4,
                       description="Training 1 kks 2", color="blue")

    new_event8 = Event(name="Event 8", details="Agrykola 8", latitude=54.166, longitude=19.422,
                       start=Event.convert_to_date("2021-11-15 10:48:10"), end=Event.convert_to_date("2021-11-15 7:00:00"), type_id=1,
                       description="Match Olimpa Elbląg", color="blue")

    new_event5.add_event_by_teams(['KKS LECH 2'])
    new_event5.save()
    print("new_event 5 kks2 added")

    new_event6.add_event_by_teams(['KKS LECH 2'])
    new_event6.save()
    print("new_event 6 kks2 added")

    new_event7.add_event_by_teams(['KKS LECH 2'])
    new_event7.save()
    print("new_event 7 kks2 added")

    new_event8.add_event_by_teams(['KKS LECH 2'])
    new_event8.save()
    print("new_event 7 kks2 added")


@click.command(name="cron_job_check_wellness")
@with_appcontext
def cron_job_check_wellness():
    "Command for check if event status is WELLNESS AND CHANGE TO MOTORIC"
    events = Event.query.filter_by(state="WELLNESS").all()
    print("Checking IF WELLNESS PAST")
    for event in events:
        event.check_state_if_event_past()


@click.command(name="cron_job_check_active")
@with_appcontext
def cron_job_check_active():
    "Command for check if event status is ACTIVE AND CHANGE TO WELLNESS"
    events = Event.query.filter_by(state="ACTIVE").all()
    print("Checking if ACTIVE PAST")
    for event in events:
        event.check_state_if_event_wellness()


@click.command(name="cron_job_check_contusion")
@with_appcontext
def cron_job_check_contusion():
    "Command for check if CONTUSION is past"
    constusions = Contusion.query.filter_by(state="ACTIVE").all()
    print("Checking Contusions")
    for con in constusions:
        con.check_state_if_contusion_past()


@click.command(name="deploy_app")
@with_appcontext
def deploy_app():
    create_positions()
    create_nationalities()
    create_basic_users()
    create_events()




@click.command(name="create_random_data")
@with_appcontext
def create_random_data():
    #KAZDEMU playerowi Z TEAMU 1 towrzy event i mu dodaje motoric
    users = User.query.filter(User.teams.any(id=1), User.roles.any(id=2)).all()

    i=1
    for i in range(40)[1:]:
        start_date = "2021-10-{}".format(i)
        date = datetime.strptime(start_date, "%Y-%m-%d")
        name = "Training {}".format(i)
        event = Event(name=name, start=date, end=date, type_id=4, state="PAST")
        print("[EVENT] {} {} {}".format(event.name , event.end, event.type_id))
        if i % 5 == 0:
            name = "Match {}".format(i)
            event = Event(name=name, start=date, end=date, type_id=1, state="PAST", has_kinase=True)
        event.save()
        for user in users:
            ###TUTAJ OSZUKANY MOTORIC
            user.events.append(event)
            print("User dodany do {} {}".format(user.first_name, event.name))
            motoric = Motoric(event_id=event.id, date=date,
                              total_distance=np.random.uniform(low=3000, high=7000),
                              sprint=np.random.uniform(low=180, high=500),
                              total_player_load=np.random.uniform(low=400, high=800),
                              hsr=np.random.uniform(low=165, high=505),
                              acceleration=np.random.randint(low=50, high=200),
                              deceleration=np.random.randint(low=62, high=150),
                              field_time=np.random.randint(low=60, high=80),
                              maximum_velocity=np.random.uniform(low=20, high=32),
                              meterage_per_minute=np.random.uniform(low=64, high=85),
                              max_vel_per_max=np.random.uniform(low=88, high=100),
                              running=np.random.uniform(low=500, high=1000), state="COMPLETED")

            wellness = Wellness(event_id=event.id, fatigue=np.random.randint(low=1, high=5),sleep_quality=np.random.randint(low=1, high=5),  mood=np.random.randint(low=1, high=5),muscle_soreness=np.random.randint(low=1, high=5),date=date,state="COMPLETED")

            rpe = RPE(event_id=event.id, value=np.random.randint(low=1, high=10), date=date, state="COMPLETED")

            kinase = Kinase(event_id=event.id, value=np.random.randint(low=1, high=10), date=date, state="COMPLETED")

            print("Motoric do {} {}".format(user.first_name, event.name))
            print(motoric)

            motoric.save()
            wellness.save()
            rpe.save()
            kinase.save()
            user.motoric.append(motoric)
            user.wellness.append(wellness)
            user.rpe.append(rpe)
            user.kinase.append(kinase)

            user.save()
        if i % 6 == 0 or i % 7 == 0:
            i += 1

'''
    events_kinase = Event.query.filter_by(state="KINASE").all()

    if len(events_kinase) != 0:
        for event in events:
            event.check_kinase()
'''


@click.command(name="create_random_messages")
@with_appcontext
def create_random_messages():

    message = Message(sender_id=3, recipient_id=1, body="Siemano jak tam?")
    message2= Message(sender_id=1, recipient_id=3, body="spoko a jak tam?")
    message3 = Message(sender_id=3, recipient_id=1, body="Świetnie!")
    message4 = Message(sender_id=1, recipient_id=3, body="Wpadniesz na tening?")

    message.save()
    message2.save()
    message3.save()
    message4.save()

app.cli.add_command(create_random_messages)
app.cli.add_command(create_random_data)
app.cli.add_command(create_basic_users)
app.cli.add_command(create_basic_survey)
app.cli.add_command(create_positions)
app.cli.add_command(create_nationalities)
app.cli.add_command(create_events)
app.cli.add_command(create_medic_contusion)


app.cli.add_command(cron_job_check_wellness)
app.cli.add_command(cron_job_check_active)
app.cli.add_command(cron_job_check_contusion)




app.cli.add_command(deploy_app)


