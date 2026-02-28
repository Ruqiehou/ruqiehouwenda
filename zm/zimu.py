#2025-12-11-17-54版本

from PIL import Image

# 修改顶部路径配置
import os
SOURCE_DIR = os.path.dirname(__file__)  # 当前文件所在目录（zm目录）

def image_a(image_name="image_a.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_a = Image.open(img_path)
    return img_a

def image_b(image_name="image_b.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_b = Image.open(img_path)
    return img_b

def image_c(image_name="image_c.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_c = Image.open(img_path)
    return img_c

def image_d(image_name="image_d.png"):  # 修正文件名
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_d = Image.open(img_path)
    return img_d

def image_e(image_name="image_e.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_e = Image.open(img_path)
    return img_e

def image_f(image_name="image_f.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_f = Image.open(img_path)
    return img_f

def image_g(image_name="image_g.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_g = Image.open(img_path)
    return img_g
   
def image_h(image_name="image_h.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_h = Image.open(img_path)
    return img_h

def image_i(image_name="image_i.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_i = Image.open(img_path)
    return img_i

def image_j(image_name="image_yj.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_j = Image.open(img_path)
    return img_j

def image_k(image_name="image_k.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_k = Image.open(img_path)
    return img_k

def image_l(image_name="image_l.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_l = Image.open(img_path)
    return img_l

def image_m(image_name="image_m.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_m = Image.open(img_path)
    return img_m
def image_n(image_name="image_n.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_n = Image.open(img_path)
    return img_n

def image_o(image_name="image_o.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_o = Image.open(img_path)
    return img_o

def image_p(image_name="image_p.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_p = Image.open(img_path)
    return img_p

def image_q(image_name="image_er.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_q = Image.open(img_path)
    return img_q
def image_r(image_name="image_r.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_r = Image.open(img_path)
    return img_r  
def image_s(image_name="image_s.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_s = Image.open(img_path)
    return img_s 

def image_t(image_name="image_t.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_t = Image.open(img_path)
    return img_t

def image_u(image_name="image_u.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_u = Image.open(img_path)
    return img_u

def image_v(image_name="image_vw.png"):  #
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_vw = Image.open(img_path)
    return img_vw

def image_w(image_name="image_vw.png"): 
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_vw = Image.open(img_path)
    return img_vw

def image_x(image_name="image_x.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_x = Image.open(img_path)
    return img_x

def image_y(image_name="image_yj.png"):  # 修正文件名从YJ改为y
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_yj = Image.open(img_path)
    return img_yj


def image_z(image_name="image_z.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_z = Image.open(img_path)
    return img_z


def image_ae(image_name="image_ae.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_ae = Image.open(img_path)
    return img_ae

def image_ie(image_name="image_ie.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_ie = Image.open(img_path)
    return img_ie

def image_oe(image_name="image_oe.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_oe = Image.open(img_path)
    return img_oe

def image_sh(image_name="image_sh.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_sh = Image.open(img_path)
    return img_sh

def image_gh(image_name="image_gh.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_gh = Image.open(img_path)
    return img_gh

def image_ch(image_name="image_ch.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_ch = Image.open(img_path)
    return img_ch

def image_cc(image_name="image_cc.png"):
    img_path = os.path.join(SOURCE_DIR, image_name)
    img_cc = Image.open(img_path)
    return img_cc



def create_space_placeholder(width, height):
    """
    创建空格占位符图片
    """
    space_img = Image.new('RGB', (width, height), (173, 216, 230))  
    return space_img

def parse_char_sequence(char_sequence):
    """
    智能解析字符序列，支持多字符组合、空格识别和复杂识别
    """
    result = []
    i = 0
    sequence_length = len(char_sequence)
    
    while i < sequence_length:
        # 检查空格
        if char_sequence[i] == ' ':
            result.append(' ')  # 空格标记
            i += 1
            continue
            
        # 检查双字符组合（优先级最高）
        if i + 1 < sequence_length:
            two_chars = char_sequence[i:i+2].lower()
            if two_chars in ['ie', 'ae', 'oe', 'er', 'sh', 'gh', 'ch', 'cc']:
                result.append(two_chars)
                i += 2
                continue
        
        # 检查单字符
        current_char = char_sequence[i].lower()
        if current_char in 'abcdefghijklmnopqrstuvwxyz':
            result.append(current_char)
            i += 1
            continue
        
        # 如果遇到无法识别的字符，跳过并记录警告
        print(f"警告: 跳过无法识别的字符 '{current_char}'")
        i += 1
    
    return result

def get_image_by_char(char):
    """
    改进的字符到图片映射，支持空格占位符
    """
    # 如果是空格，返回None，由组合函数处理
    if char == ' ':
        return None
    
    char = char.lower()
    
    # 特殊双字符组合
    special_combinations = {
        'ie': image_ie,
        'ae': image_ae,
        'oe': image_oe,
        'er': image_q,
        'sh': image_sh,
        'gh': image_gh,
        'ch': image_ch,
        'cc': image_cc
    }
    
    # 单字符映射
    single_char_mapping = {
        'a': image_a, 'b': image_b, 'c': image_c, 'd': image_d, 'e': image_e,
        'f': image_f, 'g': image_g, 'h': image_h, 'i': image_i, 'j': image_j,
        'k': image_k, 'l': image_l, 'm': image_m, 'n': image_n, 'o': image_o,
        'p': image_p, 'q': image_q, 'r': image_r, 's': image_s, 't': image_t,
        'u': image_u, 'v': image_v, 'w': image_w, 'x': image_x, 'y': image_y,
        'z': image_z
    }
    
    # 优先检查特殊组合
    if char in special_combinations:
        return special_combinations[char]()
    
    # 检查单字符
    if char in single_char_mapping:
        return single_char_mapping[char]()
    
    # 支持大写字母自动转换为小写
    if char.upper() in single_char_mapping:
        return single_char_mapping[char.upper()]()
    
    raise ValueError(f"无法识别的字符输入: '{char}'")

def combine_images(char_sequence):
    """
    改进的图片组合函数，支持换行显示，每行最多25个源图片
    """
    # 使用智能解析器处理输入序列
    parsed_chars = parse_char_sequence(char_sequence)
    
    if not parsed_chars:
        raise ValueError("输入序列中没有可识别的字符")
    
    # 获取每个字符对应的图片（空格返回None）
    images_and_spaces = []
    for char in parsed_chars:
        if char == ' ':
            images_and_spaces.append(None)  # 标记为空格
        else:
            images_and_spaces.append(get_image_by_char(char))
    
    # 获取所有非空格图片的尺寸用于计算
    valid_images = [img for img in images_and_spaces if img is not None]
    if not valid_images:
        raise ValueError("输入序列中没有有效的字符图片")
    
    widths, heights = zip(*(i.size for i in valid_images))
    max_height = max(heights)
    
    # 优化留白：上下各留最大高度的15%作为边距
    vertical_margin = int(max_height * 0.15)
    line_height = max_height + 2 * vertical_margin
    
    # 间隙宽度为最大高度的10%
    gap_width = max_height // 10
    
    # 空格宽度为最大高度的15%
    space_width = int(max_height * 0.15)
    
    # 添加首尾留白：左右各留最大高度的20%
    horizontal_margin = int(max_height * 0.20)
    
    # 计算每行的最大字符数（25个源图片）
    max_chars_per_line = 25
    
    # 计算每行的内容
    lines = []
    current_line = []
    current_char_count = 0
    
    for item in images_and_spaces:
        # 如果当前行已达到最大字符数，开始新行
        if current_char_count >= max_chars_per_line:
            lines.append(current_line)
            current_line = []
            current_char_count = 0
        
        current_line.append(item)
        if item is not None:  # 只计算非空格字符
            current_char_count += 1
    
    # 添加最后一行
    if current_line:
        lines.append(current_line)
    
    # 计算总宽度（取最宽的一行）
    max_line_width = 0
    for line in lines:
        line_width = horizontal_margin * 2
        for item in line:
            if item is None:  # 空格
                line_width += space_width
            else:  # 字符图片
                line_width += item.size[0]
            line_width += gap_width  # 每个元素后添加间隙
        line_width -= gap_width  # 最后一个元素后不需要间隙
        max_line_width = max(max_line_width, line_width)
    
    # 计算总高度（包括行间距）
    line_spacing = int(max_height * 0.10)  # 行间距为最大高度的10%
    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing
    
    # 创建组合图片
    combined_image = Image.new('RGB', (max_line_width, total_height), (251, 255, 255))
    
    # 逐行绘制
    current_y = 0
    for line in lines:
        current_x = horizontal_margin
        
        # 绘制当前行的所有元素
        for item in line:
            if item is None:  # 空格占位符
                # 创建空格占位符
                space_img = create_space_placeholder(space_width, max_height)
                y_offset = current_y + (line_height - space_img.size[1]) // 2
                combined_image.paste(space_img, (current_x, y_offset))
                current_x += space_width + gap_width
            else:  # 字符图片
                y_offset = current_y + (line_height - item.size[1]) // 2
                combined_image.paste(item, (current_x, y_offset))
                current_x += item.size[0] + gap_width
        
        # 移动到下一行
        current_y += line_height + line_spacing
    
    return combined_image

def generate_combined_image(char_sequence: str) -> bool:
    """
    改进的图片生成函数，支持更复杂的输入
    """
    try:
        # 验证输入
        if not char_sequence or not char_sequence.strip():
            print("错误: 输入序列为空")
            return False
            
        combined_img = combine_images(char_sequence)
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alphabet/picall")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{char_sequence}.png")
        combined_img.save(save_path)
        print(f"成功生成图片: {save_path}")
        return True
    except Exception as e:
        print(f"生成失败: {str(e)}")
        return False

def generate_image(text: str, save_path: str) -> bool:
    # 实现具体的图片生成逻辑
    # 返回 True 表示成功，False 表示失败
    # 示例伪代码：
    from PIL import Image, ImageDraw
    try:
        img = Image.new('RGB', (400, 200), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), text, fill=(255,255,0))
        img.save(save_path)
        return True
    except:
        return False

def main():
    """命令行交互模式"""
    while True:
        input_sequence = input("请输入单词形式（支持空格和换行，每行最多25个字符）：")
        if generate_combined_image(input_sequence):
            print("图片生成成功！")
        else:
            print("图片生成失败。")

if __name__ == "__main__":
    main()
