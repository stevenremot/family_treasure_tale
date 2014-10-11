# -*- mode: python -*-
a = Analysis(['run_game.py'],
             pathex=['/home/steven/Documents/PyWeek/family_treasure_tale'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='family_treasure',
          debug=True,
          strip=None,
          upx=True,
          console=True , resources=['data'])
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='family_treasure')
