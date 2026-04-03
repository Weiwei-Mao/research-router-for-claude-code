# Research Router for Claude Code

轻量、多模型、可交叉验证的科研辅助工具。在 Claude Code / VS Code 环境中，通过 CLI 统一调度 Codex、Gemini、Qwen，支持科研任务的 compare / review / synthesize 工作流。

## 快速开始

```bash
# Python 路径（如需要）
C:\Users\wei\anaconda3\python.exe

# 基本命令
python main.py ask "你的问题"
python main.py compare "你的问题"
python main.py review "你的问题"
python main.py synthesize

# 任务管理
python main.py task new my-research
python main.py task list
python main.py task show
```

## 项目结构

```
research-router-for-claude-code/
  main.py              # CLI 入口
  router.py            # 路由：ask/compare/review/synthesize
  strategy.py          # 策略：根据 prompt 自动选模型
  config.py            # 配置加载
  config.json          # 统一配置文件
  provider/            # 模型提供者
    base.py            # 基类（subprocess 调用逻辑）
    codex.py           # Codex (codex.exe)
    gemini.py          # Gemini (gemini CLI)
    qwen.py            # Qwen (qwen CLI)
  session/             # Session 管理
    manager.py         # JSON 读写
  data/sessions/       # Session 存储目录
  prompts/             # 可复用提示模板
  docs/
    requirements.md    # 需求文档
    usage.md           # 详细使用指南
```

## 可用模型

| 模型 | CLI 命令 | 特点 |
|------|---------|------|
| **codex** | `codex.exe exec` | 代码能力强，技术判断可靠 |
| **gemini** | `gemini -p` | 研究分析、深度推理、中文好 |
| **qwen** | `qwen` | 免费快速、中文友好、默认模型 |

> GLM（Claude Code 自身）不作为 subprocess provider 调用。

## 命令详解

### ask — 单模型调用

```bash
python main.py ask "你的问题"                    # 自动选模型
python main.py ask qwen "你的问题"               # 指定 qwen
python main.py ask gemini "研究类问题" --task x  # 指定任务
```

### compare — 多模型比较

```bash
python main.py compare "你的问题"                # 自动选模型
python main.py compare gemini qwen "你的问题"    # 手动指定
```

输出包含 RAW OUTPUT + ANALYSIS（一致点、分歧点、风险点、建议）。

### review — 执行 + 审查

```bash
python main.py review "代码或问题"               # 自动选模型
python main.py review codex qwen "写个排序函数"  # 手动指定
```

输出包含 EXECUTOR OUTPUT + 结构化 REVIEW（正确点、潜在问题、风险点、修改建议）。

### synthesize — 任务总结

```bash
python main.py synthesize                        # 总结当前任务
python main.py synthesize --task my-research     # 总结指定任务
```

输出包含：背景总结、已尝试方案、分歧点、可靠结论、不确定性、下一步建议。

### task — 任务管理

```bash
python main.py task new my-research   # 新建任务
python main.py task use my-research   # 切换当前任务
python main.py task list              # 列出所有任务
python main.py task show              # 查看当前任务历史
```

## 在 Claude Code 中怎么用

### 方式 1：安装为本地插件（推荐）

安装后可直接用 `/ask`、`/compare`、`/review`、`/synthesize` 调用。

**步骤 1：注册插件**

编辑项目级 `.claude/settings.local.json`，添加 `enabledPlugins`：

```json
{
  "permissions": { ... },
  "enabledPlugins": {
    "research-router": {
      "localPath": "c:/Users/wei/Desktop/research-router-for-claude-code"
    }
  }
}
```

**步骤 2：重启 Claude Code**

重新打开 Claude Code 会话，插件自动加载。

**步骤 3：使用技能**

```
/ask qwen "什么是潜在蒸散发？"
/compare gemini qwen "LSTM 和 GRU 哪个更适合水文预测？"
/review codex qwen "实现 Penman-Monteith 方程的 Python 代码"
/synthesize --task et-model
```

插件目录结构：
```
.claude-plugin/plugin.json    # 插件清单
skills/
  ask/SKILL.md                # /ask 技能
  compare/SKILL.md            # /compare 技能
  review/SKILL.md             # /review 技能
  synthesize/SKILL.md         # /synthesize 技能
```

### 方式 2：直接让我（Claude Code）帮你调用

在对话中这样说：

```
帮我用 qwen 问一下 LSTM 和 GRU 在水文时序预测中哪个更合适
```

我会执行：
```bash
python c:/Users/wei/Desktop/research-router-for-claude-code/main.py ask qwen "LSTM 和 GRU 在水文时序预测中哪个更合适？"
```

### 方式 3：用提示模板

`prompts/` 目录下有 4 个可复用模板（ask.md、compare.md、review.md、synthesize.md）。直接复制到对话中使用。

### 典型科研工作流

```
第一步：探索问题
  /ask qwen "什么是潜在蒸散发？" --task et-model

第二步：多模型对比
  /compare gemini qwen "PM 方程和 PT 方程有什么区别？" --task et-model

第三步：代码审查
  /review codex qwen "实现 PM 方程的 Python 代码" --task et-model

第四步：总结
  /synthesize --task et-model
```

### 自动模型选择（strategy）

不指定模型时，系统根据 prompt 内容自动选择：

| 命令 | 简单 prompt | 代码相关 | 研究相关 |
|------|------------|---------|---------|
| ask | qwen | qwen | gemini |
| compare | gemini, qwen | codex, gemini, qwen | gemini, qwen |
| review | qwen→gemini | codex→qwen | — |

## 配置

编辑 `config.json` 修改模型命令路径、超时时间、默认分析器等：

```json
{
  "session_dir": "data/sessions",
  "default_analyzer": "qwen",
  "providers": {
    "codex": { "command": ["codex.exe", "exec"], "timeout": 600, "use_stdin": false },
    "qwen":  { "command": ["qwen"], "timeout": 600, "use_stdin": true },
    "gemini":{ "command": ["gemini", "-p"], "timeout": 600, "use_stdin": false }
  }
}
```
