import os

import requests

from model.Response import Response
from utils import set_env


def get_response(request):
    group_id = os.environ.get('MINIMAX_GROUP_ID')
    api_key = os.environ.get('MINIMAX_API_KEY')
    model = request['model'].lower()
    content = request['messages'][0]['content']
    if model not in ['abab5.5-chat', 'abab5.5s-chat', 'abab6-chat']:
        return Response(message=f'模型{model}不支持', status_code=400)
    if content is None or content == "":
        return Response(status_code=400, message="问题不能为空")
    url = f"https://api.minimax.chat/v1/text/chatcompletion?GroupId={group_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": "你是一个智能AI专家，擅长用多种语言准确快速的回答用户问题。",
        "role_meta": {
            "user_name": "我",
            "bot_name": "专家"
        },
        "messages": [
            {
                "sender_type": "USER",
                "text": content
            }
        ]
    }

    try:
        result = requests.post(url, headers=headers, json=payload)
        return Response(status_code=200, message=result.json()['reply'])
    except Exception as e:
        return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "abab5.5s-chat",
        "messages": [
            {
                "role": "user",
                "content": "你觉得哪个国家最有发展前景？并阐述原因"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
