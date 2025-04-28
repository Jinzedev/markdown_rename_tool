import os
import shutil
import PyInstaller.__main__

print("开始打包应用程序...")

# 清理之前的构建文件
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("markdown_rename_tool.spec"):
    os.remove("markdown_rename_tool.spec")

# 定义图标路径
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "logo.png")
print(f"使用图标: {icon_path}")

# 使用PyInstaller打包
try:
    PyInstaller.__main__.run([
        "main.py",                          # 主程序文件
        "--name=markdown_rename_tool",      # 可执行文件名称
        "--onefile",                        # 单文件模式
        "--windowed",                       # 不显示控制台窗口
        f"--icon={icon_path}",              # 应用图标
        "--clean",                          # 每次构建前清理
        "--add-data=resources/*;resources", # 添加资源文件
        "--noconfirm",                      # 不确认覆盖
    ])
    print("打包成功！可执行文件位于 dist 文件夹中。")
except Exception as e:
    print(f"打包过程中发生错误: {e}")

print("打包过程完成。") 