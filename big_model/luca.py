import json
import os

import requests
from model.Response import Response
from utils import set_env


def get_response(request):
    model = request['model'].lower()
    access_token = os.environ.get('LUCA_ACCESS_TOKEN')
    conversation_id = os.environ.get('LUCA_CONVERSATION_ID')
    question = request['messages'][0]['content']
    if model is None or model != 'luca':
        return Response(message=f'模型{model}不支持', status_code=400)
    elif access_token is None or access_token == '' or access_token.isspace():
        return Response(message=f'模型{model}的access_token不能为空', status_code=400)
    elif conversation_id is None or conversation_id == '' or conversation_id.isspace():
        return Response(message=f'模型{model}的conversation_id不能为空', status_code=400)
    else:
        url = "https://luca.cn/openbmb/api/submitMsg"
        url_msg = "https://luca.cn/openbmb/api/queryMsg"
        payload = json.dumps({
            "generateType": "NORMAL",
            "conversationId": conversation_id,
            "parentMessageId": "",
            "chatMessage": [
                {
                    "role": "USER",
                    "content": {
                        "pairs": question,
                        "imageId": "",
                        "type": "TEXT"
                    },
                    "id": "",
                    "parentMsgId": ""
                }
            ]
        })
        headers = {
            "authority": "luca.cn",
            "method": "POST",
            "path": "/openbmb/api/submitMsg",
            "scheme": "https",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Length": "2482",
            "Content-Type": "application/json",
            "Cookie": "sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%2218d9b4765105cb-001e453ffb814c9f-4c657b58-2073600-18d9b476511e85%22%7D; sajssdk_2015_new_user_luca_cn=1; _bl_uid=aUlh8sOUiUIcb6rXv5hk6zF9OIjO; sa_jssdk_2015_luca_cn=%7B%22distinct_id%22%3A%22MTM5ODY1NjcwODM%3D%22%2C%22first_id%22%3A%2218d9b4765105cb-001e453ffb814c9f-4c657b58-2073600-18d9b476511e85%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThkOWI0NzY1MTA1Y2ItMDAxZTQ1M2ZmYjgxNGM5Zi00YzY1N2I1OC0yMDczNjAwLTE4ZDliNDc2NTExZTg1IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiTVRNNU9EWTFOamN3T0RNPSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22MTM5ODY1NjcwODM%3D%22%7D%7D",
            "Origin": "https://luca.cn",
            "Referer": "https://luca.cn/chat",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Token": access_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0."
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        try:
            data = json.loads(response.content)
            msg_id = data['data']['childMsgId']
            playload_new = json.dumps({
                "conversationId": conversation_id,
                "messageId": msg_id
            })
            while True:
                rsp = requests.request("POST", url_msg, headers=headers, data=playload_new)
                data = json.loads(rsp.content)
                if data['code'] == 0 and data['data']['stopEnum'] is not None and data['data']['stopEnum'] == 'PASS':
                    content = data['data']['output']
                    break
            return Response(status_code=200, message=content)
        except Exception as e:
            return Response(message=f'请求第三方API接口失败，原因：{e}', status_code=500)


if __name__ == '__main__':
    set_env.set_env_variables()
    req = {
        "model": "luca",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(req)
    print(response.message)
