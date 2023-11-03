import os
import time

from celery import Celery
from dotenv import load_dotenv
from generateClova import executor

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.worker_concurrency = 3


@celery.task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c


@celery.task(name="chatbot")
def respond(text):
    return executor.reply(text)
