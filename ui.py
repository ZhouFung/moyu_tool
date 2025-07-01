"""
防息屏工具 - 现代化UI界面
基于Flet框架的用户界面实现
"""

import flet as ft
from engine import ScreenProtectionEngine


class ScreenProtectionUI:
    """防息屏工具UI类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = ScreenProtectionEngine(self._on_status_change)
        self._init_components()
        self._setup_page()
        self._build_layout()
    
    def _setup_page(self):
        """页面配置"""
        self.page.title = "防息屏工具"
        # 使用黄金比例 1.618，400x250 更大尺寸符合视觉审美
        self.page.window.width = 400
        self.page.window.height = 250
        # 设置最小尺寸，保持比例
        self.page.window.min_width = 320
        self.page.window.min_height = 200
        self.page.window.resizable = True
        self.page.window.always_on_top = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        try:
            self.page.window.icon = "assets/icon.png"
        except:
            pass
    
    def _init_components(self):
        """初始化UI组件"""
        self.status_icon = ft.Icon(ft.Icons.COMPUTER, size=28, color=ft.Colors.BLUE_600)
        self.status_text = ft.Text("未激活", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700)
        self.main_button = self._create_button()
        self.info_text = ft.Text(
            "⏱️ 防超时：30-60秒间隔\n🖱️ 微动保护：轻微移动",
            size=11, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER
        )
    
    def _create_button(self):
        """创建主按钮"""
        return ft.ElevatedButton(
            text="开始保护",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self._toggle_protection,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_600,
                padding=ft.padding.symmetric(horizontal=20, vertical=8),
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            height=40
        )
    
    def _create_section(self, content, **kwargs):
        """创建通用容器"""
        defaults = {
            'alignment': ft.alignment.center,
            'padding': ft.padding.all(8)
        }
        defaults.update(kwargs)
        return ft.Container(content=content, **defaults)
    
    def _build_layout(self):
        """构建布局"""
        # 标题区
        title = self._create_section(
            ft.Row([
                ft.Icon(ft.Icons.MONITOR, size=18, color=ft.Colors.BLUE_600),
                ft.Text("防息屏工具", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_800)
            ], spacing=6, alignment=ft.MainAxisAlignment.CENTER, tight=True),
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLUE_100))
        )
        
        # 功能说明
        desc = self._create_section(
            ft.Row([
                ft.Icon(ft.Icons.FLASH_ON, size=14, color=ft.Colors.BLUE_600),
                ft.Text("系统状态保持", size=11, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER, tight=True),
            padding=ft.padding.symmetric(vertical=4)
        )
        
        # 主控制区
        control = self._create_section(
            ft.Column([
                ft.Row([self.status_icon, self.status_text], spacing=10, 
                      alignment=ft.MainAxisAlignment.CENTER, tight=True),
                self.main_button
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
            padding=ft.padding.all(12),
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_GREY_300), offset=ft.Offset(0, 1))
        )
        
        # 信息区
        info = self._create_section(self.info_text, padding=ft.padding.symmetric(vertical=4))
        
        # 主容器
        main_container = ft.Container(
            content=ft.Column([title, desc, control, info], spacing=0, tight=True, 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50,
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.page.add(main_container)
    
    def _toggle_protection(self, _):
        """切换保护状态"""
        self.engine.toggle_protection()
    
    def _on_status_change(self, is_running: bool):
        """状态变化回调"""
        if is_running:
            self.status_icon.name = ft.Icons.FLASH_ON
            self.status_icon.color = ft.Colors.ORANGE_600
            self.status_text.value = "保护中"
            self.status_text.color = ft.Colors.ORANGE_700
            self.main_button.text = "停止保护"
            self.main_button.icon = ft.Icons.PAUSE
            self.main_button.style.bgcolor = ft.Colors.ORANGE_600
        else:
            self.status_icon.name = ft.Icons.COMPUTER
            self.status_icon.color = ft.Colors.BLUE_600
            self.status_text.value = "未激活"
            self.status_text.color = ft.Colors.BLUE_GREY_700
            self.main_button.text = "开始保护"
            self.main_button.icon = ft.Icons.PLAY_ARROW
            self.main_button.style.bgcolor = ft.Colors.GREEN_600
        
        self.page.update()


def create_app(page: ft.Page):
    """创建应用程序"""
    ScreenProtectionUI(page)
