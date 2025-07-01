"""
防息屏工具 - 现代化UI界面
"""

import flet as ft
import os
import sys
from engine import ScreenProtectionEngine


class ScreenProtectionUI:
    """防息屏工具UI类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = ScreenProtectionEngine(self._update_status)
        self._setup_window()
        self._create_components()
        self._build_interface()
    
    def _setup_window(self):
        """窗口配置"""
        w = self.page.window
        w.title, w.width, w.height = "防息屏工具", 400, 250
        w.min_width, w.min_height = 320, 200
        w.resizable, w.always_on_top = True, True
        self.page.theme_mode, self.page.padding = ft.ThemeMode.LIGHT, 0
        
        # 设置窗口图标
        try:
            base = sys._MEIPASS if getattr(sys, 'frozen', False) else "."
            icon_path = os.path.join(base, "assets", "icon.png")
            if os.path.exists(icon_path):
                w.icon = icon_path
        except:
            pass
    
    def _create_components(self):
        """创建组件"""
        self.status_icon = ft.Icon(ft.Icons.COMPUTER, size=28, color=ft.Colors.BLUE_600)
        self.status_text = ft.Text("未激活", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700)
        self.main_button = ft.ElevatedButton(
            text="开始保护", icon=ft.Icons.PLAY_ARROW, height=40,
            on_click=lambda _: self.engine.toggle_protection(),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600,
                padding=ft.padding.symmetric(horizontal=20, vertical=8),
                shape=ft.RoundedRectangleBorder(radius=20)
            )
        )
    
    def _build_interface(self):
        """构建界面"""
        self.page.add(ft.Container(
            content=ft.Column([
                # 标题栏
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MONITOR, size=18, color=ft.Colors.BLUE_600),
                        ft.Text("防息屏工具", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_800)
                    ], spacing=6, alignment=ft.MainAxisAlignment.CENTER, tight=True),
                    bgcolor=ft.Colors.BLUE_50, padding=ft.padding.all(8),
                    border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLUE_100))
                ),
                # 功能说明
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FLASH_ON, size=14, color=ft.Colors.BLUE_600),
                        ft.Text("系统状态保持", size=11, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
                    ], spacing=4, alignment=ft.MainAxisAlignment.CENTER, tight=True),
                    padding=ft.padding.symmetric(vertical=4), alignment=ft.alignment.center
                ),
                # 主控制区
                ft.Container(
                    content=ft.Column([
                        ft.Row([self.status_icon, self.status_text], spacing=10, 
                              alignment=ft.MainAxisAlignment.CENTER, tight=True),
                        self.main_button
                    ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                    padding=ft.padding.all(12), bgcolor=ft.Colors.WHITE, border_radius=8,
                    border=ft.border.all(1, ft.Colors.BLUE_100), alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_GREY_300),
                                      offset=ft.Offset(0, 1))
                ),
                # 信息区
                ft.Container(
                    content=ft.Text("⏱️ 防超时：30-60秒间隔\n🖱️ 微动保护：轻微移动",
                                   size=11, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER),
                    padding=ft.padding.symmetric(vertical=4), alignment=ft.alignment.center
                )
            ], spacing=0, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50, alignment=ft.alignment.center, expand=True
        ))
    
    def _update_status(self, is_running: bool):
        """状态更新"""
        if is_running:
            self.status_icon.name, self.status_icon.color = ft.Icons.FLASH_ON, ft.Colors.ORANGE_600
            self.status_text.value, self.status_text.color = "保护中", ft.Colors.ORANGE_700
            self.main_button.text, self.main_button.icon = "停止保护", ft.Icons.PAUSE
            self.main_button.style.bgcolor = ft.Colors.ORANGE_600
        else:
            self.status_icon.name, self.status_icon.color = ft.Icons.COMPUTER, ft.Colors.BLUE_600
            self.status_text.value, self.status_text.color = "未激活", ft.Colors.BLUE_GREY_700
            self.main_button.text, self.main_button.icon = "开始保护", ft.Icons.PLAY_ARROW
            self.main_button.style.bgcolor = ft.Colors.GREEN_600
        
        self.page.update()


def create_app(page: ft.Page):
    """应用入口"""
    ScreenProtectionUI(page)
