import re, sys, os
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"

def extract_text(filepath):
    ole = olefile.OleFileIO(filepath)
    streams = ole.listdir()
    all_text = []
    for sp in streams:
        if sp[0] == "BodyText":
            raw = ole.openstream('/'.join(sp)).read()
            try:
                dec = zlib.decompress(raw, -15)
            except:
                continue
            import struct
            pos = 0
            while pos < len(dec):
                if pos + 4 > len(dec):
                    break
                hdr = struct.unpack_from('<I', dec, pos)[0]
                tag = hdr & 0x3FF
                rlen = (hdr >> 20) & 0xFFF
                pos += 4
                if pos + rlen > len(dec):
                    break
                if tag == 67:
                    try:
                        t = dec[pos:pos+rlen].decode('utf-16-le').rstrip('\x00')
                        if t:
                            all_text.append(t)
                    except:
                        pass
                pos += rlen
    ole.close()
    return '\n'.join(all_text)

import zlib, struct
text = extract_text(SRC)

ha_words = re.findall(r'[가-힣]+하[가-힣]*', text)
counter = Counter(ha_words)

ha_verb_stems = set()
for word, cnt in counter.most_common(1000):
    if word.endswith('하다') or word.endswith('하고') or word.endswith('하여') or word.endswith('해서') or word.endswith('한') or word.endswith('한다') or word.endswith('하였다') or word.endswith('하며') or word.endswith('하면') or word.endswith('하세요') or word.endswith('하기') or word.endswith('함') or word.endswith('할') or word.endswith('했'):
        stem = word[:-2] if len(word) > 2 else word
        ha_verb_stems.add(stem + '하')

for stem in sorted(ha_verb_stems)[:200]:
    print(f'"{stem}",')
