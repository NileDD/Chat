from openai import OpenAI

# 替换为你实际的 API 密钥
api_key = "5fgTkOiV4YoGPtH1rR3DU87ck4VvMOxLIm1R5ZjFkoei0OwJKmnPnRlIrjFurZDEF"
client = OpenAI(api_key=api_key, base_url="https://api.stepfun.com/v1")

# 初始化对话历史
messages = [
    {
        "role": "system",
        "content": "你是由阶跃星辰提供的AI聊天助手，你擅长中文，英文，以及多种其他语言的对话。在保证用户数据安全的前提下，你能对用户的问题和请求，作出快速和精准的回答。同时，你的回答和建议应该拒绝黄赌毒，暴力恐怖主义的内容",
    },
]

def chat_with_ai(user_message):
    global messages
    messages.append({"role": "user", "content": user_message})
    completion = client.chat.completions.create(
        model="step-1-8k",
        messages=messages,
    )
    response = completion.choices[0].message.content
    print(f"AI: {response}")
    messages.append({"role": "assistant", "content": response})

# 交互式对话
print("开始聊天 (输入 '退出' 结束对话)")
while True:
    user_input = input("你: ")
    if user_input.lower() in ["退出", "exit", "quit"]:
        break
    chat_with_ai(user_input)