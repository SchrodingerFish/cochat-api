import json
import os

import requests

from model.Response import Response
from utils import set_env


def get_response(request):
    model = request['model'].lower()
    content = request['messages'][0]['content']
    if model not in ['gemini-pro']:
        return Response(message=f'模型{model}不支持', status_code=400)
    if content is None or content == "":
        return Response(status_code=400, message="问题不能为空")
    try:
        url = f"https://gemini.chata.shop/v1beta/models/gemini-pro:generateContent?key={os.environ.get('GEMINI_API_KEY')}"

        payload = json.dumps({
            "contents": [{
                "parts": [{
                    "text": content
                }]
            }],
            "generationConfig": {
                "temperature": 1.0,
                "maxOutputTokens": 4096,
                "topP": 0.8,
                "topK": 10
            }
        }
        )
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.request("POST", url, headers=headers, data=payload)
        return Response(status_code=200, message=res.json()['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e:
        return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "gemini-pro",
        "messages": [
            {
                "role": "user",
                "content": "你都会些什么？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
