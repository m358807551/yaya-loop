# 为 Yaya Loop 做贡献

感谢你愿意改进这套工作流。当前项目以中文文档为主，欢迎修正文案、补充技术栈规则、改进 Skill/Prompt，或修复 Hook。

## 开始之前

1. 先开 issue 描述较大的流程或 schema 变更；错别字和小修复可以直接提交 PR。
2. 从 `main` 创建短期分支，不要在一个 PR 中混入无关改动。
3. Claude Code Skill 与对应的 AI-agnostic Prompt 行为应保持一致；修改一侧时检查另一侧。
4. 新增 coding rules 时，请区分经过实践验证的规则和待补全的 stub，不要把个人偏好写成通用硬约束。

## 本地检查

项目只依赖 Python 标准库。提交前运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
git diff --check
```

测试覆盖 Hook 门禁、JSON/模板语法，以及示例 feature 索引的一致性。

## Commit 与 PR

- Commit message 使用简洁的 Conventional Commits 风格，例如 `fix: ...`、`docs: ...`、`feat: ...`。
- PR 说明应包含问题、改动方式和验证结果。
- 如果改变用户可见的工作流、schema 或升级方式，请同步更新 `README.md`、`BOOTSTRAP.md`、`methodology/` 和 `upgrade-notes.md` 中相关内容。

提交贡献即表示你有权提供这些内容，并同意按仓库的 [MIT License](./LICENSE) 发布。
