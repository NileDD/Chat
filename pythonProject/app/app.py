from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time

# 替换为你实际的 API 密钥
api_key = "5fgTkOiV4YoGPtH1rR3DU87ck4VvMOxLIm1R5ZjFkoei0OwJKmnPnRlIrjFurZDEF"
client = OpenAI(api_key=api_key, base_url="https://api.stepfun.com/v1")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app)

# 初始化对话历史
messages = [
    {
        "role": "system",
        "content": "你是由阶跃星辰提供的AI聊天助手，你擅长中文，英文，以及多种其他语言的对话。在保证用户数据安全的前提下，你能对用户的问题和请求，作出快速和精准的回答。同时，你的回答和建议应该拒绝黄赌毒，暴力恐怖主义的内容",
    },
]


@app.route('/')
def index():
    return render_template('index.html')


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
    return jsonify({'response': response})


@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    global messages
    messages.append({"role": "user", "content": user_message})

    # 先发送一个初步响应
    emit('receive_message', {'response': 'AI is thinking...'}, broadcast=True)

    # 模拟处理时间并逐步发送响应
    for i in range(5):
        time.sleep(1)  # 模拟一些处理时间
        # 生成部分响应，这里简化为模拟
        partial_response = f'Part {i + 1} of response...'
        emit('receive_message', {'response': partial_response}, broadcast=True)

    # 获取完整响应
    completion = client.chat.completions.create(
        model="step-1-8k",
        messages=messages,
    )
    full_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": full_response})
    emit('receive_message', {'response': full_response}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, port=5003, allow_unsafe_werkzeug=True)