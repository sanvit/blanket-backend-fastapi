from calendar import c
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from enum import Enum
import requests
from fastapi import Body
import datetime
import time as t
import pusher
pusher_client = pusher.Pusher(app_id=u'4444', key=u'blanket', secret=u'blanket',
                              ssl=True, host=u'linode-tyo2-1.soketi.sanvit.net', port=443)
sent_ids = []

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/message/{sos_id}")
async def send_message(sos_id):
    pusher_client.trigger(u'blanket', u'sos', {
        'id': sos_id,
        'lat': 123.4567,
        'lng': 12.34567,
        'user_info': {
            'name': '김철수',
            'age': 20,
            'phone': '010-1234-5678',
            'family_contact': '010-1234-5678',
            'family_contact_name': '김철수',
        }
    })
    return {"response.json()": "response.json()"}


@app.post("/message")
async def send_message(request: Request):
    # get request body
    body = await request.json()

    print(body)
    pusher_client.trigger(u'blanket', u'sos', body)
    return body


def get_now_in_kst(timedelta=0):
    if isinstance(timedelta, int):
        timedelta = datetime.timedelta(seconds=timedelta)
    return datetime.datetime.now() + datetime.timedelta(hours=9) + timedelta


def convert_time(time, timedelta=0):
    if isinstance(timedelta, int):
        timedelta = datetime.timedelta(seconds=timedelta)
    return (time + timedelta).strftime("%Y-%m-%d %H:%M:%S")


@app.get("/lora")
async def send_message():
    time = get_now_in_kst()
    data1 = {
        "id": "12",
        "user_info": {
            "name": "김재원",
            "age": 20,
            "sex": "male",
            "phone": "010-1234-5678",
            "family_contact": "010-1234-5678",
            "family_contact_name": "김철수"
        },
        "location": [
            {
                "lat": 37.65940344029378,
                "lng": 126.9754864528261,
                "date": convert_time(time)
            }
        ]
    }
    data2 = {
        "id": "12",
        "user_info": {
            "name": "김재원",
            "age": 20,
            "sex": "male",
            "phone": "010-1234-5678",
            "family_contact": "010-1234-5678",
            "family_contact_name": "김철수"
        },
        "location": [
            {
                "lat": 37.65940344029378,
                "lng": 126.9754864528261,
                "date": convert_time(time)
            },
            {
                "lat": 37.65972619464464,
                "lng": 126.9772030666551,
                "date": convert_time(time, 5)
            }
        ]
    }
    data3 = {
        "id": "12",
        "user_info": {
            "name": "김재원",
            "age": 20,
            "sex": "male",
            "phone": "010-1234-5678",
            "family_contact": "010-1234-5678",
            "family_contact_name": "김철수"
        },
        "location": [
            {
                "lat": 37.65940344029378,
                "lng": 126.9754864528261,
                "date": convert_time(time)
            },
            {
                "lat": 37.65972619464464,
                "lng": 126.9772030666551,
                "date": convert_time(time, 5)
            },
            {
                "lat": 37.659216581870396,
                "lng": 126.97893040932051,
                "date": convert_time(time, 10)
            }
        ]
    }
    data4 = {
        "id": "12",
        "user_info": {
            "name": "김재원",
            "age": 20,
            "sex": "male",
            "phone": "010-1234-5678",
            "family_contact": "010-1234-5678",
            "family_contact_name": "김철수"
        },
        "location": [
            {
                "lat": 37.65940344029378,
                "lng": 126.9754864528261,
                "date": convert_time(time)
            },
            {
                "lat": 37.65972619464464,
                "lng": 126.9772030666551,
                "date": convert_time(time, 5)
            },
            {
                "lat": 37.659216581870396,
                "lng": 126.97893040932051,
                "date": convert_time(time, 10)
            },
            {
                "lat": 37.65941193384732,
                "lng": 126.98022859852867,
                "date": convert_time(time, 15)
            }
        ]
    }
    pusher_client.trigger(u'blanket', u'sos', data1)
    t.sleep(5)
    pusher_client.trigger(u'blanket', u'sos', data2)
    t.sleep(5)
    pusher_client.trigger(u'blanket', u'sos', data3)
    t.sleep(5)
    pusher_client.trigger(u'blanket', u'sos', data4)
    return {"success": True}
