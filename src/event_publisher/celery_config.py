from datetime import timedelta

BROKER_URL = "pyamqp://guest:guest@localhost//"

# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Specifies the number of concurrent workers. A worker processes a single task at a time.
CELERYD_CONCURRENCY = 4

CELERY_SEND_TASK_ERROR_EMAILS = False

ADMINS = [
    ("Your Name", "your_email@example.com"),
]

EMAIL_HOST = "your-smtp-server.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 5  # in seconds
SERVER_EMAIL = "server@example.com"
DEFAULT_FROM_EMAIL = "webmaster@example.com"
EMAIL_BACKEND = "smtp.EmailBackend"

CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Import task modules from registered apps.
CELERY_IMPORTS = ("event_publisher.tasks",)

CELERYBEAT_SCHEDULE = {
    # Executes every minute
    "run-every-minute": {
        "task": "event_publisher.tasks.my_periodic_task",  # Replace with your task's name
        "schedule": timedelta(minutes=1),
        "args": (),  # Arguments passed to the task. Can be omitted if not required.
    },
    # Add other tasks here as needed...
}

CELERYBEAT_PERSISTENT_SCHEDULER = (
    True  # If True, the schedule is stored in a local shelve database file.
)
CELERYBEAT_SCHEDULER = "celery.beat.PersistentScheduler"  # Use persistent scheduler. It keeps track of the last run
# times in a local shelve database file.
CELERYBEAT_SCHEDULE_FILENAME = (
    "./celerybeat-schedule"  # File path to store the last run times of the tasks.
)
