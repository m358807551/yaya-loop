---
name: generate-feature-list
description: 当用户要求首次生成、初始化、或彻底重新生成 docs/feature-list.json 时使用。本 skill 读取 docs/product.md（总览）、docs/product/ 目录下所有模块文件、以及 docs/coding_rules.md，按依赖顺序拆解出可逐步实现的 feature 列表。仅用于"从零到一"或"推倒重来"。增量更新请用 sync-feature-list。触发短语示例："生成 feature-list"、"初始化任务列表"、"拆解游戏功能"。
---

# 生成 feature-list.json

## 何时用本 skill

- `docs/feature-list.json` 不存在 → 用本 skill 首次生成。
- 产品被推倒重来（用户明确要求"重新生成、扔掉旧的"）→ 用本 skill。
- **其他情况（产品文档增量改动）→ 一律用 `sync-feature-list`，不要用本 skill**。

如果 `docs/feature-list.json` 已存在且用户没有明确说"扔掉旧的"，先提示用户「你是要增量同步还是彻底重生？前者请用 sync-feature-list」，并等待确认再继续。

## feature-list 文件三层结构

本 skill 一次性产出三类文件：

| 路径 | 内容 |
|------|------|
| `docs/feature-list.json` | 主索引：每个 feature 的 `id` / `title` / `status` / `depends_on` / `estimated_scope` / `completed_at` + meta |
| `docs/features/F0XX.json` | 每个 feature 的详情：`id` / `description` / `acceptance_criteria` / `source` / `notes` |
| `docs/feature-list-revisions.json` | 空的修订日志（`{"revision_log": []}`），交给 sync-feature-list 后续维护 |

若已存在残留旧文件而用户选择"扔掉旧的"，须把 `docs/features/` 下旧的 `F*.json` 全部清空后重写，避免脏数据混入。

---

## 输入文档（新结构）

产品文档已拆分为「总览 + 模块」两层，本 skill 必须**全部读完**才能动手：

| 路径 | 角色 |
|------|------|
| `docs/product.md` | **总览**：项目定位、用户画像、核心循环、模块清单、模块依赖、视觉基调 |
| `docs/product/NN-xxx.md`（多个文件） | **模块详情**：每个模块的功能流程、数据状态、UI、音效、数值、验收标准、边缘情况 |
| `docs/coding_rules.md` | 协作契约 + 通用架构原则 + 引擎/语言最佳实践。**技术栈信息也在这里**（含其引入的 `docs/coding-rules/engine-rules.md` 与 `docs/coding-rules/language-rules.md`） |

读取顺序建议：
1. 先读 `docs/product.md` 拿到模块清单与依赖关系。
2. 按总览中"模块依赖关系"指示的拓扑顺序读 `docs/product/*.md`。
3. 最后读 `docs/coding_rules.md`，把架构约束和技术栈作为拆解粒度与顺序的"硬约束"。

如果总览的"模块清单"与 `docs/product/` 实际文件不一致（多了、少了、命名对不上），**停下来报告差异，让用户先修复，不要靠猜测继续**。

---

## 拆解原则

1. **每个 feature 是一个可独立验证的最小完整功能**。完成后能跑、能看到/测到一个明确的结果。是"玩家能做到 X"或"系统能产生 Y"，不是"实现 XX 类"这种实现细节。
2. **顺序遵循依赖关系**：后面的 feature 只能依赖前面已列出的 feature。**第一个 feature 必定是基础设施类**（例如"项目能跑起来并显示空窗口"），不依赖任何具体玩法。
3. **顺序遵循模块依赖**：按 `docs/product.md` 中"模块依赖关系"声明的拓扑序拆解。模块 A 依赖模块 B → B 的核心 feature 排在 A 之前。
4. **顺序遵循架构约束**：`coding_rules.md` 强调"数据与表现分离"、"核心规则纯函数化"等，则同一功能的数据/规则层 feature 必须排在表现层 feature 之前。
5. **粒度匹配引擎与技术栈**：每个 feature 应当是"AI 一次会话能写完并验证"的规模。出现 `large` 必须继续拆，不允许保留 `large`。
6. **不过度设计**：只拆 product 文档里明确写了的内容。任何模块文件中"明确不做"或"边缘情况但不处理"的功能不要出现在 feature 里。
7. **不写 how，只写 what 加可观察的验收**。验收标准的每一条都是"做完后我能怎么验证"，模糊描述（"渲染正确"）不接受。
8. **覆盖率优先于美观**：宁可拆得啰嗦，也不要漏掉模块文件中已经定下的功能或数值。
9. **source 字段精确到模块文件**：例如 `product/03-combat.md#数值与配置`，而不是只写一个章节号。

---

## JSON 结构

### 主索引 `docs/feature-list.json`

```json
{
  "meta": {
    "generated_from": [
      "docs/product.md",
      "docs/product/**/*.md",
      "docs/coding_rules.md"
    ],
    "generated_at": "<ISO 8601 时间戳>",
    "total_features": <数字>,
    "details_dir": "docs/features/",
    "revisions_file": "docs/feature-list-revisions.json",
    "notes": "<一句话说明拆解思路>"
  },
  "features": [
    {
      "id": "F001",
      "title": "<动词短语，例如：搭建项目骨架并运行空窗口>",
      "status": "pending",
      "depends_on": [],
      "estimated_scope": "small | medium | large",
      "completed_at": null
    }
  ]
}
```

### 详情文件 `docs/features/F0XX.json`（每个 feature 一份）

```json
{
  "id": "F001",
  "description": "<2-4 句说明这一步要达成什么可观察的效果>",
  "acceptance_criteria": [
    "<可手动验证的判定条件 1>",
    "<可手动验证的判定条件 2>"
  ],
  "source": "<对应到哪个模块文件的哪一节，例如：product/02-cultivation.md#修炼机制；基础设施写 infrastructure>",
  "notes": ""
}
```

### 修订日志 `docs/feature-list-revisions.json`

```json
{
  "revision_log": []
}
```

字段说明：

- `id`：F001 起递增，三位数字保留扩展空间。**主索引和详情文件的 id 必须一一对应**。
- `depends_on`：仅严格依赖的前置 feature id。基础设施 feature 为空数组。**只在主索引存。**
- `acceptance_criteria`：每条是"做完后我怎么验证"的具体陈述。可机验、可手测、可肉眼看出都行，但**禁止形容词式描述**。
- `source`：精确到模块文件 + 章节（如 `product/02-cultivation.md#数值与配置`）。基础设施类写 `infrastructure`。跨多模块的少见情况写主模块即可。
- `estimated_scope`：相对估计——`small` ≈ 一次会话能写完并验证；`medium` ≈ 一次会话能写完但需要多轮调试；`large` ≈ 必须继续拆，不允许出现在最终输出。**只在主索引存。**
- `status`：首次生成一律 `pending`。其他取值（`in_progress` / `done` / `obsolete` / `obsolete_done` / `blocked`）由 execute-next-feature 与 sync-feature-list 维护。**只在主索引存。**
- `completed_at`：首次生成一律为 `null`。**只在主索引存。**
- `notes`：首次生成一律为空字符串。**只在详情文件存。**
- `revision_log`：首次生成为空数组，由 sync-feature-list 后续往里追加。**只在 `docs/feature-list-revisions.json` 存。**

JSON 字符串值中**禁止裸双引号**：内部不得出现未转义的 `"`（含中文引号 `"…"`）。需引用时用 `\"…\"` 或中文书名号 `「…」`。写完后必须用 `python3 -m json.tool <path> > /dev/null` 验证主索引、每个详情文件、以及 revisions 文件都合法。

---

## 自检清单（生成后输出前必跑）

- [ ] 第一个 feature 是基础设施类，不依赖任何具体玩法
- [ ] 没有 feature 的 `depends_on` 指向后面 id（无后向依赖）
- [ ] 没有 feature 的 `estimated_scope` 是 `large`
- [ ] 每个模块文件里描述的核心玩法都有对应 feature 覆盖
- [ ] 每个模块文件里"明确不做"或"边缘情况但不处理"的功能**没有**出现在 feature 中
- [ ] `coding_rules.md` 强调的架构原则（数据与表现分离、核心规则纯函数化等）在 feature 顺序中得到体现
- [ ] 所有详情文件的 `source` 字段指向真实存在的模块文件
- [ ] 主索引中所有 `depends_on` 引用的 id 都存在
- [ ] 所有 feature 的 `status` 为 `pending`、`completed_at` 为 `null`、详情 `notes` 为空字符串
- [ ] `docs/feature-list-revisions.json` 已写入 `{"revision_log": []}`
- [ ] **id 一致性**：主索引 `features` 数组的 id 集合 == `docs/features/` 下 `F*.json` 文件名 stem 集合 == `meta.total_features`
- [ ] JSON 字符串值中无裸双引号；主索引、所有详情文件、revisions 文件分别 `python3 -m json.tool <path>` 通过

自检不通过的项必须修正后再输出。

---

## 输出流程

1. 读完所有输入文档后，**先用一段简短文字（不超过 6 句）告诉用户**：
   - 拆解思路（按什么序、分几层）
   - 总共拆了多少个 feature
   - 各模块大致分配了多少个 feature
   - 是否发现文档矛盾或歧义需要先确认

2. **有疑问则停在这里等用户回复**，不要继续写 JSON。

3. 没有疑问 → 一次性写入三类文件：
   - 主索引 `docs/feature-list.json`
   - 每个 feature 的详情文件 `docs/features/F0XX.json`（确保目录存在 `mkdir -p docs/features`）
   - 空的修订日志 `docs/feature-list-revisions.json`（内容仅为 `{"revision_log": []}`）

   然后跑自检清单中的 JSON 校验，全部通过后告诉用户文件已生成 + 第一个可执行 feature 是哪个。

4. **不自动开始实现**。后续走 `execute-next-feature`。
