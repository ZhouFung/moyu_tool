"""
防息屏工具 - 极致体积优化构建脚本
通过创建自定义的spec文件来更精确控制打包过程
"""

import subprocess
import shutil
import os
from pathlib import Path

def create_optimized_spec():
    """创建优化的PyInstaller spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
'''
    
    with open('防息屏工具_optimized.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 创建优化的spec文件")

def create_version_info():
    """创建版本信息文件"""
    version_info = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'080404b0',
          [StringStruct(u'CompanyName', u'个人开发者'),
           StringStruct(u'FileDescription', u'防息屏工具 - 防止电脑息屏和网页超时的实用工具'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'InternalName', u'防息屏工具'),
           StringStruct(u'LegalCopyright', u'Copyright © 2025'),
           StringStruct(u'OriginalFilename', u'防息屏工具.exe'),
           StringStruct(u'ProductName', u'防息屏工具'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ 创建版本信息文件")

def build_with_optimized_spec():
    """使用优化的spec文件构建"""
    print("🔨 开始极致优化构建...")
    
    # 清理之前的构建
    if Path("dist").exists():
        shutil.rmtree("dist")
    if Path("build").exists():
        shutil.rmtree("build")
    
    try:
        # 使用PyInstaller直接构建
        cmd = [
            "pyinstaller", 
            "防息屏工具_optimized.spec",
            "--clean",
            "--noconfirm"
        ]
        
        subprocess.run(cmd, check=True)
        
        # 检查结果
        exe_path = Path("dist") / "防息屏工具.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ 极致优化构建完成，大小: {size_mb:.1f}MB")
            return True
        else:
            print("❌ 构建失败：未找到可执行文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def main():
    """主优化流程"""
    print("🎯 防息屏工具 - 极致体积优化构建器")
    print("=" * 40)
    
    # 1. 创建优化文件
    create_version_info()
    create_optimized_spec()
    
    # 2. 执行优化构建
    if build_with_optimized_spec():
        print("\n🎉 极致优化构建成功！")
        print("💡 如果这个版本可以正常运行，说明优化成功")
        print("⚠️ 如果运行出错，请使用标准构建版本")
    else:
        print("\n❌ 极致优化构建失败")
        print("💡 请检查依赖或使用标准构建脚本")

if __name__ == "__main__":
    main()
