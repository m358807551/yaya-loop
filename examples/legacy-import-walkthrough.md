# Legacy 项目接入 methodology-kit · 叙事走查

> 这是一个**虚构但合理**的走查，演示 BOOTSTRAP.md 的 STEP 2b（legacy 分支）在一个已经开发了一年多的 Django Web 项目上是怎么跑的。读完你会知道：
>
> 1. 你的旧项目接入这套方法论大概会经历什么
> 2. 反向工程产出的 product.md 长什么样
> 3. 追溯 feature-list 怎么避免淹没在历史细节里
>
> 实际操作时 AI 的具体提问会因项目而异，下面是典型样子。

---

## 项目假想背景

- 名字：`OrderForge`
- 用了什么：Django 4 + PostgreSQL + Celery + Redis；前端模板渲染 + 少量 HTMX；2 万行 Python；开发 14 个月，4 个开发者。
- 业务：B2B 订单管理系统，处理客户下单、库存扣减、物流对接、发票生成。
- 现状：没有 product.md，README 只有「how to setup」；TODO 散落在 Linear 和注释里；新来的人需要 1 周才能看明白模块边界。
- 用户痛点：「想加个新功能就得跟 4 个开发对接信息，每次都漏」「重构没人敢动，怕断了上下游」。

---

## STEP 0 · 项目探测

AI 跑：
```
$ ls docs/product.md docs/feature-list.json 2>/dev/null
（无输出）

$ git log --oneline | wc -l
1247

$ find . -maxdepth 3 -type f \( -name "*.py" ... \) | wc -l
312
```

AI 输出：「检测到这是一个已有代码的项目（312 个源文件、1247 个 commit），将走 legacy 反向工程流程。」

---

## STEP 1 · CLI 探测

用户在 Codex 里跑 BOOTSTRAP，AI 询问后确认 `CLI = other`，记录待用。

---

## STEP 2b · Legacy 反向工程

### 1. 代码考古（AI 自己跑，~5 分钟）

```
$ cat README.md | head -80
# 输出展示了 setup、docker-compose、env 变量配置，没有业务描述

$ cat CHANGELOG.md | head -50
（不存在）

$ git log --oneline | head -100
# AI 看到 commit message 主要分布在：
#  - "feat: add invoice PDF export"
#  - "fix: stock deduction race condition"
#  - "feat: webhook for SF Express"
#  - "refactor: split order_service.py"

$ find . -maxdepth 2 -type d
# 输出：apps/orders apps/inventory apps/customers apps/shipping
#       apps/invoicing apps/reporting api/v1 api/v2 tasks utils
#       templates static config docker tests

$ # 找最大的 5 个源文件
$ find . -maxdepth 4 -type f -name "*.py" -exec wc -l {} \; | sort -rn | head -5
# 输出：
# 1832  apps/orders/services/order_service.py
# 1421  apps/inventory/services/stock_service.py
# 1108  apps/shipping/services/shipping_service.py
# 892   apps/invoicing/services/invoice_generator.py
# 654   apps/customers/services/customer_service.py
```

### 2. 一页假设（AI 写给用户看）

AI 输出：

> **一页假设**：这看起来是一个**B2B 订单管理系统**，主要由 6 个 Django app 组成：
>
> - `orders` — 订单创建与状态机（看起来是核心，service 文件最大）
> - `inventory` — 库存管理与扣减（有 race condition 修复痕迹）
> - `customers` — 客户主数据
> - `shipping` — 物流对接（看到有 SF Express webhook）
> - `invoicing` — 发票生成（看到 PDF export）
> - `reporting` — 数据统计与导出
>
> **API 层有 v1 和 v2 两套**，推测在做版本迁移。
>
> **技术栈推测**：Django 4 + PostgreSQL + Celery（看 `tasks/` 目录）+ Redis（猜测）。前端有 `templates/` 目录，传统 Django 渲染为主。
>
> 几个我不确定的点，请帮忙确认（10 个 yes/no）：
>
> 1. `apps/orders/` 是核心业务，对吗？
> 2. `api/v1` 现在还在用，还是已经废弃只留 v2？
> 3. 看到 `apps/reporting/` 但代码量小，是已经开发的，还是只搭了骨架？
> 4. `tasks/` 目录的 Celery 任务主要服务哪个 app？
> 5. 你目前最痛、最想优先优化的是哪个部分？
> 6. 有没有正在做但还没合并的大功能？
> 7. 有任何「这部分能跑但没人敢动」的代码区域吗？
> 8. 你想让这套方法论先覆盖全部 6 个 app，还是先聚焦核心（orders + inventory）？
> 9. 我看到 `apps/legacy/` 目录但内容很少，是历史遗留待清理的吗？
> 10. 你期待 product.md 写到什么粒度——核心循环 + 主要 use case 就行，还是每个 API 端点都要写？

### 3. 用户回答后

（用户花 10 分钟回答，明确：orders 是核心、v1 已废弃但代码留着、reporting 只是骨架、最痛点是 inventory 的扣减并发问题、想先聚焦核心 4 个 app 不写 reporting/legacy。）

AI 把这些回答整理后，开始草拟。

### 4. 草拟 product.md

AI 用 kit 模板，产出 `docs/product.md`，每段标 `[REVERSE-ENGINEERED]`：

```markdown
# OrderForge · 反向工程版

> 当前版本：**V1.0 · 已上线运行 14 个月** [REVERSE-ENGINEERED]

## 一句话定位

B2B 订单管理系统，覆盖客户从下单到发货收发票的完整链路。[REVERSE-ENGINEERED]

## 用户画像

- **主要用户**：B2B 销售运营 + 客户采购员 [REVERSE-ENGINEERED]
- **使用场景**：每天高频登录，单次 5-30 分钟 [REVERSE-ENGINEERED]

## 核心循环（V1.0 现状）[REVERSE-ENGINEERED]

```
1. 销售或客户创建订单（apps/orders）
2. 系统校验库存并扣减（apps/inventory）
3. 订单流转到物流分配（apps/shipping，对接 SF Express）
4. 发货完成后生成发票（apps/invoicing PDF export）
5. 状态变更触发 Celery 异步通知任务（tasks/）
```

## 模块清单

| 序号 | 文件 | 模块名 | 状态 |
|------|------|--------|------|
| 01 | [01-orders.md](./product/01-orders.md) | 订单核心 | reverse-engineered |
| 02 | [02-inventory.md](./product/02-inventory.md) | 库存 | reverse-engineered |
| 03 | [03-customers.md](./product/03-customers.md) | 客户主数据 | reverse-engineered |
| 04 | [04-shipping.md](./product/04-shipping.md) | 物流对接 | reverse-engineered |
| 05 | [05-invoicing.md](./product/05-invoicing.md) | 发票 | reverse-engineered |

## 模块依赖关系

```
03-customers ──→ 01-orders ──→ 02-inventory
                     │
                     ├──→ 04-shipping
                     └──→ 05-invoicing
```

## 变更历史

- 2026-05-25：通过 methodology-kit BOOTSTRAP legacy 流程反向工程产出。锚点 commit `<git rev-parse HEAD>`。
```

### 5. 每个模块文件（5 个），同样 [REVERSE-ENGINEERED]

AI 对每个 app 读一遍 service 与 model，写出对应的 `docs/product/0N-*.md`，每个文件包含：
- 现有功能流程（从代码反推）
- 数据模型（从 Django models 抽出）
- 验收标准（推断已经在运行的行为）

不写「未来可能」「TODO」。这些留给后续用 product-change-standardizer 增量演化。

### 6. 追溯 feature-list（两阶段）

**Phase A · 追溯已完成**（硬上限 15）：

AI 与用户对齐后，写出 15 个 done feature：

| id | title | source | notes |
|----|-------|--------|-------|
| F001 | Django 项目骨架 + PostgreSQL 接入 | infrastructure | Implemented at commit abc1234. Reverse-engineered. |
| F002 | 客户主数据 CRUD（apps/customers） | product/03-customers.md | 同上 |
| F003 | 订单创建与基础状态机 | product/01-orders.md | 同上 |
| F004 | 订单状态机扩展：付款 → 发货 → 完成 | product/01-orders.md | 同上 |
| F005 | 库存模型与简单扣减 | product/02-inventory.md | 同上 |
| F006 | 库存扣减并发安全（select_for_update） | product/02-inventory.md | 同上 |
| F007 | 物流对接：SF Express webhook | product/04-shipping.md | 同上 |
| F008 | 物流：发货单生成 | product/04-shipping.md | 同上 |
| F009 | 发票 PDF 生成 | product/05-invoicing.md | 同上 |
| F010 | 发票邮件发送（Celery） | product/05-invoicing.md | 同上 |
| F011 | API v1 全部端点 | infrastructure | 已废弃，保留代码兼容老客户端 |
| F012 | API v2 重设计（替代 v1） | infrastructure | 同上 |
| F013 | 客户登录与权限（Django auth） | product/03-customers.md | 同上 |
| F014 | 销售后台管理界面（Django admin 定制） | infrastructure | 同上 |
| F015 | 基础监控与日志（structlog + Sentry） | infrastructure | 同上 |

**Phase B · 前瞻待办**（用户提的 3-5 个）：

| id | title | source | status |
|----|-------|--------|--------|
| F016 | 库存扣减改用 Redis 分布式锁，替代 select_for_update | product/02-inventory.md | pending |
| F017 | 订单导出 Excel（reporting 模块第一步） | product/01-orders.md | pending |
| F018 | SF Express webhook 失败重试机制 | product/04-shipping.md | pending |

### 7. 可选：调 pick-refactor-smell

AI 跑 `pick-refactor-smell.prompt.md`，扫描 5 个最大的 service 文件，输出：

```
🔴 高严重性（建议尽快处理）
- apps/orders/services/order_service.py 1832 行 — God Object 趋势明显
  → 建议拆分为：order_creation_service / order_state_machine / order_query_service

🟡 中等
- apps/inventory/services/stock_service.py 1421 行 — 同上风险，但目前还能管
- apps/shipping/services/shipping_service.py 含 4 处硬编码 SF Express endpoint
  → 建议提取到 config

🟢 低（可接受）
- 多处 datetime.now() 调用未注入时钟，但对当前业务影响小
```

AI 把高/中两项写入对应 feature 的 notes：

```json
// F003.json（订单创建）notes 追加
"notes": "Implemented at commit abc1234. Reverse-engineered.\nTODO must_fix: order_service.py 1832 行已是 God Object，下次改 orders 模块前必须先拆。"
```

---

## STEP 3-6（同 greenfield 流程）

技术栈识别为 Django/Python，AI 从 `coding-rules-library/languages/python.md` stub 拷出 `docs/coding-rules/language-rules.md`，引擎层用 `backend-service.md` stub。

`static_check_cmd` 记录为 `mypy . && ruff check .`。

安装 Codex 用的 `ai-agnostic-prompts/` + `git-hooks/commit-msg`。

烟囱测试通过。

---

## 用户接入后第一周做什么

1. **完善 reverse-engineered 模块文件**：每天接触一个 service 时，回头把对应 product/0N-*.md 的「[REVERSE-ENGINEERED]」段落改实，删除标记。这是渐进式而非一次性任务。
2. **从 F016 开始正式走流程**：`execute-next-feature` 拿 F016，按 8 阶段走一遍——这是接入 kit 的"第一次真实使用"，会发现哪些规则与现有代码风格冲突，及时记录到 coding_rules.md 的「偏离记录」。
3. **每周回看 pick-refactor-smell**：把 backlog 变成实际 refactor feature，按 priority 排进 feature-list。

---

## 接入后 30 天的预期收益

- 新人 onboarding 从 1 周 → 2 天（product.md + 模块文件直接覆盖了 80% 的认知建模）
- 加新功能不再"4 个开发对接"——通过 product-change-standardizer 走一遍即可识别影响模块
- 重构有了"代码气味 backlog"驱动，不再是「想到了再改」
- AI 助手的产出质量稳定，因为有了清晰的 acceptance_criteria

---

## 常见踩坑

1. **Phase A 拆太细**：30k LOC 想拆 50+ done feature → 没人会去维护 → 维护成本反而高于价值。**严守 15 个上限**。
2. **product.md 想一次写到完美**：reverse-engineered 标记的章节就是占位，让它带着标记上线，之后接触相关模块时再细化。
3. **追溯期间撞上紧急 bug**：暂停 BOOTSTRAP，先修 bug（按现有流程），bug 修完再继续 BOOTSTRAP（kit 不影响已有工作流）。
4. **认为接入后所有人都要遵守**：先 1-2 个核心开发用熟，再推广。强推会被反弹。
