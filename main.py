# -*- coding: utf-8 -*-
from ncatbot.core import BotClient,GroupMessageEvent,PrivateMessageEvent,MessageArray
from ncatbot.utils import config

config.set_bot_uin(bot_uin="3899129921") 
config.set_root(root="265478608")  
config.set_ws_uri(ws_uri="ws://localhost:3001") 
config.set_ws_token(ws_token="1212//.././1/.2/1.98898989***(*(/=0==0=0=0=0====9-080-80-0-ojoju9jojopjopj.1")  

# 基础配置（示例）
bot = BotClient()

import json,random,os,aiohttp,datetime
from urllib.parse import quote
from x2module import YunX2
from yunlite import Yunlite
from yunpro128 import Yunpro128
from number_to_chinese import NumberToChinese
from ipis import query_ip_info       
from i_weather import WeatherClient 
from i_news import News60s
from wen_to_pic import ChineseToImageConverter  
from yonghu_system import *
from QwenAI import QwenClient
        
#001智能主程序
message_counter = 0
with open ("csys.json",'r',encoding='utf-8') as f:
     fortunes=json.load(f)
with open ("danci.json",'r',encoding='utf-8') as f:
     dictionary=json.load(f)
with open ("help.md",'r',encoding='utf-8') as f:
     help=f.read()
     helptext=str(help)

hmd=[]
xzqun=["673906569"]
ANS_FILE="ans.json"   
@bot.on_group_message()
async def main_qunliao(event: GroupMessageEvent):
    xiaoxi="".join(seg.text for seg in event.message.filter_text())
    ruqiehou=["2654278608"]
    if "测试" in xiaoxi:
        if event.user_id in ruqiehou:    
            await bot.api.post_private_msg(user_id=2654278608, text="测试成功")
        else:
            pass

    elif xiaoxi.startswith("，"):
        content1 = xiaoxi.strip()  # 去掉命令前缀 
        yun = Yunlite(qq=event.user_id)
        try:
            # 调用 Yun 实例以获取回复
            response1 = await yun.call(content1)
            # 发送回复到群聊
            await bot.api.post_group_msg(group_id=event.group_id, text=response1)
        except Exception as e:
            await bot.api.post_group_msg(group_id=event.group_id, text="出错，请稍后再试。")

    elif xiaoxi.startswith("。"):
        content2 = xiaoxi.strip()  # 去掉命令前缀
        yun2 = Yunpro128(qq=event.user_id)
        try:
            # 调用 Yun 实例以获取回复
            response2 = await yun2.call(content2)
            # 发送回复到群聊
            await bot.api.post_group_msg(group_id=event.group_id, text=response2)
        except Exception as e:
           
            await bot.api.post_group_msg(group_id=event.group_id, text="出错，请稍后再试。")
  
    elif xiaoxi.startswith("q"):
        user_input=xiaoxi[1:]

        chatbot = QwenClient(
            api_key="sk-ee8a9e07615a4f9ead58e6f5bc59606c",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        assistant_output = chatbot.call(user_input)
        await bot.api.post_group_msg(group_id=event.group_id, text=assistant_output)

    elif "运势" in xiaoxi:
        image_dir = "tup"
        if os.path.exists(image_dir) and os.path.isdir(image_dir):
              images = [f for f in os.listdir(image_dir) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
              if images:
                selected_image = random.choice(images)
                image_path = os.path.join(image_dir, selected_image)
              msg= MessageArray().add_text(fortunes[random.randint(0, len(fortunes)-1)]).add_image(image_path)
       
              await bot.api.post_group_array_msg(group_id=event.group_id, msg=msg)

        else:
            await bot.api.post_group_msg(group_id=event.group_id, text="暂无运势图片")

    elif "随机图" in xiaoxi:
                image_dir = "tup"
                if os.path.exists(image_dir) and os.path.isdir(image_dir):
                    images = [f for f in os.listdir(image_dir) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    if images:
                       selected_image = random.choice(images)
                       image_path = os.path.join(image_dir, selected_image)
                       twhp=MessageArray().add_image(image_path).add_text("这是一张随机图片")
                await bot.api.post_group_array_msg(group_id=event.group_id, msg=twhp)

    elif "图文" in xiaoxi:
                image_dir = "tup"
                if os.path.exists(image_dir) and os.path.isdir(image_dir):
                    images = [f for f in os.listdir(image_dir) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    if images:
                       selected_image = random.choice(images)
                       image_path = os.path.join(image_dir, selected_image)
                # 从Yun模型获取文字
                yun = Yunlite(qq=event.user_id)
                text_content = await yun.call("随机句子")  # 或其他适当的调用方式
                
                # 发送图文消息
                message =  MessageArray().add_text(text_content).add_image(image_path)
                await bot.api.post_group_array_msg(group_id=event.group_id, msg=message)
    
    elif "正查" in xiaoxi:
       word = xiaoxi.strip()[2:]             
       if word in dictionary:
            definition = dictionary[word]
            await bot.api.post_group_msg(group_id=event.group_id, text=f"{word} 是：{definition}")
       else:
            await bot.api.post_group_msg(group_id=event.group_id, text=f"抱歉，没有找到 {word} 。")

    elif "反查" in xiaoxi:
        definition = xiaoxi.strip()[2:]  
        words = [word for word, defn in dictionary.items() if defn == definition]
        if words:
            word_list = ", ".join(words)
            await bot.api.post_group_msg(group_id=event.group_id, text=f"{definition} 可能是以下单词的意思：{word_list}")
        else:
            await bot.api.post_group_msg(group_id=event.group_id, text=f"抱歉，没有找到 {definition} 的单词。")

    elif "粗查" in xiaoxi:
      keyword = xiaoxi.strip()[2:]
      matching_words = [word for word in dictionary.keys() if keyword in word]
      if matching_words:
            # 生成带有序号的列表
            numbered_list = '\n'.join([f'{i+1}. {word}' for i, word in enumerate(matching_words)])
            
            # 添加结果统计和分隔线
            response = f"🔍 找到 {len(matching_words)} 个包含【{keyword}】的单词：\n{numbered_list}\n\n════════════════"
            await bot.api.post_group_msg(group_id=event.group_id, text=response)
      else:
            await bot.api.post_group_msg(group_id=event.group_id, 
                text=f"⚠️ 未找到包含【{keyword}】的单词，建议：\n1. 检查拼写\n2. 尝试简写形式\n3. 换相似关键词"
            )
   
    elif "发图" in xiaoxi:
        try:
            # 提取字符序列（例如 "发图hello" -> "hello"）
            char_sequence = "".join(seg.text for seg in event.message.filter_text()).strip()[2:]
            if not char_sequence:
                await bot.api.post_group_msg(
                    group_id=event.group_id,
                    text="请输入要生成的字符序列"
                )
                return

            # 修改为调用正确的生成函数
            from zm.zimu import combine_images

            # 统一保存路径（与 zimu.py 保持一致）
            save_dir = os.path.join(os.path.dirname(__file__), "zm/saves")
            os.makedirs(save_dir, exist_ok=True)
            image_path = os.path.join(save_dir, f"{char_sequence}.png")

            # 直接生成最新图片（覆盖旧版本）
            try:
                # 使用组合图片生成函数
                combined_img = combine_images(char_sequence)
                combined_img.save(image_path)
            except ValueError as e:
                await bot.api.post_group_msg(
                    group_id=event.group_id,
                    text=f"输入包含无效字符：{str(e)}"
                )
                return
            except Exception as e:
                await bot.api.post_group_msg(
                    group_id=event.group_id,
                    text=f"图片生成失败: {str(e)}"
                )

            
            # Send using post_group_file with image parameter
            await bot.api.send_group_image(
                group_id=event.group_id,
                image=os.path.abspath(image_path)  # Use absolute path
            )
            
        except Exception as e:
                await bot.api.post_group_msg(group_id=event.group_id, text=f"图片发送失败: {str(e)}")

    elif "爬" in xiaoxi:
        title = xiaoxi.strip()[2:]
        if not title:
            return
            
        try:
            api_url = "http://wiki.tucm.top/api.php"
            params = {
                "action": "query",
                "prop": "extracts|info",
                "explaintext": "true",
                "titles": title,
                "format": "json",
                "utf8": "true",
                "inprop": "url"  # 新增参数获取页面信息
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params) as response:
                    if response.status != 200:
                        await bot.api.post_group_msg(group_id=event.group_id, text=f"请求失败，状态码：{response.status}")
                        return
                        
                    data = await response.json()
                    pages = data.get("query", {}).get("pages", {})
                    page_id = next(iter(pages))
                    
                    if page_id == "-1":
                        await bot.api.post_group_msg(group_id=event.group_id, text=f"未找到与「{title}」相关的维基条目")
                        return
                        
                    page_data = pages[page_id]
                    extract = page_data.get("extract", "暂无内容")
                    
                    # 从API获取真实页面名称
                    canonical_title = page_data.get("title", title)
                    # 生成完整页面链接
                    page_link = f"http://wiki.tucm.top/index.php/{quote(canonical_title)}" 
                    
                    await bot.api.post_group_msg(
                        group_id=event.group_id,
                        text=f"【{canonical_title}】\n{extract}\n\n" 
                        f"完整页面：{page_link}"
                    )
                    
        except Exception as e:
            await bot.api.post_group_msg(group_id=event.group_id, text=f"爬取失败: {str(e)}")
            await bot.api.post_group_msg(group_id=event.group_id, text=f"查询「{title}」时发生错误")
             
    elif "打卡" in xiaoxi:
        await bot.api.set_group_sign(group_id=event.group_id)

    elif "赞我" in xiaoxi:
        await bot.api.send_like(user_id=event.user_id,times=10)

    elif "戳我" in xiaoxi:
        await bot.api.send_poke(group_id=event.group_id,user_id=event.user_id)

    elif xiaoxi.startswith("伴随打卡"):
        if event.user_id==ruqiehou:     
            try:
                await bot.api.set_group_sign(group_id=event.group_id)
                
                group_file_path = f"groups/group_{event.group_id}.json"
                os.makedirs("groups", exist_ok=True)
                
                # 初始化默认配置
                group_data = {'group_id': event.group_id, 'send_group_sign': False}
                
                # 如果文件存在，则更新配置
                if os.path.exists(group_file_path):
                    try:
                        with open(group_file_path, 'r', encoding='utf-8') as f:
                            loaded_data = json.load(f)
                            group_data.update(loaded_data)  # 合并加载的配置
                    except (json.JSONDecodeError, IOError):
                        # 处理文件读取错误，保持使用默认配置
                        pass
                else:
                    # 文件不存在时创建
                    os.makedirs(os.path.dirname(group_file_path), exist_ok=True)
                    with open(group_file_path, 'w', encoding='utf-8') as f:
                        json.dump(group_data, f, ensure_ascii=False, indent=2)
                
                # 发送通知的条件判断
                if group_data.get('send_group_sign', False):
                    await bot.api.post_private_msg(user_id=2654278608, msg=MessageArray().add_text("打卡成功"))
                    
            except Exception as e:
                print(f"打卡操作失败: {e}")
        else:
            pass
            
    elif xiaoxi=="指南":
        await bot.api.post_group_msg(group_id=event.group_id, text=helptext)
    
    elif xiaoxi.startswith("踢人") and event.user_id==ruqiehou:
        if xiaoxi[3:] in xzqun:
            pass
        else:
            jp_user_id = xiaoxi[3:]
            await bot.api.set_group_kick(group_id=event.group_id,user_id=jp_user_id)
        
    elif xiaoxi.startswith("上管") :
        if event.user_id==ruqiehou:     
            xgly_user_id=xiaoxi[3:]
            await bot.api.set_group_admin(group_id=event.group_id,user_id=xgly_user_id,enable=True)
    
    elif xiaoxi.startswith("下管") :
        if event.user_id==ruqiehou:     
            ygly_user_id=xiaoxi[3:]
            await bot.api.set_group_admin(group_id=event.group_id,user_id=ygly_user_id,enable=False)
        else:
            pass

    elif xiaoxi.startswith("改头衔"):
        aim_title=xiaoxi[4:]
        await bot.api.set_group_special_title(group_id=event.group_id,user_id=event.user_id,special_title=aim_title)
    
    elif xiaoxi.startswith("转写"):
        aim_num=float(xiaoxi[3:])
        converter=NumberToChinese()
        qqq=converter.convert(aim_num)
        await bot.api.post_group_msg(group_id=event.group_id, text=f"{aim_num} 转写为 {qqq}")

    elif xiaoxi.startswith("定位"):
        aim_addr=xiaoxi[3:]
        ip_address=str(aim_addr)
        ipcx=query_ip_info(ip_address)
        await bot.api.post_group_msg(group_id=event.group_id, text=f"定位 {aim_addr}\n{ipcx}")

    elif xiaoxi.startswith("天气"):
        aim_city=xiaoxi[3:]
        weather_client = WeatherClient()
        current_weather = weather_client.get_current_weather(aim_city)
        await bot.api.post_group_msg(group_id=event.group_id, text=f"{aim_city} 当前天气:\n{current_weather}")

    elif xiaoxi==("新闻"):
        news_client = News60s()
        result = news_client.get_news()
        if result:
            await bot.api.post_group_msg(group_id=event.group_id, text=f"获取新闻成功！\n{result}")
        else:
            await bot.api.post_group_msg(group_id=event.group_id, text="获取新闻失败")

    elif xiaoxi.startswith("转图"):
        aim_text = xiaoxi[3:].strip()

        # 检查文本是否为空
        if not aim_text:
            await bot.api.post_group_msg(group_id=event.group_id, text="请输入要转换的文本，格式：转图 文本内容")
            return

        try:
            # 创建转换器实例 - 优化大段文本处理
            converter = ChineseToImageConverter(
                font_size=32,  # 稍小字体以适应更多文本
                text_color="#2E86AB",  # 蓝色文字
                background_color="#F8F9FA",  # 浅灰色背景
                padding=15,
                line_spacing=8,
                max_width=600,  # 限制宽度
                max_height=1200,  # 限制高度
                max_text_length=2000  # 最大文本长度
            )
            
            # 使用优化后的转换方法，支持大段文本分页
            result = converter.convert_for_bot(aim_text, "alphabet/picall")
            
            if isinstance(result, list):
                # 多张图片（分页）
                if len(result) > 5:
                    await bot.api.post_group_msg(group_id=event.group_id, 
                                                text=f"文本过长，已生成前5页图片（共{len(result)}页）")
                    result = result[:5]  # 限制最多5页
                
                # 发送第一张图片
                first_image_path = result[0]
                message_chain = MessageArray().add_text(f"文本转图成功！共{len(result)}页").add_image(first_image_path)
                await bot.api.post_group_array_msg(group_id=event.group_id, msg=message_chain)
                
                # 如果有更多页，延迟发送后续图片
                if len(result) > 1:
                    import asyncio
                    for i, image_path in enumerate(result[1:], 2):
                        await asyncio.sleep(1)  # 延迟1秒发送下一张
                        page_message = MessageArray().add_text(f"第{i}页").add_image(image_path)
                        await bot.api.post_group_array_msg(group_id=event.group_id, msg=page_message)
            else:
                # 单张图片
                message_chain = MessageArray().add_text("文本转图成功！").add_image(result)
                await bot.api.post_group_array_msg(group_id=event.group_id, msg=message_chain)
            
        except Exception as e:
            error_msg = f"转图失败：{str(e)}"
            await bot.api.post_group_msg(group_id=event.group_id, text=error_msg)

    elif xiaoxi.startswith("聚合"):
        shuruci=xiaoxi[3:]
        a1=Yunlite(qq=event.user_id)
        a11= await a1.call(shuruci)
        a111=str(a11)
        a2=Yunpro128(qq=event.user_id)
        a22= await a2.call(shuruci)
        a222=str(a22)
        
        
        
        # 最基础的合并转发功能
        forward_messages = [
            {"type": "node", "data": {"name": "system", "uin": "3899129921", "content": a111}},
            {"type": "node", "data": {"name": "system", "uin": "3899129921", "content": a222}},
        ]
        
        await bot.api.send_group_forward_msg(
            group_id=event.group_id,
            messages=forward_messages,
            news=[],  # 空的新闻列表
            prompt="AI聚合回复",  # 空提示
            summary="合并转发",  # 摘要
            source=""  # 来源
        )

#002 用户系统
with open('point_shop.json', 'r', encoding='utf-8') as f:
     point_shop_items = json.load(f)
@bot.on_group_message()
async def user_qiandao_fayan_point (msg:GroupMessageEvent):  
        user_id = msg.user_id
        group_id = msg.group_id
        message = "".join(seg.text for seg in msg.message.filter_text()).strip()
        await update_user_message_count(user_id)

        # 读取用户数据
        user_data = {}
        data_file = f"yonghudata/user_{user_id}.json"
        database_path="yonghudata"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        
        # 初始化用户数据
        if 'points' not in user_data:
            user_data['points'] = 0
        if 'last_sign_in' not in user_data:
            user_data['last_sign_in'] = ''
        if 'status' not in user_data:
            user_data['status'] = '初来乍到'  
        if 'message_count' not in user_data:
            user_data['message_count'] = 0 
        
        if message == "签到":
         
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            if user_data['last_sign_in'] == today:
                await bot.api.post_group_msg(group_id=group_id, text="你今天已经签到过了")
            else: 
                suiji=random.randint(88,100000000)
                user_data['points'] += suiji  
                user_data['last_sign_in'] = today
            
                os.makedirs('yonghudata', exist_ok=True)
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(data_file), exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)            
                await bot.api.post_group_msg(group_id=group_id, text=f"签到成功！获得{suiji}积分，当前积分：{user_data['points']}\n你的发言次数：{user_data['message_count']}条")
        
        elif message == "用户帮助":
            user_help_text="""签到帮助：
            1 发送「签到」来签到
            2 发送「我的信息」来查询签到信息
            3 发送「签到帮助」来获取帮助信息
            4 发送「积分排行」来查看积分排行榜
            5 发送「积分商城」查看可兑换商品
            6 发送「兑换+商品编号」兑换商品
            7 发送「扣分」来开始积分对打
            8 发送「我的积分」来查询当前积分
            9 发送「我的发言」来查询当前发言次数

            """
            await bot.api.post_group_msg(group_id=group_id, text=user_help_text)

        elif message == "我的积分":
            await bot.api.post_group_msg(group_id=group_id, text=f"你当前的积分是：{user_data['points']}")
        
        elif message == "我的信息":
            await bot.api.post_group_msg(group_id=group_id, text=f"你当前的积分是：{user_data['points']}\n你当前的状态是：{user_data['status']}\n上次签到时间：{user_data['last_sign_in']}\n你的发言：{user_data['message_count']}条")  
        
        elif message == "积分排行":   
            all_user_data = get_all_user_data()
            sorted_users = sorted(all_user_data.items(), key=lambda x: x[1], reverse=True)
            if sorted_users:
                rank_message = "🏆 积分排行榜 🏆\n"
                for i, (user_id, points) in enumerate(sorted_users[:25]):  # 只显示前10名
                    rank_message += f"{i+1}. 用户{user_id}: {points}分\n"
                await bot.api.post_group_msg(group_id=group_id, text=rank_message)
            else:
                await bot.api.post_group_msg(group_id=group_id, text="暂无用户数据")
          
        elif message == "积分商城":
            shop_message = "🏪 积分商城 🏪\n\n"
            for item_id, item_info in point_shop_items.items():
                shop_message += f"{item_id}. {item_info['name']} - {item_info['price']}积分\n   {item_info['description']}\n\n"
            shop_message += "发送「兑换+商品编号」来兑换商品，例如：兑换1"
            await bot.api.post_group_msg(group_id=group_id, text=shop_message)
               
        elif message.startswith("兑换"):
            
            item_id = message[2:].strip()  # 获取商品编号
            
            # 检查商品是否存在
            if item_id not in point_shop_items:
                await bot.api.post_group_msg(group_id=group_id, text="无效的商品编号，请检查后重试")
                return
            
            item = point_shop_items[item_id]
            item_name = item["name"]
            item_price = item["price"]
            
            # 检查积分是否足够
            if user_data.get('points', 0) < item_price:
                await bot.api.post_group_msg(group_id=group_id, text=f"积分不足，当前积分：{user_data['points']}，所需积分：{item_price}")
                return
            
            # 根据商品编号执行不同的兑换逻辑
            if item_id == "1":  # 随机图片
                image_dir = "tup"
                if os.path.exists(image_dir) and os.path.isdir(image_dir):
                    images = [f for f in os.listdir(image_dir) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    if images:
                        selected = random.choice(images)
                        file_path = os.path.join(image_dir, selected)
                        user_data['points'] -= item_price
                        # 确保目录存在并安全写入文件
                        os.makedirs(os.path.dirname(data_file), exist_ok=True)
                        with open(data_file, 'w', encoding='utf-8') as f:
                            json.dump(user_data, f, ensure_ascii=False, indent=2)

                        message=MessageArray().add_image(file_path).add_text(f"兑换成功！这是你的{item_name}，剩余积分：{user_data['points']}")
                        await bot.api.post_group_msg(group_id=group_id, rtf=message)
                    else:
                        # 如果没有图片，退还积分
                        user_data['points'] += item_price
                        # 确保目录存在并安全写入文件
                        os.makedirs(os.path.dirname(data_file), exist_ok=True)
                        with open(data_file, 'w', encoding='utf-8') as f:
                            json.dump(user_data, f, ensure_ascii=False, indent=2)
                        await bot.api.post_group_msg(group_id=group_id, rtf=MessageArray().add_text("兑换失败，图库空空如也，积分已退还"))
            
            elif item_id == "2":  # 专属称号（从dic.json的键中随机选择）
                # 从dic.json的键中随机选择一个作为称号
                titles = list(dictionary.keys())
                if titles:
                    title = random.choice(titles)
                    # 将获得的称号设置为用户状态
                    user_data['status'] = title
                    # 保存用户数据
                    user_data['points'] -= item_price
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)
                
                    await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！恭喜获得「{title}」称号，剩余积分：{user_data['points']}，当前状态：{user_data['status']}")
                else:
                    # 如果没有可选称号，退还积分
                    user_data['points'] += item_price
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，暂无可选称号，积分已退还")

            elif item_id == "3":  # 运势查询
                # 直接调用已有的运势功能
                fortune = fortunes[random.randint(0, len(fortunes)-1)]
                user_data['points'] -= item_price
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(data_file), exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)
                await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！你的今日运势是：{fortune}，剩余积分：{user_data['points']}")
            
            elif item_id == "4":  # 高级称号
                # 从dic.json的键中随机选择一个作为高级称号
                titles = list(dictionary.keys())
                if titles:
                    title = random.choice(titles)
                    # 将获得的称号设置为用户状态
                    user_data['status'] = title
                    user_data['points'] -= item_price

                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)

                    await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！恭喜获得高级称号「{title}」，剩余积分：{user_data['points']}，当前状态：{user_data['status']}")

                
            elif item_id == "5":  # 豪华礼包
                if group_id in xzqun:
                    await bot.api.post_group_msg(group_id=group_id, text="本群不开放")
                else:
                    bonus_points = random.randint(1000000, 50000222120)
                    user_data['points'] += bonus_points
                    # 保存用户数据
                    user_data['points'] -= item_price
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)

                    await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！获得豪华礼包：{bonus_points}积分奖励，当前积分：{user_data['points']}")

            elif item_id == "6":  # 普通礼包
                # 生成随机积分奖励
                bonus_points = random.randint(1000, 50000)
                user_data['points'] += bonus_points
                # 保存用户数据
                user_data['points'] -= item_price
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(data_file), exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)

                await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！获得普通礼包：{bonus_points}积分奖励，当前积分：{user_data['points']}")

            elif item_id == "7":  # 随机减少一位用户的积分
                # 获取所有用户数据
                all_user_data = get_all_user_data()
                other_users = {uid: points for uid, points in all_user_data.items() if uid != str(user_id)}
                
                if not other_users:
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，没有其他用户可减少积分")
                    return
                    
                # 随机选择一个用户
                target_user_id = random.choice(list(other_users.keys()))
                
                # 读取目标用户的数据
                target_data_file = f"yonghudata/user_{target_user_id}.json"  # 修正路径
                target_user_data = {}
                if os.path.exists(target_data_file):
                    with open(target_data_file, 'r', encoding='utf-8') as f:
                        target_user_data = json.load(f)
                else:
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，目标用户数据不存在")
                    return
                
                # 随机生成要减少的积分（1-100000）
                reduced_points = random.randint(1, 10000000)
                
                # 确保不会将目标用户的积分减到负数
                if target_user_data.get('points', 0) >= reduced_points:
                    target_user_data['points'] -= reduced_points
                else:
                    reduced_points = target_user_data.get('points', 0)
                    target_user_data['points'] = 0
                
                # 保存目标用户的数据
                os.makedirs(os.path.dirname(target_data_file), exist_ok=True)  # 确保目录存在
                with open(target_data_file, 'w', encoding='utf-8') as f:
                    json.dump(target_user_data, f, ensure_ascii=False, indent=2)
                
                # 保存当前用户的数据
                user_data['points'] -= item_price
                os.makedirs(os.path.dirname(data_file), exist_ok=True)  # 确保目录存在
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)
                
                await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！随机选择了用户{target_user_id}，减少了{reduced_points}积分，aim user {target_user_id}的剩余积分：{target_user_data['points']},你的剩余积分：{user_data['points']}")

            elif item_id == "8":  # 随机增加一位用户的积分

                # 获取所有用户数据
                all_user_data = get_all_user_data()
                other_users = {uid: points for uid, points in all_user_data.items() if uid != str(user_id)}
                
                if not other_users:
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，没有其他用户可增加积分")
                    return
                    
                # 随机选择一个用户
                target_user_id = random.choice(list(other_users.keys()))
                # 读取目标用户的数据
                target_data_file = f"yonghudata/user_{target_user_id}.json"  # 修正路径
                target_user_data = {}
                if os.path.exists(target_data_file):
                    with open(target_data_file, 'r', encoding='utf-8') as f:
                        target_user_data = json.load(f)
                else:
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，目标用户数据不存在")
                    return
                
                #aim user
                increased_points = random.randint(1999, 1000000)
                target_user_data['points'] += increased_points
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(target_data_file), exist_ok=True)
                with open(target_data_file, 'w', encoding='utf-8') as f:
                    json.dump(target_user_data, f, ensure_ascii=False, indent=2)


                #self user
                user_data['points'] -= item_price
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(data_file), exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)

                await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！随机选择了用户{target_user_id}，增加了{increased_points}积分，用户{target_user_id}的剩余积分：{target_user_data['points']},你的的剩余积分：{user_data['points']}")
        
            elif item_id =="9" : # 随机清零一位用户的积分
                all_user_data = get_all_user_data()
                
                # 排除当前用户
                other_users = {uid: points for uid, points in all_user_data.items() if uid != str(user_id)}
                
                if not other_users:
                    # 如果没有其他用户，退还积分
                    user_data['points'] += item_price
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，没有其他用户可清零积分，积分已退还")
                    return
                
                # 随机选择一个用户
                target_user_id = random.choice(list(other_users.keys()))
                
                # 读取目标用户的数据
                target_data_file = f"yonghudata/user_{target_user_id}.json"  # 修正路径
                target_user_data = {}
                if os.path.exists(target_data_file):
                    with open(target_data_file, 'r', encoding='utf-8') as f:
                        target_user_data = json.load(f)
                else:
                    # 如果目标用户数据不存在，退还积分
                    user_data['points'] += item_price
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(data_file), exist_ok=True)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)
                    await bot.api.post_group_msg(group_id=group_id, text="兑换失败，目标用户数据不存在，积分已退还")
                    return
                
                # 清零积分
                target_user_data['points'] = 0
                
                # 保存目标用户的数据
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(target_data_file), exist_ok=True)
                with open(target_data_file, 'w', encoding='utf-8') as f:
                    json.dump(target_user_data, f, ensure_ascii=False, indent=2)
                
                # 保存当前用户的数据
                user_data['points'] -= item_price
                # 确保目录存在并安全写入文件
                os.makedirs(os.path.dirname(data_file), exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)
                
                await bot.api.post_group_msg(group_id=group_id, text=f"兑换成功！随机选择了用户{target_user_id}，积分已清零，你的剩余积分：{user_data['points']}")   
           
        elif message == "我的发言": 
            count = await get_user_message_count(user_id)
            await bot.api.post_group_msg(group_id=group_id, text=f"您总共发言了 {count} 次")
    
        elif message == "发言排行":
            rankings = await get_message_rankings()
            if rankings:
                ranking_text = "🏆 发言排行 🏆\n"
                for i, (uid, count) in enumerate(rankings[:10]):  
                    medal = ""
                    if i == 0:
                        medal = "🥇"
                    elif i == 1:
                        medal = "🥈"
                    elif i == 2:
                        medal = "🥉"
                    ranking_text += f"{medal}{i+1}. 用户{uid}: {count}次\n"
                ranking_text += "\n统计所有用户的发言次数"
                await bot.api.post_group_msg(group_id=group_id, text=ranking_text)
            else:
                await bot.api.post_group_msg(group_id=group_id, text="暂无发言记录")
        
        elif message.startswith("查发言"):   
            target_user = message[3:].strip() 
            if target_user.isdigit():
                count = await get_user_message_count(int(target_user))
                await bot.api.post_group_msg(group_id=group_id, text=f"用户 {target_user} 总共发言了 {count} 次")
            else:
                await bot.api.post_group_msg(group_id=group_id, text="请输入正确的用户ID")

        elif message=="数据重置":       
            for filename in os.listdir(database_path):
                if filename.startswith("user_") and filename.endswith(".json"):
                    user_id = filename[5:-5]  # 提取用户ID
                    database_file = os.path.join(database_path, filename)
                    try:
                        # 使用with语句确保文件正确关闭
                        # 确保目录存在并安全写入文件
                        os.makedirs(os.path.dirname(database_file), exist_ok=True)
                        with open(database_file, 'w', encoding='utf-8') as f:
                            json.dump({}, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        print(f"重置文件错误 (文件 {filename}): {e}")
                        continue
            await bot.api.post_private_msg(user_id=2654278608, text=f"所有用户的数据已重置")

#003问答系统
with open(ANS_FILE, "r", encoding="utf-8") as f:
    ans = json.load(f)
@bot.on_group_message()
async def wenda_chaxun(event: GroupMessageEvent):
    qunxiaoxi="".join(seg.text for seg in event.message.filter_text())
    qunid=event.group_id
    with open(ANS_FILE, "r", encoding="utf-8") as f:
        ans = json.load(f)
    matched_key = next((key for key in ans if key in qunxiaoxi), None)
    if matched_key:
        await bot.api.post_group_msg(qunid, text=ans[matched_key])

@bot.on_group_message()
async def wenda_xiugai(event: GroupMessageEvent):
    mm="".join(seg.text for seg in event.message.filter_text())
    qwq=event.group_id
    usr=event.user_id
    ruqiehou=["2654278608"]     
    if mm.startswith("问"):
        import re
        if usr in hmd: 
            await bot.api.post_group_msg(qwq, text="你没有权限")
        else:    
           match = re.match(r"^问(.+?)答(.+)$", mm)
           if match:
             question, answer = match.groups()
             try:
                 # 修复1：使用更安全的文件操作模式
                with open("ans.json", "a+", encoding="utf-8") as f:  # 改为 a+ 模式
                    f.seek(0)  # 移动指针到文件开头
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}  
                        
                    data[question.strip()] = answer.strip()
                    f.seek(0)
                    f.truncate()  
                    json.dump(data, f, ensure_ascii=False, indent=4)     
                await bot.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答对添加成功喵～\n问：{question.strip()}\n答：{answer.strip()}")
             except Exception as e:
                # 修复2：更详细的错误提示
                err_msg = f"保存失败喵～错误类型: {type(e).__name__}, 详情: {str(e)}"
                await bot.api.post_group_msg(group_id=qwq, text=err_msg)
           else:
                await bot.api.post_group_msg(group_id=qwq, text="格式错误")
        
    elif mm.startswith("修改"):
        if usr in ruqiehou:
            parts = mm[2:].split("答", 1)
            if len(parts) == 2:
                 old_question, new_answer = parts[0].strip(), parts[1].strip()

                 with open(ANS_FILE, "r", encoding="utf-8") as f:
                      data = json.load(f)            
                 if old_question not in data:
                      await bot.api.post_group_msg(qwq, text=f"没有找到问题『{old_question}』喵～")
                      return            
                 data[old_question] = new_answer
                 # 确保目录存在并安全写入文件
                 os.makedirs(os.path.dirname(ANS_FILE), exist_ok=True)
                 with open(ANS_FILE + ".tmp", "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                 os.replace(ANS_FILE + ".tmp", ANS_FILE)
                 await bot.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答修改成功喵～\n问：{old_question}\n新回答：{new_answer}")    
             
    elif mm.startswith("删问答"):
      if usr in ruqiehou:
          try:
            with open(ANS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if question in data:
                    del data[question]
                    # 确保目录存在并安全写入文件
                    os.makedirs(os.path.dirname(ANS_FILE), exist_ok=True)
                    with open(ANS_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    await bot.api.post_group_msg(qwq, text=f"问答已删除喵～\n问：{question.strip()}\n答：{answer.strip()}")
                else:
                    await bot.api.post_group_msg(qwq, text="未找到包含该问题的问答")
          except FileNotFoundError:
                    await bot.api.post_group_msg(qwq, text="删除问答失败")
       
    elif mm.startswith("列出所有问答"):

        if usr in hmd:  
             await bot.api.post_group_msg(group_id=qwq, text="你没有权限查看问答")
             return
        elif usr in ruqiehou: 
            try:
                with open(ANS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if not data:
                    await bot.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")

                    return
            
                qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in data.items()])
                await bot.api.post_group_msg(qwq, text=f"当前问答列表（共{len(data)}条）：\n{qa_list}")



            except FileNotFoundError:
                await bot.api.post_group_msg(qwq, text="问答文件不存在")
            except json.JSONDecodeError:
                await bot.api.post_group_msg(qwq, text="问答文件格式损坏")

    elif mm.startswith("列出部分问答"):
        if usr in hmd:
            await bot.api.post_group_msg(qwq, text="你没有权限查看问答")
            return
            
        try:
            with open(ANS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if not data:
                await bot.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")
                return
            

            random_qa = random.sample(list(data.items()), min(10, len(data)))
            qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in random_qa])
            await bot.api.post_group_msg(group_id=qwq, 
                text=f"随机选取的问答：\n{qa_list}")
            
        except FileNotFoundError:
            await bot.api.post_group_msg(qwq, text="问答文件不存在")

    elif mm.startswith("清空所有问答"):
        if usr in hmd: 
             await bot.api.post_group_msg(group_id=qwq, text="你没有权限清空问答")
             return
        elif usr in ruqiehou:
            try:
                 # 确保目录存在并安全写入文件
                 os.makedirs(os.path.dirname(ANS_FILE), exist_ok=True)
                 with open(ANS_FILE, "w", encoding="utf-8") as f:
                    f.write("")
                 await bot.api.post_group_msg(group_id=qwq, text="问答已清空")
            except FileNotFoundError:
                await bot.api.post_group_msg(group_id=qwq, text="清空问答失败")
        else:
            pass

#004私信指令
@bot.on_private_message()
async def houtaiguanli(event: PrivateMessageEvent):
    xiaoxi="".join(seg.text for seg in event.message.filter_text())
    if xiaoxi.startswith("，"):
        content = xiaoxi.strip()  # 去掉命令前缀 
        yun = Yunlite(qq=event.user_id)
        try:
            # 调用 Yun 实例以获取回复
            response = await yun.call(content)
            await bot.api.post_private_msg(user_id=event.user_id, text=response)
        except Exception as e:
            await bot.api.post_private_msg(user_id=event.user_id, text="处理消息时出错，请稍后再试。")

    elif xiaoxi.startswith("x"):
        content4 = xiaoxi[1:]  # 去掉命令前缀    
        x2 = YunX2(qq=event.user_id)
        try:
            # 调用实例以获取回复
            response4 = await x2.call(content4)
            # 发送回复到群聊
            await bot.api.post_private_msg(user_id=event.user_id, text=response4)
        except Exception as e:
            await bot.api.post_private_msg(user_id=event.user_id, text="处理消息时出错，请稍后再试。")

    else:
        help_text = """
        可用指令：
        ，[问题] - 调用Yunlite模型回答问题
        x[问题] - 调用YunX2模型回答问题
        """
        await bot.api.post_private_msg(user_id=event.user_id, text=help_text)

@bot.on_group_message()
async def handle_group_message(msg: GroupMessageEvent):
    global message_counter
    xiaoxi="".join(seg.text for seg in msg.message.filter_text())   
    if not xiaoxi.strip():
        return
    
    message_counter += 1
    print(f"收到群消息: {xiaoxi}, 计数器: {message_counter}")
    
    if message_counter % 3 == 0:
        yun222 = Yunlite(qq=msg.user_id)
        
        reply_prompt = f"""你是一个活泼可爱的群聊机器人，正在参与群聊讨论。

用户消息：{xiaoxi}

请给出一个自然、仿真人的回复。要求：
1. 语气轻松活泼，像群里的普通成员一样
2. 可以适当使用表情符号或网络用语
3. 回复要简洁，不要太长
4. 如果是问题，直接回答；如果是闲聊，自然参与
5. 不要说"我是机器人"或"作为AI"之类的话
6. 回复要口语化，不要太正式

请直接给出回复内容，不要有任何其他说明。"""
        
        try:
            reply = await yun222.call(reply_prompt)
            print(f"生成的回复: {reply}")
            await bot.api.post_group_msg(group_id=msg.group_id, text=reply)
        except Exception as e:
            print(f"生成回复错误: {e}")
            
bot.run_frontend(debug=True)