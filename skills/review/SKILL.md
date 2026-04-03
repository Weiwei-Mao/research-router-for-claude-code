---
name: review
description: Have one model execute a task and another model review its output for correctness, risks, and improvements
tags: ["review", "execute", "audit", "code-review"]
---

# Review — Execute + Review

## When to Use

Use this skill when the user wants to:
- Have a model write code or produce output, then have another model review it
- Double-check a model's work with a second opinion
- Get a structured code review or analysis audit
- The user says things like "review", "审查", "let X review Y", "double-check", "帮我审查"

## Input

The user should provide:
1. **Executor** (optional): Model to produce the initial output. Auto-selected if omitted.
2. **Reviewer** (optional): Model to review the output. Auto-selected if omitted.
3. **Prompt** (required): The task or question.
4. **Task** (optional): Task name for session tracking.

Auto-selection rules:
- Code-related prompts: codex executes, qwen reviews
- General prompts: qwen executes, gemini reviews

## Instructions

1. Parse the user's request to extract executor, reviewer, prompt, and options.
2. If models are not specified, omit them — the system auto-selects based on prompt content.
3. Run the following command:

```bash
python main.py review [EXECUTOR REVIEWER] "PROMPT" [--task TASK_NAME]
```

Examples:
- `main.py review "write a quicksort"` — auto-select (code → codex exec, qwen review)
- `main.py review codex qwen "implement PM equation"` — specify both
- `main.py review qwen gemini "explain water balance"` — specify both

4. The output has two sections:
   - **EXECUTOR OUTPUT**: The first model's work
   - **REVIEW**: Structured review (正确点、潜在问题、风险点、修改建议)
5. Present both sections to the user.

## Output Format

Present the response as:

> **[executor] executed, [reviewer] reviewed**
>
> ### EXECUTOR OUTPUT ([model])
> [executor response]
>
> ### REVIEW ([model])
> [review content with 正确点/潜在问题/风险点/修改建议]
>
> *Saved to task: [task-name]*
