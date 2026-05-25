# AI-Agnostic Prompts · 使用说明

> 本目录是给**非 Claude Code 用户**的（Codex / Aider / Cursor / 等等任何 AI CLI）。每个文件都是一段可以**直接粘贴**到你的 AI 对话窗口的 prompt。
>
> Claude Code 用户：你不需要这些文件，直接用 `../claude-code/skills/` 即可（Claude Code 自动识别 SKILL.md 的 YAML frontmatter 与触发短语）。

## 心智模型

- 这 9 个 prompt 一一对应 [methodology/00-overview.md](../methodology/00-overview.md) 提到的"三类 skill"：产品类 5 个、生成类 2 个、执行类 2 个。
- 每次用户提需求时，你判断属于哪一类，复制对应 prompt 粘给 AI，再加你的具体需求。
- AI 收到 prompt 后按里面的步骤工作。中途有疑问会问你，按要求回答即可。

## 触发短语 → 用哪个 prompt

| 用户场景 / 触发短语 | 用哪个 prompt | 干什么 |
|------|-------------|--------|
| 「这是新项目，帮我从零启动」 | [product-init-elicitor.prompt.md](./product-init-elicitor.prompt.md) | 把一句话项目描述结构化进 product.md |
| 「我想加 X 功能」/「改 Y 行为」/「Z 有 bug」 | [product-change-standardizer.prompt.md](./product-change-standardizer.prompt.md) | 任何产品变更的统一入口，会路由到下面几个 skill |
| 「这个变更细节我想说清楚」 | [product-spec-elicitor.prompt.md](./product-spec-elicitor.prompt.md) | 对一个变更追问关键模糊点 |
| 「画个 UI 草图」 | [product-ui-sketcher.prompt.md](./product-ui-sketcher.prompt.md) | 产出 ASCII 线框图（可选 html mockup） |
| 「这里要什么音效」 | [product-audio-sketcher.prompt.md](./product-audio-sketcher.prompt.md) | 产出音效条目（含 _placeholder_*.wav 占位文件名） |
| 「生成 feature-list」/「初始化任务列表」 | [generate-feature-list.prompt.md](./generate-feature-list.prompt.md) | 从零一次性拆解 product → feature |
| 「同步 feature-list」/「product 更新了，刷新一下」 | [sync-feature-list.prompt.md](./sync-feature-list.prompt.md) | product 变更后增量同步 feature-list |
| 「做下一个 feature」/「实现 F007」/「继续推进」 | [execute-next-feature.prompt.md](./execute-next-feature.prompt.md) | 按 8 阶段流程实现一个 feature |
| 「挑一个坏味道重构」/「扫一下 suggest」 | [pick-refactor-smell.prompt.md](./pick-refactor-smell.prompt.md) | 从 feature notes 挑一个坏味道 |

## 怎么粘贴

每个 prompt 文件的内容是完整的 AI 指令。粘贴时**只复制 markdown 内容本身（去掉本目录的 `# X · Y` 标题和首段说明性表格也行）**，AI 拿到指令就开始按步骤执行。

例子（在你 AI CLI 的输入框）：
```
[粘贴 execute-next-feature.prompt.md 的全部内容]

请按上述流程开始。
```

或者更精简：
```
读 docs/methodology-prompts/execute-next-feature.prompt.md 并按其执行
```

如果你的 AI CLI 支持 `@file` 引用，那就更方便：`@docs/methodology-prompts/execute-next-feature.prompt.md`。

## 重要：质量门兜底

非 Claude Code 用户**没有 PreToolUse hook 能力**，所以"不允许跳过代码气味扫描就标 done"这条硬约束需要靠 git commit-msg hook 兜底。

安装方式见 `../git-hooks/install.md`。安装后，commit 时若把任何 feature 改成 `done` 但 commit message 不含 `Code smell scan: pass`，commit 会被拒绝。

## 与 Claude Code 版本的差异

| 维度 | Claude Code skills | AI-agnostic prompts |
|------|-------------------|--------------------|
| 入口 | YAML frontmatter + 触发短语自动识别 | 用户手动粘贴 prompt |
| 子 agent 委派（execute 阶段 6） | 调用 Task 工具 | 提示用户"开新会话粘贴本子 prompt" |
| 阶段 6 质量门 | PreToolUse hook + commit message 双重阻断 | 仅靠 git commit-msg hook |
| 调试 | Claude Code 内置日志 | 看 AI 输出 + commit 历史 |

方法论层面**没有差异**。只是触发与兜底机制不同。

## 自定义

你可以把每个 prompt 按你的项目实际改造（如调整阶段数、修改自检清单），改完直接生效——这些是纯 markdown，不需要重启任何东西。
