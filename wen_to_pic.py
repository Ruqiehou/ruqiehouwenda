#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉字转图片工具类 - 专为机器人优化
支持将汉字、英文字符等转换为图片
优化大段文本处理能力
"""

import os
import re
import time
import hashlib
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional, Union
from pathlib import Path


class ChineseToImageConverter:
    """
    汉字转图片转换器类 - 机器人专用优化版
    针对大段文本进行专门优化
    """
    
    def __init__(self, 
                 font_path: Optional[str] = None,
                 font_size: int = 36,
                 text_color: str = "#2E86AB",
                 background_color: str = "#F8F9FA",
                 image_size: Optional[Tuple[int, int]] = None,
                 padding: int = 20,
                 line_spacing: int = 10,
                 auto_adjust_size: bool = True,
                 max_width: int = 800,
                 max_height: int = 2000,
                 max_text_length: int = 2000):
        """
        初始化转换器 - 大段文本优化版
        
        Args:
            font_path: 字体文件路径
            font_size: 字体大小，默认36
            text_color: 文字颜色
            background_color: 背景颜色
            image_size: 固定图片尺寸
            padding: 内边距
            line_spacing: 行间距
            auto_adjust_size: 自动调整尺寸
            max_width: 最大宽度限制
            max_height: 最大高度限制
            max_text_length: 最大文本长度限制
        """
        self.font_size = font_size
        self.text_color = self._parse_color(text_color)
        self.background_color = self._parse_color(background_color)
        self.image_size = image_size
        self.padding = padding
        self.line_spacing = line_spacing
        self.auto_adjust_size = auto_adjust_size
        self.max_width = max_width
        self.max_height = max_height
        self.max_text_length = max_text_length
        
        # 加载字体
        self.font = self._load_font(font_path, font_size)
        
        # 性能优化：缓存字体度量信息
        self._font_metrics_cache = {}
    
    def _parse_color(self, color_str: str) -> Tuple[int, int, int]:
        """解析颜色字符串"""
        if color_str.startswith('#'):
            color_str = color_str.lstrip('#')
            if len(color_str) == 3:
                color_str = ''.join([c*2 for c in color_str])
            return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
        elif color_str.startswith('rgb'):
            match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color_str)
            if match:
                return tuple(int(x) for x in match.groups())
        return (0, 0, 0)  # 默认黑色
    
    def _load_font(self, font_path: Optional[str], font_size: int) -> ImageFont.FreeTypeFont:
        """加载字体 - 机器人专用优化"""
        try:
            # 优先尝试系统字体
            system_fonts = [
                "C:/Windows/Fonts/simhei.ttf",  # 黑体
                "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                "C:/Windows/Fonts/simsun.ttc",  # 宋体
            ]
            
            if font_path and os.path.exists(font_path):
                return ImageFont.truetype(font_path, font_size)
            
            # 尝试系统字体
            for font in system_fonts:
                if os.path.exists(font):
                    return ImageFont.truetype(font, font_size)
            
            # 使用PIL默认字体
            return ImageFont.load_default()
            
        except Exception as e:
            print(f"字体加载失败，使用默认字体: {e}")
            return ImageFont.load_default()
    
    def _get_text_bbox(self, text: str) -> Tuple[int, int, int, int]:
        """获取文本边界框，带缓存优化"""
        if text in self._font_metrics_cache:
            return self._font_metrics_cache[text]
        
        bbox = self.font.getbbox(text)
        self._font_metrics_cache[text] = bbox
        return bbox
    
    def _wrap_text_smart(self, text: str, max_width: int) -> List[str]:
        """智能文本换行处理 - 支持中英文混合"""
        if not self.font:
            return [text]
        
        lines = []
        current_line = ""
        words = []
        
        # 中文按字符分割，英文按单词分割
        for char in text:
            if char.isspace():
                if words:
                    current_line = ''.join(words)
                    words = []
                current_line += char
            elif ord(char) < 128:  # ASCII字符
                words.append(char)
            else:  # 中文字符
                if words:
                    current_line = ''.join(words)
                    words = []
                test_line = current_line + char
                bbox = self._get_text_bbox(test_line)
                test_width = bbox[2] - bbox[0]
                
                if test_width <= max_width - 2 * self.padding:
                    current_line = test_line
                else:
                    if current_line.strip():
                        lines.append(current_line.strip())
                    current_line = char
        
        # 处理剩余的英文单词
        if words:
            current_line = current_line + ''.join(words)
        
        # 处理最后一行
        if current_line.strip():
            lines.append(current_line.strip())
        
        return lines
    
    def _split_long_text(self, text: str) -> List[str]:
        """分割超长文本为多个段落"""
        if len(text) <= self.max_text_length:
            return [text]
        
        # 按段落分割
        paragraphs = re.split(r'[\n\r]+', text)
        result = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # 如果段落本身就很长，按句子分割
            if len(para) > self.max_text_length // 2:
                sentences = re.split(r'[。！？.!?]', para)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(current_chunk) + len(sentence) + 1 <= self.max_text_length:
                        if current_chunk:
                            current_chunk += "\n" + sentence
                        else:
                            current_chunk = sentence
                    else:
                        if current_chunk:
                            result.append(current_chunk)
                        current_chunk = sentence
            else:
                if len(current_chunk) + len(para) + 1 <= self.max_text_length:
                    if current_chunk:
                        current_chunk += "\n" + para
                    else:
                        current_chunk = para
                else:
                    if current_chunk:
                        result.append(current_chunk)
                    current_chunk = para
        
        if current_chunk:
            result.append(current_chunk)
        
        return result
    
    def _calculate_text_size(self, text: str) -> Tuple[int, int]:
        """计算文本所需尺寸 - 优化大段文本处理"""
        if not self.font:
            return (400, 200)  # 默认尺寸
        
        # 文本换行处理
        max_text_width = self.max_width - 2 * self.padding
        lines = self._wrap_text_smart(text, self.max_width)
        
        # 计算最大宽度和总高度
        max_width = 0
        total_height = 0
        
        for line in lines:
            bbox = self._get_text_bbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            
            max_width = max(max_width, line_width)
            total_height += line_height + self.line_spacing
        
        # 调整尺寸
        if lines:
            total_height -= self.line_spacing
        
        width = min(max_width + 2 * self.padding, self.max_width)
        height = min(total_height + 2 * self.padding, self.max_height)
        
        return (width, height)
    
    def convert_to_image(self, 
                        text: str, 
                        output_path: Optional[str] = None,
                        format: str = 'PNG') -> Image.Image:
        """
        将文本转换为图片 - 大段文本优化版
        
        Args:
            text: 要转换的文本
            output_path: 输出路径
            format: 图片格式
            
        Returns:
            PIL Image对象
        """
        if not text or not text.strip():
            raise ValueError("文本不能为空")
        
        # 限制文本长度
        if len(text) > self.max_text_length:
            text = text[:self.max_text_length] + "...(文本过长，已截断)"
        
        # 计算图片尺寸
        if self.auto_adjust_size or not self.image_size:
            image_size = self._calculate_text_size(text)
        else:
            image_size = self.image_size
        
        # 创建图片
        image = Image.new('RGB', image_size, self.background_color)
        draw = ImageDraw.Draw(image)
        
        # 文本换行
        lines = self._wrap_text_smart(text, image_size[0])
        y_position = self.padding
        
        for line in lines:
            if not line.strip():
                y_position += self.font_size + self.line_spacing
                continue
                
            bbox = self._get_text_bbox(line)
            line_height = bbox[3] - bbox[1]
            text_width = bbox[2] - bbox[0]
            
            # 水平居中
            x_position = (image_size[0] - text_width) // 2
            
            # 绘制文本
            draw.text((x_position, y_position), line, font=self.font, fill=self.text_color)
            
            # 更新y坐标
            y_position += line_height + self.line_spacing
        
        # 保存图片
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image.save(output_path, format=format, optimize=True)
        
        return image
    
    def convert_long_text(self, 
                         text: str, 
                         save_dir: str = "alphabet/picall",
                         max_pages: int = 5) -> List[str]:
        """
        转换超长文本为多张图片
        
        Args:
            text: 超长文本
            save_dir: 保存目录
            max_pages: 最大分页数
            
        Returns:
            图片文件路径列表
        """
        # 分割长文本
        text_chunks = self._split_long_text(text)
        
        # 限制最大分页数
        if len(text_chunks) > max_pages:
            text_chunks = text_chunks[:max_pages]
            text_chunks[-1] += f"\n...(还有{len(text_chunks) - max_pages}页未显示)"
        
        output_paths = []
        
        for i, chunk in enumerate(text_chunks):
            if not chunk.strip():
                continue
                
            # 生成唯一文件名
            timestamp = int(time.time())
            chunk_hash = hashlib.md5(chunk.encode('utf-8')).hexdigest()[:8]
            filename = f"text_page_{i+1}_{timestamp}_{chunk_hash}.png"
            output_path = os.path.join(save_dir, filename)
            
            try:
                # 为分页添加页码标识
                display_text = chunk
                if len(text_chunks) > 1:
                    display_text = f"第{i+1}页/{len(text_chunks)}页\n{chunk}"
                
                self.convert_to_image(display_text, output_path)
                output_paths.append(output_path)
            except Exception as e:
                print(f"分页转换失败: {e}")
        
        return output_paths
    
    def convert_for_bot(self, 
                       text: str, 
                       save_dir: str = "alphabet/picall") -> Union[str, List[str]]:
        """
        专为机器人设计的转换方法
        支持大段文本自动分页
        
        Args:
            text: 要转换的文本
            save_dir: 保存目录
            
        Returns:
            图片文件路径或路径列表
        """
        # 检查文本长度决定是否分页
        if len(text) > 500:  # 超过500字符自动分页
            return self.convert_long_text(text, save_dir)
        else:
            # 生成唯一文件名
            timestamp = int(time.time())
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
            filename = f"text_image_{timestamp}_{text_hash}.png"
            output_path = os.path.join(save_dir, filename)
            
            # 转换并保存
            self.convert_to_image(text, output_path)
            
            return output_path
    
    def batch_convert(self, 
                     texts: List[str], 
                     output_dir: str,
                     filename_prefix: str = "text") -> List[str]:
        """
        批量转换 - 大段文本优化版
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_paths = []
        
        for i, text in enumerate(texts):
            if not text.strip():
                continue
                
            # 安全文件名
            safe_text = re.sub(r'[^\w\-_\. ]', '_', text[:20])
            filename = f"{filename_prefix}_{i+1:03d}_{safe_text}.png"
            output_path = os.path.join(output_dir, filename)
            
            try:
                self.convert_to_image(text, output_path)
                output_paths.append(output_path)
            except Exception as e:
                print(f"转换失败 '{text}': {e}")
        
        return output_paths


# 快捷函数 - 机器人专用
def create_text_image(text: str, 
                     save_dir: str = "alphabet/picall",
                     **kwargs) -> Optional[Union[str, List[str]]]:
    """
    快捷函数：创建文本图片
    支持大段文本自动分页
    
    Args:
        text: 文本内容
        save_dir: 保存目录
        **kwargs: 转换器参数
        
    Returns:
        图片路径或路径列表
    """
    try:
        converter = ChineseToImageConverter(**kwargs)
        return converter.convert_for_bot(text, save_dir)
    except Exception as e:
        print(f"创建图片失败: {e}")
        return None


def main():
    """测试函数"""
    converter = ChineseToImageConverter()
    
    # 测试文本 - 包含大段文本
    test_texts = [
        "你好世界",
        "Hello World",
        "这是一段测试文本，用于验证汉字转图片功能",
        "机器人专用文本转图工具",
        "这是一段非常长的文本，用于测试大段文本的处理能力。" * 50
    ]
    
    for text in test_texts:
        try:
            result = converter.convert_for_bot(text)
            if isinstance(result, list):
                print(f"✓ 生成成功: {len(result)}张图片")
                for path in result:
                    print(f"  - {path}")
            else:
                print(f"✓ 生成成功: {result}")
        except Exception as e:
            print(f"✗ 生成失败: {e}")


if __name__ == "__main__":
    main()