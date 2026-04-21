import shutil, os

src = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\rules_china_place.txt"
dst1 = r"C:\Users\doris\Desktop\xwechat_files\hwp_proofreading_package\rules_china_place.txt"

shutil.copy2(src, dst1)
print(f"Copied to xwechat_files: {os.path.getsize(dst1):,} bytes")

# Also verify all referenced paths
refs = {
    "RULES_FILE": r"C:\Users\doris\Desktop\xwechat_files\hwp_proofreading_package\rules_documentation.txt",
    "CHINA_PLACE_FILE": r"C:\Users\doris\Desktop\xwechat_files\hwp_proofreading_package\rules_china_place.txt",
    "REGEX_FILE": r"C:\AMD\AJ\hwp_proofreading_package\rules_regex.txt",
}

print("\nAll referenced files:")
for name, path in refs.items():
    exists = os.path.exists(path)
    sz = os.path.getsize(path) if exists else 0
    print(f"  {'OK' if exists else 'MISSING'}: {name} = {path} ({sz:,} bytes)")
