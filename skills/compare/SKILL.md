---
name: compare
description: Send the same prompt to multiple AI models and analyze their responses for consensus and disagreements
tags: ["compare", "multi-model", "analysis", "consensus"]
---

# Compare — Multi-Model Comparison

## When to Use

Use this skill when the user wants to:
- Compare answers from multiple models on the same question
- Cross-validate a response to avoid single-model bias
- Get different perspectives on a research question
- The user says things like "compare", "对比", "多模型比较", "cross-validate", "让几个模型都看看"

## Input

The user should provide:
1. **Models** (optional): Two or more of codex, gemini, qwen. If omitted, auto-select based on prompt.
2. **Prompt** (required): The question to send to all models.
3. **Analyzer** (optional): Model to write the analysis summary. Default: qwen.
4. **Task** (optional): Task name for session tracking.

## Instructions

1. Parse the user's request to extract models, prompt, and options.
2. If no models specified, provide only the prompt — the system auto-selects (gemini + qwen by default; adds codex for code-related prompts).
3. Run the following command:

```bash
python main.py compare [MODEL1 MODEL2 ...] --prompt "PROMPT" [--analyzer ANALYZER] [--task TASK_NAME]
```

Examples:
- `main.py compare --prompt "what is overfitting?"` — auto-select models
- `main.py compare gemini qwen --prompt "LSTM vs GRU"` — specify two models
- `main.py compare codex gemini qwen --prompt "debug script"` — specify three models
- `main.py compare gemini qwen --prompt "question" --analyzer qwen` — specify analyzer

4. The output has two sections:
   - **RAW OUTPUT**: Each model's full response
   - **ANALYSIS**: Structured comparison (一致点、分歧点、风险点、建议)
5. Present both sections to the user.

## Output Format

Present the response as:

> **Comparing [models] on: [prompt summary]**
>
> ### RAW OUTPUT
> **[model-a]**
> [response]
>
> **[model-b]**
> [response]
>
> ### ANALYSIS
> [analysis content]
>
> *Saved to task: [task-name]*
