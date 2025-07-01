"""
打包脚本 - 将摸鱼神器打包成可执行文件
使用PyInstaller将Python程序打包成exe文件
"""

import os
import subprocess
import sys

def install_pyinstaller():
    """安装pyinstaller"""
    print("正在安装PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def build_exe():
    """打包成exe文件"""
    print("开始打包摸鱼神器...")
    
    # PyInstaller打包命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 不显示控制台窗口
        "--name=摸鱼神器",               # 设置程序名称
        "--icon=assets/icon.ico",       # 程序图标
        "--add-data=README.md;.",       # 包含README文件
        "--add-data=assets;assets",     # 包含assets文件夹
        "main.py"                       # 主程序文件
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 打包成功！")
        print("📁 可执行文件位置: dist/摸鱼神器.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller未安装，正在安装...")
        install_pyinstaller()
        print("✅ PyInstaller安装完成，请重新运行此脚本")

def clean_build():
    """清理打包过程中的临时文件"""
    import shutil
    
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['摸鱼神器.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ 已删除临时目录: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️ 已删除临时文件: {file_name}")

if __name__ == "__main__":
    print("=" * 50)
    print("🐟 摸鱼神器打包工具")
    print("=" * 50)
    
    choice = input("请选择操作：\n1. 打包程序\n2. 清理临时文件\n3. 退出\n请输入选项 (1-3): ")
    
    if choice == "1":
        build_exe()
    elif choice == "2":
        clean_build()
        print("✅ 清理完成")
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选项")
