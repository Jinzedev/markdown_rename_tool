import sys
import os
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui_main import MainWindow

def refresh_icon_cache():
    # 通知Windows更新图标缓存
    try:
        SHCNE_ASSOCCHANGED = 0x08000000
        SHCNF_IDLIST = 0
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
        print("已刷新图标缓存")
    except Exception as e:
        print(f"刷新图标缓存失败: {e}")

if __name__ == "__main__":
    # 尝试刷新图标缓存
    refresh_icon_cache()
    
    app = QApplication(sys.argv)
    
    # 使用绝对路径获取图标
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "resources", "logo.png")
    
    # 设置应用程序图标（任务栏显示）
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    
    # 为了确保Windows任务栏使用正确的图标
    # 设置应用程序ID
    try:
        from ctypes import windll
        myappid = f'meow.markdowntool.1.0'  # 确保这是一个唯一的字符串
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
