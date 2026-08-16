---
name: execute-next-feature
description: 当用户要求实现下一个、当前、或指定的 feature 时使用。本 skill 从 docs/feature-list.json 中找到合适的 feature，按规范流程实现、验收并提交。触发短语示例："做下一个 feature"、"实现 F007"、"继续推进任务"、"开始干活"、"做下一步"。本 skill 不用于初始化 feature-list（用 generate-feature-list）、不用于源文档变更后的同步（用 sync-feature-list）。
---

# 实现一个 feature

本 skill 把"实现一个 feature"当作有 8 个阶段的工作流来执行。每个阶段都有明确的进入条件和产出，跳过任何阶段都视为流程违规。

> 重要：本 skill 假定用户主语言为中文，AI 与用户交互时使用中文。

---

## 全局原则

在进入具体阶段前，AI 必须先内化以下原则。这些原则在每个阶段都适用：

1. **不擅自扩大改动范围**：用户没要求的事不做，acceptance_criteria 没要求的功能不实现。
2. **遇到歧义立刻停下**：不靠猜测继续。把疑问写进 progress.md 并询问用户。
3. **AI 不能自行将 feature 标记为 done**：必须经人工验证。
4. **AI 不在 main 分支工作**：所有 commit 都发生在工作分支上。
5. **AI 不执行任何破坏性 git 操作**：禁止 force push、reset --hard、重写历史。
6. **占位资源必须可识别**：以 `_placeholder_` 为前缀，并登记到 feature 的 notes。
7. **feature-list 相关文件字符串值中禁止裸双引号**：JSON 字符串内部不得出现未转义的 `"` 字符（含中文语境中的引号 `"…"` 如 `"游戏结束"`）。若需标注词语，改用 `\"…\"` 转义或中文书名号 `「…」`。每次写入下列任一文件后，必须立即用 `python3 -m json.tool <path> > /dev/null` 验证：
   - `docs/feature-list.json`（主索引：id/title/status/depends_on/estimated_scope/completed_at）
   - `docs/features/F0XX.json`（每个 feature 的详情：description/acceptance_criteria/source/notes）
   不合法则修复后再继续。

8. **feature-list 文件三层结构**（所有阶段共用）：
   - `docs/feature-list.json`：轻量主索引，每次会话加载，承载 status/depends_on 等可扫描字段
   - `docs/features/F0XX.json`：每个 feature 的完整详情，按需 `cat` 加载
   - `docs/feature-list-revisions.json`：sync-feature-list 维护的修订日志，本 skill 不读不写

---

## 阶段 0：前置检查

**进入条件**：用户触发本 skill。

**产出**：决定本次要实现哪个 feature；环境就绪。

**行为**：

1. 读取主索引 `docs/feature-list.json`（轻量字段已含 id/title/status/depends_on/estimated_scope/completed_at，足以做选 feature 决策，无需读详情目录）：
   - 若不存在，告知用户应先调用 `generate-feature-list` skill，本流程终止。

2. 检查是否有 `status` 为 `in_progress` 的 feature：
   - 有 → 询问用户：「检测到 F0XX 处于进行中状态，是继续未完成的它，还是放弃后换一个？」
   - 无 → 继续。

3. 选择本次要实现的 feature：
   - 用户已指定 → 使用指定的 feature。
   - 用户未指定 → 自动选择第一个满足以下条件的 feature：
     - `status` 为 `pending`
     - `depends_on` 中所有 feature 的 `status` 为 `done`
   - 找不到符合条件的 feature → 告知用户当前没有可启动的 feature，并列出原因（已全部完成 / 被依赖阻塞 / 全部 obsolete）。

4. 检查所选 feature 的 `estimated_scope`：
   - 为 `large` → 停下，告知用户「该 feature 规模过大，应先通过 sync-feature-list 拆细」，本流程终止。

5. 检查 git 环境：
   - 执行 `git status` 与 `git branch --show-current`。
   - 当前在 `main` 分支 → 暂停，提示「不在 main 分支上工作。请切换到 dev 或新建工作分支后再继续」，本流程暂停。
   - 工作区不干净（有未提交的改动）→ 询问用户三选一：
     a. 先 commit 现有改动（用户自行处理）
     b. stash 现有改动
     c. 放弃现有改动（`git restore`）
     未确认前不继续。

6. 加载上下文：
   - 读取 `docs/progress.md`（若存在）。
   - 读取本 feature 的详情文件 `docs/features/F0XX.json`（取 description / acceptance_criteria / source / notes 全文，主索引里只有概要字段）。
   - 通读 `docs/product.md`（总览）、`docs/product/*.md`（当前 feature 所属模块）、`docs/coding_rules.md`（协作契约 + 架构原则 + 技术栈，含其引入的 `docs/coding-rules/engine-rules.md` 与 `docs/coding-rules/language-rules.md`）中与当前 feature 相关的部分。
   - 对本 feature 依赖的每个已 done feature，逐个读 `docs/features/{依赖 id}.json` 的 `notes` 字段（了解前置 feature 的实现细节、占位资源、TODO 等）。命令模板：`cat docs/features/F0XX.json`。

7. 输出阶段 0 摘要：本次实现 `F0XX - <title>`，依赖 `[F0YY, F0ZZ]`，工作分支为 `<branch>`。

8. **出关报告（硬约束）**：在本阶段结束、进入阶段 1 之前，必须按以下固定格式向用户输出。AI 未输出本块视为阶段 0 未完成、禁止进入阶段 1。空话、模糊概括、没有行号的引用一律视为无效。

   ```
   === 阶段 0 出关报告 ===
   已读取：
   - docs/coding_rules.md（含其引入的 docs/coding-rules/engine-rules.md 与 docs/coding-rules/language-rules.md）✓
   - docs/product.md 总览 ✓
   - docs/product/<对应模块>.md ✓
   - docs/progress.md（若存在）

   本 feature 强相关的规则条目（必须 ≥1 条，引用 coding_rules.md 或其引入子文件的原文 + 行号）：
   - <文件名> L<行号>: "<原文片段>"
   - <文件名> L<行号>: "<原文片段>"

   本 feature 可能违反或需特别注意的规则：
   <一两句话说明，例如：本 feature 会在 pawn.gd 中新增字段，需警惕 coding_rules.md 第 X 节「God Object 趋势」>
   ```

   > 这一步的目的是把"读过编码规则"变成可验证的产出。AI 在被迫援引具体行号时，无法靠模式匹配糊弄过去。引用必须真实存在于源文件，且与本 feature 实际有关。

---

## 阶段 1：资源与依赖预检查

**进入条件**：阶段 0 完成。

**产出**：一份"开工准备清单"提交给用户确认。

**行为**：

1. 列出本 feature 实现所需的所有非代码资源：
   - 图片 / 精灵 / 预制体
   - 音频 / 字体
   - 配置数据 / json / 关卡数据
   - 第三方库（若需新增依赖）
   - 引擎/编辑器内的人工操作（如挂载预制体到场景节点、配置 Cocos 编辑器面板等——AI 无法代替人类做这些）

2. 对每一项做检查并标注：
   - **✅ 已存在并符合用途**：记录路径，加入清单。
   - **❓ 不存在或不确定**：列出三个处理选项，让用户选：
     a. 由用户提供后再继续（暂停本流程）
     b. 使用占位资源继续（说明占位方案：以 `_placeholder_` 为前缀命名、采用醒目识别色或简单几何形状、并在该 feature 的 `notes` 中登记"待替换占位资源"）
     c. 跳过本 feature，先做别的（回到阶段 0 重新选 feature）

3. 列出预计涉及的文件改动：
   - **将新增的文件**：完整路径
   - **将修改的现有文件**：完整路径，并说明修改性质（小改 / 重写）
   - 若涉及 `core/` 目录之外但又涉及核心逻辑的文件，明确指出（这通常是设计警告信号）

4. 列出预计的 git commit 数量：
   - 简单 feature → 1 个 commit
   - 跨多个文件或包含测试 → 多个 commit，每个 commit 列出预计内容

5. 用清单形式输出全部上述信息，等待用户确认。

> **未得到用户确认前不动手写代码、不修改任何文件。**

---

## 阶段 2：标记开工

**进入条件**：用户确认阶段 1 的开工清单。

**产出**：feature 状态切换；progress.md 更新；可选的 chore commit。

**行为**：

1. 在主索引 `docs/feature-list.json` 中将该 feature 的 `status` 改为 `in_progress`（status 字段只在主索引，详情文件不重复存）。

2. 更新 `docs/progress.md`：
   - 把上一次"当前正在做"和"进展"的内容（若有）追加到文件末尾的"## 历史"区，加上时间戳。
   - "## 当前正在做"小节填入本 feature 的 id 和 title。
   - "## 进展"小节清空，加入第一行："开工于 `<ISO 8601 时间戳>`"。
   - "## 上下文笔记"区保留不动。

3. （可选）若用户偏好将 progress 同步到 git 历史，执行一个 chore commit：
   ```
   chore(F0XX): start feature
   ```
   - 这一步可以省略，看用户偏好。默认不做。

---

## 阶段 3：实现

**进入条件**：阶段 2 完成。

**产出**：源代码改动；可能伴随多个 git commit；progress.md 持续更新。

**行为**：

1. **严格遵循 `docs/coding_rules.md` 的所有约束**。如发现某条规则与当前 feature 实现存在冲突，停下询问用户，不擅自偏离。

2. **持续更新 progress.md**：
   - 每完成一个有意义的子步骤（写完一个文件、做完一个决策、解决一个卡点），在"## 进展"区追加一行简短记录。
   - 遇到歧义或需要决策时，在"## 进展"区记录"卡点"，并停下询问用户。
   - 这一步是 long-running agent 的核心：把工作记忆外置到磁盘，避免依赖上下文窗口。

3. **细粒度 commit**：
   - 简单 feature 一个 commit 即可。
   - 较大 feature 应分多个 commit，每个 commit 是一个原子改动。常见的拆法：
     * `feat(F0XX): add <core data structure>`
     * `feat(F0XX): wire <data> to <controller/view>`
     * `test(F0XX): cover <edge cases>`
   - **不要憋一个巨大 commit**。多 commit 让未来 `git revert` 单点改动成为可能。

4. **每个 commit 的 message 必须遵循以下格式**：

   ```
   <type>(F0XX): <动词短语描述>

   <可选的多行说明，2-4 行>
   <如改动了其他 feature 涉及的文件，列出>
   <如使用了占位资源，列出占位资源路径与替换提示>
   <如刻意未实现某些 acceptance_criteria 的边界情况，说明>
   ```

   `<type>` 取值：
   - `feat`：实现新功能
   - `fix`：修复 bug
   - `refactor`：重构（不改变行为）
   - `test`：新增或修改测试
   - `docs`：文档改动（包括 progress.md、feature-list.json）
   - `chore`：杂项（构建、配置、状态切换）

5. **每个 commit 执行前的硬检查**（AI 自行执行，无需用户确认）：
   - `git branch --show-current` 不是 `main`（双重保险）
   - 用 `git add <具体路径>` 暂存（不使用 `git add .` 或 `git add -A`，避免误加 IDE 配置、调试文件等）
   - 暂存后用 `git status` 复核：暂存清单与本次 commit 意图一致

6. 实现完成后，整理一份"变更摘要"输出给用户：
   - 改了哪些文件，每个文件的核心改动是什么（一两句话）
   - 本次产生了哪些 commit（列出 hash 与 message 的第一行）
   - 哪些 acceptance_criteria 是怎么满足的（逐条对应）
   - **主动指出**：本次实现刻意没做但用户可能预期的事；做了哪些假设；用了哪些占位资源

---

## 阶段 4：自验

**进入条件**：阶段 3 完成。

**产出**：自验报告。

**行为**：

1. 把 acceptance_criteria 的每一条分类：
   - **静态可验证**：编译通过、类型检查通过、单元测试通过、lint 通过等。AI 可执行并报告结果。
   - **行为可验证**：玩家能看到 X、按某键能触发 Y、某场景下表现 Z。AI 不能自行验证，必须列入"请人工验证"清单。

2. 执行所有静态验证：
   - **从 `docs/methodology-config.json` 读取 `static_check_cmd` 字段**，这是 BOOTSTRAP STEP 3 为本项目记录的静态检查命令。例如：
     - Node/TS 项目：`npm run typecheck`、`tsc --noEmit`
     - Python 项目：`mypy .`、`ruff check .`
     - Rust 项目：`cargo check`
     - Godot 项目：`timeout 15 godot --headless --check-only --path . 2>&1 | grep "scripts/" || true`
     - 无类型检查的项目：跑单元测试或 lint 命令
   - **若该命令对长时运行进程有要求（如 Godot headless 不自动退出）**，必须按项目配置中已写好的 `timeout N` 包裹运行；**禁止使用 `run_in_background=true`**——静态检查必须同步完成才能继续。
   - 若执行了静态检查，输出结果：通过 / 失败的具体错误。
   - **任何静态检查失败 → 回到阶段 3 修复，不进入阶段 5**。

3. 输出"请人工验证"清单。每条对应一个 acceptance_criteria，写法形如：
   - 「在编辑器中预览，按 ↑ 键，观察当前方块是否顺时针旋转 90 度」
   - 「在编辑器中预览，让方块下落到底部，观察是否锁定在最低可达位置」

4. 提示用户：「请按上述清单逐项验证后告知结果。全部通过后我会标记本 feature 为 done。」

---

## 阶段 5：人工验证

**进入条件**：阶段 4 完成，输出了人工验证清单。

**产出**：用户对每条人工验证项的判定。

**行为**：

1. 等待用户回复。

2. 用户回复"全部通过" / 等价表达 → 进入阶段 6。

3. 用户指出某项不通过 → 把不通过项记录到 progress.md 的"## 进展"区，回到阶段 3 修复（保留 `in_progress` 状态、保留已有 commit）。修复完成后再次进入阶段 4，从头跑自验。

4. 用户回复"差不多了，先这样" / "细节问题以后再说"等含糊回复 →
   - 询问：「是否仍有未完全满足的 acceptance_criteria？如果有，建议在 notes 中记录，本 feature 仍标记为 done；如果有重大缺失，建议先修复再标记。」
   - 由用户做决定。

> **严禁 AI 自行将 feature 标记为 done。即使所有静态检查都通过、即使你认为实现正确，没有用户的明确确认就不能进入阶段 6。**

---

## 阶段 6：代码气味扫描（子 agent 委派）

**进入条件**：阶段 5 用户明确确认通过。

**产出**：子 agent 返回的气味扫描 JSON 报告；must_fix 项的当场修复 commit（如有）；suggest 项写入 feature 的 notes 字段；一行 `Code smell scan: pass` 准入证据。

> **本阶段是 feature 完成的硬性准入条件。must_fix 项必须全部修复后才能进入阶段 7 标记 done。不允许跳过本阶段直接进入阶段 7，即使主观判断「这个 feature 改动很小」。**

**行为**：

### 6.1 委派子 agent 做扫描（不在主上下文里自己扫）

调用 Task 工具，subagent_type=general-purpose，prompt 模板如下。理由：主上下文走完阶段 0-5 后已被压缩，编码规则细节容易遗忘；子 agent fresh context 能完整加载两份规则（~850 行）做精确扫描。

```
你是代码气味扫描员。

先读取以下编码规则全文（务必全读，扫描结果质量取决于此）：
- docs/coding_rules.md
- docs/coding-rules/engine-rules.md（若存在）
- docs/coding-rules/language-rules.md（若存在）

本次 feature F0XX 的所有改动文件：
[此处由主 agent 填入，通过 git diff <feature 起点 commit>..HEAD --name-only 得到]

对照下列 10 项气味清单逐项检查每个改动文件：
- 文件过长（>~300 行）
- 重复知识（同一业务规则 2+ 处硬编码）
- 类型分发扩散（match/if type 写在不该知道 type 含义的类里）
- Magic 数字/字符串（裸数字直接嵌在逻辑里，未提取为具名常量）
- 跨文件共用枚举/常量（3+ 文件引用，可考虑提取）
- God Object 趋势（单文件新增字段/方法 >3 且与核心职责无关）
- 引擎/语言特有陷阱（按 docs/coding-rules/engine-rules.md 与 docs/coding-rules/language-rules.md 的「反模式速查」清单逐条对照）
- 表现与逻辑耦合（数据逻辑写进 UI 回调、绘制函数，或 UI 直接改数据字段）
- 注释解释"是什么"而非"为什么"
- 多次才改好的 Bug（如已知，2+ 次修复迹象提示设计问题）

严重性分级：
- must_fix: 导致未来 feature 一定踩坑；或已经是重复 bug 的根源
- suggest: 会随 feature 增加而恶化但当前不紧急
- acceptable: 风格偏好或极小范围；改了反而增加复杂度

输出 JSON 格式（且只输出 JSON，不要额外说明、不要 markdown 代码块包裹）：
{
  "must_fix": [
    {"file": "<path>", "line": 123, "smell": "重复知识", "rule_ref": "coding_rules.md L<行号>", "fix_suggestion": "..."}
  ],
  "suggest": [{"file":"...", "smell":"...", "note":"..."}],
  "acceptable": [{"file":"...", "smell":"...", "reason":"..."}]
}

找不到气味时返回对应数组为空。
绝对不要自己修代码、不要执行 git 操作、不要 commit。只做诊断。
```

### 6.2 主 agent 处理子 agent 返回的 JSON

1. 解析 `must_fix` 数组：
   - **为空** → 进入 6.3 输出总结，然后进入阶段 7。
   - **非空** → 在主上下文里逐条修复，每条修复独立 `refactor(F0XX): <一句话>` commit；修复完成后再次跑 `docs/methodology-config.json` 中的 `static_check_cmd` 确认静态检查通过，未通过则回到当前阶段重做。
2. 解析 `suggest` 数组：写入 feature 的 `notes` 字段（与人工验证记录并列，不阻塞流程）。
3. 解析 `acceptable` 数组：在最终报告中简要列出，不写 notes。

### 6.3 输出报告 + 准入证据

主 agent 综合子 agent JSON 与自己的修复行动，向用户输出：

```
## 代码气味扫描报告（F0XX）

### 🔴 已当场修复（来自 must_fix）
- **<smell>**：<file>:<line> — <rule_ref>
  → 已修复，commit: `<hash>`

### 🟡 已记录到 notes（来自 suggest）
- **<smell>**：<file> — <note>

### 🟢 认可不处理（来自 acceptable）
- **<smell>**：<file> — <reason>

Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
```

**最后一行是阶段 7 的准入证据，必须替换成当前 feature id 并原样输出。`must_fix` 表示扫描和修复后剩余的阻断项，所以进入阶段 7 时必须为 `0`；hook 只接受主 agent 的 assistant 文本，不接受本 skill 里的示例文字。**

### 6.4 约束

- 子 agent 调用失败（超时、返回非 JSON、无法读取规则文件）→ 不允许进入阶段 7，停下报告用户。
- must_fix 修复必须通过阶段 4 的静态检查（`docs/methodology-config.json` 中的 `static_check_cmd`），未通过则回到本阶段重做。
- 修复 commit 不能引入行为变化；如有疑问停下询问用户。
- 报告为空（must_fix / suggest / acceptable 都为空）时仍要输出最后一行准入证据，主体写「本次 feature 未发现代码气味」。

---

## 阶段 7：标记完成

**进入条件**：阶段 6 已输出 `Code smell scan: pass` 且 must_fix 为 0（或已全部修复 commit）。

**产出**：feature-list 更新；progress.md 归档；最终 commit。

**行为**：

1. 更新本 feature 的两处文件：
   - **主索引 `docs/feature-list.json`** 中本 feature 的条目：
     * `status` 改为 `done`
     * `completed_at` 填入当前 ISO 8601 时间戳
   - **详情文件 `docs/features/F0XX.json`** 的 `notes` 字段，追加实现要点：
     * 关键的实现决策（例如「方块用数组而非对象表示」）
     * 使用了哪些占位资源（路径与替换提示）
     * 刻意未做的边界情况
     * 对后续 feature 可能有用的信息
     * 阶段 6 的 suggest 项（待办代码气味，标注「TODO」前缀）

2. 更新 `docs/progress.md`：
   - 把"## 当前正在做"和"## 进展"的全部内容追加到文件末尾的"## 历史"区，加上完成时间戳和 feature id。
   - 把"## 当前正在做"清空。
   - "## 进展"清空。

3. 执行最终 commit：
   - `git add docs/feature-list.json docs/features/F0XX.json docs/progress.md`
   - 执行 commit，message 格式（必须包含 `Code smell scan: pass` 行作为硬约束证据，hook 会扫描）：

     ```
     chore(F0XX): mark feature as done

     Acceptance criteria all verified by human review.
     Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
     <如有 notes 中的关键信息，简要列出>
     ```

4. 输出本次 feature 的总结：
   - feature id 与 title
   - 总 commit 数（含本次 chore commit + 阶段 6 的 refactor commit）与每个 commit 的 hash + message 第一行
   - 实现了哪些 acceptance_criteria
   - 用了哪些占位资源（如有）
   - 留下了哪些 TODO（含阶段 6 的 suggest 项）

5. **不执行 `git push`、不切分支、不操作 main**。

---

## 阶段 8：交班

**进入条件**：阶段 7 完成。

**产出**：下一步建议。

**行为**：

1. 读取最新的主索引 `docs/feature-list.json`（轻量字段足够，无需打开详情目录），找出下一个可启动的 feature（`status` 为 `pending` 且 `depends_on` 全部 `done`）。

2. 输出"交班简报"：
   - 「本次完成：F0XX - <title>，commit 数 N，产生占位资源 M 个」
   - 「下一个可启动的 feature：F0YY - <title>」
   - 「建议是否：①直接做下一个；②先休整 / 玩一遍 / 调整文档；③合并 dev 到 main 打个里程碑」

3. **不自动开始下一个 feature**。等待用户指令。

---

## Git 操作的允许与禁止

> 本节为快速参考，所有规则在前文阶段中已分散体现。

### 允许（自动执行，无需用户确认）

- 在非 main 分支上 `git add <具体路径>`
- 在非 main 分支上 `git commit`，message 遵循规范格式
- `git status` / `git log` / `git diff` / `git branch --show-current` 等只读操作

### 需用户确认才能执行

- 创建新分支（`git checkout -b ...`）
- 切换分支
- `merge` / `rebase` / `cherry-pick`
- 删除分支或 tag
- `git restore` / `git stash` 等可能丢失改动的操作

### 绝对禁止（即使用户要求也应先警告）

- 任何 force 操作：`push --force`、`push --force-with-lease`
- `reset --hard`
- 直接修改 `.git/` 目录下的文件
- `git filter-branch` 或任何重写历史的操作
- 操作 `main` 分支（不 commit、不 merge、不 push）
- 自动 `push` 到远端

### 任何 git 命令失败的处理

立即停止本阶段，原文报告 git 输出，不尝试自动修复。让用户判断是环境问题、权限问题还是冲突。

---

## 异常处理

任何阶段中发现以下情况，立即暂停并报告：

| 情况 | 处理 |
|------|------|
| acceptance_criteria 本身有歧义或矛盾 | 提议修订该 feature；修订需走 `sync-feature-list` 流程，不在本 skill 中处理 |
| 某个 `depends_on` 中标记为 `done` 的 feature 实际上未实现完整 | 报告差距，询问处理方式（先回头补 vs 在本 feature 中绕过 vs 暂停） |
| 实现过程中需要改动当前 feature 范围外的文件 | 报告需要改的文件清单与原因，由用户决定是合并到本 feature 还是新增 feature |
| 任何自动化操作失败（git、文件读写、命令执行） | 停止，原文报告错误，不自动修复 |
| 上下文窗口接近耗尽 | 立刻把当前进展同步到 `progress.md`，提示用户开新会话续作 |
| 用户在中途要求做范围外的事 | 礼貌指出"这超出当前 feature 范围"，建议作为新 feature 处理 |

---

## 流程速查表

```
阶段 0：前置检查 ──── 选定 feature、检查 git、加载上下文、出关报告
   ↓
阶段 1：资源预检查 ── 列出资源/文件清单 ──→ 等待用户确认
   ↓
阶段 2：标记开工 ──── 切 in_progress、更新 progress.md
   ↓
阶段 3：实现 ──────── 写代码、细粒度 commit、持续更新 progress.md
   ↓
阶段 4：自验 ──────── 跑静态检查、列出人工验证清单
   ↓
阶段 5：人工验证 ──── 等待用户判定 ──→ 不通过则回阶段 3
   ↓
阶段 6：代码气味扫描 ── 子 agent 委派 → must_fix 当场修 → 输出 Code smell scan: pass
   ↓
阶段 7：标记完成 ──── 更新 feature-list、最终 commit（带 pass 证据）、归档 progress
   ↓
阶段 8：交班 ──────── 输出下一步建议、等待用户指令
```
