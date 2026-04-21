import re
logpath = r'C:\Users\doris\AppData\Local\Temp\hwp_logs\L교정로그_20260419_233319.txt'
with open(logpath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('[하]')
if idx >= 0:
    ha_section = content[idx:]
    lines = ha_section.split('\n')[:30]
    for l in lines:
        print(l)
