# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['entry_point.py'],
    pathex=[],
    binaries=[],
    datas=[('chess/assets/bishop.png', 'assets'), ('chess/assets/boo.mp3', 'assets'), ('chess/assets/clack.mp3', 'assets'), ('chess/assets/correct.wav', 'assets'), ('chess/assets/gameDefinitions.json', 'assets'), ('chess/assets/Hide.png', 'assets'), ('chess/assets/LoginButtonImage.png', 'assets'), ('chess/assets/queen.png', 'assets'), ('chess/assets/rook.png', 'assets'), ('chess/assets/Show.png', 'assets')],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='chessgame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='chessgame.app',
    icon=None,
    bundle_identifier=None,
)
