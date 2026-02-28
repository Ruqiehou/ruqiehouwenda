from ncatbot.plugin_system import filter_registry,NcatBotPlugin
from ncatbot.core import GroupMessage


import json,random,os,re
from threading import Lock


hmd=["12345556"]  # 黑名单用户ID列表（示例）
gly=["123456"]

class AnswerManager:
    """管理问答数据的类，提供线程安全的读写操作，分别管理精确和模糊问答"""
    def __init__(self, precise_file_path, fuzzy_file_path):
        self.precise_file_path = precise_file_path
        self.fuzzy_file_path = fuzzy_file_path
        self.lock = Lock()
        
    def load_precise_data(self):
        """安全地加载精确问答数据"""
        with self.lock:
            try:
                with open(self.precise_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data if isinstance(data, dict) else {}
            except FileNotFoundError:
                # 如果文件不存在，创建一个空的问答文件
                self.save_precise_data({})
                return {}
            except json.JSONDecodeError:
                # 如果文件格式错误，创建一个空的问答文件
                self.save_precise_data({})
                return {}
    
    def load_fuzzy_data(self):
        """安全地加载模糊问答数据"""
        with self.lock:
            try:
                with open(self.fuzzy_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data if isinstance(data, dict) else {}
            except FileNotFoundError:
                # 如果文件不存在，创建一个空的问答文件
                self.save_fuzzy_data({})
                return {}
            except json.JSONDecodeError:
                # 如果文件格式错误，创建一个空的问答文件
                self.save_fuzzy_data({})
                return {}
    
    def load_all_data(self):
        """加载所有问答数据（精确+模糊）"""
        precise_data = self.load_precise_data()
        fuzzy_data = self.load_fuzzy_data()
        # 合并两个字典，模糊数据覆盖精确数据同名键（如果存在）
        all_data = precise_data.copy()
        all_data.update(fuzzy_data)
        return all_data
    
    def save_precise_data(self, data):
        """安全地保存精确问答数据"""
        with self.lock:
            temp_file = self.precise_file_path + ".tmp"
            try:
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                os.replace(temp_file, self.precise_file_path)
                return True
            except Exception:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
    
    def save_fuzzy_data(self, data):
        """安全地保存模糊问答数据"""
        with self.lock:
            temp_file = self.fuzzy_file_path + ".tmp"
            try:
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                os.replace(temp_file, self.fuzzy_file_path)
                return True
            except Exception:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
    
    def add_precise_answer(self, question, answer):
        """添加精确问答对"""
        data = self.load_precise_data()
        data[question.strip()] = answer.strip()
        return self.save_precise_data(data)
    
    def add_fuzzy_answer(self, question, answer):
        """添加模糊问答对"""
        data = self.load_fuzzy_data()
        data[question.strip()] = answer.strip()
        return self.save_fuzzy_data(data)
    
    def add_normal_answer(self, question, answer):
        """添加普通问答对（默认到模糊文件）"""
        return self.add_fuzzy_answer(question, answer)
    
    def update_answer(self, question, new_answer):
        """更新问答对（先检查精确文件，再检查模糊文件）"""
        precise_data = self.load_precise_data()
        if question in precise_data:
            precise_data[question] = new_answer.strip()
            return self.save_precise_data(precise_data)
        
        fuzzy_data = self.load_fuzzy_data()
        if question in fuzzy_data:
            fuzzy_data[question] = new_answer.strip()
            return self.save_fuzzy_data(fuzzy_data)
        
        return False
    
    def delete_answer(self, question):
        """删除问答对（检查两个文件）"""
        deleted = False
        
        # 尝试从精确问答中删除
        precise_data = self.load_precise_data()
        if question in precise_data:
            del precise_data[question]
            self.save_precise_data(precise_data)
            deleted = True
        
        # 尝试从模糊问答中删除
        fuzzy_data = self.load_fuzzy_data()
        if question in fuzzy_data:
            del fuzzy_data[question]
            self.save_fuzzy_data(fuzzy_data)
            deleted = True
            
        return deleted
    
    def clear_all_answers(self):
        """清空所有问答"""
        precise_cleared = self.save_precise_data({})
        fuzzy_cleared = self.save_fuzzy_data({})
        return precise_cleared and fuzzy_cleared
    
    def search_precise(self, question):
        """精确匹配问题（只在精确问答文件中搜索）"""
        data = self.load_precise_data()
        if not question:
            return None
        # 先尝试完全匹配
        if question in data:
            return data[question]
        # 尝试去除首尾空白后匹配
        question_stripped = question.strip()
        if question_stripped in data:
            return data[question_stripped]
        # 尝试预处理后的匹配（用于处理多行文本和标点符号）
        question_processed = self._preprocess_text(question)
        # 在数据中寻找预处理后匹配的项
        for stored_question, answer in data.items():
            stored_processed = self._preprocess_text(stored_question)
            if question_processed == stored_processed:
                return answer
        return None
    
    def search_fuzzy(self, text):
        """模糊匹配问题，使用更智能的匹配算法（在模糊问答文件中搜索）"""
        data = self.load_fuzzy_data()
        if not text:
            return None
            
        text_lower = text.lower()
        # 预处理文本，标准化换行符和多余空白
        text_processed = self._preprocess_text(text_lower)
        best_match = None
        best_score = 0
        
        for question, answer in data.items():
            question_lower = question.lower()
            question_processed = self._preprocess_text(question_lower)
            
            # 计算匹配分数
            score = 0
            
            # 精确匹配加分（考虑预处理后的文本）
            if question_processed == text_processed or question_lower == text_lower:
                score += 100
            # 包含关系加分（问题包含于输入文本）
            elif question_processed in text_processed or question_lower in text_lower:
                score += 50 + len(question)  # 长度越长，相关性可能越高
            # 被包含关系加分（输入文本包含于问题）
            elif text_processed in question_processed or text_lower in question_lower:
                score += 30 + len(text)  # 长度越长，相关性可能越高
            # 文本片段匹配（支持包含文本段）
            elif self._has_common_substring(text_processed, question_processed, min_length=2):
                # 找到公共子串的长度
                common_len = self._get_longest_common_substring_length(text_processed, question_processed)
                score += common_len * 5  # 根据公共子串长度加分
            # 词语重叠度加分（使用预处理后的文本）
            else:
                # 检查词汇重叠程度
                text_words = set(text_processed.split())
                question_words = set(question_processed.split())
                common_words = text_words.intersection(question_words)
                if common_words:
                    overlap_ratio = len(common_words) / max(len(text_words), len(question_words))
                    score += int(overlap_ratio * 20)
            
            # 更新最佳匹配
            if score > best_score:
                best_score = score
                best_match = answer
        
        return best_match

    def _preprocess_text(self, text):
        """预处理文本，标准化换行符、标点符号和空白字符"""
        import re
        # 标准化换行符为单个空格
        text = re.sub(r'\n+', ' ', text)
        # 标准化多个连续空格为单个空格
        text = re.sub(r'\s+', ' ', text)
        # 移除首尾空白
        text = text.strip()
        return text

    def _has_common_substring(self, str1, str2, min_length=2):
        """检查两个字符串是否有公共子串"""
        for i in range(len(str1)):
            for j in range(i + min_length, len(str1) + 1):
                substring = str1[i:j]
                if substring in str2:
                    return True
        return False

    def _get_longest_common_substring_length(self, str1, str2):
        """获取两个字符串最长公共子串的长度"""
        m, n = len(str1), len(str2)
        # 创建二维数组存储长度
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        longest = 0
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    longest = max(longest, dp[i][j])
                else:
                    dp[i][j] = 0
        
        return longest


# 初始化问答管理器
answer_manager = AnswerManager("plugins/rqhwenda/precise_ans.json", "plugins/rqhwenda/fuzzy_ans.json")

class rqhwenda(NcatBotPlugin):
    name = "rqhwenda" # 插件名
    version = "0.5.0" # 插件版本 - 新增精确问/模糊问独立文件存储，改进查询和管理功能
    dependencies = {}  # 依赖的其他插件和版本
   
    async def on_load(self):
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")

    
    @filter_registry.group_filter
    async def wenda_chaxun(self, msg: GroupMessage):
        qunxiaoxi="".join(seg.text for seg in msg.message.filter_text())
        qunid=msg.group_id
        

        answer = answer_manager.search_precise(qunxiaoxi)
        if answer:
            await self.api.post_group_msg(qunid, text=answer)
        else:
            answer = answer_manager.search_fuzzy(qunxiaoxi)
            if answer:
                await self.api.post_group_msg(qunid, text=answer)  



    @filter_registry.group_filter
    async def wenda_help(self, msg: GroupMessage):
        """帮助命令"""
        qunxiaoxi = "".join(seg.text for seg in msg.message.filter_text()).strip()
        qunid = msg.group_id
        
        if qunxiaoxi in ["问答帮助"] and msg.user_id in gly:
            help_text = """
【问达问答插件使用说明】
• 精确问问题内容答答案内容 - 添加精确问答（管理员）
• 模糊问问题内容答答案内容 - 添加模糊问答（管理员
• 修改原问题答新答案 - 修改问答（管理员）
• 删问答问题内容 - 删除问答（检查两库都删除）（管理员）
• 列出所有问答 - 查看全部问答（合并精确库和模糊库）（非黑名单用户）
• 列出部分问答 - 随机查看部分问答（合并两库后随机）（非黑名单用户）
• 清空所有问答 - 清空全部问答（清空两库）（管理员）
• 问答帮助 - 显示此帮助信息
"""
            await self.api.post_group_msg(qunid, text=help_text)

    @filter_registry.group_filter
    async def wenda_xiugai(self, msg: GroupMessage):
        mm="".join(seg.text for seg in msg.message.filter_text())
        qwq=msg.group_id
        usr=msg.user_id

                
        
        
        if mm.startswith("模糊问"):
            if usr in hmd:
                await self.api.post_group_msg(qwq, text="黑名单不能添加问答对")
            elif usr in gly:
                match = re.match(r"^模糊问(.+?)答(.+)$", mm, re.DOTALL)
                if match:
                    question, answer = match.groups()
                    success = answer_manager.add_normal_answer(question, answer)
                    if success:
                        await self.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答对添加成功喵～\n问：{question.strip()}\n答：{answer.strip()}")
                    else:
                        await self.api.post_group_msg(group_id=qwq, text="保存失败喵～")
                else:
                    await self.api.post_group_msg(group_id=qwq, text="格式错误，正确格式：模糊问问题内容答答案内容")
                    
        elif mm.startswith("精确问"):
            if usr in hmd:
                await self.api.post_group_msg(qwq, text="黑名单不能添加问答对")
            elif usr in gly:
                match = re.match(r"^精确问(.+?)答(.+)$", mm, re.DOTALL)
                if match:
                    question, answer = match.groups()
                    success = answer_manager.add_precise_answer(question, answer)
                    if success:
                        await self.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 精确问答对添加成功喵～\n精确问：{question.strip()}\n答：{answer.strip()}")
                    else:
                        await self.api.post_group_msg(group_id=qwq, text="保存失败喵～")
                else:
                    await self.api.post_group_msg(group_id=qwq, text="格式错误，正确格式：精确问问题内容答答案内容")
       
        
       
            
        elif mm.startswith("修改"):
            if usr in gly:
                parts = mm[2:].split("答", 1)
                if len(parts) == 2:
                    old_question, new_answer = parts[0].strip(), parts[1].strip()
                    success = answer_manager.update_answer(old_question, new_answer)
                    if success:
                        await self.api.post_group_msg(qwq, text=f"ฅ^•ω•^ฅ 问答修改成功喵～\n问：{old_question}\n新回答：{new_answer}")  
                    else:
                        await self.api.post_group_msg(qwq, text=f"没有找到问题『{old_question}』喵～")
                          
        elif mm.startswith("删问答"):
            if usr in gly:
                question_to_delete = mm[3:].strip()  # 去掉"删问答"三个字，获取要删除的问题
                if not question_to_delete:
                    await self.api.post_group_msg(qwq, text="请指定要删除的问题，格式：删问答+问题内容")
                    return
                    
                success = answer_manager.delete_answer(question_to_delete)
                if success:
                    await self.api.post_group_msg(qwq, text=f"问答已删除喵～\n问：{question_to_delete.strip()}")
                else:
                    await self.api.post_group_msg(qwq, text="未找到该问题")
            else:
                await self.api.post_group_msg(qwq, text="你没有权限删除问答")
         
        elif mm.startswith("列出所有问答"):
            if usr in hmd:  
                await self.api.post_group_msg(group_id=msg.group_id, text="你没有权限查看问答")
                return
            
            data = answer_manager.load_all_data()
            if not data:
                await self.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")
                return
            
            qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in data.items()])
            await self.api.post_group_msg(qwq, text=f"当前问答列表（共{len(data)}条）：\n{qa_list}")

        elif mm.startswith("列出部分问答"):
            if usr in hmd:
                await self.api.post_group_msg(qwq, text="你没有权限查看问答")
                return
                
            data = answer_manager.load_all_data()
            if not data:
                await self.api.post_group_msg(group_id=qwq, text="还没有任何问答记录")
                return
            

            random_qa = random.sample(list(data.items()), min(10, len(data)))
            qa_list = "\n".join([f"问：{q}\n答：{a}" for q, a in random_qa])
            await self.api.post_group_msg(group_id=qwq, 
                text=f"随机选取的问答：\n{qa_list}")
                
        elif mm.startswith("清空所有问答"):
            if usr in hmd: 
                await self.api.post_group_msg(group_id=qwq, text="你没有权限清空问答")
                return
            elif usr in gly:
                success = answer_manager.clear_all_answers()
                if success:
                    await self.api.post_group_msg(group_id=qwq, text="问答已清空")
                else:
                    await self.api.post_group_msg(group_id=qwq, text="清空问答失败")
            else:
                pass