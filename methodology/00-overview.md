# 00 · 方法论总览

> 看完本文，你（人或 AI）就掌握了整套方法论的心智模型。其余 `methodology/` 下的文件都是对这里某一块的细化。

## 心智模型：三种文档 + 三类 skill

```
┌────────────────────────────────────────────────────────────────┐
│                       三种文档（在 docs/ 下）                       │
├────────────────────────────────────────────────────────────────┤
│ product.md + product/*.md  ← 要做什么（What）                       │
│ feature-list.json          ← 拆成的工作清单（轻量，每会话加载）       │
│ + features/F0XX.json       ← 每个 feature 的详情（按需 cat）         │
│ + feature-list-revisions.json ← 修订日志                            │
│ coding_rules.md            ← 怎么做的硬约束（How，四层结构）          │
└────────────────────────────────────────────────────────────────┘
                            ▲
                            │ 由下面三类 skill 操作
                            ▼
┌────────────────────────────────────────────────────────────────┐
│                       三类 skill                                  │
├────────────────────────────────────────────────────────────────┤
│ 产品类（操作 product.md）：                                          │
│   product-init-elicitor       从零启动新项目                        │
│   product-change-standardizer 任何产品变更的统一入口                  │
│   product-spec-elicitor       对一个变更追问关键模糊点                 │
│   product-ui-sketcher         产出 ASCII UI 草图                    │
│   product-audio-sketcher      产出音效条目（含占位文件名）              │
│                                                                  │
│ 生成类（操作 feature-list.json + features/）：                       │
│   generate-feature-list       从零一次性拆解 product → feature       │
│   sync-feature-list           product 变更后增量同步 feature-list      │
│                                                                  │
│ 执行类（操作源代码 + 更新 feature-list 状态）：                          │
│   execute-next-feature        按 8 阶段流程实现一个 feature           │
│   pick-refactor-smell         从 feature notes 里挑一个坏味道重构      │
└────────────────────────────────────────────────────────────────┘
```

## 为什么这样切分

| 切分 | 解决的痛点 |
|------|----------|
| **产品 vs 任务 vs 规则三层文档** | 不混淆 What（产品想做什么）/ How（编码怎么做）/ Todo（拆好的任务）——任何时候都能定位"我现在改的是哪一层" |
| **feature-list 轻量索引 + 详情懒加载** | 95 个 feature 也能塞进任何 AI 的上下文窗口，详情按需读取 |
| **产品变更 = 走 standardizer 入口** | 用户随口说的"想加 X"会被 AI 走标准化流程：判断改哪个模块文件、追问关键点、画 UI 草图、写音效条目、回写 product.md、增量更新 feature-list。不是随口改 |
| **执行 feature = 走 8 阶段流程** | 防止 AI 跳过验证就标 done；防止 AI 把"自己觉得对"当成"完成" |
| **代码气味扫描 = 子 agent 委派 + commit message 准入证据** | 主 agent 走完 7 阶段后上下文已被压缩，子 agent fresh context 能精确扫描；最终 commit 必须含当前 feature 专属、`must_fix: 0` 的完整扫描证据，hook 兜底，硬阻断遗漏 |

## 一个 feature 的完整生命周期

```
用户口头需求
   │
   ▼
[product-change-standardizer]──→ [product-spec-elicitor] (追问关键点)
   │                              │
   │                              ├─→ [product-ui-sketcher] (画草图)
   │                              └─→ [product-audio-sketcher] (写音效)
   ▼
更新 docs/product.md + docs/product/NN-*.md
   │
   ▼
[sync-feature-list]──→ 增量更新 feature-list.json + features/F0XX.json
   │
   ▼
[execute-next-feature]
   ├─ 阶段 0: 选 feature + 出关报告（必须引规则原文行号）
   ├─ 阶段 1: 资源预检查（占位资源登记）
   ├─ 阶段 2: 标记 in_progress + 更新 progress.md
   ├─ 阶段 3: 实现 + 细粒度 commit
   ├─ 阶段 4: 静态检查（项目级 static_check_cmd）
   ├─ 阶段 5: 人工验证（用户确认通过）
   ├─ 阶段 6: 代码气味扫描（子 agent，硬约束，输出 "Code smell scan: pass"）
   ├─ 阶段 7: 标记 done（commit 必须含 pass 证据）
   └─ 阶段 8: 交班（不自动做下一个）
```

## 三大硬约束（kit 全局不可绕过）

1. **产品变更走 standardizer，不直接改 product.md**：保证模块归位、增量同步可追溯。
2. **AI 不能自行标 done**：阶段 5 必须有用户文字/口头确认；阶段 7 commit message 必须含当前 feature 专属、`must_fix: 0` 的完整 `Code smell scan: pass` 证据行，hook 阻断。
3. **AI 不操作 main 分支、不 force push、不 reset --hard**：所有 commit 在工作分支，破坏性操作必须用户显式授权。

## 进一步阅读

| 想了解 | 看 |
|--------|----|
| product.md 和 product/*.md 长什么样 | [01-product-doc-structure.md](./01-product-doc-structure.md) |
| feature-list.json / F0XX.json / revisions.json 的 schema | [02-feature-list-schema.md](./02-feature-list-schema.md) |
| execute-next-feature 的 8 阶段细节 | [03-execute-loop.md](./03-execute-loop.md) |
| coding_rules.md 的 4 层结构怎么装 | [04-coding-rules-4-layers.md](./04-coding-rules-4-layers.md) |
| 想直接用 | 回到 [../README.md](../README.md) 或 [../BOOTSTRAP.md](../BOOTSTRAP.md) |
