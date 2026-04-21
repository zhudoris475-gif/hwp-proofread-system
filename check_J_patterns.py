import sys, re
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
from hwp_ollama_proofread import extract_text_from_hwp_binary

J = r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920.hwp"
text = extract_text_from_hwp_binary(J)

geot_cnt = len(re.findall(r'[가-힣]+것', text))
su_cnt = len(re.findall(r'[가-힣]+수', text))
goit_cnt = len(re.findall(r'[가-힣]+고있[가-힣]*', text))

print(f"것 패턴 총: {geot_cnt}")
print(f"수 패턴 총: {su_cnt}")
print(f"고있 패턴 총: {goit_cnt}")

for p in ["하고있다", "알고있다", "가지고있다"]:
    cnt = text.count(p)
    print(f"  직접검색 {p}: {cnt}")

for p in ["고 있", " 것", " 수 "]:
    cnt = text.count(p)
    print(f'  공백포함 "{p}": {cnt}')
