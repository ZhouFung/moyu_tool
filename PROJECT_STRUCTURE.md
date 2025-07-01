# 项目结构

```
moyu_tool/
├── main.py              # 主程序文件
├── flet_build.py        # 构建脚本 (Windows)
├── requirements.txt     # Python依赖
├── pyproject.toml       # 项目配置
├── README.md           # 项目说明
├── CONTRIBUTING.md     # 贡献指南
├── CHANGELOG.md        # 更新日志
├── LICENSE             # MIT许可证
├── assets/             # 资源文件
│   └── icon.png        # 应用图标
└── build/              # 构建输出目录
    └── windows/        # Windows 构建结果
        └── moyu_tool.exe # Windows可执行文件
```

## 核心文件说明

### 必需文件
- `main.py` - 应用主程序，包含 MoyuEngine 和 MoyuUI 类
- `flet_build.py` - 简化的构建脚本，专注 Windows 平台
- `requirements.txt` - 最小化依赖清单 (flet, pyautogui, Pillow)
- `pyproject.toml` - 精简的项目配置

### 资源文件
- `assets/icon.png` - 应用图标 (PNG格式，适用于Flet)

### 文档文件
- `README.md` - 用户使用指南
- `CONTRIBUTING.md` - 开发者贡献指南
- `CHANGELOG.md` - 版本更新记录

## 已移除的文件
- ~~`build.py`~~ - 旧的 PyInstaller 构建脚本
- ~~`摸鱼神器.spec`~~ - PyInstaller 配置文件
- ~~`assets/icon.ico`~~ - ICO格式图标 (已替换为PNG)
- ~~`build/`~~ - PyInstaller 构建缓存目录

项目现在更加简洁，专注于核心功能。
