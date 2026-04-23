---
name: "hwp-proofreading"
description: "HWP Korean document proofreading system. Invoke when user asks to proofread/correct HWP files, fix spacing, apply Korean rules, or verify Chinese character changes."
---

# HWP Korean Document Proofreading Skill

## Description

Automated proofreading system for HWP (Hancom Word Processor) files that applies Korean spacing rules, Chinese-Korean place name conversions, quote normalization, and dependency noun corrections. Supports J/L/M file types with full validation and Git integration.

## When to Use

- User asks to proofread or correct HWP files
- User mentions Korean spacing rules (띄어쓰기)
- User wants to apply Chinese-Korean conversion rules (중한규칙)
- User needs to verify Chinese character preservation (한자 검증)
- User asks to compare original vs corrected HWP files
- User mentions dependency noun corrections (의존명사 교정)
- User wants segment analysis of HWP correction rules

## Instructions

### Step 1: Identify File Type and Paths

Determine which file(s) to process:
- **J file**: `【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp`
- **L file**: `【大中朝 16】L 1787-1958--172--20240920.hwp`
- **M file**: `【大中朝 17】M 1959-2093--135--20240920.hwp`

Original files are in `C:\Users\doris\Desktop\新词典\`
Rule files are in `C:\AMD\AJ\hwp_proofreading_package\`

### Step 2: Run Core Correction Engine

Execute the appropriate correction script:

```
# Single file correction (core engine)
python c:\Users\doris\.agent-skills\fix_J_record.py

# Integrated system for multiple files
python c:\Users\doris\.agent-skills\hwp_correction_system.py --files J L M

# JLK complete correction with COM automation
python c:\Users\doris\.agent-skills\JLK_완전교정_시스템.py
```

The core engine (fix_J_record.py) runs a 7-step pipeline:
1. Original file integrity verification (OLE structure check)
2. Text extraction + rule generation (3 stages: China rules → TXT rules → Dependency nouns)
3. Record-level modification (zlib decompress → parse records → apply rules → recompress)
4. OLE stream writing (direct binary modification to preserve structure)
5. Output file verification (OLE + decompression + record count)
6. Correction result validation (before/after comparison)
7. HWP file open test

### Step 3: Apply Correction Rules

Three stages of rules are applied in order:

**Stage 1 - Chinese-Korean Rules (중한규칙)**:
- `나라→조` conversion: 당나라→당조, 송나라→송조, etc.
- Place name conversion from `rules_china_place.txt` (270 rules)

**Stage 2 - TXT Integration Rules (TXT 통합규칙)**:
- General corrections from `rules_documentation.txt` (1149 rules)
- Typo fixes, notation standardization

**Stage 3 - Dependency Noun Spacing (의존명사 띄어쓰기)**:
- 26 dependency noun categories with NOSPLIT exception lists (~800 compound words)
- Categories: 것, 수, 따위, 사이, 뿐, 척, 이상, 이하, 등, 때, 때문, 번, 데, 대로, 만큼, 중, 줄, 듯, 채, etc.
- Punctuation: 쌍따옴표→홑따옴표, 가운데점→쉼표

### Step 4: Validate Results

Run validation scripts after correction:

```
# Chinese character precise validation
python c:\Users\doris\.agent-skills\check_chinese_precise.py

# Segment detail analysis (1419 rules)
python c:\Users\doris\.agent-skills\segment_detail_analysis.py

# JLK full comparison
python c:\Users\doris\.agent-skills\compare_JLK_full.py
```

Key validation checks:
- Chinese character count must be identical between original and corrected
- Rule-explained changes vs unexplained changes (unexplained = 0 required)
- NOSPLIT exceptions must prevent over-correction
- OLE directory entry size field must match compressed data size

### Step 5: Git Commit

Commit all changes with proper attribution:
```
git config user.name "zhudoris475-gif"
git config user.email "zhudoris475@gmail.com"
git add -A
git commit -m "descriptive message about changes"
```

## Technical Details

### HWP File Format
- OLE compound document structure
- BodyText/Section0 stream contains compressed records
- zlib compression with wbits=-15 (raw deflate)
- Text records have tag_id=67, encoded as UTF-16-LE
- Record header: 4 bytes (tag_id:12bit + level:4bit) + 4 bytes (size)

### Critical Implementation Notes
- Always use direct binary modification instead of olefile.write_stream() to preserve OLE structure
- Preserve original padding beyond compressed data (do NOT use null bytes)
- Update OLE directory entry size field when compressed data size changes
- Handle read-only files with os.chmod before deletion
- Use UUID-based temporary files (.bin) during processing
- Verify decompression after recompression to catch corruption early

### NOSPLIT Exception System
Each dependency noun has a NOSPLIT set of compound words that must NOT be split:
- Example: `수도` is in SU_NOSPLIT, so `수도` → `수 도` is prevented
- Example: `것같다` → `것 같다` IS corrected (not in GEOT_NOSPLIT)
- NOSPLIT sets contain ~800 total compound words across 26 categories

### Known Issues and Solutions
| Issue | Solution |
|-------|----------|
| HWP file won't open after correction | Check OLE directory entry size field + padding preservation |
| Excessive null padding | Use original file's existing padding instead of null bytes |
| Chinese characters deleted | Verify against rule files; rule-specified deletions are normal |
| Read-only file errors | Add os.chmod(file, stat.S_IWRITE \| stat.S_IREAD) before deletion |
| Compressed data too large | Retry with zlib.compress level=1 |

## Examples

### Example 1: Correct a single J file
```
User: "J파일 교정해주세요"
→ Run: python fix_J_record.py
→ Verify: check_chinese_precise.py
→ Commit: git add -A && git commit -m "J파일 교정 완료"
```

### Example 2: Full JLK correction with validation
```
User: "JLK 세파일 모두 교정하고 검증해주세요"
→ Run: python hwp_correction_system.py --files J L M
→ Run: python segment_detail_analysis.py
→ Run: python compare_JLK_full.py
→ Commit: git add -A && git commit -m "JLK 교정+검증 완료"
```

### Example 3: Verify Chinese character preservation
```
User: "한자 삭제 없는지 확인해주세요"
→ Run: python check_chinese_precise.py
→ Check: "규칙외 변경: 0건" in output
→ Report: All changes are rule-explained (normal)
```
