from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'run-my-task-every-24-hours': {
        'task': 'crawler.tasks.scrape_article_from_url',
        'schedule': timedelta(hours=24),
    },
}