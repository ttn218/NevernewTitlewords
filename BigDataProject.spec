# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BigDataProject.py'],
             pathex=['C:\\Users\\ttn21\\OneDrive\\바탕 화면\\BigData'],
             binaries=[],
             datas=[("C:/Users/ttn21/anaconda3/Lib/site-packages/konlpy/", "./konlpy"), ("C:/Users/ttn21/anaconda3/Lib/site-packages/konlpy/java/", "./konlpy/java"), ("C:/Users/ttn21/anaconda3/Lib/site-packages/konlpy/data/tagset/*", "./konlpy/data/tagset"),("./stopword.txt", "./")],
             hiddenimports=["kr.lucypark.okt"],
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
          name='BigDataProject',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
