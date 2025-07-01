"""
Flet 构建脚本 - 构建摸鱼神器 Windows 版本
"""

import os
import subprocess
import sys
import shutil

def check_flet():
    """检查 Flet 是否已安装"""
    try:
        import flet
        print(f"✅ Flet 已安装，版本: {flet.__version__}")
        return True
    except ImportError:
        print("❌ Flet 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flet"], check=True)
        print("✅ Flet 安装完成")
        return True

def build_windows():
    """构建 Windows 版本"""
    print("开始构建摸鱼神器 Windows 版本...")
    
    cmd = [
        "flet", "build", "windows",
        "--verbose",
        "--include-packages", "pyautogui,Pillow"
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=".")
        print("✅ Windows 版本构建成功！")
        print("📁 可执行文件位置: dist/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ flet 命令未找到，请确保 Flet 已正确安装")
        return False

def clean_build():
    """清理构建文件"""
    dirs_to_remove = ['dist', 'build', '__pycache__', '.flet']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ 已删除: {dir_name}")

if __name__ == "__main__":
    print("=" * 40)
    print("🐟 摸鱼神器构建工具")
    print("=" * 40)
    
    choice = input("""请选择操作：
1. 构建 Windows 版本
2. 清理构建文件
3. 退出

请输入选项 (1-3): """)
    
    if choice == "1":
        if check_flet() and build_windows():
            print("\n🎉 构建完成！")
            print("📁 查看 dist/ 目录获取可执行文件")
    elif choice == "2":
        clean_build()
        print("✅ 清理完成")
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选项")
