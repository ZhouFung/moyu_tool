"""
摸鱼神器 - 防锁屏工具
MIT License | github.com/lanzhitu/moyu-tool | v1.0.0
"""

import flet as ft
import pyautogui
import threading
import time
import random


class MoyuEngine:
    """摸鱼引擎 - 核心逻辑封装"""
    
    def __init__(self, callback=None):
        self.running = False
        self.callback = callback
        
    def toggle(self):
        """切换摸鱼状态"""
        if self.running:
            self.stop()
        else:
            self.start()
    
    def start(self):
        """启动摸鱼"""
        self.running = True
        threading.Thread(target=self._work, daemon=True).start()
        if self.callback:
            self.callback(True)
    
    def stop(self):
        """停止摸鱼"""
        self.running = False
        if self.callback:
            self.callback(False)
    
    def _work(self):
        """工作线程"""
        while self.running:
            x, y = pyautogui.position()
            pyautogui.moveTo(
                x + random.randint(-2, 2),
                y + random.randint(-2, 2),
                duration=0.1
            )
            time.sleep(random.randint(30, 60))


class MoyuUI:
    """摸鱼界面 - UI逻辑封装"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = MoyuEngine(self._on_status_change)
        self.status_text = ft.Text(
            "🐟", 
            size=20, 
            color=ft.Colors.BLUE_GREY_700,
            weight=ft.FontWeight.W_500
        )
        self.toggle_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=ft.Colors.GREEN_600,
            icon_size=20,
            on_click=self._toggle,
            tooltip="开始摸鱼",
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.GREEN),
                overlay_color=ft.Colors.with_opacity(0.2, ft.Colors.GREEN_200),
                padding=ft.padding.all(8)
            )
        )
        self._setup_page()
    
    def _setup_page(self):
        """设置页面"""
        self.page.title = "摸鱼神器"
        self.page.window.width = 220
        self.page.window.height = 160
        self.page.window.resizable = False
        self.page.window.always_on_top = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # 设置应用图标和窗口样式
        try:
            self.page.window.icon = "assets/icon.png"
        except:
            pass
        
        # 自定义应用栏样式
        self.page.appbar = ft.AppBar(
            title=ft.Row([
                ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE_600, size=20),
                ft.Text("摸鱼神器", size=16, color=ft.Colors.BLUE_800, weight=ft.FontWeight.W_600)
            ], spacing=8),
            bgcolor=ft.Colors.SURFACE,
            elevation=0,
            toolbar_height=40
        )
        
        # 构建协调统一的界面
        self.page.add(
            ft.Container(
                content=ft.Column([
                    # 主控制区域 - 固定宽度防止溢出
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=self.status_text,
                                width=40,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=self.toggle_btn,
                                width=50,
                                height=50,
                                alignment=ft.alignment.center,
                                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_GREY_100),
                                border_radius=25,
                                border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY_200))
                            )
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15
                        ),
                        width=180,
                        padding=ft.padding.symmetric(horizontal=10, vertical=15),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_50),
                        border_radius=15,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_100)),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_300),
                            offset=ft.Offset(0, 2)
                        )
                    ),
                    # 版权信息
                    ft.Container(
                        content=ft.Text(
                            "MIT License · v1.0.0",
                            size=9,
                            color=ft.Colors.BLUE_GREY_400,
                            text_align=ft.TextAlign.CENTER
                        ),
                        margin=ft.margin.only(top=8)
                    )
                ], 
                spacing=0, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.BLUE_50)
            )
        )
    
    def _toggle(self, _):
        """切换状态"""
        self.engine.toggle()
    
    def _on_status_change(self, is_running):
        """状态变化回调"""
        if is_running:
            self.status_text.value = "🐟💨"
            self.status_text.color = ft.Colors.ORANGE_600
            self.toggle_btn.icon = ft.Icons.STOP
            self.toggle_btn.icon_color = ft.Colors.RED_600
            self.toggle_btn.tooltip = "停止摸鱼"
            self.toggle_btn.style.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.RED)
            self.toggle_btn.style.overlay_color = ft.Colors.with_opacity(0.2, ft.Colors.RED_200)
        else:
            self.status_text.value = "🐟"
            self.status_text.color = ft.Colors.BLUE_GREY_700
            self.toggle_btn.icon = ft.Icons.PLAY_ARROW
            self.toggle_btn.icon_color = ft.Colors.GREEN_600
            self.toggle_btn.tooltip = "开始摸鱼"
            self.toggle_btn.style.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.GREEN)
            self.toggle_btn.style.overlay_color = ft.Colors.with_opacity(0.2, ft.Colors.GREEN_200)
        
        self.page.update()


def main(page: ft.Page):
    """主函数"""
    MoyuUI(page)


if __name__ == "__main__":
    ft.app(
        target=main,
        name="摸鱼神器",
        assets_dir="assets"
    )
