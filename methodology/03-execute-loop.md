# 03 · execute-next-feature 的 8 阶段执行循环

> 本文档是 execute-next-feature skill 的**引擎中立**版说明。Claude Code 用户的 SKILL.md 和非 Claude 用户的 prompt 都是基于本文档的同一份内容派生而来——区别只在工具调用语法（Read/Write vs cat/echo）以及静态检查命令（项目级 `{{STATIC_CHECK_CMD}}` 填入）。

## 全局原则（每阶段都适用）

1. **不擅自扩大改动范围**：用户没要求的事不做，acceptance_criteria 没要求的功能不实现。
2. **遇到歧义立刻停下**：不靠猜测继续，把疑问写进 progress.md 并询问用户。
3. **AI 不能自行将 feature 标记为 done**：必须经人工验证（阶段 5）+ 代码气味扫描通过（阶段 6）+ commit 含准入证据（阶段 7）。
4. **AI 不在 main/master 分支工作**：所有 commit 发生在工作分支上。
5. **AI 不执行任何破坏性 git 操作**：禁止 force push、reset --hard、重写历史。
6. **占位资源必须可识别**：以 `_placeholder_` 为前缀，并登记到 feature 的 notes。
7. **feature-list JSON 字符串值禁止裸双引号**：见 02-feature-list-schema.md「JSON 字符串值禁止裸双引号」。写入后必须用 `python3 -m json.tool <path> > /dev/null` 验证。

---

## 阶段 0：前置检查 + 出关报告

**进入条件**：用户触发本流程。
**产出**：决定本次实现哪个 feature；环境就绪；出关报告确认已读规则。

**行为**：

1. 读 `docs/feature-list.json`（主索引，轻量字段足够选 feature）。文件不存在 → 提示「应先调用 generate-feature-list」，终止。
2. 检查是否有 `status = in_progress` 的 feature → 有则询问用户「继续未完成的还是放弃换一个」。
3. 选 feature：
   - 用户指定 → 用指定的。
   - 未指定 → 自动选第一个 `status = pending` 且 `depends_on` 全部 `done` 的。
   - 找不到 → 告知用户原因（全完成 / 全阻塞 / 全 obsolete）。
4. 检查 `estimated_scope`：为 `large` → 停下，提示「该 feature 规模过大，应先通过 sync-feature-list 拆细」，终止。
5. 检查 git：当前分支是 main/master 则停下；工作区不干净则询问用户三选一（commit / stash / restore）。
6. 加载上下文：
   - 读 `docs/progress.md`（如存在）
   - 读所选 feature 的 `docs/features/F0XX.json` 全文
   - 通读 `docs/product.md` 总览 + `docs/product/<对应模块>.md` 全文 + `docs/coding_rules.md` 中相关部分
   - 读每个依赖（`depends_on`）feature 的 `docs/features/{dep_id}.json` 的 `notes` 字段
7. **出关报告（硬约束）**：按下面固定格式输出。**未输出本块视为阶段 0 未完成、禁止进入阶段 1。空话、模糊概括、没有行号的引用一律视为无效。**

```
=== 阶段 0 出关报告 ===
已读取：
- docs/coding_rules.md（含其引入的 engine-rules.md / language-rules.md）✓
- docs/product.md 总览 ✓
- docs/product/<对应模块>.md ✓
- docs/progress.md（若存在）

本 feature 强相关的规则条目（必须 ≥1 条，引用 coding_rules.md 或其引入文件的原文 + 行号）：
- <文件名> L<行号>: "<原文片段>"
- <文件名> L<行号>: "<原文片段>"

本 feature 可能违反或需特别注意的规则：
<一两句话说明>
```

引用必须真实存在于源文件，且与本 feature 实际有关。这一步把"读过编码规则"变成可验证产出。

---

## 阶段 1：资源与依赖预检查

**进入条件**：阶段 0 完成。
**产出**：一份"开工准备清单"提交给用户确认。

**行为**：

1. 列出所有非代码资源需求：图片 / 音频 / 配置 / 第三方库 / 引擎/编辑器内的人工操作（AI 无法代替的）。
2. 对每一项标 ✅ 已存在 或 ❓ 不存在；后者给用户三选一：
   - a. 由用户提供后再继续（暂停）
   - b. 用占位资源（`_placeholder_` 前缀 + 醒目识别色或简单几何形状 + 登记到 notes）
   - c. 跳过本 feature，先做别的
3. 列出预计涉及的文件改动：将新增 / 将修改 / 修改性质（小改 vs 重写）。
4. 列出预计 git commit 数量与每个 commit 内容。
5. 输出清单等用户确认。

> **未得到用户确认前不动手写代码、不修改任何文件。**

---

## 阶段 2：标记开工

**进入条件**：用户确认阶段 1 清单。
**产出**：feature 状态切换；progress.md 更新；可选 chore commit。

**行为**：

1. 主索引中该 feature 的 `status` 改为 `in_progress`。
2. 更新 `docs/progress.md`：
   - 上一次「当前正在做」和「进展」追加到末尾「## 历史」区 + 时间戳
   - 「## 当前正在做」填入本 feature 的 id + title
   - 「## 进展」清空，加入第一行「开工于 `<ISO 8601 时间戳>`」
3. 可选 chore commit：`chore(F0XX): start feature`。默认不做。

---

## 阶段 3：实现

**进入条件**：阶段 2 完成。
**产出**：源代码改动 + 多个 git commit + progress.md 持续更新。

**行为**：

1. 严格遵循 `docs/coding_rules.md`。规则与当前 feature 冲突 → 停下询问用户，不擅自偏离。
2. 持续更新 progress.md：每完成一个有意义的子步骤追加一行；遇歧义记录"卡点"并停下询问。
3. **细粒度 commit**：
   - 简单 feature 一个 commit。
   - 较大 feature 分多个 commit，每个是原子改动。常见拆法：
     - `feat(F0XX): add <core data structure>`
     - `feat(F0XX): wire <data> to <controller/view>`
     - `test(F0XX): cover <edge cases>`
4. **每个 commit message 格式**：
   ```
   <type>(F0XX): <动词短语描述>

   <可选的多行说明>
   <如改动了其他 feature 涉及的文件，列出>
   <如使用了占位资源，列出占位资源路径与替换提示>
   <如刻意未实现某些 acceptance_criteria 的边界情况，说明>
   ```
   `<type>` 取值：`feat` / `fix` / `refactor` / `test` / `docs` / `chore`
5. **每个 commit 前的硬检查**：
   - `git branch --show-current` 不是 main/master
   - 用 `git add <具体路径>` 暂存（**不用 `git add .` 或 `git add -A`**）
   - `git status` 复核暂存清单与本次 commit 意图一致
6. 实现完成后输出"变更摘要"：改了哪些文件 / commit hash + message 首行 / 各 acceptance_criteria 如何满足 / 刻意没做的事 / 用了哪些占位资源。

---

## 阶段 4：自验

**进入条件**：阶段 3 完成。
**产出**：自验报告。

**行为**：

1. 把 acceptance_criteria 分类：
   - **静态可验证**：编译/类型检查/单测/lint。AI 可执行。
   - **行为可验证**：玩家能看到 X、按某键能触发 Y。AI 不能自行验证，列入"请人工验证"清单。
2. 执行所有静态验证：
   - 用项目级 `STATIC_CHECK_CMD`（在 `docs/methodology-config.json` 的 `static_check_cmd` 字段，由 BOOTSTRAP STEP 3 填入）。
   - 例：`npm run typecheck` / `cargo check` / `mypy .` / `tsc --noEmit` / Godot 项目用 `timeout 15 godot --headless --check-only --path .`
   - **如果项目静态检查需要超时包裹（如 Godot headless）**，必须显式 `timeout N`，禁止 `run_in_background=true`。
3. 任何静态检查失败 → 回阶段 3 修复，不进入阶段 5。
4. 输出"请人工验证"清单，每条对应一个 acceptance_criteria，写法形如：
   - 「在浏览器打开 http://localhost:3000，点击"添加"按钮，观察列表是否出现新条目」
5. 提示用户：「请按上述清单逐项验证后告知结果。」

---

## 阶段 5：人工验证

**进入条件**：阶段 4 完成，输出了人工验证清单。
**产出**：用户对每条人工验证项的判定。

**行为**：

1. 等用户回复。
2. 用户回「全部通过」/ 等价 → 进入阶段 6。
3. 用户指出某项不通过 → 记录到 progress.md，回阶段 3 修复（保留 `in_progress`、保留已有 commit）。修完再走阶段 4 → 5。
4. 用户回含糊（「先这样」/「细节问题以后再说」）→ 询问「是否仍有未满足的 acceptance_criteria？建议要么在 notes 中记录后标 done，要么先修复」。由用户定。

> **严禁 AI 自行将 feature 标记为 done。即使所有静态检查通过、即使你认为实现正确，没有用户的明确确认就不能进入阶段 6。**

---

## 阶段 6：代码气味扫描（子 agent 委派）

**进入条件**：阶段 5 用户明确确认通过。
**产出**：子 agent 扫描 JSON 报告；must_fix 项当场修复 commit；suggest 项写入 feature notes；一行 `Code smell scan: pass` 准入证据。

> **本阶段是硬性准入条件。must_fix 必须全部修复后才能进入阶段 7。不允许跳过，即使主观判断「这个 feature 改动很小」。**

### 6.1 委派子 agent 做扫描（不在主上下文里自己扫）

调用支持 sub-agent 的工具（Claude Code 的 Task；其他 CLI 用等价方式开个 fresh context）。原因：主上下文走完阶段 0-5 后已被压缩，编码规则细节容易遗忘；子 agent fresh context 能完整加载规则做精确扫描。

子 agent prompt 模板：
```
你是代码气味扫描员。

先读取以下编码规则全文（务必全读）：
- docs/coding_rules.md
- docs/coding-rules/engine-rules.md（若存在）
- docs/coding-rules/language-rules.md（若存在）

本次 feature F0XX 的所有改动文件：
[由主 agent 填入：git diff <feature 起点 commit>..HEAD --name-only]

对照下列 10 项气味清单逐项检查每个改动文件：
- 文件过长（>~300 行）
- 重复知识（同一业务规则 2+ 处硬编码）
- 类型分发扩散（match/if type 写在不该知道 type 含义的类里）
- Magic 数字/字符串（裸数字直接嵌在逻辑里）
- 跨文件共用枚举/常量（3+ 文件引用，可考虑提取）
- God Object 趋势（单文件新增字段/方法 >3 且与核心职责无关）
- 引擎/语言特有陷阱（按 engine-rules.md / language-rules.md 的 anti-pattern 列表）
- 表现与逻辑耦合（数据逻辑写进 UI 回调，或 UI 直接改数据字段）
- 注释解释"是什么"而非"为什么"
- 多次才改好的 Bug（已知 2+ 次修复迹象提示设计问题）

严重性分级：
- must_fix: 导致未来 feature 一定踩坑；或已经是重复 bug 的根源
- suggest: 会随 feature 增加而恶化但当前不紧急
- acceptable: 风格偏好或极小范围；改了反而增加复杂度

输出 JSON 格式（且只输出 JSON）：
{
  "must_fix": [
    {"file": "...", "line": 123, "smell": "重复知识", "rule_ref": "coding_rules.md L<行号>", "fix_suggestion": "..."}
  ],
  "suggest": [{"file":"...", "smell":"...", "note":"..."}],
  "acceptable": [{"file":"...", "smell":"...", "reason":"..."}]
}

找不到气味时返回对应数组为空。
绝对不要自己修代码、不要执行 git 操作、不要 commit。只做诊断。
```

### 6.2 主 agent 处理子 agent 返回的 JSON

1. 解析 `must_fix`：
   - 为空 → 进入 6.3
   - 非空 → 主上下文逐条修复，每条独立 `refactor(F0XX): <一句话>` commit；修复后重跑 STATIC_CHECK_CMD 确认通过
2. `suggest`：写入 feature 的 `notes`（与人工验证记录并列，不阻塞）
3. `acceptable`：在最终报告中简要列出，不写 notes

### 6.3 输出报告 + 准入证据

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

**最后一行是阶段 7 准入证据，必须写入当前 feature id，并保证修复后的 `must_fix` 为 `0`。hook（Claude Code 的 PreToolUse 或 git commit-msg）会校验完整证据行。**

### 6.4 约束

- 子 agent 调用失败（超时、返回非 JSON、读不到规则）→ 不允许进入阶段 7，停下报告用户
- must_fix 修复必须通过 STATIC_CHECK_CMD，未通过则回本阶段重做
- 修复 commit 不能引入行为变化；有疑问停下询问用户
- 报告全空也要输出最后一行准入证据，主体写「本次 feature 未发现代码气味」

---

## 阶段 7：标记完成

**进入条件**：阶段 6 已输出 `Code smell scan: pass` 且 must_fix 为 0（或已全部修复 commit）。
**产出**：feature-list 更新；progress.md 归档；最终 commit。

**行为**：

1. 更新两处：
   - **主索引** `docs/feature-list.json` 中本 feature：`status = "done"`，`completed_at = <现在 ISO 时间戳>`
   - **详情文件** `docs/features/F0XX.json` 的 `notes` 追加：关键实现决策 / 占位资源（路径 + 替换提示） / 刻意未做的边界 / 对后续 feature 有用的信息 / 阶段 6 的 suggest 项（前缀「TODO」）
2. 更新 `docs/progress.md`：把「当前正在做」+「进展」追加到「## 历史」区 + 完成时间戳 + feature id；清空前两节。
3. 最终 commit：
   ```
   chore(F0XX): mark feature as done

   Acceptance criteria all verified by human review.
   Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
   <如有 notes 中的关键信息，简要列出>
   ```
   **`Code smell scan: pass` 行必须包含**，hook 会扫描。
4. 输出本次 feature 总结：id + title / 总 commit 数与 hash / 满足了哪些 acceptance / 占位资源 / 留下的 TODO（含 suggest）。
5. **不执行 `git push`、不切分支、不操作 main**。

---

## 阶段 8：交班

**进入条件**：阶段 7 完成。
**产出**：下一步建议。

**行为**：

1. 读最新主索引，找下一个可启动的 feature（`pending` 且 `depends_on` 全 `done`）。
2. 输出"交班简报"：
   - 「本次完成：F0XX - <title>，commit 数 N，占位资源 M 个」
   - 「下一个可启动的 feature：F0YY - <title>」
   - 「建议：①直接做下一个 ②先休整 / 玩一遍 / 调整文档 ③合并到 main 打里程碑」
3. **不自动开始下一个 feature。** 等用户指令。

---

## Git 操作的允许与禁止

### 允许（自动执行，无需用户确认）

- 非 main 分支上 `git add <具体路径>`
- 非 main 分支上 `git commit`，message 遵循规范
- `git status` / `git log` / `git diff` / `git branch --show-current` 等只读

### 需用户确认才能执行

- 创建新分支 / 切换分支
- `merge` / `rebase` / `cherry-pick`
- 删除分支或 tag
- `git restore` / `git stash` 等可能丢失改动的操作

### 绝对禁止（即使用户要求也应先警告）

- 任何 force 操作：`push --force` / `push --force-with-lease`
- `reset --hard`
- 修改 `.git/` 目录文件
- `filter-branch` 或重写历史
- 操作 `main`/`master` 分支
- 自动 `push` 到远端

### git 命令失败的处理

立即停止本阶段，原文报告 git 输出，不尝试自动修复。

---

## 异常处理速查

| 情况 | 处理 |
|------|------|
| acceptance_criteria 有歧义/矛盾 | 提议修订该 feature；修订走 sync-feature-list，不在本流程处理 |
| 某 depends_on done feature 实际未实现完整 | 报告差距，询问用户（先回头补 / 在本 feature 中绕过 / 暂停） |
| 实现需改动当前 feature 范围外的文件 | 报告需改文件清单与原因，由用户决定合并到本 feature 还是新 feature |
| 自动化操作失败（git、文件读写、命令执行） | 停止，原文报告错误，不自动修复 |
| 上下文窗口接近耗尽 | 立刻把当前进展同步到 progress.md，提示开新会话续作 |
| 用户中途要求做范围外的事 | 礼貌指出超出当前 feature 范围，建议新 feature 处理 |

---

## 流程速查

```
阶段 0：前置检查 + 出关报告 ──→ 选定 feature、检查 git、加载上下文、引规则行号
   ↓
阶段 1：资源预检查 ─────→ 列资源/文件清单 ─→ 等用户确认
   ↓
阶段 2：标记开工 ───────→ 切 in_progress、更新 progress.md
   ↓
阶段 3：实现 ───────────→ 写代码、细粒度 commit、持续更新 progress
   ↓
阶段 4：自验 ───────────→ 跑 STATIC_CHECK_CMD、列人工验证清单
   ↓
阶段 5：人工验证 ───────→ 等用户判定 ─→ 不通过则回阶段 3
   ↓
阶段 6：代码气味扫描 ───→ 子 agent 委派 → must_fix 当场修 → 输出 "Code smell scan: pass"
   ↓
阶段 7：标记完成 ───────→ 更新 feature-list、最终 commit（含 pass 证据）、归档 progress
   ↓
阶段 8：交班 ───────────→ 输出下一步建议、等用户指令
```
