import datetime
import numpy as np
import pandas as pd
from datetime import datetime

from app.models.models import User, Motoric, Event, Role, Team

lolo = '/home/xoin/Escritorio/lechsys-backend/docs/export4.csv'
data = pd.read_csv (lolo)
df = pd.DataFrame(data, columns = ['Name', 'Date',
                                   'Total Distance (m)', 'Sprint (m)',
                                   'Total Player Load', 'HSR (m)',
                                   'Acceleration','Deceleration', 'Field Time',
                                   'Maximum Velocity (km/h)', 'Meterage Per Minute', 'Max Vel (% Max)',
                                   'Running (m)'])


for i, row in df.iterrows():
    print(i , row )
'''
def import_one_real():
    event = Event.query.filter_by(id=142).first()
    users_planed_in_event = event.get_users_of_event()
    for i, row in df.iterrows():
        first_name, last_name = row[0].split(" ")[0], row[0].split(" ")[1]
        user = User.query.filter(User.first_name==first_name, User.last_name==last_name).first()
        if user:
            #minutes to time = int() ->  if field.type == intdatetime.timedelta(minutes=72)datetime.timedelta(minutes=row[8])
            motoric = Motoric(event_id=event.id, date=datetime.strptime(row[1] , '%d/%m/%Y'), total_distance=row[2], sprint=row[3], total_player_load=row[4], hsr=row[5], acceleration=row[6], deceleration=row[7], field_time=row[8], maximum_velocity=row[9], meterage_per_minute=row[10], max_vel_per_max=row[11], running=row[12])
            print(motoric)
            motoric.save()
            user.motoric.append(motoric)
            user.save()
            print('dodany')



users = User.query.filter(User.teams.any(id=1), User.roles.any(id=2)).all()

def create_40_events():
    users = User.query.filter(User.teams.any(id=1), User.roles.any(id=2)).all()

    i=1
    for i in range(40)[1:]:
        start_date = "2021-12-{}".format(i)
        date = datetime.strptime(start_date, "%Y-%m-%d")
        name = "Training {}".format(i)
        event = Event(name=name, start=date, end=date, type_id=4)
        print("[EVENT] {} {} {}".format(event.name , event.end, event.type_id))
        if i % 5 == 0:
            name = "Match {}".format(i)
            event = Event(name=name, start=date, end=date, type_id=1)
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
                              running=np.random.uniform(low=500, high=1000))

            print("Motoric do {} {}".format(user.first_name, event.name))
            print(motoric)

            motoric.save()
            user.motoric.append(motoric)

            user.save()
        if i % 6 == 0 or i % 7 == 0:
            i += 1



def import_40_random():


    for i, row in df.iterrows():
        first_name, last_name = row[0].split(" ")[0], row[0].split(" ")[1]
        user = User.query.filter(User.first_name==first_name, User.last_name==last_name).first()
        if user:pass


#create_40_events()


def make_widget_data(num):
    fake_widgets = [{'Item Number': id(y),
                     'Total distance (m)': np.random.uniform(low=3000, high=7000),
                     'sprint (m)': np.random.uniform(low=30,high=40),
                     'Step 3': np.random.exponential(4)} for y in range(num)]

    return fake_widgets


create_40_events()
'''


lol = [{'total_distance-1': ['1'], 'sprint-1': ['2'], 'total_player_load-1': ['3'], 'hsr-1': ['4'], 'acceleration-1': ['5'], 'deceleration-1': ['6'], 'field_time-1': ['7'], 'maximum_velocity-1': ['8'], 'meterage_per_minute-1': ['9'], 'max_vel_per_max-1': ['10'], 'running-1': ['11'], 'submitManually': ['Submit']}]