// 不完全名词训练数据集
// 来源: 《朝鲜语规范集解说》(2019)
// 更新时间: 2024
// 总条目数: 162

const incompleteNounTrainingData = [
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "좋은것으로 고르시오.",
    "output": "좋은 것으로 고르시오.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "것",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'것'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 좋은 것으로 고르시오.\n그릇됨: 좋은것으로 고르시오.",
    "output": "'것'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 좋은 것으로 고르시오.\n그릇됨: 좋은것으로 고르시오.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "것",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "제도개나 쓰던 놈.",
    "output": "제도 개나 쓰던 놈.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "개",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'개'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 제도 개나 쓰던 놈.\n그릇됨: 제도개나 쓰던 놈.",
    "output": "'개'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 제도 개나 쓰던 놈.\n그릇됨: 제도개나 쓰던 놈.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "개",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "시작한김에 일을 끝내다.",
    "output": "시작한 김에 일을 끝내다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "김",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'김'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 시작한 김에 일을 끝내다.\n그릇됨: 시작한김에 일을 끝내다.",
    "output": "'김'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 시작한 김에 일을 끝내다.\n그릇됨: 시작한김에 일을 끝내다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "김",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사람나름이다.",
    "output": "사람 나름이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "나름",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'나름'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사람 나름이다.\n그릇됨: 사람나름이다.",
    "output": "'나름'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 사람 나름이다.\n그릇됨: 사람나름이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "나름",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말할나위가 없다.",
    "output": "말할 나위가 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "나위",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'나위'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말할 나위가 없다.\n그릇됨: 말할나위가 없다.",
    "output": "'나위'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 말할 나위가 없다.\n그릇됨: 말할나위가 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "나위",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "점심 먹을나절이라.",
    "output": "점심 먹을 나절이라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "나절",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'나절'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 점심 먹을 나절이라.\n그릇됨: 점심 먹을나절이라.",
    "output": "'나절'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 점심 먹을 나절이라.\n그릇됨: 점심 먹을나절이라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "나절",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "해가 뜰녘에 집을 떠났다.",
    "output": "해가 뜰 녘에 집을 떠났다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "녘",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'녘'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 해가 뜰 녘에 집을 떠났다.\n그릇됨: 해가 뜰녘에 집을 떠났다.",
    "output": "'녘'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 해가 뜰 녘에 집을 떠났다.\n그릇됨: 해가 뜰녘에 집을 떠났다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "녘",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "주인노릇을 잘하시오.",
    "output": "주인 노릇을 잘하시오.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "노릇",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'노릇'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 주인 노릇을 잘하시오.\n그릇됨: 주인노릇을 잘하시오.",
    "output": "'노릇'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 주인 노릇을 잘하시오.\n그릇됨: 주인노릇을 잘하시오.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "노릇",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈듯도 하다.",
    "output": "갈 듯도 하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "듯",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'듯'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 듯도 하다.\n그릇됨: 갈듯도 하다.",
    "output": "'듯'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 갈 듯도 하다.\n그릇됨: 갈듯도 하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "듯",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사과, 배등 과일.",
    "output": "사과, 배 등 과일.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "등",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'등'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사과, 배 등 과일.\n그릇됨: 사과, 배등 과일.",
    "output": "'등'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 사과, 배 등 과일.\n그릇됨: 사과, 배등 과일.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "등",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "바람 부는대로 항라.",
    "output": "바람 부는 대로 항라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "대로",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'대로'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 바람 부는 대로 항라.\n그릇됨: 바람 부는대로 항라.",
    "output": "'대로'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 바람 부는 대로 항라.\n그릇됨: 바람 부는대로 항라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "대로",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "노래 부르는데 소절이 있다.",
    "output": "노래 부르는 데 소절이 있다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "데",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'데'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 노래 부르는 데 소절이 있다.\n그릇됨: 노래 부르는데 소절이 있다.",
    "output": "'데'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 노래 부르는 데 소절이 있다.\n그릇됨: 노래 부르는데 소절이 있다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "데",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그가 늦을리 없다.",
    "output": "그가 늦을 리 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "리",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'리'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그가 늦을 리 없다.\n그릇됨: 그가 늦을리 없다.",
    "output": "'리'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 그가 늦을 리 없다.\n그릇됨: 그가 늦을리 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "리",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "노래를 부를만하다.",
    "output": "노래를 부를 만하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "만",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'만'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 노래를 부를 만하다.\n그릇됨: 노래를 부를만하다.",
    "output": "'만'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 노래를 부를 만하다.\n그릇됨: 노래를 부를만하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "만",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "요구하는만치 일을 맡기다.",
    "output": "요구하는 만치 일을 맡기다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "만치",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'만치'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 요구하는 만치 일을 맡기다.\n그릇됨: 요구하는만치 일을 맡기다.",
    "output": "'만치'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 요구하는 만치 일을 맡기다.\n그릇됨: 요구하는만치 일을 맡기다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "만치",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "볼만큼 보았다.",
    "output": "볼 만큼 보았다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "만큼",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'만큼'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 볼 만큼 보았다.\n그릇됨: 볼만큼 보았다.",
    "output": "'만큼'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 볼 만큼 보았다.\n그릇됨: 볼만큼 보았다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "만큼",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "식사를 끝낼물력에.",
    "output": "식사를 끝낼 물력에.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "물력",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'물력'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 식사를 끝낼 물력에.\n그릇됨: 식사를 끝낼물력에.",
    "output": "'물력'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 식사를 끝낼 물력에.\n그릇됨: 식사를 끝낼물력에.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "물력",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "한물밖에 안 입은 옷.",
    "output": "한 물밖에 안 입은 옷.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "물",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'물'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 한 물밖에 안 입은 옷.\n그릇됨: 한물밖에 안 입은 옷.",
    "output": "'물'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 한 물밖에 안 입은 옷.\n그릇됨: 한물밖에 안 입은 옷.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "물",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "느낀바를 얘기하다.",
    "output": "느낀 바를 얘기하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "바",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'바'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 느낀 바를 얘기하다.\n그릇됨: 느낀바를 얘기하다.",
    "output": "'바'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 느낀 바를 얘기하다.\n그릇됨: 느낀바를 얘기하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "바",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "놓칠번하다.",
    "output": "놓칠 번하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "번",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'번'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 놓칠 번하다.\n그릇됨: 놓칠번하다.",
    "output": "'번'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 놓칠 번하다.\n그릇됨: 놓칠번하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "번",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "4촌별이 되는 사람.",
    "output": "4촌 별이 되는 사람.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "별",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'별'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 4촌 별이 되는 사람.\n그릇됨: 4촌별이 되는 사람.",
    "output": "'별'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 4촌 별이 되는 사람.\n그릇됨: 4촌별이 되는 사람.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "별",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "저기 오시는분이 누구냐?",
    "output": "저기 오시는 분이 누구냐?",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "분",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'분'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 저기 오시는 분이 누구냐?\n그릇됨: 저기 오시는분이 누구냐?",
    "output": "'분'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 저기 오시는 분이 누구냐?\n그릇됨: 저기 오시는분이 누구냐?",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "분",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "붐을 사한사과.",
    "output": "붐을 사한 사과.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "사",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'사'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 붐을 사한 사과.\n그릇됨: 붐을 사한사과.",
    "output": "'사'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 붐을 사한 사과.\n그릇됨: 붐을 사한사과.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "사",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "이 근방에 있을상 싶다.",
    "output": "이 근방에 있을 상 싶다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "상",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'상'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 이 근방에 있을 상 싶다.\n그릇됨: 이 근방에 있을상 싶다.",
    "output": "'상'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 이 근방에 있을 상 싶다.\n그릇됨: 이 근방에 있을상 싶다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "상",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "될성 싶다.",
    "output": "될 성 싶다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "성",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'성'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 될 성 싶다.\n그릇됨: 될성 싶다.",
    "output": "'성'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 될 성 싶다.\n그릇됨: 될성 싶다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "성",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈손 치더라도.",
    "output": "갈 손 치더라도.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "손",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'손'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 손 치더라도.\n그릇됨: 갈손 치더라도.",
    "output": "'손'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 갈 손 치더라도.\n그릇됨: 갈손 치더라도.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "손",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈수가 없다.",
    "output": "갈 수가 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "수",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'수'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 수가 없다.\n그릇됨: 갈수가 없다.",
    "output": "'수'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 갈 수가 없다.\n그릇됨: 갈수가 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "수",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는이.",
    "output": "모르는 이.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "이",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'이'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 이.\n그릇됨: 모르는이.",
    "output": "'이'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 모르는 이.\n그릇됨: 모르는이.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "이",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "느껴 본적이 없다.",
    "output": "느껴 본 적이 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "적",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'적'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 느껴 본 적이 없다.\n그릇됨: 느껴 본적이 없다.",
    "output": "'적'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 느껴 본 적이 없다.\n그릇됨: 느껴 본적이 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "적",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "올줄 알았다.",
    "output": "올 줄 알았다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "줄",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'줄'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 올 줄 알았다.\n그릇됨: 올줄 알았다.",
    "output": "'줄'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 올 줄 알았다.\n그릇됨: 올줄 알았다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "줄",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "뼈날 즈음에그가 왔다.",
    "output": "뼈날 즈음에 그가 왔다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "즈음",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'즈음'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 뼈날 즈음에 그가 왔다.\n그릇됨: 뼈날 즈음에그가 왔다.",
    "output": "'즈음'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 뼈날 즈음에 그가 왔다.\n그릇됨: 뼈날 즈음에그가 왔다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "즈음",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "간지가 오래다.",
    "output": "간 지가 오래다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "지",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'지'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 간 지가 오래다.\n그릇됨: 간지가 오래다.",
    "output": "'지'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 간 지가 오래다.\n그릇됨: 간지가 오래다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "지",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "못된짓을 하다.",
    "output": "못된 짓을 하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "짓",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'짓'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 못된 짓을 하다.\n그릇됨: 못된짓을 하다.",
    "output": "'짓'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 못된 짓을 하다.\n그릇됨: 못된짓을 하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "짓",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는척하지 말라.",
    "output": "모르는 척하지 말라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "척",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'척'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 척하지 말라.\n그릇됨: 모르는척하지 말라.",
    "output": "'척'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 모르는 척하지 말라.\n그릇됨: 모르는척하지 말라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "척",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "한달치 식량.",
    "output": "한달 치 식량.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "치",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'치'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 한달 치 식량.\n그릇됨: 한달치 식량.",
    "output": "'치'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 한달 치 식량.\n그릇됨: 한달치 식량.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "치",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는체하다.",
    "output": "모르는 체하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "체",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'체'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 체하다.\n그릇됨: 모르는체하다.",
    "output": "'체'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 모르는 체하다.\n그릇됨: 모르는체하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "체",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "바다쪽에서 부는 바람.",
    "output": "바다 쪽에서 부는 바람.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "쪽",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'쪽'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 바다 쪽에서 부는 바람.\n그릇됨: 바다쪽에서 부는 바람.",
    "output": "'쪽'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 바다 쪽에서 부는 바람.\n그릇됨: 바다쪽에서 부는 바람.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "쪽",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "한달쯤 걸린다.",
    "output": "한달 쯤 걸린다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "쯤",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'쯤'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 한달 쯤 걸린다.\n그릇됨: 한달쯤 걸린다.",
    "output": "'쯤'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 한달 쯤 걸린다.\n그릇됨: 한달쯤 걸린다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "쯤",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "과학자가 될터이다.",
    "output": "과학자가 될 터이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "터",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'터'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 과학자가 될 터이다.\n그릇됨: 과학자가 될터이다.",
    "output": "'터'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 과학자가 될 터이다.\n그릇됨: 과학자가 될터이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "터",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말하는품이 서로 다르다.",
    "output": "말하는 품이 서로 다르다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "품",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'품'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말하는 품이 서로 다르다.\n그릇됨: 말하는품이 서로 다르다.",
    "output": "'품'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 말하는 품이 서로 다르다.\n그릇됨: 말하는품이 서로 다르다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "품",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말하는깐을 보다.",
    "output": "말하는 깐을 보다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "깐",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'깐'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말하는 깐을 보다.\n그릇됨: 말하는깐을 보다.",
    "output": "'깐'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 말하는 깐을 보다.\n그릇됨: 말하는깐을 보다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "깐",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "있는껏 가져오너라.",
    "output": "있는 껏 가져오너라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "껏",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'껏'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 있는 껏 가져오너라.\n그릇됨: 있는껏 가져오너라.",
    "output": "'껏'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 있는 껏 가져오너라.\n그릇됨: 있는껏 가져오너라.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "껏",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "너따위는 셈도 없다.",
    "output": "너 따위는 셈도 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "따위",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'따위'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 너 따위는 셈도 없다.\n그릇됨: 너따위는 셈도 없다.",
    "output": "'따위'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 너 따위는 셈도 없다.\n그릇됨: 너따위는 셈도 없다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "따위",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그때문이 아니다.",
    "output": "그 때문이 아니다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "때문",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'때문'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그 때문이 아니다.\n그릇됨: 그때문이 아니다.",
    "output": "'때문'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 그 때문이 아니다.\n그릇됨: 그때문이 아니다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "때문",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "같은 나이또래.",
    "output": "같은 나이 또래.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "또래",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'또래'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 같은 나이 또래.\n그릇됨: 같은 나이또래.",
    "output": "'또래'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 같은 나이 또래.\n그릇됨: 같은 나이또래.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "또래",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "눈물만 흘릴 뿐이다.",
    "output": "눈물만 흘릴 뿐이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "뿐",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'뿐'는 불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 눈물만 흘릴 뿐이다.\n그릇됨: 눈물만 흘릴 뿐이다.",
    "output": "'뿐'는 불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 눈물만 흘릴 뿐이다.\n그릇됨: 눈물만 흘릴 뿐이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "뿐",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'남자뿐'는 접미사로 쓰인 경우이다. 띄여쓰기가 올바른지 판단하라.",
    "input": "남자 뿐이다",
    "output": "남자뿐이다",
    "metadata": {
      "category": "spacing",
      "type": "suffix_correction",
      "noun": "뿐",
      "usage": "suffix",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'셋뿐'는 접미사로 쓰인 경우이다. 띄여쓰기가 올바른지 판단하라.",
    "input": "셋 뿐이다",
    "output": "셋뿐이다",
    "metadata": {
      "category": "spacing",
      "type": "suffix_correction",
      "noun": "뿐",
      "usage": "suffix",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'한번뿐'는 접미사로 쓰인 경우이다. 띄여쓰기가 올바른지 판단하라.",
    "input": "한번 뿐이다",
    "output": "한번뿐이다",
    "metadata": {
      "category": "spacing",
      "type": "suffix_correction",
      "noun": "뿐",
      "usage": "suffix",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "'두장뿐'는 접미사로 쓰인 경우이다. 띄여쓰기가 올바른지 판단하라.",
    "input": "두장 뿐이다",
    "output": "두장뿐이다",
    "metadata": {
      "category": "spacing",
      "type": "suffix_correction",
      "noun": "뿐",
      "usage": "suffix",
      "language_type": "native",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "형제간에 화목하다.",
    "output": "형제 간에 화목하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "간(間)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'간(間)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 형제 간에 화목하다.\n그릇됨: 형제간에 화목하다.",
    "output": "'간(間)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 형제 간에 화목하다.\n그릇됨: 형제간에 화목하다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "간(間)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "5월경에 완공될 예정이다.",
    "output": "5월경에 완공될 예정이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "경(頃)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'경(頃)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 5월경에 완공될 예정이다.\n그릇됨: 5월경에 완공될 예정이다.",
    "output": "'경(頃)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 5월경에 완공될 예정이다.\n그릇됨: 5월경에 완공될 예정이다.",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "경(頃)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "고위급회의",
    "output": "고위급 회의",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "급(級)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'급(級)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 고위급 회의\n그릇됨: 고위급회의",
    "output": "'급(級)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 고위급 회의\n그릇됨: 고위급회의",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "급(級)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "은하계의별들",
    "output": "은하계의 별들",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "계(系)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'계(系)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 은하계의 별들\n그릇됨: 은하계의별들",
    "output": "'계(系)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 은하계의 별들\n그릇됨: 은하계의별들",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "계(系)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "산부인과진료",
    "output": "산부인과 진료",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "과(科)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'과(科)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 산부인과 진료\n그릇됨: 산부인과진료",
    "output": "'과(科)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 산부인과 진료\n그릇됨: 산부인과진료",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "과(科)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "직장내 위생사업",
    "output": "직장 내 위생사업",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "내(內)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'내(內)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 직장 내 위생사업\n그릇됨: 직장내 위생사업",
    "output": "'내(內)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 직장 내 위생사업\n그릇됨: 직장내 위생사업",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "내(內)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "단위당수확고",
    "output": "단위당 수확고",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "당(當)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'당(當)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 단위당 수확고\n그릇됨: 단위당수확고",
    "output": "'당(當)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 단위당 수확고\n그릇됨: 단위당수확고",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "당(當)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "몇십년래오는 더위",
    "output": "몇십년래 오는 더위",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "래(來)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'래(來)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 몇십년래 오는 더위\n그릇됨: 몇십년래오는 더위",
    "output": "'래(來)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 몇십년래 오는 더위\n그릇됨: 몇십년래오는 더위",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "래(來)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "2월말생산실적",
    "output": "2월말 생산실적",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "말(末)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'말(末)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 2월말 생산실적\n그릇됨: 2월말생산실적",
    "output": "'말(末)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 2월말 생산실적\n그릇됨: 2월말생산실적",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "말(末)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "연길발북경행 렬차",
    "output": "연길발 북경행 렬차",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "발(發)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'발(發)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 연길발 북경행 렬차\n그릇됨: 연길발북경행 렬차",
    "output": "'발(發)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 연길발 북경행 렬차\n그릇됨: 연길발북경행 렬차",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "발(發)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "개인별계획",
    "output": "개인별 계획",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "별(別)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'별(別)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 개인별 계획\n그릇됨: 개인별계획",
    "output": "'별(別)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 개인별 계획\n그릇됨: 개인별계획",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "별(別)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "3일부로결정하다",
    "output": "3일부로 결정하다",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "부(附)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'부(附)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 3일부로 결정하다\n그릇됨: 3일부로결정하다",
    "output": "'부(附)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 3일부로 결정하다\n그릇됨: 3일부로결정하다",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "부(附)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "6월분자료",
    "output": "6월분 자료",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "분(份)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'분(份)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 6월분 자료\n그릇됨: 6월분자료",
    "output": "'분(份)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 6월분 자료\n그릇됨: 6월분자료",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "분(份)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "개성산인삼",
    "output": "개성산 인삼",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "산(産)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'산(産)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 개성산 인삼\n그릇됨: 개성산인삼",
    "output": "'산(産)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 개성산 인삼\n그릇됨: 개성산인삼",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "산(産)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사상상진보해야 한다",
    "output": "사상상 진보해야 한다",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "상(上)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'상(上)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사상상 진보해야 한다\n그릇됨: 사상상진보해야 한다",
    "output": "'상(上)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 사상상 진보해야 한다\n그릇됨: 사상상진보해야 한다",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "상(上)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "식물성중독",
    "output": "식물성 중독",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "성(性)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'성(性)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 식물성 중독\n그릇됨: 식물성중독",
    "output": "'성(性)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 식물성 중독\n그릇됨: 식물성중독",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "성(性)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "중국식사회주의",
    "output": "중국식 사회주의",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "식(式)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'식(式)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 중국식 사회주의\n그릇됨: 중국식사회주의",
    "output": "'식(式)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 중국식 사회주의\n그릇됨: 중국식사회주의",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "식(式)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "1951년생사람",
    "output": "1951년생 사람",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "생(生)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'생(生)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 1951년생 사람\n그릇됨: 1951년생사람",
    "output": "'생(生)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 1951년생 사람\n그릇됨: 1951년생사람",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "생(生)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "집여일동안",
    "output": "집여일 동안",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "여(餘)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'여(餘)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 집여일 동안\n그릇됨: 집여일동안",
    "output": "'여(餘)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 집여일 동안\n그릇됨: 집여일동안",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "여(餘)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "학생용가방",
    "output": "학생용 가방",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "용(用)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'용(用)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 학생용 가방\n그릇됨: 학생용가방",
    "output": "'용(用)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 학생용 가방\n그릇됨: 학생용가방",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "용(用)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "력사이래의사변",
    "output": "력사이래의 사변",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "이래(以來)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'이래(以來)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 력사이래의 사변\n그릇됨: 력사이래의사변",
    "output": "'이래(以來)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 력사이래의 사변\n그릇됨: 력사이래의사변",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "이래(以來)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "계획외공사",
    "output": "계획외 공사",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "외(外)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'외(外)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 계획외 공사\n그릇됨: 계획외공사",
    "output": "'외(外)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 계획외 공사\n그릇됨: 계획외공사",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "외(外)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "제1장내용",
    "output": "제1장 내용",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "장(章)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'장(章)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 제1장 내용\n그릇됨: 제1장내용",
    "output": "'장(章)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 제1장 내용\n그릇됨: 제1장내용",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "장(章)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "력사적문제",
    "output": "력사적 문제",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "적(的)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'적(的)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 력사적 문제\n그릇됨: 력사적문제",
    "output": "'적(的)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 력사적 문제\n그릇됨: 력사적문제",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "적(的)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "회의중통화",
    "output": "회의중 통화",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "중(中)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'중(中)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 회의중 통화\n그릇됨: 회의중통화",
    "output": "'중(中)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 회의중 통화\n그릇됨: 회의중통화",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "중(中)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "국산제자전거",
    "output": "국산제 자전거",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "제(制)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'제(制)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 국산제 자전거\n그릇됨: 국산제자전거",
    "output": "'제(制)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 국산제 자전거\n그릇됨: 국산제자전거",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "제(制)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "제23차올림픽대회",
    "output": "제23차 올림픽대회",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "차(次)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'차(次)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 제23차 올림픽대회\n그릇됨: 제23차올림픽대회",
    "output": "'차(次)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 제23차 올림픽대회\n그릇됨: 제23차올림픽대회",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "차(次)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "금년초에시작",
    "output": "금년초에 시작",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "초(初)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'초(初)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 금년초에 시작\n그릇됨: 금년초에시작",
    "output": "'초(初)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 금년초에 시작\n그릇됨: 금년초에시작",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "초(初)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "우리측대표",
    "output": "우리측 대표",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "측(側)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'측(側)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 우리측 대표\n그릇됨: 우리측대표",
    "output": "'측(側)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 우리측 대표\n그릇됨: 우리측대표",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "측(側)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "새로운형세하에서",
    "output": "새로운 형세하에서",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "하(下)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'하(下)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 새로운 형세하에서\n그릇됨: 새로운형세하에서",
    "output": "'하(下)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 새로운 형세하에서\n그릇됨: 새로운형세하에서",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "하(下)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "최신형무기",
    "output": "최신형 무기",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "형(型)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'형(型)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 최신형 무기\n그릇됨: 최신형무기",
    "output": "'형(型)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 최신형 무기\n그릇됨: 최신형무기",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "형(型)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "개혁개방후변화",
    "output": "개혁개방후 변화",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "후(后)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'후(后)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 개혁개방후 변화\n그릇됨: 개혁개방후변화",
    "output": "'후(后)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 개혁개방후 변화\n그릇됨: 개혁개방후변화",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "후(后)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "북경행렬차",
    "output": "북경행 렬차",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_correction",
      "noun": "행(行)",
      "language_type": "chinese",
      "has_examples": true
    }
  },
  {
    "instruction": "'행(行)'는 한자어불완전명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 북경행 렬차\n그릇됨: 북경행렬차",
    "output": "'행(行)'는 한자어불완전명사로 앞의 단어와 띄여써야 한다.\n\n올바름: 북경행 렬차\n그릇됨: 북경행렬차",
    "metadata": {
      "category": "spacing",
      "type": "incomplete_noun_explanation",
      "noun": "행(行)",
      "language_type": "chinese",
      "has_examples": true
    }
  }
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { incompleteNounTrainingData };
}
