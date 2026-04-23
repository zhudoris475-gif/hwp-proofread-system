# 朝鲜语发音知识库

## 概述
本知识库从《朝鲜语规范集解说》文档中提取，包含朝鲜语（韩语）发音相关的规则和示例。

## 数据文件

### 1. pronunciation_knowledge.json
知识库格式（JSON数组），每条包含instruction/input/output字段，可直接用于RAG检索。

- 条目数: 312
- 格式: JSON数组

### 2. pronunciation_raw_data.json
原始提取数据，包含更详细的元数据。

- 条目数: 312
- 格式: JSON数组

### 3. knowledge_registry.json
知识库注册信息，包含统计和元数据。

## 数据分类

- phonetic_rule: 36 条
- single_pronunciation: 174 条
- pronunciation_variant: 25 条
- position_pronunciation: 77 条

## 使用方式

### 作为本地知识库
```python
import json

# 加载知识库
with open('data/pronunciation_knowledge.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

# 检索相关知识
def search_knowledge(query, knowledge_base):
    results = []
    for item in knowledge_base:
        if query in item['instruction'] or query in item['output']:
            results.append(item)
    return results
```

### 用于RAG系统
每条知识条目包含:
- `instruction`: 问题/指令
- `input`: 输入（可为空）
- `output`: 详细回答
- `metadata`: 元数据（分类、单词、段落索引等）

## 数据来源
- 文档: 《朝鲜语规范集解说》(2019)
- 出版社: 延边教育出版社
- 编写: 中国朝鲜语审订委员会
