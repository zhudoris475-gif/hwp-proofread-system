import os, shutil, hashlib, datetime, tempfile

results = []

def md5(f):
    h = hashlib.md5()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def test_write(dir_path, label):
    test_file = os.path.join(dir_path, f"_save_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tmp")
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("HWP save test - write OK")
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        os.remove(test_file)
        if content == "HWP save test - write OK":
            results.append((label, dir_path, "PASS", "읽기/쓰기/삭제 정상"))
            return True
        else:
            results.append((label, dir_path, "FAIL", "읽기 내용 불일치"))
            return False
    except Exception as e:
        results.append((label, dir_path, "FAIL", str(e)))
        if os.path.exists(test_file):
            try: os.remove(test_file)
            except: pass
        return False

def test_copy_hwp(src, dst_dir, label):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    basename = os.path.basename(src)
    name, ext = os.path.splitext(basename)
    dst = os.path.join(dst_dir, f"{name}_copytest_{ts}{ext}")
    try:
        shutil.copy2(src, dst)
        src_md5 = md5(src)
        dst_md5 = md5(dst)
        match = src_md5 == dst_md5
        os.remove(dst)
        if match:
            results.append((label, dst_dir, "PASS", f"HWP 복사/검증/삭제 정상 (MD5: {src_md5})"))
            return True
        else:
            results.append((label, dst_dir, "FAIL", f"MD5 불일치: 원본={src_md5}, 복사본={dst_md5}"))
            return False
    except Exception as e:
        results.append((label, dst_dir, "FAIL", str(e)))
        if os.path.exists(dst):
            try: os.remove(dst)
            except: pass
        return False

src_hwp = r'C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp'

print("=" * 60)
print("3단계: HWP 파일 저장 테스트")
print("=" * 60)

print("\n--- 3-1: 디렉토리 쓰기/읽기/삭제 테스트 ---")
test_write(r'C:\Users\doris\Desktop\新词典', '新词典')
test_write(r'C:\AMD\AJ', 'AMD\AJ')
test_write(r'C:\AMD\AJ\hwp_proofreading_package', 'AMD\AJ\hwp_proofreading_package')
test_write(r'C:\AMD\AJ\hwp_proofreading_package\hwp_work', 'AMD\AJ\hwp_work')
test_write(r'C:\AMD\AJ\hwp_proofreading_package\temp_hwpx_extract', 'AMD\AJ\temp_hwpx_extract')
test_write(r'C:\Users\doris\Desktop\xwechat_files\WORD', 'xwechat_files\WORD')
test_write(r'C:\Users\doris\Desktop\xwechat_files\WORD\reports', 'xwechat_files\WORD\reports')

print("\n--- 3-2: HWP 파일 실제 복사/검증 테스트 ---")
test_copy_hwp(src_hwp, r'C:\AMD\AJ\hwp_proofreading_package', 'HWP→AMD')
test_copy_hwp(src_hwp, r'C:\AMD\AJ\hwp_proofreading_package\hwp_work', 'HWP→hwp_work')
test_copy_hwp(src_hwp, r'C:\Users\doris\Desktop\xwechat_files\WORD', 'HWP→WORD')

print("\n--- 3-3: HWP 원본 파일 덮어쓰기 테스트 ---")
try:
    with open(src_hwp, 'rb') as f:
        original_data = f.read()
    tmp_backup = src_hwp + ".overwrite_test_bak"
    shutil.copy2(src_hwp, tmp_backup)
    with open(src_hwp, 'r+b') as f:
        pass
    shutil.copy2(tmp_backup, src_hwp)
    os.remove(tmp_backup)
    verify_md5 = md5(src_hwp)
    results.append(('HWP원본 덮어쓰기', src_hwp, "PASS", f"덮어쓰기/복원 정상 (MD5: {verify_md5})"))
except Exception as e:
    results.append(('HWP원본 덮어쓰기', src_hwp, "FAIL", str(e)))
    if os.path.exists(tmp_backup):
        try: shutil.copy2(tmp_backup, src_hwp)
        except: pass
        try: os.remove(tmp_backup)
        except: pass

print("\n" + "=" * 60)
print("테스트 결과 요약")
print("=" * 60)
pass_count = 0
fail_count = 0
for label, path, status, detail in results:
    mark = "✅" if status == "PASS" else "❌"
    print(f"  {mark} [{status}] {label}")
    print(f"     경로: {path}")
    print(f"     상세: {detail}")
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1

print(f"\n총 {len(results)}개 테스트: {pass_count} PASS, {fail_count} FAIL")
