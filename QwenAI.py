from openai import OpenAI

class QwenClient:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.messages = [
            {
                "role": "system",
                "content": """无"""
            }
        ]
    
    def call(self, user_input):
        """发送请求并获取模型响应"""
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="qwen3.5-plus-2026-02-15" ,
            messages=self.messages
        )
        assistant_output = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_output})
        return assistant_output
    