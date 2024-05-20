# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tinker2_csv.py'],
    pathex=[],
    binaries=[],
    datas=[('csv_app.db', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='tinker2_csv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['python-icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='tinker2_csv',
)
app = BUNDLE(
    coll,
    name='tinker2_csv.app',
    icon='python-icon.icns',
    bundle_identifier=None,
)
