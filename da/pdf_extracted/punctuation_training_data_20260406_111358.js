const punctuationTrainingData = [
  {
    "instruction": "마침표(.)는 어떻게 사용하나요?",
    "input": "",
    "output": "마침표는 문장이 끝났음을 나타내는 문장부호입니다.\n\n사용 규칙:\n1. 평서문 끝에 사용합니다\n2. 명령문 끝에 사용합니다\n3. 청유문 끝에 사용합니다\n\n예시:\n- 오늘은 날씨가 좋다.\n- 문을 닫아라.\n- 같이 가자.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "쉼표(,)는 어떻게 사용하나요?",
    "input": "",
    "output": "쉼표는 문장 속에서 잠시 쉬는 곳을 나타내는 문장부호입니다.\n\n사용 규칙:\n1. 문장 성분을 구분할 때 사용합니다\n2. 열거할 때 사용합니다\n3. 호응 관계에 있는 말 사이에 사용합니다\n\n예시:\n- 사과, 배, 바나나를 샀다.\n- 그는 똑똑하고, 착하다.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "물음표(?)는 어떻게 사용하나요?",
    "input": "",
    "output": "물음표는 의문문 끝에 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 의문문 끝에 사용합니다\n2. 의문을 나타내는 구문 끝에 사용합니다\n\n예시:\n- 오늘 무엇을 하겠는가?\n- 정말 그런가?",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "느낌표(!)는 어떻게 사용하나요?",
    "input": "",
    "output": "느낌표는 감탄이나 느낌을 나타내는 문장부호입니다.\n\n사용 규칙:\n1. 감탄문 끝에 사용합니다\n2. 명령문이나 청유문에서 강한 느낌을 줄 때 사용합니다\n\n예시:\n- 참 아름답구나!\n- 빨리 와라!",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "따옴표는 어떻게 사용하나요?",
    "input": "",
    "output": "따옴표는 인용이나 특별한 의미를 나타낼 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 낱따옴표('')는 인용할 때 사용합니다\n2. 겹따옴표(\"\")는 인용 안의 인용이나 특별한 의미를 나타낼 때 사용합니다\n\n예시:\n- 그는 '열심히 하자'고 말했다.\n- 이것이 바른 '길'이다.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "줄표(—)는 어떻게 사용하나요?",
    "input": "",
    "output": "줄표는 문장 속에서 설명이나 보충을 나타낼 때 사용하는 문장부호입니다.\n\n사용 규칙:\n1. 설명을 덧붙일 때 사용합니다\n2. 말을 고칠 때 사용합니다\n3. 대화에서 화자를 나타낼 때 사용합니다\n\n예시:\n- 우리 고향—평양—은 아름답다.\n- 그는—아니 그녀는—학생이다.",
    "category": "punctuation",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"불과\"는 어떻게 쓰나요?",
    "input": "",
    "output": "불과는 관형사로, \"불과 몇 해 동안\", \"불과 몇 사람\" 등으로 쓰입니다.\n\n예시:\n- 불과 몇 해 동안\n- 불과 몇 사람\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  },
  {
    "instruction": "\"뿔과\"는 어떻게 쓰나요?",
    "input": "",
    "output": "뿔과는 관형사로, \"뿔과 몇 사람\" 등으로 쓰입니다.\n\n예시:\n- 뿔과 몇 사람\n\n관형사로만 쓰이므로 언제나 뒤 단어와 띄여쓴다.",
    "category": "determinative",
    "source": "pdf_extracted"
  }
];

if (typeof module !== "undefined" && module.exports) { module.exports = punctuationTrainingData; }
