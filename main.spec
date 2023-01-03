# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    [
        'src\\main.py',
        'src\\config.py',
        'src\\protocols\\__init__.py',
        'src\\protocols\\btp.py',
        'src\\protocols\\btp_lru.py',
        'src\\protocols\\http.py',
        'src\\proxy\\__init__.py',
        'src\\proxy\\bad_proxy.py',
        'src\\proxy\\inbound.py',
        'src\\proxy\\outbound.py',
    ],
    pathex=['C:\\Users\\wang.weiran\\Documents\\code\\wproxy\\src'],
    binaries=[],
    datas=[('conf\\config.json', 'conf')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
