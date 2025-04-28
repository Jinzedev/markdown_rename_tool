# Markdown图片重命名工具

一个简单实用的工具，用于自动重命名Markdown文档中引用的图片文件。

## 功能特点

- 支持单个Markdown文件或整个目录的批量处理
- 自动同步更新Markdown文件中的图片引用路径
- 支持拖放操作，方便快捷
- 提供进度显示和结果反馈
- 支持中英文语言切换
- 支持浅色/深色主题切换

## 使用方法

1. 点击"选择Markdown文件"按钮选择单个.md文件
2. 点击"选择目录处理"按钮选择包含多个.md文件的文件夹
3. 或直接将.md文件/文件夹拖放到应用程序窗口

程序会自动处理并重命名相关图片文件，保持引用路径的一致性。

## 技术实现

- 使用Python和PyQt6构建跨平台GUI应用
- 使用正则表达式识别并处理Markdown中的图片引用
- 实现了响应式界面设计和主题切换功能

## 安装方法

```bash
# 克隆仓库
git clone https://github.com/yourusername/markdown_rename_tool.git

# 进入项目目录
cd markdown_rename_tool

# 安装依赖
pip install PyQt6

# 运行程序
python main.py
```

## 截图

![应用截图](resources/screenshot.png)

## 许可证

MIT 许可证 