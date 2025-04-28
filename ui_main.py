from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar,
    QMenuBar, QMenu, QFrame, QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect,
    QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui  import QColor, QDragEnterEvent, QDropEvent, QFont, QIcon, QPixmap

import os
import sys
import core_logic

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和PyInstaller打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 不是通过PyInstaller打包，使用当前文件夹
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# ---------- 主窗口 ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # -------- 基本属性 --------
        self.lang = "zh"
        self.theme = "light"
        self.resize(800, 600)
        self.setWindowTitle(self.texts()["title"])
        self.setAcceptDrops(True)
        
        # 设置应用图标
        icon_path = resource_path(os.path.join("resources", "logo.png"))
        self.setWindowIcon(QIcon(icon_path))

        # 背景色（浅灰）+ 全局字体
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                color: #333;
                font-family: "微软雅黑", Arial, sans-serif;
                font-size: 14px;
            }
        """)

        # -------- 布局 --------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(15)  # 减小整体间距

        # ------ 顶部菜单区域 ------
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # 语言切换按钮 - 与主题切换按钮样式统一
        self.btn_lang = QPushButton(self.texts()["language_text"])
        self.btn_lang.setStyleSheet("""
            QPushButton {
                background: rgba(77, 166, 255, 0.15);
                color: #4da6ff;
                border: 1px solid rgba(77, 166, 255, 0.3);
                border-radius: 6px;
                padding: 5px 15px;
                font-size: 13px;
                max-width: 100px;
            }
            QPushButton:hover { 
                background: rgba(77, 166, 255, 0.25);
            }
            QPushButton:pressed { 
                background: rgba(77, 166, 255, 0.35);
            }
        """)
        top_layout.addWidget(self.btn_lang)
        
        # 语言菜单
        self.lang_menu = QMenu(self)
        self.lang_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background: rgba(77, 166, 255, 0.2);
            }
        """)
        
        self.lang_menu.addAction("中文", lambda: self.switch_language("zh"))
        self.lang_menu.addAction("English", lambda: self.switch_language("en"))
        self.btn_lang.clicked.connect(self.show_lang_menu)
        
        # 添加中间间隔
        top_layout.addStretch()
        
        # 主题切换按钮 - 移至顶部右侧
        self.btn_theme = QPushButton(self.texts()["theme_switch"])
        self.btn_theme.setStyleSheet("""
            QPushButton {
                background: rgba(77, 166, 255, 0.15);
                color: #4da6ff;
                border: 1px solid rgba(77, 166, 255, 0.3);
                border-radius: 6px;
                padding: 5px 15px;
                font-size: 13px;
                max-width: 100px;
            }
            QPushButton:hover { 
                background: rgba(77, 166, 255, 0.25);
            }
            QPushButton:pressed { 
                background: rgba(77, 166, 255, 0.35);
            }
        """)
        # 添加到右侧
        top_layout.addWidget(self.btn_theme)
        
        # 将顶部布局添加到主布局
        main_layout.addLayout(top_layout)

        # ------ Logo ------
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedHeight(80)
        # 设置Logo图片
        logo_path = resource_path(os.path.join("resources", "logo.png"))
        logo_pixmap = QPixmap(logo_path)
        logo_pixmap = logo_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        main_layout.addWidget(self.logo_label)

        # ------ 标题 ------
        self.label_title = QLabel(self.texts()["title"])
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 600;
            color: #2c3e50;
            margin: 5px 0;
        """)
        main_layout.addWidget(self.label_title)

        # ------ 说明文字 ------
        self.label_info = QLabel(self.texts()["instruction"])
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setWordWrap(True)
        self.label_info.setStyleSheet("""
            color: #5a6a7f;
            font-size: 15px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(self.label_info)

        # ------ 图片目录设置 ------
        img_dir_layout = QHBoxLayout()
        img_dir_layout.setSpacing(10)
        
        # 图片目录标签
        self.img_dir_label = QLabel(self.texts()["img_dir_label"])
        self.img_dir_label.setStyleSheet("""
            color: #5a6a7f;
            font-size: 14px;
        """)
        
        # 图片目录输入框
        self.img_dir_input = QLineEdit("img")
        self.img_dir_input.setPlaceholderText("img")
        self.img_dir_input.setMaximumWidth(150)
        self.img_dir_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px 10px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #4da6ff;
            }
        """)
        
        # 布局添加控件
        img_dir_layout.addWidget(self.img_dir_label)
        img_dir_layout.addWidget(self.img_dir_input)
        img_dir_layout.addStretch()
        
        main_layout.addLayout(img_dir_layout)

        # ------ 操作按钮 ------
        # 按钮统一样式
        btn_css = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #5ab9ff, stop:1 #4da6ff);
                color: white;
                border: none;
                border-radius: 10px;
                height: 42px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #4da6ff, stop:1 #3a93ff); 
            }
            QPushButton:pressed { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #3a93ff, stop:1 #2788ee); 
            }
        """

        # 按钮布局 - 文件和文件夹按钮并排
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.btn_file = QPushButton(self.texts()["start_button"])
        self.btn_folder = QPushButton(self.texts()["folder_button"])
        
        for b in (self.btn_file, self.btn_folder):
            b.setStyleSheet(btn_css)
            button_layout.addWidget(b)
        
        main_layout.addLayout(button_layout)

        # ------ 拖拽区域 ------
        self.drop_box = QLabel(self.texts()["drag_hint"])
        self.drop_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_box.setFixedHeight(110)  # 减小高度
        self.drop_box.setStyleSheet("""
            QLabel {
                border: 2px dashed #b4b4b4;
                border-radius: 14px;
                background: rgba(255,255,255,0.6);
                color: #7f8c8d;
                font-size: 15px;
            }
        """)
        main_layout.addWidget(self.drop_box, 1)  # 拖拽区域可伸展

        # ------ 状态标签 ------
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            margin: 5px 0;
            min-height: 24px;
        """)
        main_layout.addWidget(self.status_label)

        # ------ 进度条 ------
        self.progress = QProgressBar()
        self.progress.setFixedHeight(12)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #e1e1e1;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #4da6ff, stop:1 #4e72f9);
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress)

        # 添加阴影效果到主要按钮
        for b in (self.btn_file, self.btn_folder):
            b.setGraphicsEffect(self.create_shadow_effect())

        # -------- 信号连接 --------
        self.btn_file.clicked.connect(self.open_files)
        self.btn_folder.clicked.connect(self.open_folder)
        self.btn_theme.clicked.connect(self.toggle_theme)

    # 创建阴影效果
    def create_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        return shadow

    # ---------- 语言菜单显示 ----------
    def show_lang_menu(self):
        """显示语言选择菜单"""
        # 计算菜单显示位置
        pos = self.btn_lang.mapToGlobal(self.btn_lang.rect().bottomLeft())
        self.lang_menu.exec(pos)
    
    # ---------- 语言切换 ----------
    def texts(self):
        return {
            "zh": {
                "title": "Markdown 图片重命名工具",
                "instruction": "点击按钮选择文件或拖拽文件/目录到下方区域，自动同步图片文件名。",
                "start_button": "选择 Markdown 文件",
                "folder_button": "选择目录处理",
                "theme_switch": "切换主题",
                "drag_hint": "将 .md 文件或目录拖到这里 ↓",
                "success_msg": "处理成功！已重命名 {0} 个图片文件。",
                "no_img_msg": "未找到需要处理的图片文件。",
                "success_title": "处理成功",
                "language_text": "语言",
                "img_dir_label": "图片目录"
            },
            "en": {
                "title": "Markdown Image Rename Tool",
                "instruction": "Click buttons or drag files/folder below – image filenames sync automatically.",
                "start_button": "Select Markdown Files",
                "folder_button": "Select Folder",
                "theme_switch": "Switch Theme",
                "drag_hint": "Drag .md files or folder here ↓",
                "success_msg": "Success! Renamed {0} image files.",
                "no_img_msg": "No images found to process.",
                "success_title": "Success",
                "language_text": "Language",
                "img_dir_label": "Image Directory"
            }
        }[self.lang]

    def switch_language(self, lang):
        self.lang = lang
        t = self.texts()
        self.setWindowTitle(t["title"])
        self.label_title.setText(t["title"])
        self.label_info.setText(t["instruction"])
        self.btn_file.setText(t["start_button"])
        self.btn_folder.setText(t["folder_button"])
        self.btn_theme.setText(t["theme_switch"])
        self.drop_box.setText(t["drag_hint"])
        self.btn_lang.setText(t["language_text"])
        self.img_dir_label.setText(t["img_dir_label"])

    # ---------- 文件选择 ----------
    def open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Markdown", "", "Markdown (*.md)")
        self.handle_items(paths)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            md_files = []
            for root, _, files in os.walk(folder):
                md_files += [os.path.join(root, f) for f in files if f.endswith(".md")]
            self.handle_items(md_files)

    # ---------- 拖拽 ----------
    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            # 根据主题高亮边框
            if self.theme == "light":
                self.drop_box.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #4da6ff;
                        border-radius: 14px;
                        background: rgba(232, 245, 255, 0.8);
                        color: #4da6ff;
                        font-size: 15px;
                    }
                """)
            else:
                self.drop_box.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #4da6ff;
                        border-radius: 14px;
                        background: rgba(77, 166, 255, 0.15);
                        color: #72b8ff;
                        font-size: 15px;
                    }
                """)

    def dragLeaveEvent(self, e):
        if self.theme == "light":
            self.reset_drop_style()
        else:
            self.reset_drop_style_dark()

    def dropEvent(self, e: QDropEvent):
        paths = [u.toLocalFile() for u in e.mimeData().urls()]
        self.handle_items(paths)
        if self.theme == "light":
            self.reset_drop_style()
        else:
            self.reset_drop_style_dark()

    def reset_drop_style(self):
        self.drop_box.setStyleSheet("""
            QLabel {
                border: 2px dashed #b4b4b4;
                border-radius: 14px;
                background: rgba(255,255,255,0.6);
                color: #7f8c8d;
                font-size: 15px;
            }
        """)

    def reset_drop_style_dark(self):
        self.drop_box.setStyleSheet("""
            QLabel {
                border: 2px dashed #52616a;
                border-radius: 14px;
                background: rgba(60, 64, 72, 0.6);
                color: #9e9e9e;
                font-size: 15px;
            }
        """)

    # ---------- 处理 ----------
    def handle_items(self, paths):
        if not paths:
            return
            
        total_img_count = 0
        self.progress.setValue(0)
        self.status_label.setText("")
        
        # 获取用户设置的图片目录
        img_dir_name = self.img_dir_input.text().strip()
        if not img_dir_name:
            img_dir_name = "img"  # 默认值
        
        for p in paths:
            img_count = core_logic.process_md_file(p, self.update_progress, img_dir_name)
            total_img_count += img_count
        
        self.progress.setValue(100)
        
        # 显示成功消息
        t = self.texts()
        if total_img_count > 0:
            success_text = t["success_msg"].format(total_img_count)
            self.status_label.setText(success_text)
            self.status_label.setStyleSheet(f"""
                color: {'#2ecc71' if self.theme == 'light' else '#2ecc71'};
                font-weight: 600;
                font-size: 15px;
                min-height: 24px;
            """)
            
            # 添加成功对话框 - 修改样式为简洁现代风格
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(t["success_title"])
            msg_box.setText(success_text)
            
            # 移除图标，使用简洁样式
            msg_box.setIcon(QMessageBox.Icon.NoIcon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # 根据主题设置不同样式
            if self.theme == "light":
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #ffffff;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                    }
                    QMessageBox QLabel {
                        color: #333333;
                        font-size: 15px;
                        font-weight: 500;
                        padding: 10px;
                    }
                    QPushButton {
                        background-color: #4da6ff;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 20px;
                        font-size: 14px;
                        font-weight: 500;
                        margin: 10px;
                    }
                    QPushButton:hover {
                        background-color: #3a93ff;
                    }
                """)
            else:
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #222831;
                        border: 1px solid #393e46;
                        border-radius: 8px;
                    }
                    QMessageBox QLabel {
                        color: #e5e5e5;
                        font-size: 15px;
                        font-weight: 500;
                        padding: 10px;
                    }
                    QPushButton {
                        background-color: #4da6ff;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 20px;
                        font-size: 14px;
                        font-weight: 500;
                        margin: 10px;
                    }
                    QPushButton:hover {
                        background-color: #3a93ff;
                    }
                """)
            msg_box.exec()
        else:
            self.status_label.setText(t["no_img_msg"])
            self.status_label.setStyleSheet(f"""
                color: {'#e67e22' if self.theme == 'light' else '#f39c12'};
                font-weight: 600;
                font-size: 15px;
                min-height: 24px;
            """)
            
        # 3秒后清除状态标签消息
        QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def update_progress(self, cur, tot):
        if tot > 0:
            self.progress.setValue(int(cur / tot * 100))

    # ---------- 主题切换 ----------
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.setStyleSheet("""
                QWidget { 
                    background-color: #222831; 
                    color: #eeeeee; 
                    font-family: "微软雅黑"; 
                }
            """)
            
            # 深色模式下的标题和说明
            self.label_title.setStyleSheet("font-size: 28px; font-weight: 600; color: #e5e5e5;")
            self.label_info.setStyleSheet("color: #aaaaaa; font-size: 15px;")
            
            # 深色模式下的logo标签
            self.logo_label.setStyleSheet("background-color: transparent;")
            
            # 深色模式下的图片目录输入框
            self.img_dir_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
            self.img_dir_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #464e5c;
                    border-radius: 5px;
                    padding: 5px 10px;
                    background: #333842;
                    color: #e5e5e5;
                }
                QLineEdit:focus {
                    border: 1px solid #4da6ff;
                }
            """)
            
            # 深色模式下的拖拽区域
            self.reset_drop_style_dark()
            
            # 深色模式下的状态标签
            self.status_label.setStyleSheet("""
                font-size: 15px;
                font-weight: 600;
                margin: 5px 0;
                min-height: 24px;
                color: #e5e5e5;
            """)
            
            # 深色模式下的进度条
            self.progress.setStyleSheet("""
                QProgressBar {
                    background: #393e46;
                    border-radius: 6px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4da6ff, stop:1 #4e72f9);
                    border-radius: 6px;
                }
            """)
            
            # 深色模式下的功能按钮
            btn_main_css = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #4a69bd, stop:1 #3a56a8);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    height: 42px;
                    font-size: 15px;
                    font-weight: 500;
                }
                QPushButton:hover { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #3a56a8, stop:1 #2a4598); 
                }
                QPushButton:pressed { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #2a4598, stop:1 #203788); 
                }
            """
            
            for b in (self.btn_file, self.btn_folder):
                b.setStyleSheet(btn_main_css)
                # 更新阴影颜色
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(15)
                shadow.setColor(QColor(0, 0, 50, 50))
                shadow.setOffset(0, 3)
                b.setGraphicsEffect(shadow)
            
            # 深色模式下的小按钮
            btn_style = """
                QPushButton {
                    background: rgba(77, 166, 255, 0.15);
                    color: #72b8ff;
                    border: 1px solid rgba(77, 166, 255, 0.3);
                    border-radius: 6px;
                    padding: 5px 15px;
                    font-size: 13px;
                    max-width: 100px;
                }
                QPushButton:hover { 
                    background: rgba(77, 166, 255, 0.25);
                }
                QPushButton:pressed { 
                    background: rgba(77, 166, 255, 0.35);
                }
            """
            self.btn_theme.setStyleSheet(btn_style)
            self.btn_lang.setStyleSheet(btn_style)
        else:
            self.theme = "light"
            self.setStyleSheet("""
                QWidget { background-color: #f5f7fa; color: #333; font-family: "微软雅黑"; }
            """)
            
            # 浅色模式下的标题和说明
            self.label_title.setStyleSheet("font-size: 28px; font-weight: 600; color: #2c3e50; margin: 5px 0;")
            self.label_info.setStyleSheet("color: #5a6a7f; font-size: 15px; margin-bottom: 10px;")
            
            # 浅色模式下的logo标签
            self.logo_label.setStyleSheet("background-color: transparent;")
            
            # 浅色模式下的图片目录输入框
            self.img_dir_label.setStyleSheet("color: #5a6a7f; font-size: 14px;")
            self.img_dir_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 5px 10px;
                    background: white;
                    color: #333;
                }
                QLineEdit:focus {
                    border: 1px solid #4da6ff;
                }
            """)
            
            # 浅色模式下的拖拽区域
            self.reset_drop_style()
            
            # 浅色模式下的状态标签
            self.status_label.setStyleSheet("""
                font-size: 15px;
                font-weight: 600;
                margin: 5px 0;
                min-height: 24px;
                color: #2c3e50;
            """)
            
            # 浅色模式下的进度条
            self.progress.setStyleSheet("""
                QProgressBar {
                    background: #e1e1e1;
                    border-radius: 6px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4da6ff, stop:1 #4e72f9);
                    border-radius: 6px;
                }
            """)
            
            # 浅色模式下的功能按钮
            btn_main_css = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #5ab9ff, stop:1 #4da6ff);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    height: 42px;
                    font-size: 15px;
                    font-weight: 500;
                }
                QPushButton:hover { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #4da6ff, stop:1 #3a93ff); 
                }
                QPushButton:pressed { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 #3a93ff, stop:1 #2788ee); 
                }
            """
            
            for b in (self.btn_file, self.btn_folder):
                b.setStyleSheet(btn_main_css)
                # 更新阴影颜色
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(15)
                shadow.setColor(QColor(0, 0, 0, 30))
                shadow.setOffset(0, 3)
                b.setGraphicsEffect(shadow)
            
            # 浅色模式下的小按钮
            btn_style = """
                QPushButton {
                    background: rgba(77, 166, 255, 0.15);
                    color: #4da6ff;
                    border: 1px solid rgba(77, 166, 255, 0.3);
                    border-radius: 6px;
                    padding: 5px 15px;
                    font-size: 13px;
                    max-width: 100px;
                }
                QPushButton:hover { 
                    background: rgba(77, 166, 255, 0.25);
                }
                QPushButton:pressed { 
                    background: rgba(77, 166, 255, 0.35);
                }
            """
            self.btn_theme.setStyleSheet(btn_style)
            self.btn_lang.setStyleSheet(btn_style)
    
