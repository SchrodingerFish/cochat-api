# cochat-api
## 项目名
> 整合各家API的接口
## 作者
> SchrodingersFish
## 版本
> v1.0.0
## 项目目录结构
   
    |---big_model                       大模型
    |---model                           对象
    |---utils                           工具包
    |---.env                            环境变量的配置文件
    |---.env.example                    环境变量的配置文件例子
    |---.dockerignore                   docker构建时忽略的文件
    |---Dockerfile                      DockerFile构建文件
    |---README                          项目说明
    |---README_CN                       项目中文说明
    |---requirements.txt                项目运行需要的依赖


## 1、源码运行方式
>1.安装依赖,按顺序安装：
>>`pip install frozenlist-1.3.0-py3-none-any.whl`


>>`pip install multidict-6.0.2-py3-none-any.whl`


>>`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`


>2.运行程序：
>> `python app.py`


## 2、Docker运行方式（自己构建）
>1. 构建镜像
> `docker build -t cochat-api .`
>2. 运行容器
> `docker run -d -p 8000:8000 cochat-api`
>3. 可配置的环境变量如下
```text
#讯飞星火配置
-e SPARK_APPID=XXXX
-e SPARK_API_KEY=XXXX
-e SPARK_API_SECRET=XXXX
#通义千问配置
-e DASHSCOPE_API_KEY=XXXX
#面壁Luca(前端获取)
-e LUCA_ACCESS_TOKEN=XXXX
-e LUCA_CONVERSATION_ID=XXXX
#DeepSeek
-e DEEP_SEEK_API_KEY=XXXX
#MINIMAX
-e MINIMAX_API_KEY=XXXX
-e MINIMAX_GROUP_ID=XXXX
#LinkAI
-e LINK_AI_API_KEY=XXXX
#360智脑
-e ZHINAO_API_KEY=XXXX
#chatanywhere
-e CHATANYWHERE_API_KEY=XXXX
#gemini
-E GEMINI_API_KEY=XXXX
#baichuan
-E BAICHUAN_API_KEY=XXXX
```


## 3、Docker运行方式（用dockerhub上已有的镜像）
>1. 拉取镜像
> `docker pull johnsonschrodinger/cochat-api:latest`
>2. 配置环境变量，否则无法使用
> 参考上面的已知环境变量
>3. 运行容器
>`docker run -d -p 8888:8000 johnsonschrodinger/cochat-api:latest`


## 4、使用方法
整合各种常见的chat-api
1. 使用时首先调用 ip:port/api/login
获取JWT_TOKEN
```json
{"username":"admin","password":"admin"} 
```


2. 再根据JWT_TOKEN调用: ip:port/api/chat
Header加入：Authorization Bearer ${your JWT_TOKEN} 
```json
{ "model": "qwen-max", "messages": [ { "role": "user", "content": "你是什么模型" } ] }
```


3. 目前支持模型：
'gpt-3.5-turbo','gpt-3.5-turbo-0125', 'gpt-4', 'deepseek-chat', 'deepseek-coder','gpt-3.5-turbo-16k', 'gpt-4', 'wenxin', 'xunfei', 'luca', 'abab5.5-chat', 'abab5.5s-chat', 'abab6-chat' , 'qwen-max', 'qwen-max-1201', 'qwen-max-longcontext','spark'(讯飞星火，model同级可携带，version指定版本),'360gpt_s2_v9', '360gpt-pro'


## 联系方式
> QQ：506421453


> 邮箱：schrodingersfish@outlook.com


## 特别说明
> 本项目版权受法律保护，未经作者允许禁止传播
