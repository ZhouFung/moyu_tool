"""
防息屏工具 - 优化构建脚本
生成用户友好的绿色版发布包
"""

import subprocess
import shutil
import zipfile
import json
from pathlib import Path
from datetime import datetime

# 版本信息
VERSION = "1.0.0"
APP_NAME = "防息屏工具"

def get_version():
    """获取版本号"""
    try:
        # 从git标签获取版本
        result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().lstrip('v')
    except:
        pass
    return VERSION

def build_executable(version):
    """构建可执行文件"""
    print(f"🔨 开始构建 {APP_NAME} v{version}...")

    # 确保有ICO格式的图标
    if not convert_png_to_ico():
        print("⚠️ 图标转换失败，将不使用图标")
        cmd = [
            "flet", "pack", "main.py",
            "--name", APP_NAME,
            "--add-data", "assets:assets",
            "--file-description", f"{APP_NAME} - 防止电脑息屏和网页超时的实用工具",
            "--product-name", APP_NAME,
            "--product-version", version
        ]
    else:
        cmd = [
            "flet", "pack", "main.py",
            "--name", APP_NAME,
            "--add-data", "assets:assets",
            "--icon", "assets/icon.ico",  # 使用转换后的 ICO 文件
            "--file-description", f"{APP_NAME} - 防止电脑息屏和网页超时的实用工具",
            "--product-name", APP_NAME,
            "--product-version", version
        ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 可执行文件构建完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_portable_package(version):
    """创建绿色版发布包"""
    print(f"📦 创建绿色版发布包 v{version}...")
    
    # 创建发布目录
    release_name = f"{APP_NAME}_v{version}_Windows绿色版"
    release_dir = Path("release") / release_name
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制主程序
    exe_source = Path("dist") / f"{APP_NAME}.exe"
    exe_target = release_dir / f"{APP_NAME}.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_target)
        print(f"✅ 复制主程序: {exe_target}")
    else:
        print(f"❌ 未找到可执行文件: {exe_source}")
        return False
    
    # 复制资源文件
    assets_source = Path("assets")
    if assets_source.exists():
        assets_target = release_dir / "assets"
        shutil.copytree(assets_source, assets_target, dirs_exist_ok=True)
        print("✅ 复制资源文件")
    
    # 创建使用说明
    create_user_guide(release_dir, version)
    
    # 复制重要文档
    docs = ["README.md", "LICENSE"]
    for doc in docs:
        doc_path = Path(doc)
        if doc_path.exists():
            shutil.copy2(doc_path, release_dir / doc)
    
    # 创建ZIP压缩包
    zip_path = Path("release") / f"{release_name}.zip"
    create_zip_package(release_dir, zip_path)
    
    # 生成发布信息
    create_release_info(version, zip_path)
    
    return True

def create_user_guide(release_dir, version):
    """创建用户使用指南"""
    guide_content = f"""{APP_NAME} v{version} - 使用指南

🚀 快速开始
═══════════════════════════════════════
1. 双击"{APP_NAME}.exe"启动程序
2. 点击"开始保护"按钮
3. 程序开始工作，防止电脑息屏和网页超时

⭐ 功能特色
═══════════════════════════════════════
• 智能防息屏：防止电脑自动锁屏
• 防网页超时：保持网页登录状态
• 微动保护：30-60秒智能间隔微调鼠标
• 绿色软件：无需安装，即下即用
• 资源友好：占用内存极低，不影响系统性能

⚠️ 重要提醒
═══════════════════════════════════════
• 首次运行可能被杀毒软件误报，请选择"允许"
• 程序运行时会微调鼠标位置（1-2像素），这是正常现象
• 建议关闭程序前先点击"停止保护"
• 本程序为绿色软件，删除文件夹即可完全卸载

🔧 适用场景
═══════════════════════════════════════
• 在线学习/工作时保持页面活跃
• 演示/展示时防止屏幕自动关闭
• 下载大文件时保持电脑运行状态
• 公司电脑防止自动锁屏（无需安装权限）

📞 技术支持
═══════════════════════════════════════
• 项目主页: https://github.com/lanzhitu/moyu-tool
• 问题反馈: https://github.com/lanzhitu/moyu-tool/issues
• 版本更新: 关注GitHub Release页面

💡 小贴士
═══════════════════════════════════════
• 可以将程序放在桌面或任务栏，方便随时使用
• 支持开机自启动（在程序设置中启用）
• 可以最小化到系统托盘，不占用任务栏空间

═══════════════════════════════════════
版权所有 © {datetime.now().year} | MIT License
感谢使用 {APP_NAME}！
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ 创建使用说明")

def create_zip_package(source_dir, zip_path):
    """创建ZIP压缩包"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                arc_path = file_path.relative_to(source_dir.parent)
                zf.write(file_path, arc_path)
    
    # 计算文件大小
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ 创建压缩包: {zip_path} ({size_mb:.1f}MB)")

def create_release_info(version, zip_path):
    """生成发布信息"""
    release_info = {
        "version": version,
        "build_time": datetime.now().isoformat(),
        "files": [
            {
                "name": zip_path.name,
                "size": zip_path.stat().st_size,
                "type": "绿色版",
                "description": "即下即用，无需安装"
            }
        ],
        "system_requirements": [
            "Windows 10/11 (64位)",
            "无需额外依赖"
        ],
        "features": [
            "智能防息屏保护",
            "防网页超时退出", 
            "现代化UI界面",
            "一键启停控制",
            "绿色免安装"
        ]
    }
    
    info_path = Path("release") / f"release_info_v{version}.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成发布信息: {info_path}")

def convert_png_to_ico():
    """将PNG图标转换为ICO格式"""
    png_path = Path("assets/icon.png")
    ico_path = Path("assets/icon.ico")
    
    if not png_path.exists():
        print("❌ 未找到 PNG 图标文件")
        return False
    
    if ico_path.exists():
        print("✅ ICO 图标文件已存在")
        return True
    
    try:
        from PIL import Image
        
        # 打开PNG图像
        img = Image.open(png_path)
        
        # 转换为ICO格式，包含多个尺寸
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("✅ 成功转换 PNG 为 ICO 格式")
        return True
        
    except ImportError:
        print("❌ 需要安装 Pillow 库: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ 转换图标失败: {e}")
        return False

def main():
    """主构建流程"""
    print(f"🎯 {APP_NAME} 发布构建器")
    print("=" * 40)

    version = get_version()
    
    # 1. 构建可执行文件
    if not build_executable(version):
        return False
    
    # 2. 创建绿色版发布包
    if not create_portable_package(version):
        return False
    
    # 3. 转换图标
    convert_png_to_ico()
    
    print("\n🎉 构建完成！")
    print("=" * 40)
    print("📁 发布文件位置: release/")
    print("📋 接下来可以:")
    print("  1. 测试发布包中的可执行文件")
    print("  2. 上传到GitHub Release")
    print("  3. 分享给用户使用")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ 构建被用户取消")
        exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程出现错误: {e}")
        exit(1)
