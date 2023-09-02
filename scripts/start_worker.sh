#!/bin/sh

celery -A event_publisher.tasks worker --beat --loglevel=info
