"""
发布前检查脚本
确保项目处于最佳发布状态
"""

import os
import sys
from pathlib import Path

def check_required_files():
    """检查必需文件是否存在"""
    print("🔍 检查必需文件...")
    
    required_files = [
        'main.py',
        'ui.py', 
        'engine.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
        'optimize_build.py',
        'build_release.py',
        'assets/icon.png'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必需文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print(f"✅ 所有必需文件已就绪 ({len(required_files)} 个)")
        return True

def check_cleanup():
    """检查是否有需要清理的文件"""
    print("\n🧹 检查需要清理的文件...")
    
    cleanup_patterns = [
        ('build/', 'PyInstaller构建缓存'),
        ('dist/', '之前的构建产物'),
        ('__pycache__/', 'Python缓存'),
        ('*.pyc', 'Python字节码'),
        ('*.log', '日志文件'),
        ('*.tmp', '临时文件'),
    ]
    
    found_cleanup = []
    for pattern, description in cleanup_patterns:
        if '*' in pattern:
            # 通配符模式
            if list(Path('.').glob(f"**/{pattern}")):
                found_cleanup.append((pattern, description))
        else:
            # 目录或文件
            if Path(pattern).exists():
                found_cleanup.append((pattern, description))
    
    if found_cleanup:
        print("⚠️ 发现需要清理的文件:")
        for pattern, desc in found_cleanup:
            print(f"   - {pattern} ({desc})")
        print("\n💡 建议运行构建脚本前先清理这些文件")
        return False
    else:
        print("✅ 项目目录干净，可以构建")
        return True

def check_git_status():
    """检查Git状态"""
    print("\n📝 检查Git状态...")
    
    try:
        import subprocess
        
        # 检查是否有未提交的更改
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            if result.stdout.strip():
                print("⚠️ 发现未提交的更改:")
                print(result.stdout)
                print("💡 建议先提交所有更改再发布")
                return False
            else:
                print("✅ Git工作区干净")
                return True
        else:
            print("ℹ️ 无法检查Git状态（可能不是Git仓库）")
            return True
            
    except FileNotFoundError:
        print("ℹ️ Git未安装，跳过Git状态检查")
        return True
    except Exception as e:
        print(f"⚠️ Git状态检查出错: {e}")
        return True

def check_dependencies():
    """检查依赖是否安装"""
    print("\n📦 检查Python依赖...")
    
    required_packages = [
        ('flet', 'flet'),
        ('pyautogui', 'pyautogui'), 
        ('pillow', 'PIL'),
        ('pyinstaller', 'PyInstaller')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name.replace('-', '_'))
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ 缺少必需的Python包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 运行: pip install -r requirements.txt")
        return False
    else:
        print(f"✅ 所有依赖已安装 ({len(required_packages)} 个)")
        return True

def suggest_build_command():
    """建议构建命令"""
    print("\n🚀 建议的构建流程:")
    print("=" * 40)
    print("1. 快速测试构建:")
    print("   python optimize_build.py")
    print()
    print("2. 测试可执行文件:")
    print("   .\\dist\\防息屏工具.exe")
    print()
    print("3. 正式发布构建:")
    print("   python build_release.py")
    print()
    print("4. 检查发布包:")
    print("   ls release/")

def main():
    """主检查流程"""
    print("🎯 防息屏工具 - 发布前检查")
    print("=" * 50)
    
    all_checks = [
        check_required_files(),
        check_dependencies(),
        check_cleanup(),
        check_git_status()
    ]
    
    print("\n" + "=" * 50)
    
    if all(all_checks):
        print("🎉 所有检查通过！项目已准备就绪")
        suggest_build_command()
        return True
    else:
        print("⚠️ 部分检查未通过，请先解决问题")
        failed_count = len([x for x in all_checks if not x])
        passed_count = len([x for x in all_checks if x])
        print(f"📊 检查结果: {passed_count} 通过, {failed_count} 需要处理")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
