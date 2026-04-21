import os

BASE = r"C:\Users\doris\Documents\nootbook\Chess"

NOTES = {
    "09_구매가이드\\체스 구매 가이드.md": """---
tags: [체스, 구매, 장비, 가이드]
date: 2026-04-19
---

# 체스 구매 가이드

## 1. 체스 세트 종류

### 1.1 나무 체스 세트 (추천)
- **스타운턴(Staunton) 세트**: 공식 대회용 표준 디자인
- **장미나무(Rosewood) 세트**: 고급스러운 색감과 무게감
- **흑단(Ebony) 세트**: 최고급 소재, 프로용
- **합판/원목 보드**: 내구성 좋고 가격 합리적

### 1.2 자석 체스 세트 (여행용)
- 이동 중에도 기물이 고정되어 편리
- 접이식 보드 + 기물 보관함 일체형
- 가격: 20,000~50,000원대
- 추천: ColorGo Magnetic Travel Chess Set (약 37,000원)

### 1.3 전자 체스 세트
- LCD 화면 내장, AI 대전 가능
- 레벨 조절 기능 (초보자~전문가)
- "Why" 수 설명 기능 탑재 모델도 있음
- 추천: Grandmaster Electronic Chess Set

### 1.4 토너먼트용 세트
- FIDE 공인 규격 (킹 높이 3.75인치)
- 가중식(Weighted) 기물 필수
- 보드에 좌표 표기(Notation) 필수
- DGT 체스 시계와 호환

---

## 2. 한국에서 체스 구매처

### 2.1 온라인 쇼핑몰
| 쇼핑몰 | 특징 | 가격대 |
|---------|------|--------|
| **쿠팡** | 빠른 배송, 다양한 선택 | 15,000~200,000원 |
| **11번가** | 명인랜드 등 전문 브랜드 | 20,000~150,000원 |
| **네이버 쇼핑** | 가격 비교 용이 | 다양 |
| **G마켓** | 수입품 많음 | 10,000~300,000원 |
| **naturebridge.kr** | 자석 체스 세트 전문 | 30,000~50,000원 |

### 2.2 해외 직구
| 쇼핑몰 | 특징 | 배송 |
|--------|------|------|
| **World Chess Shop** (shop.worldchess.com) | FIDE 공식 스토어 | 해외배송 |
| **ChessBazaar** (chessbazaar.com) | 인도 수공예 나무 세트 | 해외배송 |
| **USCF Sales** (uscfsales.com) | 미국 체스 연맹 스토어 | 해외배송 |
| **Amazon** | 다양한 브랜드, 리뷰 풍부 | 해외배송 |

### 2.3 오프라인 매장
- **교보문고/영풍문고**: 입문용 체스 세트 취급
- **보드게임 전문점**: 강남, 홍대 등
- **대형 마트**: 롯데마트, 이마트 (시즌 한정)

---

## 3. 체스 시계

| 모델 | 가격 | 특징 |
|------|------|------|
| **DGT 3000** | 약 $95 | FIDE 공인, 디지털 |
| **DGT 2500** | 약 $95 | 인기 모델 |
| **Analog 체스시계** | 20,000~50,000원 | 아날로그 방식 |

---

## 4. 구매 추천 가이드

### 초보자 추천 세트
1. **자석 체스 세트** (2~5만원대): 가성비 최고
2. **합판 스타운턴 세트** (3~7만원대): 본격 학습용

### 중급자 추천 세트
1. **가중식 스타운턴 세트** (7~15만원대): 클럽 활동용
2. **원목 보드 + 가중식 기물** (10~20만원대): 대회 준비용

### 전문가 추천 세트
1. **토너먼트 세트** (15~30만원대): FIDE 공인 규격
2. **장미나무/흑단 세트** (20~50만원대): 수집가용

---

## 5. 구매 시 체크리스트

- [ ] 킹 높이 3.75인치 (토너먼트 규격)
- [ ] 보드 칸 크기 2~2.25인치
- [ ] 기물 가중(Weighted) 여부
- [ ] 보드 좌표 표기 여부
- [ ] 여분 퀸 포함 여부
- [ ] 보관함/가방 포함 여부
- [ ] 소재 확인 (나무/플라스틱/금속)
""",

    "09_구매가이드\\체스 훈련집 & 교재.md": """---
tags: [체스, 훈련집, 교재, 책, 학습]
date: 2026-04-19
---

# 체스 훈련집 & 교재

## 1. 한국어 체스 교재

### 1.1 입문서
| 도서 | 저자 | 출판사 | 특징 |
|------|------|--------|------|
| **체스가 궁금한 당신을 위한** | - | - | 체스 입문 가이드, 전략/전술 기초 |
| **체스교본** | 이상범 | 서락 (2008) | 체스 기초~기술 체계적 정리, 23단계 구성 |
| **DK 체스 바이블** | 클레어 서머스케일 | - | 그림으로 배우는 체스 정석, 양장본 |
| **어린이를 위한 체스 따라잡기** | - | - | 어린이 눈높이 맞춤, 10가지 핵심 내용 |

### 1.2 전술/실전서
| 도서 | 저자 | 출판사 | 특징 |
|------|------|--------|------|
| **1001 체크메이트# (개정판)** | 프레드 라인필드 | - | 체크메이트 기법 고전, 해답 보강/오류 수정 |
| **체스 챔피언** | - | 사이버출판사 (2022) | 이기는 체스 게임의 법칙 |
| **아이체스(Ichess) 시리즈** | - | - | 만화로 배우는 체스, 대표 예제 수록 |

---

## 2. 영문 체스 훈련집 (필수 추천)

### 2.1 초보자용 (레이팅 0~1200)
| 도서 | 저자 | 내용 | 추천도 |
|------|------|------|--------|
| **Bobby Fischer Teaches Chess** | Bobby Fischer | 체크메이트 기초, 프로그래밍 방식 | ⭐⭐⭐⭐⭐ |
| **How to Win at Chess** | Levy Rozman (GothamChess) | 현대적이고 이해하기 쉬운 입문서 | ⭐⭐⭐⭐⭐ |
| **Logical Chess: Move by Move** | Irving Chernev | 모든 수를 설명하는 전략 이해 | ⭐⭐⭐⭐⭐ |
| **Winning Chess Strategy for Kids** | Jeff Coakley | 어른도 유용한 단계별 전략 | ⭐⭐⭐⭐ |
| **1001 Chess Exercises for Beginners** | Masetti & Messa | 퍼즐 사다리식 훈련 | ⭐⭐⭐⭐⭐ |

### 2.2 중급자용 (레이팅 1200~1800)
| 도서 | 저자 | 내용 | 추천도 |
|------|------|------|--------|
| **The Woodpecker Method Vol.1 & 2** | Hans Renfelt | 반복 훈련으로 전술 시야 향상 | ⭐⭐⭐⭐⭐ |
| **100 Endgames You Must Know** | Jesus de la Villa | 엔딩 이론 필수 가이드 | ⭐⭐⭐⭐⭐ |
| **How to Reassess Your Chess** | Jeremy Silman | 포지셔널 체스 전략의 바이블 | ⭐⭐⭐⭐⭐ |
| **Complete Endgame Course** | Jeremy Silman | 레이팅별 엔딩 교육 | ⭐⭐⭐⭐ |
| **Chess Structures: A Grandmaster Guide** | Mauricio Flores Rios | 폰 구조별 플랜 정리 | ⭐⭐⭐⭐ |
| **100 Tactical Patterns You Must Know Workbook** | Frank Erwich | 500+ 훈련 문제 | ⭐⭐⭐⭐⭐ |

### 2.3 상급자용 (레이팅 1800+)
| 도서 | 저자 | 내용 | 추천도 |
|------|------|------|--------|
| **Think Like a Grandmaster** | Alexander Kotov | 후보 수 분석 트리 | ⭐⭐⭐⭐⭐ |
| **Positional Decision Making in Chess** | Boris Gelfand | 공간/변환/실전 선택 | ⭐⭐⭐⭐ |
| **Grandmaster Preparation: Calculation** | Jacob Aagaard | 계산력 훈련 | ⭐⭐⭐⭐ |
| **Complete Manual of Positional Chess Vol.1** | Sakaev & Landa | 포지셔널 플레이 심화 | ⭐⭐⭐⭐ |
| **Chess: 5334 Problems, Combinations, and Games** | Laszlo Polgar | 5000+ 퍼즐 대학습서 | ⭐⭐⭐⭐⭐ |

---

## 3. 온라인 체스 훈련 플랫폼

### 3.1 Chess.com (무료 + 유료)
| 기능 | 무료 | 프리미엄 |
|------|------|----------|
| 퍼즐 | 5개/일 | 무제한 |
| 레슨 | 1개/주 | 무제한 |
| 게임 분석 | 제한적 | 무제한 |
| 커스텀 퍼즐 | O | O |
| 일일 퍼즐 | O | O |

### 3.2 Lichess.org (완전 무료)
- 무제한 퍼즐
- 무료 게임 분석
- 체스 엔진 (Stockfish) 통합
- 스터디 기능
- 토너먼트 참가

### 3.3 ChessBase (전문가용)
- ChessBase 18: 데이터베이스 관리
- Mega Database 2025: 1100만+ 게임
- Opening Encyclopaedia 2025: 오프닝 백과
- Fritz 20: 체스 엔진 + 트레이닝

---

## 4. 훈련집 추천 학습 순서

### Step 1: 기초 (1~3개월)
1. Bobby Fischer Teaches Chess
2. How to Win at Chess (Levy Rozman)
3. Chess.com 퍼즐 매일 10개 이상

### Step 2: 전술 강화 (3~6개월)
1. 1001 Chess Exercises for Beginners
2. 100 Tactical Patterns You Must Know Workbook
3. The Woodpecker Method Vol.1

### Step 3: 전략 & 엔딩 (6~12개월)
1. Logical Chess: Move by Move
2. How to Reassess Your Chess
3. 100 Endgames You Must Know

### Step 4: 실전 심화 (12개월+)
1. Chess Structures: A Grandmaster Guide
2. Think Like a Grandmaster
3. Chess: 5334 Problems, Combinations, and Games

---

## 5. 구매처

### 한국어 도서
- **교보문고**: kyobobook.co.kr
- **알라딘**: aladin.co.kr
- **예스24**: yes24.com
- **인터파크 도서**: book.interpark.com

### 영문 도서
- **Amazon**: amazon.com
- **USCF Sales**: uscfsales.com
- **World Chess Shop**: shop.worldchess.com
- **Everyman Chess**: everymanchess.com

### 전자책
- **Kindle**: amazon.com/kindle
- **Google Play Books**: play.google.com/books
"""
}

def main():
    print("=" * 40)
    print("  체스 구매 & 훈련집 노트 생성")
    print("=" * 40)

    count = 0
    for name, content in NOTES.items():
        path = os.path.join(BASE, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        count += 1
        print(f"  [{count}/{len(NOTES)}] {name}")

    print(f"\n  총 {len(NOTES)}개 노트 생성 완료!")
    print(f"  경로: {BASE}")

if __name__ == "__main__":
    main()
