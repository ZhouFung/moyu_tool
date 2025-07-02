# 🚀 构建脚本快速使用指南

## 快速上手

### 1️⃣ 日常开发 - 使用优化构建
```bash
# 进入项目目录
cd e:\lanzt\moyu_tool

# 一键优化构建（推荐）
python optimize_build.py
```
**结果**: 生成 `dist/防息屏工具.exe` (97.1MB)

### 2️⃣ 正式发布 - 使用完整构建
```bash
# 完整发布包构建
python build_release.py
```
**结果**: 生成 `release/防息屏工具_v1.0.0_Windows绿色版.zip`

---

## 📋 两个脚本的区别

|              | optimize_build.py | build_release.py |
|--------------|-------------------|------------------|
| **输出**     | 单个exe文件       | 完整zip发布包    |
| **大小**     | 97.1MB            | 107MB+           |
| **速度**     | 快 ⚡              | 慢 🐌            |
| **适用场景** | 开发测试          | 正式发布         |

---

## 🎯 推荐使用流程

### 开发阶段
```bash
# 快速构建测试
python optimize_build.py

# 测试功能
.\dist\防息屏工具.exe
```

### 发布阶段
```bash
# 生成发布包
python build_release.py

# 发布包位置: release/ 目录下的zip文件
```

---

## 📁 输出文件说明

### optimize_build.py 输出
```
dist/
└── 防息屏工具.exe     # 97.1MB，体积优化版
```

### build_release.py 输出
```
release/
├── 防息屏工具_v1.0.0_Windows绿色版/
│   ├── 防息屏工具.exe
│   ├── 使用说明.txt
│   ├── README.md
│   ├── LICENSE
│   └── assets/
└── 防息屏工具_v1.0.0_Windows绿色版.zip
```

---

## 🛠️ 常见问题

### Q: 构建失败怎么办？
A: 检查依赖安装
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Q: 文件太大怎么办？ 
A: 使用 `optimize_build.py`，已优化到97.1MB

### Q: 需要完整发布包？
A: 使用 `build_release.py`，包含所有文档和说明

---

## ⚡ 一句话总结

- **开发测试**: `python optimize_build.py` 
- **正式发布**: `python build_release.py`
