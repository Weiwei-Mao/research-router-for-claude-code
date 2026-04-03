# Ask 提示模板

## 用法

复制下面的模板到 Claude Code 对话中，替换 `[问题]` 部分。

---

## 模板 1：快速问答（自动选模型）

```
请帮我调用 research-router 问一个问题：

python main.py ask "[问题]"
```

---

## 模板 2：指定模型

```
请帮我调用 research-router 向 [模型] 提问：

python main.py ask [qwen|gemini|codex] "[问题]"
```

---

## 模板 3：在指定任务下提问

```
请帮我调用 research-router 在任务 [任务名] 下提问：

python main.py ask "[问题]" --task [任务名]
```

---

## 示例

```
请帮我调用 research-router 向 qwen 提问：

python main.py ask qwen "水文模型中如何处理土壤异质性问题？"
```
