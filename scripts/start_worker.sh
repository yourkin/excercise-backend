#!/bin/sh

celery -A event_publisher.app worker --loglevel=info

