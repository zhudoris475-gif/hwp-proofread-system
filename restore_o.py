# -*- coding: utf-8 -*-
import shutil, os

src = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp.bak"
dst = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"

shutil.copy2(src, dst)
print(f"✅ 백업에서 복원 완료!")
print(f"   원본: {src}")
print(f"   복원: {dst}")
print(f"   크기: {round(os.path.getsize(dst)/1024, 1)} KB")
