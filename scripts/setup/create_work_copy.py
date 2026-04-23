# -*- coding: utf-8 -*-
import shutil, os, datetime

src = r"C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp"
dst_dir = r"C:\Users\doris\Desktop\xwechat_files\WORD"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
dst_name = f"【20】O 2179-2182排版页数4-金花顺_작업본_inplace_{ts}.hwp"
dst = os.path.join(dst_dir, dst_name)

shutil.copy2(src, dst)
print(f"✅ 작업본 복사 완료!")
print(f"   경로: {dst}")
print(f"   크기: {round(os.path.getsize(dst)/1024, 1)} KB")
print(f"   → 제자리(in-place) 교정 가능!")
