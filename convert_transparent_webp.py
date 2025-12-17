#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
透明背景PNG转WebP脚本
保持抠图效果，不添加白色背景
"""

import os
from PIL import Image

def convert_transparent_png_to_webp(input_path, output_path, quality=85):
    """
    将带透明背景的PNG转换为WebP，保持透明效果
    
    Args:
        input_path: 输入PNG文件路径
        output_path: 输出WebP文件路径
        quality: WebP质量 (0-100)
    """
    try:
        with Image.open(input_path) as img:
            # 检查是否有透明通道
            if img.mode in ('RGBA', 'LA'):
                print(f"✅ 检测到透明背景: {os.path.basename(input_path)}")
                # 直接保存，保持透明通道
                img.save(output_path, 'WEBP', quality=quality, optimize=True, lossless=False)
            else:
                print(f"⚠️  无透明背景: {os.path.basename(input_path)}")
                # 转换为RGB并保存
                img = img.convert('RGB')
                img.save(output_path, 'WEBP', quality=quality, optimize=True)
            
            # 计算压缩比
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"   原始大小: {original_size/1024:.1f}KB")
            print(f"   压缩后: {compressed_size/1024:.1f}KB")
            print(f"   压缩比: {compression_ratio:.1f}%")
            print()
            
            return True
            
    except Exception as e:
        print(f"❌ 转换失败 {input_path}: {str(e)}")
        return False

def main():
    """主函数"""
    print("🔄 透明背景PNG转WebP工具")
    print("=" * 50)
    
    # 专门处理CALL ME.png
    input_file = "CALL ME.png"
    output_file = "CALL ME.webp"
    
    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        return
    
    print(f"📁 处理文件: {input_file}")
    print()
    
    # 转换文件
    if convert_transparent_png_to_webp(input_file, output_file, quality=85):
        print("=" * 50)
        print("🎉 转换完成!")
        print(f"✅ 文件: {input_file} -> {output_file}")
        print("📝 透明背景已保持")
        print()
        print("📝 下一步操作:")
        print("1. 检查转换后的WebP文件")
        print("2. 在浏览器中测试透明效果")
        print("3. 如果满意，可以删除原始PNG文件")
    else:
        print("❌ 转换失败")

if __name__ == "__main__":
    main() 