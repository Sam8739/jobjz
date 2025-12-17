#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件中的图片引用
将PNG图片引用更新为WebP格式
"""

import os
import re
import glob

def update_html_file(file_path):
    """
    更新HTML文件中的图片引用
    
    Args:
        file_path: HTML文件路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原始内容
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 替换PNG引用为WebP
        # 匹配 src="./图片名.png" 或 src="图片名.png"
        pattern = r'src=(["\'])([^"\']*\.png)\1'
        
        def replace_png_with_webp(match):
            quote = match.group(1)
            png_path = match.group(2)
            
            # 生成WebP路径
            webp_path = png_path.replace('.png', '.webp')
            
            # 检查WebP文件是否存在
            if os.path.exists(webp_path):
                return f'src={quote}{webp_path}{quote}'
            else:
                print(f"⚠️  WebP文件不存在: {webp_path}")
                return match.group(0)  # 保持原样
        
        updated_content = re.sub(pattern, replace_png_with_webp, content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已更新: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 更新失败 {file_path}: {str(e)}")
        return False

def main():
    """主函数"""
    print("🔄 HTML图片引用更新工具")
    print("=" * 50)
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    
    if not html_files:
        print("❌ 当前目录下没有找到HTML文件")
        return
    
    print(f"📁 找到 {len(html_files)} 个HTML文件")
    print()
    
    success_count = 0
    
    for html_file in html_files:
        if update_html_file(html_file):
            success_count += 1
    
    print()
    print("=" * 50)
    print(f"🎉 更新完成!")
    print(f"✅ 成功更新: {success_count}/{len(html_files)} 个文件")
    print()
    print("📝 注意事项:")
    print("1. 原始HTML文件已备份为 .backup 文件")
    print("2. 请测试网站确保所有图片正常显示")
    print("3. 如果测试正常，可以删除 .backup 文件")
    print("4. 建议保留原始PNG文件作为备用")

if __name__ == "__main__":
    main() 