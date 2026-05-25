# Upgrade Notes · 已接入项目如何拉取 kit 更新

> 本文件给"已经用 BOOTSTRAP 装过本 kit 的目标项目"使用——告诉你下次 kit 发新版时，目标项目里该改什么。
>
> Kit 自身使用语义化版本（`kit-version.txt`）：
> - **MAJOR**（破坏性改动）：需要手动迁移
> - **MINOR**（新增能力）：可选拷贝
> - **PATCH**（修补 / 文案优化）：直接覆盖

## 升级前的准备

1. 看你目标项目当前用的 kit 版本：
   ```bash
   cat docs/methodology-config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['kit_version'])"
   ```
2. 看 kit 最新版本：
   ```bash
   cat <KIT>/kit-version.txt
   ```
3. 看 changelog（本文件下方）确认是否需要手动迁移。

## 升级流程（通用模板）

```bash
# 0) 备份现有 skill 与 hook
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p .backup-kit
cp -r .claude .backup-kit/claude-$TS 2>/dev/null || true
cp -r docs/methodology-prompts .backup-kit/prompts-$TS 2>/dev/null || true
cp .git/hooks/commit-msg .backup-kit/commit-msg-$TS 2>/dev/null || true

# 1) Claude Code 用户
cp -r <KIT>/claude-code/skills/* .claude/skills/
cp <KIT>/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py

# 1') 非 Claude Code 用户
cp <KIT>/ai-agnostic-prompts/*.md docs/methodology-prompts/
cp <KIT>/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg

# 2) coding-rules 库（仅在 stub 升级或加新 stub 时需要——一般不动你已经填充的 engine-rules.md / language-rules.md）
#    若 kit 新增了你当前技术栈的实战版规则文件（如以前是 stub 现在变实战），询问用户是否要 diff 合并：
#    diff <KIT>/coding-rules-library/<engines|languages>/<stack>.md docs/coding-rules/{engine,language}-rules.md

# 3) 升级 methodology-config.json
python3 -c "
import json
c = json.load(open('docs/methodology-config.json'))
c['kit_version'] = open('<KIT>/kit-version.txt').read().strip()
c['upgraded_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
json.dump(c, open('docs/methodology-config.json','w'), ensure_ascii=False, indent=2)
"

# 4) 验证
python3 -m json.tool docs/feature-list.json > /dev/null
python3 -m json.tool docs/methodology-config.json > /dev/null
ls .claude/skills/ 2>/dev/null || ls docs/methodology-prompts/
```

## 不要做的事

- **不要直接拷贝 `templates/*.tmpl` 覆盖你的 docs/**：模板只在 BOOTSTRAP 第一次用，之后你的 `docs/product.md` 已经长成自己的样子。
- **不要把 `examples/` 拷进自己的项目**：它只是示例。
- **不要修改 `<KIT>` 目录本身然后用**：那是单向的"上游"。要改本地行为，改你目标项目里的副本。要改 kit 通用部分，正常的开源贡献流程（fork / PR）。

## changelog

### v0.1.0（首发）

- 三种文档 + 三类 skill 模型成型
- 9 个 SKILL.md（Claude Code 版） + 9 个 .prompt.md（AI agnostic 版）
- 2 个 hook：`gate-feature-done.py`（PreToolUse）+ `commit-msg`（git）
- 引擎规则库：godot（实战）+ unity/unreal/web-frontend/backend-service（stub）
- 语言规则库：gdscript（实战）+ csharp/typescript/python/rust（stub）
- BOOTSTRAP.md 支持 greenfield + legacy 双分支
- 示例：greenfield-todo-app（5 feature） + legacy-import-walkthrough（叙事）

未来版本若有破坏性 schema 变化，会在这里列出迁移脚本。
