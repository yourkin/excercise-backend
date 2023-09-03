from celery import Celery

from event_publisher import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)
