// 朝鲜语规范训练数据集
// 来源: 《朝鲜语规范集解说》(2019)
// 生成时间: 2024
// 总条目数: 426

const nonPronunciationData = [
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "15) 장소를 나타내는 고유명사와 관련한 띄여쓰기",
    "output": "15) 장소를 나타내는 고유명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 장소를 나타내는 고유명사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 130,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "16) 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기",
    "output": "16) 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 133,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "18) 붙여쓰편 ㅂ른 뜻이 생길 경수외 관련한 띄여쓰",
    "output": "18) 붙여쓰편 ㅂ른 뜻이 생길 경수외 관련한 띄여쓰",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 붙여쓰편 ",
        "른 뜻이 생길 경수외 관련한 띄여쓰"
      ],
      "paragraph_index": 142,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "제2장 수사 봐관 련한킈 \t 178",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 145,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "4) 수사가 힌체기관 이름과 결합될 뺴의 끠여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 151,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "그리고 수사 ‘여덟’만은 받침  ‘래’이  받침소리로 될경우, 즉 ‘여덟’로 끝나거나 그 아래 자음이  올 경우에는언제나 ‘ㄹ’로 발음한다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 366,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "그리고 제11항 [붙임 2]에 밝히여있다싶이  [ㄹ]받침소리를 가진 수사‘열, 여덟’아래에 오는 명사의  첫머리의순한소리도 된소리로 발음한다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 469,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "첫째, 모음토를 붙여보고 받침을 바로잡아 적어야 한다.",
    "output": "첫째, 모음토를 붙여보고 받침을 바로잡아 적어야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "첫째",
        " 모음토를 붙여보고 받침을 바로잡아 적어야 한다"
      ],
      "paragraph_index": 995,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "홀받침‘ㄱ,  ㄴ,  ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅅ,  ㅈ,  ㅊ, ㅋ,ㅌ, ㅍ, ㄲ, ㅆ’가운데서 어느 것을 받침으로 잡아야 하겠는가를 알려면 우선 모음토를 붙여보고 그 모음토",
    "output": "홀받침‘ㄱ,  ㄴ,  ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅅ,  ㅈ,  ㅊ, ㅋ,ㅌ, ㅍ, ㄲ, ㅆ’가운데서 어느 것을 받침으로 잡아야 하겠는가를 알려면 우선 모음토를 붙여보고 그 모음토의 첫소리로 발음하는 자음을 그 형태의 받침으로 바로잡아 적는다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "홀받침",
        "  ",
        "  ",
        "  ",
        "  "
      ],
      "paragraph_index": 996,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "둘받침‘ㅛ, ㅁ, ㄹ, ㄹ, ㄹ, ㅍ, ㅂ, ㅍ’은 모음토를 붙여봐서 토의 첫소리로 나는 것을 오른쪽에, 어간의 끝소리로 나는 것을 왼쪽에 바로잡아 적어야 한다.",
    "output": "둘받침‘ㅛ, ㅁ, ㄹ, ㄹ, ㄹ, ㅍ, ㅂ, ㅍ’은 모음토를 붙여봐서 토의 첫소리로 나는 것을 오른쪽에, 어간의 끝소리로 나는 것을 왼쪽에 바로잡아 적어야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "둘받침",
        "은 모음토를 붙여봐서 토의 첫소리로 나는 것을 오른쪽에",
        " 어간의 끝소리로 나는 것을 왼쪽에 바로잡아 적어야 한"
      ],
      "paragraph_index": 997,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "둘째, 토를 붙여보아 어간의 끝소리가 바뀔 때와 바뀌지  않을 때를 구별하여  받침을 바로잡아 적어야 한다.",
    "output": "둘째, 토를 붙여보아 어간의 끝소리가 바뀔 때와 바뀌지  않을 때를 구별하여  받침을 바로잡아 적어야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "둘째",
        " 토를 붙여보아 어간의 끝소리가 바뀔 때와 바뀌지  않",
        "을 때를 구별하여  받침을 바로잡아 적어야 한다"
      ],
      "paragraph_index": 1005,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "셋째, 토‘-다, -고, -지’를 붙여보아 그것이  거센소리로 발음하면 ‘ㅎ’받침을 적는다.",
    "output": "셋째, 토‘-다, -고, -지’를 붙여보아 그것이  거센소리로 발음하면 ‘ㅎ’받침을 적는다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "셋째",
        " 토",
        "를 붙여보아 그것이  거센소리로 발음하면 ",
        "받침을 적는다"
      ],
      "paragraph_index": 1006,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "[붙임] 받침‘ ㅎ’,' ㅍ'인 경우에는 토‘-다,-고,-지’를 붙여봐서  거센소리가 나면 ‘ㅎ’을 오른쪽에,  어간의 끝소리를 왼쪽에 바로잡아 적어야 한다.",
    "output": "[붙임] 받침‘ ㅎ’,' ㅍ'인 경우에는 토‘-다,-고,-지’를 붙여봐서  거센소리가 나면 ‘ㅎ’을 오른쪽에,  어간의 끝소리를 왼쪽에 바로잡아 적어야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "붙임",
        " 받침",
        "인 경우에는 토",
        "를 붙여봐서  거센소리가 나면 ",
        "을 오른쪽에"
      ],
      "paragraph_index": 1007,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "는다면 ‘너구리’를 ‘너굴이’로,  ‘개미’를 ‘갬이’로 혼동하여  적을 수 있다.  또한 ‘귀뚜라미’는 “귀뚤귀뚤”한다고하면서  ‘귀뚤’을 어근으로 보고 ‘아미’를 접미사로 보아",
    "output": "는다면 ‘너구리’를 ‘너굴이’로,  ‘개미’를 ‘갬이’로 혼동하여  적을 수 있다.  또한 ‘귀뚜라미’는 “귀뚤귀뚤”한다고하면서  ‘귀뚤’을 어근으로 보고 ‘아미’를 접미사로 보아‘귀뚤아미’로 표기할 수 있는 사람들이  있을 수 있는가 하면 또 어떤 사람들은 “귀뚜람귀뚜람”운다고 ‘귀뚜람’까지어근으로 보고 거기에  접미사 ‘—이’를 붙여  ‘귀뚜람이’라고 적는 사람들이  있을 수 있다.  이처럼  허다한 시끄러움과 혼동을 초래할 필요  없이  소리  나는 내로 적는  것이합리하다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "는다면 ",
        "너구리",
        "를 ",
        "너굴이",
        "  "
      ],
      "paragraph_index": 1682,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "왼쪽의 부사들은 단음절의 명사가 겹쳐서  이루어진 어근으로서  이런 어근에는 ‘하다’가 붙어서 형용사를 이루지못한다.  오른쪽의 부사들은 그 어근에 ‘하다’가 붙어서  형용사로 될",
    "output": "왼쪽의 부사들은 단음절의 명사가 겹쳐서  이루어진 어근으로서  이런 어근에는 ‘하다’가 붙어서 형용사를 이루지못한다.  오른쪽의 부사들은 그 어근에 ‘하다’가 붙어서  형용사로 될 수 있다.  그려므로 어근에  ‘하다’를 붙여보아형용사로 되는 것은 접미사 ‘ㅡ히’를 붙이고 형용사로 되지  않는 것은 접미사 ‘ㅡ이’를 붙이면 된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "왼쪽의 부사들은 단음절의 명사가 겹쳐서  이루어진 어근",
        "으로서  이런 어근에는 ",
        "하다",
        "가 붙어서 형용사를 이루지못한다",
        "  오른쪽의 부사들은 그 어근에 "
      ],
      "paragraph_index": 1747,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "띄여쓰기란 문장을 글로 적을 때 어떤 단위를 띄여쓰고 어떤 단위를 붙여쓰는가 하는 것을 규정한 규칙을 말한다.  이런 띄여쓰기규범은 독서능률을 높이고 문장을 빠르고도 정확히 리해하",
    "output": "띄여쓰기란 문장을 글로 적을 때 어떤 단위를 띄여쓰고 어떤 단위를 붙여쓰는가 하는 것을 규정한 규칙을 말한다.  이런 띄여쓰기규범은 독서능률을 높이고 문장을 빠르고도 정확히 리해하는 데 큰 의의를 가진다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "띄여쓰기란 문장을 글로 적을 때 어떤 단위를 띄여쓰고 ",
        "어떤 단위를 붙여쓰는가 하는 것을 규정한 규칙을 말한다",
        "  이런 띄여쓰기규범은 독서능률을 높이고 문장을 빠르고",
        "도 정확히 리해하는 데 큰 의의를 가진다"
      ],
      "paragraph_index": 1817,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "띄여쓰기규범을 잘 세우면 글의 내용이 한눈에 안겨와글을 쉽게 리해하고 빨리 읽을 수 있게 된다.  반면에 단어들을 쭉 잇달아 붙여쓰거나 지나치게 토막토막 띄여쓰면글을 읽기도 힘들고",
    "output": "띄여쓰기규범을 잘 세우면 글의 내용이 한눈에 안겨와글을 쉽게 리해하고 빨리 읽을 수 있게 된다.  반면에 단어들을 쭉 잇달아 붙여쓰거나 지나치게 토막토막 띄여쓰면글을 읽기도 힘들고 그 뜻을 파악하기도 힘들다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "띄여쓰기규범을 잘 세우면 글의 내용이 한눈에 안겨와글을",
        " 쉽게 리해하고 빨리 읽을 수 있게 된다",
        "  반면에 단어들을 쭉 잇달아 붙여쓰거나 지나치게 토막",
        "토막 띄여쓰면글을 읽기도 힘들고 그 뜻을 파악하기도 힘",
        "들다"
      ],
      "paragraph_index": 1818,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "례하면 띄여쓰기를 하지  않고 ‘학생이백명’이라고 쭉붙여쓴다면 ‘학생이  백명’인지  ‘학생  이백명’인지 그 내용을 잘 알 수 없게 되며 ‘아버지가방으로들어간다.’의 띄여쓰기를 ",
    "output": "례하면 띄여쓰기를 하지  않고 ‘학생이백명’이라고 쭉붙여쓴다면 ‘학생이  백명’인지  ‘학생  이백명’인지 그 내용을 잘 알 수 없게 되며 ‘아버지가방으로들어간다.’의 띄여쓰기를 잘못하면 ‘아버지 가방으로 들어간다’와 같이 잘못리해될 수도 있다.  반면 ‘학생 이 백 명’처럼 너무 토막토막 띄여써도 읽기 힘들고 그 뜻을 파악하기 힘들다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "례하면 띄여쓰기를 하지  않고 ",
        "학생이백명",
        "이라고 쭉붙여쓴다면 ",
        "학생이  백명",
        "인지  "
      ],
      "paragraph_index": 1819,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "따라서 띄여쓰기규범을 잘 세우고 규범 내로 글을 써야 글을 보는 사람들이 내용파악을 쉽게 할 수 있다.",
    "output": "따라서 띄여쓰기규범을 잘 세우고 규범 내로 글을 써야 글을 보는 사람들이 내용파악을 쉽게 할 수 있다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "따라서 띄여쓰기규범을 잘 세우고 규범 내로 글을 써야 ",
        "글을 보는 사람들이 내용파악을 쉽게 할 수 있다"
      ],
      "paragraph_index": 1820,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이와 같이 띄여쓰기는 글의 독서능률을 높이고 그 내용을 리해하는 데서 결정적  역할을 한다고 말할 수 있다.",
    "output": "이와 같이 띄여쓰기는 글의 독서능률을 높이고 그 내용을 리해하는 데서 결정적  역할을 한다고 말할 수 있다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이와 같이 띄여쓰기는 글의 독서능률을 높이고 그 내용을",
        " 리해하는 데서 결정적  역할을 한다고 말할 수 있다"
      ],
      "paragraph_index": 1821,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "그것은 띄여쓰기가 문장을 제대로 읽도록 어음—의미적 단위를 갈라줌으로써 발음상 막힘이  없이  읽는 속도를보장하며 눈으로 볼 때 합리적인 하나의 뜻덩이를 구획해",
    "output": "그것은 띄여쓰기가 문장을 제대로 읽도록 어음—의미적 단위를 갈라줌으로써 발음상 막힘이  없이  읽는 속도를보장하며 눈으로 볼 때 합리적인 하나의 뜻덩이를 구획해",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "그것은 띄여쓰기가 문장을 제대로 읽도록 어음",
        "의미적 단위를 갈라줌으로써 발음상 막힘이  없이  읽는",
        " 속도를보장하며 눈으로 볼 때 합리적인 하나의 뜻덩이를",
        " 구획해"
      ],
      "paragraph_index": 1822,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "더우기 띄여쓰기는 우리글이 소리글자이면서도 음절을단위로 묶어서  표기하는 특성으로 하여  단어의  형태화가되어있지  않고 따라서 단어와 단어 사이의 한계가 명백하지  않은 조건에서",
    "output": "더우기 띄여쓰기는 우리글이 소리글자이면서도 음절을단위로 묶어서  표기하는 특성으로 하여  단어의  형태화가되어있지  않고 따라서 단어와 단어 사이의 한계가 명백하지  않은 조건에서  더욱 중요하게 제기된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "더우기 띄여쓰기는 우리글이 소리글자이면서도 음절을단위로",
        " 묶어서  표기하는 특성으로 하여  단어의  형태화가되",
        "어있지  않고 따라서 단어와 단어 사이의 한계가 명백하",
        "지  않은 조건에서  더욱 중요하게 제기된다"
      ],
      "paragraph_index": 1828,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범집  총칙에는 “첫째, 조선말은 단어를 단위로하여 띄여쓰는 것을 원칙으로 한다.”고 규정하였다.  띄여쓰기를 잘하려면 ‘단어’의  개념과 그 특성에  대하여  알아둘 필요가",
    "output": "새 규범집  총칙에는 “첫째, 조선말은 단어를 단위로하여 띄여쓰는 것을 원칙으로 한다.”고 규정하였다.  띄여쓰기를 잘하려면 ‘단어’의  개념과 그 특성에  대하여  알아둘 필요가 있다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범집  총칙에는 ",
        "첫째",
        " 조선말은 단어를 단위로하여 띄여쓰는 것을 원칙으로 한",
        "고 규정하였다",
        "  띄여쓰기를 잘하려면 "
      ],
      "paragraph_index": 1829,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "접두사와 접미사는 홀로 쓰이지 못하기에 어근의  앞이거나 뒤에 붙여쓴다.",
    "output": "접두사와 접미사는 홀로 쓰이지 못하기에 어근의  앞이거나 뒤에 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "접두사와 접미사는 홀로 쓰이지 못하기에 어근의  앞이거",
        "나 뒤에 붙여쓴다"
      ],
      "paragraph_index": 1856,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 ",
    "output": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 접두사가 덧붙는 ‘접두파생법’과 어근에 접미사가 덧붙는 ‘접미파생법’이  있다.  그 밖에 접두사와 접미사가 각각 어근에 어울려서  이루어지는 ‘량면파생법’도 있고 뒤따르는 떤 어근과 합성어를 이루는 ‘파생합성법’도있다.  파생어에도 띄여쓰기가 제기되지  않는다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "파생어는 어근에  접사가 덧붙어  이루어진 단어이다",
        "파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게 ",
        " 형성된 단어이다",
        "  조선어  접사에는 접두사와 접미사가 있으므로 어근에",
        " 접두사가 덧붙는 "
      ],
      "paragraph_index": 2068,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "합성어를 이루고 있는 여러 단위를 띄여쓰는가 아니면 붙여쓰는가 하는 문제가 제기된다.",
    "output": "합성어를 이루고 있는 여러 단위를 띄여쓰는가 아니면 붙여쓰는가 하는 문제가 제기된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "합성어를 이루고 있는 여러 단위를 띄여쓰는가 아니면 붙",
        "여쓰는가 하는 문제가 제기된다"
      ],
      "paragraph_index": 2084,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "여러 단위들이  결합하여 합성어를 이룰 때 그 단위들은 붙여쓴다.",
    "output": "여러 단위들이  결합하여 합성어를 이룰 때 그 단위들은 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "여러 단위들이  결합하여 합성어를 이룰 때 그 단위들은",
        " 붙여쓴다"
      ],
      "paragraph_index": 2085,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "依存名词的分写规则是什么？",
    "input": "",
    "output": "완전명사란 문장구조 속에서 다른 단어에 의존하지  않",
    "metadata": {
      "category": "spacing",
      "type": "dependent_noun",
      "paragraph_index": 2092,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체",
    "output": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체가 하나의 단어로 되기에 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 ",
        "다른 새로운 단어를 만든다",
        "  이  때 쓰이는 단어조성수법이 바로 어근합성법이다",
        "  어근합성법에 의하여 만들어진단어는 그 전체가 하나의",
        " 단어로 되기에 붙여쓴다"
      ],
      "paragraph_index": 2100,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "(1) 명사가 다른 명사거나 동사, 형용사, 부사와 결합되어 하나의 뜻덩어리로 될 경우 붙여쓴다.",
    "output": "(1) 명사가 다른 명사거나 동사, 형용사, 부사와 결합되어 하나의 뜻덩어리로 될 경우 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 명사가 다른 명사거나 동사",
        " 형용사",
        " 부사와 결합되어 하나의 뜻덩어리로 될 경우 붙여쓴다"
      ],
      "paragraph_index": 2101,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "명사에 토가 붙은 경우에는 뒤의 단어와 띄여쓴다고하였으나 명사가 토를 매개로 다른 명사, 동사, 형용사와결합되는 경우에는 하나의 뜻덩이로 묶어지기에 앞의 단어에 붙여쓴다.  ①에서",
    "output": "명사에 토가 붙은 경우에는 뒤의 단어와 띄여쓴다고하였으나 명사가 토를 매개로 다른 명사, 동사, 형용사와결합되는 경우에는 하나의 뜻덩이로 묶어지기에 앞의 단어에 붙여쓴다.  ①에서의  ‘곰의열, 귀에고리, 쩡의바람꽃,닭의살, 닭의홰’등과 같은 경우이다.  이  경우 토를 셍략하지 못한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "명사에 토가 붙은 경우에는 뒤의 단어와 띄여쓴다고하였으",
        "나 명사가 토를 매개로 다른 명사",
        " 동사",
        " 형용사와결합되는 경우에는 하나의 뜻덩이로 묶어지기에 ",
        "앞의 단어에 붙여쓴다"
      ],
      "paragraph_index": 2116,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이 부류의 단어들은 2007년의 규범에서는 붙여쓴다고규정하였으나 새 규범의 종칙 “조선말은 단어를 단위로 하",
    "output": "이 부류의 단어들은 2007년의 규범에서는 붙여쓴다고규정하였으나 새 규범의 종칙 “조선말은 단어를 단위로 하",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이 부류의 단어들은 ",
        "년의 규범에서는 붙여쓴다고규정하였으나 새 규범의 종칙 ",
        "조선말은 단어를 단위로 하"
      ],
      "paragraph_index": 2118,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "依存名词的分写规则是什么？",
    "input": "",
    "output": "불완전명사란 문장구조 속에서  다른 단어에 의존하지않고서는 홀로 자립적으로 쓰일 수 없는 명사를 가리킨다.불완전명사는 다른 어떤 표식의 보충을 받지  않고서는 어면 대상에 대하여  이름을 지어준다고 보기  어려울 정도로대상적 의미가 불완전하나 명사의 하위분류로서 하나의 단어로 인식되기에 앞의 단어와 띄여써야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "dependent_noun",
      "paragraph_index": 2126,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범에서는 고유어불완전명사는 앞의 단어와 띄여쓰고 한자어불완전명사는 앞의 단어에 붙여쓴다고 규정하였다.  한자는 매개 글자가 뜻글자이기에 앞의 단어와 띄여",
    "output": "새 규범에서는 고유어불완전명사는 앞의 단어와 띄여쓰고 한자어불완전명사는 앞의 단어에 붙여쓴다고 규정하였다.  한자는 매개 글자가 뜻글자이기에 앞의 단어와 띄여",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범에서는 고유어불완전명사는 앞의 단어와 띄여쓰고 ",
        "한자어불완전명사는 앞의 단어에 붙여쓴다고 규정하였다",
        "  한자는 매개 글자가 뜻글자이기에 앞의 단어와 띄여"
      ],
      "paragraph_index": 2127,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "쓰면 그것이 완전명사인지  아니면 불완전명사인지를 가늠하기 힘들다.  그러므로 그것이 불완전명사라는 것을 뚜렷이 하기 위하여  한자어불완전명사는 앞의 단어와 붙여쓴다.",
    "output": "쓰면 그것이 완전명사인지  아니면 불완전명사인지를 가늠하기 힘들다.  그러므로 그것이 불완전명사라는 것을 뚜렷이 하기 위하여  한자어불완전명사는 앞의 단어와 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "쓰면 그것이 완전명사인지  아니면 불완전명사인지를 가늠",
        "하기 힘들다",
        "  그러므로 그것이 불완전명사라는 것을 뚜렷이 하기 위",
        "하여  한자어불완전명사는 앞의 단어와 붙여쓴다"
      ],
      "paragraph_index": 2132,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "①  그러나 ‘남자뿐이다, 셋뿐이다, 한번뿐이다, 두장뿐이다’처럼 체언의 뒤에 붙어서 한정의 뜻을 나타내는 경우는 접미사로 다루어 붙여쓴다.",
    "output": "①  그러나 ‘남자뿐이다, 셋뿐이다, 한번뿐이다, 두장뿐이다’처럼 체언의 뒤에 붙어서 한정의 뜻을 나타내는 경우는 접미사로 다루어 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "  그러나 ",
        "남자뿐이다",
        " 셋뿐이다",
        " 한번뿐이다",
        " 두장뿐이다"
      ],
      "paragraph_index": 2215,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "단위명사를 앞의 단어에 붙여쓰게 되는 데는 다음과같은 경우가 있기 때문이다.",
    "output": "단위명사를 앞의 단어에 붙여쓰게 되는 데는 다음과같은 경우가 있기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "단위명사를 앞의 단어에 붙여쓰게 되는 데는 다음과같은 ",
        "경우가 있기 때문이다"
      ],
      "paragraph_index": 2254,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "전문용어는 붙여쓴다. 그것은 전문용어를 이룬 단어들이 어울리여 하나의 내상을 나타내기 때문이다. 전문용어의 띄여쓰기는 다음과 같이 한다.",
    "output": "전문용어는 붙여쓴다. 그것은 전문용어를 이룬 단어들이 어울리여 하나의 내상을 나타내기 때문이다. 전문용어의 띄여쓰기는 다음과 같이 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "전문용어는 붙여쓴다",
        " 그것은 전문용어를 이룬 단어들이 어울리여 하나의 내상",
        "을 나타내기 때문이다",
        " 전문용어의 띄여쓰기는 다음과 같이 한다"
      ],
      "paragraph_index": 2419,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "① 용언에 규정토 ‘ㄴ,  ㄹ’이 끼여  이루어진 형래도다 붙여쓴다.",
    "output": "① 용언에 규정토 ‘ㄴ,  ㄹ’이 끼여  이루어진 형래도다 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 용언에 규정토 ",
        "  ",
        "이 끼여  이루어진 형래도다 붙여쓴다"
      ],
      "paragraph_index": 2421,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "③ 부사, 관형사가 명사나 용언의 체언형에 붙어  이루어진 형태도 다 붙여쓴다.",
    "output": "③ 부사, 관형사가 명사나 용언의 체언형에 붙어  이루어진 형태도 다 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 부사",
        " 관형사가 명사나 용언의 체언형에 붙어  이루어진 형태",
        "도 다 붙여쓴다"
      ],
      "paragraph_index": 2428,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "④ 보통명사에 속격토 ‘의’가 붙어  이루어진 형태도붙여쓴다.",
    "output": "④ 보통명사에 속격토 ‘의’가 붙어  이루어진 형태도붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 보통명사에 속격토 ",
        "가 붙어  이루어진 형태도붙여쓴다"
      ],
      "paragraph_index": 2429,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "⑤ 기타 특수하게  이루어진 형태도 다 붙여쓴다.",
    "output": "⑤ 기타 특수하게  이루어진 형태도 다 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 기타 특수하게  이루어진 형태도 다 붙여쓴다"
      ],
      "paragraph_index": 2430,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "② 여러 말마디로 된 긴 학술용어는 토가 없이  결합된단위가 너무 길 때 뜻을 단위로 띄여쓸 수 있다는 규정에따라 뜻의  리해에 맞게 띄여쓰기를 할 수 있다.",
    "output": "② 여러 말마디로 된 긴 학술용어는 토가 없이  결합된단위가 너무 길 때 뜻을 단위로 띄여쓸 수 있다는 규정에따라 뜻의  리해에 맞게 띄여쓰기를 할 수 있다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 여러 말마디로 된 긴 학술용어는 토가 없이  결합된단",
        "위가 너무 길 때 뜻을 단위로 띄여쓸 수 있다는 규정에",
        "따라 뜻의  리해에 맞게 띄여쓰기를 할 수 있다"
      ],
      "paragraph_index": 2439,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "조선민족의  성과 이름,  성과 호는 정식  이름이므로“고유한 대상의  이름은 붙여쓴다.”는 제6항의 규정꽈 “한국꽈 조선이 합의를 본 것은 그대로 쓴다.”는 종칙에 따라붙여써야 ",
    "output": "조선민족의  성과 이름,  성과 호는 정식  이름이므로“고유한 대상의  이름은 붙여쓴다.”는 제6항의 규정꽈 “한국꽈 조선이 합의를 본 것은 그대로 쓴다.”는 종칙에 따라붙여써야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "조선민족의  성과 이름",
        "  성과 호는 정식  이름이므로",
        "고유한 대상의  이름은 붙여쓴다",
        "는 제",
        "항의 규정꽈 "
      ],
      "paragraph_index": 2444,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "호칭어와 관련한 띄여쓰기는 사람의 사회적 관계를 나타내는 말의 띄여쓰기이다.",
    "output": "호칭어와 관련한 띄여쓰기는 사람의 사회적 관계를 나타내는 말의 띄여쓰기이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "호칭어와 관련한 띄여쓰기는 사람의 사회적 관계를 나타내",
        "는 말의 띄여쓰기이다"
      ],
      "paragraph_index": 2450,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "호칭어는 주로 입말에서 쓰이기에  이름에 붙든 직위에붙든 앞의 단어와 붙여쓰고 뒤의 단어와는 띄여쓴다.  호칭어  다음에는 반점을 찍는다.",
    "output": "호칭어는 주로 입말에서 쓰이기에  이름에 붙든 직위에붙든 앞의 단어와 붙여쓰고 뒤의 단어와는 띄여쓴다.  호칭어  다음에는 반점을 찍는다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "호칭어는 주로 입말에서 쓰이기에  이름에 붙든 직위에붙",
        "든 앞의 단어와 붙여쓰고 뒤의 단어와는 띄여쓴다",
        "  호칭어  다음에는 반점을 찍는다"
      ],
      "paragraph_index": 2460,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "그려나 성씨  바로 뒤에 울 때에는 붙여쓴다.  성씨 뒤에 울 경우 떠여쓰면  읽을 때 불편을 가져울 수  있기  때문이다.",
    "output": "그려나 성씨  바로 뒤에 울 때에는 붙여쓴다.  성씨 뒤에 울 경우 떠여쓰면  읽을 때 불편을 가져울 수  있기  때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "그려나 성씨  바로 뒤에 울 때에는 붙여쓴다",
        "  성씨 뒤에 울 경우 떠여쓰면  읽을 때 불편을 가져",
        "울 수  있기  때문이다"
      ],
      "paragraph_index": 2463,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이므로 붙여쓴다.  ‘리부 부장’으로 떠여쓰면 두 글자로 된이름 뒤에 관직명이 온 경우이므로 ‘리부부장’과 다른 의미가 된다.  ‘장총국장’도 마찬가지로 성씨  뒤에  관직명이온 ",
    "output": "이므로 붙여쓴다.  ‘리부 부장’으로 떠여쓰면 두 글자로 된이름 뒤에 관직명이 온 경우이므로 ‘리부부장’과 다른 의미가 된다.  ‘장총국장’도 마찬가지로 성씨  뒤에  관직명이온 경우로서  ‘장총 국장’과 의미가 다르다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이므로 붙여쓴다",
        "  ",
        "리부 부장",
        "으로 떠여쓰면 두 글자로 된이름 뒤에 관직명이 온 경우",
        "이므로 "
      ],
      "paragraph_index": 2469,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "지명의 단위를 나타내는 단어는 “한국과 조선이  합의를 본 것은 그대로 쓴다.”는 총칙에  따라 앞말에 붙여쓴다.",
    "output": "지명의 단위를 나타내는 단어는 “한국과 조선이  합의를 본 것은 그대로 쓴다.”는 총칙에  따라 앞말에 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "지명의 단위를 나타내는 단어는 ",
        "한국과 조선이  합의를 본 것은 그대로 쓴다",
        "는 총칙에  따라 앞말에 붙여쓴다"
      ],
      "paragraph_index": 2471,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "9) 고유한 대상의 이름과 관련한 띄여쓰기",
    "output": "9) 고유한 대상의 이름과 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 고유한 대상의 이름과 관련한 띄여쓰기"
      ],
      "paragraph_index": 2472,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "고유한 대상의  이름은 원칙적으로 붙여쓴다.",
    "output": "고유한 대상의  이름은 원칙적으로 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "고유한 대상의  이름은 원칙적으로 붙여쓴다"
      ],
      "paragraph_index": 2473,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "고유한 대상의  이름과 관련한 띄여쓰기에는 고유하다고 볼 수 있는 대상의 명칭 례하면 내중운동, 사변, 전쟁,회의, 기념일, 강령, 선언 등과 같이  특별히  지어 부르는일정한 대",
    "output": "고유한 대상의  이름과 관련한 띄여쓰기에는 고유하다고 볼 수 있는 대상의 명칭 례하면 내중운동, 사변, 전쟁,회의, 기념일, 강령, 선언 등과 같이  특별히  지어 부르는일정한 대상들의  이름도 포함된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "고유한 대상의  이름과 관련한 띄여쓰기에는 고유하다고 ",
        "볼 수 있는 대상의 명칭 례하면 내중운동",
        " 사변",
        " 전쟁",
        "회의"
      ],
      "paragraph_index": 2483,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "10) 당조직, 국가기구, 인민단체, 행정구역 등의 명칭과 관련한 띄여쓰기",
    "output": "10) 당조직, 국가기구, 인민단체, 행정구역 등의 명칭과 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 당조직",
        " 국가기구",
        " 인민단체",
        " 행정구역 등의 명칭과 관련한 띄여쓰기"
      ],
      "paragraph_index": 2484,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "11) 국가나 정당, 사회단체 등의 정식 이름 뒤에 오는 보통명사와 관련한 띄여쓰기",
    "output": "11) 국가나 정당, 사회단체 등의 정식 이름 뒤에 오는 보통명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 국가나 정당",
        " 사회단체 등의 정식 이름 뒤에 오는 보통명사와 관련한",
        " 띄여쓰기"
      ],
      "paragraph_index": 2486,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "12) 기관이나 부서의 이름, 직무 이름과 관련한 띄여쓰기",
    "output": "12) 기관이나 부서의 이름, 직무 이름과 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 기관이나 부서의 이름",
        " 직무 이름과 관련한 띄여쓰기"
      ],
      "paragraph_index": 2493,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "기관이나 부서의  이름과 직무 이름(또는 직업, 신분,칭호), 사람 이름 사이는 각각 떠여쓴다.  그러나 정식으로되는 기관이나 부서의  이름과 직무가 완전히 줄어든 경우에는 띄여쓰",
    "output": "기관이나 부서의  이름과 직무 이름(또는 직업, 신분,칭호), 사람 이름 사이는 각각 떠여쓴다.  그러나 정식으로되는 기관이나 부서의  이름과 직무가 완전히 줄어든 경우에는 띄여쓰기를 다음과 같이 처리한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "기관이나 부서의  이름과 직무 이름",
        "또는 직업",
        " 신분",
        "칭호",
        " 사람 이름 사이는 각각 떠여쓴다"
      ],
      "paragraph_index": 2494,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "13) 회의명칭(전람회, 운동회 명칭도 포함)과 관련한 띄여쓰기",
    "output": "13) 회의명칭(전람회, 운동회 명칭도 포함)과 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 회의명칭",
        "전람회",
        " 운동회 명칭도 포함",
        "과 관련한 띄여쓰기"
      ],
      "paragraph_index": 2508,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "동격어란 어떤 대상에 대하여 같은 자격을 가진 말을덧붙여 보래여주어 그것을 두드려지게  강조하는 규정어의일종이다.  따라서 동격어는 뒤의 말과 띄여써야 한다.",
    "output": "동격어란 어떤 대상에 대하여 같은 자격을 가진 말을덧붙여 보래여주어 그것을 두드려지게  강조하는 규정어의일종이다.  따라서 동격어는 뒤의 말과 띄여써야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "동격어란 어떤 대상에 대하여 같은 자격을 가진 말을덧붙",
        "여 보래여주어 그것을 두드려지게  강조하는 규정어의일종",
        "이다",
        "  따라서 동격어는 뒤의 말과 띄여써야 한다"
      ],
      "paragraph_index": 2520,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "15) 장소를 나타내는 고유명사와 관련한 띄여쓰기",
    "output": "15) 장소를 나타내는 고유명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 장소를 나타내는 고유명사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 2527,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "장소를 나타내는 고유명사는 뒤에 오는 명칭과 띄여쓴다.  붙여쓰면 그 전체가 또 하나의 고유한 대상의  이름으로 될 수 있기 때문이다.",
    "output": "장소를 나타내는 고유명사는 뒤에 오는 명칭과 띄여쓴다.  붙여쓰면 그 전체가 또 하나의 고유한 대상의  이름으로 될 수 있기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "장소를 나타내는 고유명사는 뒤에 오는 명칭과 띄여쓴다",
        "  붙여쓰면 그 전체가 또 하나의 고유한 대상의  이름",
        "으로 될 수 있기 때문이다"
      ],
      "paragraph_index": 2528,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "‘할빈지 흑룡강일보사’는 ‘할빈시에  있는 흑룡강일보사’라는 뜻을 나타내는데 붙여쓰면  ‘할빈지흑룡강일보사’즉 또 다른 하나의  고유한 대상의  이름으로 될 수  있어오해를 일으킬",
    "output": "‘할빈지 흑룡강일보사’는 ‘할빈시에  있는 흑룡강일보사’라는 뜻을 나타내는데 붙여쓰면  ‘할빈지흑룡강일보사’즉 또 다른 하나의  고유한 대상의  이름으로 될 수  있어오해를 일으킬 수 있다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "할빈지 흑룡강일보사",
        "는 ",
        "할빈시에  있는 흑룡강일보사",
        "라는 뜻을 나타내는데 붙여쓰면  ",
        "할빈지흑룡강일보사"
      ],
      "paragraph_index": 2529,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "16) 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기",
    "output": "16) 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 앞의 명사를 다시 받는 명사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 2530,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이  경우 폐하면 ‘답사자 일행’에서  ‘일행’은 ‘답사자’를 다시 가리키는데 만약 ‘답사자일행’처럼 붙여쓴다면 하나의 뜻덩이를 나타내는 것으로 인식된다.  즉 ‘일행’은 앞의  ",
    "output": "이  경우 폐하면 ‘답사자 일행’에서  ‘일행’은 ‘답사자’를 다시 가리키는데 만약 ‘답사자일행’처럼 붙여쓴다면 하나의 뜻덩이를 나타내는 것으로 인식된다.  즉 ‘일행’은 앞의  명사를 다시 가리키는 역할을 놓 수 없게 된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이  경우 폐하면 ",
        "답사자 일행",
        "에서  ",
        "일행",
        "은 "
      ],
      "paragraph_index": 2540,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "17) 사람의 이름 뒤에 오는 ‘작곡. 작사. 안무. 각색. 목각.시…’등 명사와 관련한 띄여쓰기",
    "output": "17) 사람의 이름 뒤에 오는 ‘작곡. 작사. 안무. 각색. 목각.시…’등 명사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 사람의 이름 뒤에 오는 ",
        "작곡",
        " 작사",
        " 안무",
        " 각색"
      ],
      "paragraph_index": 2541,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "18)붙여쓰면 다른 뜻이 생길 경우와 관련한 띄여쓰기",
    "output": "18)붙여쓰면 다른 뜻이 생길 경우와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "붙여쓰면 다른 뜻이 생길 경우와 관련한 띄여쓰기"
      ],
      "paragraph_index": 2549,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "“한국과 조선이 합의를 본 것은 그대로 쓴다.”는 총칙에 따라 명사결합체에서 붙여쓰면 다른 뜻이 생길 경우 의미단위별로 뜻이 통하게 떠여쓴다.",
    "output": "“한국과 조선이 합의를 본 것은 그대로 쓴다.”는 총칙에 따라 명사결합체에서 붙여쓰면 다른 뜻이 생길 경우 의미단위별로 뜻이 통하게 떠여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "한국과 조선이 합의를 본 것은 그대로 쓴다",
        "는 총칙에 따라 명사결합체에서 붙여쓰면 다른 뜻이 생길",
        " 경우 의미단위별로 뜻이 통하게 떠여쓴다"
      ],
      "paragraph_index": 2550,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "제2장  수사와 관련한  띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2553,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "수사란 대상의 일정한 수량이나 순서를 나타내는 품사를 말한다.  수사는 십진법에 따라 떠여쓰면 리상적이라고생각되지만 그렇게 되면 너무 토막토막 작게 갈라놓아 의미 파악에 지장이 될 수 있기 때문에 십진법을 따르지  않고 있다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2554,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "2007년의 규범에서는 띄여쓰기 제7항과 제8항에서 수",
    "output": "2007년의 규범에서는 띄여쓰기 제7항과 제8항에서 수",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "년의 규범에서는 띄여쓰기 제",
        "항과 제",
        "항에서 수"
      ],
      "paragraph_index": 2555,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "사의 띄여쓰기에 대하여 다음과 같이 규정하였다.",
    "output": "사의 띄여쓰기에 대하여 다음과 같이 규정하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "사의 띄여쓰기에 대하여 다음과 같이 규정하였다"
      ],
      "paragraph_index": 2560,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "제7항 수사는 아라비아수자로 적는 것을 원칙으로 하되 조선문자로 단위를 달아줄 경우거나 순 조선문자로 적을 경우에는 ‘만,  억, 조’등의 단위에서 띄여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2561,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "제8항 수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.",
    "output": "제8항 수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "항 수사가 완전명사와 어울리는 경우에는 띄여쓴다",
        "  ",
        " 그러나 단위명사와 어울리는 경우에는 붙여쓴다"
      ],
      "paragraph_index": 2562,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "제8항 수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2562,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범 제23항에서는 수사의 띄여쓰기를 다음과 같이규정하였다.",
    "output": "새 규범 제23항에서는 수사의 띄여쓰기를 다음과 같이규정하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범 제",
        "항에서는 수사의 띄여쓰기를 다음과 같이규정하였다"
      ],
      "paragraph_index": 2563,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "새 규범 제23항에서는 수사의 띄여쓰기를 다음과 같이규정하였다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2563,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "제23항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.  조선문자로 단위를 달",
    "output": "제23항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.  조선문자로 단위를 달아줄 경우거나 순 조선문자로 적을 경우에는 ‘만,  억, 조’등의 단위에서 띄여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수",
        "인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 ",
        "소수인 경우 오른쪽으로 가면서 다 붙여쓴다",
        "  조선문자로 단위를 달아줄 경우거나 순 조선문자로 적",
        "을 경우에는 "
      ],
      "paragraph_index": 2564,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "제23항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.  조선문자로 단위를 달아줄 경우거나 순 조선문자로 적을 경우에는 ‘만,  억, 조’등의 단위에서 띄여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2564,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범에서는 “정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다붙여쓴다.”를 더 보태고 2007년의 규범에서의 “수사가 완전명사와 어울리",
    "output": "새 규범에서는 “정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다붙여쓴다.”를 더 보태고 2007년의 규범에서의 “수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.”는 내용을 삭제하였다.완전명사는 하나의 자립적인 단어이므로 “조선말은 단어를단위로 하여 띄여쓰는 것을 원칙으로 한다.”는 총칙에 따",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범에서는 ",
        "정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주",
        "고 소수인 경우 오른쪽으로 가면서 다붙여쓴다",
        "를 더 보태고 ",
        "년의 규범에서의 "
      ],
      "paragraph_index": 2565,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "새 규범에서는 “정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다붙여쓴다.”를 더 보태고 2007년의 규범에서의 “수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.”는 내용을 삭제하였다.완전명사는 하나의 자립적인 단어이므로 “조선말은 단어를단위로 하여 띄여쓰는 것을 원칙으로 한다.”는 총칙에 따",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2565,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "라 당연히 띄여쓰게 되여있기 때문이다.  그리고 새 규범의제22항 “단위명사는 앞의 단어와 붙여쓴다.”는 규칙에  따라 붙여쓰게 되여있기 때문에 더 설명할 필요가 없게 되였다.  ",
    "output": "라 당연히 띄여쓰게 되여있기 때문이다.  그리고 새 규범의제22항 “단위명사는 앞의 단어와 붙여쓴다.”는 규칙에  따라 붙여쓰게 되여있기 때문에 더 설명할 필요가 없게 되였다.  따라서 삭제하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "라 당연히 띄여쓰게 되여있기 때문이다",
        "  그리고 새 규범의제",
        "항 ",
        "단위명사는 앞의 단어와 붙여쓴다",
        "는 규칙에  따라 붙여쓰게 되여있기 때문에 더 설명할 "
      ],
      "paragraph_index": 2570,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "1) 아라비아수자로 적을 때의 띄여쓰기",
    "output": "1) 아라비아수자로 적을 때의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 아라비아수자로 적을 때의 띄여쓰기"
      ],
      "paragraph_index": 2571,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.",
    "output": "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면",
        "서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로",
        " 가면서 다 붙여쓴다"
      ],
      "paragraph_index": 2572,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2572,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "2) 순 조선문자로 적을 때의 띄여쓰기",
    "output": "2) 순 조선문자로 적을 때의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 순 조선문자로 적을 때의 띄여쓰기"
      ],
      "paragraph_index": 2573,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "3) 조선문자와 아라비아수자를 섞어적는 경우의 띄여쓰기",
    "output": "3) 조선문자와 아라비아수자를 섞어적는 경우의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 조선문자와 아라비아수자를 섞어적는 경우의 띄여쓰기"
      ],
      "paragraph_index": 2577,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "4) 수사가 인체기관 이름과 결합될 때의 띄여쓰기",
    "output": "4) 수사가 인체기관 이름과 결합될 때의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 수사가 인체기관 이름과 결합될 때의 띄여쓰기"
      ],
      "paragraph_index": 2582,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "4) 수사가 인체기관 이름과 결합될 때의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2582,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "수사가 ‘손, 발, 귀, 눈, 입, 어깨, 몸…’등 인체기관 이름과 결합될 경우에도 떠여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2583,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "단 사전에 오른‘한손, 한발, 한눈, 한입, 두어깨, 한몸, 한가슴, 한다리…’는 붙여쓴다.",
    "output": "단 사전에 오른‘한손, 한발, 한눈, 한입, 두어깨, 한몸, 한가슴, 한다리…’는 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "단 사전에 오른",
        "한손",
        " 한발",
        " 한눈",
        " 한입"
      ],
      "paragraph_index": 2584,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범집에서는 내명사는 아래 단어와 띄여쓰는데 다만 ‘이것’, ‘그것’, ‘저것’만은 붙여쓴다고 규정하였다.",
    "output": "새 규범집에서는 내명사는 아래 단어와 띄여쓰는데 다만 ‘이것’, ‘그것’, ‘저것’만은 붙여쓴다고 규정하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범집에서는 내명사는 아래 단어와 띄여쓰는데 다만 ",
        "이것",
        "그것",
        "저것",
        "만은 붙여쓴다고 규정하였다"
      ],
      "paragraph_index": 2589,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "인칭대명사에서  ‘우리’의  띄여쓰기는 “한국과 조선이합의를 본 것은 그대로 쓴다.”는 총칙에 따라 다음과 같이띄여쓰기를 한다.",
    "output": "인칭대명사에서  ‘우리’의  띄여쓰기는 “한국과 조선이합의를 본 것은 그대로 쓴다.”는 총칙에 따라 다음과 같이띄여쓰기를 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "인칭대명사에서  ",
        "우리",
        "의  띄여쓰기는 ",
        "한국과 조선이합의를 본 것은 그대로 쓴다",
        "는 총칙에 따라 다음과 같이띄여쓰기를 한다"
      ],
      "paragraph_index": 2599,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "‘우리말’,  ‘우리글’은 합성어로 보아 붙여쓰고 ‘우리나라’는 구로 보아 띄여쓴다.",
    "output": "‘우리말’,  ‘우리글’은 합성어로 보아 붙여쓰고 ‘우리나라’는 구로 보아 띄여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "우리말",
        "  ",
        "우리글",
        "은 합성어로 보아 붙여쓰고 ",
        "우리나라"
      ],
      "paragraph_index": 2600,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "지시내명사에는 ‘이, 그, 저’와 ‘여기, 거기, 저기’가있다.  규칙에 따르면 ‘이, 그, 저’와 ‘여기,  거기, 저기’는 아래  오는 단어와 띄여써야 한다.  다만 ‘이것’,",
    "output": "지시내명사에는 ‘이, 그, 저’와 ‘여기, 거기, 저기’가있다.  규칙에 따르면 ‘이, 그, 저’와 ‘여기,  거기, 저기’는 아래  오는 단어와 띄여써야 한다.  다만 ‘이것’,  ‘그것’,  ‘저것’만은 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "지시내명사에는 ",
        " 그",
        " 저",
        "와 ",
        "여기"
      ],
      "paragraph_index": 2602,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이 가운데서 의문대명사 ‘몇’은 그 아래 오는 단위명사와 붙여써야 하고 그것이 ‘몇몇’의 형태로 쓰일 경우 아래 단어와 띄여쓴다.",
    "output": "이 가운데서 의문대명사 ‘몇’은 그 아래 오는 단위명사와 붙여써야 하고 그것이 ‘몇몇’의 형태로 쓰일 경우 아래 단어와 띄여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이 가운데서 의문대명사 ",
        "은 그 아래 오는 단위명사와 붙여써야 하고 그것이 ",
        "몇몇",
        "의 형태로 쓰일 경우 아래 단어와 띄여쓴다"
      ],
      "paragraph_index": 2610,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "제4장 동사,  형용사와 관련한 띄여쓰기",
    "output": "제4장 동사,  형용사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "장 동사",
        "  형용사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 2612,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "(2) 보조적  형용사와 관련한 띄여쓰기",
    "output": "(2) 보조적  형용사와 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 보조적  형용사와 관련한 띄여쓰기"
      ],
      "paragraph_index": 2635,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "(3) 토 ‘—아, —어, —어’ 바로 다음에 오는 보조용언과 관련한 띄여쓰기",
    "output": "(3) 토 ‘—아, —어, —어’ 바로 다음에 오는 보조용언과 관련한 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 토 ",
        " 바로 다음에 오는 보조용언과 관련한 띄여쓰기"
      ],
      "paragraph_index": 2641,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범에서는 토‘ㅡ아, ㅡ어, ㅡ여’ 바로 다음에 오는 보조용언은 앞말에 붙여쓴다고 규정하였다.  2007년의규범에서는 토‘ㅡ아, ㅡ어, ㅡ여, ㅡ아다, ㅡ어다, ㅡ여다’가 붙은",
    "output": "새 규범에서는 토‘ㅡ아, ㅡ어, ㅡ여’ 바로 다음에 오는 보조용언은 앞말에 붙여쓴다고 규정하였다.  2007년의규범에서는 토‘ㅡ아, ㅡ어, ㅡ여, ㅡ아다, ㅡ어다, ㅡ여다’가 붙은 동사나 형용사가 다른 동사나 형용사와 어울려하나의 동작, 상태를 나타내는 것은 붙여쓴다고 규정하였다.  새 규범에서는 ‘ㅡ아다, ㅡ어다, ㅡ여다’가 붙은 동사의 경우를 제외하였다.  왜냐하면 ‘ㅡ아다,  ㅡ어다,  ㅡ여다’는 방식의 뜻을 갖고 있기에  이것들이 붙은 동사는 뒤의 행동이  이루어지는 방식을 나타내므로 하나의 뜻덩이로인식되지  않기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범에서는 토",
        " 바로 다음에 오는 보조용언은 앞말에 붙여쓴다고 규정하",
        "였다",
        "  ",
        "년의규범에서는 토"
      ],
      "paragraph_index": 2646,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "동사, 형용사의 규정형 뒤에 오는 ‘듯, 만,  번,  법,사, 척, 체…’등과 같은 불완전명사는 앞 단어와는 떠여쓰고‘하다’와는 붙여쓴다.",
    "output": "동사, 형용사의 규정형 뒤에 오는 ‘듯, 만,  번,  법,사, 척, 체…’등과 같은 불완전명사는 앞 단어와는 떠여쓰고‘하다’와는 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "동사",
        " 형용사의 규정형 뒤에 오는 ",
        " 만",
        "  번",
        "  법"
      ],
      "paragraph_index": 2648,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "2) 서로 다른 품사들이 결합되여 새로운 동사를 이룰 경우의띄여쓰기",
    "output": "2) 서로 다른 품사들이 결합되여 새로운 동사를 이룰 경우의띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 서로 다른 품사들이 결합되여 새로운 동사를 이룰 경우",
        "의띄여쓰기"
      ],
      "paragraph_index": 2657,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법",
    "output": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법이다.  따라서  띄여쓰기를 어떻게  해야 하는가 하는 문제가 제기된다.  왜냐하면 총칙에 “조선말은단어를 단위로 하여 띄여쓰는 것을 원칙으로 한다.”고 했기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "서로 다른 품사들이  결합되여  새로운 동사를 조성할수",
        " 있다",
        "  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또",
        "는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는",
        " 어근합성법이다"
      ],
      "paragraph_index": 2658,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "output": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "붙여쓴다",
        "  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 ",
        "단어로 되기 때문이다"
      ],
      "paragraph_index": 2664,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "3) 서로 다른 품사들이 결합되여 새로운 형용사를 이룰 경우의띄여쓰기",
    "output": "3) 서로 다른 품사들이 결합되여 새로운 형용사를 이룰 경우의띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 서로 다른 품사들이 결합되여 새로운 형용사를 이룰 경",
        "우의띄여쓰기"
      ],
      "paragraph_index": 2671,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 ",
    "output": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 품사들이 직접 어울려서 하나의 형용사로 된것은 붙여쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되",
        "여 새로운 형용사를 조성할 수 있다",
        "  어근합성법에 의하여 만들어진 단어도 하나의 단어로 ",
        "되므로 붙여써야 한다",
        "즉 서로 다른 품사들이 직접 어울려서 하나의 형용사로 "
      ],
      "paragraph_index": 2672,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "2007년 규범에서는“관형사는 아래의 단어와 띄여쓰는것을 원칙으로 한다.”고 하였으나 새 규범에서는 “관형사가 접두사적으로 쓰일 때는 아래의 단어와 붙여쓴다.”고규정하였다.  새 ",
    "output": "2007년 규범에서는“관형사는 아래의 단어와 띄여쓰는것을 원칙으로 한다.”고 하였으나 새 규범에서는 “관형사가 접두사적으로 쓰일 때는 아래의 단어와 붙여쓴다.”고규정하였다.  새 규범에서 “관형사는 아래의 단어와 띄여쓰는 것을 원칙으로 한다.”고 굳이 규정을 하지  않은 것은관형사 그 자체가 하나의 단어이기에 자연히 아래의 단어와 띄여쓰도록 되여있기 때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "년 규범에서는",
        "관형사는 아래의 단어와 띄여쓰는것을 원칙으로 한다",
        "고 하였으나 새 규범에서는 ",
        "관형사가 접두사적으로 쓰일 때는 아래의 단어와 붙여쓴다",
        "고규정하였다"
      ],
      "paragraph_index": 2691,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "5) 합성명사 앞에 쓰이는 관형사는 일반적으로 뒤의단위와 띄어쓴다.",
    "output": "5) 합성명사 앞에 쓰이는 관형사는 일반적으로 뒤의단위와 띄어쓴다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 합성명사 앞에 쓰이는 관형사는 일반적으로 뒤의단위와 ",
        "띄어쓴다"
      ],
      "paragraph_index": 2722,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "흔히 쓰이는 조선말 관형사에는 다음과 같은 것들이있다.  이런 관형사들은 아래의 단어와 띄어써야 한다.",
    "output": "흔히 쓰이는 조선말 관형사에는 다음과 같은 것들이있다.  이런 관형사들은 아래의 단어와 띄어써야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "흔히 쓰이는 조선말 관형사에는 다음과 같은 것들이있다",
        "  이런 관형사들은 아래의 단어와 띄어써야 한다"
      ],
      "paragraph_index": 2733,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "단(單): (수사나 또는 수와 관련되는 일부 명사의  앞에 쓰이여)  ‘오직’ 또는 ‘다만’의 뜻을 나타낸다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2758,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "약(約): (수사나 수와 관련되는 일부 명사 앞에 쓰이여) ‘대략’, ‘대개’, ‘대강’의 뜻을 나타낸다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2793,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "数字和数词的分写规则是什么？",
    "input": "",
    "output": "연(延): (수사와 길이, 너비, 시간 등과 관련된 단위명사와의  결합 앞에 쓰이여)  ‘모두 합친’의  뜻을 나타낸다.",
    "metadata": {
      "category": "spacing",
      "type": "number",
      "paragraph_index": 2801,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "2007년 규범에서는 띄여쓰기 제16항으로 “부사는 아래단어와 띄어쓴다.”고 규정하였다.  그러나 새 규범에서는이 부분을 단독 항으로 규정하지  않았다.  그것은 종칙에이미 “조선",
    "output": "2007년 규범에서는 띄여쓰기 제16항으로 “부사는 아래단어와 띄어쓴다.”고 규정하였다.  그러나 새 규범에서는이 부분을 단독 항으로 규정하지  않았다.  그것은 종칙에이미 “조선말은 단어를 단위로 하여 띄여쓰는 것을 원칙으로 한다.”고 명확히 규정했는데 부사도 하나의 단어이기때문이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "년 규범에서는 띄여쓰기 제",
        "항으로 ",
        "부사는 아래단어와 띄어쓴다",
        "고 규정하였다",
        "  그러나 새 규범에서는이 부분을 단독 항으로 규정하지"
      ],
      "paragraph_index": 2884,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "output": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들",
        "이  적지  않다",
        "  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제",
        "가 제기된다"
      ],
      "paragraph_index": 2887,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이상의 단어조성수법에 의하여 만들어진 부사는 그 전체가 하나의 단어로 되기에 붙여쓰게 된다.",
    "output": "이상의 단어조성수법에 의하여 만들어진 부사는 그 전체가 하나의 단어로 되기에 붙여쓰게 된다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이상의 단어조성수법에 의하여 만들어진 부사는 그 전체가",
        " 하나의 단어로 되기에 붙여쓰게 된다"
      ],
      "paragraph_index": 2901,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "새 규범에서는 2007년의 규범과는 달리 제33항 문장의첫머리와 단락을 바꿀 때의 띄여쓰기, 제34항 문장부호의띄여쓰기를 보충하였다.",
    "output": "새 규범에서는 2007년의 규범과는 달리 제33항 문장의첫머리와 단락을 바꿀 때의 띄여쓰기, 제34항 문장부호의띄여쓰기를 보충하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "새 규범에서는 ",
        "년의 규범과는 달리 제",
        "항 문장의첫머리와 단락을 바꿀 때의 띄여쓰기",
        " 제",
        "항 문장부호의띄여쓰기를 보충하였다"
      ],
      "paragraph_index": 2904,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "1) 문장의 첫머리와 단락을 바꿀 때의 띄여쓰기",
    "output": "1) 문장의 첫머리와 단락을 바꿀 때의 띄여쓰기",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        " 문장의 첫머리와 단락을 바꿀 때의 띄여쓰기"
      ],
      "paragraph_index": 2905,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "한국에서는 문장의  첫머리와 단락을 바꿀 때 한칸을띄여쓴다.  중국의 조선말규범에서  이 부분을 규정하지  않았지만 문장의 첫머리와 단락을 바꿀 때 두칸을 띄여씀을규칙으로 삼아왔다",
    "output": "한국에서는 문장의  첫머리와 단락을 바꿀 때 한칸을띄여쓴다.  중국의 조선말규범에서  이 부분을 규정하지  않았지만 문장의 첫머리와 단락을 바꿀 때 두칸을 띄여씀을규칙으로 삼아왔다. 하기에 새 규범에서는 이를 명문화하였다. 즉 문장의 첫머리와 단락을 바꿀 때 두칸을 띄어써야 한다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "한국에서는 문장의  첫머리와 단락을 바꿀 때 한칸을띄여",
        "쓴다",
        "  중국의 조선말규범에서  이 부분을 규정하지  않았지",
        "만 문장의 첫머리와 단락을 바꿀 때 두칸을 띄여씀을규칙",
        "으로 삼아왔다"
      ],
      "paragraph_index": 2906,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성",
    "output": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성 요구가 더욱 높아지고 있는 시점에서일부 문장부호 례하면 마침표, 쉼표, 물음표, 느낌표, 가운테점, 두점의 띄여쓰기에 대하여 간단히 규정하였다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다",
        "  그러나 시대의 발전과 더불어  언어도 변화하게 되고",
        " 언어전산화의 발전과 더불어 조선말의 맞춤법",
        " 띄여쓰기 등에 대한 과학성 요구가 더욱 높아지고 있는",
        " 시점에서일부 문장부호 례하면 마침표"
      ],
      "paragraph_index": 2908,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下朝鲜语分写规则",
    "input": "이와 같이 이음표를 쓰는 것은 두개 이상의 단어가 나란히 놓이면서 붙여쓰게 될 때 그 사이를 갈라서 알아보기쉽게 하기 위함이며 또한 이음표를 쯤으로써 붙여쓴 몇개의 단어가 통일된 ",
    "output": "이와 같이 이음표를 쓰는 것은 두개 이상의 단어가 나란히 놓이면서 붙여쓰게 될 때 그 사이를 갈라서 알아보기쉽게 하기 위함이며 또한 이음표를 쯤으로써 붙여쓴 몇개의 단어가 통일된 개념을 나타념을 보여주기 위한 것이다.",
    "metadata": {
      "category": "spacing",
      "type": "general_rule",
      "examples": [
        "이와 같이 이음표를 쓰는 것은 두개 이상의 단어가 나란",
        "히 놓이면서 붙여쓰게 될 때 그 사이를 갈라서 알아보기",
        "쉽게 하기 위함이며 또한 이음표를 쯤으로써 붙여쓴 몇개",
        "의 단어가 통일된 개념을 나타념을 보여주기 위한 것이다"
      ],
      "paragraph_index": 3108,
      "source_category": "spacing"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "2) 서로 나른  품사들 이결합퇴 여새로 운동사 를이",
    "output": "2) 서로 나른  품사들 이결합퇴 여새로 운동사 를이",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 168,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "3) 서로 나른 품사들이 결합퇴여 새로운 형홋사를 이",
    "output": "3) 서로 나른 품사들이 결합퇴여 새로운 형홋사를 이",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 170,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "이것은 어느 품사에서나 무성자음 야래의 순한소리는언제팃소리로  발음한냐 는것 을말해준.  무성자음으이루어죄 받침소리는 꼭 닫혔냐가 냐슴에 호는 순한소리를반냐게 되끄로 순한소리를 언",
    "output": "이것은 어느 품사에서나 무성자음 야래의 순한소리는언제팃소리로  발음한냐 는것 을말해준.  무성자음으이루어죄 받침소리는 꼭 닫혔냐가 냐슴에 호는 순한소리를반냐게 되끄로 순한소리를 언제나 된소리로 발슴하게 된니. 여기에서 받‘ㄱ, ㅋ, ㄲ, ㄳ, ㄺ’의 받쉠소리는[7]이고 받침‘ㄷ, ㅅ, ㅈ, ㅊ, ㄹ, ㅆ’의 받침소리는[ㄷ]이며 받캪‘日, ㅍ, 괜, 改, ㅄ’희  받쉠소리 [ ]니. 이  받침소리 는모 두무성슴들. 냐그버 끄 로그희 순한소리는 엔제나  된소리 로된.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 418,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "호상동화는 런접되어있는 소리들이  서로 영향을 주어서 동화되는 현상이다.",
    "output": "호상동화는 런접되어있는 소리들이  서로 영향을 주어서 동화되는 현상이다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 574,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "추다: 주어—줘, 주었다—줬다",
    "output": "추다: 주어—줘, 주었다—줬다",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 1295,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下活用（활용）规则",
    "input": "모음으로 시작된 접미사는 그 수가 상당히 많다.  모음으로 시작된 접미사들 가운데 어떤 것은 활용성이 많아 어근과 접미사를 갈라내기 쉽고 어떤 것은 활용성이  어느 정도 있다 하더",
    "output": "모음으로 시작된 접미사는 그 수가 상당히 많다.  모음으로 시작된 접미사들 가운데 어떤 것은 활용성이 많아 어근과 접미사를 갈라내기 쉽고 어떤 것은 활용성이  어느 정도 있다 하더라도 그 계선이 분명하지  않아 어근과 접미사를 밝혀내기 어렵다.  어떤 것은 어근의 끋음절의  받침소리가 상당히 녹아들어가서  어근과 접미사를 밝히려 드는 것이  더  번거롭고 힘든 경우가 있다.",
    "metadata": {
      "category": "grammar",
      "type": "conjugation",
      "paragraph_index": 1576,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下活用（활용）规则",
    "input": "어근과 접미사의  계선이  분명한가, 활용성이  어뗘한가를보아 어근과 접미사를 밝혀 적는 경우와 밝혀  적지  않는경우를 보게 된다.",
    "output": "어근과 접미사의  계선이  분명한가, 활용성이  어뗘한가를보아 어근과 접미사를 밝혀 적는 경우와 밝혀  적지  않는경우를 보게 된다.",
    "metadata": {
      "category": "grammar",
      "type": "conjugation",
      "paragraph_index": 1582,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下活用（활용）规则",
    "input": "모음으로 시작된 접미사들 가운데서 활용성이  많아 어근과 접미사의 계선이 분명한 것은 밝혀 적는다.  이에  관한 것을 류형별로 갈라 보이면 다음과 같다.",
    "output": "모음으로 시작된 접미사들 가운데서 활용성이  많아 어근과 접미사의 계선이 분명한 것은 밝혀 적는다.  이에  관한 것을 류형별로 갈라 보이면 다음과 같다.",
    "metadata": {
      "category": "grammar",
      "type": "conjugation",
      "paragraph_index": 1584,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "우의 례에서 보여주다싶이  일부 단어들은 형태변화를하면서 문장에서  알맞게 쓰이도록 하는 문법적 특성이  있으며 또 일부 단어들은 형태변화를 하지 않거나 또는 외딴성분으로 되면서 ",
    "output": "우의 례에서 보여주다싶이  일부 단어들은 형태변화를하면서 문장에서  알맞게 쓰이도록 하는 문법적 특성이  있으며 또 일부 단어들은 형태변화를 하지 않거나 또는 외딴성분으로 되면서 문법적 특성을 지니고 있다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 1854,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "어간 또는 줄기라고 하는 것은 한 단어가 지닌 고유의성분 전체를 일컫는다.  일반적으로 어근과 접사를 모두 합친 것이  어간이다.  한 단어가 어근 하나만으로 이루어진경우에는 그 ",
    "output": "어간 또는 줄기라고 하는 것은 한 단어가 지닌 고유의성분 전체를 일컫는다.  일반적으로 어근과 접사를 모두 합친 것이  어간이다.  한 단어가 어근 하나만으로 이루어진경우에는 그 어근 자체가 어간이며  한 어근에  딴 어근이결합되여  이루어진 날말은 그 결합체가 어간이 된다.  어간은 적어도 한 어근을 지니는 구성체인데  실질적으로 단어자체를 가리키는 것이다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 2044,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词尾（어미）规则",
    "input": "‘가’의 례는 어근, 어간 및 단어  형태가 같은 단순어이고 ‘나’의 례는 용언의 경우로서 어미  ‘-다’를 빼면 단일 어근인 단순어임을 알 수 있다. 단순어는 형태로 볼 때",
    "output": "‘가’의 례는 어근, 어간 및 단어  형태가 같은 단순어이고 ‘나’의 례는 용언의 경우로서 어미  ‘-다’를 빼면 단일 어근인 단순어임을 알 수 있다. 단순어는 형태로 볼 때",
    "metadata": {
      "category": "grammar",
      "type": "ending",
      "examples": [
        "있다"
      ],
      "paragraph_index": 2061,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "명사란 대상을 이름 지어 나타내는 품사를 말한다.  따라서 인물, 동물, 사물, 식물 및 기타 여러가지 대상의 이름을 나타내는 단어는 다 명사에 속하게 된다.",
    "output": "명사란 대상을 이름 지어 나타내는 품사를 말한다.  따라서 인물, 동물, 사물, 식물 및 기타 여러가지 대상의 이름을 나타내는 단어는 다 명사에 속하게 된다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2088,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체",
    "output": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체가 하나의 단어로 되기에 붙여쓴다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2100,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "동격어란 어떤 대상에 대하여 같은 자격을 가진 말을덧붙여 보래여주어 그것을 두드려지게  강조하는 규정어의일종이다.  따라서 동격어는 뒤의 말과 띄여써야 한다.",
    "output": "동격어란 어떤 대상에 대하여 같은 자격을 가진 말을덧붙여 보래여주어 그것을 두드려지게  강조하는 규정어의일종이다.  따라서 동격어는 뒤의 말과 띄여써야 한다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 2520,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "수사란 대상의 일정한 수량이나 순서를 나타내는 품사를 말한다.  수사는 십진법에 따라 떠여쓰면 리상적이라고생각되지만 그렇게 되면 너무 토막토막 작게 갈라놓아 의미 파악에 지장이 될",
    "output": "수사란 대상의 일정한 수량이나 순서를 나타내는 품사를 말한다.  수사는 십진법에 따라 떠여쓰면 리상적이라고생각되지만 그렇게 되면 너무 토막토막 작게 갈라놓아 의미 파악에 지장이 될 수 있기 때문에 십진법을 따르지  않고 있다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2554,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "내명사란 내상을 가리키기만 하는 품사를 말한다.",
    "output": "내명사란 내상을 가리키기만 하는 품사를 말한다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2588,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "2) 서로 다른 품사들이 결합되여 새로운 동사를 이룰 경우의띄여쓰기",
    "output": "2) 서로 다른 품사들이 결합되여 새로운 동사를 이룰 경우의띄여쓰기",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2657,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법",
    "output": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법이다.  따라서  띄여쓰기를 어떻게  해야 하는가 하는 문제가 제기된다.  왜냐하면 총칙에 “조선말은단어를 단위로 하여 띄여쓰는 것을 원칙으로 한다.”고 했기 때문이다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2658,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "서로 다른 품사들이  어울려서 하나의 동사로 된 것은",
    "output": "서로 다른 품사들이  어울려서 하나의 동사로 된 것은",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2659,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "3) 서로 다른 품사들이 결합되여 새로운 형용사를 이룰 경우의띄여쓰기",
    "output": "3) 서로 다른 품사들이 결합되여 새로운 형용사를 이룰 경우의띄여쓰기",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2671,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 ",
    "output": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 품사들이 직접 어울려서 하나의 형용사로 된것은 붙여쓴다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2672,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "관형사는 대상의 특성을 규정하는 품사로서 하나의 단어이고 접두사는 어근에 첨가되여 새로운 의미를 부여하면서 새로운 단어를 만드는 형태소이다.",
    "output": "관형사는 대상의 특성을 규정하는 품사로서 하나의 단어이고 접두사는 어근에 첨가되여 새로운 의미를 부여하면서 새로운 단어를 만드는 형태소이다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2692,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "1) 관형사는 독자적인 품사이기 때문에 대부분의 관형사는 아래 단위와 띄여쓴다.",
    "output": "1) 관형사는 독자적인 품사이기 때문에 대부분의 관형사는 아래 단위와 띄여쓴다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 2707,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "이내: ‘다름 아닌 바로 나의’의 뜻을 힘 주어  이르는200",
    "output": "이내: ‘다름 아닌 바로 나의’의 뜻을 힘 주어  이르는200",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 2807,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下语序（어순）规则",
    "input": "우리는 글을 쓰거나 읽을 때 글의 내용을 쉽게 알려주고 파악하기 위하여 문장들 사이 또는 문장 안에서의 각단위들 사이에 필요되는 문장부호를 찍는다.  물론 문장과문장, 단락과 단락",
    "output": "우리는 글을 쓰거나 읽을 때 글의 내용을 쉽게 알려주고 파악하기 위하여 문장들 사이 또는 문장 안에서의 각단위들 사이에 필요되는 문장부호를 찍는다.  물론 문장과문장, 단락과 단락, 문단과 문단 사이에서의 런계는 주로접속어, 토, 어순 등에 의하여 맺어질 수도 있고 장, 절을나타내는 말을 쓰거나 기타 수단들이  리용될 수도 있다.그러나 글에서 여러 단위들 사이의  런계가 이러한 언어적수단으로써만 충분한 것이 아니다.  문장부호는 여러  언어자체의 수단만으로는 맡아나설 수 없는 여러가지 독특한역할을 하면서 문장들, 문장 속에서의 여러 단위들 사이의런계와 다양한 뜻, 그 기능을 잘 나타내기 위하여 효과적으로 쓰인다.",
    "metadata": {
      "category": "grammar",
      "type": "word_order",
      "paragraph_index": 2921,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "여기에서  ‘선생님’은 호칭어,  ‘간단히 말하면’은 삽입어이고 ‘아’는 감동어, ‘용기’는 제지어이다.  이것들은 문장 안에서  어느 한 성분과만 런계되여있는 것이  아니라 상대",
    "output": "여기에서  ‘선생님’은 호칭어,  ‘간단히 말하면’은 삽입어이고 ‘아’는 감동어, ‘용기’는 제지어이다.  이것들은 문장 안에서  어느 한 성분과만 런계되여있는 것이  아니라 상대적으로 떨어져서 뒤에 오는 전체 문장과 관계를 발생한다.  이런 독립적인 성분을 문장에서의 다른 성분들과 갈라보기 위하여 그 뒤에 쉼표를 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3043,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "그리고 ‘첫째로, 둘째로, 셋째로…’, ‘끝으로, 간략해말하면, 다시 말하면, 마지막으로, 종합하여 말하면, 다음으로…’등은 삽입어로서 뒤에 오는 성분들과의 사이를 갈라보기 위하여",
    "output": "그리고 ‘첫째로, 둘째로, 셋째로…’, ‘끝으로, 간략해말하면, 다시 말하면, 마지막으로, 종합하여 말하면, 다음으로…’등은 삽입어로서 뒤에 오는 성분들과의 사이를 갈라보기 위하여 쉼표를 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3044,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "넷째, 문장성분이  전도된 어순에서  종결술어  뒤에 찍는다.",
    "output": "넷째, 문장성분이  전도된 어순에서  종결술어  뒤에 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3045,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下语序（어순）规则",
    "input": "넷째, 문장성분이  전도된 어순에서  종결술어  뒤에 찍는다.",
    "output": "넷째, 문장성분이  전도된 어순에서  종결술어  뒤에 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "word_order",
      "paragraph_index": 3045,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "전도된 어순은 문장성분의  차례가 바뀌여  나타난다.우의 례에서 보다싶이 문장성분의 차례가 어떻게  바뀌였는가를 뚜렷이  갈라보이기 위하여  앞에  내세운 성분의  뒤에",
    "output": "전도된 어순은 문장성분의  차례가 바뀌여  나타난다.우의 례에서 보다싶이 문장성분의 차례가 어떻게  바뀌였는가를 뚜렷이  갈라보이기 위하여  앞에  내세운 성분의  뒤에",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3046,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下语序（어순）规则",
    "input": "전도된 어순은 문장성분의  차례가 바뀌여  나타난다.우의 례에서 보다싶이 문장성분의 차례가 어떻게  바뀌였는가를 뚜렷이  갈라보이기 위하여  앞에  내세운 성분의  뒤에",
    "output": "전도된 어순은 문장성분의  차례가 바뀌여  나타난다.우의 례에서 보다싶이 문장성분의 차례가 어떻게  바뀌였는가를 뚜렷이  갈라보이기 위하여  앞에  내세운 성분의  뒤에",
    "metadata": {
      "category": "grammar",
      "type": "word_order",
      "paragraph_index": 3046,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "그리고 우리말에서  시간 또는 장소와 관련된 것은 문정의 맨앞에 내세워 독립적이라 할 수 있을 정도로 독자성을 가지고 뒤의 문장 전체와 관련되게 하는 경우가  있다.이  때  앞에",
    "output": "그리고 우리말에서  시간 또는 장소와 관련된 것은 문정의 맨앞에 내세워 독립적이라 할 수 있을 정도로 독자성을 가지고 뒤의 문장 전체와 관련되게 하는 경우가  있다.이  때  앞에 내세운 성분의 뒤에 반점을 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3052,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "다섯째, 동종의 문장성분들을 똑똑히  갈라주기 위하여그 사이에 찍는다.",
    "output": "다섯째, 동종의 문장성분들을 똑똑히  갈라주기 위하여그 사이에 찍는다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3056,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "첫째, 동종의 문장성분들과 총괄어 사이에  친다.",
    "output": "첫째, 동종의 문장성분들과 총괄어 사이에  친다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3118,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下句子成分规则",
    "input": "례문과 같이 동종의 문장성분간에는 쉼표로 갈라주고동종의 문장성분들과 총괄어 사이에는 풀이표를 쳐서  갈라준다.  만약 동종의 문장성분들과 총괄어 사이에도 쉼표를찍는다면 쉼표가 계속",
    "output": "례문과 같이 동종의 문장성분간에는 쉼표로 갈라주고동종의 문장성분들과 총괄어 사이에는 풀이표를 쳐서  갈라준다.  만약 동종의 문장성분들과 총괄어 사이에도 쉼표를찍는다면 쉼표가 계속되여  이 사이를 섞갈릴 수 있기 때문이다.",
    "metadata": {
      "category": "grammar",
      "type": "sentence_component",
      "paragraph_index": 3122,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "여섯째, 사전 등에서 올림말의 품사거나 발음을 표시할 때 중괄호를 쓴다.",
    "output": "여섯째, 사전 등에서 올림말의 품사거나 발음을 표시할 때 중괄호를 쓴다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 3246,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词类（품사）规则",
    "input": "례문의 어휘들은 《조선말사전》에 수록된 올림말로서매 올림말 뒤의  첫번째 중괄호는 발음을 나타내고 두번째중팔호는 해당 올림말의 품사 소속을 나타낸다.",
    "output": "례문의 어휘들은 《조선말사전》에 수록된 올림말로서매 올림말 뒤의  첫번째 중괄호는 발음을 나타내고 두번째중팔호는 해당 올림말의 품사 소속을 나타낸다.",
    "metadata": {
      "category": "grammar",
      "type": "word_class",
      "paragraph_index": 3247,
      "source_category": "grammar"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제5장  접두사와 어근 적기\t 102",
    "output": "제5장  접두사와 어근 적기\t 102",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 96,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제6장  어근과 접미사 적기\t 105",
    "output": "제6장  어근과 접미사 적기\t 105",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 97,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제7항에서는“‘아, 어, 오, 우, 으, 애, 에, 외’로 시작한 어근의  앞에  있는 받침‘ㅋ, ㄲ,  ㄹ’,  ‘ㅅ, ㅈ,  ㅊ,",
    "output": "제7항에서는“‘아, 어, 오, 우, 으, 애, 에, 외’로 시작한 어근의  앞에  있는 받침‘ㅋ, ㄲ,  ㄹ’,  ‘ㅅ, ㅈ,  ㅊ,",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 388,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "여기에서 보면 이 규정에 속하는 것은 모든 받침이 아니라‘ㄱ, ㄴ,  ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅇ’  이외의  받침들이라는것을 알 수 있으며 또 모든 모음 앞이  아니라 어근의",
    "output": "여기에서 보면 이 규정에 속하는 것은 모든 받침이 아니라‘ㄱ, ㄴ,  ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅇ’  이외의  받침들이라는것을 알 수 있으며 또 모든 모음 앞이  아니라 어근의 모음으로서‘l’를 제외한 홀모음의  앞이라는 것을 알 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 394,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "조선말에서‘ㄱ, ㄴ, ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅇ’  이외의  받침들 가운데서 어근 앞에 쓰이는 받침들로는‘ㅋ, ㄲ, ㄹ’,‘ㅅ, ㅈ, ㅊ,  ㅌ’, ‘ㅍ, ㅂ’이다.  이  ",
    "output": "조선말에서‘ㄱ, ㄴ, ㄷ,  ㄹ,  ㅁ,  ㅂ,  ㅇ’  이외의  받침들 가운데서 어근 앞에 쓰이는 받침들로는‘ㅋ, ㄲ, ㄹ’,‘ㅅ, ㅈ, ㅊ,  ㅌ’, ‘ㅍ, ㅂ’이다.  이  받침들은 아래  어근이 자기의 독자성을 유지하려는 데서  ‘l’  이외의  ‘ㅏ,ㅓ, ㅗ, ㅜ, ㅡ, ㅐ, ㅔ, ㅚ’ 등의 홀모음 앞에서는 일단닫힌소리, 즉 받침소리로 끊기였다가 다시 모음에  이어서발음한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 395,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제10항에서는 “용언어근의 끝음절받침  ‘ㄴ,  ㄴ’,‘ㅁ,口,다음에 오는 토나 접미사의 첫머리에 오는 순한四’,‘王’소리는 된소리로 발음한다.”고 규정하였다.",
    "output": "제10항에서는 “용언어근의 끝음절받침  ‘ㄴ,  ㄴ’,‘ㅁ,口,다음에 오는 토나 접미사의 첫머리에 오는 순한四’,‘王’소리는 된소리로 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 430,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "받침 ‘ㄴ,  ㄴ’의 받침소리는 [ㄴ]이고 받침 ‘ㅁ, ㅁ’의 받침소리는 [ㅁ]이며  받침  ‘王’의  받침소리는 [ㄹ]이다.  이 받침소리들은 제9항과는 사정이 달라서 첫째로, ",
    "output": "받침 ‘ㄴ,  ㄴ’의 받침소리는 [ㄴ]이고 받침 ‘ㅁ, ㅁ’의 받침소리는 [ㅁ]이며  받침  ‘王’의  받침소리는 [ㄹ]이다.  이 받침소리들은 제9항과는 사정이 달라서 첫째로, 반드시 용언어근의 끝음절 받침소리여야 되고 둘째로, 반드시 토나 접미사를 만날 경우여야 되고 셋째로, [ㄹ]받침소리는 반드시 둘받침의  받침소리여야 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 431,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "첫째, 용언어근 끝음절받침이  아닐 경우에는 된소리로되지  않을 수 있다.",
    "output": "첫째, 용언어근 끝음절받침이  아닐 경우에는 된소리로되지  않을 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 442,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "안받침[안받침](어근+어근+접미사)",
    "output": "안받침[안받침](어근+어근+접미사)",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 453,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "남잡이[남자비](어근+어근+접미사)",
    "output": "남잡이[남자비](어근+어근+접미사)",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 455,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그리고 [붙임]에 밝혀있다싶이  ‘ㅎ’이  아래에 오는 어근의 첫소리로 순한소리를 만날 경우에는 거센소리로 되지않는다.",
    "output": "그리고 [붙임]에 밝혀있다싶이  ‘ㅎ’이  아래에 오는 어근의 첫소리로 순한소리를 만날 경우에는 거센소리로 되지않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 495,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "여기에서‘옳바르다’는‘옳고 바르다’즉‘옳다’, ‘바르다’의 용언어근들이  결합되였을 뿐만 아니라 병렬적으로결합된 것이여서‘ㅎ’의  아래소리가 거센소리로도 된소리로도 되지 않고 그대",
    "output": "여기에서‘옳바르다’는‘옳고 바르다’즉‘옳다’, ‘바르다’의 용언어근들이  결합되였을 뿐만 아니라 병렬적으로결합된 것이여서‘ㅎ’의  아래소리가 거센소리로도 된소리로도 되지 않고 그대로 순한소리로 되였다.  그리고‘싫증’은 용언어근과 명사어근이  종속적으로 결합된  것이여서‘ㅎ’의 아래소리가 거센소리로도 순한소리로도 되지  않고된소리로 되였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 506,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "여기에서  반드시  지적하여야 할 것은‘ㅎ’이  받침이여야 한다는 것이다.  받침이 아닌, 어근 내부의‘ㅎ’은 약화되기는 하나 발음은 한다.  례를 들면 다음과 같다.",
    "output": "여기에서  반드시  지적하여야 할 것은‘ㅎ’이  받침이여야 한다는 것이다.  받침이 아닌, 어근 내부의‘ㅎ’은 약화되기는 하나 발음은 한다.  례를 들면 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 528,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제24항에서는 “합성어 또는 파생어에서  앞 형태소의끝소리가 ‘ㄴ’이고 뒤 형태소의  첫소리가 ‘ㄹ’일 때는 제대로 [ㄴ,  ㄹ]로 발음하는 것을 원칙으로 하면서 [ㄴ, ㄴ]으로 ",
    "output": "제24항에서는 “합성어 또는 파생어에서  앞 형태소의끝소리가 ‘ㄴ’이고 뒤 형태소의  첫소리가 ‘ㄹ’일 때는 제대로 [ㄴ,  ㄹ]로 발음하는 것을 원칙으로 하면서 [ㄴ, ㄴ]으로 발음할 수도 있다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 634,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제24항에서는 “합성어 또는 파생어에서  앞 형태소의끝소리가 ‘ㄴ’이고 뒤 형태소의  첫소리가 ‘ㄹ’일 때는 제대로 [ㄴ,  ㄹ]로 발음하는 것을 원칙으로 하면서 [ㄴ, ㄴ]으로 ",
    "output": "제24항에서는 “합성어 또는 파생어에서  앞 형태소의끝소리가 ‘ㄴ’이고 뒤 형태소의  첫소리가 ‘ㄹ’일 때는 제대로 [ㄴ,  ㄹ]로 발음하는 것을 원칙으로 하면서 [ㄴ, ㄴ]으로 발음할 수도 있다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 634,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘ㄴ+ㄹ’이‘ㄹ+ㄹ’로의  여행동화는 한 형태소 내부에서 진행되나 형태소와 형태소 사이, 즉 접두사와 어근사이, 어근과 접미사 사이, 어근과 어근 사이에서는 진행되지  않고 그대로",
    "output": "‘ㄴ+ㄹ’이‘ㄹ+ㄹ’로의  여행동화는 한 형태소 내부에서 진행되나 형태소와 형태소 사이, 즉 접두사와 어근사이, 어근과 접미사 사이, 어근과 어근 사이에서는 진행되지  않고 그대로 발음한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 635,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이것은 고유어  어근과 한자어  어근의  결합에서도 마찬가지이다.",
    "output": "이것은 고유어  어근과 한자어  어근의  결합에서도 마찬가지이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 636,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제28항에서는 “합성어(또는 파생어)에서  앞 형태소가유향음이거나 모음으로 끝나고 뒤 형태소의 첫소리가 순한소리일 때는 그 순한소리를 된소리로 발음한다.”고 규정하였다.",
    "output": "제28항에서는 “합성어(또는 파생어)에서  앞 형태소가유향음이거나 모음으로 끝나고 뒤 형태소의 첫소리가 순한소리일 때는 그 순한소리를 된소리로 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 745,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제28항에서는 “합성어(또는 파생어)에서  앞 형태소가유향음이거나 모음으로 끝나고 뒤 형태소의 첫소리가 순한소리일 때는 그 순한소리를 된소리로 발음한다.”고 규정하였다.",
    "output": "제28항에서는 “합성어(또는 파생어)에서  앞 형태소가유향음이거나 모음으로 끝나고 뒤 형태소의 첫소리가 순한소리일 때는 그 순한소리를 된소리로 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 745,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ, ",
    "output": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ,  ㅈ’이여야 한다.  그러나 이  경우에도 언제나 된소리현상이  일어나는 것은 아니다.  합성어의  어근들이  병렬적  결합관계에 놓여있을 때는 된소리현상이  일어나지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어",
        "또는",
        "파생어의"
      ],
      "paragraph_index": 752,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ, ",
    "output": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ,  ㅈ’이여야 한다.  그러나 이  경우에도 언제나 된소리현상이  일어나는 것은 아니다.  합성어의  어근들이  병렬적  결합관계에 놓여있을 때는 된소리현상이  일어나지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 752,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ, ",
    "output": "합성어 또는 파생어의  형태소 사이에서 보동 된소리현상이  일어난다.  즉 앞 형태소의 끝소리가 유향음이거나 모음이여야 하고 뒤  형태소의  첫소리가 순한소리  ‘ㄱ,  ㄷ,ㅂ,  ㅈ’이여야 한다.  그러나 이  경우에도 언제나 된소리현상이  일어나는 것은 아니다.  합성어의  어근들이  병렬적  결합관계에 놓여있을 때는 된소리현상이  일어나지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 752,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어의  어근들이  종속적  결합관계에 놓여있을 때도언제나 된소리현상이  일어나는 것은 아니다.  합성어들의어근 사이에 규정토 ‘ㅡㄹ’이 끼일 때는 뒤 형태소의 첫소",
    "output": "합성어의  어근들이  종속적  결합관계에 놓여있을 때도언제나 된소리현상이  일어나는 것은 아니다.  합성어들의어근 사이에 규정토 ‘ㅡㄹ’이 끼일 때는 뒤 형태소의 첫소",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어의",
        "어근들이",
        "종속적"
      ],
      "paragraph_index": 753,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "합성어의  어근들이  종속적  결합관계에 놓여있을 때도언제나 된소리현상이  일어나는 것은 아니다.  합성어들의어근 사이에 규정토 ‘ㅡㄹ’이 끼일 때는 뒤 형태소의 첫소",
    "output": "합성어의  어근들이  종속적  결합관계에 놓여있을 때도언제나 된소리현상이  일어나는 것은 아니다.  합성어들의어근 사이에 규정토 ‘ㅡㄹ’이 끼일 때는 뒤 형태소의 첫소",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 753,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어희 어군들의 종속적 결합관계에서(피생어도 포함함) 이상의 조제을 제외하고는 단어에 따라 된소리현상이일어난냐. 니시 말하편 같은 어슴론적 조건하에서도 된소리현상이 일어날 빼가 ",
    "output": "합성어희 어군들의 종속적 결합관계에서(피생어도 포함함) 이상의 조제을 제외하고는 단어에 따라 된소리현상이일어난냐. 니시 말하편 같은 어슴론적 조건하에서도 된소리현상이 일어날 빼가 있고 일어냐지 않을 빼가 있냐. 이것은 합성어외 피생어에 있어서 된소리현상이 보편적인 법칙성을 ㄲ지 못한니는 것을 말하여준냐.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어희",
        "어군들의",
        "종속적"
      ],
      "paragraph_index": 761,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~가'的构词规则是什么？",
    "input": "",
    "output": "后缀'~가'（汉字义：价）的构词规则：\n\n~가(价): 원가[원까], 물가[물까], 대가[내까]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~가",
      "hanja_meaning": "价",
      "paragraph_index": 788,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~건'的构词规则是什么？",
    "input": "",
    "output": "后缀'~건'（汉字义：件）的构词规则：\n\n~건(件): 문건[문껀], 사건[사껀]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~건",
      "hanja_meaning": "件",
      "paragraph_index": 789,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~격'的构词规则是什么？",
    "input": "",
    "output": "后缀'~격'（汉字义：格）的构词规则：\n\n~격(格): 성격[성껴], 엄격성[엄꺽썽], 주격[주껴]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~격",
      "hanja_meaning": "格",
      "paragraph_index": 790,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~구'的构词规则是什么？",
    "input": "",
    "output": "后缀'~구'（汉字义：句）的构词规则：\n\n~구(句): 성구[성꾸], 례구[레꾸]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~구",
      "hanja_meaning": "句",
      "paragraph_index": 791,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~고'的构词规则是什么？",
    "input": "",
    "output": "后缀'~고'（汉字义：库）的构词规则：\n\n~고(库): 창고[창ㅍ], 금고[금ㅍ], 저장고[저장ㅍ]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~고",
      "hanja_meaning": "库",
      "paragraph_index": 792,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~과'的构词规则是什么？",
    "input": "",
    "output": "后缀'~과'（汉字义：果）的构词规则：\n\n~과(果): 성과[성꽈], 효과[효꽈]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~과",
      "hanja_meaning": "果",
      "paragraph_index": 793,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~과'的构词规则是什么？",
    "input": "",
    "output": "后缀'~과'（汉字义：科）的构词规则：\n\n~과(科): 분과[분꽈], 내과[내꽈]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~과",
      "hanja_meaning": "科",
      "paragraph_index": 794,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~권'的构词规则是什么？",
    "input": "",
    "output": "后缀'~권'（汉字义：权）的构词规则：\n\n~권(权): 정권[정꿘], 인권[인꿘]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~권",
      "hanja_meaning": "权",
      "paragraph_index": 795,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~법'的构词规则是什么？",
    "input": "",
    "output": "后缀'~법'（汉字义：法）的构词规则：\n\n~법(法): 헌법[헌뼘], 필법[필뼘], 가법[가뼘]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~법",
      "hanja_meaning": "法",
      "paragraph_index": 796,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~수'的构词规则是什么？",
    "input": "",
    "output": "后缀'~수'（汉字义：数）的构词规则：\n\n~수(数): 허수[허쑤], 우수[우쑤]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~수",
      "hanja_meaning": "数",
      "paragraph_index": 803,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~자'的构词规则是什么？",
    "input": "",
    "output": "后缀'~자'（汉字义：字）的构词规则：\n\n~자(字): 문자[문짜], 한자[한짜]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~자",
      "hanja_meaning": "字",
      "paragraph_index": 804,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~적'的构词规则是什么？",
    "input": "",
    "output": "后缀'~적'（汉字义：的）的构词规则：\n\n~적(的): 인적[인쩍], 내적[내쩍]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~적",
      "hanja_meaning": "的",
      "paragraph_index": 805,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~점'的构词规则是什么？",
    "input": "",
    "output": "后缀'~점'（汉字义：点）的构词规则：\n\n~점(点): 관점[관쩜], 중점[중쩜], 우점[우쩜]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~점",
      "hanja_meaning": "点",
      "paragraph_index": 806,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~권'的构词规则是什么？",
    "input": "",
    "output": "后缀'~권'（汉字义：券）的构词规则：\n\n~권(券): 러행권[러행퀸], 관람권[팔람퀸]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~권",
      "hanja_meaning": "券",
      "paragraph_index": 815,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~병'的构词规则是什么？",
    "input": "",
    "output": "后缀'~병'（汉字义：病）的构词规则：\n\n~병(病): 랭병[랭뻥], 급성병[급썽뻥]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~병",
      "hanja_meaning": "病",
      "paragraph_index": 816,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~성'的构词规则是什么？",
    "input": "",
    "output": "后缀'~성'（汉字义：性）的构词规则：\n\n~성(性): 만성[만성], 본성[본성]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~성",
      "hanja_meaning": "性",
      "paragraph_index": 819,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~급'的构词规则是什么？",
    "input": "",
    "output": "后缀'~급'（汉字义：级）的构词规则：\n\n~급(级): 초급[초급], 중급[중급]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~급",
      "hanja_meaning": "级",
      "paragraph_index": 820,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~증'的构词规则是什么？",
    "input": "",
    "output": "后缀'~증'（汉字义：症）的构词规则：\n\n~증(症): 부증[부증]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~증",
      "hanja_meaning": "症",
      "paragraph_index": 821,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "后缀'~병'的构词规则是什么？",
    "input": "",
    "output": "后缀'~병'（汉字义：病）的构词规则：\n\n~병(病): 본병[본병], 만병[만병]",
    "metadata": {
      "category": "wordformation",
      "type": "suffix",
      "suffix": "~병",
      "hanja_meaning": "病",
      "paragraph_index": 822,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제29항에서는 “합성어(또는 파생어)에서  앞 형태소가자음으로 끝나고 뒤 형태소가 모음 ‘ㅑ,  ㅕ, ㅛ, ㅠ,  ㅣ’로 시작될 때는 아래음절의 첫소리에  언제나 [ㄴ]을 덧내여 ",
    "output": "제29항에서는 “합성어(또는 파생어)에서  앞 형태소가자음으로 끝나고 뒤 형태소가 모음 ‘ㅑ,  ㅕ, ㅛ, ㅠ,  ㅣ’로 시작될 때는 아래음절의 첫소리에  언제나 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 824,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제29항에서는 “합성어(또는 파생어)에서  앞 형태소가자음으로 끝나고 뒤 형태소가 모음 ‘ㅑ,  ㅕ, ㅛ, ㅠ,  ㅣ’로 시작될 때는 아래음절의 첫소리에  언제나 [ㄴ]을 덧내여 ",
    "output": "제29항에서는 “합성어(또는 파생어)에서  앞 형태소가자음으로 끝나고 뒤 형태소가 모음 ‘ㅑ,  ㅕ, ㅛ, ㅠ,  ㅣ’로 시작될 때는 아래음절의 첫소리에  언제나 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 824,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "여기에서 보면 합성어 또는 파생어의  형태소와 형태소들이  결합할 때  앞 형태소의 끝소리가 자음이고 뒤  형태소의 첫소리가 모음‘ㅑ, ㅕ, ㅛ, ㅠ, ㅣ’, 다시 말하면 모음‘ㅣ",
    "output": "여기에서 보면 합성어 또는 파생어의  형태소와 형태소들이  결합할 때  앞 형태소의 끝소리가 자음이고 뒤  형태소의 첫소리가 모음‘ㅑ, ㅕ, ㅛ, ㅠ, ㅣ’, 다시 말하면 모음‘ㅣ’거나‘ㅣ’를 가진 상승적  이중모음일 때는 반드시 첫소리에 [ㄴ]이 첨가된다.  이것은 고유어에서나 한자어에서나마찬가지다.  아래에 세가지로 나누어  설명할 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "여기에서",
        "보면",
        "합성어"
      ],
      "paragraph_index": 831,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "여기에서 보면 합성어 또는 파생어의  형태소와 형태소들이  결합할 때  앞 형태소의 끝소리가 자음이고 뒤  형태소의 첫소리가 모음‘ㅑ, ㅕ, ㅛ, ㅠ, ㅣ’, 다시 말하면 모음‘ㅣ",
    "output": "여기에서 보면 합성어 또는 파생어의  형태소와 형태소들이  결합할 때  앞 형태소의 끝소리가 자음이고 뒤  형태소의 첫소리가 모음‘ㅑ, ㅕ, ㅛ, ㅠ, ㅣ’, 다시 말하면 모음‘ㅣ’거나‘ㅣ’를 가진 상승적  이중모음일 때는 반드시 첫소리에 [ㄴ]이 첨가된다.  이것은 고유어에서나 한자어에서나마찬가지다.  아래에 세가지로 나누어  설명할 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 831,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제30항에서는 “합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 유향음‘ㄴ,ㅁ’으로 시작될때는 그 사이에 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "output": "제30항에서는 “합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 유향음‘ㄴ,ㅁ’으로 시작될때는 그 사이에 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 848,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제30항에서는 “합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 유향음‘ㄴ,ㅁ’으로 시작될때는 그 사이에 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "output": "제30항에서는 “합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 유향음‘ㄴ,ㅁ’으로 시작될때는 그 사이에 [ㄴ]을 덧내여 발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 848,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "여기에서  보면 합성어  또는 파생어에서  앞 형태소의끝소리가 모음이고 뒤 형태소의 첫소리가 유향음‘ㄴ,ㅁ’일 때 앞 형태소의 끝소리에 받침소리 [ㄴ]을 첨가하여 발음한다.  이것",
    "output": "여기에서  보면 합성어  또는 파생어에서  앞 형태소의끝소리가 모음이고 뒤 형태소의 첫소리가 유향음‘ㄴ,ㅁ’일 때 앞 형태소의 끝소리에 받침소리 [ㄴ]을 첨가하여 발음한다.  이것은 필수적 현상이 아니라 합성어 또는 파생어사이에서의 된소리현상과 같이 단어에 따라 첨가한다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "여기에서",
        "보면",
        "합성어"
      ],
      "paragraph_index": 849,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "여기에서  보면 합성어  또는 파생어에서  앞 형태소의끝소리가 모음이고 뒤 형태소의 첫소리가 유향음‘ㄴ,ㅁ’일 때 앞 형태소의 끝소리에 받침소리 [ㄴ]을 첨가하여 발음한다.  이것",
    "output": "여기에서  보면 합성어  또는 파생어에서  앞 형태소의끝소리가 모음이고 뒤 형태소의 첫소리가 유향음‘ㄴ,ㅁ’일 때 앞 형태소의 끝소리에 받침소리 [ㄴ]을 첨가하여 발음한다.  이것은 필수적 현상이 아니라 합성어 또는 파생어사이에서의 된소리현상과 같이 단어에 따라 첨가한다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 849,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제31항에서는“합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 ‘야, 여, 요, 유,  이’로 시작될 때는 그 사이에 [ㄴ, ㄴ]을 덧내여  발음한다.”고 규정하",
    "output": "제31항에서는“합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 ‘야, 여, 요, 유,  이’로 시작될 때는 그 사이에 [ㄴ, ㄴ]을 덧내여  발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 868,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제31항에서는“합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 ‘야, 여, 요, 유,  이’로 시작될 때는 그 사이에 [ㄴ, ㄴ]을 덧내여  발음한다.”고 규정하",
    "output": "제31항에서는“합성어(또는 파생어)에서  앞 형태소가모음으로 끝나고 뒤 형태소가 ‘야, 여, 요, 유,  이’로 시작될 때는 그 사이에 [ㄴ, ㄴ]을 덧내여  발음한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 868,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "이것은 합성어 또는 파생어에서 모음과 모음 사이(뒤형태소의  첫소리는 반드시  ‘ㅣ’거나 ‘ㅣ’를 가진 상승적이중모음이여야 한다.)에서  어음을 첨가하는 현상이다.  여기에서  앞",
    "output": "이것은 합성어 또는 파생어에서 모음과 모음 사이(뒤형태소의  첫소리는 반드시  ‘ㅣ’거나 ‘ㅣ’를 가진 상승적이중모음이여야 한다.)에서  어음을 첨가하는 현상이다.  여기에서  앞 형태소의 끝소리에  받침소리  [ㄴ]을 첨가하고뒤  형태소의 첫소리에 또 [ㄴ]을 첨가한다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "이것은",
        "합성어",
        "또는"
      ],
      "paragraph_index": 869,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "이것은 합성어 또는 파생어에서 모음과 모음 사이(뒤형태소의  첫소리는 반드시  ‘ㅣ’거나 ‘ㅣ’를 가진 상승적이중모음이여야 한다.)에서  어음을 첨가하는 현상이다.  여기에서  앞",
    "output": "이것은 합성어 또는 파생어에서 모음과 모음 사이(뒤형태소의  첫소리는 반드시  ‘ㅣ’거나 ‘ㅣ’를 가진 상승적이중모음이여야 한다.)에서  어음을 첨가하는 현상이다.  여기에서  앞 형태소의 끝소리에  받침소리  [ㄴ]을 첨가하고뒤  형태소의 첫소리에 또 [ㄴ]을 첨가한다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 869,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제6항은 한 형태소 안에서 같은 음절이나 비슷한 음절이  겹쳐나는 것을 갈거나 비슷한 글자로 적는 규정이다.이와 같은 규정은 ‘ㅡ하다’형 형용사의  어근적  단어를 고정시키고 음절",
    "output": "제6항은 한 형태소 안에서 같은 음절이나 비슷한 음절이  겹쳐나는 것을 갈거나 비슷한 글자로 적는 규정이다.이와 같은 규정은 ‘ㅡ하다’형 형용사의  어근적  단어를 고정시키고 음절간의  발음현상을 직접 표기에  반영하려는 목적에서  나온 규정이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1066,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "용언어간의  모음이  ‘ㅏㅡ,  ㅗㅡ’(어간의  끝소리가‘ㅡ’로 된 것)인 경우라도 합성어간인 경우에는 ‘ㅡ아, ㅡ았ㅡ’으로 적지  않고 ‘ㅡ어, ㅡ었ㅡ’으로 적는다.",
    "output": "용언어간의  모음이  ‘ㅏㅡ,  ㅗㅡ’(어간의  끝소리가‘ㅡ’로 된 것)인 경우라도 합성어간인 경우에는 ‘ㅡ아, ㅡ았ㅡ’으로 적지  않고 ‘ㅡ어, ㅡ었ㅡ’으로 적는다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "용언어간의",
        "모음이",
        "어간의"
      ],
      "paragraph_index": 1242,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어란 두개 어근 또는 그 이성의  어근이 합쳐서  이루어진 단어를 말한다.  ‘부삽’은 ‘불’이라는 명사어근과‘삽’이라는 명사어근이  합쳐서  이루어진  것이고 ‘된장’은‘되다",
    "output": "합성어란 두개 어근 또는 그 이성의  어근이 합쳐서  이루어진 단어를 말한다.  ‘부삽’은 ‘불’이라는 명사어근과‘삽’이라는 명사어근이  합쳐서  이루어진  것이고 ‘된장’은‘되다’라는 형용사어근 ‘되—’와 ‘장’이라는 명사어근이합쳐서  이루어진 것이며  ‘검붉다’는 ‘검다’와 ‘붉다’의  형용사어근 ‘검—’과 ‘붉—’이  서로 어울려  합성어를  이룬것이다.  이와 같이 둘 또는 그 이상의  어근이 합쳐서  이루어진 합성어의  적기에서는 매개  어근의  형태를 각각 밝혀주는 형태주의원칙을 기본으로 따르면서  어근과 어근이  어",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어란",
        "두개",
        "어근"
      ],
      "paragraph_index": 1380,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "합성어란 두개 어근 또는 그 이성의  어근이 합쳐서  이루어진 단어를 말한다.  ‘부삽’은 ‘불’이라는 명사어근과‘삽’이라는 명사어근이  합쳐서  이루어진  것이고 ‘된장’은‘되다",
    "output": "합성어란 두개 어근 또는 그 이성의  어근이 합쳐서  이루어진 단어를 말한다.  ‘부삽’은 ‘불’이라는 명사어근과‘삽’이라는 명사어근이  합쳐서  이루어진  것이고 ‘된장’은‘되다’라는 형용사어근 ‘되—’와 ‘장’이라는 명사어근이합쳐서  이루어진 것이며  ‘검붉다’는 ‘검다’와 ‘붉다’의  형용사어근 ‘검—’과 ‘붉—’이  서로 어울려  합성어를  이룬것이다.  이와 같이 둘 또는 그 이상의  어근이 합쳐서  이루어진 합성어의  적기에서는 매개  어근의  형태를 각각 밝혀주는 형태주의원칙을 기본으로 따르면서  어근과 어근이  어",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1380,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제15항에서는“합성어는 매개  어근의  형태를 각각 밝혀 적는 것을 원칙으로 한다.”고 규정하였다.",
    "output": "제15항에서는“합성어는 매개  어근의  형태를 각각 밝혀 적는 것을 원칙으로 한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어는",
        "매개"
      ],
      "paragraph_index": 1388,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제15항에서는“합성어는 매개  어근의  형태를 각각 밝혀 적는 것을 원칙으로 한다.”고 규정하였다.",
    "output": "제15항에서는“합성어는 매개  어근의  형태를 각각 밝혀 적는 것을 원칙으로 한다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1388,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "다시 말하면 어근과 어근이  어울려 합성어를 이룰 때어근과 어근 사이에  어음동화현상이  일어나거나 런음 또는절음 현상이 일어날 경우에도 매개 어근의 원 형태를 각각밝혀 적는다는 ",
    "output": "다시 말하면 어근과 어근이  어울려 합성어를 이룰 때어근과 어근 사이에  어음동화현상이  일어나거나 런음 또는절음 현상이 일어날 경우에도 매개 어근의 원 형태를 각각밝혀 적는다는 것이다.  어음동화현상이  일어나지  않는 경우는 그 형태를 밝혀 적기 어렵지  않다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "다시",
        "말하면",
        "어근과"
      ],
      "paragraph_index": 1389,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "다시 말하면 어근과 어근이  어울려 합성어를 이룰 때어근과 어근 사이에  어음동화현상이  일어나거나 런음 또는절음 현상이 일어날 경우에도 매개 어근의 원 형태를 각각밝혀 적는다는 ",
    "output": "다시 말하면 어근과 어근이  어울려 합성어를 이룰 때어근과 어근 사이에  어음동화현상이  일어나거나 런음 또는절음 현상이 일어날 경우에도 매개 어근의 원 형태를 각각밝혀 적는다는 것이다.  어음동화현상이  일어나지  않는 경우는 그 형태를 밝혀 적기 어렵지  않다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1389,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "일어나는 경우에 그 어근의  형태를 어떻게  밝혀 적는가에내하여 보기로 하자.",
    "output": "일어나는 경우에 그 어근의  형태를 어떻게  밝혀 적는가에내하여 보기로 하자.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1395,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이와 같이 두 어근(또는 접두사와 어근) 사이에서  받침  아래에 모음이 올 때 그것을 이어서  발음하지  않고 받침과 모음 사이를 끊어서  받침소리로 발음하다가 그 받침소리를 그",
    "output": "이와 같이 두 어근(또는 접두사와 어근) 사이에서  받침  아래에 모음이 올 때 그것을 이어서  발음하지  않고 받침과 모음 사이를 끊어서  받침소리로 발음하다가 그 받침소리를 그대로 모음에  이어서  발음하는 현상을 절음현상이라고 한다.  우리말에서  절음현상이  일어나는 경우를 보면두 어근(또는 접두사와 어근) 사이에서  모음으로 시작한고유어어근의  앞에  있는 받침  ‘ㅋ, ㄲ, ㄹ’,  ‘ㅅ, ㅈ,  ㅊ,ㅌ’,  ‘ㅍ,  ㅃ,  ㅂ’등이 각각 받침소리  ‘ㄱ’,  ‘ㄷ’,  ‘ㅂ’으로 발음하다가 그 받침소리를 모음에  이어  발음하므로절음현상이  일어난다.  이러한 규칙적인 발음현상은 우리말맞춤법에서  발음 내로 적지  않고 원  형태를 밝혀  적기로한 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1405,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그러나 오늘날 두개의  어근이  뚜렷하지  않은 것은 그형태를 밝혀 적지  않는다.",
    "output": "그러나 오늘날 두개의  어근이  뚜렷하지  않은 것은 그형태를 밝혀 적지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1406,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘며칠’은 ‘몇날,  몇달’에서의 의문대명사 ‘몇’과 명사인 ‘일’로 갈라볼 수 있을 것 같으나 사실은 ‘일’의  어원적 근거가 똑똑하지  않다.  만일 ‘일’이  ‘날’과 같은 ",
    "output": "‘며칠’은 ‘몇날,  몇달’에서의 의문대명사 ‘몇’과 명사인 ‘일’로 갈라볼 수 있을 것 같으나 사실은 ‘일’의  어원적 근거가 똑똑하지  않다.  만일 ‘일’이  ‘날’과 같은 그런어근이라면 ‘몇+일’은 [면닐]로 발음하여야 한다.  ‘며칠’은 ‘수량’을 나타낼 뿐 아니라 ‘순서’를 나타내기도 한다.(래일이  음력으로 며칠인가?) 그러므로 이  단어는 ‘몇일’",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1407,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”",
    "output": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 1416,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”",
    "output": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 1416,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”",
    "output": "제16항에서는 “합성어(또는 파생어)를  이룰 때  어근사이에서  ‘ㅂ’이  덧나거나 뒤에 오는 어근의  첫소리가 거센소리로 바뀌여 나는 것은 덧나고 바뀌여  나는 내로 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1416,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "단어  ‘맵쌀, 좁쌀,  참쌀’은 ‘메(日)+쌀’,  ‘조(日)+쌀’,  ‘차(日)+쌀’에서  보다싶이  두 형태소가 합쳐지면서‘ㅂ’이  덧난 것이다.  이것은 아래어근 ‘쌀’에 ",
    "output": "단어  ‘맵쌀, 좁쌀,  참쌀’은 ‘메(日)+쌀’,  ‘조(日)+쌀’,  ‘차(日)+쌀’에서  보다싶이  두 형태소가 합쳐지면서‘ㅂ’이  덧난 것이다.  이것은 아래어근 ‘쌀’에 의하여  이루어진 것이다.  옛날에 ‘쌀’은 ‘빨’이였다.  옛날의  ‘ㅄ’이 오늘날 된소리  ‘ㅆ’으로 변하여  ‘쌀’로 됨과 동시에  합성어에서는 ‘ㅄ’에서의  ‘ㅂ’이 잔존형태로 남아서 오늘날 덧나",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "단어",
        "맵쌀",
        "좁쌀"
      ],
      "paragraph_index": 1418,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단어  ‘맵쌀, 좁쌀,  참쌀’은 ‘메(日)+쌀’,  ‘조(日)+쌀’,  ‘차(日)+쌀’에서  보다싶이  두 형태소가 합쳐지면서‘ㅂ’이  덧난 것이다.  이것은 아래어근 ‘쌀’에 ",
    "output": "단어  ‘맵쌀, 좁쌀,  참쌀’은 ‘메(日)+쌀’,  ‘조(日)+쌀’,  ‘차(日)+쌀’에서  보다싶이  두 형태소가 합쳐지면서‘ㅂ’이  덧난 것이다.  이것은 아래어근 ‘쌀’에 의하여  이루어진 것이다.  옛날에 ‘쌀’은 ‘빨’이였다.  옛날의  ‘ㅄ’이 오늘날 된소리  ‘ㅆ’으로 변하여  ‘쌀’로 됨과 동시에  합성어에서는 ‘ㅄ’에서의  ‘ㅂ’이 잔존형태로 남아서 오늘날 덧나",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1418,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "례를 들면 ‘머리카락(머리+가락)’,  ‘수탉(수+탉)’,‘마파람(마+바람)’등에서 보는 바와 같이 두 형태소 사이에‘ㅎ’소리가 보래여져서 뒤의 순한소리가 거센소리로되었다.  이것",
    "output": "례를 들면 ‘머리카락(머리+가락)’,  ‘수탉(수+탉)’,‘마파람(마+바람)’등에서 보는 바와 같이 두 형태소 사이에‘ㅎ’소리가 보래여져서 뒤의 순한소리가 거센소리로되었다.  이것은 지난날 일부 단어의 어근에‘ㅎ’이 첨가되던 현상(ㅎ종성체언)인데 현대어에 와서 극히 개별적인 어근에 붙으면서  뒤의 순한소리가 거센소리로 바뀌어  나는것은 합성어의 뒤 단위의  첫소리가‘ㄱ,  ㄷ,  ㅂ’과 같은자음으로 시작되었을 경우에‘ㅎ’을 만나면서 같은 계렬의거센소리로 이루어지기  때문이다.  이러한 류형에  속하는단어들은 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "례를",
        "들면",
        "머리카락"
      ],
      "paragraph_index": 1427,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들면 ‘머리카락(머리+가락)’,  ‘수탉(수+탉)’,‘마파람(마+바람)’등에서 보는 바와 같이 두 형태소 사이에‘ㅎ’소리가 보래여져서 뒤의 순한소리가 거센소리로되었다.  이것",
    "output": "례를 들면 ‘머리카락(머리+가락)’,  ‘수탉(수+탉)’,‘마파람(마+바람)’등에서 보는 바와 같이 두 형태소 사이에‘ㅎ’소리가 보래여져서 뒤의 순한소리가 거센소리로되었다.  이것은 지난날 일부 단어의 어근에‘ㅎ’이 첨가되던 현상(ㅎ종성체언)인데 현대어에 와서 극히 개별적인 어근에 붙으면서  뒤의 순한소리가 거센소리로 바뀌어  나는것은 합성어의 뒤 단위의  첫소리가‘ㄱ,  ㄷ,  ㅂ’과 같은자음으로 시작되었을 경우에‘ㅎ’을 만나면서 같은 계렬의거센소리로 이루어지기  때문이다.  이러한 류형에  속하는단어들은 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1427,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제17항에서는“합성어(또는 파생어)를 이룰 때  ‘ㄹ’이‘ㄴ, ㄷ, ㅅ, ㅈ’ 우에서 빠지는 경우에는 빠진 내로 적는다.”고 규정하였다.",
    "output": "제17항에서는“합성어(또는 파생어)를 이룰 때  ‘ㄹ’이‘ㄴ, ㄷ, ㅅ, ㅈ’ 우에서 빠지는 경우에는 빠진 내로 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어",
        "또는"
      ],
      "paragraph_index": 1435,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "제17항에서는“합성어(또는 파생어)를 이룰 때  ‘ㄹ’이‘ㄴ, ㄷ, ㅅ, ㅈ’ 우에서 빠지는 경우에는 빠진 내로 적는다.”고 규정하였다.",
    "output": "제17항에서는“합성어(또는 파생어)를 이룰 때  ‘ㄹ’이‘ㄴ, ㄷ, ㅅ, ㅈ’ 우에서 빠지는 경우에는 빠진 내로 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 1435,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "제18항에서는“합성어에서  어근의 받침소리 [ㄹ]이 뒤에 오는 어근과 어울리면서 페쇄음으로 된 것은 ‘ㄷ’으로적는다.”고 규정하였다.",
    "output": "제18항에서는“합성어에서  어근의 받침소리 [ㄹ]이 뒤에 오는 어근과 어울리면서 페쇄음으로 된 것은 ‘ㄷ’으로적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "항에서는",
        "합성어에서",
        "어근의"
      ],
      "paragraph_index": 1440,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제18항에서는“합성어에서  어근의 받침소리 [ㄹ]이 뒤에 오는 어근과 어울리면서 페쇄음으로 된 것은 ‘ㄷ’으로적는다.”고 규정하였다.",
    "output": "제18항에서는“합성어에서  어근의 받침소리 [ㄹ]이 뒤에 오는 어근과 어울리면서 페쇄음으로 된 것은 ‘ㄷ’으로적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1440,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제5장  접두사와  어근 적기",
    "output": "제5장  접두사와  어근 적기",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1449,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제19항에서는“접두사와 어근이  어울릴 때 각각 그 형래를 밝혀 적는다.”고 규정하였다.",
    "output": "제19항에서는“접두사와 어근이  어울릴 때 각각 그 형래를 밝혀 적는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1450,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접두사는 어근의  앞에 붙어서  일정한 뜻을 더해주면서새 단어를 만들어 표현을 섬세하고 다양하게 하며  어휘를풍부히 한다.  그런데 접두사도 어근과 어울릴 때 받침소리가 일정하게 ",
    "output": "접두사는 어근의  앞에 붙어서  일정한 뜻을 더해주면서새 단어를 만들어 표현을 섬세하고 다양하게 하며  어휘를풍부히 한다.  그런데 접두사도 어근과 어울릴 때 받침소리가 일정하게 바뀌여 나는 경우가 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1451,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "아래에 접두사와 어근의  적기에서  틀리기  쉬운 례를들어보이면 다음과 같다.",
    "output": "아래에 접두사와 어근의  적기에서  틀리기  쉬운 례를들어보이면 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1454,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접미사는 어근과 어울리여  새로운 단어를 만드는 데있어서 접두사의 경우보다도 훨씬 다양하고 활약적이며  어휘를 풍부히 하는 데 중요한 역할을 한다.  접미사가 어근과 어울릴 때 자",
    "output": "접미사는 어근과 어울리여  새로운 단어를 만드는 데있어서 접두사의 경우보다도 훨씬 다양하고 활약적이며  어휘를 풍부히 하는 데 중요한 역할을 한다.  접미사가 어근과 어울릴 때 자음으로 시작된 대부분 접미사와 모음으로시작된 접미사의 일부에 한해서는 그 본래 형태를 각각 밝혀 적는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1478,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제20항에서는“자음으로 시작된 접미사가 어근과 어울릴 때 그 형태를 각각 밝혀 적는 것을 원칙으로 한다.”고규정하였다.  그것은 자음으로 시작된 대부분의  접미사는어근과 어울릴  ",
    "output": "제20항에서는“자음으로 시작된 접미사가 어근과 어울릴 때 그 형태를 각각 밝혀 적는 것을 원칙으로 한다.”고규정하였다.  그것은 자음으로 시작된 대부분의  접미사는어근과 어울릴  경우에도 형태소 계선이 분명하므로 능히형태소를 밝혀 적을 수 있기 때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1480,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들면‘덮개, 맞추다,  엮히다’에서  어근‘덮—,맞—, 엮—’과 자음으로 시작된  접미사  ‘—개,  —추,—히’의 형태소 계선이 쉽게 갈라진다.  이와 같이  형태소계선이 ",
    "output": "례를 들면‘덮개, 맞추다,  엮히다’에서  어근‘덮—,맞—, 엮—’과 자음으로 시작된  접미사  ‘—개,  —추,—히’의 형태소 계선이 쉽게 갈라진다.  이와 같이  형태소계선이 명확한 것은 본래 형태를 밝혀 적음으로 하여 뜻을포착하고 리해하기 쉽다.  만일 ‘덮개’에서의  ‘덮’을 ‘덥’으로 적는다면‘날씨가 덥다.’에서의  ‘덥—’의 뜻과 혼동된다.  자음으로 시작된 대부분의 접미사는 어근과의 계선이 분명하므로 본래 형태를 밝혀 적기로 하고 그 가운데일부는 받침소리의 규칙에 맞지 않아 발음 내로 적기로 하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1481,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "아래에 자음으로 시작된 접미사와 어근을 밝혀 적는경우의 몇가지를 류형별로 갈라서 보기로 하자.",
    "output": "아래에 자음으로 시작된 접미사와 어근을 밝혀 적는경우의 몇가지를 류형별로 갈라서 보기로 하자.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1482,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "[붙임] ‘나직하다’에서  ‘나직’은 원래  형용사 ‘낮다’의  어근 ‘낮’과 ‘높직하다’ 등에서의  접미사 ‘-직’이  어울린  것이다.  이것을 형태를 밝혀 적는다면 ‘낮직’으",
    "output": "[붙임] ‘나직하다’에서  ‘나직’은 원래  형용사 ‘낮다’의  어근 ‘낮’과 ‘높직하다’ 등에서의  접미사 ‘-직’이  어울린  것이다.  이것을 형태를 밝혀 적는다면 ‘낮직’으로 적어야 한다.  그러나 실제 발음은 ‘나직-’이므로 발음 내로‘나직-’으로 표기하였다.  (‘느직하다’도  이와 마찬가지다.)",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1499,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들면 ‘놓치다, 덮치다, 돋치다, 밀치다, 받치다,부딪치다, 엎치다, 뻗치다’등에서  ‘—치’는 각각 동사어근에 붙어서 동사의 의미를 강조하여주는 역할을 한다.",
    "output": "례를 들면 ‘놓치다, 덮치다, 돋치다, 밀치다, 받치다,부딪치다, 엎치다, 뻗치다’등에서  ‘—치’는 각각 동사어근에 붙어서 동사의 의미를 강조하여주는 역할을 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1512,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "[붙임] 맞춤법에서  강조의 뜻을 나타내는 접미사 ‘-치’와 사역 또는 피동을 나타내는 접미사 ‘-히’가 ‘ㄷ’,‘ㅈ’받침으로 끝난 동사어근의 뒤에 붙을 때 발음이 갈게난다 하더라",
    "output": "[붙임] 맞춤법에서  강조의 뜻을 나타내는 접미사 ‘-치’와 사역 또는 피동을 나타내는 접미사 ‘-히’가 ‘ㄷ’,‘ㅈ’받침으로 끝난 동사어근의 뒤에 붙을 때 발음이 갈게난다 하더라도 문법적인 측면이 전혀 다름에 따라 뜻도 다르므로 이것을 엄격히 갈라서 틀리지  않게 써야 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1518,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이  접미사들은 고유어로 된 형용사어근에 붙어서  그형용사를 타동사로 만들어준다.",
    "output": "이  접미사들은 고유어로 된 형용사어근에 붙어서  그형용사를 타동사로 만들어준다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1521,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들편‘말끔하냐, 말쑥하냐, 말짱하냐’에서 어근은‘맑냐’의‘맑-’일 것이고‘널직하냐, 널냐랗냐’에서어곤은‘넓냐’의‘넓’일 것이냐. ‘얄직햐냐, 얄팍햐냐’에서 어곤은‘얇’의‘얇ㅡ",
    "output": "례를 들편‘말끔하냐, 말쑥하냐, 말짱하냐’에서 어근은‘맑냐’의‘맑-’일 것이고‘널직하냐, 널냐랗냐’에서어곤은‘넓냐’의‘넓’일 것이냐. ‘얄직햐냐, 얄팍햐냐’에서 어곤은‘얇’의‘얇ㅡ’일 것이고‘실쭉하냐’에서 어근은‘싫니’의‘싫’일 것이냐.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1529,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이렇게 받침소리 특셍에 맞지 않게 발음하므로 어근희",
    "output": "이렇게 받침소리 특셍에 맞지 않게 발음하므로 어근희",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1533,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제21항에서는 “어근과 접미사가 어울리여  그 뜻이  달라질 때에는 어근과 접미사를 밝혀 적지  않는다.”고 규정하였다.",
    "output": "제21항에서는 “어근과 접미사가 어울리여  그 뜻이  달라질 때에는 어근과 접미사를 밝혀 적지  않는다.”고 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1539,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "제22항에서는 모음으로 시작된 접미사가 어근과 어울릴 때 나서는 맞춤법에  대하여 규정하였다.",
    "output": "제22항에서는 모음으로 시작된 접미사가 어근과 어울릴 때 나서는 맞춤법에  대하여 규정하였다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1575,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "모음으로 시작된 접미사는 그 수가 상당히 많다.  모음으로 시작된 접미사들 가운데 어떤 것은 활용성이 많아 어근과 접미사를 갈라내기 쉽고 어떤 것은 활용성이  어느 정도 있다 하더",
    "output": "모음으로 시작된 접미사는 그 수가 상당히 많다.  모음으로 시작된 접미사들 가운데 어떤 것은 활용성이 많아 어근과 접미사를 갈라내기 쉽고 어떤 것은 활용성이  어느 정도 있다 하더라도 그 계선이 분명하지  않아 어근과 접미사를 밝혀내기 어렵다.  어떤 것은 어근의 끋음절의  받침소리가 상당히 녹아들어가서  어근과 접미사를 밝히려 드는 것이  더  번거롭고 힘든 경우가 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1576,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "따라서 모음으로 시작된 접미사가 어근과 어울릴  때는",
    "output": "따라서 모음으로 시작된 접미사가 어근과 어울릴  때는",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1577,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "어근과 접미사의  계선이  분명한가, 활용성이  어뗘한가를보아 어근과 접미사를 밝혀 적는 경우와 밝혀  적지  않는경우를 보게 된다.",
    "output": "어근과 접미사의  계선이  분명한가, 활용성이  어뗘한가를보아 어근과 접미사를 밝혀 적는 경우와 밝혀  적지  않는경우를 보게 된다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1582,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "1)  어근과 접미사를 밝혀 적는 경우.",
    "output": "1)  어근과 접미사를 밝혀 적는 경우.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1583,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "모음으로 시작된 접미사들 가운데서 활용성이  많아 어근과 접미사의 계선이 분명한 것은 밝혀 적는다.  이에  관한 것을 류형별로 갈라 보이면 다음과 같다.",
    "output": "모음으로 시작된 접미사들 가운데서 활용성이  많아 어근과 접미사의 계선이 분명한 것은 밝혀 적는다.  이에  관한 것을 류형별로 갈라 보이면 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1584,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "① 형용사나 동사의  어근에 붙어서  명사나 부사를 만드는 접미사 ‘ㅡ이’.",
    "output": "① 형용사나 동사의  어근에 붙어서  명사나 부사를 만드는 접미사 ‘ㅡ이’.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1586,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "여기서  ‘길이, 깊이, 높이’ 등은 형용사 ‘길다, 깊다,높다’에서  어근 ‘길ㅡ’,  ‘깊ㅡ’,  ‘높ㅡ’에  접미사 ‘ㅡ이’가 붙어서  명사로도 되고 부사로도 된다.",
    "output": "여기서  ‘길이, 깊이, 높이’ 등은 형용사 ‘길다, 깊다,높다’에서  어근 ‘길ㅡ’,  ‘깊ㅡ’,  ‘높ㅡ’에  접미사 ‘ㅡ이’가 붙어서  명사로도 되고 부사로도 된다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1587,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "‘미닫이’는 동사 ‘밀다’의  어근 ‘밀ㅡ’에 동사 ‘닫다’의  어근 ‘닫ㅡ’이  어울리여 합성어를 이룬 다음 또다시  접미사 ‘ㅡ이’가 덧붙어서  명사를 이룬 것이다.",
    "output": "‘미닫이’는 동사 ‘밀다’의  어근 ‘밀ㅡ’에 동사 ‘닫다’의  어근 ‘닫ㅡ’이  어울리여 합성어를 이룬 다음 또다시  접미사 ‘ㅡ이’가 덧붙어서  명사를 이룬 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "미닫이",
        "동사",
        "밀다"
      ],
      "paragraph_index": 1588,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘미닫이’는 동사 ‘밀다’의  어근 ‘밀ㅡ’에 동사 ‘닫다’의  어근 ‘닫ㅡ’이  어울리여 합성어를 이룬 다음 또다시  접미사 ‘ㅡ이’가 덧붙어서  명사를 이룬 것이다.",
    "output": "‘미닫이’는 동사 ‘밀다’의  어근 ‘밀ㅡ’에 동사 ‘닫다’의  어근 ‘닫ㅡ’이  어울리여 합성어를 이룬 다음 또다시  접미사 ‘ㅡ이’가 덧붙어서  명사를 이룬 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1588,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "② 명사의  어근에 붙어서  명사나 부사를 만드는 접미사‘ㅡ이’.",
    "output": "② 명사의  어근에 붙어서  명사나 부사를 만드는 접미사‘ㅡ이’.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1594,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그러나 다음과 같은 단어는 어근과 접미사를 밝혀 적지  않는다.",
    "output": "그러나 다음과 같은 단어는 어근과 접미사를 밝혀 적지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1604,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘거름’은 원래  ‘땅이  걸다, 죽이  걸다’에서 볼 수  있는 바와 같이  형용사 ‘걸다’의 어근 ‘걸’에 접미사 ‘ㅡ음’이 붙어서  ‘걸음→거름’으로 된  것이지만 ‘걸다’(",
    "output": "‘거름’은 원래  ‘땅이  걸다, 죽이  걸다’에서 볼 수  있는 바와 같이  형용사 ‘걸다’의 어근 ‘걸’에 접미사 ‘ㅡ음’이 붙어서  ‘걸음→거름’으로 된  것이지만 ‘걸다’(형용사)와는 의미가 다르다.  그러므로 이런 경우에  ‘걸다’와 런계시켜  ‘걸음’으로 적을 필요가 없다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1605,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "다음과 같은 단어들도 어근과 접미사를 밝혀 적지  않는다.",
    "output": "다음과 같은 단어들도 어근과 접미사를 밝혀 적지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1606,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "넷째, ‘ㅡ거리’와 어울릴 수 있는 어근에 붙어서 동사를 만드는 접미사 ‘ㅡ이’.",
    "output": "넷째, ‘ㅡ거리’와 어울릴 수 있는 어근에 붙어서 동사를 만드는 접미사 ‘ㅡ이’.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1633,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접미사 ‘ㅡ거리’는  이음절  이상으로 이루어진 의정의래어나 또는 그런 류형의 일부 어근에 붙어 그 현상이  되풀이됨을 나타낸다.",
    "output": "접미사 ‘ㅡ거리’는  이음절  이상으로 이루어진 의정의래어나 또는 그런 류형의 일부 어근에 붙어 그 현상이  되풀이됨을 나타낸다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1634,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접미사 ‘ㅡ이’는 ‘딸랑ㅡ딸랑딸랑ㅡ딸랑거리다ㅡ딸랑이다’에서와 같이  접미사 ‘ㅡ거리’와 어울릴 수 있는 어근에붙어  새로운 동사를 만든다.",
    "output": "접미사 ‘ㅡ이’는 ‘딸랑ㅡ딸랑딸랑ㅡ딸랑거리다ㅡ딸랑이다’에서와 같이  접미사 ‘ㅡ거리’와 어울릴 수 있는 어근에붙어  새로운 동사를 만든다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1635,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그러나 ‘—거리’와 어울릴 수 있는 어근에  다 접미사‘—이’가 어울릴 수 있는 것은 아니다.",
    "output": "그러나 ‘—거리’와 어울릴 수 있는 어근에  다 접미사‘—이’가 어울릴 수 있는 것은 아니다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1641,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘건드리다’는 ‘건들리다’(‘건드리다’의 희동형)로 적으나 ‘건들이다’로는 적지  않는다.  그것은 ‘건드리다’가 ‘건들—건들건들’과 같은 의성의래어적인 어근과는 이미  인연이  ",
    "output": "‘건드리다’는 ‘건들리다’(‘건드리다’의 희동형)로 적으나 ‘건들이다’로는 적지  않는다.  그것은 ‘건드리다’가 ‘건들—건들건들’과 같은 의성의래어적인 어근과는 이미  인연이  먼 다른 말로 되였기  때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1643,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "2) 어근과 접미사를 밝혀 적지  않는 경우.",
    "output": "2) 어근과 접미사를 밝혀 적지  않는 경우.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1644,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "첫째, 어근에  ‘—이’,  ‘——음’이외의  접미사가 붙어서이루어진 명사나 부사.",
    "output": "첫째, 어근에  ‘—이’,  ‘——음’이외의  접미사가 붙어서이루어진 명사나 부사.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1645,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "우에서 든 류형의  례들로부터  어근에  ‘ㅡ이’,  ‘ㅡ음’이외의 접미사가 어울리는 경우에 그 형태를 밝혀 적지  않는 근거를 찾아보면 내체로 다음과 같다.",
    "output": "우에서 든 류형의  례들로부터  어근에  ‘ㅡ이’,  ‘ㅡ음’이외의 접미사가 어울리는 경우에 그 형태를 밝혀 적지  않는 근거를 찾아보면 내체로 다음과 같다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1663,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "우선, 어근과 접미사의 계선이  명확하지 못하여  갈라쓰기 어렵다.",
    "output": "우선, 어근과 접미사의 계선이  명확하지 못하여  갈라쓰기 어렵다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1664,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "다음으로 단어조성의  역할로부터 본다면  접미사 ‘ㅡ이’, ‘ㅡ음’은 단어를 만드는 기능이  매우 활발하고 적극적이여서  여러  어근에 붙어 수많은 단어를 만들지만 ‘ㅡ이’, ‘ㅡ",
    "output": "다음으로 단어조성의  역할로부터 본다면  접미사 ‘ㅡ이’, ‘ㅡ음’은 단어를 만드는 기능이  매우 활발하고 적극적이여서  여러  어근에 붙어 수많은 단어를 만들지만 ‘ㅡ이’, ‘ㅡ음’이외의  접미사들은 한개 또는 몇개의  어근에만 붙어서  얼마 안되는 단어를 만든다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1666,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "의성의래어에  접미사 ‘ㅡ이’가 붙어서  단어가  이루어절 때  어근과 접미사를 밝혀 적지  않는 까닭은 주요하게의성의래어 가운데 어떤 단어는 그 어원을 명확히 밝힐 수없기  때문",
    "output": "의성의래어에  접미사 ‘ㅡ이’가 붙어서  단어가  이루어절 때  어근과 접미사를 밝혀 적지  않는 까닭은 주요하게의성의래어 가운데 어떤 단어는 그 어원을 명확히 밝힐 수없기  때문이다.  그것이  의성의래어에서 온 것인지  아니면원래부터 한 어근으로 된 것인지 가려내기  어려운 경우가적지  않다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1675,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들면  ‘두루미’를 “두룸두룸” 한다고,  ‘제비’를“접접”, ‘파리’를 “짤짤” 한다고 그 소리를 본딴 것인지원래부터 한 어근으로 되어있는 것인지  그 어원을 밝혀내기  어",
    "output": "례를 들면  ‘두루미’를 “두룸두룸” 한다고,  ‘제비’를“접접”, ‘파리’를 “짤짤” 한다고 그 소리를 본딴 것인지원래부터 한 어근으로 되어있는 것인지  그 어원을 밝혀내기  어렵다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1676,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그 다음으로 의성의래어에서  어근과 접미사를 각각 밝혀 적는다면 서사생활에서  많은 불편과 혼동을 초래할 수있다.  그리고 ‘피꼬리’,  ‘매미’를 ‘피꿀이’,  ‘맴이’로 적",
    "output": "그 다음으로 의성의래어에서  어근과 접미사를 각각 밝혀 적는다면 서사생활에서  많은 불편과 혼동을 초래할 수있다.  그리고 ‘피꼬리’,  ‘매미’를 ‘피꿀이’,  ‘맴이’로 적",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1677,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "는다면 ‘너구리’를 ‘너굴이’로,  ‘개미’를 ‘갬이’로 혼동하여  적을 수 있다.  또한 ‘귀뚜라미’는 “귀뚤귀뚤”한다고하면서  ‘귀뚤’을 어근으로 보고 ‘아미’를 접미사로 보아",
    "output": "는다면 ‘너구리’를 ‘너굴이’로,  ‘개미’를 ‘갬이’로 혼동하여  적을 수 있다.  또한 ‘귀뚜라미’는 “귀뚤귀뚤”한다고하면서  ‘귀뚤’을 어근으로 보고 ‘아미’를 접미사로 보아‘귀뚤아미’로 표기할 수 있는 사람들이  있을 수 있는가 하면 또 어떤 사람들은 “귀뚜람귀뚜람”운다고 ‘귀뚜람’까지어근으로 보고 거기에  접미사 ‘—이’를 붙여  ‘귀뚜람이’라고 적는 사람들이  있을 수 있다.  이처럼  허다한 시끄러움과 혼동을 초래할 필요  없이  소리  나는 내로 적는  것이합리하다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1682,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "셋째,  어떤 토나 ‘하다’가 붙어서 단어를 이루는 일이없는 어근에 접미사 ‘—이’,  ‘—아기’,  ‘—애기’,  ‘—어기(에기)’가 붙어서 된 명사나 부사.",
    "output": "셋째,  어떤 토나 ‘하다’가 붙어서 단어를 이루는 일이없는 어근에 접미사 ‘—이’,  ‘—아기’,  ‘—애기’,  ‘—어기(에기)’가 붙어서 된 명사나 부사.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1683,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘갑자기’는 ‘갑작이’로 적지  않는다.  왜냐하면  ‘갑작스럽다,  갑작스레’라고는 하여도  ‘갑작하다’라고는 하지않기  때문이다.  그리고 ‘술며시’를 ‘술몃이’로 적지  않고",
    "output": "‘갑자기’는 ‘갑작이’로 적지  않는다.  왜냐하면  ‘갑작스럽다,  갑작스레’라고는 하여도  ‘갑작하다’라고는 하지않기  때문이다.  그리고 ‘술며시’를 ‘술몃이’로 적지  않고‘일찌기’를 ‘일찍’으로는 쓰나 ‘일찍이’로 적지  않는 것은어근 ‘술몃,  일찍’에  ‘하다’가 붙는 일이  없으며  또한 토가 붙어서 단어로 쓰이는 일이  없기  때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1685,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘가맣다’는 형용사 ‘감다’의  어근 ‘감ㅡ’에  접미사‘ㅡ앟’이 붙어서  이루어진 것이고 형용사 ‘써느렇다’는 어근 ‘써늘ㅡ’에 접미사 ‘ㅡ엱’이 붙어  이루어진 것이다.",
    "output": "‘가맣다’는 형용사 ‘감다’의  어근 ‘감ㅡ’에  접미사‘ㅡ앟’이 붙어서  이루어진 것이고 형용사 ‘써느렇다’는 어근 ‘써늘ㅡ’에 접미사 ‘ㅡ엱’이 붙어  이루어진 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1693,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단어  ‘보드랍다’는 의성의태어  ‘보들ㅡ보들보들’의  어근 ‘보들’에 접미사 ‘ㅡ압’이 붙어서  이루어진 것이고 ‘어지럽다’는 어근 ‘어질’에  접미사 ‘ㅡ엽’이  붙어서  이루",
    "output": "단어  ‘보드랍다’는 의성의태어  ‘보들ㅡ보들보들’의  어근 ‘보들’에 접미사 ‘ㅡ압’이 붙어서  이루어진 것이고 ‘어지럽다’는 어근 ‘어질’에  접미사 ‘ㅡ엽’이  붙어서  이루어진 것이며  ‘간지럽다’는 ‘간절ㅡ간절간절ㅡ간절거리다’의어근 ‘간절’에  접미사 ‘ㅡ업’이 붙어서  이루어진  것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1711,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단어  ‘우습다’도 ‘웃다’의  어근 ‘웃ㅡ’에  접미사 ‘ㅡ읍’이  붙어서  이루어진  것이다.",
    "output": "단어  ‘우습다’도 ‘웃다’의  어근 ‘웃ㅡ’에  접미사 ‘ㅡ읍’이  붙어서  이루어진  것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1712,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이상의 두 경우에  어근과 접미사를 모두 밝혀 적지  않는다.",
    "output": "이상의 두 경우에  어근과 접미사를 모두 밝혀 적지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1713,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그것은 접미사 ‘ㅡ앙(ㅡ옇)’또는  ‘ㅡ압(ㅡ업)’,  ‘ㅡ읍’이  붙어서  이루어진 형용사인 경우에 그 어근과 접미사를 각각 밝혀 적기  어려운 경우가 있기  때문이다.",
    "output": "그것은 접미사 ‘ㅡ앙(ㅡ옇)’또는  ‘ㅡ압(ㅡ업)’,  ‘ㅡ읍’이  붙어서  이루어진 형용사인 경우에 그 어근과 접미사를 각각 밝혀 적기  어려운 경우가 있기  때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1714,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "례를 들면 ‘거멓다’는 ‘검(다)+옇다’에서,  ‘씨느랗다’는 ‘씨늘(하다)+앟다’에서  그 어근을 찾아볼 수  있지만‘까맣다’는 ‘깜앟다’에서  ‘깜’이  어근으로 되기  어렵다",
    "output": "례를 들면 ‘거멓다’는 ‘검(다)+옇다’에서,  ‘씨느랗다’는 ‘씨늘(하다)+앟다’에서  그 어근을 찾아볼 수  있지만‘까맣다’는 ‘깜앟다’에서  ‘깜’이  어근으로 되기  어렵다.또 ‘노랗다, 파랗다,  벌겋다’에서  ‘놀’,  ‘팔’, ‘뻥’이 각각해당한 단어의  어근으로 되기  어렵다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1715,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "보아야 한다.  ‘하다’를 붙일 수 있는 것은 어근의 끝음절받침이  ‘ㅅ,  ㄱ’으로 끝나지  않는 한 ‘ㅡ히’로 적는 것을원칙으로 하고 ‘하다’를 붙일 수 없는 것은 ‘ㅡ이’로 ",
    "output": "보아야 한다.  ‘하다’를 붙일 수 있는 것은 어근의 끝음절받침이  ‘ㅅ,  ㄱ’으로 끝나지  않는 한 ‘ㅡ히’로 적는 것을원칙으로 하고 ‘하다’를 붙일 수 없는 것은 ‘ㅡ이’로 적는것을 원칙으로 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1723,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "첫째, 어근의 끝음절이  받침  ‘ㅅ,  ㄱ’을 제외한 기타의  받침이거나 모음으로 끝난 경우에는 ‘ㅡ히’로 적는다.",
    "output": "첫째, 어근의 끝음절이  받침  ‘ㅅ,  ㄱ’을 제외한 기타의  받침이거나 모음으로 끝난 경우에는 ‘ㅡ히’로 적는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1726,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "둘째, 어근의 끝음절이  받침  ‘ㅅ’으로 끝난 경우에는‘ㅡ이’로 적는다.",
    "output": "둘째, 어근의 끝음절이  받침  ‘ㅅ’으로 끝난 경우에는‘ㅡ이’로 적는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1728,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "그러나 뚜렷이  ‘ㅡ히’로 발음되는 다음과 같은 것은‘ㅡ히’로 적는다.  (어근이 한자어로 이루어진 경우이다.)",
    "output": "그러나 뚜렷이  ‘ㅡ히’로 발음되는 다음과 같은 것은‘ㅡ히’로 적는다.  (어근이 한자어로 이루어진 경우이다.)",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1739,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "동음이의어적인 어근을 가진 다음과 같은 부사들은 맞춤법에서 틀리기 쉬우므로 잘 갈라서 써야 한다.",
    "output": "동음이의어적인 어근을 가진 다음과 같은 부사들은 맞춤법에서 틀리기 쉬우므로 잘 갈라서 써야 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1740,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "왼쪽의 부사들은 단음절의 명사가 겹쳐서  이루어진 어근으로서  이런 어근에는 ‘하다’가 붙어서 형용사를 이루지못한다.  오른쪽의 부사들은 그 어근에 ‘하다’가 붙어서  형용사로 될",
    "output": "왼쪽의 부사들은 단음절의 명사가 겹쳐서  이루어진 어근으로서  이런 어근에는 ‘하다’가 붙어서 형용사를 이루지못한다.  오른쪽의 부사들은 그 어근에 ‘하다’가 붙어서  형용사로 될 수 있다.  그려므로 어근에  ‘하다’를 붙여보아형용사로 되는 것은 접미사 ‘ㅡ히’를 붙이고 형용사로 되지  않는 것은 접미사 ‘ㅡ이’를 붙이면 된다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1747,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단어는 형태소로 이루어지는데 단어를 이루는 형태소는 그 기능이나 결합관계에 따라 어근, 접사, 어간으로 나눈다.  어근은 단어를 이루는 핵심요소이며  접사는 어근의앞이나 뒤에 첨가",
    "output": "단어는 형태소로 이루어지는데 단어를 이루는 형태소는 그 기능이나 결합관계에 따라 어근, 접사, 어간으로 나눈다.  어근은 단어를 이루는 핵심요소이며  접사는 어근의앞이나 뒤에 첨가되여 새로운 의미를 보충하며  새로운 단어를 만드는 구실을 한다.  어근의  앞에 붙는 접사를 접두사라 하고 뒤에 붙는 접사를 접미사라 한다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1855,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접두사와 접미사는 홀로 쓰이지 못하기에 어근의  앞이거나 뒤에 붙여쓴다.",
    "output": "접두사와 접미사는 홀로 쓰이지 못하기에 어근의  앞이거나 뒤에 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 1856,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "어간은 줄기라고도 하는데  일반적으로 어근과 접사가결합된 것이거나 어근들이 합성된 것이다.",
    "output": "어간은 줄기라고도 하는데  일반적으로 어근과 접사가결합된 것이거나 어근들이 합성된 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "어간은",
        "줄기라고도",
        "하는데"
      ],
      "paragraph_index": 2042,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "어간은 줄기라고도 하는데  일반적으로 어근과 접사가결합된 것이거나 어근들이 합성된 것이다.",
    "output": "어간은 줄기라고도 하는데  일반적으로 어근과 접사가결합된 것이거나 어근들이 합성된 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2042,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "문장의 ‘날씨’,  ‘매우’,  ‘좋-’,  ‘꽃나비’,  ‘아름-’은 모두 어근이다.",
    "output": "문장의 ‘날씨’,  ‘매우’,  ‘좋-’,  ‘꽃나비’,  ‘아름-’은 모두 어근이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2043,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "어간 또는 줄기라고 하는 것은 한 단어가 지닌 고유의성분 전체를 일컫는다.  일반적으로 어근과 접사를 모두 합친 것이  어간이다.  한 단어가 어근 하나만으로 이루어진경우에는 그 ",
    "output": "어간 또는 줄기라고 하는 것은 한 단어가 지닌 고유의성분 전체를 일컫는다.  일반적으로 어근과 접사를 모두 합친 것이  어간이다.  한 단어가 어근 하나만으로 이루어진경우에는 그 어근 자체가 어간이며  한 어근에  딴 어근이결합되여  이루어진 날말은 그 결합체가 어간이 된다.  어간은 적어도 한 어근을 지니는 구성체인데  실질적으로 단어자체를 가리키는 것이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2044,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "첫째, 어간은 접두사—어근—접미사로 이루어질 수 있다.",
    "output": "첫째, 어간은 접두사—어근—접미사로 이루어질 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2045,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "둘째, 어간은 접두사—어근으로 이루어질 수 있다.",
    "output": "둘째, 어간은 접두사—어근으로 이루어질 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2046,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "셋째, 어간은 어근—접미사로 이루어질 수 있다.",
    "output": "셋째, 어간은 어근—접미사로 이루어질 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2047,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "넷째, 어간은 하나의 어근으로 이루어질 수 있다.",
    "output": "넷째, 어간은 하나의 어근으로 이루어질 수 있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2053,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "어근이 둘 이상이고 거기에 접사가 붙는 경우도 더러있으므로 어간의 구조는 상당히 복잡할 수 있다.  례를 들면‘헛탕치기’, ‘헛기침소리’, ‘술래잠기’등은 두 어근에접사가 붙어서 ",
    "output": "어근이 둘 이상이고 거기에 접사가 붙는 경우도 더러있으므로 어간의 구조는 상당히 복잡할 수 있다.  례를 들면‘헛탕치기’, ‘헛기침소리’, ‘술래잠기’등은 두 어근에접사가 붙어서  이루어진 어간이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2056,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "접사의 첨가로 파생되는 단어는 일반적으로 기본 류형곧‘(접두사)어근(접미사)’을 바탕으로 하여  이루어진다.",
    "output": "접사의 첨가로 파생되는 단어는 일반적으로 기본 류형곧‘(접두사)어근(접미사)’을 바탕으로 하여  이루어진다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 2057,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "접사의 첨가로 파생되는 단어는 일반적으로 기본 류형곧‘(접두사)어근(접미사)’을 바탕으로 하여  이루어진다.",
    "output": "접사의 첨가로 파생되는 단어는 일반적으로 기본 류형곧‘(접두사)어근(접미사)’을 바탕으로 하여  이루어진다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2057,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합",
    "output": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합된 단어를 복합어라 부른다.  복합어는다시 어근에 파생접사가 덧붙어서 된 파생어와 둘 또는 그보다 많은 어근이  어울려  어간을 이룬 합성어로 가를 수있다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "단어는",
        "형태소의",
        "어울림관계에"
      ],
      "paragraph_index": 2058,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합",
    "output": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합된 단어를 복합어라 부른다.  복합어는다시 어근에 파생접사가 덧붙어서 된 파생어와 둘 또는 그보다 많은 어근이  어울려  어간을 이룬 합성어로 가를 수있다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 2058,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합",
    "output": "단어는 각 형태소의 어울림관계에 따라 몇가지 구조류형으로 나누어 볼 수 있다.  어간이 한 형태조만으로 이루어진 단어를 단순어 또는 단일어라 하고 둘 또는 그보다많은 형태소가 결합된 단어를 복합어라 부른다.  복합어는다시 어근에 파생접사가 덧붙어서 된 파생어와 둘 또는 그보다 많은 어근이  어울려  어간을 이룬 합성어로 가를 수있다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2058,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "단순어는 그 어간이 한 형태소로 된 것이다.  단순어는어근, 어간과 단어가 서로 같은 형태로 되여있다.  그러므로 뼈여쓰기가 제기되지  않는다.",
    "output": "단순어는 그 어간이 한 형태소로 된 것이다.  단순어는어근, 어간과 단어가 서로 같은 형태로 되여있다.  그러므로 뼈여쓰기가 제기되지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2060,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘가’의 례는 어근, 어간 및 단어  형태가 같은 단순어이고 ‘나’의 례는 용언의 경우로서 어미  ‘-다’를 빼면 단일 어근인 단순어임을 알 수 있다. 단순어는 형태로 볼 때",
    "output": "‘가’의 례는 어근, 어간 및 단어  형태가 같은 단순어이고 ‘나’의 례는 용언의 경우로서 어미  ‘-다’를 빼면 단일 어근인 단순어임을 알 수 있다. 단순어는 형태로 볼 때",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2061,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 ",
    "output": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 접두사가 덧붙는 ‘접두파생법’과 어근에 접미사가 덧붙는 ‘접미파생법’이  있다.  그 밖에 접두사와 접미사가 각각 어근에 어울려서  이루어지는 ‘량면파생법’도 있고 뒤따르는 떤 어근과 합성어를 이루는 ‘파생합성법’도있다.  파생어에도 띄여쓰기가 제기되지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "파생어는",
        "어근에",
        "접사가"
      ],
      "paragraph_index": 2068,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 ",
    "output": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 접두사가 덧붙는 ‘접두파생법’과 어근에 접미사가 덧붙는 ‘접미파생법’이  있다.  그 밖에 접두사와 접미사가 각각 어근에 어울려서  이루어지는 ‘량면파생법’도 있고 뒤따르는 떤 어근과 합성어를 이루는 ‘파생합성법’도있다.  파생어에도 띄여쓰기가 제기되지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 2068,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 ",
    "output": "파생어는 어근에  접사가 덧붙어  이루어진 단어이다.파생어는 어근에 하나 이상의 접사가 덧붙어서  새롭게  형성된 단어이다.  조선어  접사에는 접두사와 접미사가 있으므로 어근에 접두사가 덧붙는 ‘접두파생법’과 어근에 접미사가 덧붙는 ‘접미파생법’이  있다.  그 밖에 접두사와 접미사가 각각 어근에 어울려서  이루어지는 ‘량면파생법’도 있고 뒤따르는 떤 어근과 합성어를 이루는 ‘파생합성법’도있다.  파생어에도 띄여쓰기가 제기되지  않는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2068,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下派生词规则",
    "input": "이  밖에도 조선말에는 혼종파생어라는 단어가 있는데그것은 한자어  어근에 고유어 접사가 붙거나 고유어  어근에 한자어 접사가 결합되여  이루어진다.",
    "output": "이  밖에도 조선말에는 혼종파생어라는 단어가 있는데그것은 한자어  어근에 고유어 접사가 붙거나 고유어  어근에 한자어 접사가 결합되여  이루어진다.",
    "metadata": {
      "category": "wordformation",
      "type": "derivation",
      "paragraph_index": 2076,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "이  밖에도 조선말에는 혼종파생어라는 단어가 있는데그것은 한자어  어근에 고유어 접사가 붙거나 고유어  어근에 한자어 접사가 결합되여  이루어진다.",
    "output": "이  밖에도 조선말에는 혼종파생어라는 단어가 있는데그것은 한자어  어근에 고유어 접사가 붙거나 고유어  어근에 한자어 접사가 결합되여  이루어진다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2076,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어란 두개나 그보다 많은 어근이  서로 결합하여새로운 한 단어로서의 의미기능을 드러내는 것을 일컫는다.",
    "output": "합성어란 두개나 그보다 많은 어근이  서로 결합하여새로운 한 단어로서의 의미기능을 드러내는 것을 일컫는다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어란",
        "두개나",
        "그보다"
      ],
      "paragraph_index": 2078,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "합성어란 두개나 그보다 많은 어근이  서로 결합하여새로운 한 단어로서의 의미기능을 드러내는 것을 일컫는다.",
    "output": "합성어란 두개나 그보다 많은 어근이  서로 결합하여새로운 한 단어로서의 의미기능을 드러내는 것을 일컫는다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2078,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "‘가’의례는 두개 어근의 결합으로 이루어졌고 ‘나’의례는 세개  어근의  결합으로 이루어진 합성어이다.  하기에",
    "output": "‘가’의례는 두개 어근의 결합으로 이루어졌고 ‘나’의례는 세개  어근의  결합으로 이루어진 합성어이다.  하기에",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "의례는",
        "두개",
        "어근의"
      ],
      "paragraph_index": 2079,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "‘가’의례는 두개 어근의 결합으로 이루어졌고 ‘나’의례는 세개  어근의  결합으로 이루어진 합성어이다.  하기에",
    "output": "‘가’의례는 두개 어근의 결합으로 이루어졌고 ‘나’의례는 세개  어근의  결합으로 이루어진 합성어이다.  하기에",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2079,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "합성어를 이루고 있는 여러 단위를 띄여쓰는가 아니면 붙여쓰는가 하는 문제가 제기된다.",
    "output": "합성어를 이루고 있는 여러 단위를 띄여쓰는가 아니면 붙여쓰는가 하는 문제가 제기된다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성어를",
        "이루고",
        "있는"
      ],
      "paragraph_index": 2084,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "여러 단위들이  결합하여 합성어를 이룰 때 그 단위들은 붙여쓴다.",
    "output": "여러 단위들이  결합하여 합성어를 이룰 때 그 단위들은 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "여러",
        "단위들이",
        "결합하여"
      ],
      "paragraph_index": 2085,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체",
    "output": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체가 하나의 단어로 되기에 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "명사는",
        "명사",
        "아니라"
      ],
      "paragraph_index": 2100,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체",
    "output": "명사는 명사 뿐 아니라 기타 다른 품사들과 결합하여또 다른 새로운 단어를 만든다.  이  때 쓰이는 단어조성수법이 바로 어근합성법이다.  어근합성법에 의하여 만들어진단어는 그 전체가 하나의 단어로 되기에 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2100,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "‘우리말’,  ‘우리글’은 합성어로 보아 붙여쓰고 ‘우리나라’는 구로 보아 띄여쓴다.",
    "output": "‘우리말’,  ‘우리글’은 합성어로 보아 붙여쓰고 ‘우리나라’는 구로 보아 띄여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "우리말",
        "우리글",
        "합성어로"
      ],
      "paragraph_index": 2600,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법",
    "output": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법이다.  따라서  띄여쓰기를 어떻게  해야 하는가 하는 문제가 제기된다.  왜냐하면 총칙에 “조선말은단어를 단위로 하여 띄여쓰는 것을 원칙으로 한다.”고 했기 때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "서로",
        "다른",
        "품사들이"
      ],
      "paragraph_index": 2658,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법",
    "output": "서로 다른 품사들이  결합되여  새로운 동사를 조성할수 있다.  동사의 단어조성에서 가장 중요한 수법의 하나가둘 또는 그 이상의 어근들이 결합하여 새로운 단어를 조성하는 어근합성법이다.  따라서  띄여쓰기를 어떻게  해야 하는가 하는 문제가 제기된다.  왜냐하면 총칙에 “조선말은단어를 단위로 하여 띄여쓰는 것을 원칙으로 한다.”고 했기 때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2658,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "output": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "붙여쓴다",
        "왜냐하면",
        "어근합성법에"
      ],
      "paragraph_index": 2664,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "output": "붙여쓴다.  왜냐하면 어근합성법에 의하여 만들어진 단어는하나의 단어로 되기 때문이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2664,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 ",
    "output": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 품사들이 직접 어울려서 하나의 형용사로 된것은 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "형용사도",
        "동사와",
        "마찬가지로"
      ],
      "paragraph_index": 2672,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 ",
    "output": "형용사도 동사와 마찬가지로 서로 다른 품사들이  결합되여 새로운 형용사를 조성할 수 있다.  어근합성법에 의하여 만들어진 단어도 하나의 단어로 되므로 붙여써야 한다.즉 서로 다른 품사들이 직접 어울려서 하나의 형용사로 된것은 붙여쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2672,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "관형사는 대상의 특성을 규정하는 품사로서 하나의 단어이고 접두사는 어근에 첨가되여 새로운 의미를 부여하면서 새로운 단어를 만드는 형태소이다.",
    "output": "관형사는 대상의 특성을 규정하는 품사로서 하나의 단어이고 접두사는 어근에 첨가되여 새로운 의미를 부여하면서 새로운 단어를 만드는 형태소이다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2692,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "둘째, 두 형태소 사이에 휴지를 둘 수 있는가 없는가를 보아야 한다.  관형사는 자립적인 악센트를 가지고 다음단어와의 사이에 일정한 휴지가 오면서 발음되나 접두사적형태는 그 자체가",
    "output": "둘째, 두 형태소 사이에 휴지를 둘 수 있는가 없는가를 보아야 한다.  관형사는 자립적인 악센트를 가지고 다음단어와의 사이에 일정한 휴지가 오면서 발음되나 접두사적형태는 그 자체가 하나의 단어로 되지 못하기에 자립적인악센트를 가지지 못하고 다음에 오는 명사적 어근과 이어서 발음된다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2705,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "셋째, 두 형태소 사이에 다른 말을 끼울 수 있는가 없는가를 보아야 한다.  관형사와 명사 사이에는 다른 말을끼울 수 있지만 접두사적 형태와 명사적 어근 사이에는 다른 말을 끼울 ",
    "output": "셋째, 두 형태소 사이에 다른 말을 끼울 수 있는가 없는가를 보아야 한다.  관형사와 명사 사이에는 다른 말을끼울 수 있지만 접두사적 형태와 명사적 어근 사이에는 다른 말을 끼울 수 없다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2706,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "5) 합성명사 앞에 쓰이는 관형사는 일반적으로 뒤의단위와 띄어쓴다.",
    "output": "5) 합성명사 앞에 쓰이는 관형사는 일반적으로 뒤의단위와 띄어쓴다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "합성명사",
        "앞에",
        "쓰이는"
      ],
      "paragraph_index": 2722,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "output": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "동사나",
        "형용사와",
        "마찬가지로"
      ],
      "paragraph_index": 2887,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下词根活用规则",
    "input": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "output": "동사나 형용사와 마찬가지로 어근합성법으로 이루어진부사들이  적지  않다.  이럴 때에 띄여쓰기를 어떻게  해야하는가 하는 문제가 제기된다.",
    "metadata": {
      "category": "wordformation",
      "type": "root",
      "paragraph_index": 2887,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "첫째, 복합문에서 절속로가 없이 문장들이 이어질 때단순문 사이에 찍는냐.",
    "output": "첫째, 복합문에서 절속로가 없이 문장들이 이어질 때단순문 사이에 찍는냐.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "첫째",
        "복합문에서",
        "절속로가"
      ],
      "paragraph_index": 3022,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "삐문에서 보다싶이 접속토 없이 쉽표에 의하여 단순푼들이 이어지면서 복합푼을 이룬 경수에 매 단순푼슬 갈라주기 위햐여 숮표플  찍었.   복합문에 서접속토 가없 는후에는 쉽표에 의하",
    "output": "삐문에서 보다싶이 접속토 없이 쉽표에 의하여 단순푼들이 이어지면서 복합푼을 이룬 경수에 매 단순푼슬 갈라주기 위햐여 숮표플  찍었.   복합문에 서접속토 가없 는후에는 쉽표에 의하여 난순푼들 사이의 련계가 맺어진냐.이 빼 쉽표를 찍지 않으면 매 단순문을 구분하기 어려우며난순문들 사이플 억향으로 이어주기도 어려운   경수 가니. 따라서 복합문에서의 매 난순문을 이어주는 접속토가없냐편 그 사이에 쉽표를 찍어서 구분한냐.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "삐문에서",
        "보다싶이",
        "접속토"
      ],
      "paragraph_index": 3023,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "접속토이다.  접속토‘요’뒤에 쉼표를 찍어서 단순문의 경계를 구분하여줄 뿐만 아니라 억양으로 이들 사이를 이어주면서 복합문을 이루었음을 보여준다.",
    "output": "접속토이다.  접속토‘요’뒤에 쉼표를 찍어서 단순문의 경계를 구분하여줄 뿐만 아니라 억양으로 이들 사이를 이어주면서 복합문을 이루었음을 보여준다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "접속토이다",
        "접속토",
        "뒤에"
      ],
      "paragraph_index": 3030,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下复合词规则",
    "input": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고",
    "output": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고 그 전체로 하나의 복합문을 구성하였다.그러므로 우의 폐문은 마침표로 표시된 부분에 가서 문장이 완전히 끝난 것으로 된다.",
    "metadata": {
      "category": "wordformation",
      "type": "compound",
      "examples": [
        "글에서",
        "종결토",
        "끝난"
      ],
      "paragraph_index": 3033,
      "source_category": "wordformation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "제15항 묵음표(소괄호, 중괄호, 내괄호)( ( ),〔 〕, { } )",
    "output": "제15항 묵음표(소괄호, 중괄호, 내괄호)( ( ),〔 〕, { } )",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 197,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "제23항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.  조선문자로 단위를 달",
    "output": "제23항 수사는 아라비아수자로 적는 것을 원칙으로 하되 정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.  조선문자로 단위를 달아줄 경우거나 순 조선문자로 적을 경우에는 ‘만,  억, 조’등의 단위에서 띄여쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 2564,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "새 규범에서는 “정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다붙여쓴다.”를 더 보태고 2007년의 규범에서의 “수사가 완전명사와 어울리",
    "output": "새 규범에서는 “정수인 경우 왼쪽으로 가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다붙여쓴다.”를 더 보태고 2007년의 규범에서의 “수사가 완전명사와 어울리는 경우에는 띄여쓴다.  … 그러나 단위명사와 어울리는 경우에는 붙여쓴다.”는 내용을 삭제하였다.완전명사는 하나의 자립적인 단어이므로 “조선말은 단어를단위로 하여 띄여쓰는 것을 원칙으로 한다.”는 총칙에 따",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 2565,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.",
    "output": "수사는 아라비아수자로 적을 때 정수인 경우 왼쪽으로가면서 세개 단위씩 쉼표를 찍어주고 소수인 경우 오른쪽으로 가면서 다 붙여쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 2572,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성",
    "output": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성 요구가 더욱 높아지고 있는 시점에서일부 문장부호 례하면 마침표, 쉼표, 물음표, 느낌표, 가운테점, 두점의 띄여쓰기에 대하여 간단히 규정하였다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2908,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성",
    "output": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성 요구가 더욱 높아지고 있는 시점에서일부 문장부호 례하면 마침표, 쉼표, 물음표, 느낌표, 가운테점, 두점의 띄여쓰기에 대하여 간단히 규정하였다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 2908,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성",
    "output": "종전의 규범에서는 문장부호의 띄여쓰기를 규범하지않았다.  그러나 시대의 발전과 더불어  언어도 변화하게 되고 언어전산화의 발전과 더불어 조선말의 맞춤법, 띄여쓰기 등에 대한 과학성 요구가 더욱 높아지고 있는 시점에서일부 문장부호 례하면 마침표, 쉼표, 물음표, 느낌표, 가운테점, 두점의 띄여쓰기에 대하여 간단히 규정하였다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 2908,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "이 때 마침표를 찍으면 문장이 끝났음을 보여준다.  종결토로 끝난 문장에서도 마침표를 치면 문장이 끝났음을더 직관적으로 보여주는 데 그 의의가 있다.",
    "output": "이 때 마침표를 찍으면 문장이 끝났음을 보여준다.  종결토로 끝난 문장에서도 마침표를 치면 문장이 끝났음을더 직관적으로 보여주는 데 그 의의가 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2942,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "그러나 문장은 어느 때나 종결토거나 마침표를 쳐서만끝나는 것이 아니다.",
    "output": "그러나 문장은 어느 때나 종결토거나 마침표를 쳐서만끝나는 것이 아니다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2943,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "례문의 “돌격!”에서는 마침표를 쓰지  않고 느낌표를쳐서 하나의 단어가 문장으로 끝났음을 나타내였다.  이와같이 느낌표나 물음표로 끝난 것은 그것으로도 문장이 끝",
    "output": "례문의 “돌격!”에서는 마침표를 쓰지  않고 느낌표를쳐서 하나의 단어가 문장으로 끝났음을 나타내였다.  이와같이 느낌표나 물음표로 끝난 것은 그것으로도 문장이 끝",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2944,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "례문의 “돌격!”에서는 마침표를 쓰지  않고 느낌표를쳐서 하나의 단어가 문장으로 끝났음을 나타내였다.  이와같이 느낌표나 물음표로 끝난 것은 그것으로도 문장이 끝",
    "output": "례문의 “돌격!”에서는 마침표를 쓰지  않고 느낌표를쳐서 하나의 단어가 문장으로 끝났음을 나타내였다.  이와같이 느낌표나 물음표로 끝난 것은 그것으로도 문장이 끝",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 2944,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "났음을 표시하므로 마침표를 다시  치지  않는다.",
    "output": "났음을 표시하므로 마침표를 다시  치지  않는다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2950,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "넷째, 대목이나 장과 절을 가르는 부호에 소괄호, 중괄호, 대괄호나 동그라미가 없을 때에는 그 부호 뒤에 찍는다.",
    "output": "넷째, 대목이나 장과 절을 가르는 부호에 소괄호, 중괄호, 대괄호나 동그라미가 없을 때에는 그 부호 뒤에 찍는다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 2953,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "다섯째, 표제어나 표어에는 마침표를 쓰지  않는다.",
    "output": "다섯째, 표제어나 표어에는 마침표를 쓰지  않는다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 2954,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "반두점은 한 문장에서 쉼표로 구분된 말이  여러개  잇달아있을 때 더 크게 묶어지는 단위 사이에 찍을 수 있다.",
    "output": "반두점은 한 문장에서 쉼표로 구분된 말이  여러개  잇달아있을 때 더 크게 묶어지는 단위 사이에 찍을 수 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 2988,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "빗금은 아래와 같은 세가지 경우에 찍는다.",
    "output": "빗금은 아래와 같은 세가지 경우에 찍는다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3000,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "쉼표는 ㅁ음과 같은 경수에 찍는냐.",
    "output": "쉼표는 ㅁ음과 같은 경수에 찍는냐.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3021,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "접속토이다.  접속토‘요’뒤에 쉼표를 찍어서 단순문의 경계를 구분하여줄 뿐만 아니라 억양으로 이들 사이를 이어주면서 복합문을 이루었음을 보여준다.",
    "output": "접속토이다.  접속토‘요’뒤에 쉼표를 찍어서 단순문의 경계를 구분하여줄 뿐만 아니라 억양으로 이들 사이를 이어주면서 복합문을 이루었음을 보여준다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3030,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고",
    "output": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고 그 전체로 하나의 복합문을 구성하였다.그러므로 우의 폐문은 마침표로 표시된 부분에 가서 문장이 완전히 끝난 것으로 된다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 3033,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고",
    "output": "이 글에서 종결토‘다’로 끝난 각각의 부분이 하나의완전한 문장을 구성한 것이  아니다.  종결토 뒤에  쉼표를찍은 부분은 하나의 문장 안에서  여러개 단위들을 상대적으로 갈라보이고 그 전체로 하나의 복합문을 구성하였다.그러므로 우의 폐문은 마침표로 표시된 부분에 가서 문장이 완전히 끝난 것으로 된다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3033,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "그리고 일반적으로 종결토가 오면 문장이 끝난 것으로되지만 종결토 뒤에 마침표를 찍지 않고 쉼표를 찍게 되면억양이  맺음억양으로 되지  않고 이음억양으로 되면서 뒤에오는 단위와 밀접",
    "output": "그리고 일반적으로 종결토가 오면 문장이 끝난 것으로되지만 종결토 뒤에 마침표를 찍지 않고 쉼표를 찍게 되면억양이  맺음억양으로 되지  않고 이음억양으로 되면서 뒤에오는 단위와 밀접한 런계를 갖게 된다.  따라서 종결토가온다 하더라도 쉼표로 런결된 것은 그 런결된 전체의 단위가 하나의 문장으로 되므로 이 때 문장부호 쉼표는 문장으로 끝나지  않은 단위임을 뚜렷이 보여주는 역할을 한다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 3034,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "그리고 일반적으로 종결토가 오면 문장이 끝난 것으로되지만 종결토 뒤에 마침표를 찍지 않고 쉼표를 찍게 되면억양이  맺음억양으로 되지  않고 이음억양으로 되면서 뒤에오는 단위와 밀접",
    "output": "그리고 일반적으로 종결토가 오면 문장이 끝난 것으로되지만 종결토 뒤에 마침표를 찍지 않고 쉼표를 찍게 되면억양이  맺음억양으로 되지  않고 이음억양으로 되면서 뒤에오는 단위와 밀접한 런계를 갖게 된다.  따라서 종결토가온다 하더라도 쉼표로 런결된 것은 그 런결된 전체의 단위가 하나의 문장으로 되므로 이 때 문장부호 쉼표는 문장으로 끝나지  않은 단위임을 뚜렷이 보여주는 역할을 한다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3034,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "여기에서  ‘선생님’은 호칭어,  ‘간단히 말하면’은 삽입어이고 ‘아’는 감동어, ‘용기’는 제지어이다.  이것들은 문장 안에서  어느 한 성분과만 런계되여있는 것이  아니라 상대",
    "output": "여기에서  ‘선생님’은 호칭어,  ‘간단히 말하면’은 삽입어이고 ‘아’는 감동어, ‘용기’는 제지어이다.  이것들은 문장 안에서  어느 한 성분과만 런계되여있는 것이  아니라 상대적으로 떨어져서 뒤에 오는 전체 문장과 관계를 발생한다.  이런 독립적인 성분을 문장에서의 다른 성분들과 갈라보기 위하여 그 뒤에 쉼표를 찍는다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3043,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "그리고 ‘첫째로, 둘째로, 셋째로…’, ‘끝으로, 간략해말하면, 다시 말하면, 마지막으로, 종합하여 말하면, 다음으로…’등은 삽입어로서 뒤에 오는 성분들과의 사이를 갈라보기 위하여",
    "output": "그리고 ‘첫째로, 둘째로, 셋째로…’, ‘끝으로, 간략해말하면, 다시 말하면, 마지막으로, 종합하여 말하면, 다음으로…’등은 삽입어로서 뒤에 오는 성분들과의 사이를 갈라보기 위하여 쉼표를 찍는다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3044,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "쉼표는 이와 같이  같은 자격으로 죽 들어서  이야기할때 그 단위들이  섞갈리지  않도록 갈라주기 위하여  친다.",
    "output": "쉼표는 이와 같이  같은 자격으로 죽 들어서  이야기할때 그 단위들이  섞갈리지  않도록 갈라주기 위하여  친다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3057,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "이 밖에  몇개의 단위들을 같은 자격으로 나란히 놓고‘기타’, ‘그 밖에’, ‘따위’, ‘등’, ‘등등’이 왔을 때 앞에 놓인 단위와 이들 사이에 쉼표를 찍지 않는다. 물론 이런 ",
    "output": "이 밖에  몇개의 단위들을 같은 자격으로 나란히 놓고‘기타’, ‘그 밖에’, ‘따위’, ‘등’, ‘등등’이 왔을 때 앞에 놓인 단위와 이들 사이에 쉼표를 찍지 않는다. 물론 이런 단위",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3059,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "물음표는 이러저러하게 물음과 관련되는 문장에 쓰인다.  물음표는 문장이 끝난 뒤에만 치는데 그 구체적 사용규정은 다음과 같다.",
    "output": "물음표는 이러저러하게 물음과 관련되는 문장에 쓰인다.  물음표는 문장이 끝난 뒤에만 치는데 그 구체적 사용규정은 다음과 같다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3067,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 ",
    "output": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 훌륭한 기둥감이냐”에서는 꼭 물음표를 쳐야 할 리유가 없다.  느낌의 뜻으로 강한 어조가 동반될 때에는 느낌표를 칠 수 있고 일반적으로 이야기를 끝낼 경우라면 마침표를 찍을 수도 있으며 문장이 끝나지  않고 아래오는 말과 밀접히  런관되였을 경우에는 쉼표를 찍을 수도있다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 3075,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 ",
    "output": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 훌륭한 기둥감이냐”에서는 꼭 물음표를 쳐야 할 리유가 없다.  느낌의 뜻으로 강한 어조가 동반될 때에는 느낌표를 칠 수 있고 일반적으로 이야기를 끝낼 경우라면 마침표를 찍을 수도 있으며 문장이 끝나지  않고 아래오는 말과 밀접히  런관되였을 경우에는 쉼표를 찍을 수도있다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3075,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 ",
    "output": "그러면 의문과 관련된 문장에는 꼭 물음표를 쳐야 하는가? 그것은 문장의  성질로 보아서 무엇을 알려고 묻지않을 경우에는 물음표를 치지  않고 다른 부호를 칠 수도있다.  “얼마나 훌륭한 기둥감이냐”에서는 꼭 물음표를 쳐야 할 리유가 없다.  느낌의 뜻으로 강한 어조가 동반될 때에는 느낌표를 칠 수 있고 일반적으로 이야기를 끝낼 경우라면 마침표를 찍을 수도 있으며 문장이 끝나지  않고 아래오는 말과 밀접히  런관되였을 경우에는 쉼표를 찍을 수도있다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3075,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "음 을 나타낼 때에 물음표를 친다.  이런 류형의 문장에 물음표를 치게 되는 것은 먼저 물음의 형식을 취한 뒤에는스스로 대답이 따라오기 마련이기 때문이다.",
    "output": "음 을 나타낼 때에 물음표를 친다.  이런 류형의 문장에 물음표를 치게 되는 것은 먼저 물음의 형식을 취한 뒤에는스스로 대답이 따라오기 마련이기 때문이다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3082,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "셋째, 의문과 감탄의 뜻이 동반되는 문장에서는 물음표와 느낌표를 함께 쓴다.",
    "output": "셋째, 의문과 감탄의 뜻이 동반되는 문장에서는 물음표와 느낌표를 함께 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3083,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "이와 같이 의문의 뜻을 나타내면서도 감탄 또는 놀람의 느낌을 나타낼 때 물음표와 느낌표를 함께 쓸 수 있다.넷째, 모르거나 불확실한 내용임을 나타낼 때 쓴다.",
    "output": "이와 같이 의문의 뜻을 나타내면서도 감탄 또는 놀람의 느낌을 나타낼 때 물음표와 느낌표를 함께 쓸 수 있다.넷째, 모르거나 불확실한 내용임을 나타낼 때 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3084,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "례문에서 김홍도는 출생년도는 명확하지만 사망년도가불확실하고 최세진은 출생년도가 불확실하기  때문에 물음표를 찍은 것이다.",
    "output": "례문에서 김홍도는 출생년도는 명확하지만 사망년도가불확실하고 최세진은 출생년도가 불확실하기  때문에 물음표를 찍은 것이다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3085,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "느낌표는 어떤 사실에 대하여 감동적인 느낌을 나타낼때 쓰인다.  입말에서는 억양과 표정, 손짓, 몸짓 등으로",
    "output": "느낌표는 어떤 사실에 대하여 감동적인 느낌을 나타낼때 쓰인다.  입말에서는 억양과 표정, 손짓, 몸짓 등으로",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3088,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "느낌을 나타내나 글에서는 이런 수단들이 동반될 수 없으므로 느낌표를 쳐서 나타낸다. 느낌표를 쓰는 경우는 다음과 같다.",
    "output": "느낌을 나타내나 글에서는 이런 수단들이 동반될 수 없으므로 느낌표를 쳐서 나타낸다. 느낌표를 쓰는 경우는 다음과 같다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3093,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "이와 같이  감탄의 뜻을 나타내거나 강한 어조를 동반하는 경우에는 그 어떤 문장의 류형이거나를 가리지  않고느낌표를 쳐서 나타낼 수 있다.",
    "output": "이와 같이  감탄의 뜻을 나타내거나 강한 어조를 동반하는 경우에는 그 어떤 문장의 류형이거나를 가리지  않고느낌표를 쳐서 나타낼 수 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3095,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "호칭어, 감동어, 제시어 같은 것들은 어느 정도 독자성이  강하여 문장에서 특별한 자리에  있다.  이런 단위들에는 느낌표를 칠  수 있다.",
    "output": "호칭어, 감동어, 제시어 같은 것들은 어느 정도 독자성이  강하여 문장에서 특별한 자리에  있다.  이런 단위들에는 느낌표를 칠  수 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3097,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "그리고 호칭어나 감동어가 겹칠 때에는 필자의 필요에따라 어느 부분을 선택하여 느낌표를 쓸 수 있다.",
    "output": "그리고 호칭어나 감동어가 겹칠 때에는 필자의 필요에따라 어느 부분을 선택하여 느낌표를 쓸 수 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3098,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "례문과 같이 동종의 문장성분간에는 쉼표로 갈라주고동종의 문장성분들과 총괄어 사이에는 풀이표를 쳐서  갈라준다.  만약 동종의 문장성분들과 총괄어 사이에도 쉼표를찍는다면 쉼표가 계속",
    "output": "례문과 같이 동종의 문장성분간에는 쉼표로 갈라주고동종의 문장성분들과 총괄어 사이에는 풀이표를 쳐서  갈라준다.  만약 동종의 문장성분들과 총괄어 사이에도 쉼표를찍는다면 쉼표가 계속되여  이 사이를 섞갈릴 수 있기 때문이다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3122,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "동격어와 그것을 받는 밀의 관계는 한 대상에  대하여두가지로 부르는 표현들 사이의 관계를 나타낸다.  이런 동격어의 관계는 쉼표로 표시할 수도 있지만 풀이표를 쓰면그 관계가 더 뚜",
    "output": "동격어와 그것을 받는 밀의 관계는 한 대상에  대하여두가지로 부르는 표현들 사이의 관계를 나타낸다.  이런 동격어의 관계는 쉼표로 표시할 수도 있지만 풀이표를 쓰면그 관계가 더 뚜렷해진다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3127,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "이 밖에도 풀이표는 머리 속에 생각한 바를 보여주기위하여서거나 대화로 주고받는 말임을 나타내거나 말이나글을 인용할 때 쓸 수 있다.",
    "output": "이 밖에도 풀이표는 머리 속에 생각한 바를 보여주기위하여서거나 대화로 주고받는 말임을 나타내거나 말이나글을 인용할 때 쓸 수 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3149,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "줄임표는 세점을 찍고 그 사용에 대한 규정은 다음과같다.",
    "output": "줄임표는 세점을 찍고 그 사용에 대한 규정은 다음과같다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3153,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "른 사람의 말을 옮겨오면서 줄인 것이나 관계없이  줄임표는 두루 쓰인다.  때로는 문장들 사이에서 하나 또는 둘 이상의 구절이나 문장이 줄어지는 경우에도 쓰인다.",
    "output": "른 사람의 말을 옮겨오면서 줄인 것이나 관계없이  줄임표는 두루 쓰인다.  때로는 문장들 사이에서 하나 또는 둘 이상의 구절이나 문장이 줄어지는 경우에도 쓰인다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3164,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도",
    "output": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 3166,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도",
    "output": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3166,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도",
    "output": "이와 같이 말의 여운을 남기거나 신중한 어조를 보이거나 조용히 말을 낮추어 할 때 표현적 효과를 높이기 위해서도 쓰인다.  그리고 줄임표는 마침표나 물음표, 느낌표뒤에 오는 경우도 있다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3166,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "셋째, 제목이나 차례의 뒤에 보충하는 설명을 붙일 때쓴다.  이  때 줄임표의 점의 수는 제한이  없다.",
    "output": "셋째, 제목이나 차례의 뒤에 보충하는 설명을 붙일 때쓴다.  이  때 줄임표의 점의 수는 제한이  없다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3167,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "제13항  인용표(“”,  ‘  ’)",
    "output": "제13항  인용표(“”,  ‘  ’)",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3175,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "인용표에는 일반적인 인용표(“”)와 거듭인용표(‘’)가 있다.  인용표는 한짝만 쓰지 않고 앞뒤 짝을 이루어쓴다.  인용표의 사용에 대한 규정은 다음과 같다.",
    "output": "인용표에는 일반적인 인용표(“”)와 거듭인용표(‘’)가 있다.  인용표는 한짝만 쓰지 않고 앞뒤 짝을 이루어쓴다.  인용표의 사용에 대한 규정은 다음과 같다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3177,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "첫째, 다른 사람의 말이나 글을 그대로 인용할 때 그문장의 앞뒤에 갈라 쓴다.",
    "output": "첫째, 다른 사람의 말이나 글을 그대로 인용할 때 그문장의 앞뒤에 갈라 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3178,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "우의 례문과 같이 소설, 산문 등 문학작품(희곡을 제외함.)들에서 인물간의 대화는 인용표를 쳐서 나타낸다.",
    "output": "우의 례문과 같이 소설, 산문 등 문학작품(희곡을 제외함.)들에서 인물간의 대화는 인용표를 쳐서 나타낸다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3185,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "둘째, 인용표 안에 또 다른 인용표를 써야 할 경우에는 거듭인용표(·’)를 쓴다.",
    "output": "둘째, 인용표 안에 또 다른 인용표를 써야 할 경우에는 거듭인용표(·’)를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3186,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "첫번째 례문에서 거듭인용표 안에 묶어진 것은 우리말속담을 인용하였음을 나타내고 인용표 안에 묶어진  것은호소자의 말이다.  두번째 례문에서  거듭인용표 안에 묶어진 것은 스승의 교",
    "output": "첫번째 례문에서 거듭인용표 안에 묶어진 것은 우리말속담을 인용하였음을 나타내고 인용표 안에 묶어진  것은호소자의 말이다.  두번째 례문에서  거듭인용표 안에 묶어진 것은 스승의 교시이고 인용표 안에 묶어진 것은 결심발표자의 말이다.  이와 같이 거듭인용표는 어떤 말을 옮겨다가 넣어서 한 말을 다시 옮겨울 경우에  이  랑자를 섞갈리지  않게 하기 위하여 쓰인다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3187,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "셋째, 마음속으로 한 말을 적을 때에는 거듭인용표(‘’ )를 쓴다.",
    "output": "셋째, 마음속으로 한 말을 적을 때에는 거듭인용표(‘’ )를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3192,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "넷째, 문장에서 중요한 부분을 두드러지게  나타낼 때거듭인용표(‘ ’)를 쓴다.",
    "output": "넷째, 문장에서 중요한 부분을 두드러지게  나타낼 때거듭인용표(‘ ’)를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3198,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "례문에서는 21세기에 가장 중요한 것이  ‘정보’라는 것을 두드러지게  나타내기 위해 거듭인용표를 썼고 ‘지식’과‘실천’ 랑자를 강조하기 위해 거듭인용표로 나타냈다.",
    "output": "례문에서는 21세기에 가장 중요한 것이  ‘정보’라는 것을 두드러지게  나타내기 위해 거듭인용표를 썼고 ‘지식’과‘실천’ 랑자를 강조하기 위해 거듭인용표로 나타냈다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3199,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "제15항  묶음표(소괄호,  중괄호,  내괄호)",
    "output": "제15항  묶음표(소괄호,  중괄호,  내괄호)",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3220,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "묶음표에는 소괄호( ( ) ), 중괄호( [ ] ),  내괄호( { } )가 있다.  묶음표는 앞뒤에 갈라서 짝을 이루어  친다.  묶음표의 사용에 대한 구체적인 규정은 다음과 같",
    "output": "묶음표에는 소괄호( ( ) ), 중괄호( [ ] ),  내괄호( { } )가 있다.  묶음표는 앞뒤에 갈라서 짝을 이루어  친다.  묶음표의 사용에 대한 구체적인 규정은 다음과 같다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3222,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "첫째, 어떤 말에 대한 간단한 설명이나 보충적인 부분을 첨가하는 경우에 그 내용을 묶어주기 위하여 소괄호를그 앞뒤에 쓴다.",
    "output": "첫째, 어떤 말에 대한 간단한 설명이나 보충적인 부분을 첨가하는 경우에 그 내용을 묶어주기 위하여 소괄호를그 앞뒤에 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3223,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "례문과 같이  기본적인 줄거리에 따라 이야기를 전개하면서도 보충적인 설명이 필요한 경우에 괄호 안에  넣어서보여준다.",
    "output": "례문과 같이  기본적인 줄거리에 따라 이야기를 전개하면서도 보충적인 설명이 필요한 경우에 괄호 안에  넣어서보여준다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3224,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "둘째, 우리글에서 한자거나 외래어를 밝힐 경우에 한자거나 외래어의  앞뒤에 소괄호를 쓴다.",
    "output": "둘째, 우리글에서 한자거나 외래어를 밝힐 경우에 한자거나 외래어의  앞뒤에 소괄호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3225,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "셋째, 인용문의  출처를 밝힐 때 그 앞뒤에 소괄호를쓴다.",
    "output": "셋째, 인용문의  출처를 밝힐 때 그 앞뒤에 소괄호를쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3233,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "셋째, 인용문의  출처를 밝힐 때 그 앞뒤에 소괄호를쓴다.",
    "output": "셋째, 인용문의  출처를 밝힐 때 그 앞뒤에 소괄호를쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3233,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "넷째, 묶음표 안에 또 다른 묶음표가 있게  될 때에는바깥 것은 중괄호를,  안의  것은 소괄호를 쓴다.",
    "output": "넷째, 묶음표 안에 또 다른 묶음표가 있게  될 때에는바깥 것은 중괄호를,  안의  것은 소괄호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3236,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "로 앞뒤에 소괄호를 치고 이 문장의 제목은 〈9월 2일의 의미〉이므로 전체의  앞뒤에 중괄호를 쳐서 출처와 문장제목을 갈라서 나타낸다.",
    "output": "로 앞뒤에 소괄호를 치고 이 문장의 제목은 〈9월 2일의 의미〉이므로 전체의  앞뒤에 중괄호를 쳐서 출처와 문장제목을 갈라서 나타낸다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3243,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "다섯째, 제목이나 종목을 특별히 나타내기 위하여  중괄호를 쓴다.",
    "output": "다섯째, 제목이나 종목을 특별히 나타내기 위하여  중괄호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3244,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "《조선어문편람》과 같은 책들에서는 큰 대목을 〈문학편〉과 〈언어편〉으로 갈라볼 수 있다.  여기서  〈언어편〉은큰 대목으로 표시되면서 중괄호를 쳐주었는데 각종 사전,편람, 참고서 ",
    "output": "《조선어문편람》과 같은 책들에서는 큰 대목을 〈문학편〉과 〈언어편〉으로 갈라볼 수 있다.  여기서  〈언어편〉은큰 대목으로 표시되면서 중괄호를 쳐주었는데 각종 사전,편람, 참고서 등에 흔히 리용된다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3245,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "여섯째, 사전 등에서 올림말의 품사거나 발음을 표시할 때 중괄호를 쓴다.",
    "output": "여섯째, 사전 등에서 올림말의 품사거나 발음을 표시할 때 중괄호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3246,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "례문의 어휘들은 《조선말사전》에 수록된 올림말로서매 올림말 뒤의  첫번째 중괄호는 발음을 나타내고 두번째중팔호는 해당 올림말의 품사 소속을 나타낸다.",
    "output": "례문의 어휘들은 《조선말사전》에 수록된 올림말로서매 올림말 뒤의  첫번째 중괄호는 발음을 나타내고 두번째중팔호는 해당 올림말의 품사 소속을 나타낸다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3247,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "일곱째, 여러 단어를 동등하게 묶어서 보일 때 대괄호를 쓴다.",
    "output": "일곱째, 여러 단어를 동등하게 묶어서 보일 때 대괄호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3248,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "제21항  인용표나 묶음표  안에서의  부호",
    "output": "제21항  인용표나 묶음표  안에서의  부호",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3298,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "인용표나 묶음표 안에는 이러저려한 단위가 묶어져 들어간다.  이런 경우에 문장부호를 어떻게 치느냐 하는 문제가 나서는데 이에 대한 규정은 다음과 같다.",
    "output": "인용표나 묶음표 안에는 이러저려한 단위가 묶어져 들어간다.  이런 경우에 문장부호를 어떻게 치느냐 하는 문제가 나서는데 이에 대한 규정은 다음과 같다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3300,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "첫째, 인용표 안의 말이 문장인 경우는 거기에 문장으로서 필요한 부호를 쓴다.",
    "output": "첫째, 인용표 안의 말이 문장인 경우는 거기에 문장으로서 필요한 부호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3301,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "output": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3307,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下句号使用规则",
    "input": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "output": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "metadata": {
      "category": "punctuation",
      "type": "period",
      "paragraph_index": 3307,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下逗号使用规则",
    "input": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "output": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "metadata": {
      "category": "punctuation",
      "type": "comma",
      "paragraph_index": 3307,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下问号/感叹号使用规则",
    "input": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "output": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "metadata": {
      "category": "punctuation",
      "type": "question_exclamation",
      "paragraph_index": 3307,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下省略号/破折号使用规则",
    "input": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "output": "례문에서  인용표 안의  내화부분이  문장으로 구성되였으므로 느낌표(  !  ), 쉼표(  , ),  마침표( .  ), 줄임표( … ) 등 문장부호를 해당한 곳에 찍었다.",
    "metadata": {
      "category": "punctuation",
      "type": "ellipsis_dash",
      "paragraph_index": 3307,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "둘째, 인용표 안의  말이  문장이  아닐  경우는 그것을위한 아무 부호도 치지  않는다.",
    "output": "둘째, 인용표 안의  말이  문장이  아닐  경우는 그것을위한 아무 부호도 치지  않는다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3308,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "례문에서  인용표 안에 들어간 ‘혁명’, ‘참된 삶’은 문장보다 작은 단위인 단어나 단어결합으로 이루어졌기에  인용표 안에 아무 부호도 치지  않았다.",
    "output": "례문에서  인용표 안에 들어간 ‘혁명’, ‘참된 삶’은 문장보다 작은 단위인 단어나 단어결합으로 이루어졌기에  인용표 안에 아무 부호도 치지  않았다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3309,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "셋째, 인용표 안의 문장과 전체로서의 문장이 같은 종류의 문장일 때에는 인용표 밖에만 해당한 부호를 쓴다.",
    "output": "셋째, 인용표 안의 문장과 전체로서의 문장이 같은 종류의 문장일 때에는 인용표 밖에만 해당한 부호를 쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3310,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "례문의 서술문,  감탄문, 의문문이  인용표 안의  것과",
    "output": "례문의 서술문,  감탄문, 의문문이  인용표 안의  것과",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3311,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "전체로서의 문장이 갈게 끝난 경우이므로 문장부호를 겹쳐치지  않고 인용표 밖에 갈이  친다.",
    "output": "전체로서의 문장이 갈게 끝난 경우이므로 문장부호를 겹쳐치지  않고 인용표 밖에 갈이  친다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3316,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "넷째, 인용표 안의 문장과 전체로서의 문장이 다른 종류의 문장일 때에는 인용표의  안팎에 각각 해당한 부호를쓴다.",
    "output": "넷째, 인용표 안의 문장과 전체로서의 문장이 다른 종류의 문장일 때에는 인용표의  안팎에 각각 해당한 부호를쓴다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3317,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下引号使用规则",
    "input": "여기에서  인용표 안의 문장기능과 문장 전체로서의  기능이 다른 경우에는 해당한 문장부호를 각기  쳐서  문장기능이 서로 다름을 나타낸다.",
    "output": "여기에서  인용표 안의 문장기능과 문장 전체로서의  기능이 다른 경우에는 해당한 문장부호를 각기  쳐서  문장기능이 서로 다름을 나타낸다.",
    "metadata": {
      "category": "punctuation",
      "type": "quotation",
      "paragraph_index": 3318,
      "source_category": "punctuation"
    }
  },
  {
    "instruction": "解释以下括号使用规则",
    "input": "묶음표 안의 말은 앞 문장에  대해 내용상 보충설명하는 기능을 할 뿐 형식상으로는 문장 전체와 아무런 관계를발생하지  않는다.  이런 경우에는 묶음표 안에서 보충적으로 설명된 말의",
    "output": "묶음표 안의 말은 앞 문장에  대해 내용상 보충설명하는 기능을 할 뿐 형식상으로는 문장 전체와 아무런 관계를발생하지  않는다.  이런 경우에는 묶음표 안에서 보충적으로 설명된 말의 끝에 해당한 문장부호를 쳐주고 괄호 밖에는 아무 부호도 치지 않는다.",
    "metadata": {
      "category": "punctuation",
      "type": "parenthesis",
      "paragraph_index": 3320,
      "source_category": "punctuation"
    }
  }
];

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { nonPronunciationData };
}
