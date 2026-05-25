# 02 · feature-list 三文件 schema

## 总览：三文件结构

```
docs/
├── feature-list.json              ← 主索引：扫得快，每会话加载
├── features/
│   ├── F001.json                  ← 详情：按需 cat，不自动进上下文
│   ├── F002.json
│   └── ...
└── feature-list-revisions.json    ← 修订日志：sync-feature-list 自动维护
```

**为什么拆三层**：主索引保持轻量（每个 feature 5-6 个字段），AI 一次可扫几百个 feature；详情文件懒加载，避免无关 feature 的 acceptance_criteria 占用上下文；修订日志独立，方便回溯产品演化。

---

## 文件 1：`docs/feature-list.json`（主索引）

```json
{
  "meta": {
    "generated_from": [
      "docs/product.md",
      "docs/product/**/*.md",
      "docs/coding_rules.md"
    ],
    "generated_at": "2026-05-23T05:46:48Z",
    "total_features": 95,
    "details_dir": "docs/features/",
    "revisions_file": "docs/feature-list-revisions.json",
    "notes": "按模块依赖序拆解：infra → 02 地图 → 01 角色 → 03 资源 → 04 建造 → ...；模块内部按 数据→规则→表现/交互 纵切片推进。"
  },
  "features": [
    {
      "id": "F001",
      "title": "搭建项目骨架并运行空主窗口",
      "status": "done",
      "depends_on": [],
      "estimated_scope": "small",
      "completed_at": "2026-05-16T10:30:00Z"
    },
    {
      "id": "F002",
      "title": "...",
      "status": "pending",
      "depends_on": ["F001"],
      "estimated_scope": "medium",
      "completed_at": null
    }
  ]
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | `F` + 三位数字，从 F001 起递增。**主索引和详情文件的 id 必须一一对应。** |
| `title` | string | 动词短语，描述这一步要让用户/系统能做到什么。 |
| `status` | enum | 取值：`pending` / `in_progress` / `done` / `obsolete` / `obsolete_done` / `blocked` |
| `depends_on` | string[] | 严格依赖的前置 feature id。基础设施 feature 为 `[]`。**只在主索引存。** |
| `estimated_scope` | enum | `small`（一次会话能写完并验证）/ `medium`（一次会话能写完但需多轮调试）/ `large`（必须继续拆，不允许出现在最终输出） |
| `completed_at` | string \| null | ISO 8601 时间戳，未完成为 `null` |

---

## 文件 2：`docs/features/F0XX.json`（每个 feature 一份）

```json
{
  "id": "F042",
  "description": "玩家可在建造面板放置 1×2 木墙蓝图；小人取材建造后形成阻挡寻路的实体。",
  "acceptance_criteria": [
    "建造面板「木墙」可见且选中后进入放置模式",
    "1×2 占地虚影跟随鼠标，合法位置绿色、非法红色",
    "下单后地图保留蓝色蓝图，小人接单取 2 木头",
    "施工 5 秒后木墙实体生成，寻路系统识别为阻挡"
  ],
  "source": "product/04-building.md#木墙",
  "notes": "TODO: 拆除时需返还 1 木头（acceptance 未要求，本次未实现）。建议后续 feature 处理。"
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 与主索引完全一致 |
| `description` | string | 2-4 句说明：这一步要达成什么**可观察**的效果。What，不写 How |
| `acceptance_criteria` | string[] | 每条是"做完后我能怎么验证"的**具体**陈述，禁止形容词式（如「渲染正确」） |
| `source` | string | 精确到模块文件 + 章节，如 `product/04-building.md#木墙`。基础设施类写 `infrastructure` |
| `notes` | string | 首次生成空。execute-next-feature 完成时追加实现要点、占位资源、TODO、代码气味 suggest 项 |

---

## 文件 3：`docs/feature-list-revisions.json`（修订日志）

```json
{
  "revision_log": [
    {
      "revised_at": "2026-05-20T08:30:00Z",
      "synced_at_commit": "78cfcb9",
      "anchor_commit": "e25178b",
      "user_intent": "加入作息系统",
      "summary": "新增 11-schedule 模块，引入 F063~F066 作息相关 feature；标记 F046/F047 心境影响修炼为 obsolete（被作息系统替代）",
      "added": ["F063", "F064", "F065", "F066"],
      "obsoleted": ["F046", "F047"],
      "revised_via_new_feature": [],
      "source_path_updates": [],
      "depends_on_warnings": []
    }
  ]
}
```

由 `sync-feature-list` skill 自动追加。首次生成内容为 `{"revision_log": []}`。

---

## 状态机：feature 的 status 流转

```
pending ──(execute 阶段 2)──→ in_progress ──(execute 阶段 7 + 用户确认)──→ done
   │                              │
   │                              └──(用户中途放弃)──→ pending
   │
   ├──(sync-feature-list 判定不再相关)──→ obsolete
   └──(被新 feature 拆走)──→ obsolete

done ──(sync-feature-list 判定已实现部分被产品移除)──→ obsolete_done
pending ──(依赖意外失效)──→ blocked
```

- `obsolete`：从未实现就被废弃。
- `obsolete_done`：曾实现但产品演化中被移除。区分这俩是为了 git 历史可追溯（obsolete_done 的代码可能还在）。

---

## 硬约束

### JSON 字符串值禁止裸双引号

JSON 字符串内部不得出现未转义的 `"`（含中文 `"…"`）。需引用时用 `\"…\"` 或中文书名号 `「…」`。

**反例**（解析失败）：
```json
"description": "在编辑器中预览，按 ↑ 键，观察"游戏结束"是否触发"
```

**正例**：
```json
"description": "在编辑器中预览，按 ↑ 键，观察「游戏结束」是否触发"
```

**写入后必须立即校验**：
```bash
python3 -m json.tool docs/feature-list.json > /dev/null
python3 -m json.tool docs/features/F0XX.json > /dev/null
python3 -m json.tool docs/feature-list-revisions.json > /dev/null
```

### id 一致性

- 主索引 `features[]` 的 id 集合 == `docs/features/` 下 `F*.json` 文件名 stem 集合 == `meta.total_features`
- 不允许主索引存在而详情缺失（反之也不行）

### depends_on 不能后向

- feature F0NN 的 `depends_on` 中不能出现 id > NN 的 feature
- generate-feature-list 输出后会自检；sync-feature-list 在新增 feature 时会插入到正确位置

---

## 拆解原则（generate-feature-list 用的）

1. **每个 feature 是一个可独立验证的最小完整功能**——「用户能做到 X」或「系统能产生 Y」，不是「实现 XX 类」。
2. **第一个 feature 必定是基础设施**：例如「项目能跑起来并显示空窗口」，`depends_on: []`。
3. **顺序遵循模块依赖**：被依赖的模块的核心 feature 排在前面。
4. **顺序遵循架构约束**：coding_rules.md 强调"数据与表现分离" → 同功能的数据层 feature 排在表现层之前。
5. **不允许 `large`**：粒度过大必须继续拆。
6. **不过度设计**：只拆 product 文档明确写了的内容，"未来可能" / "边缘但不处理" 一律不出现。
7. **不写 how，只写 what + 可观察的验收**。

---

## 实际使用模式

| 操作 | 用哪个 skill | 改哪些文件 |
|------|------------|----------|
| 项目首次拆解 | generate-feature-list | 创建主索引 + 所有 F0XX.json + 空 revisions |
| 产品发生增量变更 | sync-feature-list | 增/删/改主索引 + 增/删/改 F0XX.json + 追加 revisions |
| 实现一个 feature | execute-next-feature | 切 in_progress → 切 done；F0XX.json 的 notes 追加实现要点 |
| 选个坏味道重构 | pick-refactor-smell | 只读所有 F0XX.json 的 notes，不修改 |

更多细节见各 skill 的 SKILL.md（Claude Code 用户）或 ai-agnostic-prompts/*.prompt.md（其他 CLI 用户）。
