# LechSys - Backend
## _Intrukcj&#234; aby odpali&#230; lokalnie_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Aplikacje napisane we flasku maj&#185; pewngeo rodzaju struktur&#234; plik�w, o kt�r&#185; trzeba dba&#230; podczas pisania aplikacji webowych.
Poni&#191;ej jest przedstawine drzewko projektu:

- app - tutaj jest ca&#179;a aplikacja;
- /models - klasy zwi&#185;zane z obiektami z bazy (ORM), ale i te&#191; jaki kolwiek element, kt�ry mo&#191;e zosta&#230; przedstawiony za pomoc&#185; klasy (formularze te&#191; mog&#185; tutaj si&#234; znajdowa&#230;);
- /static - jak nazwa wskazuje, znajduj&#185; si&#234; elementy statyczne aplikacji, takimi elementami mog&#185; by&#230; arkusze styl�w (.css), albo i zdj&#234;cia (.jpg, .png);
- /template - tutaj s&#185; pliki zwi&#185;zane z szablonem strony (.html)
- config.py - konfiguracja aplikacji
- run.py - co&#339; na wz�rch __init__, odwo&#179;uje si&#234; do struktury katalogu app i j&#185; uruchamia (oraz wszystkie jego modu&#179;Y).

## Wymagania

Aplikacja korzysta z bazy danych, aby sobie najszybciej skonfigurowa&#230; tak&#185; (oraz wiele innch rzeczy) wystarczy &#339;ci&#185;gn&#185;&#230; oprogramowanie XAMPP, kt�ry ma w sobie zestaw narz&#234;dzi do podmontowania bazy mysql, serwer apache, filezilla i inne.
- &#338;ci&#185;gnij XAMPP ze strony producenta i zainstaluj;
- Nast&#234;pnie otw�rz XAMPP CONTROL PANEL
- APACHE > START, MYSQL > START
- Tym samym odpali&#179;e&#339; instancj&#234; serwera www apache (tak aby m�c hostowa&#230; pewn&#185; aplikacj&#234;), oraz odpali&#179;e&#339; instancj&#234; silnika baz mysql, kt�r dodatkowo ma interwejs www do zarz&#185;dzania baz&#185; (phpmyadmin - dlatego ci jest potrzebny serwer www - aby m�c si&#234; do ten interfejs wy&#339;wietli&#230; z poziomu przegl&#185;darki) mo&#191;esz sprawdzi&#230; t&#234; storn&#234; pod adresem:
- _localhost/phpmyadmin_

Teraz mo&#191;esz &#339;ci&#185;gn&#185;&#230; rzeczy z tego repozytorium. Potem wystarczy, &#191;e utworzysz wirtualne &#339;rodowisko (tak by nie za&#339;mieca&#230; ca&#179;y komputer a tylko wyodr&#234;bnion&#185; cz&#234;&#339;&#230; pami&#234;ci do tego przystosowan&#185;)

## Tworzenie wirtualnego &#339;rodowiska
```sh
python3 -m venv /path/to/new/virtual/environment
```
## Aktywacja wirtualnego &#339;rodowiska
```sh
/path/to/new/virtual/environment/Scripts/activate.bat    <--- aktywacja Na windowsie
source /path/to/new/virtual/environment/Scripts/activate       <------aktywacja Na Linux / MacOs pewnie te&#191;
```
## &#338;ci&#185;gni&#234;cie potrzebnych bibliotek
Przygotowa&#179;em plik, kt�ry ma w sobie potrzebne rzeczy, wystarczy go tylko "wyeksportowa&#230;" za pomoc&#185; prostej komendy (pamietaj, aby to zrobi&#230; w wirtualnym &#339;rodowisku):

> pip -r install requirements.txt

pip sam zainstaluje potrzebne paczki.

## BUG Z ODPALENIEM
Niestety jak robi si&#234; deploy aplikacji powinno si&#234; bra&#230; pod uwag&#234; to, &#191;e niekt�re rzeczy musz&#185; by&#230; odg�rnie skonfigurowane by dzia&#179;a&#179;y. Ostatnio nie by&#179;o modeli w bazie - dlatego mieli&#339;my b&#179;&#185;d.
Nale&#191;y przed zrobi&#230;:

1.Zakomentowa&#230; w pliku models.py
```
'''

#create USERs and send to databse if they are not created

if not User.query.filter(User.username == "player").first():
    player_user = User(
        username = "player",
        first_name="playerName",
        last_name="playerLastName",
        email="player@mail.com"
    )
    player_user._set_password('lol')
    db.session.add(player_user)
    db.session.commit()

if not User.query.filter(User.username == "staff").first():
    staff_user = User(
        username = "staff",
        first_name="staffName",
        last_name="staffLastName",
        email="staff@mail.com"
    )
    staff_user._set_password('lol')
    db.session.add(staff_user)
    db.session.commit()

if not User.query.filter(User.username == "admin").first():
    admin_user = User(
        username = "admin",
        first_name="adminName",
        last_name="adminLastName",
        email="admin@mail.com"
    )
    admin_user._set_password('lol')
    db.session.add(admin_user)
    db.session.commit()

#create Roles and send to databse if they are not created

if not Role.query.filter(Role.name == "player").first():
    player_role = Role(id= 2, name ="player")
    db.session.add(player_role)
    player_user.roles.append(player_role)
    db.session.add(player_user)
    db.session.commit()

if not Role.query.filter(Role.name == "admin").first():
    admin_role = Role(id= 1, name ="admin")
    db.session.add(admin_role)
    admin_user.roles.append(admin_role)
    db.session.add(admin_user)
    db.session.commit()

if not Role.query.filter(Role.name == "staff").first():
    staff_role = Role(id= 3, name ="staff")
    db.session.add(staff_role)
    staff_user.roles.append(staff_role)
    db.session.add(staff_user)
    db.session.commit()
'''
```

Ustawi&#230; zmienna globaln&#185; dla apki FLASK:
>export FLASK_APP=run.py (odpal z poziomu katalogu g&#179;�wnego /LechSys-backend/<tutaj>)

Potem

> flask db init

Poprawny wynik:
```
(envLechsys) C:\Users\Tonid\Desktop\LechSYs>flask db init
Creating directory C:\Users\Tonid\Desktop\LechSYs\migrations ...  done
Creating directory C:\Users\Tonid\Desktop\LechSYs\migrations\versions ...  done
Generating C:\Users\Tonid\Desktop\LechSYs\migrations\alembic.ini ...  done
Generating C:\Users\Tonid\Desktop\LechSYs\migrations\env.py ...  done
Generating C:\Users\Tonid\Desktop\LechSYs\migrations\README ...  done
Generating C:\Users\Tonid\Desktop\LechSYs\migrations\script.py.mako ...  done
Please edit configuration/connection/logging settings in 'C:\\Users\\Tonid\\Desktop\\LechSYs\\migrations\\alembic.ini' before proceeding.
```

I ostatecznie
> flask db migrate
> flask db upgrade

Poprawny wynik:
```
(envLechsys) C:\Users\Tonid\Desktop\LechSYs>flask db migrate
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.env] No changes in schema detected.
```

teraz stworzy tabele i nie b&#234;dzie p&#179;aka&#179;, TERAZ ODKOMENTUJECIE TAMTO I PU&#338;CIE APP.

## Odpalenie aplikacji
Je&#191;eli wszystko wcze&#339;niej zrobi&#179;e&#339; dobrze to do odpalenia wystarczy w katalogu g&#179;�wnym:

> flask run





najpierw basic obraz, srodowisko ./build-python.sh
./build.sh