# Synthesize 提示模板

## 用法

复制下面的模板到 Claude Code 对话中，替换相关部分。

---

## 模板 1：总结当前任务

```
请帮我调用 research-router 总结当前任务的历史记录：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py synthesize
```

---

## 模板 2：总结指定任务

```
请帮我调用 research-router 总结任务 [任务名] 的历史记录：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py synthesize --task [任务名]
```

---

## 模板 3：指定分析模型

```
请帮我调用 research-router 用 [模型] 来总结任务历史：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py synthesize --analyzer [qwen|gemini] --task [任务名]
```

---

## 示例

```
请帮我调用 research-router 总结 et-model 任务的所有讨论：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py synthesize --task et-model
```

---

## 典型工作流

```
# 1. 先做几轮 ask/compare/review
python main.py ask qwen "什么是潜在蒸散发？" --task et-model
python main.py compare gemini qwen "Penman-Monteith 和 Priestley-Taylor 有什么区别？" --task et-model
python main.py review codex qwen "实现 PM 方程的 Python 代码" --task et-model

# 2. 最后用 synthesize 收束
python main.py synthesize --task et-model
```
