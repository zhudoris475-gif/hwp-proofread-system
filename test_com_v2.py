import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
import win32com.client, pythoncom, time

pythoncom.CoInitialize()
hwp = win32com.client.DispatchEx('HWPFrame.HwpObject', clsctx=4)
hwp.RegisterModule('FilePathCheckDLL', 'AutomationModule')
try:
    hwp.SetMessageBoxMode(0x00020000)
except:
    pass
print('COM connected')

r = hwp.Open(r'C:\사전\【20】O 2179-2182排版页数4-金花顺.hwp', 'HWP', 'forceopen:true')
print(f'Open result: {r}')
time.sleep(2)

test_items = ['저장성', '절강성', '한것', '유럽안', '해 보다', '뜻으로', '噢', '欧姆']
for s in test_items:
    hwp.HAction.GetDefault('AllReplace', hwp.HParameterSet.HFindReplace.HSet)
    hwp.HParameterSet.HFindReplace.FindString = s
    hwp.HParameterSet.HFindReplace.ReplaceString = s
    hwp.HParameterSet.HFindReplace.Direction = 0
    hwp.HParameterSet.HFindReplace.ReplaceMode = 1
    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
    hwp.HParameterSet.HFindReplace.FindType = 1
    result = hwp.HAction.Execute('AllReplace', hwp.HParameterSet.HFindReplace.HSet)
    print(f'Find "{s}": {result}')

hwp.Quit()
pythoncom.CoUninitialize()
print('Done')
