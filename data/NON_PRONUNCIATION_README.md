# 非发音类知识库

## 概述

本知识库包含分写、语法、构词、标点四大类别的朝鲜语规范知识，**不含发音类数据**。

## 文件说明

### 1. non_pronunciation_knowledge.json
完整知识库数据（JSON数组格式）
- 条目数: 426
- 格式: JSON数组

### 2. non_pronunciation_knowledge.jsonl
JSONL格式（每行一个JSON对象）
- 条目数: 426
- 格式: JSON Lines

### 3. non_pronunciation_stats.json
统计报告

## 数据分类

- **spacing**: 118 条
- **grammar**: 37 条
- **wordformation**: 184 条
- **punctuation**: 87 条

**总计**: 426 条

## 数据格式

```json
{
  "instruction": "问题/指令",
  "input": "输入内容（可为空）",
  "output": "详细回答",
  "metadata": {
    "category": "类别",
    "type": "子类型",
    "source_category": "数据来源（spacing/grammar/wordformation/punctuation）",
    "paragraph_index": 段落索引
  }
}
```

## 使用示例

```python
import json

# 加载数据
with open('non_pronunciation_knowledge.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

# 按类别筛选
def filter_by_category(data, category):
    return [item for item in data if item['metadata'].get('source_category') == category]

# 获取所有分写规则
spacing_rules = filter_by_category(knowledge, 'spacing')

# 搜索
def search(query, data):
    results = []
    for item in data:
        if query in item['instruction'] or query in item['output']:
            results.append(item)
    return results
```

## 数据来源

- 文档: 《朝鲜语规范集解说》(2019)
- 出版社: 延边教育出版社
- 编写: 中国朝鲜语审订委员会

---

*生成时间: 2024*
*总条目数: 426*
