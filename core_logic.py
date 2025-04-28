import os
import re
import shutil
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def sanitize_filename(name):
    """净化文件名，替换非法字符"""
    invalid_chars = r'\/:*?"<>|'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name

def process_md_file(md_file_path, progress_callback=None, img_dir_name="img"):
    """处理单个Markdown文件中的图片链接
    
    Args:
        md_file_path: Markdown文件路径
        progress_callback: 进度回调函数
        img_dir_name: 图片保存目录名称，默认为"img"
        
    Returns:
        处理的图片数量
    """
    try:
        base_dir = os.path.dirname(md_file_path)
        img_folder_path = os.path.join(base_dir, img_dir_name)

        # 检查img文件夹是否存在
        if not os.path.exists(img_folder_path):
            os.makedirs(img_folder_path, exist_ok=True)
            logger.info(f"已创建 {img_dir_name} 文件夹: {img_folder_path}")

        # 读取Markdown文件内容
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(md_file_path, 'r', encoding='gbk') as f:
                content = f.read()

        # 查找图片链接 - 改进正则表达式以匹配更多格式
        pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        
        # 跟踪所有图片描述和路径的映射关系
        desc_to_path = {}
        path_to_desc = {}
        desc_set = set()
        
        new_content = content
        img_count = 0
        
        # 第一步：收集所有图片描述和路径
        for alt_text, img_path in matches:
            # 规范化路径，解决Windows路径问题
            normalized_path = os.path.normpath(img_path)
            
            # 记录描述和路径的对应关系
            desc_to_path[alt_text] = normalized_path
            path_to_desc[normalized_path] = alt_text

        # 第二步：处理每个图片
        processed_paths = set()  # 跟踪已处理的路径
        
        for i, (alt_text, img_path) in enumerate(matches):
            # 规范化路径
            normalized_img_path = os.path.normpath(img_path)
            
            # 如果此路径已处理过，跳过
            if normalized_img_path in processed_paths:
                continue
                
            processed_paths.add(normalized_img_path)
            
            # 构建完整路径
            img_full_path = os.path.abspath(os.path.join(base_dir, normalized_img_path))
            
            # 检查文件是否存在
            if not os.path.exists(img_full_path):
                logger.info(f"⚠️ 找不到图片：{img_full_path}，跳过")
                continue

            # 处理重复描述
            if alt_text in desc_set:
                # 重复描述，提供唯一名称
                base_alt = alt_text
                count = 1
                while alt_text in desc_set:
                    alt_text = f"{base_alt}_{count}"
                    count += 1
                logger.info(f"图片描述重复: '{base_alt}' 改为 '{alt_text}'")
            
            desc_set.add(alt_text)

            # 生成新文件名和路径
            file_ext = os.path.splitext(img_full_path)[1]
            safe_alt_text = sanitize_filename(alt_text)
            new_filename = f"{safe_alt_text}{file_ext}"
            
            # 确保新文件保存在指定文件夹中
            img_dir = os.path.join(base_dir, img_dir_name)
            new_full_path = os.path.join(img_dir, new_filename)
            # 使用用户指定的目录构建新路径
            new_relative_path = f"./{img_dir_name}/{new_filename}".replace("\\", "/")

            # 判断源路径和目标路径是否相同
            if os.path.normcase(img_full_path) == os.path.normcase(new_full_path):
                logger.info(f"图片名称已经符合要求: {new_filename}")
                continue

            # 安全复制文件
            try:
                # 如果目标文件已存在，先删除
                if os.path.exists(new_full_path):
                    os.remove(new_full_path)
                
                # 复制而不是移动，避免源文件不存在的问题
                shutil.copy2(img_full_path, new_full_path)
                
                # 源文件和目标文件不同才计算为成功处理
                if os.path.normcase(img_full_path) != os.path.normcase(new_full_path):
                    img_count += 1
                    logger.info(f"已处理: {os.path.basename(img_full_path)} -> {new_filename}")
                
                # 替换文件内容中的所有此图片路径实例
                for orig_path in matches:
                    if os.path.normpath(orig_path[1]) == normalized_img_path:
                        orig_text = f"![{orig_path[0]}]({orig_path[1]})"
                        new_text = f"![{orig_path[0]}]({new_relative_path})"
                        new_content = new_content.replace(orig_text, new_text)
                
            except Exception as e:
                logger.info(f"处理图片时出错: {e}")
                continue

            # 更新进度
            if progress_callback:
                progress_callback(i + 1, len(matches))

        # 保存新内容到文件
        try:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            if img_count > 0:
                logger.info(f"✅ 已完成 {img_count} 个图片的处理")
            else:
                logger.info(f"ℹ️ 没有需要处理的图片")
        except Exception as e:
            logger.info(f"保存文件时出错: {e}")

        return img_count
    except Exception as e:
        logger.info(f"处理文件时出现未知错误: {e}")
        return 0
