import ctypes
import sys
import os

def refresh_icon_cache():
    # 通知Windows更新图标缓存
    SHCNE_ASSOCCHANGED = 0x08000000
    SHCNF_IDLIST = 0
    ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
    print("已刷新图标缓存！")

if __name__ == "__main__":
    refresh_icon_cache() 