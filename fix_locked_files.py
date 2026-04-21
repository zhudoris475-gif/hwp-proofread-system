import os, shutil, hashlib, datetime

def md5(f):
    h = hashlib.md5()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

src_hwp = r'C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp'
src_md5 = md5(src_hwp)

locked_files = [
    r'C:\Users\doris\Desktop\新词典\【20】O 2179-2182排版页数4-金花顺.hwp',
    r'C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_外部复制.hwp',
    r'C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_20260417_221444.hwp',
    r'C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_사전원본_작업본_20260417_020241.hwp',
    r'C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_작업본_20260417_220345.hwp',
]

print("=" * 60)
print("잠금 파일 권한 수정")
print("=" * 60)

import subprocess

for fp in locked_files:
    if os.path.exists(fp):
        print(f"\n수정 중: {os.path.basename(fp)}")
        try:
            result = subprocess.run(
                ['icacls', fp, '/grant', 'doriszhu\\doris:F', '/inheritance:e'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print(f"  icacls 권한 부여 성공")
            else:
                print(f"  icacls 출력: {result.stdout.strip()}")
                print(f"  icacls 에러: {result.stderr.strip()}")

            try:
                with open(fp, 'r+b') as f:
                    pass
                print(f"  ✅ 파일 접근 가능")
            except Exception as e:
                print(f"  ❌ 여전히 접근 불가: {e}")
                try:
                    os.chmod(fp, 0o666)
                    with open(fp, 'r+b') as f:
                        pass
                    print(f"  ✅ chmod 후 접근 가능")
                except Exception as e2:
                    print(f"  ❌ chmod 후에도 불가: {e2}")
        except Exception as e:
            print(f"  에러: {e}")
    else:
        print(f"\n파일 없음: {fp}")

print("\n" + "=" * 60)
print("hwp_work에 최신 버전 동기화")
print("=" * 60)

hwp_work_dir = r'C:\AMD\AJ\hwp_proofreading_package\hwp_work'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
dst = os.path.join(hwp_work_dir, f"【20】O 2179-2182작업본_{ts}.hwp")
try:
    shutil.copy2(src_hwp, dst)
    dst_md5 = md5(dst)
    match = "✅ MATCH" if dst_md5 == src_md5 else "❌ MISMATCH"
    print(f"  복사 완료: {dst}")
    print(f"  MD5: {dst_md5} {match}")
except Exception as e:
    print(f"  ❌ 복사 실패: {e}")

print("\n" + "=" * 60)
print("최종 잠금 상태 재확인")
print("=" * 60)

all_hwp = []
search_dirs = [
    r'C:\Users\doris\Desktop\新词典',
    r'C:\AMD\AJ\hwp_proofreading_package',
    r'C:\AMD\AJ\hwp_proofreading_package\hwp_work',
    r'C:\Users\doris\Desktop\xwechat_files\WORD',
]

for d in search_dirs:
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith('.hwp') and '2179' in f and '2182' in f:
                all_hwp.append(os.path.join(d, f))

locked_remaining = []
for fp in all_hwp:
    try:
        with open(fp, 'rb') as f:
            f.read(1)
        status = "✅"
    except:
        status = "❌"
        locked_remaining.append(fp)
    print(f"  {status} {os.path.basename(fp)}")

if locked_remaining:
    print(f"\n잠금 잔여: {len(locked_remaining)}개")
    for fp in locked_remaining:
        print(f"  - {fp}")
else:
    print(f"\n✅ 모든 파일 접근 가능!")
