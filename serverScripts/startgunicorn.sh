sudo gunicorn --workers 2 --bind unix:/var/www/application.sock -m 007 wsgi:app
