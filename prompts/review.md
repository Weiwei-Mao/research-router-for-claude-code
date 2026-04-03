# Review 提示模板

## 用法

复制下面的模板到 Claude Code 对话中，替换相关部分。

---

## 模板 1：自动选模型 review

```
请帮我调用 research-router 做执行 + 审查：

python main.py review "[问题或代码]"
```

代码类问题会自动用 codex 执行 + qwen 审查。
普通问题会自动用 qwen 执行 + gemini 审查。

---

## 模板 2：手动指定执行和审查模型

```
请帮我调用 research-router，让 [执行模型] 执行，[审查模型] 审查：

python main.py review [执行模型] [审查模型] "[问题或代码]"
```

---

## 模板 3：代码审查

```
请帮我调用 research-router 对以下代码做双模型审查：

python main.py review "[代码或代码描述]"
```

---

## 示例

```
请帮我调用 research-router，让 codex 写代码，qwen 审查：

python main.py review codex qwen "写一个 Python 函数计算 Penman-Monteith 蒸散发方程" --task et-model
```
