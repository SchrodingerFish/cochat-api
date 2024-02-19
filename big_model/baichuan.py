import json
import os

import requests

from model.Response import Response
from utils import set_env


def get_response(request):
    model = request['model']
    content = request['messages'][0]['content']
    if model not in ['Baichuan2-Turbo','Baichuan2-Turbo-192k']:
        return Response(message=f'模型{model}不支持', status_code=400)
    if content is None or content == "":
        return Response(status_code=400, message="问题不能为空")
    try:
        url = "https://api.baichuan-ai.com/v1/chat/completions"

        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        })
        headers = {
            'Authorization': f'Bearer {os.environ.get("BAICHUAN_API_KEY")}',
            'Content-Type': 'application/json'
        }
        res = requests.request("POST", url, headers=headers, data=payload)
        return Response(status_code=200, message=res.json()['choices'][0]['message']['content'])
    except Exception as e:
        return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "Baichuan2-Turbo",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
