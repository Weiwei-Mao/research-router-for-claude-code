# Compare 提示模板

## 用法

复制下面的模板到 Claude Code 对话中，替换相关部分。

---

## 模板 1：自动选模型比较

```
请帮我调用 research-router 做多模型比较：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py compare "[问题]"
```

---

## 模板 2：指定模型比较

```
请帮我调用 research-router 比较 [模型1] 和 [模型2] 的回答：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py compare [模型1] [模型2] "[问题]"
```

---

## 模板 3：代码问题比较（自动加 codex）

```
请帮我调用 research-router 比较多个模型对这段代码的看法：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py compare "[代码相关的问题]"
```

---

## 示例

```
请帮我调用 research-router 比较 gemini 和 qwen 的回答：

python c:/Users/wei/Desktop/research-router-for-claude-code/main.py compare gemini qwen "LSTM 和 GRU 在水文时序预测中哪个更合适？为什么？" --task lstm-vs-gru
```
