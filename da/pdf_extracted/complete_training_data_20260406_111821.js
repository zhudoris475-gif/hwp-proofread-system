const completeTrainingData = [
  {
    "instruction": "가욱데점(·)은 어떻게 사용하나요?",
    "input": "",
    "output": "가욱데점(중점)은 열거할 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 병렬되는 단어들 사이에 사용합니다\n2. 나열할 때 사용합니다\n\n예시:\n- 사과·배·바나나\n- 봄·여름·가을·겨울",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "두점(:)은 어떻게 사용하나요?",
    "input": "",
    "output": "두점(콜론)은 뒤에 오는 내용이 앞 내용을 설명하거나 구체적으로 나타낼 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 앞 내용을 뒤에서 설명할 때 사용합니다\n2. 인용문 앞에 사용합니다\n3. 열거할 때 사용합니다\n\n예시:\n- 다음과 같다: 사과, 배, 바나나\n- 그는 말했다: \"안녕하세요.\"",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "반두점(;)은 어떻게 사용하나요?",
    "input": "",
    "output": "반두점(세미콜론)은 문장 속에서 계층적으로 구분할 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 쉼표보다 더 큰 구분이 필요할 때 사용합니다\n2. 병렬되는 절 사이에 사용합니다\n\n예시:\n- 그는 똑똑하다; 그러나 게으르다.\n- 오늘은 날씨가 좋다; 내일은 비가 온다고 한다.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "생략부호(…)는 어떻게 사용하나요?",
    "input": "",
    "output": "생략부호는 말이나 글을 생략했음을 나타내는 문장부호입니다.\n\n사용 규칙:\n1. 인용문에서 일부를 생략했을 때 사용합니다\n2. 말을 더듬거나 중단했을 때 사용합니다\n3. 열거를 생략할 때 사용합니다\n\n예시:\n- \"그는 말했다…그리고 갔다.\"\n- 사과, 배, 바나나… 등을 샀다.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "붙임표(-)는 어떻게 사용하나요?",
    "input": "",
    "output": "붙임표(하이픈)는 단어를 붙여 쓸 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 복합어를 만들 때 사용합니다\n2. 줄바꿈 시 단어를 나눌 때 사용합니다\n\n예시:\n- 조선-중국\n- 불-꽃놀이",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"근\"은 어떻게 쓰나요?",
    "input": "",
    "output": "근은 관형사로, \"가까운\"의 뜻을 나타냅니다.\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"런\"은 어떻게 쓰나요?",
    "input": "",
    "output": "런은 관형사로, \"그러한\"의 뜻을 나타냅니다.\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"만\"은 어떻게 쓰나요?",
    "input": "",
    "output": "만은 관형사로, \"딴\" 또는 \"다른\"의 뜻을 나타냅니다.\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"야\"는 어떻게 쓰나요?",
    "input": "",
    "output": "야는 관형사로, \"어떤\"의 뜻을 나타냅니다.\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"일대\"는 어떻게 쓰나요?",
    "input": "",
    "output": "일대는 관형사로, \"그런\" 또는 \"그러한\"의 뜻을 나타냅니다.\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"한다하는\"은 어떻게 쓰나요?",
    "input": "",
    "output": "한다하는은 관형사로, \"그렇다는\" 또는 \"그러한\"의 뜻을 나타냅니다.\n\n예시:\n- 한다하는 사람\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "의존명사는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "의존명사는 앞에 오는 단어와 띄여쓴다.\n\n의존명사는 뜻이 완전하지 않아 다른 말에 의존하여 쓰이는 명사이다.\n\n예시:\n- 책 읽기 (책읽기 ✗)\n- 산 보기 (산보기 ✗)\n- 밥 먹음 (밥먹음 ✗)\n\n의존명사 종류: 일, 것, 리, 바, 뿐, 대로, 만큼, 대로, 적, 끝, 나름, 따름 등",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  },
  {
    "instruction": "단위명사는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "단위명사는 앞에 오는 수관형사와 붙여쓰고, 뒤에 오는 단어와는 띄여쓴다.\n\n예시:\n- 한 개 (한개)\n- 두 마리 (두마리)\n- 세 권 (세권)\n- 네 사람 (네사람)\n\n단위명사 종류: 개, 마리, 권, 장, 명, 사람, 번, 번지, 켤레, 킬로그람, 미터 등",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  },
  {
    "instruction": "조사는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "조사는 앞에 오는 단어와 붙여쓴다.\n\n예시:\n- 학교에 (학교 에 ✗)\n- 책을 (책 을 ✗)\n- 친구와 (친구 와 ✗)\n- 집에서 (집 에서 ✗)\n\n조사 종류: 은/는, 이/가, 을/를, 에, 에서, 로/으로, 와/과, 하고, 보다, 처럼 등",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  },
  {
    "instruction": "어미는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "어미는 앞에 오는 용언과 붙여쓴다.\n\n예시:\n- 가다 (가 다 ✗)\n- 먹었다 (먹었 다 ✗)\n- 예쁘다 (예쁘 다 ✗)\n- 학생이다 (학생이 다 ✗)\n\n어미는 용언(동사, 형용사)에 붙어 문법적 기능을 나타내는 말이다.",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  },
  {
    "instruction": "접두사는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "접두사는 뒤에 오는 단어와 붙여쓴다.\n\n예시:\n- 새로운 (새 로운 ✗)\n- 원대한 (원 대한 ✗)\n- 불가능한 (불 가능한 ✗)\n- 재입학 (재 입학 ✗)\n\n접두사 종류: 새, 원, 불, 재, 맨, 첫, 각, 군, 양, 전, 후, 대, 중, 최, 초, 반, 왕, 시, 월, 하, 별, 만, 수, 온, 온갖, 옹근, 현, 헌, 이, 그, 저, 어느, 무슨, 어떤, 몇, 스무, 서른, 마흔, 쉰, 예순, 일흔, 여든, 아흔 등",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  },
  {
    "instruction": "접미사는 어떻게 띄여쓰나요?",
    "input": "",
    "output": "접미사는 앞에 오는 단어와 붙여쓴다.\n\n예시:\n- 선생님 (선생 님 ✗)\n- 나무꾼 (나무 꾼 ✗)\n- 책상뿐 (책상 뿐 ✗)\n- 집안 (집 안 ✗)\n\n접미사 종류: 님, 씨, 꾼, 뿐, 만, 대로, 적, 스럽, 답, 하다, 되다, 없다, 있다, 싶다, 같다 등",
    "category": "spacing_rule",
    "source": "pdf_extracted"
  }
];

if (typeof module !== "undefined" && module.exports) { module.exports = completeTrainingData; }
