#!/bin/sh

celery -A messaging.app worker --loglevel=info

