from ncatbot.plugin_system import filter_registry,NcatBotPlugin
from ncatbot.core import GroupMessage


import json,random,os
with open("plugins/rqhwenda/ans.json", "r", encoding="utf-8") as f:
    ans = json.load(f)


hmd=["qq id"]
gly=["qq id"]

class rqhwenda(NcatBotPlugin):
    name = "rqhwenda" # 插件名
    version = "0.1.0" # 插件版本
    dependencies = {}  # 依赖的其他插件和版本
   
    async def on_load(self):
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")

    
    @filter_registry.group_filter
    async def wenda_chaxun(self, msg: GroupMessage):
        qunxiaoxi="".join(seg.text for seg in msg.message.filter_text())
        qunid=msg.group_id
        with open("plugins/rqhwenda/ans.json", "r", encoding="utf-8") as f:
              ans = json.load(f)
                
        if any(key in qunxiaoxi for key in ans):   
            matched_key = next(key for key in shujiyuan if key in qunxiaoxi)
            await self.api.post_group_msg(qunid, text=shujiyuan[matched_key])  



    @filter_registry.group_filter
    async def wenda_xiugai(self, msg: GroupMessage):
        mm="".join(seg.text for seg in msg.message.filter_text())
        qwq=msg.group_id
        usr=msg.user_id

                
        if mm.startswith("问"):
            import re
            
            match = re.match(r"^问(.+?)答(.+)$", mm)
            if match:
                question, answer = match.groups()
                try:
                    # 修复1：使用更安全的文件操作模式
                    with open("plugins/rqhwenda/ans.json", "a+", encoding="utf-8") as f:  # 改为 a+ 模式
                        f.seek(0)  # 移动指针到文件开头
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            data = {}  
                            
                        data[question.strip()] = answer.strip()
                        f.seek(0)
                        f.truncate()  
                        json.dump(data, f, ensure_ascii=False, indent=4)     
                    await self.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答对添加成功喵～\n问：{question.strip()}\n答：{answer.strip()}")
                except Exception as e:
                    # 修复2：更详细的错误提示
                    err_msg = f"保存失败喵～错误类型: {type(e).__name__}, 详情: {str(e)}"
                    await self.api.post_group_msg(group_id=qwq, text=err_msg)
            else:
                    await self.api.post_group_msg(group_id=qwq, text="格式错误")
            
        elif mm.startswith("修改"):
            if usr in  gly:
                parts = mm[2:].split("答", 1)
                if len(parts) == 2:
                    old_question, new_answer = parts[0].strip(), parts[1].strip()
                    data = ans            
                    if old_question not in data:
                        await self.api.post_group_msg(qwq, text=f"没有找到问题『{old_question}』喵～")
                        return            
                    data[old_question] = new_answer
                    with open("plugins/rqhwenda/ans.json" + ".tmp", "w", encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                    os.replace("plugins/rqhwenda/ans.json" + ".tmp", "plugins/rqhwenda/ans.json")
                    await self.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答修改成功喵～\n问：{old_question}\n新回答：{new_answer}")  
                          
        elif mm.startswith("删问答"):
            if usr in gly :
                try:
                    with open("plugins/rqhwenda/ans.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if question in data:
                            del data[question]
                            with open("plugins/rqhwenda/ans.json", "w", encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                            await self.api.post_group_msg(qwq, text=f"问答已删除喵～\n问：{old_question.strip()}\n答：{new_answer.strip()}")
                        else:
                            await self.api.post_group_msg(qwq, text="未找到包含该问题的问答")
                except FileNotFoundError:
                            await self.api.post_group_msg(qwq, text="删除问答失败")
         
        elif mm.startswith("列出所有问答"):

            if usr in hmd:  
                await self.api.post_group_msg(group_id=msg.group_id, text="你没有权限查看问答")
                return
            elif usr not in hmd: 
                try:
                    with open("plugins/rqhwenda/ans.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    if not data:
                        await self.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")



                        return
                
                    qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in data.items()])
                    await self.api.post_group_msg(qwq, text=f"当前问答列表（共{len(data)}条）：\n{qa_list}")



                except FileNotFoundError:
                    await self.api.post_group_msg(qwq, text="问答文件不存在")
                except json.JSONDecodeError:
                    await self.api.post_group_msg(qwq, text="问答文件格式损坏")

        elif mm.startswith("列出部分问答"):
            if usr in hmd:
                await self.api.post_group_msg(qwq, text="你没有权限查看问答")
                return
                
            try:
                with open("plugins/rqhwenda/ans.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if not data:
                    await self.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")
                    return
                

                random_qa = random.sample(list(data.items()), min(10, len(data)))
                qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in random_qa])
                await self.api.post_group_msg(group_id=qwq, 
                    text=f"随机选取的问答：\n{qa_list}")
                
            except FileNotFoundError:
                await self.api.post_group_msg(qwq, text="问答文件不存在")

        elif mm.startswith("清空所有问答"):
            if usr in hmd: 
                await self.api.post_group_msg(group_id=qwq, text="你没有权限清空问答")
                return
            elif usr in gly:
                try:
                    with open("plugins/rqhwenda/ans.json", "w", encoding="utf-8") as f:
                        f.write("")
                    await self.api.post_group_msg(group_id=qwq, text="问答已清空")
                except FileNotFoundError:
                    await self.api.post_group_msg(group_id=qwq, text="清空问答失败")
            else:

                pass
