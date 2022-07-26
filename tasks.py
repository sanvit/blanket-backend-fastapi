import os
import time
from celery import Celery
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
celery.conf.task_track_started = True

@celery.task(name="add_delete_task")
def add_delete_task(ts_list, channel, token):
    for ts in ts_list:
        delete_msg(ts, channel, token)
        print('passing to delete_msg...', ts)
        time.sleep(1.2)
    return True

@celery.task(name="delete_msg")
def delete_msg(ts, channel, token):
    import requests
    url = f"https://slack.com/api/chat.delete?channel={channel}&ts={ts}&as_user=true"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        rsp = requests.post(url=url, headers=headers)
        print('rsp.text', rsp.text)
        print('rsp.status_code:', rsp.status_code)
    except Exception as e:
        print('exception occured:', e)
    return True

"""
https://slack.com/api/chat.delete?channel=D02169BQDAN&ts=1657680383.511599&as_user=true
"""