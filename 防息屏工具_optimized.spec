# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 排除不需要的模块
excludes = [
    'tkinter', 'tkinter.*',
    'matplotlib', 'matplotlib.*',
    'numpy', 'numpy.*',  # 很遗憾，Flet需要numpy
    'scipy', 'scipy.*',
    'pandas', 'pandas.*',
    'IPython', 'IPython.*',
    'jupyter', 'jupyter.*',
    'notebook', 'notebook.*',
    'sphinx', 'sphinx.*',
    'docutils', 'docutils.*',
    'test', 'test.*',
    'unittest', 'unittest.*',
    'xml', 'xml.*',
    'email', 'email.*',
    'pydoc', 'pydoc.*',
    'distutils', 'distutils.*',
    'lib2to3', 'lib2to3.*',
    'multiprocessing.pool',
    'multiprocessing.dummy',
]

# 隐藏导入（Flet需要的）
hiddenimports = [
    'flet.app',
    'flet.control_event',
    'flet.control',
    'flet.utils',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 移除不必要的文件
a.binaries = [x for x in a.binaries if not any(exclude in x[0].lower() for exclude in [
    'test', 'example', 'sample', 'demo',
    'tcl8', 'tk8',  # 如果不需要tkinter
    # 注意：不能排除太多，否则Flet可能无法运行
])]

# 移除重复的DLL
a.binaries = list({x[0]: x for x in a.binaries}.values())

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='防息屏工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 移除调试信息
    upx=False,   # 禁用UPX（效果不佳）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='version_info.txt'
)
