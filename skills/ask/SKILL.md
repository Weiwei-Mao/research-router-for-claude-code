---
name: ask
description: Ask a single AI model (codex, gemini, or qwen) a question and get a response
tags: ["ask", "question", "single-model"]
---

# Ask — Single Model Q&A

## When to Use

Use this skill when the user wants to:
- Ask a question to a specific AI model
- Get a quick answer from a single model
- Send a prompt to codex, gemini, or qwen
- The user says things like "ask qwen", "ask gemini", "用 qwen 问一下", "让 codex 看看"

## Input

The user should provide:
1. **Model** (optional): codex, gemini, or qwen. If omitted, auto-select based on prompt content.
2. **Prompt** (required): The question or instruction to send.
3. **Task** (optional): A task name to group the conversation. Default: "default".

## Instructions

1. Parse the user's request to extract the model name, prompt, and optional task name.
2. If no model specified, omit it — the system will auto-select (qwen for simple, gemini for research-oriented).
3. Run the following command:

```bash
python main.py ask [MODEL] "PROMPT" [--task TASK_NAME]
```

Examples:
- `main.py ask "what is overfitting?"` — auto-select model
- `main.py ask qwen "explain LSTM"` — specify qwen
- `main.py ask gemini "research methodology"` — specify gemini
- `main.py ask codex "fix this bug"` — specify codex

4. Return the model's response to the user.
5. Mention which model was used and that the result was saved to the task session.

## Output Format

Present the response as:

> **[model-name]** responded:
>
> [response content]
>
> *Saved to task: [task-name]*
