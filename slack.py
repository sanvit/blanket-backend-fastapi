from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from enum import Enum
import requests
from fastapi import Body


app = FastAPI()


@app.post('/users')
async def get_dm_user_list(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = 'https://slack.com/api/conversations.list?types=im'
    rsp = requests.post(url=url, headers=headers).json()
    users_dict = dict()
    if rsp.get('ok'):
        channels = rsp.get('channels')  # user값과 id 값이 있음
        for e in channels:
            user = e['user']
            users_dict[user] = {'id': e['id']}
    print('users dict:', users_dict)
    url = 'https://slack.com/api/users.list'
    rsp = requests.post(url=url, headers=headers).json()
    print(rsp)
    if rsp.get('ok'):
        members = rsp.get('members')  # 프로필 정보 있음
        print('members:', members)
        for e in members:
            id = e['id']  # member의 id값
            print('id:', id)
            if not e['is_bot'] and not e['deleted']:
                print('is bot:', e['is_bot'])
                profile = e['profile']  # 개별 profile
                print(profile.get('real_name'))
                print('--------------------------------')
                if id in users_dict:  # 대화목록에 id가 없는 경우가 있음
                    users_dict[id]['real_name'] = profile['real_name']
                    if profile.get('image_original'):
                        users_dict[id]['image_original'] = profile['image_original']
                    else:
                        users_dict[id]['image_original'] = profile['image_32']
            else:
                if id in users_dict:
                    del users_dict[id]


    return users_dict


@app.post('/conversation/{channel}')
async def get_conversation(token, channel):
    headers = {"Authorization": f"Bearer {token}"}
    url = f'https://slack.com/api/conversations.history?channel={channel}'
    rsp = requests.post(url=url, headers=headers).json()
    return rsp


@app.post('/messages')
async def create_delete_task(payload = Body(...)):
    ids = payload['ids']
    from tasks import delete_message
    for id in ids:
        print('creating task...')
        task = delete_message.delay(id)
        return JSONResponse({"task_id": task.id})
    return {"success": "ok"}


@app.get("/tasks/{task_id}")
def get_status(task_id):
    from tasks import celery
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)