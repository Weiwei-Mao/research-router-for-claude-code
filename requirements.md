多模型科研助手插件需求文档 v0.1
1. 项目名称

暂定：research-router-for-claude-code

2. 项目目标

在 Claude Code CLI / VS Code 插件环境 中，提供一个轻量、多模型、可交叉验证的科研辅助系统，服务于水文学/陆面模型/机器学习研究中的代码编写、方法讨论、实验设计、结果解释与多模型互审。

系统目标不是做重型多 agent 平台，而是提供一个低复杂度的本地插件/脚本层，让用户可以方便地：

调用 GLM、Codex、Gemini、Qwen
对同一问题做并行比较
让一个模型执行，另一个模型审查
维护任务级共享上下文
在成本、速度、能力之间做平衡
3. 背景与约束
3.1 用户现状
主工作场景：科研，不是高频软件工程
主要任务：
水文模型、陆面模型相关代码
数据处理脚本
机器学习/深度学习研究代码
方法设计、实验解释、结果分析
当前模型资源：
GLM 5.1：已作为 Claude Code 底层主模型
Codex：现有 Team 方案，未来可能切 Pro
Gemini：教育账户可用
Qwen：免费
使用偏好：
更相信 Codex 的技术判断
但担心单模型偏差，希望多模型交叉验证
不追求复杂系统，不要 UI
3.2 约束
仅在 CLI / VS Code 中使用
不引入复杂前端
不以“全自动长期自治 agent”为目标
尽量兼容 Windows
尽量复用现有 CLI 调用方式
4. 产品定位

这是一个Claude Code 插件/本地路由层，不是独立产品界面。
核心定位：

用 Claude Code 作为统一入口，用本地 router 统一调度 GLM / Codex / Gemini / Qwen，支持科研任务的 compare / review / synthesize 工作流。

5. 关键设计原则
轻量优先：先可用，再优雅
Codex 高权重但不强制全局默认：关键代码任务优先 Codex
任务级上下文：不做复杂长期记忆，按 task/session 管理
低摩擦调用：尽量通过少量命令完成常见工作
可扩展：后续可加规则路由、缓存、更多 provider
可审计：保留各模型原始回答，便于科研复查
6. 用户故事
6.1 并行比较

作为科研用户，我希望把同一个问题同时发给多个模型，对比它们的思路和结论，避免被单一模型误导。

6.2 执行 + 审查

作为科研用户，我希望让一个模型写/改代码，再让另一个模型审查逻辑、边界条件和潜在错误。

6.3 任务上下文复用

作为科研用户，我希望一个研究任务可以维护共享背景，让多次追问和多模型调用都基于同一上下文。

6.4 成本控制

作为科研用户，我希望普通问题优先走低成本路径，重要代码和高风险问题再调动更强模型。

7. 核心功能范围
7.1 必做功能（MVP）
A. 单模型调用

支持调用：

glm
codex
gemini
qwen

命令示例：

/ask codex ...
/ask gemini ...
B. 并行比较

同一 prompt 发给多个模型，并输出分模型结果。

命令示例：

/compare codex gemini "..."
C. 执行 + 审查

一个模型执行，一个模型检查。

命令示例：

/review codex by gemini "修复这个脚本并审查"
D. 综合汇总

将多个模型结果整合成：

一致点
分歧点
风险点
建议下一步

命令示例：

/synthesize current
E. 任务级 session

支持：

新建任务
切换任务
查看当前任务上下文
将模型输出写入任务记录
F. 统一输出格式

至少保证：

模型名
时间
原始输出
摘要
是否为 review / compare 结果
7.2 非必做但建议预留
简单路由规则
并发调用
token / 调用次数日志
prompt 模板
导出 markdown 报告
8. 不做的内容

当前阶段不做：

Web UI
复杂数据库
向量检索系统
全自动多 agent 长时间自治运行
自动 PR / CI/CD 流水线
重型 MCP 编排体系
9. 推荐工作流
工作流 1：普通科研问答
默认：GLM
可选：Gemini 作为第二意见
工作流 2：关键代码任务
默认：Codex 执行
Gemini 或 Qwen 审查
最后 synthesize
工作流 3：高风险科研判断
Codex + Gemini 并行
Qwen 可选做低成本 baseline
synthesize 输出最终摘要
10. 命令设计草案
10.1 ask
/ask <model> "<prompt>"
10.2 compare
/compare <model1> <model2> [model3...] "<prompt>"
10.3 review
/review <executor> by <reviewer> "<prompt>"
10.4 synthesize
/synthesize [task-id|current]
10.5 task
/task new <name>
/task use <name>
/task show
11. 目录结构建议
research-router-for-claude-code/
  plugin/
    commands/
    agents/
    hooks/
  router/
    main.py
    providers/
      codex.py
      gemini.py
      qwen.py
      glm.py
    sessions/
    templates/
  docs/
    requirements.md
    architecture.md
  README.md
12. 技术实现建议
12.1 顶层形式

优先实现为 Claude Code plugin。Claude Code 官方插件就是用来打包 commands、agents、hooks、MCP servers 的。

12.2 中间层

本地 router 脚本，负责：

调用各模型 CLI
统一参数
管理 session
保存结果
提供 compare/review/synthesize 逻辑
12.3 Claude Code 内部能力使用建议
commands：作为主要入口
subagents：只做少量角色化封装，例如 coder-codex、reviewer-gemini
hooks：只做自动加载/写回 session，别搞太重
skills：可选，用于补充固定说明，不做主架构
Claude Code 官方文档也明确把 plugins、subagents、hooks、skills 作为不同层次的扩展机制。
13. OMC 参考策略
13.1 可以参考 OMC 的内容
命令命名方式
ask-codex / ask-gemini 的 provider 思路
多 provider 协作模式
插件化组织方式
13.2 不建议直接 fork 作为起点的原因
OMC 功能面较大，超出当前需求
维护节奏快，行为可能变化
最近 release 仍在修 ask-codex / ask-gemini 行为、路径可移植性、worker pane 等兼容性问题，对你的“轻量科研助手”目标来说有点重。
13.3 结论

建议：参考 OMC，不直接依赖 OMC。

14. MVP 里程碑
M1：最小可用
/ask
/compare
/task
session 文件可读写
四个 provider 至少接通三个
M2：研究可用
/review
/synthesize
统一输出格式
task 级上下文稳定
M3：长期使用
路由规则
token / 调用日志
导出研究记录
更好的 prompt 模板
15. 成功标准

满足以下条件即认为 MVP 成功：

能在 Claude Code CLI/VS Code 中直接调用
能稳定调起 Codex、Gemini、Qwen、GLM 中至少三个
能完成 compare / review / synthesize
能以 task 为单位保存上下文
使用复杂度足够低，用户一周内可自然上手