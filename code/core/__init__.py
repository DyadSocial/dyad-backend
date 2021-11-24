import os
import celery as Celery
__all__ = ['celeryApp']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings');
celeryApp = Celery()
celeryApp.config_from_object('django.conf:settings', namespace='CELERY')
celeryApp.autodiscover_tasks()