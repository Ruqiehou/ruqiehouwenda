import requests

class News60s:
    def __init__(self, token=None):
        """初始化60秒新闻API客户端"""
        self.api_url = "https://api.52vmy.cn/api/wl/60s/new"
        self.token = token
        self.headers = {}
        
        # 如果有token就加到请求头里
        if token:
            self.headers['Authorization'] = f'Bearer {token}'
    
    def get_news(self):
        """
        获取60秒新闻
        返回: 字典格式的新闻数据，失败返回None
        """
        try:
            # 发送GET请求
            response = requests.get(
                self.api_url,
                headers=self.headers,
                timeout=10
            )
            
            # 检查请求是否成功
            if response.status_code == 200:
                return response.json()  # 返回JSON数据
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")
            return None
    
    def set_token(self, token):
        """设置API token"""
        self.token = token
        self.headers['Authorization'] = f'Bearer {token}'
        print("Token设置成功")

    def save_to_file(self, data, filename="news.json"):
        """把新闻数据保存到文件"""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filename}")


# 使用示例
if __name__ == "__main__":
    # 1. 创建客户端（不传token就是普通模式）
    news_client = News60s()
    
    # 2. 获取新闻
    result = news_client.get_news()
    
    # 3. 处理结果
    if result:
        print("获取新闻成功！")
        print(f"数据格式: {type(result)}")
        
        # 打印数据（只打印前3项，避免太多输出）
        print("\n新闻数据预览:")
        for i, (key, value) in enumerate(list(result.items())[:3]):
            print(f"{key}: {value}")
        
        # 保存到文件
        news_client.save_to_file(result)
    else:
        print("获取新闻失败")
    
    # 如果有token可以这样设置
    # news_client.set_token("你的token")
    # 再调用 get_news() 就没有速率限制了