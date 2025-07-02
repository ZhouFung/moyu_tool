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
VERSION = "1.0.1"
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
    """构建可执行文件（优化体积版本）"""
    print(f"🔨 开始构建 {APP_NAME} v{version}（优化体积模式）...")

    # 确保有ICO格式的图标
    has_icon = convert_png_to_ico()
    
    # 基础构建参数
    base_cmd = [
        "flet", "pack", "main.py",
        "--name", APP_NAME,
        "--file-description", f"{APP_NAME} - 防止电脑息屏和网页超时的实用工具",
        "--product-name", APP_NAME,
        "--product-version", version,
        "--add-data", "assets:assets"
    ]
    
    # 添加图标（如果存在）
    if has_icon:
        base_cmd.extend(["--icon", "assets/icon.ico"])
    
    try:
        print("📦 执行基础构建...")
        subprocess.run(base_cmd, check=True)
        
        # 检查生成的文件大小
        exe_path = Path("dist") / f"{APP_NAME}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ 可执行文件构建完成，大小: {size_mb:.1f}MB")
            
            # 尝试UPX压缩（如果可用）
            try_upx_compression(exe_path)
            
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

def try_upx_compression(exe_path):
    """尝试使用UPX压缩可执行文件"""
    try:
        original_size = exe_path.stat().st_size / (1024 * 1024)
        print(f"🗜️ 尝试UPX压缩（原始大小: {original_size:.1f}MB）...")
        
        # 检查UPX是否可用
        result = subprocess.run(["upx", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️ UPX未安装，跳过压缩优化")
            return False
        
        # 执行UPX压缩（添加--force绕过CFG保护）
        backup_path = exe_path.with_suffix('.exe.bak')
        shutil.copy2(exe_path, backup_path)  # 备份原文件
        
        compress_result = subprocess.run([
            "upx", "--best", "--lzma", "--force", str(exe_path)
        ], capture_output=True, text=True)
        
        if compress_result.returncode == 0:
            compressed_size = exe_path.stat().st_size / (1024 * 1024)
            reduction = ((original_size - compressed_size) / original_size) * 100
            print(f"✅ UPX压缩成功: {compressed_size:.1f}MB (减少{reduction:.1f}%)")
            backup_path.unlink()  # 删除备份
            return True
        else:
            print(f"❌ UPX压缩失败: {compress_result.stderr}")
            print("💡 提示：可能是由于Windows CFG保护，这在某些情况下是正常的")
            shutil.copy2(backup_path, exe_path)  # 恢复备份
            backup_path.unlink()
            return False
            
    except FileNotFoundError:
        print("⚠️ UPX未找到，跳过压缩优化")
        print("💡 安装UPX可进一步减小文件体积: https://upx.github.io/")
        return False
    except Exception as e:
        print(f"❌ UPX压缩过程出错: {e}")
        return False

def optimize_for_release():
    """为发布版本优化代码（移除调试信息）"""
    print("🔧 优化发布版本...")
    
    # 创建临时优化版本的文件
    files_to_optimize = ['main.py', 'ui.py', 'engine.py']
    backup_files = []
    
    try:
        for file_path in files_to_optimize:
            if Path(file_path).exists():
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)
                backup_files.append((file_path, backup_path))
                
                # 移除详细的调试打印
                optimize_file_for_release(file_path)
        
        print("✅ 代码优化完成（移除调试信息）")
        return backup_files
        
    except Exception as e:
        print(f"❌ 代码优化失败: {e}")
        # 恢复所有备份文件
        for original, backup in backup_files:
            if Path(backup).exists():
                shutil.copy2(backup, original)
                Path(backup).unlink()
        return []

def optimize_file_for_release(file_path):
    """优化单个文件，移除调试信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除或简化调试打印语句
    lines = content.split('\n')
    optimized_lines = []
    
    for line in lines:
        # 保留重要的错误和状态信息，移除详细调试信息
        if any(debug_keyword in line.lower() for debug_keyword in [
            'print("✅ 防护措施', 'print("🔄 执行', 'print("📱 执行', 
            'print("⌨️ 执行', 'print("🖱️ 执行', 'print("💤 休眠'
        ]):
            # 将详细调试信息转换为简单的状态信息或移除
            continue
        else:
            optimized_lines.append(line)
    
    # 写回优化后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(optimized_lines))

def restore_backup_files(backup_files):
    """恢复备份文件"""
    for original, backup in backup_files:
        if Path(backup).exists():
            shutil.copy2(backup, original)
            Path(backup).unlink()
    print("✅ 已恢复原始文件")

def main():
    """主构建流程（优化版本）"""
    print(f"🎯 {APP_NAME} 发布构建器 (体积优化版)")
    print("=" * 40)

    version = get_version()
    backup_files = []
    
    try:
        # 1. 优化代码（移除调试信息）
        backup_files = optimize_for_release()
        
        # 2. 构建优化的可执行文件
        if not build_executable(version):
            return False
        
        # 3. 创建绿色版发布包
        if not create_portable_package(version):
            return False
        
        print("\n🎉 构建完成！")
        print("=" * 40)
        
        # 显示最终文件大小
        exe_path = Path("dist") / f"{APP_NAME}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 最终可执行文件大小: {size_mb:.1f}MB")
        
        zip_path = Path("release").glob(f"*v{version}*.zip")
        for zp in zip_path:
            zip_size_mb = zp.stat().st_size / (1024 * 1024)
            print(f"📦 发布包大小: {zip_size_mb:.1f}MB")
            break
        
        print("📁 发布文件位置: release/")
        print("📋 接下来可以:")
        print("  1. 测试发布包中的可执行文件")
        print("  2. 运行 python upload_release.py 自动上传到GitHub")
        print("  3. 分享给用户使用")
        
        return True
        
    finally:
        # 恢复原始文件
        if backup_files:
            restore_backup_files(backup_files)

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
