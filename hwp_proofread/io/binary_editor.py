import os
import struct
import zlib
import hashlib
import shutil
import stat
import time

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
    i = 0
    while i < len(data):
        if i + 4 > len(data):
            break
        tag_id = struct.unpack_from('<H', data, i)[0]
        level = struct.unpack_from('<H', data, i + 2)[0]
        if i + 8 > len(data):
            break
        size = struct.unpack_from('<I', data, i + 4)[0]
        header_size = 8
        if size == 0xFFFFFFFF:
            if i + 12 > len(data):
                break
            size = struct.unpack_from('<I', data, i + 8)[0]
            header_size = 12
        payload_start = i + header_size
        payload_end = payload_start + size
        if payload_end > len(data):
            payload = data[payload_start:]
            records.append({"tag_id": tag_id, "level": level, "size": size, "header_size": header_size, "payload": payload})
            break
        payload = data[payload_start:payload_end]
        records.append({"tag_id": tag_id, "level": level, "size": size, "header_size": header_size, "payload": payload})
        i = payload_end
    return records


def rebuild_stream(records):
    buf = bytearray()
    for rec in records:
        buf += struct.pack('<HH', rec["tag_id"], rec["level"])
        if rec["header_size"] == 12:
            buf += struct.pack('<I', 0xFFFFFFFF)
            buf += struct.pack('<I', len(rec["payload"]))
        else:
            buf += struct.pack('<I', len(rec["payload"]))
        buf += rec["payload"]
    return bytes(buf)


def extract_text_from_records(records):
    parts = []
    for rec in records:
        if rec["tag_id"] == 67:
            try:
                t = rec["payload"].decode('utf-16-le', errors='replace')
                parts.append(t)
            except Exception:
                pass
    return ''.join(parts)


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
    for level in [6, 5, 4, 3, 2, 1]:
        co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
        nc = co.compress(new_dec) + co.flush()
        if original_compressed_size is None or len(nc) <= original_compressed_size:
            verify_dec = zlib.decompress(nc, -15)
            verify_records = parse_records(verify_dec)
            return nc, new_dec, level
    return None, new_dec, 0


def write_stream_to_hwp(src_path, out_path, stream_updates):
    if olefile is None:
        raise ImportError("olefile 패키지가 필요합니다")

    out_tmp = out_path.replace('.hwp', f'_work_{time.strftime("%H%M%S")}_{os.getpid()}.bin')
    shutil.copy2(src_path, out_tmp)
    os.chmod(out_tmp, stat.S_IWRITE | stat.S_IREAD)

    ole_info = olefile.OleFileIO(src_path, write_mode=False)
    sector_size = ole_info.sector_size

    for sn, compressed_data in stream_updates.items():
        sp = sn.split('/')
        sid = ole_info._find(sp)
        entry = ole_info.direntries[sid]
        stream_size = entry.size
        start_sector = entry.isectStart

        with open(out_tmp, 'r+b') as f:
            header = f.read(512)
            num_fat_sectors = struct.unpack_from('<I', header, 44)[0]
            first_dir_sect = struct.unpack_from('<I', header, 48)[0]

            difat = []
            for i in range(109):
                s = struct.unpack_from('<I', header, 76 + i * 4)[0]
                if s != 0xFFFFFFFE and s != 0xFFFFFFFF:
                    difat.append(s)

            fat = []
            for fs in difat[:num_fat_sectors]:
                f.seek(512 + fs * sector_size)
                for _ in range(sector_size // 4):
                    fat.append(struct.unpack('<I', f.read(4))[0])

            chain = []
            cur = start_sector
            while cur != 0xFFFFFFFE and cur != 0xFFFFFFFF and cur < len(fat):
                chain.append(cur)
                cur = fat[cur]
                if len(chain) > 10000:
                    break

            for idx, sect in enumerate(chain):
                offset = 512 + sect * sector_size
                f.seek(offset)
                chunk_size = min(sector_size, len(compressed_data) - idx * sector_size)
                if chunk_size <= 0:
                    break
                chunk = compressed_data[idx * sector_size:idx * sector_size + chunk_size]
                if len(chunk) < sector_size:
                    existing = f.read(sector_size)
                    f.seek(offset)
                    chunk = chunk + existing[len(chunk):]
                f.seek(offset)
                f.write(chunk)

            if len(compressed_data) != stream_size:
                dir_chain = []
                cur_d = first_dir_sect
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
                    dir_entry_offset = 512 + dir_sect * sector_size + entry_idx * 128

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


def binary_proofread(src_path, out_path, rules, log_fn=None):
    if log_fn is None:
        def log_fn(msg):
            print(msg, flush=True)

    if olefile is None:
        log_fn("[오류] olefile 패키지 필요")
        return None, [], 0

    if not os.path.exists(src_path):
        log_fn(f"[오류] 원본 파일 없음: {src_path}")
        return None, [], 0

    BACKUP_DIR = os.path.join(os.path.dirname(out_path), "backup")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = os.path.basename(src_path).replace('.hwp', f'_bak_{time.strftime("%H%M%S")}.hwp')
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(src_path, backup_path)
    log_fn(f"  백업: {backup_path}")

    ole = olefile.OleFileIO(src_path, write_mode=False)
    all_stream_data = {}
    stream_list = ole.listdir()
    for sp in stream_list:
        sn = '/'.join(sp)
        all_stream_data[sn] = ole.openstream(sn).read()
    ole.close()

    total_changes = 0
    stream_updates = {}
    change_log = []

    for sp in stream_list:
        sn = '/'.join(sp)
        if sp[0] != "BodyText":
            continue
        raw = all_stream_data[sn]
        try:
            dec = zlib.decompress(raw, -15)
        except zlib.error:
            log_fn(f"  [경고] {sn}: 압축해제 실패 - 건너뜀")
            continue

        records = parse_records(dec)
        log_fn(f"\n  {sn}: {len(records)}개 레코드, 압축={len(raw):,}, 해제={len(dec):,}")

        records, stream_changes, modified_rec_count, rec_change_log = apply_rules_to_records(records, rules)
        change_log.extend(rec_change_log)
        total_changes += stream_changes

        log_fn(f"  텍스트 레코드 수정: {modified_rec_count}개, 교정: {stream_changes}건")

        if stream_changes > 0:
            compressed, new_dec, level = compress_stream(records, len(raw))
            if compressed is None:
                log_fn(f"  [오류] 압축 불가! 파일이 너무 커짐")
                return None, change_log, total_changes
            stream_updates[sn] = compressed
            log_fn(f"  압축(level={level}): {len(compressed):,} / {len(raw):,} (여유: {len(raw) - len(compressed):,})")

    if not stream_updates:
        log_fn(f"\n  변경된 스트림 없음")
        return out_path, change_log, 0

    final_path = write_stream_to_hwp(src_path, out_path, stream_updates)
    log_fn(f"\n  출력 파일: {final_path}")
    log_fn(f"  출력 크기: {os.path.getsize(final_path):,} bytes")
    log_fn(f"  총 교정: {total_changes}건")

    return final_path, change_log, total_changes
