---
name: product-change-standardizer
version: 2.0
description: 产品变更总调度。任何涉及产品需求、功能、UI、音效、Bug 修复的变更都从这里进入。负责路由到合适的子 skill、统一写入模块文件、调用同步 skill。这是产品变更的唯一入口。
triggers:
  - 用户提出产品改进、新功能、Bug 修复、需求调整
  - 用户说"做一个 XXX"（项目初始化）
  - 用户说"改进"、"优化"、"增加"、"删除"、"修复"、"调整"、"新需求"
priority: high
---

# product-change-standardizer（产品变更总调度）

## 核心铁律

1. **`docs/product.md` 及 `docs/product/*.md` 是产品设计的唯一真实来源**。
2. **任何产品变更必须先更新文档，再同步 feature-list.json，最后才进入实现**。
3. **本 skill 是唯一的写入者**。子 skill（elicitor、sketcher）只返回结构化数据，由本 skill 落盘。
4. **不写技术栈、不写实现细节**。编码规范走 `docs/coding_rules.md`。
5. **product.md 描述 what，不描述 how**。

---

## 文件结构约定

```
docs/
├── product.md              # 总览（项目定位、用户画像、核心循环、模块清单）
├── product/                # 模块文件夹
│   ├── 01-xxx.md          # 模块（数字前缀 = 创建顺序）
│   ├── 02-xxx.md
│   └── ...
└── ui-mockups/             # 可选：html+tailwind UI 探索（与 product.md 解耦）
    └── xxx.html
```

**模块文件命名**：`NN-kebab-case.md`，`NN` 是两位数序号（01、02、...），按创建/依赖顺序。

---

## 模块文件标准模板

每个 `docs/product/NN-xxx.md` 必须按此结构写。AI 写、用户不写，但结构固定：

```markdown
# 模块名

## 模块定位
（一句话：这个模块是干什么的、为什么存在）

## 核心循环 / 功能流程
（用户在这个模块里能做什么、典型流程是什么。可用编号步骤）

## 数据与状态

### 数据模型
（关键数据字段、类型、默认值）

### 状态机
（≥3 个状态时必须画出来。用列表或简单文字图）

### 持久化要求
（哪些数据要存、丢失后果）

## UI / 交互

### 主界面布局
（ASCII 线框图。由 product-ui-sketcher 生成）

### 交互细节
（每个可交互元素的行为）

### 意图说明
（为什么这么设计，传达什么感觉）

### 视觉探索
（可选：指向 docs/ui-mockups/xxx.html）

## 音效
（由 product-audio-sketcher 生成。每个音效一条目）

### sfx_xxx
- **时机**：什么情况下触发
- **意图**：传达什么感觉
- **时长**：大约多久
- **占位文件**：_placeholder_xxx.wav

## 数值与配置
（可调参数、默认值、范围。这部分要细，AI 实现时直接读）

## 验收标准
（每条都是可验证的事实陈述，用编号列表）

## 边缘情况
（断电、切走、异常输入、并发操作...）

## 变更历史
- YYYY-MM-DD：初始版本
- YYYY-MM-DD：[变更内容] - [变更原因]
```

---

## 总览文件（docs/product.md）模板

```markdown
# 项目名

## 一句话定位
（这个产品是给谁、解决什么问题、关键体验是什么）

## 用户画像
（目标用户、使用场景、使用频率）

## 核心循环
（最重要的一段——用户用这个产品的核心闭环是什么）

## 模块清单
| 序号 | 文件 | 模块名 | 状态 |
|------|------|--------|------|
| 01 | [01-xxx.md](./product/01-xxx.md) | XXX | draft / done |
| 02 | ... | ... | ... |

## 模块依赖关系
（哪些模块依赖哪些。可用文字描述或简单图）

## 整体视觉风格基调
（不细描述每个 UI，只定基调：暖色 vs 冷色、写实 vs 卡通、紧张 vs 治愈...）

## 变更历史
- YYYY-MM-DD：项目初始化
- YYYY-MM-DD：新增模块 XX
```

---

## 执行流程

### 步骤 1：识别用户意图

用 1-2 句话复述用户的变更点，问："是否确认按产品变更流程处理？"
（防止误触发。例如用户只是闲聊"番茄钟好用吗"不应该启动流程）

### 步骤 2：读取当前文档状态

必须读：
- `docs/product.md`（如果存在）
- `docs/product/*.md`（如果存在）
- `docs/feature-list.json`（如果存在；这是轻量主索引，含 id/title/status/depends_on，足够做路由判断。无需打开 `docs/features/F0XX.json` 详情目录——后续路由到的 sync/generate-feature-list 会按需读写）

判断当前状态属于以下哪种：

| 状态 | 判断条件 | 路由到 |
|------|---------|--------|
| **A. 初始化** | product.md 不存在或仅含模板 | product-init-elicitor |
| **B. 新增模块** | 变更明显属于一个尚不存在的模块 | product-spec-elicitor（模式：新模块） |
| **C. 修改现有模块** | 变更属于已有模块的范围内 | product-spec-elicitor（模式：修改） |
| **D. Bug 修复** | 用户描述了已实现功能的问题 | product-spec-elicitor（模式：Bug） |
| **E. 跨模块变更** | 影响多个模块（如增加全局设置） | product-spec-elicitor（模式：跨模块） |

### 步骤 3：路由到子 skill

#### 路由到 product-init-elicitor（状态 A）

调用 `product-init-elicitor`，传入用户的一句话描述。

elicitor 会全程交互问完所有维度，返回一个**结构化草稿**（包含总览 + 各模块的所有维度内容，但 UI 线框图和音效条目可能仍是占位）。

#### 路由到 product-spec-elicitor（状态 B/C/D/E）

调用 `product-spec-elicitor`，传入：
- 变更描述
- 模式（新模块 / 修改 / Bug / 跨模块）
- 受影响模块的当前内容

elicitor 会**适度追问**（只问明显模糊的关键点），返回一个**结构化变更补丁**。

### 步骤 4：补全 UI 和音效维度

检查 elicitor 返回的草稿/补丁，对每个**新增或修改了 UI 的部分**：

- 调用 `product-ui-sketcher`，传入该部分的功能描述和交互细节
- sketcher 返回 ASCII 线框图 + 意图说明
- 询问用户："要不要同时生成一个 html+tailwind mockup 放到 docs/ui-mockups/？"
  - 是 → sketcher 同时产出 html 文件
  - 否 → 仅 product.md 内 ASCII

对每个**新增或修改了音效需求的部分**：

- 调用 `product-audio-sketcher`，传入该部分的功能流程
- sketcher 追问音效时机、风格、时长，返回完整音效条目
- 自动生成 `_placeholder_xxx.wav` 占位文件名

### 步骤 5：写入文档

由本 skill 统一执行：

1. **新模块**：创建 `docs/product/NN-xxx.md`，按模板填入所有维度。`NN` 取当前最大序号 +1。
2. **修改现有模块**：精确编辑对应章节，不动其他章节。
3. **总览**：更新 `docs/product.md` 的模块清单、依赖关系（如有变化）。
4. **变更历史**：在受影响文件的"变更历史"小节追加一条 `YYYY-MM-DD：变更内容 - 原因`。
5. **占位音频文件**：若产生了 `_placeholder_*.wav`，登记到对应 feature 的 notes 字段（在步骤 6 同步时由 sync skill 处理）。

### 步骤 6：同步 feature-list.json

根据变更类型选择：

- **新增模块 / 大型重构** → 调用 `generate-feature-list`
- **现有模块小修改 / Bug** → 调用 `sync-feature-list`

调用后等待返回，**不要假设同步成功**——失败要告知用户。

### 步骤 7：汇报与下一步

清晰列出：

- 改了哪些文件、改了什么
- feature-list.json 同步状态
- 受影响的 feature 当前状态
- 是否产生了占位资源（音效、图片等）

询问用户：
- 对文档修改是否满意？
- 是否需要立即进入实现阶段？（提示走 `execute-next-feature`，不要在本 skill 内启动实现）

---

## 关键边界（不能违反）

1. **不写技术栈**。若用户在变更描述中混入技术决策（"用 Godot 的 AnimationPlayer 做"），剥离掉，只保留产品意图（"切换状态时要有过渡动画"）。

2. **不直接写代码**。即使用户说"顺手把代码也改了"，也要先走完产品文档流程。

3. **不自作主张做产品决策**。
   - 模糊点 → init-elicitor 全问，spec-elicitor 选关键点问
   - **绝不**："番茄钟时长我就定 25 分钟了"——这是用户该拍板的事

4. **不跳过同步**。每次写完文档必须调用 sync/generate-feature-list。

5. **不在已 done 的 feature 上偷偷改**。如果变更影响已完成 feature，应建议把状态改为 `blocked` 或新建子 feature 处理。

6. **关键变更前确认**。删除模块、删除已 done 的 feature、修改用户画像或核心循环这种"大动作"，必须二次确认。

---

## 失败模式与回滚

- **elicitor 返回的草稿用户不满意** → 不要硬塞进文档，回到 elicitor 重新追问。
- **sync-feature-list 失败** → 告知用户、不要让 product.md 和 feature-list.json 脱钩。建议用户检查或回滚 product.md 的本次修改（git）。
- **写入文件冲突**（如已有同名模块文件） → 停下问用户：是合并、覆盖、还是用新序号。

---

## 永远记住

**产品文档先行 → 同步特性列表 → 最后实现代码**

这是本项目开发铁律。本 skill 是这条铁律的守门人。