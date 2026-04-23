// 单位名词训练数据集 (文档提取)
// 来源: 《朝鲜语规范集解说》
// 更新时间: 2024
// 总条目数: 332

const unitNounsExtractedData = [
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "김명철장지광진청",
    "output": "김명철  장지광  진  청",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "부주임",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'부주임'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 김명철  장지광  진  청\n그릇됨: 김명철장지광진청",
    "output": "'부주임'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 김명철  장지광  진  청\n그릇됨: 김명철장지광진청",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "부주임",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "김철준김광수지동은김영수",
    "output": "김철준  김광수  지동은  김영수",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "집필자",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'집필자'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 김철준  김광수  지동은  김영수\n그릇됨: 김철준김광수지동은김영수",
    "output": "'집필자'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 김철준  김광수  지동은  김영수\n그릇됨: 김철준김광수지동은김영수",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "집필자",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "옳음\t그름",
    "output": "옳음\t그름",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "례",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'례'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 옳음\t그름\n그릇됨: 옳음\t그름",
    "output": "'례'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 옳음\t그름\n그릇됨: 옳음\t그름",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "례",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "좋은것으로고르시오",
    "output": "좋은 것으로 고르시오",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "것",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'것'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 좋은 것으로 고르시오\n그릇됨: 좋은것으로고르시오",
    "output": "'것'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 좋은 것으로 고르시오\n그릇됨: 좋은것으로고르시오",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "것",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "제도개나쓰던놈",
    "output": "제도 개나 쓰던 놈",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "개",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'개'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 제도 개나 쓰던 놈\n그릇됨: 제도개나쓰던놈",
    "output": "'개'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 제도 개나 쓰던 놈\n그릇됨: 제도개나쓰던놈",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "개",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "시작한김에일을끝내다",
    "output": "시작한 김에 일을 끝내다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "김",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'김'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 시작한 김에 일을 끝내다\n그릇됨: 시작한김에일을끝내다",
    "output": "'김'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 시작한 김에 일을 끝내다\n그릇됨: 시작한김에일을끝내다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "김",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "잘먹고못먹고는사람나름이다",
    "output": "잘 먹고 못 먹고는 사람 나름이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "나름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'나름'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 잘 먹고 못 먹고는 사람 나름이다\n그릇됨: 잘먹고못먹고는사람나름이다",
    "output": "'나름'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 잘 먹고 못 먹고는 사람 나름이다\n그릇됨: 잘먹고못먹고는사람나름이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "나름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말할나위가없다",
    "output": "말할 나위가 없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "나위",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'나위'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말할 나위가 없다\n그릇됨: 말할나위가없다",
    "output": "'나위'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 말할 나위가 없다\n그릇됨: 말할나위가없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "나위",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "점심먹을나절이라장사군과장군들로붐볐다",
    "output": "점심 먹을 나절이라 장사군과 장군들로 붐볐다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "나절",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'나절'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 점심 먹을 나절이라 장사군과 장군들로 붐볐다\n그릇됨: 점심먹을나절이라장사군과장군들로붐볐다",
    "output": "'나절'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 점심 먹을 나절이라 장사군과 장군들로 붐볐다\n그릇됨: 점심먹을나절이라장사군과장군들로붐볐다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "나절",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "해가뜰넉에집을떠났다",
    "output": "해가 뜰 넉에 집을 떠났다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "녁",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'녁'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 해가 뜰 넉에 집을 떠났다\n그릇됨: 해가뜰넉에집을떠났다",
    "output": "'녁'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 해가 뜰 넉에 집을 떠났다\n그릇됨: 해가뜰넉에집을떠났다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "녁",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "주인노릇을잘하시오",
    "output": "주인 노릇을 잘하시오",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "노릇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'노릇'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 주인 노릇을 잘하시오\n그릇됨: 주인노릇을잘하시오",
    "output": "'노릇'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 주인 노릇을 잘하시오\n그릇됨: 주인노릇을잘하시오",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "노릇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈듯도하다",
    "output": "갈 듯도 하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "듯",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'듯'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 듯도 하다\n그릇됨: 갈듯도하다",
    "output": "'듯'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 갈 듯도 하다\n그릇됨: 갈듯도하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "듯",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "바람부는내로해라",
    "output": "바람 부는 내로 해라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "대로",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'대로'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 바람 부는 내로 해라\n그릇됨: 바람부는내로해라",
    "output": "'대로'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 바람 부는 내로 해라\n그릇됨: 바람부는내로해라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "대로",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "노래부르는데소절이있다",
    "output": "노래 부르는 데 소절이  있다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "데",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'데'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 노래 부르는 데 소절이  있다\n그릇됨: 노래부르는데소절이있다",
    "output": "'데'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 노래 부르는 데 소절이  있다\n그릇됨: 노래부르는데소절이있다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "데",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그가늦을리없다",
    "output": "그가 늦을 리 없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그가 늦을 리 없다\n그릇됨: 그가늦을리없다",
    "output": "'리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 그가 늦을 리 없다\n그릇됨: 그가늦을리없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "노래를부를만하다",
    "output": "노래를 부를 만하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "만",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'만'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 노래를 부를 만하다\n그릇됨: 노래를부를만하다",
    "output": "'만'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 노래를 부를 만하다\n그릇됨: 노래를부를만하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "만",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "요구하는만치일을말기다",
    "output": "요구하는 만치 일을 말기다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "만치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'만치'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 요구하는 만치 일을 말기다\n그릇됨: 요구하는만치일을말기다",
    "output": "'만치'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 요구하는 만치 일을 말기다\n그릇됨: 요구하는만치일을말기다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "만치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "불만큼보았다",
    "output": "불 만큼 보았다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "만큼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'만큼'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 불 만큼 보았다\n그릇됨: 불만큼보았다",
    "output": "'만큼'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 불 만큼 보았다\n그릇됨: 불만큼보았다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "만큼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "식사를끝낼무렵에물이상당히빠져있었다",
    "output": "식사를 끝낼 무렵에 물이 상당히 빠져있었다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "무렵",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'무렵'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 식사를 끝낼 무렵에 물이 상당히 빠져있었다\n그릇됨: 식사를끝낼무렵에물이상당히빠져있었다",
    "output": "'무렵'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 식사를 끝낼 무렵에 물이 상당히 빠져있었다\n그릇됨: 식사를끝낼무렵에물이상당히빠져있었다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "무렵",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "느낀바를얘기하다",
    "output": "느낀 바를 얘기하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "바",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'바'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 느낀 바를 얘기하다\n그릇됨: 느낀바를얘기하다",
    "output": "'바'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 느낀 바를 얘기하다\n그릇됨: 느낀바를얘기하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "바",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "놓칠번하다",
    "output": "놓칠 번하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "번",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'번'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 놓칠 번하다\n그릇됨: 놓칠번하다",
    "output": "'번'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 놓칠 번하다\n그릇됨: 놓칠번하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "번",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "4촌벌이되는사람",
    "output": "4촌 벌이 되는 사람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "별",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'별'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 4촌 벌이 되는 사람\n그릇됨: 4촌벌이되는사람",
    "output": "'별'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 4촌 벌이 되는 사람\n그릇됨: 4촌벌이되는사람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "별",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "붐을사한사과",
    "output": "붐을 사한 사과",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "사",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'사'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 붐을 사한 사과\n그릇됨: 붐을사한사과",
    "output": "'사'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 붐을 사한 사과\n그릇됨: 붐을사한사과",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "사",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "이근방에있을상싶다",
    "output": "이 근방에 있을 상 싶다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "상",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'상'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 이 근방에 있을 상 싶다\n그릇됨: 이근방에있을상싶다",
    "output": "'상'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 이 근방에 있을 상 싶다\n그릇됨: 이근방에있을상싶다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "상",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "될성싶다",
    "output": "될 성 싶다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "성",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'성'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 될 성 싶다\n그릇됨: 될성싶다",
    "output": "'성'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 될 성 싶다\n그릇됨: 될성싶다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "성",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈수가없다",
    "output": "갈 수가 없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "수",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'수'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 수가 없다\n그릇됨: 갈수가없다",
    "output": "'수'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 갈 수가 없다\n그릇됨: 갈수가없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "수",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "일을할양으로",
    "output": "일을 할 양으로",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "앙",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'앙'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 일을 할 양으로\n그릇됨: 일을할양으로",
    "output": "'앙'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 일을 할 양으로\n그릇됨: 일을할양으로",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "앙",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사랑의손길을가슴뜨겁게느껴본적이없다",
    "output": "사랑의 손길을 가슴 뜨겁게 느껴본 적이  없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "적",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'적'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사랑의 손길을 가슴 뜨겁게 느껴본 적이  없다\n그릇됨: 사랑의손길을가슴뜨겁게느껴본적이없다",
    "output": "'적'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 사랑의 손길을 가슴 뜨겁게 느껴본 적이  없다\n그릇됨: 사랑의손길을가슴뜨겁게느껴본적이없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "적",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "장난하는조로묻다",
    "output": "장난하는 조로 묻다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "조",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'조'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 장난하는 조로 묻다\n그릇됨: 장난하는조로묻다",
    "output": "'조'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 장난하는 조로 묻다\n그릇됨: 장난하는조로묻다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "조",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "올줄알았다",
    "output": "올 줄 알았다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "줄",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'줄'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 올 줄 알았다\n그릇됨: 올줄알았다",
    "output": "'줄'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 올 줄 알았다\n그릇됨: 올줄알았다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "줄",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "뼈날즈음에그가왔다",
    "output": "뼈날 즈음에 그가 왔다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "즈음",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'즈음'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 뼈날 즈음에 그가 왔다\n그릇됨: 뼈날즈음에그가왔다",
    "output": "'즈음'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 뼈날 즈음에 그가 왔다\n그릇됨: 뼈날즈음에그가왔다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "즈음",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "갈즘",
    "output": "갈 즘",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "즘",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'즘'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 갈 즘\n그릇됨: 갈즘",
    "output": "'즘'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 갈 즘\n그릇됨: 갈즘",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "즘",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "간지가오래다",
    "output": "간 지가 오래다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 간 지가 오래다\n그릇됨: 간지가오래다",
    "output": "'지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 간 지가 오래다\n그릇됨: 간지가오래다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "못된짓을하다",
    "output": "못된 짓을 하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "짓",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'짓'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 못된 짓을 하다\n그릇됨: 못된짓을하다",
    "output": "'짓'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 못된 짓을 하다\n그릇됨: 못된짓을하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "짓",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는척하지말라",
    "output": "모르는 척하지 말라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "척",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'척'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 척하지 말라\n그릇됨: 모르는척하지말라",
    "output": "'척'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 모르는 척하지 말라\n그릇됨: 모르는척하지말라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "척",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "한달치식량",
    "output": "한달 치 식량",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'치'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 한달 치 식량\n그릇됨: 한달치식량",
    "output": "'치'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 한달 치 식량\n그릇됨: 한달치식량",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "산채로잡은짐승",
    "output": "산 채로 잡은 짐승",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "채",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'채'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 산 채로 잡은 짐승\n그릇됨: 산채로잡은짐승",
    "output": "'채'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 산 채로 잡은 짐승\n그릇됨: 산채로잡은짐승",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "채",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는체하다",
    "output": "모르는 체하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "체",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'체'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 체하다\n그릇됨: 모르는체하다",
    "output": "'체'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 모르는 체하다\n그릇됨: 모르는체하다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "체",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "우리켠사람",
    "output": "우리 켠 사람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "켠",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'켠'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 우리 켠 사람\n그릇됨: 우리켠사람",
    "output": "'켠'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 우리 켠 사람\n그릇됨: 우리켠사람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "켠",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "될타이없다",
    "output": "될 타이 없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "탁",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'탁'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 될 타이 없다\n그릇됨: 될타이없다",
    "output": "'탁'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 될 타이 없다\n그릇됨: 될타이없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "탁",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "과학자가될터이다",
    "output": "과학자가 될 터이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "터",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'터'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 과학자가 될 터이다\n그릇됨: 과학자가될터이다",
    "output": "'터'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 과학자가 될 터이다\n그릇됨: 과학자가될터이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "터",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "뼈들어대는통에자지못했다",
    "output": "뼈들어대는 통에 자지 못했다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "통",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'통'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 뼈들어대는 통에 자지 못했다\n그릇됨: 뼈들어대는통에자지못했다",
    "output": "'통'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 뼈들어대는 통에 자지 못했다\n그릇됨: 뼈들어대는통에자지못했다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "통",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그저그렉이다",
    "output": "그저 그 렉이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "랙",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'랙'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그저 그 렉이다\n그릇됨: 그저그렉이다",
    "output": "'랙'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 그저 그 렉이다\n그릇됨: 그저그렉이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "랙",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "일이잘된폭이다",
    "output": "일이 잘된 폭이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "폭",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'폭'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 일이 잘된 폭이다\n그릇됨: 일이잘된폭이다",
    "output": "'폭'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 일이 잘된 폭이다\n그릇됨: 일이잘된폭이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "폭",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말하는품이서로다르다",
    "output": "말하는 품이 서로 다르다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "품",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'품'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말하는 품이 서로 다르다\n그릇됨: 말하는품이서로다르다",
    "output": "'품'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 말하는 품이 서로 다르다\n그릇됨: 말하는품이서로다르다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "품",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "이물건은내해이다",
    "output": "이 물건은 내 해이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "해",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'해'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 이 물건은 내 해이다\n그릇됨: 이물건은내해이다",
    "output": "'해'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 이 물건은 내 해이다\n그릇됨: 이물건은내해이다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "해",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "말하는깐을보다",
    "output": "말하는 깐을 보다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "깐",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'깐'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 말하는 깐을 보다\n그릇됨: 말하는깐을보다",
    "output": "'깐'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 말하는 깐을 보다\n그릇됨: 말하는깐을보다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "깐",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "있는껏가져오너라",
    "output": "있는 껏 가져오너라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "껏",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'껏'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 있는 껏 가져오너라\n그릇됨: 있는껏가져오너라",
    "output": "'껏'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 있는 껏 가져오너라\n그릇됨: 있는껏가져오너라",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "껏",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "너따위는셈도없다",
    "output": "너 따위는 셈도 없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "따위",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'따위'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 너 따위는 셈도 없다\n그릇됨: 너따위는셈도없다",
    "output": "'따위'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 너 따위는 셈도 없다\n그릇됨: 너따위는셈도없다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "따위",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "같은나이또래",
    "output": "같은 나이 또래",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "또래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'또래'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 같은 나이 또래\n그릇됨: 같은나이또래",
    "output": "'또래'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 같은 나이 또래\n그릇됨: 같은나이또래",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "또래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그때문이아니다",
    "output": "그 때문이 아니다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "때문",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'때문'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그 때문이 아니다\n그릇됨: 그때문이아니다",
    "output": "'때문'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 그 때문이 아니다\n그릇됨: 그때문이아니다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "때문",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "바다쪽에서부는바람",
    "output": "바다 쪽에서 부는 바람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "쪽",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'쪽'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 바다 쪽에서 부는 바람\n그릇됨: 바다쪽에서부는바람",
    "output": "'쪽'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 바다 쪽에서 부는 바람\n그릇됨: 바다쪽에서부는바람",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "쪽",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "한달쯤걸린다",
    "output": "한달 쯤 걸린다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "쯤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'쯤'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 한달 쯤 걸린다\n그릇됨: 한달쯤걸린다",
    "output": "'쯤'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 한달 쯤 걸린다\n그릇됨: 한달쯤걸린다",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "쯤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "엿한",
    "output": "엿 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가락",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가락'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 엿 한\n그릇됨: 엿한",
    "output": "'가락'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 엿 한\n그릇됨: 엿한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가락",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "벼두",
    "output": "벼 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 벼 두\n그릇됨: 벼두",
    "output": "'가리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 벼 두\n그릇됨: 벼두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "훅두",
    "output": "훅 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가래'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 훅 두\n그릇됨: 훅두",
    "output": "'가래'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 훅 두\n그릇됨: 훅두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "숯다섯",
    "output": "숯 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가마",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가마'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 숯 다섯\n그릇됨: 숯다섯",
    "output": "'가마'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 숯 다섯\n그릇됨: 숯다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가마",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "나무세",
    "output": "나무 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 나무 세\n그릇됨: 나무세",
    "output": "'가지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 나무 세\n그릇됨: 나무세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "성냥다섯",
    "output": "성냥 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "가치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'가치'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 성냥 다섯\n그릇됨: 성냥다섯",
    "output": "'가치'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 성냥 다섯\n그릇됨: 성냥다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "가치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "방두",
    "output": "방 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "간",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'간'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 방 두\n그릇됨: 방두",
    "output": "'간'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 방 두\n그릇됨: 방두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "간",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "양복두",
    "output": "양복 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "감",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'감'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 양복 두\n그릇됨: 양복두",
    "output": "'감'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 양복 두\n그릇됨: 양복두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "감",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "권연두",
    "output": "권연 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "갑",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'갑'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 권연 두\n그릇됨: 권연두",
    "output": "'갑'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 권연 두\n그릇됨: 권연두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "갑",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "장작다섯",
    "output": "장작 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "강다리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'강다리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 장작 다섯\n그릇됨: 장작다섯",
    "output": "'강다리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 장작 다섯\n그릇됨: 장작다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "강다리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "옷한",
    "output": "옷 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "견지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'견지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 옷 한\n그릇됨: 옷한",
    "output": "'견지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 옷 한\n그릇됨: 옷한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "견지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "소주두",
    "output": "소주 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "고리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'고리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 소주 두\n그릇됨: 소주두",
    "output": "'고리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 소주 두\n그릇됨: 소주두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "고리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "명곡세",
    "output": "명곡 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "곡",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'곡'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 명곡 세\n그릇됨: 명곡세",
    "output": "'곡'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 명곡 세\n그릇됨: 명곡세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "곡",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "백양나무한",
    "output": "백양나무 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "그루",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'그루'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 백양나무 한\n그릇됨: 백양나무한",
    "output": "'그루'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 백양나무 한\n그릇됨: 백양나무한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "그루",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "국수세",
    "output": "국수 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "그릇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'그릇'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 국수 세\n그릇됨: 국수세",
    "output": "'그릇'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 국수 세\n그릇됨: 국수세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "그릇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "성냥두",
    "output": "성냥 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "개비",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'개비'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 성냥 두\n그릇됨: 성냥두",
    "output": "'개비'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 성냥 두\n그릇됨: 성냥두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "개비",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "타일한",
    "output": "타일 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꽝주리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꽝주리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 타일 한\n그릇됨: 타일한",
    "output": "'꽝주리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 타일 한\n그릇됨: 타일한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꽝주리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "책열",
    "output": "책 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "권",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'권'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 책 열\n그릇됨: 책열",
    "output": "'권'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 책 열\n그릇됨: 책열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "권",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "벼짚두",
    "output": "벼짚 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "단",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'단'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 벼짚 두\n그릇됨: 벼짚두",
    "output": "'단'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 벼짚 두\n그릇됨: 벼짚두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "단",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "자치주창립55",
    "output": "자치주 창립 55",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "돓",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'돓'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 자치주 창립 55\n그릇됨: 자치주창립55",
    "output": "'돓'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 자치주 창립 55\n그릇됨: 자치주창립55",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "돓",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "빨세",
    "output": "빨 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "두둑",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'두둑'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 빨 세\n그릇됨: 빨세",
    "output": "'두둑'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 빨 세\n그릇됨: 빨세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "두둑",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "청어열",
    "output": "청어 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "두름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'두름'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 청어 열\n그릇됨: 청어열",
    "output": "'두름'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 청어 열\n그릇됨: 청어열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "두름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "국수두",
    "output": "국수 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "대접",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'대접'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 국수 두\n그릇됨: 국수두",
    "output": "'대접'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 국수 두\n그릇됨: 국수두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "대접",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "노래한",
    "output": "노래 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "마디",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'마디'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 노래 한\n그릇됨: 노래한",
    "output": "'마디'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 노래 한\n그릇됨: 노래한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "마디",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "이영두",
    "output": "이영 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "마름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'마름'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 이영 두\n그릇됨: 이영두",
    "output": "'마름'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 이영 두\n그릇됨: 이영두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "마름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "썰두",
    "output": "썰 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "말",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'말'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 썰 두\n그릇됨: 썰두",
    "output": "'말'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 썰 두\n그릇됨: 썰두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "말",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "물두",
    "output": "물 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "모금",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'모금'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 물 두\n그릇됨: 물두",
    "output": "'모금'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 물 두\n그릇됨: 물두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "모금",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "찰떡한",
    "output": "찰떡 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "모래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'모래'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 찰떡 한\n그릇됨: 찰떡한",
    "output": "'모래'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 찰떡 한\n그릇됨: 찰떡한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "모래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "석탄두",
    "output": "석탄 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "무지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'무지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 석탄 두\n그릇됨: 석탄두",
    "output": "'무지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 석탄 두\n그릇됨: 석탄두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "무지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "미나리세",
    "output": "미나리 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "뭇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'뭇'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 미나리 세\n그릇됨: 미나리세",
    "output": "'뭇'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 미나리 세\n그릇됨: 미나리세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "뭇",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "꽃두",
    "output": "꽃 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "묶음",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'묶음'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 꽃 두\n그릇됨: 꽃두",
    "output": "'묶음'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 꽃 두\n그릇됨: 꽃두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "묶음",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "물두",
    "output": "물 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "바가지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'바가지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 물 두\n그릇됨: 물두",
    "output": "'바가지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 물 두\n그릇됨: 물두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "바가지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "과일한",
    "output": "과일 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "바구니",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'바구니'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 과일 한\n그릇됨: 과일한",
    "output": "'바구니'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 과일 한\n그릇됨: 과일한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "바구니",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "떨나무두",
    "output": "떨나무 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "바리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'바리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 떨나무 두\n그릇됨: 떨나무두",
    "output": "'바리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 떨나무 두\n그릇됨: 떨나무두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "바리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "새끼다섯",
    "output": "새끼 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "발",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'발'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 새끼 다섯\n그릇됨: 새끼다섯",
    "output": "'발'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 새끼 다섯\n그릇됨: 새끼다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "발",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "치마저고리한",
    "output": "치마저고리 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "벌",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'벌'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 치마저고리 한\n그릇됨: 치마저고리한",
    "output": "'벌'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 치마저고리 한\n그릇됨: 치마저고리한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "벌",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "맥주다섯",
    "output": "맥주 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "병",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'병'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 맥주 다섯\n그릇됨: 맥주다섯",
    "output": "'병'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 맥주 다섯\n그릇됨: 맥주다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "병",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "담배두",
    "output": "담배 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "보루",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'보루'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 담배 두\n그릇됨: 담배두",
    "output": "'보루'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 담배 두\n그릇됨: 담배두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "보루",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "짐두",
    "output": "짐 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "보따리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'보따리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 짐 두\n그릇됨: 짐두",
    "output": "'보따리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 짐 두\n그릇됨: 짐두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "보따리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사탕두",
    "output": "사탕 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "봉지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'봉지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사탕 두\n그릇됨: 사탕두",
    "output": "'봉지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 사탕 두\n그릇됨: 사탕두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "봉지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "밀가루한",
    "output": "밀가루 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "부대",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'부대'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 밀가루 한\n그릇됨: 밀가루한",
    "output": "'부대'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 밀가루 한\n그릇됨: 밀가루한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "부대",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "병아리를두",
    "output": "병아리를 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "배",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'배'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 병아리를 두\n그릇됨: 병아리를두",
    "output": "'배'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 병아리를 두\n그릇됨: 병아리를두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "배",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "과일한",
    "output": "과일 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "사라",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'사라'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 과일 한\n그릇됨: 과일한",
    "output": "'사라'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 과일 한\n그릇됨: 과일한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "사라",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "국수세",
    "output": "국수 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "사리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'사리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 국수 세\n그릇됨: 국수세",
    "output": "'사리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 국수 세\n그릇됨: 국수세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "사리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "국두",
    "output": "국 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "사발",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'사발'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 국 두\n그릇됨: 국두",
    "output": "'사발'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 국 두\n그릇됨: 국두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "사발",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "임신한치두",
    "output": "임신한 치 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "삭",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'삭'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 임신한 치 두\n그릇됨: 임신한치두",
    "output": "'삭'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 임신한 치 두\n그릇됨: 임신한치두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "삭",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "훔두",
    "output": "훔 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "삽",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'삽'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 훔 두\n그릇됨: 훔두",
    "output": "'삽'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 훔 두\n그릇됨: 훔두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "삽",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "부속품10",
    "output": "부속품 10",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "상자",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'상자'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 부속품 10\n그릇됨: 부속품10",
    "output": "'상자'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 부속품 10\n그릇됨: 부속품10",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "상자",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "콩세",
    "output": "콩 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "섬",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'섬'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 콩 세\n그릇됨: 콩세",
    "output": "'섬'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 콩 세\n그릇됨: 콩세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "섬",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "꽃두",
    "output": "꽃 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "종이",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'종이'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 꽃 두\n그릇됨: 꽃두",
    "output": "'종이'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 꽃 두\n그릇됨: 꽃두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "종이",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "술두",
    "output": "술 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "순배",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'순배'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 술 두\n그릇됨: 술두",
    "output": "'순배'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 술 두\n그릇됨: 술두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "순배",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "밥두",
    "output": "밥 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "술",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'술'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 밥 두\n그릇됨: 밥두",
    "output": "'술'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 밥 두\n그릇됨: 밥두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "술",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "포도두",
    "output": "포도 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "숭어리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'숭어리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 포도 두\n그릇됨: 포도두",
    "output": "'숭어리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 포도 두\n그릇됨: 포도두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "숭어리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "나무두",
    "output": "나무 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "아름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'아름'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 나무 두\n그릇됨: 나무두",
    "output": "'아름'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 나무 두\n그릇됨: 나무두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "아름",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사탕두",
    "output": "사탕 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "알",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'알'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사탕 두\n그릇됨: 사탕두",
    "output": "'알'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 사탕 두\n그릇됨: 사탕두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "알",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "탄알세",
    "output": "탄알 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "알쌈",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'알쌈'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 탄알 세\n그릇됨: 탄알세",
    "output": "'알쌈'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 탄알 세\n그릇됨: 탄알세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "알쌈",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "질세",
    "output": "질 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "오리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'오리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 질 세\n그릇됨: 질세",
    "output": "'오리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 질 세\n그릇됨: 질세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "오리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "철사두",
    "output": "철사 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "올",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'올'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 철사 두\n그릇됨: 철사두",
    "output": "'올'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 철사 두\n그릇됨: 철사두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "올",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "쌀두",
    "output": "쌀 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "웅큼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'웅큼'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 쌀 두\n그릇됨: 쌀두",
    "output": "'웅큼'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 쌀 두\n그릇됨: 쌀두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "웅큼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "꾸미두",
    "output": "꾸미 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "자밤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'자밤'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 꾸미 두\n그릇됨: 꾸미두",
    "output": "'자밤'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 꾸미 두\n그릇됨: 꾸미두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "자밤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "술두",
    "output": "술 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "잔",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'잔'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 술 두\n그릇됨: 술두",
    "output": "'잔'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 술 두\n그릇됨: 술두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "잔",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "5원25",
    "output": "5원 25",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "전",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'전'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 5원 25\n그릇됨: 5원25",
    "output": "'전'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 5원 25\n그릇됨: 5원25",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "전",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "괘종이두",
    "output": "괘종이 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "점",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'점'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 괘종이 두\n그릇됨: 괘종이두",
    "output": "'점'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 괘종이 두\n그릇됨: 괘종이두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "점",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "사과한",
    "output": "사과 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "접시",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'접시'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 사과 한\n그릇됨: 사과한",
    "output": "'접시'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 사과 한\n그릇됨: 사과한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "접시",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "논여섯",
    "output": "논 여섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "정보",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'정보'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 논 여섯\n그릇됨: 논여섯",
    "output": "'정보'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 논 여섯\n그릇됨: 논여섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "정보",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "규정두",
    "output": "규정 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "조목",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'조목'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 규정 두\n그릇됨: 규정두",
    "output": "'조목'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 규정 두\n그릇됨: 규정두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "조목",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "품종50",
    "output": "품종 50",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "종",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'종'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 품종 50\n그릇됨: 품종50",
    "output": "'종'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 품종 50\n그릇됨: 품종50",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "종",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "간장두",
    "output": "간장 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "종지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'종지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 간장 두\n그릇됨: 간장두",
    "output": "'종지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 간장 두\n그릇됨: 간장두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "종지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "강물한",
    "output": "강물 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "줄기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'줄기'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 강물 한\n그릇됨: 강물한",
    "output": "'줄기'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 강물 한\n그릇됨: 강물한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "줄기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "쌀한",
    "output": "쌀 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "줌",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'줌'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 쌀 한\n그릇됨: 쌀한",
    "output": "'줌'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 쌀 한\n그릇됨: 쌀한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "줌",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "책두",
    "output": "책 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "질",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'질'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 책 두\n그릇됨: 책두",
    "output": "'질'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 책 두\n그릇됨: 책두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "질",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "나무두",
    "output": "나무 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "짐",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'짐'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 나무 두\n그릇됨: 나무두",
    "output": "'짐'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 나무 두\n그릇됨: 나무두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "짐",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "세멘트10",
    "output": "세멘트 10",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "차판",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'차판'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 세멘트 10\n그릇됨: 세멘트10",
    "output": "'차판'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 세멘트 10\n그릇됨: 세멘트10",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "차판",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "초약두",
    "output": "초약 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "첩",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'첩'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 초약 두\n그릇됨: 초약두",
    "output": "'첩'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 초약 두\n그릇됨: 초약두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "첩",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "석유두",
    "output": "석유 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "초롱",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'초롱'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 석유 두\n그릇됨: 석유두",
    "output": "'초롱'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 석유 두\n그릇됨: 석유두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "초롱",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "벼모두",
    "output": "벼모 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "춤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'춤'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 벼모 두\n그릇됨: 벼모두",
    "output": "'춤'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 벼모 두\n그릇됨: 벼모두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "춤",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "교과서열",
    "output": "교과서 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "책",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'책'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 교과서 열\n그릇됨: 교과서열",
    "output": "'책'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 교과서 열\n그릇됨: 교과서열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "책",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "시루며서너",
    "output": "시루며 서너",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "켜",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'켜'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 시루며 서너\n그릇됨: 시루며서너",
    "output": "'켜'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 시루며 서너\n그릇됨: 시루며서너",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "켜",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "그물쉰",
    "output": "그물 쉰",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "코",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'코'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 그물 쉰\n그릇됨: 그물쉰",
    "output": "'코'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 그물 쉰\n그릇됨: 그물쉰",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "코",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "실한",
    "output": "실 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "타래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'타래'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 실 한\n그릇됨: 실한",
    "output": "'타래'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 실 한\n그릇됨: 실한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "타래",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "실두",
    "output": "실 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "토리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'토리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 실 두\n그릇됨: 실두",
    "output": "'토리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 실 두\n그릇됨: 실두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "토리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "새끼열",
    "output": "새끼 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "퉁구리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'퉁구리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 새끼 열\n그릇됨: 새끼열",
    "output": "'퉁구리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 새끼 열\n그릇됨: 새끼열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "퉁구리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "실다섯",
    "output": "실 다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "떼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'떼'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 실 다섯\n그릇됨: 실다섯",
    "output": "'떼'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 실 다섯\n그릇됨: 실다섯",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "떼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "인삼세",
    "output": "인삼 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "편",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'편'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 인삼 세\n그릇됨: 인삼세",
    "output": "'편'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 인삼 세\n그릇됨: 인삼세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "편",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "배추열",
    "output": "배추 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "포기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'포기'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 배추 열\n그릇됨: 배추열",
    "output": "'포기'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 배추 열\n그릇됨: 배추열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "포기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "세멘트두",
    "output": "세멘트 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "포대",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'포대'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 세멘트 두\n그릇됨: 세멘트두",
    "output": "'포대'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 세멘트 두\n그릇됨: 세멘트두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "포대",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "농가200여",
    "output": "농가 200여",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "호",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'호'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 농가 200여\n그릇됨: 농가200여",
    "output": "'호'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 농가 200여\n그릇됨: 농가200여",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "호",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "미시가루세",
    "output": "미시가루 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "홉",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'홉'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 미시가루 세\n그릇됨: 미시가루세",
    "output": "'홉'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 미시가루 세\n그릇됨: 미시가루세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "홉",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "제21",
    "output": "제21",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "회",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'회'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 제21\n그릇됨: 제21",
    "output": "'회'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 제21\n그릇됨: 제21",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "회",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "닭이두",
    "output": "닭이 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "홰",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'홰'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 닭이 두\n그릇됨: 닭이두",
    "output": "'홰'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 닭이 두\n그릇됨: 닭이두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "홰",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "곶감한",
    "output": "곶감 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꼬치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꼬치'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 곶감 한\n그릇됨: 곶감한",
    "output": "'꼬치'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 곶감 한\n그릇됨: 곶감한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꼬치",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "콩열",
    "output": "콩 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꼬투리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꼬투리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 콩 열\n그릇됨: 콩열",
    "output": "'꼬투리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 콩 열\n그릇됨: 콩열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꼬투리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "미역열",
    "output": "미역 열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꼭지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꼭지'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 미역 열\n그릇됨: 미역열",
    "output": "'꼭지'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 미역 열\n그릇됨: 미역열",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꼭지",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "실두",
    "output": "실 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꾸리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꾸리'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 실 두\n그릇됨: 실두",
    "output": "'꾸리'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 실 두\n그릇됨: 실두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꾸리",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "하루세",
    "output": "하루 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "끼(끼니)",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'끼(끼니)'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 하루 세\n그릇됨: 하루세",
    "output": "'끼(끼니)'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 하루 세\n그릇됨: 하루세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "끼(끼니)",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "양고기두",
    "output": "양고기 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "꿰미(쨈)",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'꿰미(쨈)'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 양고기 두\n그릇됨: 양고기두",
    "output": "'꿰미(쨈)'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 양고기 두\n그릇됨: 양고기두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "꿰미(쨈)",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "들국화두",
    "output": "들국화 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "별기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'별기'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 들국화 두\n그릇됨: 들국화두",
    "output": "'별기'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 들국화 두\n그릇됨: 들국화두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "별기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "논두",
    "output": "논 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "퇘기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'퇘기'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 논 두\n그릇됨: 논두",
    "output": "'퇘기'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 논 두\n그릇됨: 논두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "퇘기",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "나비한",
    "output": "나비 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "쌍",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'쌍'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 나비 한\n그릇됨: 나비한",
    "output": "'쌍'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 나비 한\n그릇됨: 나비한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "쌍",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "양말한",
    "output": "양말 한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "짝",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'짝'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 양말 한\n그릇됨: 양말한",
    "output": "'짝'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 양말 한\n그릇됨: 양말한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "짝",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "유리세",
    "output": "유리 세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "쪼각",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'쪼각'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 유리 세\n그릇됨: 유리세",
    "output": "'쪼각'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 유리 세\n그릇됨: 유리세",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "쪼각",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "천두",
    "output": "천 두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "쪼박",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'쪼박'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 천 두\n그릇됨: 천두",
    "output": "'쪼박'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 천 두\n그릇됨: 천두",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "쪼박",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "여러가지로온갖",
    "output": "여러가지로 온갖",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "갖은",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'갖은'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 여러가지로 온갖\n그릇됨: 여러가지로온갖",
    "output": "'갖은'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 여러가지로 온갖\n그릇됨: 여러가지로온갖",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "갖은",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "멀고먼또는머나먼",
    "output": "멀고먼 또는 머나먼",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "먼먼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'먼먼'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 멀고먼 또는 머나먼\n그릇됨: 멀고먼또는머나먼",
    "output": "'먼먼'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 멀고먼 또는 머나먼\n그릇됨: 멀고먼또는머나먼",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "먼먼",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "빠짐이나남김이없이전부의",
    "output": "빠짐이나 남김이  없이 전부의",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "모든",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'모든'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 빠짐이나 남김이  없이 전부의\n그릇됨: 빠짐이나남김이없이전부의",
    "output": "'모든'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 빠짐이나 남김이  없이 전부의\n그릇됨: 빠짐이나남김이없이전부의",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "모든",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "못되고고약한",
    "output": "못되고 고약한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "몹쓸",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'몹쓸'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 못되고 고약한\n그릇됨: 못되고고약한",
    "output": "'몹쓸'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 못되고 고약한\n그릇됨: 못되고고약한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "몹쓸",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "모르는사람이나대상을가리킬때에이르는말",
    "output": "모르는 사람이나 대상을 가리킬  때에  이르는말",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "무슨",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'무슨'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 모르는 사람이나 대상을 가리킬  때에  이르는말\n그릇됨: 모르는사람이나대상을가리킬때에이르는말",
    "output": "'무슨'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 모르는 사람이나 대상을 가리킬  때에  이르는말\n그릇됨: 모르는사람이나대상을가리킬때에이르는말",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "무슨",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "처음으로생겨났거나생겨난지오래지않은또는낡은것으로되지않은",
    "output": "처음으로 생겨났거나 생겨난 지 오래지  않은 또는낡은것으로 되지  않은",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "새",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'새'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 처음으로 생겨났거나 생겨난 지 오래지  않은 또는낡은것으로 되지  않은\n그릇됨: 처음으로생겨났거나생겨난지오래지않은또는낡은것으로되지않은",
    "output": "'새'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 처음으로 생겨났거나 생겨난 지 오래지  않은 또는낡은것으로 되지  않은\n그릇됨: 처음으로생겨났거나생겨난지오래지않은또는낡은것으로되지않은",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "새",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "여러가지의모든",
    "output": "여러가지의 모든",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "온갖",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'온갖'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 여러가지의 모든\n그릇됨: 여러가지의모든",
    "output": "'온갖'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 여러가지의 모든\n그릇됨: 여러가지의모든",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "온갖",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "이려하고저러한",
    "output": "이려하고 저러한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "이런저런",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'이런저런'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 이려하고 저러한\n그릇됨: 이려하고저러한",
    "output": "'이런저런'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 이려하고 저러한\n그릇됨: 이려하고저러한",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "이런저런",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "바로전보다한번더지난",
    "output": "바로 전보다 한번 더 지난",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "지지난",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'지지난'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 바로 전보다 한번 더 지난\n그릇됨: 바로전보다한번더지난",
    "output": "'지지난'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 바로 전보다 한번 더 지난\n그릇됨: 바로전보다한번더지난",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "지지난",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "상당하다고인정을하거나자처하는",
    "output": "상당하다고 인정을 하거나 자처하는",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "한다하는",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'한다하는'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 상당하다고 인정을 하거나 자처하는\n그릇됨: 상당하다고인정을하거나자처하는",
    "output": "'한다하는'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 상당하다고 인정을 하거나 자처하는\n그릇됨: 상당하다고인정을하거나자처하는",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "한다하는",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "다음 문장의 띄여쓰기 오류를 수정하라.",
    "input": "서로관계가없이다른",
    "output": "서로 관계가 없이 다른",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_correction",
      "noun": "딴",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  },
  {
    "instruction": "'딴'는 단위명사이다. 다음 문장의 띄여쓰기가 올바른지 판단하라.",
    "input": "올바름: 서로 관계가 없이 다른\n그릇됨: 서로관계가없이다른",
    "output": "'딴'는 단위명사로 앞의 수사와 띄여써야 한다.\n\n올바름: 서로 관계가 없이 다른\n그릇됨: 서로관계가없이다른",
    "metadata": {
      "category": "spacing",
      "type": "unit_noun_explanation",
      "noun": "딴",
      "noun_type": "unit_noun",
      "source": "document_extracted"
    }
  }
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { unitNounsExtractedData };
}
