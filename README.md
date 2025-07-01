# 摸鱼神器 🐟

一个极简的Python防锁屏工具，低调、优雅、高效。

## ✨ 特色

- 🎯 **极简设计** - 160x120小窗口，不抢夺注意力
- � **一键操作** - 单按钮切换，简单直观
- 🎨 **优雅界面** - 图标+emoji的极简视觉设计
- 🔧 **智能引擎** - 随机移动算法，模拟真实操作
- � **窗口置顶** - 方便随时访问控制

## 🛠️ 技术栈

- **Python 3.7+** - 现代Python开发
- **Flet** - 跨平台UI框架  
- **PyAutoGUI** - 自动化控制库

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 📐 设计哲学

### 极简主义
- **代码精简**: 80行核心代码，易读易维护
- **界面简洁**: 去除一切不必要的视觉元素
- **操作简单**: 一个按钮解决所有问题

### 面向对象
- **MoyuEngine**: 核心业务逻辑封装
- **MoyuUI**: 界面表现逻辑封装
- **职责分离**: 引擎专注功能，UI专注体验

### 用户体验
- **低调隐蔽**: 小窗口设计，不影响工作
- **即时反馈**: 🐟/🐟💨 状态一目了然
- **便捷访问**: 窗口置顶，随时可控

## 注意事项

⚠️ **重要声明**：
- 本工具仅供学习和技术交流使用
- 请在合规的范围内使用，遵守公司规章制度
- 使用过程中产生的任何后果由用户自行承担
- 建议合理使用，避免影响工作效率

## 项目结构

```
moyu_tool/
├── main.py          # 主程序文件
├── requirements.txt # 依赖包列表
├── README.md        # 说明文档
└── build.py         # 打包脚本
```

## 打包发布

运行打包脚本生成可执行文件：
```bash
python build.py
```

## 开源信息

### 许可证
本项目采用 MIT 许可证开源，详情请查看 [LICENSE](LICENSE) 文件。

### 贡献指南
欢迎大家贡献代码和建议！

**如何贡献：**
1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 版权信息
- **作者**: lanzhitu
- **版本**: 1.0.0
- **许可证**: MIT License
- **项目地址**: https://github.com/lanzhitu/moyu-tool

### 致谢
感谢以下开源项目：
- [Flet](https://flet.dev/) - 现代化的Python GUI框架
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Python自动化控制库

### 免责声明
本软件按"原样"提供，不提供任何形式的明示或暗示保证。使用本软件的风险由用户自行承担。开发者不对因使用本软件而导致的任何直接或间接损失承担责任。
