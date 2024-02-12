import os

from big_model import spark_offical_api
from big_model.spark_offical_api import query
from model.Response import Response
from utils import set_env

set_env.set_env_variables()

text = []


def get_text(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def get_length(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def check_len(text):
    while (get_length(text) > 8000):
        del text[0]
    return text


global spark_url, domain

# 以下密钥信息从控制台获取
appid = os.environ.get('SPARK_APPID')  # 填写控制台中获取的 APPID 信息
api_secret = os.environ.get('SPARK_API_SECRET')  # 填写控制台中获取的 APISecret 信息
api_key = os.environ.get('SPARK_API_KEY')  # 填写控制台中获取的 APIKey 信息


def get_response(request):
    global appid, api_secret, api_key, spark_url, domain
    version = request['version']
    model = request['model']
    content = request['messages'][0]['content']
    if version not in [1, 2, 3, 3.5]:
        return Response(400, "version参数错误")
    if model != "spark":
        return Response(400, "model参数错误")
    if content is None or content == "":
        return Response(400, "问题不能为空")
    if version == 1:
        domain = "general"  # v1.5版本
        spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
    elif version == 2:
        domain = "generalv2"  # v2.0版本
        spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
    elif version == 3:
        domain = "generalv3"  # v3.0版本
        spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
    elif version == 3.5:
        domain = "generalv3.5"  # v3.5版本
        spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v3.0环境的地址
    text.clear()
    question = check_len(get_text("user", content))
    spark_offical_api.answer = ""
    query(appid, api_key, api_secret, spark_url, domain, question)
    return Response(200, get_text("assistant", spark_offical_api.answer)[-1]["content"])


if __name__ == '__main__':
    request = {
        "version": 3,
        "model": "spark",
        "messages": [
            {
                "role": "user",
                "content": "你是什么模型？"
            }
        ]
    }
    response = get_response(request)
    print(response.message)
