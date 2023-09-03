#!/usr/bin/env bash

celery -A messaging.app beat --loglevel=info
