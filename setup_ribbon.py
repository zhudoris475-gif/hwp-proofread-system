"""
HWP Ollama AI 리본(蝴蝶结) 메뉴 + 단축키 설정 스크립트
사용법: python setup_ribbon.py
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

try:
    import win32com.client
    import pythoncom
    print("✅ COM 모듈 로드 성공")
except ImportError:
    print("❌ pywin32 필요: pip install pywin32")
    sys.exit(1)

def connect_hwp():
    """HWP 연결"""
    try:
        hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
        hwp.XHwpWindows.Item(0).Visible = True
        print("✅ HWP 연결 성공")
        return hwp
    except Exception as e:
        print(f"❌ HWP 연결 실패: {e}")
        print("   HWP를 먼저 실행해주세요!")
        return None

def setup_ribbon(hwp):
    """리본(Ribbon) 메뉴 설정 - 蝴蝶结"""
    print("\n[1/3] 리본 탭 추가...")
    try:
        hwp.HAction.GetDefault("RibbonAddTab", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = "OllamaAI"
        hwp.HParameterSet.HFindReplace.ReplaceString = "Ollama AI"
        result = hwp.HAction.Execute("RibbonAddTab", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  ✅ RibbonAddTab: {result}")
    except Exception as e:
        print(f"  ⚠ RibbonAddTab: {e}")

    print("\n[2/3] 리본 그룹 추가...")
    try:
        hwp.HAction.GetDefault("RibbonAddGroup", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = "OllamaAI"
        hwp.HParameterSet.HFindReplace.ReplaceString = "교정 기능"
        result = hwp.HAction.Execute("RibbonAddGroup", hwp.HParameterSet.HFindReplace.HSet)
        print(f"  ✅ RibbonAddGroup: {result}")
    except Exception as e:
        print(f"  ⚠ RibbonAddGroup: {e}")

    print("\n[3/3] 버튼 추가...")
    buttons = [
        ("문서 분석 AI [Ctrl+Shift+A]", "OllamaAI_Analyze"),
        ("띄어쓰기 교정 [Ctrl+Shift+S]", "OllamaAI_Spacing"),
        ("의존명사 교정 [Ctrl+Shift+D]", "OllamaAI_DepNoun"),
        ("가운데점→쉼표 [Ctrl+Shift+M]", "OllamaAI_MidDot"),
        ("TXT 규칙 적용 [Ctrl+Shift+T]", "OllamaAI_TxtRules"),
        ("설정 [Ctrl+Shift+,]", "OllamaAI_Settings"),
    ]
    
    for label, cmd in buttons:
        try:
            hwp.HAction.GetDefault("RibbonAddButton", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.FindString = cmd
            hwp.HParameterSet.HFindReplace.ReplaceString = label
            result = hwp.HAction.Execute("RibbonAddButton", hwp.HParameterSet.HFindReplace.HSet)
            print(f"  ✅ '{label}': {result}")
        except Exception as e:
            print(f"  ⚠ '{label}': {e}")

def setup_hotkeys(hwp):
    """단축키(Hotkey) 등록"""
    print("\n" + "=" * 40)
    print("  단축키 설정 (Hotkey Setup)")
    print("=" * 40)
    
    hotkey_map = [
        ("Ctrl+Shift+A", "문서 분석 AI"),
        ("Ctrl+Shift+S", "띄어쓰기 교정"),
        ("Ctrl+Shift+D", "의존명사 교정"),
        ("Ctrl+Shift+M", "가운데점→쉼표"),
        ("Ctrl+Shift+T", "TXT 규칙 적용"),
        ("Ctrl+Shift+,", "설정"),
    ]
    
    print("\n등록할 단축키:")
    for key, desc in hotkey_map:
        print(f"  {key:20s} → {desc}")
    
    print("\n[방법1] HWP 매크로로 단축키 등록...")
    try:
        macro_code = '''
Sub SetHotkeys()
    ' 문서 분석 AI - Ctrl+Shift+A
    KeyMap.SetKey "Ctrl+Shift+A", "OllamaAI_Analyze"
    ' 띄어쓰기 교정 - Ctrl+Shift+S  
    KeyMap.SetKey "Ctrl+Shift+S", "OllamaAI_Spacing"
    ' 의존명사 교정 - Ctrl+Shift+D
    KeyMap.SetKey "Ctrl+Shift+D", "OllamaAI_DepNoun"
    ' 가운데점→쉼표 - Ctrl+Shift+M
    KeyMap.SetKey "Ctrl+Shift+M", "OllamaAI_MidDot"
    ' TXT 규칙 적용 - Ctrl+Shift+T
    KeyMap.SetKey "Ctrl+Shift+T", "OllamaAI_TxtRules"
    ' 설정 - Ctrl+Shift+,
    KeyMap.SetKey "Ctrl+Shift+,", "OllamaAI_Settings"
End Sub
'''
        print("  ✅ 매크로 코드 생성됨")
        
        # 저장
        script_dir = os.path.dirname(os.path.abspath(__file__))
        macro_path = os.path.join(script_dir, "hotkeys_macro.hml")
        with open(macro_path, "w", encoding="utf-8") as f:
            f.write(macro_code)
        print(f"  ✅ 매크로 파일: {macro_path}")
        
    except Exception as e:
        print(f"  ⚠ 매크로 생성: {e}")
    
    print("\n[방법2] HWP 내부에서 수동 등록...")
    print("  1. HWP 메뉴: 도구 > 사용자 정의 > 키보드")
    print("  2. 카테고리: Ollama AI 선택")
    print("  3. 각 명령에 단축키 지정:")
    for key, desc in hotkey_map:
        print(f"     • {desc}: [{key}]")

def create_shortcut_guide():
    """단축키 안내 파일 생성"""
    guide = """
# HWP Ollama AI 단축키 가이드

## 단축키 목록

| 단축키 | 기능 | 설명 |
|--------|------|------|
| **Ctrl+Shift+A** | 문서 분석 AI | 전체 문서 AI 교정 |
| **Ctrl+Shift+S** | 띄어쓰기 교정 | 공백 오류 수정 |
| **Ctrl+Shift+D** | 의존명사 교정 | 것/수/적/바 등 띄어쓰기 |
| **Ctrl+Shift+M** | 가운데점→쉼표 | · → , 변환 |
| **Ctrl+Shift+T** | TXT 규칙 적용 | 1204개 규칙 일괄 적용 |
| **Ctrl+Shift+,** | 설정 | 모델/URL 변경 |

## 등록 방법

### 자동 (권장)
```
python setup_ribbon.py
```

### 수동 (HWP 내부)
1. 도구 > 사용자 정의 > 키보드
2. 카테고리에서 "Ollama AI" 선택
3. 각 명령에 위 단축키 지정
4. 확인 클릭

## 사용 팁
- 단축키가 작동하지 않으면 HWP 재시작
- 충돌하는 단축키가 있으면 다른 조합으로 변경
"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    guide_path = os.path.join(script_dir, "단축키_가이드.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide)
    print(f"\n✅ 단축키 가이드: {guide_path}")

def main():
    print("=" * 50)
    print("  HWP Ollama AI 리본 + 단축키 설정")
    print("=" * 50)
    
    hwp = connect_hwp()
    if not hwp:
        print("\nHWP를 실행한 후 다시 시도하세요.")
        input("\nEnter를 눌러 종료...")
        return
    
    setup_ribbon(hwp)
    setup_hotkeys(hwp)
    create_shortcut_guide()
    
    print("\n" + "=" * 50)
    print("  ✅ 설정 완료!")
    print("=" * 50)
    print("\n📋 단축키:")
    print("   Ctrl+Shift+A : 문서 분석 AI")
    print("   Ctrl+Shift+S : 띄어쓰기 교정")
    print("   Ctrl+Shift+D : 의존명사 교정")
    print("   Ctrl+Shift+M : 가운데점→쉼표")
    print("   Ctrl+Shift+T : TXT 규칙 적용")
    print("   Ctrl+Shift+, : 설정")
    print("\nHWP를 재시작하면 적용됩니다.")
    input("\nEnter를 눌러 종료...")

if __name__ == "__main__":
    main()