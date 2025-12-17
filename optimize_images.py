#!/usr/bin/env python3
"""
图片优化脚本
将大图片压缩到合理大小，提高加载速度
"""

import os
from PIL import Image
import glob

def optimize_image(input_path, output_path, max_size_mb=0.3, quality=85):
    """优化图片大小"""
    try:
        with Image.open(input_path) as img:
            # 获取原始文件大小
            original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            
            if original_size <= max_size_mb:
                print(f"✓ {os.path.basename(input_path)} 已经足够小 ({original_size:.2f}MB)")
                return
            
            # 如果图片太大，进行压缩
            if original_size > max_size_mb:
                # 计算压缩比例
                scale_factor = (max_size_mb / original_size) ** 0.5
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)
                
                # 调整图片大小
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存优化后的图片
                img_resized.save(output_path, 'WEBP', quality=quality, optimize=True)
                
                new_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"✓ {os.path.basename(input_path)}: {original_size:.2f}MB → {new_size:.2f}MB")
                
    except Exception as e:
        print(f"✗ 处理 {input_path} 时出错: {e}")

def main():
    """主函数"""
    print("开始优化图片...")
    
    # 查找所有webp文件
    webp_files = glob.glob("*.webp")
    
    for file_path in webp_files:
        # 跳过已经很小的文件
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        if file_size > 0.3:  # 只优化大于300KB的文件
            optimize_image(file_path, file_path, max_size_mb=0.3, quality=85)
        else:
            print(f"✓ {file_path} 已经足够小 ({file_size:.2f}MB)")
    
    print("图片优化完成！")

if __name__ == "__main__":
    main() 