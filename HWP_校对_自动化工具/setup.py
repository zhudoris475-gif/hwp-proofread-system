import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

print("=" * 50)
print("HWP 교정 자동화 - 환경 설정")
print("=" * 50)
print()

py_version = sys.version_info
print(f"Python 버전: {py_version.major}.{py_version.minor}.{py_version.micro}")

if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
    print("❌ Python 3.8 이상이 필요합니다!")
    input("Enter를 눌러 종료...")
    sys.exit(1)

print("\n필수 패키지 설치 중...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"], stdout=subprocess.DEVNULL)
    print("✅ pywin32 설치 완료")
except:
    print("⚠ pywin32 설치 실패 - 수동 설치 필요: pip install pywin32")

print("\n설정 확인...")
try:
    import win32com.client
    print("✅ win32com.client 사용 가능")
except ImportError:
    print("❌ win32com.client를 가져올 수 없습니다")
    print("   수동으로 실행: python -m pip install pywin32")

try:
    import pythoncom
    print("✅ pythoncom 사용 가능")
except ImportError:
    print("❌ pythoncom을 가져올 수 없습니다")

script_dir = os.path.dirname(os.path.abspath(__file__))
rules_file = os.path.join(script_dir, "config", "proofread_rules.txt")
if os.path.exists(rules_file):
    with open(rules_file, 'r', encoding='utf-8') as f:
        rule_count = sum(1 for l in f if l.strip() and not l.startswith('#') and '->' in l)
    print(f"✅ 교정 규칙: {rule_count}개")
else:
    print(f"❌ 규칙 파일 없음: {rules_file}")

print("\n" + "=" * 50)
print("환경 설정 완료!")
print("=" * 50)
print()
print("사용법:")
print('  python hwp_proofread.py "HWP파일_경로"')
print('  python hwp_proofread.py "HWP폴더_경로"')
print('  python hwp_verify.py "HWP파일_또는_폴더_경로"')
print()
input("Enter를 눌러 종료...")
