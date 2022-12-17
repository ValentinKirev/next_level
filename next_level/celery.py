import os

import dotenv
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'next_level.settings')

celery_app = Celery('next_level')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env.prod')
dotenv.read_dotenv(env_file)
