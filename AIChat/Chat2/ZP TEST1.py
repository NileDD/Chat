import requests
import time

# 设置你的API密钥
api_key = '0e9a7ec2e8b4bdd87c980b95495db8cb.tTQOueweEpIxl2KY'

def generate_response(prompt):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"  # 智谱API的端点
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "glm-4-0520",  # 更新为正确的模型名称
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        response_json = response.json()

        # 根据实际的响应结构提取聊天回复
        if 'choices' in response_json and len(response_json['choices']) > 0:
            content = response_json['choices'][0]['message']['content']
            return content
        else:
            return "对不起，我遇到了一些问题。"
    except requests.exceptions.HTTPError as err:
        print(f"HTTP错误: {err}")
        print(f"响应内容: {response.text}")
        return None

def stream_response(content):
    """模拟流式输出"""
    for char in content:
        print(char, end='', flush=True)
        time.sleep(0.05)  # 调整输出速度，根据需要调整时间间隔

def chat():
    print("AI Chatbot: 你好！有什么我可以帮忙的吗？")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ['退出', 'exit', 'quit']:
            print("AI Chatbot: 再见！")
            break

        response = generate_response(user_input)
        if response:
            print("AI Chatbot: ", end='')
            stream_response(response)
            print()  # 打印换行符
        else:
            print("AI Chatbot: 对不起，我遇到了一些问题。")

if __name__ == "__main__":
    chat()