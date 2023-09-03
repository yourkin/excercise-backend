from celery import Celery

from messaging import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)
