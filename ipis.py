import urllib.request
import urllib.parse
import sys


def query_ip_info(ip_address):
    """
    查询IP信息的函数
    """
    try:
        # 构造API URL
        base_url = "https://api.52vmy.cn/api/query/itad/pro?ip="
        url = base_url + urllib.parse.quote(ip_address)

        # 发送请求并获取响应
        response = urllib.request.urlopen(url)

        # 读取并返回响应内容
        result = response.read().decode('utf-8')
        return result

    except Exception as e:
        return f"Error: {str(e)}"


