# cochat-api
## project name
> Integrate the interfaces of various APIs
## author
> SchrodingersFish
## version
> v1.0.0
## Project directory structure
   
    | --- big_model large model
    | --- Model object
    | --- Utils Toolkit
    | --- .env environment variables configuration file
    | --- .env.example configuration file for environment variables
    | --- .dockerignore files ignored during docker build
    | --- DockerFile DockerFile build file
    | --- README Project Description
    | --- README_CN project Chinese description
    | --- requirements.txt Dependencies required for project operation


## 1. How the source code runs
> 1. Install dependencies, install in order:
> > 'pip install frozen list - 1.3.0 - py3 - none - any.whl'


> > 'pip install multidict - 6.0.2 - py3 - none - any.whl'


> > 'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt'


> 2. Run the program:
> > 'Python app.py'


## 2. How Docker Runs (Build Yourself)
> 1. Build an image
> 'Docker build -t cochat-api.'
> 2. Run the container
> 'Docker run -d -p 8000:8000 cochat-api'
> 3. Configurable environment variables are as follows
"text
#iFLYTEK Spark configuration
-E SPARK_APPID = XXXX
-E SPARK_API_KEY = XXXX
-E SPARK_API_SECRET = XXXX
#Tongyi Qianwen configuration
-E DASHSCOPE_API_KEY = XXXX
#Wall Luca (front-end acquisition)
-E LUCA_ACCESS_TOKEN = XXXX
-E LUCA_CONVERSATION_ID = XXXX
#DeepSeek
-E DEEP_SEEK_API_KEY = XXXX
#MINIMAX
-E MINIMAX_API_KEY = XXXX
-E MINIMAX_GROUP_ID = XXXX
#LinkAI
-E LINK_AI_API_KEY = XXXX
#360 Brain
-E ZHINAO_API_KEY = XXXX
#chatanywhere
-E CHATANYWHERE_API_KEY = XXXX
#gemini
-E GEMINI_API_KEY=XXXX
#baichuan
-E BAICHUAN_API_KEY=XXXX
"..."


## 3. How Docker runs (using existing images on dockerhub)
> 1. Pull the mirror image
> 'Docker pull johnsonschrodinger/cochat-api: latest'
> 2. Configure environment variables, otherwise it cannot be used
> Refer to the known environment variables above
> 3. Run the container
> 'Docker run -d -p 8888:8000 johnsonschrodinger/cochat-api: latest'


## 4. How to use it
Integrate various common chat-APIs.
1. First call ip: port/api/login when using
Get JWT_TOKEN
"json
{"Username": "admin", "password": "admin"} 
"..."


2. Then call according to JWT_TOKEN: ip: port/api/chat
Header added: Authorization Bearer ${your JWT_TOKEN} 
"json
{"Model": "qwen-max", "messages ": [ { " role": "user", "content": "What model are you " } ] }
"..."


3. Current support models:
'Gpt-3.5-turbo ',' gpt-3.5-turbo-0125 ',' gpt-4 ',' deepseek-chat ',' deepseek-coder ',' gpt-3.5-turbo-16k ',' gpt-4 ',' wenxin ',' xunfei ',' luca ',' abab5.5-chat ',' abab5.5s-chat ',' abab6-chat ',' qwen-max ',' qwen-max-1201 ',' qwen-max-longcontext ',' spark ' (iFLYTEK Spark, model can be carried at the same level, version specified version),' 360gpt_s2_v9 ',' 360gpt-pro'


## contact information
> QQ: 506421453


> Email: schrodingersfish@outlook.com


## Special instructions
The copyright of this project is protected by law, and dissemination is prohibited without the author's permission
