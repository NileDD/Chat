from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from openai import OpenAI
import time
import redis
import json

# 替换为你实际的 API 密钥
api_key = "5fgTkOiV4YoGPtH1rR3DU87ck4VvMOxLIm1R5ZjFkoei0OwJKmnPnRlIrjFurZDEF"
client = OpenAI(api_key=api_key, base_url="https://api.stepfun.com/v1")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
redis_chat_key = "chat_history"

# 加载对话历史
def load_messages_from_redis():
    try:
        data = redis_client.get(redis_chat_key)
        if data:
            return json.loads(data)
        else:
            return []
    except redis.exceptions.ResponseError:
        print("Error loading from Redis: WRONGTYPE Operation against a key holding the wrong kind of value")
        return []

# 保存对话历史
def save_messages_to_redis(messages):
    redis_client.set(redis_chat_key, json.dumps(messages))

messages = load_messages_from_redis()

@app.route('/')
def index():
    messages = [
        {'role': 'user', 'content': 'Hello'},
        {'role': 'ai', 'content': 'Hi there!'}
    ]
    return render_template('index.html', messages=json.dumps(messages))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    global messages
    messages.append({"role": "user", "content": user_message})
    completion = client.chat.completions.create(
        model="step-1-8k",
        messages=messages,
    )
    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    save_messages_to_redis(messages)
    return jsonify({'response': response})

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    global messages
    messages.append({"role": "user", "content": user_message})

    # 获取完整响应
    completion = client.chat.completions.create(
        model="step-1-8k",
        messages=messages,
    )
    full_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": full_response})
    save_messages_to_redis(messages)

    # 逐字发送响应
    for char in full_response:
        emit('receive_message', {'response': char}, broadcast=True)
        time.sleep(0.05)  # 调整发送速度

if __name__ == "__main__":
    socketio.run(app, port=5003, allow_unsafe_werkzeug=True)