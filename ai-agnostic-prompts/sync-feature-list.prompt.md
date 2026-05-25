# sync-feature-list · prompt

> **触发场景**：当用户要求同步、更新、修订 docs/feature-list.json 以匹配最新的 docs/product.md、docs/product/*.md 或 docs/coding_rules.md 时使用。本 skill 通过 git diff 精确识别源文档变化，增量更新已存在的 feature-list。不用于初次生成（请用 generate-feature-list）。触发短语示例:"同步 feature-list"、"product 更新了，刷新一下任务列表"、"重新对齐 feature-list"、"我改了 product.md，更新一下任务清单"。
>
> **用法**：把"# sync-feature-list"以下的全部内容粘到你 AI 对话窗口，AI 会按里面的步骤工作。

---


# 同步 feature-list

本 skill 把"同步 feature-list"当作有 6 个阶段的工作流来执行。

**核心思想：通过 git diff 精确识别源文档的变化，而不是靠对比当前文档与 feature-list 反推变化。**

> 与用户交互一律使用中文。

## feature-list 文件三层结构

| 路径 | 角色 | 本 skill 的读写方式 |
|------|------|------|
| `docs/feature-list.json` | **主索引**：每个 feature 的 id/title/status/depends_on/estimated_scope/completed_at | 读全文做扫描；新增/修订时双写（索引+详情） |
| `docs/features/F0XX.json` | **详情**：每个 feature 的 description/acceptance_criteria/source/notes | 按 id 读单个文件；新增/修订时双写 |
| `docs/feature-list-revisions.json` | **修订日志**：revision_log 数组 | 读末条取上次 anchor；阶段 5 追加一条 |

---

## 源文档（新结构）

产品文档已拆分为「总览 + 模块」两层，本 skill 关注的源文档是：

| 路径 | 角色 |
|------|------|
| `docs/product.md` | **总览**（项目定位、用户画像、核心循环、模块清单、模块依赖、视觉基调） |
| `docs/product/NN-xxx.md`（多个文件） | **模块详情**：每个模块的功能流程、数据状态、UI、音效、数值、验收标准、边缘情况 |
| `docs/coding_rules.md` | 协作契约 + 通用架构原则 + 引擎/语言最佳实践（**技术栈信息也在这里**，含其引入的 engine-rules.md 与 language-rules.md） |

模块文件可能在两次同步之间被**新增、删除、重命名（含序号变化）、修改**，下面的 diff 流程必须处理全部四种情况。

---

## 全局原则

1. **源文档变更通过 git diff 识别，而非靠 AI 推断**。这保证识别精确、可追溯。
2. **feature-list 是 append-only ledger**：删除即标记 obsolete，修改 done 即新增回归 feature。
3. **任何已 done 的 feature 不可修改**其 `id` / `description` / `acceptance_criteria`。
4. **未经用户确认不修改 feature-list.json**。
5. **AI 不在 main 分支操作**，且修改前工作区必须干净（docs 改动除外）。
6. **feature-list 相关文件字符串值中禁止裸双引号**：内部不得出现未转义的 `"`（含中文引号 `"…"`）。需引用时用 `\"…\"` 或中文书名号 `「…」`。每次写入下列任一文件后都必须 `python3 -m json.tool <path> > /dev/null` 验证：
   - `docs/feature-list.json`
   - `docs/features/F0XX.json`（每个本次改动的详情文件）
   - `docs/feature-list-revisions.json`

---

## 阶段 0：前置检查

**进入条件**：用户触发本 skill。

**产出**：环境就绪；找到上次同步的锚点。

**行为**：

1. 检查主索引 `docs/feature-list.json` 是否存在：
   - 不存在 → 告知用户应使用 `generate-feature-list`，本流程终止。
   - 存在 → 读取主索引取所有 feature 的当前 status / depends_on 等扫描字段；再读取 `docs/feature-list-revisions.json` 的 revision_log 数组（首次同步时该文件可能尚不存在，按"找不到锚点"处理）。详情文件不必预读，阶段 4 处理具体 feature 时再 `cat docs/features/F0XX.json`。

2. 检查 git 环境：
   - 当前在 `main` 分支 → 暂停，提示切换到工作分支后再继续。
   - 工作区不干净（除了 `docs/` 下的 md 文件以外有未提交改动）→ 询问用户三选一：
     a. 先 commit 现有改动
     b. stash 现有改动
     c. 放弃现有改动
   - 工作区只有 `docs/` 下的 md 改动 → 这是预期情况（用户刚改完源文档），继续。

3. 确定**对比锚点**（上一次同步时的 git commit）：
   - 读取 `docs/feature-list-revisions.json` 中 `revision_log` 数组最后一条的 `synced_at_commit` 字段。
   - 该字段存在 → 用它作为对比锚点。
   - 该字段不存在（首次使用本 skill 或老版本数据）→ 在 `git log` 中查找最近一次涉及 `docs/feature-list.json` 或 `docs/features/` 的 commit 作为锚点；若也找不到，使用 feature-list.json 首次出现的 commit 作为锚点。
   - 仍找不到 → 告知用户「无法确定上次同步点，将退化为整文档对比模式」，让用户确认是否继续。

4. 输出阶段 0 摘要：
   - 当前分支
   - 对比锚点 commit hash + 该 commit 的日期与一行说明
   - 当前 feature-list 中各状态 feature 的数量统计

---

## 阶段 1：收集用户先验

**进入条件**：阶段 0 完成。

**产出**：用户的「这次主要想做什么」描述（可选）。

**行为**：

1. 询问用户：「在我读 git diff 之前，请简要说明这次源文档修改的主要意图（例如：『新增了 03-cultivation 模块』、『修改了得分规则』、『暂停界面加了提示文案』）。这能帮我更准确地理解 diff，避免误判表达调整为语义变化。」

2. 用户回答 → 记录为本次同步的「用户先验」，会在阶段 2 用到。

3. 用户回复「自己看 diff 即可，不想说」→ 跳过先验，进入阶段 2。

> 这一步可跳过，但**强烈建议不跳过**。带着先验做差异分析，准确率显著高于纯靠 diff 推断。

---

## 阶段 2：基于 git diff 的差异分析

**进入条件**：阶段 1 完成。

**产出**：一份精确的差异报告。

**行为**：

### 2.1 拉取 diff（覆盖新结构的全部文件）

按下列顺序执行 git diff。每个命令同时覆盖未提交改动（`<锚点> HEAD` 即可包含已 commit；再补一条 `git diff HEAD -- ...` 获取工作区改动）：

```
# 总览
git diff <锚点 commit> -- docs/product.md

# 模块目录的"哪些文件被改动 / 新增 / 删除 / 重命名"
git diff --stat -M <锚点 commit> -- docs/product/
git diff --name-status -M <锚点 commit> -- docs/product/

# 模块目录的逐文件内容 diff
git diff -M <锚点 commit> -- docs/product/

# 编码规则
git diff <锚点 commit> -- docs/coding_rules.md
```

`-M` 让 git 识别"重命名/改名"（例如 `02-foo.md` 改名为 `03-foo.md` 时给出 `R` 状态），避免把它误判为"删除一个 + 新增一个"。

### 2.2 把 diff 分类

结合阶段 1 的用户先验，把每一处变更分到下列四类之一：

- **a. 实质性新增**：增加了一段全新的产品规则、规则变更、约束；或新增了一个模块文件。
- **b. 实质性修订**：原有规则的语义变化（数值变了、行为变了、条件变了）；或模块文件被改名但内容相同（仅仅是文件重命名，**视为表达性调整**，除非内容也有实质变化）。
- **c. 实质性删除**：原本的功能被移除、被列入"明确不做的事"，或整个模块文件被删除。
- **d. 表达性调整**：仅措辞、排版、错别字修复、纯重命名；语义未变。**不产生任何 feature 变更**。

### 2.3 映射到现有 feature

把 a/b/c 三类变更映射到现有 feature（通过 `source` 字段定位）：

- 新增 → 找出对应的新建 feature 占位
- 修订 → 找出受影响的现有 feature id
- 删除 → 找出对应的现有 feature id

**模块文件重命名**：如果一个模块文件改名（如 `02-foo.md` → `03-foo.md`），所有 `source` 引用旧路径的 feature 都需要更新 `source` 字段（仅这一项调整，**不算 feature 变更**，但要在差异报告"路径修正"小节列出）。

### 2.4 特别考察：done feature 的连带回归

每一个被识别为「修订 done feature」的项，列出**所有 depends_on 包含该 feature 的其他 feature**，提示用户「这些 feature 的实现建立在被修订 feature 的旧行为上，是否需要回归验证？」

### 2.5 输出差异报告

```
## 本次差异报告（基于 git diff，锚点 commit: <hash>）

### 表达性调整（不产生变更）
- product.md 第 X 节：[一句话描述]，仅措辞调整
- product/02-foo.md 改名为 product/03-foo.md，内容未变
- ...

### 路径修正（不算变更，但需要更新 source）
- 模块文件 product/02-foo.md → product/03-foo.md：F005、F006 的 source 字段需要更新
- ...

### 实质性变更

#### 新增 [N 项]
1. 来源：product/04-combat.md（新增模块文件）
   变更内容：<一两句话说明>
   建议处理：新增 feature「<title>」，依赖 [F0XX, F0YY]
2. ...

#### 修订 [N 项]
1. 受影响 feature：F0XX (status: <当前状态>)
   变更内容：<一两句话说明>
   建议处理：<根据状态决定>
   连带影响：依赖 F0XX 的 feature [F0YY, F0ZZ] 可能需要回归验证
2. ...

#### 删除 [N 项]
1. 受影响 feature：F0XX (status: <当前状态>)
   变更内容：<一两句话说明>
   建议处理：<根据状态决定>
2. ...

### 与用户先验的吻合度
<说明：用户提到的意图是否在 diff 中都找到了对应；diff 中是否有用户没提到的变化（可能是无意中改的）>

### 待用户决策的事项
- <例如：F008 修订是否需要触发对 F012、F015 的回归验证 feature>
- ...
```

### 2.6 不修改任何文件

此阶段**只输出报告**，等待用户确认。

---

## 阶段 3：用户审阅与决策

**进入条件**：阶段 2 输出了差异报告。

**产出**：用户对每项变更的最终决策。

**行为**：

1. 提示用户：「请审阅以上差异报告。你可以：
   a. 确认全部建议，开始执行
   b. 调整某些项的处理方式（指出哪条改怎么处理）
   c. 中止本次同步（如发现 diff 与你预期不符，可能需要回头检查 md 文件是否被错误修改）」

2. 用户选 a → 进入阶段 4。
3. 用户选 b → 记录调整意见，重新输出修订后的差异报告，再次确认。
4. 用户选 c → 终止本流程，**不修改任何文件**。

> **未得到用户明确确认前，绝不进入阶段 4。**

---

## 阶段 4：执行修改

**进入条件**：阶段 3 用户确认。

**产出**：修改后的 `docs/feature-list.json`（主索引）+ 新增/修订的 `docs/features/F0XX.json`（详情）。每次新增或修订必须**同时**写两边，确保 id 集合一致。

### 字段分布提示（决定写哪里）

| 字段 | 写入位置 |
|------|------|
| `id` | 主索引 + 详情（详情里冗余存一份方便单文件可读） |
| `title` / `status` / `depends_on` / `estimated_scope` / `completed_at` | 主索引 |
| `description` / `acceptance_criteria` / `source` / `notes` | 详情 |

### 处理新增项

- 在主索引 `features` 数组末尾追加 `{id, title, status, depends_on, estimated_scope, completed_at: null}` 条目；同时在 `docs/features/` 下创建 `F0XX.json` 写入 `{id, description, acceptance_criteria, source, notes}`。
- id 使用未被使用过的下一个（即使中间有 obsolete 留下的空洞也用下一个新 id，**不复用旧 id**）。
- 初始 `status` 为 `pending`，详情的 `notes` 为空字符串。
- 如果新 feature 依赖某个已 done feature 的能力扩展，在 description 中明确说明。
- `source` 精确到模块文件 + 章节。

### 处理删除项

| 当前 status | 处理 |
|------------|------|
| `pending` | 主索引 `status` 改为 `obsolete`；详情 `notes` 追加「于 <时间戳> 因 product 文档修订移除：<原因>」 |
| `in_progress` | 主索引 `status` 改为 `obsolete`；详情 `notes` 追加移除原因；并在差异报告的「待用户决策」区提示「已写代码可能需要回滚」 |
| `done` | 主索引 `status` 改为 `obsolete_done`；详情 `notes` 追加移除原因；**并在末尾新增一个回归 feature**「移除 F00X 引入的 XXX 功能」，依赖关系视情况 |
| `obsolete` / `obsolete_done` | 不变，但在详情 `notes` 追加一条「再次确认本期不做」 |

### 处理修订项

| 当前 status | 处理 |
|------------|------|
| `pending` | 修改详情文件的 `description` / `acceptance_criteria`，`notes` 追加「于 <时间戳> 因 product 文档修订更新」；主索引仅 title 受影响时才改 |
| `in_progress` | 同 `pending`，并在差异报告的「待用户决策」区提示「当前实现可能需要调整」 |
| `done` | **不修改原 feature 的任何字段**（主索引条目 + 详情文件都保留为历史档案）。在末尾新增一个 feature「修订 F00X 实现以匹配 <来源> 新版规则」，`depends_on` 包含原 F00X，新建对应的详情文件，acceptance_criteria 写明新行为 |
| `obsolete` / `obsolete_done` | 一般不处理。若用户希望"重新启用"该功能，应在差异报告的「待用户决策」区由用户明确确认后再新增 feature |

### 处理路径修正（模块文件重命名）

- 更新所有受影响 feature **详情文件**（`docs/features/F0XX.json`）的 `source` 字段为新路径。
- **不修改其他字段**。
- 不计入「修订」处理。

### 处理连带回归

对阶段 2.4 识别出的「修订 done feature 的连带影响」，按用户在阶段 3 的决策：

- 需要回归 → 在末尾新增 feature「回归验证 F0YY 在 F0XX 修订后的行为」，依赖于刚才新增的修订 feature
- 无需回归 → 不新增，但在修订 feature 的 `notes` 中记录「已与用户确认 F0YY、F0ZZ 无需回归」

---

## 阶段 5：更新 meta 与提交

**进入条件**：阶段 4 完成。

**产出**：更新主索引 meta + 修订日志；git commit。

**行为**：

1. 更新主索引 `docs/feature-list.json` 的 `meta.total_features`、`meta.generated_at`（改为本次同步时间）。`meta.generated_from` 应保持为 `["docs/product.md", "docs/product/**/*.md", "docs/coding_rules.md"]`。

2. 在 `docs/feature-list-revisions.json` 的 `revision_log` 数组末尾追加一条（**不再写入主索引的 meta**）：
   ```json
   {
     "revised_at": "<ISO 8601 时间戳>",
     "synced_at_commit": "<HEAD commit hash>",
     "anchor_commit": "<对比锚点 commit hash>",
     "user_intent": "<阶段 1 收集的用户先验，未收集则为 null>",
     "summary": "<一句话总结本次修订>",
     "added": ["F0XX", "F0YY"],
     "obsoleted": ["F0AA"],
     "revised_via_new_feature": [{"original": "F0BB", "regression": "F0CC"}],
     "source_path_updates": [{"feature": "F005", "from": "product/02-foo.md", "to": "product/03-foo.md"}],
     "depends_on_warnings": ["F0DD", "F0EE"]
   }
   ```

   > `synced_at_commit` 是下一次本 skill 运行时的对比锚点，不可省略。
   > `source_path_updates` 是新增字段，用于追溯模块文件重命名导致的 source 修正。

3. 自检清单（AI 自行核对，不通过则回阶段 4 修复）：
   - [ ] 没有任何条目被物理删除（主索引 + 详情目录）
   - [ ] 没有任何已 done feature 的 `id` / `description` / `acceptance_criteria` 被修改（主索引和详情都保持原值）
   - [ ] 主索引中每个 feature.id 在 `docs/features/` 下都有同名详情文件，反之亦然
   - [ ] 所有新增 feature 的 id 都是未被使用过的
   - [ ] 主索引中所有 `depends_on` 引用的 id 都存在
   - [ ] 所有 `depends_on` 没有指向 `obsolete` / `obsolete_done` 状态的 feature（如有，应在差异报告中已提示）
   - [ ] 详情文件中所有 `source` 字段指向真实存在的模块文件（含本次重命名后的新路径）
   - [ ] `docs/feature-list-revisions.json` 末条的 `synced_at_commit` 字段已正确填入
   - [ ] 主索引 `meta.total_features` 与 features 数组长度一致，并等于 `docs/features/` 下的详情文件数
   - [ ] `python3 -m json.tool docs/feature-list.json > /dev/null` 通过
   - [ ] `python3 -m json.tool docs/feature-list-revisions.json > /dev/null` 通过
   - [ ] 对每个本次新增/修订的详情文件 `python3 -m json.tool docs/features/F0XX.json > /dev/null` 通过

4. 执行 git commit：
   ```
   git add docs/feature-list.json docs/feature-list-revisions.json docs/features/
   git commit -m "chore(sync): update feature-list per docs revision

   Anchor: <锚点 commit 短 hash>
   Added: <N> features
   Obsoleted: <N> features
   Revised via new feature: <N> features

   <一句话总结>"
   ```

   > 源文档（`docs/product.md`、`docs/product/*.md`、`docs/coding_rules.md`）的改动应在用户调用本 skill **之前**就已 commit。若仍在工作区未提交，应在阶段 0 提示用户先 commit md 改动再来调用本 skill——这样 git diff 才有意义。

5. **不执行 git push**。

---

## 阶段 6：交班

**进入条件**：阶段 5 完成。

**产出**：本次同步总结。

**行为**：

1. 输出同步总结：
   - 「本次同步基于 anchor commit `<hash>` 的差异分析」
   - 「新增 N 个 feature，废弃 M 个 feature，新增 K 个回归 feature，修正 source 路径 J 处」
   - 「下一个可执行的 feature：F0XX - <title>」（如果有）
   - 「需要你额外注意：<列出 obsolete in_progress 的代码回滚提示、需要回归验证的 feature 等>」

2. **不自动开始下一个 feature**，等待用户指令。

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 找不到对比锚点 | 退化为整文档对比模式，但明确告知用户精度会下降 |
| diff 显示改动巨大（例如超过 50% 行数变化或新增/删除模块文件超过 3 个） | 暂停，提示用户「这是一次大重构，建议拆分成多次小同步，或考虑用 generate-feature-list 重新生成」 |
| diff 与用户先验严重不一致 | 暂停，列出不一致点，让用户核对是否修改了不该修改的内容（可能是误改） |
| `docs/product.md` 的"模块清单"与 `docs/product/` 实际文件不一致 | 暂停，列出差异，让用户先修复总览，不要靠猜测继续 |
| `feature-list.json` / 详情文件 / `feature-list-revisions.json` 任一存在格式错误（含裸双引号） | 停止，原文报告，不尝试自动修复格式 |
| 阶段 4 修改过程中报错 | 停止，建议用户 `git restore docs/feature-list.json docs/feature-list-revisions.json docs/features/` 回滚到本次修改前的状态 |
| 任何 git 命令失败 | 立即停止，原文报告错误，不尝试自动修复 |

---

## Git 操作的允许与禁止

继承 execute-next-feature 中的同名约束。简要重述：

- **允许**：在非 main 分支上 `git diff` / `git log` / `git add docs/feature-list.json docs/feature-list-revisions.json docs/features/` / `git commit`
- **需用户确认**：切换分支、stash、restore
- **禁止**：force 操作、reset --hard、操作 main 分支、push

---

## 流程速查表

```
阶段 0：前置检查 ──────── 检查环境、找到对比锚点
   ↓
阶段 1：收集用户先验 ─── 询问"这次主要想做什么"
   ↓
阶段 2：基于 diff 的差异分析 ── 输出差异报告
        （覆盖 product.md + product/ 目录 + coding_rules.md）
   ↓
阶段 3：用户审阅决策 ─── 等待确认 ──→ 不通过则回阶段 2 调整
   ↓
阶段 4：执行修改 ──────── 按规则更新 feature-list（含 source 路径修正）
   ↓
阶段 5：更新 meta 与 commit ── 自检、提交
   ↓
阶段 6：交班 ──────────── 输出总结、等待指令
```
