# -*- coding: utf-8 -*-
import shutil, os, datetime

src = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"
dst_dir = r"C:\사전"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
dst_name = f"【20】O 2179-2182排版页数4-金花顺_교정본_{timestamp}.hwp"
dst = os.path.join(dst_dir, dst_name)

shutil.copy2(src, dst)
print(f"✅ 복사본 생성 완료!")
print(f"   원본: {os.path.basename(src)}")
print(f"   복사본: {dst_name}")
print(f"   경로: {dst}")
print(f"   크기: {round(os.path.getsize(dst)/1024, 1)} KB")
