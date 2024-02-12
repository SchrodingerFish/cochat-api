from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel, ValidationError

import big_model
from big_model.chatanywhere import get_response as anywhere
from big_model.zhinao import get_response as zhinao
from big_model.qianwen import get_response as qianwen
from big_model.minimax import get_response as minimax
from big_model.deepseek import get_response as deepseek
from big_model.spark import get_response as spark

from model.User import User

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'just for fun'  # 用于 JWT 加密的密钥

jwt = JWTManager(app)
CORS(app)

# 假设这是您的数据
data = {
    "1": {"name": "Alice", "age": 25},
    "2": {"name": "Bob", "age": 30}
}


# 用户身份验证
@app.route('/', methods=['GET'])
def index():
    return jsonify({"error": "请先登录"})


@app.route('/api/login', methods=['POST'])
@validate(body=User)
def login():
    user = request.json
    if user['username'] == 'admin' and user['password'] == 'admin':
        access_token = create_access_token(identity=user['username'])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    req = request.json
    if req['model'].lower() == 'gpt-3.5-turbo':
        response = big_model.chatanywhere.get_response(req)
        return jsonify(response)
    if req['model'].lower() == 'gpt-4':
        response = big_model.chatanywhere.get_response(req)
        return jsonify(response)
    if req['model'].lower() == '360gpt-pro':
        response = big_model.zhinao.get_response(req)
        return jsonify(response)
    if req['model'].lower() == 'spark':
        # 默认模型
        version = req.get('version')
        if version is None or version == '':
            req['version'] = 1
        response = big_model.spark.get_response(req)
        return jsonify(response)
    if req['model'].lower() in ['deepseek-chat', 'deepseek-coder']:
        response = big_model.deepseek.get_response(req)
        return jsonify(response)
    if req['model'].lower() in ['abab5.5-chat', 'abab5.5s-chat', 'abab6-chat']:
        response = big_model.minimax.get_response(req)
        return jsonify(response)
    if req['model'].lower() in ['qwen-max', 'qwen-max-1201', 'qwen-max-longcontext']:
        response = big_model.qianwen.get_response(req)
        return jsonify(response)
    else:
        return jsonify({"error": "模型不支持"}), 400


# 获取所有数据（需要身份验证）
@app.route('/api/data', methods=['GET'])
@jwt_required()
def get_data():
    return jsonify(data)


# 获取特定数据（需要身份验证）
@app.route('/api/data/<id>', methods=['GET'])
@jwt_required()
def get_specific_data(id):
    return jsonify(data.get(id, {"error": "Data not found"}))


# 添加数据（需要身份验证）
class NewData(BaseModel):
    id: str
    name: str
    age: int


@app.route('/api/data', methods=['POST'])
@jwt_required()
@validate(body=NewData)
def add_data():
    new_data = request.json
    data[new_data['id']] = {"name": new_data['name'], "age": new_data['age']}
    return jsonify({"message": "Data added successfully"})


# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500
