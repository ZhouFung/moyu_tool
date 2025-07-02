# 防息屏工具 - 构建脚本使用指南

## 📋 构建脚本概览

项目包含两个主要的构建脚本，各有不同的用途：

1. **`optimize_build.py`** - 深度优化构建脚本 (推荐日常使用)
2. **`build_release.py`** - 完整发布构建脚本 (正式发布使用)

---

## 🎯 `optimize_build.py` - 深度优化构建

### 用途
- 生成体积优化的单文件可执行程序
- 从135MB优化到97.1MB (减少28%体积)
- 适合日常开发和测试

### 使用方法
```bash
# 进入项目目录
cd e:\lanzt\moyu_tool

# 运行深度优化构建
python optimize_build.py
```

### 构建过程
1. 自动创建版本信息文件 (`version_info.txt`)
2. 生成优化的PyInstaller spec文件 (`防息屏工具_optimized.spec`)
3. 排除112个无用模块（matplotlib, scipy, pandas等）
4. 过滤不必要的二进制文件
5. 生成优化后的可执行文件

### 输出结果
- **位置**: `dist/防息屏工具.exe`
- **大小**: ~97.1MB
- **特点**: 体积小，功能完整，启动快

### 使用场景
- ✅ 日常开发测试
- ✅ 快速分享给用户
- ✅ 体积敏感的分发场景

---

## 🚀 `build_release.py` - 完整发布构建

### 用途
- 生成完整的发布包
- 包含版本管理、自动打包、上传等功能
- 适合正式发布流程

### 使用方法
```bash
# 进入项目目录
cd e:\lanzt\moyu_tool

# 运行完整发布构建
python build_release.py

# 或者指定特定功能
python build_release.py --pack-only    # 仅打包
python build_release.py --upload-only  # 仅上传
```

### 构建过程
1. 检查环境和依赖
2. 自动获取版本号（从git标签或默认版本）
3. 清理之前的构建文件
4. 使用flet pack或PyInstaller构建
5. 创建发布目录结构
6. 复制必要文件（README、LICENSE等）
7. 压缩成发布包
8. 可选：自动上传到GitHub Release

### 输出结果
- **位置**: `release/防息屏工具_v1.0.0_windows.zip`
- **内容**: 
  - 可执行文件
  - README.md
  - LICENSE
  - 使用说明
  - 版本信息

### 使用场景
- ✅ 正式版本发布
- ✅ GitHub Release发布
- ✅ 需要完整文档的分发
- ✅ 版本管理需求

---

## 📊 两个脚本对比

| 特性         | optimize_build.py | build_release.py |
|------------|-------------------|------------------|
| **主要用途** | 体积优化          | 完整发布         |
| **文件大小** | ~97.1MB           | ~107MB+          |
| **构建速度** | 快                | 较慢             |
| **包含内容** | 仅可执行文件      | 完整发布包       |
| **版本管理** | 无                | 自动版本管理     |
| **文档打包** | 无                | 包含完整文档     |
| **上传功能** | 无                | 支持GitHub上传   |
| **适用场景** | 日常开发测试      | 正式发布         |

---

## 🛠️ 使用建议

### 开发阶段
```bash
# 快速构建测试版本
python optimize_build.py
```

### 发布阶段
```bash
# 生成完整发布包
python build_release.py
```

### 自动化发布
```bash
# 构建并上传到GitHub Release
python build_release.py --auto-release
```

---

## ⚙️ 配置选项

### optimize_build.py 配置
- 修改 `防息屏工具_optimized.spec` 文件可以调整优化参数
- 在脚本中修改 `excludes` 列表可以排除更多模块

### build_release.py 配置
- 修改脚本顶部的 `VERSION` 和 `APP_NAME` 变量
- 配置GitHub token用于自动上传功能

---

## 🚨 注意事项

1. **首次使用前确保安装依赖**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Windows环境**:
   - 确保有足够的磁盘空间（至少2GB）
   - 某些防病毒软件可能会误报，需要添加白名单

3. **构建后测试**:
   - 每次构建后都应该测试可执行文件
   - 特别是optimize_build.py的激进优化可能影响功能

---

## 📞 故障排除

### 常见问题
1. **构建失败**: 检查Python环境和依赖
2. **文件过大**: 使用optimize_build.py
3. **功能缺失**: 检查排除的模块列表
4. **上传失败**: 检查GitHub token配置

### 推荐工作流
```bash
# 1. 开发时使用优化构建
python optimize_build.py

# 2. 测试功能完整性
./dist/防息屏工具.exe

# 3. 发布时使用完整构建
python build_release.py
```
