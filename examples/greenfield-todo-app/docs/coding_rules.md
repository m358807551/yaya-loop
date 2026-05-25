# AI 辅助开发 · 代码最佳实践（TodoMate 项目）

> 本项目使用 methodology-kit 初始化。第 1 层与第 2 层从 kit template 直接复制；第 3 层 / 第 4 层引用 web-frontend + typescript 的 stub。
>
> 第 1+2 层内容详见 kit 的 `methodology/templates/coding_rules.md.tmpl`（首次拷贝时已粘贴到此处，下方略去重复，仅保留引擎/语言层引用）。

---

# 第一部分 · 协作契约

（完整文本见 kit template，本示例文件为简化版仅展示结构）

## 1.2 工作流约束

- 实现 feature 时必须通过 `execute-next-feature` skill / prompt 走完整流程，不允许跳过预检查或人工验证阶段直接写代码。
- AI 不能自行将 feature 标记为 done，必须经人工验证后由人类口头/文字确认。
- 占位资源必须以 `_placeholder_` 为前缀命名（如有），并在 feature 的 notes 中登记。

**执行 execute-next-feature 时，阶段 0 出关报告（含规则原文 + 行号引用）和阶段 6 代码气味扫描是流程硬约束，不是可选步骤。最终 commit message 必须包含 `Code smell scan: pass` 行，否则会被 git commit-msg hook 阻断。**

---

# 第二部分 · 通用设计模式与架构原则

（完整文本见 kit template，本示例略）

要点：
- 首选命令模式（凡是"做一件事"封装成命令类）
- 数据与表现分离（数据层不感知 UI）
- 状态用状态机管理
- 反模式：God Object、UI 回调写业务、裸单例、状态散落、预先抽象、魔法数字

---

# 第三部分 · 引擎 / 平台最佳实践

## 3.1 当前平台

web-frontend（Vite + React 18 + TypeScript）

请遵循: @docs/coding-rules/engine-rules.md

---

# 第四部分 · 编程语言最佳实践

## 4.1 当前语言

TypeScript 5.x

请遵循: @docs/coding-rules/language-rules.md
