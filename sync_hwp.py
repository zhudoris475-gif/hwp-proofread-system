import shutil, hashlib, os, datetime

src = r'C:\Users\doris\Desktop\新词典\【20】O 2179-2182작업본.hwp'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

amd_dst = rf'C:\AMD\AJ\hwp_proofreading_package\【20】O 2179-2182작업본_backup_{ts}.hwp'
shutil.copy2(src, amd_dst)
print(f'AMD backup: {amd_dst}')

word_dst = rf'C:\Users\doris\Desktop\xwechat_files\WORD\【20】O 2179-2182排版页数4-金花顺_新词典원본_작업본_{ts}.hwp'
shutil.copy2(src, word_dst)
print(f'WORD copy: {word_dst}')

def md5(f):
    h = hashlib.md5()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

orig = md5(src)
amd_h = md5(amd_dst)
word_h = md5(word_dst)

print(f'\nOriginal MD5: {orig}')
match_amd = "MATCH" if orig == amd_h else "MISMATCH"
match_word = "MATCH" if orig == word_h else "MISMATCH"
print(f'AMD MD5:      {amd_h} {match_amd}')
print(f'WORD MD5:     {word_h} {match_word}')

print('\n=== All O 2179-2182 HWP files ===')
locations = [
    r'C:\Users\doris\Desktop\新词典',
    r'C:\AMD\AJ\hwp_proofreading_package',
    r'C:\Users\doris\Desktop\xwechat_files\WORD'
]
for loc in locations:
    if os.path.exists(loc):
        for f in os.listdir(loc):
            if '2179' in f and '2182' in f and f.endswith('.hwp'):
                fp = os.path.join(loc, f)
                sz = os.path.getsize(fp)
                mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
                print(f'  {fp} ({sz} bytes, {mt})')
