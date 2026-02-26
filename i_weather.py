import requests
import json
from typing import Dict, Optional

class WeatherClient:
    """
    天气查询客户端类
    """
    
    def __init__(self, base_url: str = "https://api.52vmy.cn/api/query/tian/three"):
        self.base_url = base_url
    
    def query_weather(self, city: str, info_type: str = "weather") -> Dict:
        """
        查询天气信息
        
        参数:
        city: 城市名称
        info_type: 信息类型
        
        返回:
        包含天气信息的字典
        """
        try:
            url = f"{self.base_url}?city={city}&type={info_type}"
            response = requests.get(url)
            response.raise_for_status()
            
            # 尝试解析JSON响应
            try:
                data = response.json()
                return {
                    "success": True,
                    "city": city,
                    "type": info_type,
                    "data": data
                }
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始文本
                return {
                    "success": True,
                    "city": city,
                    "type": info_type,
                    "data": response.text
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "city": city,
                "type": info_type,
                "error": str(e)
            }
    
    def get_current_weather(self, city: str) -> Dict:
        """获取当前天气"""
        return self.query_weather(city, "weather")
    
    def get_weather_forecast(self, city: str) -> Dict:
        """获取天气预报"""
        return self.query_weather(city, "forecast")

