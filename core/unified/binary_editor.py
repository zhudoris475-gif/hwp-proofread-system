# -*- coding: utf-8 -*-
import os, re, struct, zlib, shutil, hashlib, stat, time
from collections import Counter

try:
    import olefile
except ImportError:
    olefile = None


def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


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
            "tag_id": tag_id,
            "level": level,
            "size": size,
            "header_size": header_size,
            "payload": payload,
        })
        offset += header_size + size
    return records


def rebuild_stream(records):
    parts = []
    for rec in records:
        payload = rec["payload"]
        size = len(payload)
        level = rec["level"]
        tag_id = rec["tag_id"]
        if size < 0xFFF:
            header = struct.pack('<I', tag_id | (level << 10) | (size << 20))
        else:
            header = struct.pack('<I', tag_id | (level << 10) | (0xFFF << 20)) + struct.pack('<I', size)
        parts.append(header + payload)
    return b''.join(parts)


def extract_text_from_records(records):
    texts = []
    for rec in records:
        if rec["tag_id"] != 67:
            continue
        try:
            texts.append(rec["payload"].decode("utf-16-le", errors="replace"))
        except Exception:
            continue
    return ''.join(texts)


def extract_text(filepath):
    if olefile is None:
        raise ImportError("olefile 패키지가 필요합니다: pip install olefile")
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        all_texts = []
        for sp in ole.listdir():
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                try:
                    dec = zlib.decompress(raw, -15)
                except zlib.error:
                    continue
                records = parse_records(dec)
                all_texts.append(extract_text_from_records(records))
    finally:
        ole.close()
    return '\n'.join(all_texts)


def apply_rules_to_records(records, rules):
    total_changes = 0
    modified_rec_count = 0
    change_log = []

    for i, rec in enumerate(records):
        if rec["tag_id"] != 67:
            continue
        try:
            rec_text = rec["payload"].decode('utf-16-le', errors='replace')
        except Exception:
            continue

        new_text = rec_text
        rec_changes = 0

        for src_word, dst_word, cat, cnt in rules:
            actual_cnt = new_text.count(src_word)
            if actual_cnt > 0:
                new_text = new_text.replace(src_word, dst_word)
                rec_changes += actual_cnt
                total_changes += actual_cnt
                change_log.append((src_word, dst_word, cat, actual_cnt))

        if rec_changes > 0:
            new_payload = new_text.encode('utf-16-le')
            records[i] = {
                "tag_id": rec["tag_id"],
                "level": rec["level"],
                "size": len(new_payload),
                "header_size": rec["header_size"],
                "payload": new_payload,
            }
            modified_rec_count += 1

    return records, total_changes, modified_rec_count, change_log


def compress_stream(records, original_compressed_size=None):
    new_dec = rebuild_stream(records)
    co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
    new_compressed = co.compress(new_dec) + co.flush()

    if original_compressed_size and len(new_compressed) > original_compressed_size:
        co2 = zlib.compressobj(level=1, method=zlib.DEFLATED, wbits=-15)
        new_compressed = co2.compress(new_dec) + co2.flush()
        if len(new_compressed) > original_compressed_size:
            return None, new_dec

    verify_dec = zlib.decompress(new_compressed, -15)
    verify_records = parse_records(verify_dec)

    return new_compressed, new_dec


def write_stream_to_hwp(src_path, out_path, stream_updates):
    if olefile is None:
        raise ImportError("olefile 패키지가 필요합니다")

    out_tmp = out_path + ".tmp_" + str(__import__('uuid').uuid4().hex[:8]) + ".bin"
    shutil.copy2(src_path, out_tmp)
    os.chmod(out_tmp, stat.S_IWRITE | stat.S_IREAD)

    ole_info = olefile.OleFileIO(src_path, write_mode=False)
    sector_size = ole_info.sector_size
    fat = ole_info.fat

    for sn, compressed_data in stream_updates.items():
        sp = sn.split('/')
        sid = ole_info._find(sp)
        entry = ole_info.direntries[sid]
        stream_size = entry.size
        start_sector = entry.isectStart

        chain = []
        current = start_sector
        while current >= 0 and current < len(fat):
            chain.append(current)
            current = fat[current]
            if len(chain) > 100000:
                break

        with open(out_tmp, 'r+b') as f:
            data_offset = 0
            for sect_idx, sect in enumerate(chain):
                offset = sector_size + sect * sector_size
                if data_offset >= len(compressed_data):
                    break
                chunk_end = min(data_offset + sector_size, len(compressed_data))
                chunk = compressed_data[data_offset:chunk_end]
                if len(chunk) < sector_size:
                    f.seek(offset)
                    existing = f.read(sector_size)
                    chunk = chunk + existing[len(chunk):]
                f.seek(offset)
                f.write(chunk)
                data_offset += sector_size

        if len(compressed_data) != stream_size:
            with open(out_tmp, 'r+b') as f:
                header = f.read(512)
                dir_start_sect = struct.unpack_from('<I', header, 48)[0]

                dir_chain = []
                cur_d = dir_start_sect
                while cur_d >= 0 and cur_d < len(fat):
                    dir_chain.append(cur_d)
                    cur_d = fat[cur_d]
                    if len(dir_chain) > 100:
                        break

                entries_per_sect = sector_size // 128
                sect_idx = sid // entries_per_sect
                entry_idx = sid % entries_per_sect

                if sect_idx < len(dir_chain):
                    dir_sect = dir_chain[sect_idx]
                    dir_entry_offset = sector_size + dir_sect * sector_size + entry_idx * 128

                    f.seek(dir_entry_offset + 120)
                    f.write(struct.pack('<I', len(compressed_data)))
                    f.seek(dir_entry_offset + 124)
                    f.write(struct.pack('<I', 0))

    ole_info.close()

    if os.path.exists(out_path):
        try:
            os.chmod(out_path, stat.S_IWRITE | stat.S_IREAD)
            os.remove(out_path)
        except PermissionError:
            out_path = out_path.replace('.hwp', '_new.hwp')

    os.rename(out_tmp, out_path)
    return out_path


def binary_proofread(src_path, out_path, rules, log_func=None):
    def log(msg):
        if log_func:
            log_func(msg)
        else:
            print(msg, flush=True)

    if olefile is None:
        log("[오류] olefile 패키지 필요")
        return False

    if not os.path.exists(src_path):
        log(f"[오류] 원본 파일 없음: {src_path}")
        return False

    src_hash = file_hash(src_path)
    log(f"원본: {os.path.basename(src_path)} (해시: {src_hash[:8]})")

    text = extract_text(src_path)
    log(f"추출 텍스트: {len(text):,}자")

    ole = olefile.OleFileIO(src_path, write_mode=False)
    all_stream_data = {}
    stream_list = ole.listdir()
    for sp in stream_list:
        sn = '/'.join(sp)
        all_stream_data[sn] = ole.openstream(sn).read()
    ole.close()

    total_changes = 0
    stream_updates = {}

    for sp in stream_list:
        sn = '/'.join(sp)
        if sp[0] != "BodyText":
            continue

        raw = all_stream_data[sn]
        try:
            dec = zlib.decompress(raw, -15)
        except zlib.error:
            log(f"[경고] {sn}: 압축해제 실패")
            continue

        records = parse_records(dec)
        records, changes, mod_recs, change_log = apply_rules_to_records(records, rules)

        if changes > 0:
            compressed, new_dec = compress_stream(records, len(raw))
            if compressed is None:
                log(f"[오류] {sn}: 압축 불가 (파일이 너무 커짐)")
                continue
            stream_updates[sn] = compressed
            total_changes += changes
            log(f"{sn}: {changes}건 교정, {mod_recs}개 레코드 수정")

    if not stream_updates:
        log("변경된 스트림 없음")
        return False

    backup_dir = os.path.join(os.path.dirname(out_path), "backup")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(src_path).replace('.hwp', f'_bak_{time.strftime("%H%M%S")}.hwp'))
    shutil.copy2(src_path, backup_path)
    log(f"백업: {backup_path}")

    final_path = write_stream_to_hwp(src_path, out_path, stream_updates)
    log(f"출력: {final_path}")

    try:
        verify_ole = olefile.OleFileIO(final_path, write_mode=False)
        verify_ole.close()
        log("검증: OLE 구조 정상")
    except Exception as e:
        log(f"[오류] 검증 실패: {e}")
        return False

    text_after = extract_text(final_path)
    log(f"수정 후 텍스트: {len(text_after):,}자 (원본: {len(text):,}자)")

    return True
