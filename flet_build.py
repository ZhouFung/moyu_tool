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
        # 尝试获取版本号，如果失败就跳过版本显示
        try:
            version = flet.__version__
            print(f"✅ Flet 已安装，版本: {version}")
        except AttributeError:
            print("✅ Flet 已安装")
        return True
    except ImportError:
        print("❌ Flet 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flet"], check=True)
        print("✅ Flet 安装完成")
        return True

def build_windows():
    """构建 Windows 版本"""
    print("开始构建摸鱼神器 Windows 版本...")
    
    # 设置环境变量解决中文编码问题
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    cmd = ["flet", "build", "windows"]
    
    try:
        result = subprocess.run(cmd, check=True, cwd=".", env=env, capture_output=True, text=True, encoding='utf-8')
        print("✅ Windows 版本构建成功！")
        print("📁 可执行文件位置: dist/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败")
        print("💡 尝试手动构建:")
        print("   flet build windows")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ flet 命令未找到")
        print("💡 请确保 Flet 已正确安装:")
        print("   pip install --upgrade flet")
        return False
    except Exception as ex:
        print(f"❌ 构建过程中出现异常: {ex}")
        print("💡 建议手动运行构建命令:")
        print("   flet build windows")
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
3. 手动构建说明
4. 退出

请输入选项 (1-4): """)
    
    if choice == "1":
        if check_flet() and build_windows():
            print("\n🎉 构建完成！")
            print("📁 查看 dist/ 目录获取可执行文件")
        else:
            print("\n💡 如果自动构建失败，请尝试手动构建:")
            print("   1. 在当前目录打开命令行")
            print("   2. 运行: flet build windows")
            print("   3. 等待构建完成")
    elif choice == "2":
        clean_build()
        print("✅ 清理完成")
    elif choice == "3":
        print("\n📋 手动构建步骤:")
        print("1. 确保已安装依赖: pip install -r requirements.txt")
        print("2. 在项目根目录运行: flet build windows")
        print("3. 构建完成后在 dist/ 目录中找到可执行文件")
        print("4. 如果遇到编码问题，可以尝试:")
        print("   - 设置环境变量: set PYTHONIOENCODING=utf-8")
        print("   - 然后再运行构建命令")
    elif choice == "4":
        print("👋 再见！")
    else:
        print("❌ 无效选项")
