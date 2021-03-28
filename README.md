# Janch - The Friendful Reminder Service

## Setting up

Install packages
```
pip install -r requirements.txt
```

Initialize database
```
python manage.py makemigrations
python manage.py migrate
```

Run development server
```
python manage.py runserver [<hostname>:<port>]
```

To deploy, apply the standard Django WSGI or ASGI middleware and can be served with Nginx

****LAHacks21*
