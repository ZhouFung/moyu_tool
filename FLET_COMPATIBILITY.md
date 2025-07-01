# Flet 版本兼容性说明

## 当前使用版本

本项目已升级到 **Flet 0.28.3**，支持以下 API：
- ✅ `ft.app()` - 主应用启动函数
- ✅ `name` 参数 - 应用名称设置（新版本支持）
- ✅ `assets_dir` 参数 - 资源目录配置
- ✅ `view`, `host`, `port` 等高级参数
- ❌ `ft.run()` - 此版本中尚未引入

## API 使用

```python
# 当前版本推荐用法
ft.app(
    target=main,
    name="摸鱼神器",
    assets_dir="assets"
)

# 更多可用参数
ft.app(
    target=main,
    name="摸鱼神器",
    assets_dir="assets",
    view=ft.AppView.FLET_APP,
    port=0
)
```

## 版本特性

### Flet 0.28.3 的改进
- ✅ 更稳定的构建系统
- ✅ 改进的资源处理
- ✅ 更好的跨平台支持
- ✅ 增强的 API 参数支持

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
