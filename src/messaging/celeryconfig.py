from datetime import timedelta

from ex_back.config import get_settings

broker_url = get_settings().broker_url

imports = ("messaging.tasks.producer", "messaging.tasks.consumer")


# result_backend = 'redis://localhost:6379/0'

# Specifies the number of concurrent workers. A worker processes a single task at a time.
worker_concurrency = 4

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

task_default_queue = "default"
task_default_exchange_type = "direct"
task_default_routing_key = "default"

accept_content = ["json"]
task_serializer = "json"
result_serializer = "json"
timezone = "UTC"

beat_schedule = {
    # Executes every minute
    "run-every-minute": {
        "task": "messaging.tasks.producer.publish_events_to_rabbitmq",  # The name of the task to execute
        "schedule": timedelta(minutes=1),
        "args": (),  # Arguments passed to the task. Can be omitted if not required.
    },
    "consume_order_messages_once": {
        "task": "messaging.tasks.consumer.consume_order_messages",
        "schedule": timedelta(seconds=10),  # run 10 seconds after starting
        "options": {
            "expires": 9
        },  # task expires after 9 seconds to ensure it only runs once
    },
}

CELERYBEAT_PERSISTENT_SCHEDULER = (
    True  # If True, the schedule is stored in a local shelve database file.
)
beat_scheduler = "celery.beat.PersistentScheduler"  # Use persistent scheduler. It keeps track of the last run
# times in a local shelve database file.
beat_schedule_filename = "./messaging/celerybeat-schedule"  # File path to store the last run times of the tasks.
