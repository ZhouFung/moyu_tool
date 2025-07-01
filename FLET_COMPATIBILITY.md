# Flet 版本兼容性说明

## 当前使用版本

本项目目前使用的 Flet 版本支持以下 API：
- ✅ `ft.app()` - 主应用启动函数
- ✅ `assets_dir` 参数 - 资源目录配置
- ❌ `ft.run()` - 新版本 API（当前版本不支持）
- ❌ `name`, `description`, `version` 参数 - 不支持的参数

## API 使用

```python
# 当前兼容的用法
ft.app(
    target=main,
    assets_dir="assets"
)

# 避免使用不支持的参数
# ft.app(
#     target=main,
#     assets_dir="assets",
#     name="摸鱼神器",        # ❌ 不支持
#     description="防锁屏工具", # ❌ 不支持  
#     version="1.0.0"       # ❌ 不支持
# )
```

## 升级建议

如果您想使用最新的 Flet API，可以考虑升级 Flet：

```bash
pip install --upgrade flet
```

升级后可以使用新的 API：
```python
ft.run(target=main, assets_dir="assets")
```

## 构建兼容性

当前的构建配置与您的 Flet 版本完全兼容：
- ✅ `flet build windows` 命令正常工作
- ✅ 生成的可执行文件功能完整
- ✅ assets 目录正确加载

项目已针对当前版本优化，无需额外配置即可正常使用。
