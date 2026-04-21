import os
import re

VAULT = r"C:\Users\doris\Documents\nootbook"
CHESS = os.path.join(VAULT, "Chess")

FOLDER_LINK_FIXES = {
    "[[Chess/01_규칙]]": "[[Chess/01_규칙/체스 기본 규칙|01_규칙]]",
    "[[Chess/02_전술]]": "[[Chess/02_전술/체스 핵심 전술|02_전술]]",
    "[[Chess/03_오프닝]]": "[[Chess/03_오프닝/체스 오프닝 가이드|03_오프닝]]",
    "[[Chess/04_엔딩]]": "[[Chess/04_엔딩/체스 엔딩 가이드|04_엔딩]]",
    "[[Chess/05_기보]]": "[[Chess/05_기보/체스 기보 표기법|05_기보]]",
    "[[Chess/06_엔진]]": "[[Chess/06_엔진/체스 엔진 & 라이브러리|06_엔진]]",
    "[[Chess/07_프로그램]]": "[[Chess/07_프로그램/chess_game|07_프로그램]]",
    "[[Chess/08_데이터베이스]]": "[[Chess/08_데이터베이스/ChessBase 데이터 & 리소스|08_데이터베이스]]",
    "[[Chess/09_구매가이드]]": "[[Chess/09_구매가이드/체스 구매 가이드|09_구매가이드]]",
    "[[Chess/10_중국체스]]": "[[Chess/10_중국체스/중국체스 학습 가이드|10_중국체스]]",
}

HOME_NOTE = """---
title: "체스 노트 홈"
category: "Chess"
subcategory: "인덱스"
tags:
  - Chess/인덱스
date: "2026-04-19"
---

# ♟ 체스 노트 홈

체스 학습을 위한 종합 노트 시스템입니다.

---

## 📂 폴더 구조

| 폴더 | 내용 | 메인 노트 |
|------|------|-----------|
| 01_규칙 | 기본 규칙, 기물 이동, 특수 규칙 | [[Chess/01_규칙/체스 기본 규칙\|체스 기본 규칙]] |
| 02_전술 | 포크, 핀, 스큐어, 디스커버드 어택 | [[Chess/02_전술/체스 핵심 전술\|체스 핵심 전술]] |
| 03_오프닝 | 오픈/세미오픈/클로즈드 게임 | [[Chess/03_오프닝/체스 오프닝 가이드\|체스 오프닝 가이드]] |
| 04_엔딩 | 기본 엔딩, 룩 엔딩, 폰 엔딩 | [[Chess/04_엔딩/체스 엔딩 가이드\|체스 엔딩 가이드]] |
| 05_기보 | 대수 기보법, FEN, PGN | [[Chess/05_기보/체스 기보 표기법\|체스 기보 표기법]] |
| 06_엔진 | Stockfish, python-chess, UCI | [[Chess/06_엔진/체스 엔진 & 라이브러리\|체스 엔진 & 라이브러리]] |
| 07_프로그램 | 체스 게임 프로그램 | [[Chess/07_프로그램/chess_game\|chess_game.py]] |
| 08_데이터베이스 | ChessBase, Mega Database | [[Chess/08_데이터베이스/ChessBase 데이터 & 리소스\|ChessBase 데이터 & 리소스]] |
| 09_구매가이드 | 체스 세트 구매, 훈련집 | [[Chess/09_구매가이드/체스 구매 가이드\|체스 구매 가이드]] |
| 10_중국체스 | 중국체스(象棋) 학습 | [[Chess/10_중국체스/중국체스 학습 가이드\|중국체스 학습 가이드]] |

---

## 📝 전체 노트 목록

### 규칙 & 기초
- [[Chess/01_규칙/체스 기본 규칙\|체스 기본 규칙]]
- [[Chess/05_기보/체스 기보 표기법\|체스 기보 표기법]]

### 전술 & 전략
- [[Chess/02_전술/체스 핵심 전술\|체스 핵심 전술]]
- [[Chess/03_오프닝/체스 오프닝 가이드\|체스 오프닝 가이드]]
- [[Chess/04_엔딩/체스 엔딩 가이드\|체스 엔딩 가이드]]

### 도구 & 자료
- [[Chess/06_엔진/체스 엔진 & 라이브러리\|체스 엔진 & 라이브러리]]
- [[Chess/07_프로그램/chess_game\|chess_game.py]]
- [[Chess/08_데이터베이스/ChessBase 데이터 & 리소스\|ChessBase 데이터 & 리소스]]

### 구매 & 학습
- [[Chess/09_구매가이드/체스 구매 가이드\|체스 구매 가이드]]
- [[Chess/09_구매가이드/체스 훈련집 & 교재\|체스 훈련집 & 교재]]

### 중국체스
- [[Chess/10_중국체스/중국체스 학습 가이드\|중국체스 학습 가이드]]
- [[Chess/10_중국체스/중국체스 커뮤니티 & 자료\|중국체스 커뮤니티 & 자료]]

---

## 🗺 학습 경로

| 주차 | 학습 내용 | 노트 |
|------|-----------|------|
| 1주차 | 기본 규칙 → 기보 표기법 | [[Chess/01_규칙/체스 기본 규칙\|규칙]] → [[Chess/05_기보/체스 기보 표기법\|기보]] |
| 2주차 | 핵심 전술 → 퍼즐 풀기 | [[Chess/02_전술/체스 핵심 전술\|전술]] |
| 3주차 | 오프닝 가이드 → 집중 학습 | [[Chess/03_오프닝/체스 오프닝 가이드\|오프닝]] |
| 4주차 | 엔딩 기본 → 룩 엔딩 연습 | [[Chess/04_엔딩/체스 엔딩 가이드\|엔딩]] |
| 지속 | 엔진 활용 → DB 분석 | [[Chess/06_엔진/체스 엔진 & 라이브러리\|엔진]] → [[Chess/08_데이터베이스/ChessBase 데이터 & 리소스\|DB]] |

---

## 🌐 온라인 플랫폼

### 국제체스
- [Chess.com](https://www.chess.com) — 퍼즐, 레슨, 게임
- [Lichess.org](https://lichess.org) — 무료, 오픈소스
- [ChessTempo](https://chesstempo.com) — 전술 훈련
- [ChessBase Online](https://en.chessbase.com/) — 데이터베이스 & 분석

### 중국체스
- [Xiangqi.com](https://www.xiangqi.com) — 글로벌 중국체스
- [天天象棋](https://xiangqi.qq.com) — 텐센트, 가장 인기
- [象棋微学堂](https://www.xqwxt.com.cn) — 세계 챔피언 강의

---

## 🔌 설치된 플러그인

| 플러그인 | 기능 |
|----------|------|
| Chess Study | PGN 뷰어/에디터, 체스 학습 |
| Chesser | 체스 게임 뷰어/에디터 |
| Chessboard Viewer | 체스 포지션 다이어그램 |
| Translate | Google/DeepL/Azure 번역 |
| Image Toolkit | 이미지 확대, 줌, 회전, 갤러리 |
"""


def fix_links_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for old_link, new_link in FOLDER_LINK_FIXES.items():
        content = content.replace(old_link, new_link)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 50)
    print("  Vault 링크 수정 & 노트 재정리")
    print("=" * 50)

    print("\n[1/3] 체스 노트 홈 재작성...")
    home_path = os.path.join(CHESS, "체스 노트 홈.md")
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(HOME_NOTE.strip() + "\n")
    print("  -> 체스 노트 홈 재작성 완료")

    print("\n[2/3] 모든 노트 링크 수정...")
    fixed_count = 0
    for root, dirs, files in os.walk(CHESS):
        for fname in files:
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                if fix_links_in_file(fpath):
                    fixed_count += 1
                    rel = os.path.relpath(fpath, CHESS)
                    print(f"  -> 수정: {rel}")

    print(f"\n  -> 총 {fixed_count}개 파일 링크 수정 완료")

    print("\n[3/3] 노트 내용 재정리...")

    notes_to_fix = {}

    rules_path = os.path.join(CHESS, "01_규칙", "체스 기본 규칙.md")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/02_전술/체스 핵심 전술|체스 핵심 전술]]
- [[Chess/05_기보/체스 기보 표기법|체스 기보 표기법]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[rules_path] = content

    tactics_path = os.path.join(CHESS, "02_전술", "체스 핵심 전술.md")
    if os.path.exists(tactics_path):
        with open(tactics_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/01_규칙/체스 기본 규칙|체스 기본 규칙]]
- [[Chess/03_오프닝/체스 오프닝 가이드|체스 오프닝 가이드]]
- [[Chess/04_엔딩/체스 엔딩 가이드|체스 엔딩 가이드]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[tactics_path] = content

    opening_path = os.path.join(CHESS, "03_오프닝", "체스 오프닝 가이드.md")
    if os.path.exists(opening_path):
        with open(opening_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/02_전술/체스 핵심 전술|체스 핵심 전술]]
- [[Chess/04_엔딩/체스 엔딩 가이드|체스 엔딩 가이드]]
- [[Chess/05_기보/체스 기보 표기법|체스 기보 표기법]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[opening_path] = content

    ending_path = os.path.join(CHESS, "04_엔딩", "체스 엔딩 가이드.md")
    if os.path.exists(ending_path):
        with open(ending_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/03_오프닝/체스 오프닝 가이드|체스 오프닝 가이드]]
- [[Chess/06_엔진/체스 엔진 & 라이브러리|체스 엔진 & 라이브러리]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[ending_path] = content

    notation_path = os.path.join(CHESS, "05_기보", "체스 기보 표기법.md")
    if os.path.exists(notation_path):
        with open(notation_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/01_규칙/체스 기본 규칙|체스 기본 규칙]]
- [[Chess/03_오프닝/체스 오프닝 가이드|체스 오프닝 가이드]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[notation_path] = content

    engine_path = os.path.join(CHESS, "06_엔진", "체스 엔진 & 라이브러리.md")
    if os.path.exists(engine_path):
        with open(engine_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/04_엔딩/체스 엔딩 가이드|체스 엔딩 가이드]]
- [[Chess/07_프로그램/chess_game|chess_game.py]]
- [[Chess/08_데이터베이스/ChessBase 데이터 & 리소스|ChessBase 데이터 & 리소스]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[engine_path] = content

    db_path = os.path.join(CHESS, "08_데이터베이스", "ChessBase 데이터 & 리소스.md")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/06_엔진/체스 엔진 & 라이브러리|체스 엔진 & 라이브러리]]
- [[Chess/09_구매가이드/체스 구매 가이드|체스 구매 가이드]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[db_path] = content

    purchase_path = os.path.join(CHESS, "09_구매가이드", "체스 구매 가이드.md")
    if os.path.exists(purchase_path):
        with open(purchase_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/09_구매가이드/체스 훈련집 & 교재|체스 훈련집 & 교재]]
- [[Chess/08_데이터베이스/ChessBase 데이터 & 리소스|ChessBase 데이터 & 리소스]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[purchase_path] = content

    workbook_path = os.path.join(CHESS, "09_구매가이드", "체스 훈련집 & 교재.md")
    if os.path.exists(workbook_path):
        with open(workbook_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/09_구매가이드/체스 구매 가이드|체스 구매 가이드]]
- [[Chess/02_전술/체스 핵심 전술|체스 핵심 전술]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[workbook_path] = content

    xiangqi_learn_path = os.path.join(CHESS, "10_중국체스", "중국체스 학습 가이드.md")
    if os.path.exists(xiangqi_learn_path):
        with open(xiangqi_learn_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/10_중국체스/중국체스 커뮤니티 & 자료|중국체스 커뮤니티 & 자료]]
- [[Chess/01_규칙/체스 기본 규칙|체스 기본 규칙]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[xiangqi_learn_path] = content

    xiangqi_community_path = os.path.join(CHESS, "10_중국체스", "중국체스 커뮤니티 & 자료.md")
    if os.path.exists(xiangqi_community_path):
        with open(xiangqi_community_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[[Chess/" not in content:
            content += """

---

## 관련 노트

- [[Chess/10_중국체스/중국체스 학습 가이드|중국체스 학습 가이드]]
- [[Chess/06_엔진/체스 엔진 & 라이브러리|체스 엔진 & 라이브러리]]
- [[Chess/체스 노트 홈|체스 노트 홈]]
"""
            notes_to_fix[xiangqi_community_path] = content

    for fpath, content in notes_to_fix.items():
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        rel = os.path.relpath(fpath, CHESS)
        print(f"  -> 관련노트 추가: {rel}")

    print(f"\n  -> 총 {len(notes_to_fix)}개 파일 관련노트 추가 완료")

    print("\n" + "=" * 50)
    print("  완료!")
    print("=" * 50)
    print("\n수정 내역:")
    print("  1. community-plugins.json 올바른 위치로 이동")
    print("  2. 폴더 링크 -> 파일 링크로 수정")
    print("  3. 체스 노트 홈 재작성 (테이블 구조 개선)")
    print("  4. 모든 노트에 관련노트 링크 추가")
    print("  5. 플러그인 정보 섹션 추가")
    print("\nObsidian을 재시작하세요!")


if __name__ == "__main__":
    main()
