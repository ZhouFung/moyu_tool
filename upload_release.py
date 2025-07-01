"""
GitHub Release 自动发布脚本
使用 GitHub CLI 创建 Release 并上传文件
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def check_gh_cli():
    """检查 GitHub CLI 是否安装"""
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI 已安装")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ 未检测到 GitHub CLI")
    print("请先安装 GitHub CLI: https://cli.github.com/")
    print("或者手动上传到 GitHub Release 页面")
    return False

def check_git_auth():
    """检查 GitHub 认证状态"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        # 检查输出中是否包含登录成功的标识
        output = result.stdout + result.stderr
        if "Logged in to github.com" in output or "Active account: true" in output:
            print("✅ GitHub 已登录")
            return True
    except:
        pass
    
    print("❌ 未登录 GitHub")
    print("请运行: gh auth login")
    return False

def get_release_info():
    """获取发布信息"""
    info_file = Path("release/release_info_v1.0.0.json")
    if info_file.exists():
        with open(info_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def create_release_notes():
    """生成 Release 说明"""
    info = get_release_info()
    version = info['version'] if info else "1.0.0"
    
    notes = f"""# 防息屏工具 v{version}

## 🎉 新版本发布

一款现代化、美观、专业的防息屏与防网页超时工具。

## ✨ 主要功能

- **智能防息屏**：防止电脑自动锁屏
- **防网页超时**：保持网页登录状态不掉线
- **现代化UI**：简洁美观的用户界面
- **一键操作**：单击即可启动/停止保护
- **绿色免安装**：下载即用，无需安装

## 📦 下载说明

### 🟢 推荐下载：绿色版
- **文件名**：`防息屏工具_v{version}_Windows绿色版.zip`
- **适用系统**：Windows 10/11 (64位)
- **使用方法**：解压后直接运行 `防息屏工具.exe`

## 🚀 快速开始

1. 下载上面的绿色版压缩包
2. 解压到任意文件夹
3. 双击运行 `防息屏工具.exe`
4. 点击"开始保护"按钮即可

## ⚠️ 重要提醒

- 首次运行可能被杀毒软件误报，请选择"允许"
- 程序运行时会微调鼠标位置（1-2像素），这是正常现象
- 本程序为绿色软件，删除文件夹即可完全卸载

## 🔧 适用场景

- 在线学习/工作时保持页面活跃
- 演示/展示时防止屏幕自动关闭
- 下载大文件时保持电脑运行状态
- 公司电脑防止自动锁屏（无需安装权限）

## 📞 技术支持

如有问题请在 [Issues](https://github.com/lanzhitu/moyu-tool/issues) 页面反馈。

---
感谢使用防息屏工具！⭐ 如果觉得好用，请给个 Star 支持一下～
"""
    return notes

def create_github_release():
    """创建 GitHub Release"""
    if not check_gh_cli():
        return False
    
    if not check_git_auth():
        return False
    
    # 获取版本信息
    info = get_release_info()
    version = info['version'] if info else "1.0.0"
    tag = f"v{version}"
    
    # 检查发布文件
    zip_file = Path(f"release/防息屏工具_v{version}_Windows绿色版.zip")
    if not zip_file.exists():
        print(f"❌ 发布文件不存在: {zip_file}")
        return False
    
    print(f"🚀 准备创建 GitHub Release v{version}")
    
    # 生成发布说明
    notes = create_release_notes()
    notes_file = Path("release/RELEASE_NOTES.md")
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(notes)
    
    # 创建 Release
    cmd = [
        'gh', 'release', 'create', tag,
        str(zip_file),  # 上传的文件
        '--title', f'防息屏工具 v{version}',
        '--notes-file', str(notes_file),
        '--latest'  # 标记为最新版本
    ]
    
    try:
        print("📤 正在创建 GitHub Release...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("✅ GitHub Release 创建成功!")
        print(f"🔗 Release 链接: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建 Release 失败: {e}")
        print(f"错误信息: {e.stderr}")
        return False

def manual_upload_instructions():
    """手动上传说明"""
    print("""
📋 手动上传到 GitHub Release 的步骤：

1. 打开您的 GitHub 仓库页面
2. 点击右侧的 "Releases" 或直接访问：
   https://github.com/lanzhitu/moyu-tool/releases

3. 点击 "Create a new release" 按钮

4. 填写发布信息：
   - Tag version: v1.0.0
   - Release title: 防息屏工具 v1.0.0
   - Description: 复制下面的发布说明

5. 上传文件：
   - 将 release/防息屏工具_v1.0.0_Windows绿色版.zip 拖拽到文件上传区域

6. 勾选 "Set as the latest release"

7. 点击 "Publish release" 完成发布

📝 发布说明文本已保存到: release/RELEASE_NOTES.md
您可以复制其中的内容作为 Release 描述。
""")

def main():
    """主函数"""
    print("🎯 GitHub Release 发布工具")
    print("=" * 40)
    
    # 尝试自动创建 Release
    if create_github_release():
        return
    
    # 如果自动创建失败，提供手动上传说明
    create_release_notes()  # 确保生成发布说明文件
    notes_file = Path("release/RELEASE_NOTES.md")
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(create_release_notes())
    
    manual_upload_instructions()

if __name__ == "__main__":
    main()
