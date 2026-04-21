import sys, os, time
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

import win32com.client

TARGET = r"C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp"
TEMP_DIR = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'hwp_proofread')
os.makedirs(TEMP_DIR, exist_ok=True)
TEMP_HWP = os.path.join(TEMP_DIR, 'diag_test.hwp')

import shutil
if os.path.exists(TEMP_HWP):
    os.remove(TEMP_HWP)
shutil.copy2(TARGET, TEMP_HWP)
print(f"[1] 원본 -> 임시 복사: {TEMP_HWP}")

print("\n=== TEST A: 임시 파일로 COM 열기 ===")
hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
r = hwp.Open(TEMP_HWP, "", "")
print(f"  Open result: {r}")

test_searches = ["저장성", "절강성", "한것", "유럽안", "해 보다", "뜻으로", "噢", "欧姆"]
for s in test_searches:
    pset = hwp.HParameterSet.HFindReplace
    hwp.HAction.GetDefault("AllReplace", pset.HSet)
    pset.FindString = s
    pset.ReplaceString = s
    pset.Direction = 0
    pset.WholeWordOnly = 0
    pset.MatchCase = 0
    pset.UseWildCards = 0
    pset.ReplaceMode = 1
    pset.SeveralWords = 0
    result = hwp.HAction.Execute("AllReplace", pset.HSet)
    print(f"  Find '{s}': {result}")

hwp.Clear(1)
print("  Cleared")

print("\n=== TEST B: 원본 파일로 COM 열기 ===")
hwp2 = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp2.RegisterModule("FilePathCheckDLL", "AutomationModule")
r2 = hwp2.Open(TARGET, "", "")
print(f"  Open result: {r2}")

for s in test_searches:
    pset2 = hwp2.HParameterSet.HFindReplace
    hwp2.HAction.GetDefault("AllReplace", pset2.HSet)
    pset2.FindString = s
    pset2.ReplaceString = s
    pset2.Direction = 0
    pset2.WholeWordOnly = 0
    pset2.MatchCase = 0
    pset2.UseWildCards = 0
    pset2.ReplaceMode = 1
    pset2.SeveralWords = 0
    result2 = hwp2.HAction.Execute("AllReplace", pset2.HSet)
    print(f"  Find '{s}': {result2}")

hwp2.Clear(1)
print("  Cleared")

print("\n=== TEST C: MoveCursorToTop 후 검색 ===")
hwp3 = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp3.RegisterModule("FilePathCheckDLL", "AutomationModule")
r3 = hwp3.Open(TARGET, "", "")
print(f"  Open result: {r3}")

hwp3.HAction.GetDefault("MoveTop", hwp3.HParameterSet.HFindReplace.HSet)
hwp3.HAction.Execute("MoveTop", hwp3.HParameterSet.HFindReplace.HSet)
print("  MoveTop done")

for s in test_searches:
    pset3 = hwp3.HParameterSet.HFindReplace
    hwp3.HAction.GetDefault("AllReplace", pset3.HSet)
    pset3.FindString = s
    pset3.ReplaceString = s
    pset3.Direction = 0
    pset3.WholeWordOnly = 0
    pset3.MatchCase = 0
    pset3.UseWildCards = 0
    pset3.ReplaceMode = 1
    pset3.SeveralWords = 0
    result3 = hwp3.HAction.Execute("AllReplace", pset3.HSet)
    print(f"  Find '{s}': {result3}")

hwp3.Clear(1)
print("  Cleared")

print("\n진단 완료")
