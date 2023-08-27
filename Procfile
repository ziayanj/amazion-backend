release: python manage.py migrate
web: gunicorn amazion_backend.wsgi
worker: celery -A amazion_backend worker