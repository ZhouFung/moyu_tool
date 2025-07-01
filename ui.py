"""
防息屏工具 - 现代化UI界面
"""

import flet as ft
from engine import ScreenProtectionEngine


class ScreenProtectionUI:
    """防息屏工具UI类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = ScreenProtectionEngine(self._update_status)
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self._setup_window()
        self._create_components()
        self._build_interface()
    
    def _setup_window(self):
        """窗口配置"""
        window = self.page.window
        window.title = "防息屏工具"
        window.width, window.height = 400, 250
        window.min_width, window.min_height = 320, 200
        window.resizable = True
        window.always_on_top = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        try:
            window.icon = "assets/icon.png"
        except:
            pass
    
    def _create_components(self):
        """创建组件"""
        self.status_icon = ft.Icon(ft.Icons.COMPUTER, size=28, color=ft.Colors.BLUE_600)
        self.status_text = ft.Text("未激活", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700)
        self.main_button = ft.ElevatedButton(
            text="开始保护", icon=ft.Icons.PLAY_ARROW, on_click=lambda _: self.engine.toggle_protection(),
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600,
                               padding=ft.padding.symmetric(horizontal=20, vertical=8),
                               shape=ft.RoundedRectangleBorder(radius=20)), height=40
        )
        self.info_text = ft.Text("⏱️ 防超时：30-60秒间隔\n🖱️ 微动保护：轻微移动",
                                size=11, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER)
    
    def _create_container(self, content, **kwargs):
        """通用容器工厂"""
        defaults = {'alignment': ft.alignment.center, 'padding': ft.padding.all(8)}
        defaults.update(kwargs)
        return ft.Container(content=content, **defaults)
    
    def _build_interface(self):
        """构建界面"""
        sections = [
            # 标题
            self._create_container(
                ft.Row([ft.Icon(ft.Icons.MONITOR, size=18, color=ft.Colors.BLUE_600),
                       ft.Text("防息屏工具", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_800)],
                      spacing=6, alignment=ft.MainAxisAlignment.CENTER, tight=True),
                bgcolor=ft.Colors.BLUE_50, border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLUE_100))
            ),
            # 功能说明
            self._create_container(
                ft.Row([ft.Icon(ft.Icons.FLASH_ON, size=14, color=ft.Colors.BLUE_600),
                       ft.Text("系统状态保持", size=11, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)],
                      spacing=4, alignment=ft.MainAxisAlignment.CENTER, tight=True),
                padding=ft.padding.symmetric(vertical=4)
            ),
            # 主控制区
            self._create_container(
                ft.Column([
                    ft.Row([self.status_icon, self.status_text], spacing=10, 
                          alignment=ft.MainAxisAlignment.CENTER, tight=True),
                    self.main_button
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                padding=ft.padding.all(12), bgcolor=ft.Colors.WHITE, border_radius=8,
                border=ft.border.all(1, ft.Colors.BLUE_100),
                shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_GREY_300),
                                  offset=ft.Offset(0, 1))
            ),
            # 信息区
            self._create_container(self.info_text, padding=ft.padding.symmetric(vertical=4))
        ]
        
        self.page.add(ft.Container(
            content=ft.Column(sections, spacing=0, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50, alignment=ft.alignment.center, expand=True
        ))
    
    def _update_status(self, is_running: bool):
        """状态更新"""
        states = {
            True: (ft.Icons.FLASH_ON, ft.Colors.ORANGE_600, "保护中", ft.Colors.ORANGE_700, 
                  "停止保护", ft.Icons.PAUSE, ft.Colors.ORANGE_600),
            False: (ft.Icons.COMPUTER, ft.Colors.BLUE_600, "未激活", ft.Colors.BLUE_GREY_700,
                   "开始保护", ft.Icons.PLAY_ARROW, ft.Colors.GREEN_600)
        }
        
        icon, icon_color, text, text_color, btn_text, btn_icon, btn_color = states[is_running]
        
        self.status_icon.name, self.status_icon.color = icon, icon_color
        self.status_text.value, self.status_text.color = text, text_color
        self.main_button.text, self.main_button.icon = btn_text, btn_icon
        self.main_button.style.bgcolor = btn_color
        
        self.page.update()


def create_app(page: ft.Page):
    """应用入口"""
    ScreenProtectionUI(page)
