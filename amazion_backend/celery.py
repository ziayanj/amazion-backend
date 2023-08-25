import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazion_backend.settings.dev')

celery = Celery('amazion_backend')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
