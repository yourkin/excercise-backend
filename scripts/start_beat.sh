#!/usr/bin/env bash

celery -A event_publisher.app beat --loglevel=info
