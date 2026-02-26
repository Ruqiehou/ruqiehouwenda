class NumberToChinese:
    """
    将数字转换为中文读法的工具类
    支持整数、负数、小数，以及大数（最大支持36位数）
    """

    def __init__(self):
        self.digits = '零一二三四五六七八九'
        self.units = ['', '十', '百', '千']
        # 扩展大数单位以支持36位数
        self.big_units = ['', '万', '亿', '兆', '京', '垓', '秭', '穰', '沟', '涧', '正', '载']

    def convert(self, num):
        """
        主接口：将输入的数字（int/float/str）转为中文读法
        :param num: 用户输入的数字或数字字符串
        :return: 中文读法字符串
        """
        usernums = num  # 接收变量

        # 类型处理
        if isinstance(usernums, str):
            usernums = usernums.strip()
            if not usernums:
                raise ValueError("输入不能为空")
            
            # 检查是否为科学计数法
            if 'e' in usernums.lower():
                try:
                    # 先尝试转换为浮点数
                    num_float = float(usernums)
                    # 转换为字符串避免科学计数法
                    usernums = f"{num_float:.15f}".rstrip('0').rstrip('.')
                except ValueError:
                    raise ValueError("无效的数字格式")
            
            if '.' in usernums:
                return self._convert_float(usernums)
            else:
                try:
                    # 检查是否为有效整数
                    if not usernums.lstrip('-').lstrip('+').isdigit():
                        raise ValueError("无效的整数格式")
                    return self._convert_integer(usernums)
                except:
                    raise ValueError("无效的整数格式")

        elif isinstance(usernums, (int, float)):
            if isinstance(usernums, int):
                return self._convert_integer(str(usernums))
            else:
                # 将浮点数转换为字符串，避免科学计数法
                num_str = f"{usernums:.15f}".rstrip('0').rstrip('.')
                return self._convert_float(num_str)
        else:
            raise TypeError("输入类型不支持，请传入 int、float 或 str")

    def _convert_integer(self, num_str):
        """转换整数部分"""
        # 检查是否为负数
        if num_str.startswith('-'):
            return "负" + self._convert_positive_integer(num_str[1:])
        
        # 去除前导零
        num_str = num_str.lstrip('0')
        if not num_str:
            return "零"
            
        return self._convert_positive_integer(num_str)

    def _convert_float(self, num_str):
        """转换小数"""
        # 处理科学计数法
        if 'e' in num_str.lower():
            try:
                # 将科学计数法转换为普通小数
                num_float = float(num_str)
                # 转换为字符串，避免科学计数法表示
                num_str = f"{num_float:.15f}".rstrip('0').rstrip('.')
            except ValueError:
                raise ValueError("无效的科学计数法格式")
        
        if '.' in num_str:
            parts = num_str.split('.')
            integer_part = parts[0]
            decimal_part = parts[1]
            
            # 处理整数部分
            integer_chinese = self._convert_integer(integer_part)
            
            # 处理小数部分 - 只处理数字字符
            decimal_chinese = ''.join(self.digits[int(d)] for d in decimal_part if d.isdigit())
            return f"{integer_chinese}点{decimal_chinese}"
        else:
            return self._convert_integer(num_str)

    def _convert_positive_integer(self, num_str):
        """转换正整数（核心逻辑）"""
        if num_str == "0":
            return "零"

        # 检查数字长度是否超过支持范围
        if len(num_str) > 36:
            raise ValueError(f"数字过长，最大支持36位数，当前为{len(num_str)}位")

        result = ""
        group = 0
        # 从右向左每4位一组
        for i in range(len(num_str), 0, -4):
            start = max(0, i - 4)
            section_str = num_str[start:i]
            section_num = int(section_str) if section_str else 0

            if section_num != 0:
                section_chinese = self._convert_section(section_num)
                if group > 0:
                    section_chinese += self.big_units[group]
                result = section_chinese + result
            elif group > 0 and result:  # 当前段为0，但高位还有数
                if not result.startswith("零"):
                    result = "零" + result
                    
            group += 1

        # 特殊处理：10~19 的"十"前面不加"一"
        if result.startswith("一十"):
            result = result[1:]

        return result

    def _convert_section(self, n):
        """将 1~9999 的数字转为中文（不含单位如"万"）"""
        if n == 0:
            return "零"
            
        result = ""
        str_n = str(n)
        length = len(str_n)
        for i, digit in enumerate(str_n):
            d = int(digit)
            unit = self.units[length - i - 1]
            if d != 0:
                result += self.digits[d] + unit
            else:
                if result and result[-1] != "零":
                    result += "零"
        return result.rstrip("零")  # 去掉末尾多余的"零"


# ================= 使用示例 =================
if __name__ == "__main__":
    converter = NumberToChinese()
    
    # 提供多种测试用例，包括大数测试
    test_cases = [
        0, 1, 10, 11, 123, 1000, 1001, 1234, 10000,
        10001, 12345, 100000, 1234567, 123456789,
        1234567890, -1, -123, 3.14, 123.45, 0.123,
        # 大数测试
        "100000000000000000000000000000000000",  # 36位数
        "123456789012345678901234567890123456",  # 36位数
        "999999999999999999999999999999999999",  # 最大36位数
        "1000000000000000000000000000000000000",  # 37位数（应该报错）
    ]
    
    print("=== 预设测试用例 ===")
    for num in test_cases:
        try:
            result = converter.convert(num)
            print(f"{num} -> {result}")
        except Exception as e:
            print(f"{num} -> 错误: {e}")
    
    print("\n=== 用户输入测试 ===")
    while True:
        try:
            usernums = input("请输入一个数字（输入'q'退出）：")
            if usernums.lower() == 'q':
                break
            result = converter.convert(usernums)
            print(f"转换结果：{result}")
        except Exception as e:
            print(f"错误: {e}")