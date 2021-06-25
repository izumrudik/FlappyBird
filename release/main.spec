# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['<ENTER FULL PATH TO\\main.py>'],
             binaries=[],
             datas=[('images\\bg.png','images'),
			 ('images\\bird1.png','images'),
			 ('images\\bird2.png','images'),
			 ('images\\bird3.png','images'),
			 ('images\\pipe.png','images'),
			 ('neat_stuff\\config-feedforward.txt','neat_stuff'),
			 ('neat_stuff\\best.pkl','neat_stuff')
			 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
