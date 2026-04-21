# 朝鲜语规范集解说 - 完整知识库汇总报告

## 📊 总体统计

| 知识库类别 | 条目数量 |
|-----------|---------|
| 发音规则 (Pronunciation) | 312 |
| 分写规则 (Spacing) | 118 |
| 语法规则 (Grammar) | 37 |
| 构词规则 (Word Formation) | 184 |
| 标点规则 (Punctuation) | 87 |
| 书籍内容 (Book Content) | 239 |
| **总计** | **977** |

## 📁 完整文件结构

```
data/
├── 发音类 (本地知识库，不用于训练)
│   ├── pronunciation_knowledge.json      # 发音规则 (312条)
│   └── pronunciation_raw_data.json
│
├── 非发音类 (可用于训练)
│   ├── non_pronunciation_knowledge.json  # 合并数据 (426条)
│   ├── non_pronunciation_knowledge.jsonl # JSONL格式
│   ├── spacing_knowledge.json            # 分写规则 (118条)
│   ├── grammar_knowledge.json            # 语法规则 (37条)
│   ├── wordformation_knowledge.json      # 构词规则 (184条)
│   └── punctuation_knowledge.json        # 标点规则 (87条)
│
├── 书籍内容
│   ├── book_content_knowledge.json       # 书籍内容 (239条)
│   └── book_content_raw.json
│
├── 原始数据
│   └── *_raw_data.json                   # 各类原始数据
│
└── 文档
    ├── knowledge_registry.json           # 注册信息
    ├── KNOWLEDGE_SUMMARY.md              # 汇总报告
    ├── NON_PRONUNCIATION_README.md       # 非发音类说明
    └── FINAL_SUMMARY.md                  # 本报告
```

## 🎯 数据分类说明

### 1. 发音类 (Pronunciation) - 312条
- **用途**: 本地知识库，RAG检索
- **内容**: 发音变体、音变规则、位置发音
- **格式**: instruction/input/output/metadata

### 2. 分写规则 (Spacing) - 118条
- **用途**: 可用于训练
- **内容**: 띄여쓰기/붙여쓰기规则、助词分写、依存名词分写
- **格式**: instruction/input/output/metadata

### 3. 语法规则 (Grammar) - 37条
- **用途**: 可用于训练
- **内容**: 词尾规则、词类规则、活用规则、敬语规则
- **格式**: instruction/input/output/metadata

### 4. 构词规则 (Word Formation) - 184条
- **用途**: 可用于训练
- **内容**: 后缀构词、前缀构词、复合词、派生词
- **格式**: instruction/input/output/metadata

### 5. 标点规则 (Punctuation) - 87条
- **用途**: 可用于训练
- **内容**: 引号、括号、句号、逗号等使用规则
- **格式**: instruction/input/output/metadata

### 6. 书籍内容 (Book Content) - 239条
- **用途**: 可用于训练
- **内容**: 章节结构、正误对比、详细解释、编号规则
- **格式**: instruction/input/output/metadata

## 📈 数据分布

```
发音类:       312条  (26.8%)
构词规则:     184条  (15.8%)
分写规则:     118条  (10.1%)
标点规则:      87条   (7.5%)
书籍内容:     239条  (20.5%)
语法规则:      37条   (3.2%)
─────────────────────────
总计:       977条 (100%)
```

## 💡 使用建议

### 1. 发音类数据
```python
# 作为本地知识库使用
with open('pronunciation_knowledge.json', 'r', encoding='utf-8') as f:
    pron_knowledge = json.load(f)

# RAG检索
def search_pronunciation(query):
    results = []
    for item in pron_knowledge:
        if query in item['instruction'] or query in item['output']:
            results.append(item)
    return results
```

### 2. 非发音类数据（训练用）
```python
# 加载所有非发音数据
with open('non_pronunciation_knowledge.json', 'r', encoding='utf-8') as f:
    training_data = json.load(f)

# 或按类别加载
with open('spacing_knowledge.json', 'r', encoding='utf-8') as f:
    spacing_data = json.load(f)
```

### 3. 完整数据加载
```python
import json
import glob
import os

# 加载所有知识库
all_knowledge = {}
files = glob.glob('data/*_knowledge.json')
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    category = os.path.basename(f).replace('_knowledge.json', '')
    all_knowledge[category] = data
```

## 🔧 提取工具列表

1. `extract_pronunciation_knowledge.py` - 发音知识提取
2. `extract_spacing_knowledge.py` - 分写知识提取
3. `extract_grammar_knowledge.py` - 语法知识提取
4. `extract_wordformation_knowledge.py` - 构词知识提取
5. `extract_punctuation_knowledge.py` - 标点知识提取
6. `extract_book_content.py` - 书籍内容提取
7. `merge_non_pronunciation_data.py` - 合并非发音数据

## 📚 数据来源

- **文档**: 《朝鲜语规范集解说》(2019)
- **出版社**: 延边教育出版社
- **编写**: 中国朝鲜语审订委员会
- **文档段落数**: 3,342个

## 📝 数据格式统一

所有知识库条目均采用统一格式：

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

## 🎯 应用场景

1. **朝鲜语学习助手**: 提供全面的规范查询
2. **规范检查工具**: 检查文本是否符合规范
3. **RAG知识库**: 为AI模型提供准确知识
4. **模型训练**: 非发音类数据可用于微调
5. **教学辅助**: 为教师和学生提供参考

---

*生成时间: 2024*
*总条目数: 977*
*数据来源: 《朝鲜语规范集解说》(2019)*
*文档段落: 3,342个*