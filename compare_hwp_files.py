#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 비교 스크립트
두 HWP 파일의 차이점을 분석합니다.
"""

import os
import sys
import hashlib
import struct
from datetime import datetime

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_hwp_file_info(file_path):
    """HWP 파일의 기본 정보를 추출합니다."""
    file_info = {
        'path': file_path,
        'size': os.path.getsize(file_path),
        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
        'md5': '',
        'header': '',
        'version': '',
        'charset': ''
    }

    try:
        with open(file_path, 'rb') as f:
            # HWP 파일 헤더 읽기 (0-8 바이트)
            header = f.read(8)
            file_info['header'] = header.hex()
            file_info['version'] = header[2:4].hex()

            # 파일 위치 복원
            f.seek(0)

            # MD5 해시 계산
            file_info['md5'] = hashlib.md5()

            # 파일 내용 읽기 (헤더 제외)
            f.seek(8)
            chunk_size = 8192
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                file_info['md5'].update(chunk)

            file_info['md5'] = file_info['md5'].hexdigest()

    except Exception as e:
        print(f"❌ 파일 정보 추출 실패: {e}")
        return None

    return file_info

def compare_hwp_files(file1, file2):
    """두 HWP 파일을 비교합니다."""
    print("=" * 60)
    print("HWP 파일 비교 분석")
    print("=" * 60)
    print()

    # 파일 정보 읽기
    info1 = get_hwp_file_info(file1)
    info2 = get_hwp_file_info(file2)

    if not info1 or not info2:
        print("❌ 파일 정보를 읽을 수 없습니다.")
        return

    # 기본 정보 출력
    print("📁 파일 1:")
    print(f"   경로: {info1['path']}")
    print(f"   크기: {info1['size']:,} bytes")
    print(f"   수정일: {info1['modified']}")
    print(f"   버전: 0x{info1['version']}")
    print(f"   MD5: {info1['md5']}")
    print()

    print("📁 파일 2:")
    print(f"   경로: {info2['path']}")
    print(f"   크기: {info2['size']:,} bytes")
    print(f"   수정일: {info2['modified']}")
    print(f"   버전: 0x{info2['version']}")
    print(f"   MD5: {info2['md5']}")
    print()

    # 비교 결과
    print("=" * 60)
    print("🔍 비교 결과")
    print("=" * 60)
    print()

    # 크기 비교
    size_diff = info1['size'] - info2['size']
    if size_diff == 0:
        print("✅ 크기: 동일")
    else:
        print(f"⚠️  크기: 차이 {abs(size_diff):,} bytes")
        if size_diff > 0:
            print(f"   파일 1이 {size_diff:,} bytes 더 큼")
        else:
            print(f"   파일 2가 {abs(size_diff):,} bytes 더 큼")
    print()

    # 버전 비교
    if info1['version'] == info2['version']:
        print("✅ 버전: 동일")
    else:
        print(f"⚠️  버전: 다름 (파일 1: 0x{info1['version']}, 파일 2: 0x{info2['version']})")
    print()

    # MD5 비교
    if info1['md5'] == info2['md5']:
        print("✅ 내용: 완전히 동일")
    else:
        print("❌ 내용: 서로 다름")
        print(f"   파일 1 MD5: {info1['md5']}")
        print(f"   파일 2 MD5: {info2['md5']}")
    print()

    # 헤더 비교
    if info1['header'] == info2['header']:
        print("✅ 헤더: 동일")
    else:
        print("⚠️  헤더: 다름")
        print(f"   파일 1 헤더: {info1['header']}")
        print(f"   파일 2 헤더: {info2['header']}")
    print()

    # 수정일 비교
    if info1['modified'] == info2['modified']:
        print("✅ 수정일: 동일")
    else:
        print(f"⚠️  수정일: 다름")
        print(f"   파일 1: {info1['modified']}")
        print(f"   파일 2: {info2['modified']}")
    print()

    # 결론
    print("=" * 60)
    print("📋 결론")
    print("=" * 60)
    print()

    if info1['md5'] == info2['md5']:
        print("✅ 두 파일은 완전히 동일합니다.")
    elif info1['size'] == info2['size'] and info1['header'] == info2['header']:
        print("⚠️  파일 크기와 헤더는 동일하지만, 내용은 다릅니다.")
        print("   → 텍스트 내용이나 데이터가 변경되었습니다.")
    else:
        print("❌ 두 파일은 다른 파일입니다.")
        print("   → 크기, 내용, 헤더 모두 다릅니다.")

    print()
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python compare_hwp.py <파일1.hwp> <파일2.hwp>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not os.path.exists(file1):
        print(f"❌ 파일 1을 찾을 수 없습니다: {file1}")
        sys.exit(1)

    if not os.path.exists(file2):
        print(f"❌ 파일 2를 찾을 수 없습니다: {file2}")
        sys.exit(1)

    compare_hwp_files(file1, file2)
