# Yaya Loop · Product → Feature → Ship

这是一套**面向各类软件项目的「产品需求 → 任务拆解 → 一步一步实现」工作流**，从一个 Godot + GDScript 游戏项目中沉淀出来，已用同一套流程稳定推进了 95 个 feature。

> 当前版本：`v0.1.0`。核心方法论、Godot 与 GDScript 规则来自实际项目；其他引擎和语言规则目前以可协作补全的 stub 为主。

## 它解决了什么

软件项目最常见的两个失控来源：
1. **产品需求散在群聊、记忆、TODO 列表里** —— 需要一个唯一真实来源（single source of truth）。
2. **AI 写代码失控** —— 跳过验证、混入未要求的改动、把"自己觉得对"当成"完成"。

这个 kit 用三种文档 + 三类 AI skill 解决这两个问题：

| 文档 | 角色 | 谁维护 |
|------|------|--------|
| `docs/product.md` + `docs/product/*.md` | **要做什么**（What） | 你 + 产品类 skill |
| `docs/feature-list.json` + `docs/features/F0XX.json` | **拆成的任务清单 + 状态** | 生成类 skill 自动维护 |
| `docs/coding_rules.md` | **怎么做的硬约束**（How） | 你 + AI 协作填写 |

三类 skill：
- **产品类**：把口语化需求结构化进 product.md（init / change / spec / ui / audio）
- **生成类**：把 product.md 拆成 feature-list（generate-feature-list / sync-feature-list）
- **执行类**：按规范流程实现一个 feature 并交付（execute-next-feature / pick-refactor-smell）

## 用法（人类视角）

```
1. 把这个文件夹拷一份到自己电脑（如果你还没有的话）：
   git clone https://github.com/m358807551/yaya-loop.git ~/code/yaya-loop
   # 或：cp -r yaya-loop ~/code/

2. 进入你的目标项目目录（新的、旧的都行）：
   cd ~/code/<your-project>

3. 打开你的 AI CLI（Claude Code / Codex / Aider / Cursor 都行），
   把以下指令丢给它：

   "请按 ~/code/yaya-loop/BOOTSTRAP.md 的步骤，把这套
    方法论在当前项目里初始化好。"

4. 跟着 AI 的提问回答（10 分钟左右），完成后：
   - 新项目：你已经有了 product.md 和初始 feature-list，可以开干。
   - 老项目：AI 反向工程出 product.md 雏形 + 已完成 feature 清单 +
     代码气味 backlog，你可以继续推进。

5. 之后每次想推进，对 AI 说：
   - 「做下一个 feature」 → 触发 execute-next-feature
   - 「我想加 X 功能 / 改 Y 行为」 → 触发 product-change-standardizer
   - 「挑一个坏味道重构」 → 触发 pick-refactor-smell
```

## 用法（AI 视角）

如果你是被用户授权来初始化这个 kit 的 AI：**直接读 `BOOTSTRAP.md`**，里面有完整的 6 步指令。

## 目录速览

| 路径 | 给谁看 | 备注 |
|------|--------|------|
| `README.md` | 人类 | 你正在看 |
| `BOOTSTRAP.md` | AI | 任何 AI CLI 读完都能初始化 |
| `methodology/` | AI + 高级用户 | 方法论原理、schema、模板，全部技术栈无关 |
| `coding-rules-library/` | AI | 各种引擎/语言的最佳实践片段，可换装到目标项目 |
| `claude-code/` | Claude Code 用户 | 9 个 SKILL.md + 2 个 hook + settings 示例 |
| `ai-agnostic-prompts/` | 非 Claude AI CLI 用户 | 同样 9 个 skill 的 prose 版本，剥了 YAML 可粘贴使用 |
| `git-hooks/` | 非 Claude 用户的兜底 | 1 个 commit-msg hook，commit 时校验 |
| `examples/` | 想看完整样子的人 | 端到端 5-feature 小示例 + legacy 接入叙事 |
| `upgrade-notes.md` | 已经用了一段的人 | kit 升级时如何迁移 |

## 它**不**解决什么

- **不是项目管理工具**：没有甘特图、燃尽图、看板。feature-list.json 是给 AI 看的工作清单，不是给团队看的进度仪表盘。
- **不是 CI/CD**：阶段 4 的静态检查只是「编译/类型检查通过」，不替代真实的 CI 流水线。
- **不是代码生成器**：每个 feature 还是 AI 一行一行写出来的，kit 只规范流程。
- **不是银弹**：feature 拆得糙、product.md 写得乱，kit 救不了你；它只在你愿意先把"想做什么"想清楚的前提下放大效率。

## 反馈与升级

这套 kit 还在演化。如果你在新项目里用出新的问题或经验，建议：
1. 在那个项目里改 `docs/coding_rules.md`，让它适配你的实际节奏。
2. 把通用的经验回流到这个 kit 的 `methodology/` 或 `coding-rules-library/` 对应文件。
3. 升级 `kit-version.txt`（语义化版本：破坏性 +1.0.0，新增 +0.1.0，修补 +0.0.1）。

## 关于作者

我是一名后端开发工程师，主要使用 Python，也使用 Go。目前正在寻找远程软件开发工作或长期合作机会。

如果你正在招聘，或者有合适的合作机会，欢迎通过邮箱联系我：m358807551@163.com。

## License

[MIT](./LICENSE)。允许使用、复制、修改和商用；再分发本项目或其实质部分时，请保留版权与许可声明。

参与贡献请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)；安全问题请按 [SECURITY.md](./SECURITY.md) 私密报告。
