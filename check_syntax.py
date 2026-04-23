import ast
import os

files = ['compare_hwp.py', 'generate_recovery_list.py', 'chinese_detail_check.py']
for f in files:
    path = os.path.join(os.path.dirname(__file__), f)
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            ast.parse(fp.read())
        print(f'{f}: OK')
    except SyntaxError as e:
        print(f'{f}: ERROR - {e}')
