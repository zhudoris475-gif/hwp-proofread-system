import shutil

src = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\rules_china_place.txt"
dst = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"

shutil.copy2(src, dst)
print(f"Copied: {src}")
print(f"  -> {dst}")

import os
print(f"  Size: {os.path.getsize(dst):,} bytes")
print(f"  Exists: {os.path.exists(dst)}")
