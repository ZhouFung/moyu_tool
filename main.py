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
        self.status_text = ft.Text("🐟", size=20, color=ft.Colors.BLUE_GREY_700)
        self.toggle_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=ft.Colors.GREEN,
            on_click=self._toggle,
            tooltip="开始摸鱼",
            icon_size=20
        )
        self._setup_page()
    
    def _setup_page(self):
        """设置页面"""
        self.page.title = "🐟"
        self.page.window.width = 160
        self.page.window.height = 100
        self.page.window.resizable = False
        self.page.window.always_on_top = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # 设置图标
        try:
            self.page.window.icon = "assets/icon.png"
        except:
            pass
        
        # 构建界面
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        self.status_text,
                        self.toggle_btn
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Text(
                        "MIT License",
                        size=8,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                alignment=ft.alignment.center
            )
        )
    
    def _toggle(self, _):
        """切换状态"""
        self.engine.toggle()
    
    def _on_status_change(self, is_running):
        """状态变化回调"""
        if is_running:
            self.status_text.value = "🐟💨"
            self.toggle_btn.icon = ft.Icons.STOP
            self.toggle_btn.icon_color = ft.Colors.RED
            self.toggle_btn.tooltip = "停止摸鱼"
        else:
            self.status_text.value = "🐟"
            self.toggle_btn.icon = ft.Icons.PLAY_ARROW
            self.toggle_btn.icon_color = ft.Colors.GREEN
            self.toggle_btn.tooltip = "开始摸鱼"
        
        self.page.update()


def main(page: ft.Page):
    """主函数"""
    MoyuUI(page)


if __name__ == "__main__":
    ft.app(target=main)
