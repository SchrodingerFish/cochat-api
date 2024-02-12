import os
from pprint import pprint

import requests

from model.Response import Response
from utils import set_env


def get_response(request):
    content = request['messages'][0]['content']
    model = request['model'].lower()
    if content is None or content == "":
        return Response(status_code=400, message="问题不能为空")
    if model not in ['360gpt_s2_v9', '360gpt-pro']:
        return Response(message=f'模型{model}不支持', status_code=400)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("ZHINAO_API_KEY")}',
    }

    json_data = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': content,
            },
        ],
        'stream': False,
    }
    try:
        response = requests.post('https://api.360.cn/v1/chat/completions', headers=headers, json=json_data)
        return Response(status_code=200, message=response.json()['choices'][0]['message']['content'])
    except Exception as e:
        return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "360gpt-pro",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
