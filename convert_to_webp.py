#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PNG to WebP 批量转换脚本
用于优化网站图片大小，提升加载速度
"""

import os
import sys
from PIL import Image
import glob

def convert_png_to_webp(input_path, output_path, quality=85):
    """
    将PNG图片转换为WebP格式
    
    Args:
        input_path: 输入PNG文件路径
        output_path: 输出WebP文件路径
        quality: WebP质量 (0-100)
    """
    try:
        with Image.open(input_path) as img:
            # 转换为RGB模式（WebP不支持RGBA）
            if img.mode in ('RGBA', 'LA'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # 使用alpha通道作为mask
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为WebP格式
            img.save(output_path, 'WEBP', quality=quality, optimize=True)
            
            # 计算压缩比
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"✅ {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
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
    print("🔄 PNG to WebP 批量转换工具")
    print("=" * 50)
    
    # 获取当前目录下的所有PNG文件
    png_files = glob.glob("*.png")
    
    if not png_files:
        print("❌ 当前目录下没有找到PNG文件")
        return
    
    print(f"📁 找到 {len(png_files)} 个PNG文件")
    print()
    
    # 创建webp目录
    webp_dir = "webp"
    if not os.path.exists(webp_dir):
        os.makedirs(webp_dir)
        print(f"📂 创建目录: {webp_dir}")
    
    # 转换设置
    quality = 85  # WebP质量
    
    success_count = 0
    total_original_size = 0
    total_compressed_size = 0
    
    for png_file in png_files:
        # 生成WebP文件名
        webp_file = os.path.splitext(png_file)[0] + ".webp"
        webp_path = os.path.join(webp_dir, webp_file)
        
        # 转换文件
        if convert_png_to_webp(png_file, webp_path, quality):
            success_count += 1
            total_original_size += os.path.getsize(png_file)
            total_compressed_size += os.path.getsize(webp_path)
    
    # 显示总结
    print("=" * 50)
    print(f"🎉 转换完成!")
    print(f"✅ 成功转换: {success_count}/{len(png_files)} 个文件")
    print(f"📊 总原始大小: {total_original_size/1024/1024:.2f}MB")
    print(f"📊 总压缩后大小: {total_compressed_size/1024/1024:.2f}MB")
    print(f"📊 总体压缩比: {(1 - total_compressed_size/total_original_size)*100:.1f}%")
    print()
    print("📝 下一步操作:")
    print("1. 检查 webp/ 目录中的转换结果")
    print("2. 将WebP文件复制到项目根目录")
    print("3. 更新HTML文件中的图片引用")
    print("4. 删除或备份原始PNG文件")

if __name__ == "__main__":
    main() 