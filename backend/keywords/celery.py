from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "keyword-metrics-daily": {
        "task": "keywords.tasks.update_keyword_metrics",
        "schedule": crontab(hour=0, minute=0),
        "args": (["chatbot","ai"], "8157050680"),
    },
}
