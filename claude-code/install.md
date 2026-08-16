# Claude Code 安装说明

> 本目录的内容是 Claude Code 用户的"开箱即用"包。把它装进目标项目的 `.claude/` 目录后，重启 Claude Code 即可识别全部 9 个 skill + 2 个 hook。
>
> 如果你不是 Claude Code 用户（Codex / Aider / Cursor 等），请改用 `../ai-agnostic-prompts/` + `../git-hooks/`。

## 一键安装（在目标项目根目录跑）

```bash
# 假定 Yaya Loop 在 ~/code/yaya-loop/
mkdir -p .claude/skills .claude/hooks

# 1) 拷 9 个 skill
cp -r ~/code/yaya-loop/claude-code/skills/* .claude/skills/

# 2) 拷 2 个 hook
cp ~/code/yaya-loop/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py

# 3) 合并 settings.json
#    - 若 .claude/settings.json 不存在：
cp ~/code/yaya-loop/claude-code/settings.example.json .claude/settings.json

#    - 若已存在：手动把 settings.example.json 的 hooks 段并入你的 .claude/settings.json
```

## 文件清单

```
claude-code/
├── skills/
│   ├── execute-next-feature/SKILL.md      # 实现一个 feature（8 阶段）
│   ├── generate-feature-list/SKILL.md     # 从零生成 feature-list
│   ├── sync-feature-list/SKILL.md         # product 变更后增量同步
│   ├── pick-refactor-smell/SKILL.md       # 从 notes 挑坏味道重构
│   ├── product-init-elicitor/SKILL.md     # 新项目首问
│   ├── product-change-standardizer/SKILL.md  # 产品变更统一入口
│   ├── product-spec-elicitor/SKILL.md     # 追问关键点
│   ├── product-ui-sketcher/SKILL.md       # ASCII UI 草图
│   └── product-audio-sketcher/SKILL.md    # 音效条目
├── hooks/
│   ├── gate-feature-done.py               # PreToolUse：阻断未通过气味扫描的 feature 标 done
│   └── check-feature-list.py              # PostToolUse：feature-list 结构自检（备用）
├── settings.example.json                  # hook 注册示例
└── install.md                             # 你正在读
```

## 安装后验证

```bash
# 1) 看 skill 是否被 Claude Code 识别（重启 Claude Code 后）
#    可以在 Claude Code 中输入 / 看是否出现这 9 个 skill 的选项

# 2) 测试 hook
#    随便修改 docs/feature-list.json 把某个 feature 改成 done（不通过气味扫描），
#    保存时 hook 应阻断并提示 "Code smell scan: pass" 缺失

# 3) 跑 execute-next-feature
#    对 AI 说"做下一个 feature"——它应该按 8 阶段流程走，阶段 0 出关报告会引用
#    docs/coding_rules.md 的行号
```

## 与方法论文档的关系

- 这里的 9 个 `SKILL.md` 是 [methodology/03-execute-loop.md](../methodology/03-execute-loop.md) 等概念文档的**可执行版**——每个文件都有 YAML frontmatter，Claude Code 自动识别触发短语，按 prompt 走流程。
- 修改 skill 行为：直接编辑 `.claude/skills/<name>/SKILL.md`。
- 修改 hook 行为：编辑 `.claude/hooks/<name>.py`。

## 升级

新版本 kit 发布时：

```bash
# 备份当前 skill 与 hook（如有自定义改动）
cp -r .claude .claude.backup-$(date +%Y%m%d)

# 重新拷贝
cp -r ~/code/yaya-loop/claude-code/skills/* .claude/skills/
cp ~/code/yaya-loop/claude-code/hooks/*.py .claude/hooks/
```

详细升级流程见 [../upgrade-notes.md](../upgrade-notes.md)。

## 故障排查

- **hook 没触发**：确认 `.claude/settings.json` 含 `hooks` 配置；hook 文件可执行（`ls -l .claude/hooks/`）。
- **skill 没出现在 `/` 列表**：重启 Claude Code；确认 `.claude/skills/<name>/SKILL.md` 存在且首行 YAML 完整。
- **阶段 0 出关报告引用规则失败**：检查 `docs/coding_rules.md` 是否存在；BOOTSTRAP STEP 3 是否完成。
