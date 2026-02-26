import os
import json
import random
import datetime


# 获取所有用户数据
def get_all_user_data():
    user_data_dict = {}
    data_dir = "yonghudata"
    
    if not os.path.exists(data_dir):
        return user_data_dict
    
    for filename in os.listdir(data_dir):
        if filename.startswith("user_") and filename.endswith(".json"):
            user_id = filename[5:-5]  # 提取用户ID
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    user_data_dict[user_id] = user_data.get('points', 0)
            except Exception as e:
                print(f"读取用户数据失败 {filename}: {e}")
    
    return user_data_dict

async def update_user_data(user_id, user_data):
    """更新用户数据到文件"""
    file_path = f"yonghudata/user_{user_id}.json"
    # 确保目录存在并安全写入文件
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

async def update_user_message_count(user_id):
    """更新用户发言次数"""
    data_file = f"yonghudata/user_{user_id}.json"
    user_data = {}
    
    # 读取用户数据
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 (用户 {user_id}): {e}")
            # 创建新的用户数据
            user_data = {}
    
    # 初始化用户数据字段
    if 'points' not in user_data:
        user_data['points'] = 0
    if 'last_sign_in' not in user_data:
        user_data['last_sign_in'] = ''
    if 'status' not in user_data:
        user_data['status'] = '初来乍到'
    if 'message_count' not in user_data:
        user_data['message_count'] = 0
    
    # 增加发言计数
    user_data['message_count'] += random.randint(99, 999)
    
    #发言送积分 
    user_data['points'] += random.randint(999, 10099)

    # 保存用户数据
    # 确保目录存在并安全写入文件
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

async def get_user_message_count(user_id):
    """获取用户发言次数"""
    data_file = f"yonghudata/user_{user_id}.json"
    
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            return user_data.get('message_count', 0)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 (用户 {user_id}): {e}")
            return 0
    return 0

async def get_message_rankings():
    """获取用户发言排行榜"""
    rankings = []
    data_dir = "yonghudata"
    
    # 检查目录是否存在
    if not os.path.exists(data_dir):
        return rankings
    
    # 一次性读取所有文件，减少I/O操作
    for filename in os.listdir(data_dir):
        if filename.startswith("user_") and filename.endswith(".json"):
            user_id = filename[5:-5]  # 提取用户ID
            data_file = os.path.join(data_dir, filename)
            
            try:
                # 使用with语句确保文件正确关闭
                with open(data_file, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    count = user_data.get('message_count', 0)
                    if count > 0:  # 只统计有发言的用户
                        rankings.append((user_id, count))
            except json.JSONDecodeError as e:
                print(f"JSON解析错误 (文件 {filename}): {e}")
                # 出错时跳过该文件，继续处理其他文件
                continue
            except Exception as e:
                print(f"读取文件错误 (文件 {filename}): {e}")
                continue
    
    # 按发言次数排序
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings