---
name: synthesize
description: Summarize an entire task's multi-model discussion history into a structured research synthesis
tags: ["synthesize", "summarize", "research", "conclusion"]
---

# Synthesize — Task Synthesis

## When to Use

Use this skill when the user wants to:
- Summarize all discussions within a task (ask, compare, review entries)
- Get a structured conclusion after multiple rounds of multi-model interaction
- Review what has been discussed and what remains uncertain
- The user says things like "synthesize", "总结", "summarize task", "收束结论", "帮我整理"

## Input

The user should provide:
1. **Task** (optional): Task name to synthesize. Default: current active task.
2. **Analyzer** (optional): Model to write the synthesis. Default: qwen.

## Instructions

1. Determine the task name. If the user says "current" or doesn't specify one, use the current active task.
2. Run the following command:

```bash
C:/Users/wei/anaconda3/python.exe "c:/Users/wei/Desktop/research-router-for-claude-code/main.py" synthesize [--task TASK_NAME] [--analyzer ANALYZER]
```

Examples:
- `main.py synthesize` — synthesize current task
- `main.py synthesize --task my-research` — specify task
- `main.py synthesize my-research` — positional task name
- `main.py synthesize --analyzer gemini` — use gemini for analysis

3. The output is a structured synthesis with six sections:
   - 当前问题背景总结
   - 已尝试的方案/思路
   - 各模型的主要分歧点
   - 已确认的可靠结论
   - 仍存在的不确定性
   - 下一步建议

4. Present the full synthesis to the user.

## Output Format

Present the response as:

> **Synthesis of task: [task-name]**
>
> [full synthesis content]
>
> *Synthesis saved to task: [task-name]*
