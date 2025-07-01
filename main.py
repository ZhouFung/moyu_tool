"""
防息屏工具 - 现代化UI版本
专业的防息屏/防网页超时保护工具
MIT License | v2.0.0
"""

import flet as ft
from ui import create_app


def main(page: ft.Page):
    """应用程序主入口"""
    create_app(page)


if __name__ == "__main__":
    ft.app(
        target=main,
        name="防息屏工具",
        assets_dir="assets"
    )
