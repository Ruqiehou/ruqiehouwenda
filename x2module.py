import asyncio
import requests
from typing import Optional

class YunX2:
    def __init__(self, qq: (int|str), api_password: str = 'CJSvUFcLdYYAWNIoKwII:RIoQVHZNaaBqYFunHlWA', model: str = 'spark-x'):
        self.messages = []
        self.data = {
            "model": model,
            "user": str(qq),
            "messages": self.messages
        }
        self.api_password = api_password
        self.url = "https://spark-api-open.xf-yun.com/x2/chat/completions"  # 修正后的 URL

    def add_user(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content
        })
        return self

    def add_system(self, content: str):
        self.messages.append({
            "role": "system",
            "content": content
        })
        return self

    async def call(self, content: str) -> Optional[str]:
        self.add_user(content)
        
        if len(self.messages) > 1000:
            self.messages = [self.messages[0]] + self.messages[-999:]
        
        self.data["messages"] = self.messages
        
        try:
            from functools import partial
            post_request = partial(
                requests.post,
                url=self.url,
                json=self.data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_password}'
                }
            )
            response = await asyncio.get_event_loop().run_in_executor(None, post_request)
            
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    return self._parse_error(response_data)
                return self._parse_success(response_data)
            return f"请求失败，状态码：{response.status_code}"
        
        except Exception as e:
            return f"处理错误：{str(e)}"
    
    def _parse_error(self, data):
        error_message = data.get("error", {}).get("message", "")
        return f"API 返回错误信息：{error_message}"

    def _parse_success(self, data):
        reply_content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return reply_content

