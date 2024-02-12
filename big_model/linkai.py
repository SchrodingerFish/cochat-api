import os
from pprint import pprint

import requests

from model.Response import Response
from utils import set_env


##

def get_response(request):
    if request['model'].lower() not in ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4', 'wenxin', 'xunfei']:
        return Response(message=f'模型{request["model"]}不支持', status_code=400)
    content = request['messages'][0]['content']
    if content is None or content == "":
        return Response(status_code=400, message="问题不能为空")

    url = "https://api.link-ai.chat/v1/chat/completions"

    payload = {
        "app_code": "default",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('LINK_AI_API_KEY')}"
    }
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        # pprint(response.json())
        return Response(status_code=200, message=response.json()['choices'][0]['message']['content'])
    except Exception as e:
        return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
