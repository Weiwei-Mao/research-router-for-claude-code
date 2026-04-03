# Research Router 使用指南

## 命令一览

| 命令 | 用途 | 模型选择 |
|------|------|---------|
| `ask` | 单模型问答 | 默认 qwen，研究类用 gemini |
| `compare` | 多模型并行比较 | 默认 gemini + qwen，代码类加 codex |
| `review` | 执行 + 审查 | 代码：codex 执行 + qwen 审查；普通：qwen 执行 + gemini 审查 |
| `synthesize` | 总结 task 历史 | 默认 qwen 分析 |
| `task` | 任务管理 | — |

---

## ask — 单模型调用

### 基本用法

```bash
# 自动选择模型
python main.py ask "你的问题"

# 手动指定模型
python main.py ask qwen "你的问题"
python main.py ask gemini "你的问题"
python main.py ask codex "你的问题"
```

### 推荐场景

| 模型 | 适合什么时候 |
|------|-------------|
| **qwen**（默认） | 一般问答、快速验证、中文友好、免费 |
| **gemini** | 研究分析、方法论讨论、需要深度推理时 |
| **codex** | 代码编写、debug、重构、技术实现 |

### 使用 --task 管理上下文

```bash
# 在同一个研究任务下持续对话
python main.py ask qwen "什么是土壤导水率？" --task soil-hydrology
python main.py ask gemini "有哪些测量方法？" --task soil-hydrology
```

---

## compare — 多模型比较

### 基本用法

```bash
# 自动选择模型（默认 gemini + qwen）
python main.py compare "你的问题"

# 代码相关问题自动加入 codex
python main.py compare "debug this python script error"

# 手动指定模型
python main.py compare codex gemini "你的问题"
python main.py compare qwen gemini "你的问题" --analyzer qwen
```

### 输出结构

```
=== RAW OUTPUT ===
[model_a]
...原始回答...

[model_b]
...原始回答...

=== ANALYSIS ===
...自动分析：一致点、分歧点、风险点、建议...
```

### 推荐场景

- 不确定单一模型是否可靠时，用 compare 交叉验证
- 重要科研决策前，用 compare 收集不同视角
- 代码方案选型时，用 compare 对比实现思路

---

## review — 执行 + 审查

### 基本用法

```bash
# 自动选择（代码类：codex 执行 + qwen 审查）
python main.py review "fix this sorting bug in Python"

# 自动选择（普通类：qwen 执行 + gemini 审查）
python main.py review "explain the water balance equation"

# 手动指定
python main.py review codex qwen "你的代码或问题"
python main.py review qwen gemini "你的问题"
```

### 输出结构

```
=== EXECUTOR OUTPUT ===
...执行模型的输出...

=== REVIEW ===
...审查模型的结构化审查...
- 正确点
- 潜在问题
- 风险点
- 修改建议
```

### 推荐场景

- 让 codex 写代码，再让 qwen 审查逻辑和边界
- 让 qwen 写分析，再让 gemini 检查推理链
- 关键代码上线前的双模型验证

---

## synthesize — 任务总结

### 基本用法

```bash
# 总结当前任务
python main.py synthesize

# 总结指定任务
python main.py synthesize --task soil-hydrology
python main.py synthesize soil-hydrology

# 指定分析模型
python main.py synthesize --analyzer gemini
```

### 输出结构

```
=== SYNTHESIZE ===
1. 当前问题背景总结
2. 已尝试的方案/思路
3. 各模型的主要分歧点
4. 已确认的可靠结论
5. 仍存在的不确定性
6. 下一步建议（科研导向）
```

### 推荐场景

- 一轮多模型讨论结束后，用 synthesize 收束结论
- 研究笔记整理时，快速回顾已有结论和待解决问题
- 写论文或报告前，用 synthesize 生成研究进展摘要

---

## 模型选择速查

### 什么时候用 codex

- 写代码、debug、重构
- 技术方案选型
- 代码 review 执行端

### 什么时候用 gemini

- 研究方法论讨论
- 深度推理和理论分析
- 多语言（中文 + 英文）场景
- compare 的默认成员

### 什么时候用 qwen

- 日常问答（默认模型）
- 快速验证想法
- 作为 analyzer 做 compare-analysis 和 synthesize
- 免费无限调用
