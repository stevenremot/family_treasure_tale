# -*- mode: python -*-
a = Analysis(['run_game.py'],
             pathex=['family_treasure_tale'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('data', prefix='data'),
          name='family_treasure.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
