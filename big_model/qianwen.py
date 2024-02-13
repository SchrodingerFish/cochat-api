import logging
import os
import random
import dashscope
from http import HTTPStatus

from dashscope.api_entities.dashscope_response import Message

from model.Response import Response
from utils import set_env


# 通义千问
def get_response(request):
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
    model = request['model']
    if model not in ['qwen-max', 'qwen-max-1201', 'qwen-max-longcontext']:
        return Response(message=f'模型{model}不支持', status_code=400)
    else:
        question = request['messages'][0]['content']
        role = request['messages'][0]['role']
        if not question:
            return Response(message='您提问的问题不能为空', status_code=400)
        messages = [{'role': 'system', 'content': role},
                    {'role': 'user', 'content': question}]
        try:
            result = dashscope.Generation.call(
                model,
                messages=messages,
                seed=random.randint(1, 10000),
                result_format='message',
                temperature=0.9,  # set the result to be "message" format.
            )
            if result.status_code == HTTPStatus.OK:
                return Response(status_code=200, message=result.output.choices[0].message.content)
            else:
                logging.error('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    result.request_id, result.status_code,
                    result.code, result.message
                ))
                return Response(status_code=500, message=f'请求第三方API接口失败，原因：{result.message}')
        except Exception as e:
            logging.error(f'请求第三方API接口失败，原因：{e}')
            return Response(status_code=500, message=f'请求第三方API接口失败，原因：{e}')


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "qwen-max",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)

