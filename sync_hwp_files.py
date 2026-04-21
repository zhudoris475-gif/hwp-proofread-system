#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 전체 대비 및 동기화 스크립트
파일 2의 내용을 파일 1에 반영합니다.
"""

import os
import sys
import shutil
from datetime import datetime

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def backup_file(file_path):
    """파일 백업"""
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    return backup_path

def sync_hwp_files(file1, file2):
    """HWP 파일 동기화"""
    print("=" * 80)
    print("HWP 파일 동기화")
    print("=" * 80)
    print()

    # 백업
    print("💾 파일 1 백업 중...")
    backup_path = backup_file(file1)
    print(f"   ✅ 백업 완료: {backup_path}")
    print()

    # 파일 2를 파일 1로 복사
    print("🔄 파일 2를 파일 1로 복사 중...")
    shutil.copy2(file2, file1)
    print("   ✅ 동기화 완료")
    print()

    # 파일 정보 확인
    print("=" * 80)
    print("📁 동기화 후 파일 정보")
    print("=" * 80)
    print()

    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    mtime1 = datetime.fromtimestamp(os.path.getmtime(file1))
    mtime2 = datetime.fromtimestamp(os.path.getmtime(file2))

    print(f"📄 파일 1 (동기화됨):")
    print(f"   경로: {file1}")
    print(f"   크기: {size1:,} bytes")
    print(f"   수정일: {mtime1}")
    print()

    print(f"📄 파일 2 (원본):")
    print(f"   경로: {file2}")
    print(f"   크기: {size2:,} bytes")
    print()

    if size1 == size2:
        print("✅ 크기가 일치합니다.")
    else:
        print(f"⚠️  크기 차이: {abs(size1 - size2):,} bytes")
    print()

    # 백업 파일 삭제 옵션
    print("=" * 80)
    print("💾 백업 파일")
    print("=" * 80)
    print()
    print(f"   백업 파일: {backup_path}")
    print(f"   삭제하시려면: del {backup_path}")
    print(f"   보존하려면: 남겨두세요")
    print()

    print("=" * 80)
    print("✅ 동기화 완료!")
    print("=" * 80)
    print()
    print("💡 팁:")
    print("   - 파일 1이 파일 2의 내용으로 업데이트되었습니다.")
    print("   - 원본 파일 1은 백업으로 저장되었습니다.")
    print("   - 필요하면 백업 파일을 복원할 수 있습니다.")

if __name__ == "__main__":
    file1 = 'C:/Users/doris/xwechat_files/zhuchunyan331793_600e/msg/file/2026-04/【大中朝 14】J 1419-1693--275--_전체재수정v3.hwp'
    file2 = 'C:/Users/doris/Desktop/hwp_backup/【大中朝 14】J 1419-1693--275--20240920.hwp'

    if not os.path.exists(file1):
        print(f"❌ 파일 1을 찾을 수 없습니다: {file1}")
        sys.exit(1)

    if not os.path.exists(file2):
        print(f"❌ 파일 2를 찾을 수 없습니다: {file2}")
        sys.exit(1)

    sync_hwp_files(file1, file2)
