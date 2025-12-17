/**
 * 图片加载优化脚本
 * 专门处理Zeabur部署环境中的图片加载问题
 */

class ImageLoader {
  constructor() {
    this.failedImages = new Set();
    this.retryCount = 0;
    this.maxRetries = 3;
  }

  // 预加载图片
  preloadImages(imageList) {
    console.log('开始预加载图片...');
    imageList.forEach(src => {
      const img = new Image();
      img.onload = () => console.log(`✓ 预加载成功: ${src}`);
      img.onerror = () => {
        console.warn(`✗ 预加载失败: ${src}`);
        this.failedImages.add(src);
      };
      img.src = src;
    });
  }

  // 处理图片加载错误
  handleImageError(img, fallbackSrc) {
    if (this.retryCount < this.maxRetries) {
      this.retryCount++;
      console.log(`重试加载图片 (${this.retryCount}/${this.maxRetries}): ${img.src}`);
      
      // 延迟重试
      setTimeout(() => {
        img.src = fallbackSrc || img.src;
      }, 1000 * this.retryCount);
    } else {
      console.error(`图片加载最终失败: ${img.src}`);
      // 设置默认占位符
      img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDQwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yMDAgMTUwTDE1MCAxMDBIMjUwTDIwMCAxNTBaIiBmaWxsPSIjOTRBM0Y2Ii8+Cjx0ZXh0IHg9IjIwMCIgeT0iMTgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjNjM3Mzk0IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPuaPkuS7tuWbvueJhzwvdGV4dD4KPC9zdmc+';
    }
  }

  // 初始化图片错误处理
  initImageErrorHandling() {
    document.addEventListener('DOMContentLoaded', () => {
      const images = document.querySelectorAll('img');
      images.forEach(img => {
        img.addEventListener('error', (e) => {
          const originalSrc = e.target.src;
          const fallbackSrc = e.target.getAttribute('data-fallback');
          
          if (fallbackSrc && fallbackSrc !== originalSrc) {
            this.handleImageError(e.target, fallbackSrc);
          } else {
            this.handleImageError(e.target);
          }
        });
      });
    });
  }

  // 检查图片是否可访问
  async checkImageAccessibility(src) {
    try {
      const response = await fetch(src, { method: 'HEAD' });
      return response.ok;
    } catch (error) {
      console.warn(`图片访问检查失败: ${src}`, error);
      return false;
    }
  }

  // 批量检查图片可访问性
  async checkImagesAccessibility(imageList) {
    console.log('检查图片可访问性...');
    const results = await Promise.allSettled(
      imageList.map(src => this.checkImageAccessibility(src))
    );
    
    results.forEach((result, index) => {
      const src = imageList[index];
      if (result.status === 'fulfilled' && result.value) {
        console.log(`✓ 图片可访问: ${src}`);
      } else {
        console.warn(`✗ 图片不可访问: ${src}`);
      }
    });
  }
}

// 创建全局实例
window.imageLoader = new ImageLoader();

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
  // 初始化错误处理
  window.imageLoader.initImageErrorHandling();
  
  // 预加载关键图片
  const criticalImages = [
    './decision-support-model.webp',
    './other-projects.webp',
    './项目其他.webp',
    './项目7图-1.webp',
    './项目7图-2.webp',
    './项目7图-3.webp',
    './项目7图-4.webp',
    './项目7图-5.webp',
    './项目7图-6.webp'
  ];
  
  window.imageLoader.preloadImages(criticalImages);
  
  // 检查图片可访问性（仅在开发环境）
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.imageLoader.checkImagesAccessibility(criticalImages);
  }
});

// 导出供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ImageLoader;
} 