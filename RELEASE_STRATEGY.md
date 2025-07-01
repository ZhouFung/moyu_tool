# Windows 版本发布策略指南

## 🎯 推荐方案：绿色版（非安装版）+ 可选安装包

### 为什么选择绿色版作为主要发布方式？

#### ✅ 绿色版优势
1. **即下即用**：下载后直接双击运行，无需安装
2. **无系统污染**：不写注册表，不留残留文件
3. **便携性强**：可放在U盘、网盘，随身携带
4. **权限友好**：普通用户权限即可运行，无需管理员
5. **卸载简单**：直接删除文件夹即可
6. **信任度高**：用户更信任不需要安装的工具

#### 🎯 适合场景
- 公司电脑（通常限制安装软件）
- 临时使用需求
- 不想污染系统的用户
- 技术人员和极客用户

## 📦 发布文件结构

### 主要发布：绿色版
```
防息屏工具_v1.0.0_Windows绿色版.zip
├── 防息屏工具.exe          # 主程序
├── assets/                 # 资源文件夹
│   └── icon.png
├── 使用说明.txt            # 简单说明
└── README.md              # 详细文档
```

### 可选发布：安装版
```
防息屏工具_v1.0.0_Windows安装版.exe
# 使用 Inno Setup 或 NSIS 制作的安装包
```

## 🛠️ 文件命名规范

### 文件名格式
```
[软件名]_v[版本号]_[系统]_[类型].[扩展名]

示例：
- 防息屏工具_v1.0.0_Windows_绿色版.zip
- 防息屏工具_v1.0.0_Windows_安装版.exe
- 防息屏工具_v1.0.0_源码.zip
```

### GitHub Release 资产建议
```
📁 Release Assets:
├── 🟢 防息屏工具_v1.0.0_Windows绿色版.zip    [主推荐]
├── 📦 防息屏工具_v1.0.0_Windows安装版.exe    [可选]
├── 💾 Source_code.zip                        [自动生成]
└── 💾 Source_code.tar.gz                     [自动生成]
```

## 📋 用户使用说明

### 绿色版使用方法
```markdown
## 🚀 快速开始

### 方法一：绿色版（推荐）⭐
1. 下载 `防息屏工具_v1.0.0_Windows绿色版.zip`
2. 解压到任意文件夹
3. 双击 `防息屏工具.exe` 运行
4. 点击"开始保护"即可

### 方法二：安装版
1. 下载 `防息屏工具_v1.0.0_Windows安装版.exe`
2. 右键"以管理员身份运行"
3. 按提示完成安装
4. 从开始菜单启动程序

## ⚠️ 注意事项
- 首次运行可能被杀毒软件误报，请添加信任
- 程序需要鼠标操作权限才能正常工作
- 建议将程序固定到任务栏方便使用
```

## 🔧 构建脚本优化

让我更新 flet build 命令以生成最佳的发布版本：

```python
# build.py - 优化的构建脚本
import subprocess
import shutil
import zipfile
from pathlib import Path

def build_app():
    """构建应用程序"""
    print("🔨 开始构建防息屏工具...")
    
    # 1. 使用 flet pack 打包（生成单个exe文件）
    cmd = [
        "flet", "pack", "main.py",
        "--name", "防息屏工具",
        "--icon", "assets/icon.ico",
        "--add-data", "assets:assets",
        "--onefile",  # 生成单个exe文件
        "--noconsole"  # 不显示控制台窗口
    ]
    
    subprocess.run(cmd, check=True)
    
    # 2. 创建绿色版发布包
    create_portable_package()

def create_portable_package():
    """创建绿色版发布包"""
    print("📦 创建绿色版发布包...")
    
    version = "v1.0.0"  # 从版本文件读取
    dist_dir = Path("dist")
    release_dir = Path(f"release/防息屏工具_{version}_Windows绿色版")
    
    # 创建发布目录
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    files_to_copy = [
        ("dist/防息屏工具.exe", "防息屏工具.exe"),
        ("assets", "assets"),
        ("README.md", "README.md"),
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        dst_path = release_dir / dst
        
        if src_path.is_file():
            shutil.copy2(src_path, dst_path)
        elif src_path.is_dir():
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    
    # 创建使用说明
    create_usage_guide(release_dir)
    
    # 打包为zip
    zip_path = f"release/防息屏工具_{version}_Windows绿色版.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in release_dir.rglob('*'):
            if file_path.is_file():
                arc_path = file_path.relative_to(release_dir.parent)
                zf.write(file_path, arc_path)
    
    print(f"✅ 绿色版发布包已创建: {zip_path}")

def create_usage_guide(release_dir):
    """创建使用说明文件"""
    guide_content = """防息屏工具 - 使用说明

🚀 快速开始
1. 双击"防息屏工具.exe"启动程序
2. 点击"开始保护"按钮
3. 程序将在后台自动工作，防止电脑息屏

⚠️ 注意事项
- 首次运行可能被杀毒软件拦截，请选择"允许"
- 程序运行时会微调鼠标位置（不可见），这是正常现象
- 关闭程序前记得点击"停止保护"

🔧 功能说明
- 防止电脑自动锁屏
- 防止网页会话超时
- 30-60秒智能间隔
- 资源占用极低

📞 技术支持
- GitHub: https://github.com/your-username/moyu-tool
- 问题反馈: https://github.com/your-username/moyu-tool/issues

版权所有 © 2025 | MIT License
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)

if __name__ == "__main__":
    build_app()
```

## 📊 用户偏好分析

### 不同用户群体的偏好

| 用户类型 | 绿色版     | 安装版     | 原因                     |
|------|----------|----------|------------------------|
| 企业用户 | ✅ 强烈推荐 | ❌ 限制安装 | 公司电脑通常禁止安装软件 |
| 个人用户 | ✅ 推荐     | ⚪ 可选     | 喜欢简单、无污染          |
| 技术用户 | ✅ 强烈推荐 | ❌ 不需要   | 偏爱绿色、便携工具        |
| 普通用户 | ✅ 推荐     | ⚪ 可选     | 安装版可能更熟悉         |

### 💡 最佳实践建议

1. **主推绿色版**：在 GitHub Release 页面突出显示
2. **提供安装版**：满足部分用户的传统习惯
3. **详细说明**：在 README 中说明两种版本的区别
4. **文件大小**：绿色版通常更小，下载更快

## 🎯 发布页面描述模板

```markdown
## 📦 下载选择

### 🟢 绿色版（推荐）
**适合大多数用户，即下即用**
- 📁 `防息屏工具_v1.0.0_Windows绿色版.zip` (2.5MB)
- ✅ 无需安装，解压即用
- ✅ 适合公司电脑使用
- ✅ 无系统污染，删除即卸载

### 📦 安装版（可选）
**喜欢传统安装方式的用户**
- 📁 `防息屏工具_v1.0.0_Windows安装版.exe` (3.2MB)
- ℹ️ 需要管理员权限安装
- ℹ️ 自动创建桌面快捷方式
- ℹ️ 通过控制面板卸载

### 💻 系统要求
- Windows 10/11 (64位)
- 无需额外依赖

### 🚀 推荐使用绿色版的原因
1. **更安全**：不需要管理员权限
2. **更便携**：可以放在U盘随身携带
3. **更干净**：不修改注册表和系统文件
4. **更快速**：下载后立即使用
```

**结论：对于您的防息屏工具，绿色版是最佳选择！用户会更喜欢这种简单、安全、便携的方式。** 🎯
