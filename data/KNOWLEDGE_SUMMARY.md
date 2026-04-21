# 朝鲜语规范知识库完整汇总报告

## 📊 总体统计

| 知识库类别 | 条目数量 |
|-----------|---------|
| 发音 (Pronunciation) | 312 |
| 分写 (Spacing) | 118 |
| 语法 (Grammar) | 37 |
| 构词 (Word Formation) | 184 |
| 标点 (Punctuation) | 87 |
| **总计** | **738** |

## 📁 文件结构

```
data/
├── pronunciation_knowledge.json      # 发音规则知识库 (312条)
├── pronunciation_raw_data.json       # 发音原始数据
├── spacing_knowledge.json            # 分写规则知识库 (118条)
├── spacing_raw_data.json             # 分写原始数据
├── grammar_knowledge.json            # 语法规则知识库 (37条)
├── grammar_raw_data.json             # 语法原始数据
├── wordformation_knowledge.json      # 构词规则知识库 (184条)
├── wordformation_raw_data.json       # 构词原始数据
├── punctuation_knowledge.json        # 标点规则知识库 (87条)
├── punctuation_raw_data.json         # 标点原始数据
├── knowledge_registry.json           # 知识库注册信息
├── README.md                         # 使用说明
└── KNOWLEDGE_SUMMARY.md              # 本汇总报告
```

## 🎯 知识库格式

每个知识库条目包含以下字段：

```json
{
  "instruction": "问题/指令",
  "input": "输入内容（可为空）",
  "output": "详细回答",
  "metadata": {
    "category": "类别",
    "type": "子类型",
    "paragraph_index": 段落索引
  }
}
```

## 📖 使用方式

### 1. 加载知识库

```python
import json

# 加载各类知识库
knowledge_bases = {}
files = {
    'pronunciation': 'pronunciation_knowledge.json',
    'spacing': 'spacing_knowledge.json',
    'grammar': 'grammar_knowledge.json',
    'wordformation': 'wordformation_knowledge.json',
    'punctuation': 'punctuation_knowledge.json'
}

for name, filename in files.items():
    with open(f'data/{filename}', 'r', encoding='utf-8') as f:
        knowledge_bases[name] = json.load(f)
```

### 2. 检索知识

```python
def search_knowledge(query, knowledge_base, top_k=5):
    # 基于关键词检索知识
    results = []
    for item in knowledge_base:
        score = 0
        if query in item['instruction']:
            score += 3
        if query in item['output']:
            score += 1
        if 'metadata' in item:
            if query in str(item['metadata'].get('word', '')):
                score += 5
        if score > 0:
            results.append((score, item))
    
    # 按分数排序
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:top_k]]

# 示例：搜索发音规则
results = search_knowledge('낮고', knowledge_bases['pronunciation'])
```

### 3. 用于RAG系统

```python
# 构建向量索引（需要sentence-transformers）
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 编码所有知识
all_knowledge = []
for kb in knowledge_bases.values():
    all_knowledge.extend(kb)

knowledge_texts = [f"{k['instruction']} {k['output']}" for k in all_knowledge]
knowledge_embeddings = model.encode(knowledge_texts)

# 搜索
def semantic_search(query, embeddings, knowledge_base, top_k=5):
    query_emb = model.encode([query])
    scores = np.dot(embeddings, query_emb.T).squeeze()
    top_indices = scores.argsort()[-top_k:][::-1]
    return [knowledge_base[i] for i in top_indices]
```

## 📚 数据来源

- **文档**: 《朝鲜语规范集解说》(2019)
- **出版社**: 延边教育出版社
- **编写**: 中国朝鲜语审订委员会

## 🔧 提取工具

- `extract_pronunciation_knowledge.py` - 发音知识提取
- `extract_spacing_knowledge.py` - 分写知识提取
- `extract_grammar_knowledge.py` - 语法知识提取
- `extract_wordformation_knowledge.py` - 构词知识提取
- `extract_punctuation_knowledge.py` - 标点知识提取

## 📝 注意事项

1. 知识库中的数据为本地知识库格式，**不直接用于模型训练**
2. 可用于RAG（检索增强生成）系统
3. 可用于构建朝鲜语规范检查工具
4. 数据包含原始段落索引，可追溯到原文
5. 所有知识库条目均包含instruction/input/output/metadata字段

## 🎯 应用场景

1. **朝鲜语学习助手**: 提供发音、语法、分写等规则查询
2. **规范检查工具**: 检查文本是否符合朝鲜语规范
3. **RAG知识库**: 为AI模型提供准确的规范知识
4. **教学辅助**: 为教师和学生提供规则参考

---

*生成时间: 2024*
*总条目数: 738*
*数据来源: 《朝鲜语规范集解说》(2019)
