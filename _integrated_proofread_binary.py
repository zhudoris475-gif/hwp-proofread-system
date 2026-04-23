import os
import sys
import re
import zlib
import struct
import shutil
import olefile

RULES_FILE = r'C:\Users\51906\Desktop\rules_integrated.txt'
HWP_DIR = r'C:\Users\51906\Desktop\사전'
REPORT_FILE = os.path.join(HWP_DIR, '_통합규칙_교정_보고서.txt')

SECTION_HEADERS = {
    '띄어쓰기',
    '붙여쓰기',
}

def parse_rules(rules_file):
    rules = []
    seen = set()
    with open(rules_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ' -> ' not in line:
                continue
            m = re.match(r'\s*(.+?)\s+->\s+(.+)', line)
            if m:
                src = m.group(1).strip()
                dst = m.group(2).strip()
                if src in SECTION_HEADERS:
                    continue
                if src != dst and src not in seen:
                    seen.add(src)
                    rules.append((src, dst))
    return rules

def decompress_stream(data):
    for wbits in [-15, 15, 31]:
        try:
            return zlib.decompress(data, wbits)
        except:
            continue
    return None

def decompress_stream_incremental(data):
    for wbits in [-15, 15]:
        dc = zlib.decompressobj(wbits=wbits)
        result = b''
        for i in range(0, len(data), 65536):
            chunk = data[i:i+65536]
            try:
                result += dc.decompress(chunk)
            except zlib.error:
                break
        try:
            result += dc.flush()
        except:
            pass
        if result:
            return result
    return None

def compress_to_size(data, target_size):
    for level in range(1, 10):
        co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
        compressed = co.compress(data) + co.flush()
        if len(compressed) <= target_size:
            padded = compressed + b'\x00' * (target_size - len(compressed))
            return padded
    return None

def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF

        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4

        if offset + header_size + size > len(data):
            break

        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            'offset': offset,
            'tag_id': tag_id,
            'level': level,
            'size': size,
            'header_size': header_size,
            'payload': payload,
        })

        offset += header_size + size

    return records

def serialize_records(records):
    buf = bytearray()
    for rec in records:
        tag_id = rec['tag_id']
        level = rec['level']
        payload = rec['payload']
        size = len(payload)

        if size < 0xFFF:
            hdr = (size << 20) | (level << 10) | tag_id
            buf += struct.pack('<I', hdr)
        else:
            hdr = (0xFFF << 20) | (level << 10) | tag_id
            buf += struct.pack('<II', hdr, size)

        buf += payload

    return bytes(buf)

def apply_rules_to_text(text, rules):
    changes = []
    for src, dst in rules:
        count = text.count(src)
        if count > 0:
            text = text.replace(src, dst)
            changes.append((src, dst, count))
    return text, changes

def process_hwp_file(fpath, rules):
    report_lines = []
    fname = os.path.basename(fpath)
    report_lines.append(f'\n{"="*60}')
    report_lines.append(f'파일: {fname}')
    report_lines.append(f'{"="*60}')

    backup_path = fpath + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(fpath, backup_path)
        report_lines.append(f'  백업 생성: {os.path.basename(backup_path)}')

    ole = olefile.OleFileIO(fpath, write_mode=True)
    streams = ole.listdir()
    body_streams = [s for s in streams if s[0] == 'BodyText']
    report_lines.append(f'  BodyText 스트림 수: {len(body_streams)}')

    total_changes = 0
    modified = False
    write_error = False

    for stream_path in body_streams:
        stream_name = '/'.join(stream_path)
        orig_data = ole.openstream(stream_name).read()
        orig_size = len(orig_data)

        dec = decompress_stream(orig_data)
        if dec is None:
            dec = decompress_stream_incremental(orig_data)
            if dec is None:
                report_lines.append(f'  {stream_name}: 압축 해제 실패 (비표준 압축 형식)')
                continue
            else:
                full_dec = decompress_stream(orig_data)
                if full_dec is None:
                    report_lines.append(f'  {stream_name}: 부분 압축 해제 성공 ({len(dec)}바이트) - 비표준 다중 세그먼트 압축')
                    report_lines.append(f'  ⚠ 이 파일은 다중 세그먼트 압축을 사용하여 바이너리 수정이 불가능합니다')
                    report_lines.append(f'  ⚠ 한컴오피스에서 직접 교정해 주세요')
                    continue

        records = parse_records(dec)
        report_lines.append(f'  {stream_name}: {len(records)}개 레코드, 원본 압축 크기: {orig_size}바이트')

        stream_changes = 0
        for rec in records:
            if rec['tag_id'] == 67:
                try:
                    text = rec['payload'].decode('utf-16-le', errors='replace')
                except:
                    continue

                new_text, changes = apply_rules_to_text(text, rules)

                if changes:
                    for src, dst, cnt in changes:
                        report_lines.append(f'    [{src}] -> [{dst}] ({cnt}건)')
                        stream_changes += cnt

                    new_payload = new_text.encode('utf-16-le')
                    rec['payload'] = new_payload
                    rec['size'] = len(new_payload)

        if stream_changes > 0:
            new_dec = serialize_records(records)
            new_body = compress_to_size(new_dec, orig_size)

            if new_body is None:
                report_lines.append(f'  {stream_name}: 압축 크기 초과 (원본: {orig_size}, 필요: {len(zlib.compress(new_dec, -1))})')
                write_error = True
            else:
                try:
                    ole.write_stream(stream_name, new_body)
                    total_changes += stream_changes
                    modified = True
                    report_lines.append(f'  {stream_name} 변경: {stream_changes}건')
                except Exception as e:
                    report_lines.append(f'  {stream_name} 쓰기 오류: {e}')
                    write_error = True

    ole.close()

    if write_error:
        report_lines.append(f'  ⚠ 일부 스트림 쓰기 실패 - 백업에서 복원 필요')

    if total_changes > 0:
        report_lines.append(f'  총 변경: {total_changes}건')
        report_lines.append(f'  파일 저장 완료')
    else:
        report_lines.append(f'  변경 사항 없음')

    return report_lines, total_changes

def main():
    rules = parse_rules(RULES_FILE)
    print(f'규칙 수: {len(rules)}')
    if len(rules) > 0:
        print(f'첫 번째 규칙: {rules[0]}')
        print(f'마지막 규칙: {rules[-1]}')

    hwp_files = [f for f in os.listdir(HWP_DIR) if f.endswith('.hwp') and not f.startswith('~')]
    print(f'HWP 파일 수: {len(hwp_files)}')

    all_reports = []
    grand_total = 0
    failed_files = []

    for i, fname in enumerate(hwp_files):
        fpath = os.path.join(HWP_DIR, fname)
        print(f'처리 중 [{i+1}/{len(hwp_files)}]: {fname}')
        try:
            report_lines, total = process_hwp_file(fpath, rules)
            all_reports.extend(report_lines)
            grand_total += total
            if total == 0 and any('압축 해제 실패' in l or '비표준' in l for l in report_lines):
                failed_files.append(fname)
        except Exception as e:
            import traceback
            all_reports.append(f'\n{"="*60}')
            all_reports.append(f'파일: {fname}')
            all_reports.append(f'{"="*60}')
            all_reports.append(f'  오류: {e}')
            all_reports.append(f'  {traceback.format_exc()}')
            failed_files.append(fname)
            print(f'  오류: {e}')

    header = []
    header.append('통합규칙 교정 보고서')
    header.append(f'규칙 파일: {RULES_FILE}')
    header.append(f'규칙 수: {len(rules)}')
    header.append(f'처리 파일 수: {len(hwp_files)}')
    header.append(f'총 변경 건수: {grand_total}')
    if failed_files:
        header.append(f'')
        header.append(f'⚠ 다음 파일은 비표준 압축 형식으로 바이너리 수정 불가:')
        for ff in failed_files:
            header.append(f'  - {ff}')
        header.append(f'  → 한컴오피스에서 직접 교정 필요')
    header.append('')

    full_report = '\n'.join(header + all_reports)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_report)

    print(f'\n총 변경 건수: {grand_total}')
    if failed_files:
        print(f'⚠ 바이너리 수정 불가 파일 ({len(failed_files)}개):')
        for ff in failed_files:
            print(f'  - {ff}')
    print(f'보고서 저장: {REPORT_FILE}')

if __name__ == '__main__':
    main()
