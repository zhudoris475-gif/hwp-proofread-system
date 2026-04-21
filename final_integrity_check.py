import os, hashlib, datetime, json

def md5(f):
    h = hashlib.md5()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

src_hwp = r'C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp'
src_md5 = md5(src_hwp)
src_size = os.path.getsize(src_hwp)
src_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(src_hwp))

print("=" * 60)
print("4단계: 전체 파일 무결성 체크 및 동기화 최종 확인")
print("=" * 60)

print(f"\n원본 파일: {src_hwp}")
print(f"  크기: {src_size:,} bytes")
print(f"  수정일: {src_mtime}")
print(f"  MD5: {src_md5}")

locations = {
    "新词典 (원본)": r'C:\Users\doris\Desktop\新词典',
    "AMD\\AJ\\hwp_proofreading_package": r'C:\AMD\AJ\hwp_proofreading_package',
    "AMD\\AJ\\hwp_proofreading_package\\hwp_work": r'C:\AMD\AJ\hwp_proofreading_package\hwp_work',
    "xwechat_files\\WORD": r'C:\Users\doris\Desktop\xwechat_files\WORD',
}

print("\n--- 4-1: 전체 HWP 파일 인벤토리 및 MD5 체크 ---")
all_files = []
for label, loc in locations.items():
    if not os.path.exists(loc):
        print(f"\n  [{label}] 디렉토리 없음: {loc}")
        continue
    print(f"\n  [{label}] {loc}")
    hwp_files = []
    for f in sorted(os.listdir(loc)):
        if f.endswith('.hwp') and '2179' in f and '2182' in f:
            fp = os.path.join(loc, f)
            sz = os.path.getsize(fp)
            mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
            h = md5(fp)
            is_latest = (sz == src_size and h == src_md5)
            mark = "⭐ 최신" if is_latest else ("📋 이전" if sz != src_size else "⚠️ 동일크기/다른내용")
            print(f"    {mark} {f}")
            print(f"         크기={sz:,}  수정={mt}  MD5={h}")
            all_files.append({
                "location": label,
                "path": fp,
                "name": f,
                "size": sz,
                "mtime": str(mt),
                "md5": h,
                "is_latest": is_latest
            })

latest_count = sum(1 for f in all_files if f["is_latest"])
old_count = sum(1 for f in all_files if not f["is_latest"])

print(f"\n--- 4-2: 동기화 상태 요약 ---")
print(f"  최신 버전 (159,744 bytes, MD5={src_md5}): {latest_count}개")
print(f"  이전 버전 (48,128 bytes 등): {old_count}개")

print(f"\n--- 4-3: 각 위치별 최신 버전 보유 여부 ---")
for label, loc in locations.items():
    has_latest = any(f["is_latest"] and f["location"] == label for f in all_files)
    mark = "✅" if has_latest else "❌"
    print(f"  {mark} {label}")

print(f"\n--- 4-4: 파일 잠금 상태 확인 ---")
lock_check = []
for f_info in all_files:
    fp = f_info["path"]
    try:
        stream = open(fp, 'r+b')
        stream.close()
        lock_check.append((fp, "잠금 없음"))
    except Exception as e:
        lock_check.append((fp, f"잠금됨: {e}"))

for fp, status in lock_check:
    mark = "✅" if "없음" in status else "❌"
    print(f"  {mark} {os.path.basename(fp)}: {status}")

print(f"\n--- 4-5: 디스크 여유공간 ---")
for drive in ['C:\\']:
    usage = os.statvfs(drive) if hasattr(os, 'statvfs') else None
    try:
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, None, None, ctypes.pointer(free_bytes))
        free_gb = round(free_bytes.value / (1024**3), 2)
        print(f"  {drive} 여유공간: {free_gb} GB")
    except:
        print(f"  {drive} 확인 불가")

print("\n" + "=" * 60)
print("최종 결과")
print("=" * 60)
all_ok = True

if latest_count >= 3:
    print("  ✅ 최신 HWP 파일이 3개 이상 위치에 동기화됨")
else:
    print("  ❌ 최신 HWP 파일 동기화 부족")
    all_ok = False

locked = [fp for fp, s in lock_check if "잠금됨" in s]
if not locked:
    print("  ✅ 모든 파일 잠금 없음")
else:
    print(f"  ❌ 잠금된 파일 {len(locked)}개")
    all_ok = False

if all_ok:
    print("\n  🎉 전체 무결성 체크 통과 - HWP 저장 환경 정상")
else:
    print("\n  ⚠️ 일부 항목 추가 조치 필요")
