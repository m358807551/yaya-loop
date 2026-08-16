# BOOTSTRAP · 给 AI 的初始化指令

> **AI 读者注意**：本文件是你的执行脚本。从 STEP 0 开始按顺序执行，每一步完成后再进入下一步。**遇到歧义就停下来问用户，不要靠猜测继续。** 6 步全部完成后，目标项目就装好这套方法论了。
>
> **重要假设**：用户主语言是中文，你与用户的所有交互使用中文（除非用户主动切换语言）。
>
> Yaya Loop 的根目录位置由用户告诉你，可能是 `~/code/yaya-loop/` 或别的路径。下文用 `<KIT>` 代指。先问用户：「请告诉我这个 yaya-loop 文件夹的绝对路径，比如 `/Users/xxx/code/yaya-loop/`」。拿到后写死在本次会话里。

---

## STEP 0：项目状态探测

**目的**：判断当前项目是 already-bootstrapped / greenfield / legacy。

**做什么**：

1. 进入用户的目标项目根目录（用户已经在那里启动你了，通常你的 cwd 就是）。确认 cwd 正确：跟用户对一下「我现在在 `<pwd>`，是你要初始化方法论的项目吗？」

2. 跑下面三条 shell 命令（按顺序，单独跑，看结果）：
   ```bash
   ls docs/product.md docs/feature-list.json 2>/dev/null
   git log --oneline 2>/dev/null | wc -l
   find . -maxdepth 3 -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.gd" -o -name "*.cs" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.cpp" -o -name "*.h" \) ! -path "./node_modules/*" ! -path "./.git/*" 2>/dev/null | wc -l
   ```

3. 分类规则（不要问用户，按命令结果自己判断）：

   | 命令 1（docs 是否齐） | 命令 2（commit 数） | 命令 3（源码文件数） | 分类 |
   |---|---|---|---|
   | 两个文件都在 | 任意 | 任意 | **already-bootstrapped** |
   | 没有 | ≤ 3 | < 20 | **greenfield** |
   | 没有 | 其它任意 | 其它任意 | **legacy** |

4. 输出一行结论给用户：
   - already-bootstrapped → 「检测到项目已经装过本方法论，跳到 STEP 5 做版本检查与升级。」（参考 `<KIT>/upgrade-notes.md`，本流程在 STEP 5 完成后结束）
   - greenfield → 「检测到这是一个新项目（无产品文档、源码很少），将走 greenfield 流程。」
   - legacy → 「检测到这是一个已有代码的项目（X 个源文件、Y 个 commit），将走 legacy 反向工程流程。」

5. 等用户回「继续」或纠正分类（用户可能说「不对，这是个练习项目，按 greenfield 走」）。

---

## STEP 1：AI CLI 探测

**目的**：决定 STEP 4 装 Claude Code 那套还是 AI-agnostic 那套。

**做什么**：

1. 自检你自己是谁，按下面顺序：
   ```bash
   env | grep -E '^(CLAUDE_PROJECT_DIR|CLAUDE_CODE)' 2>/dev/null
   ls .aider.conf.yml .cursorrules .vscode/aider 2>/dev/null
   ```

2. 推断 CLI：
   - 有 `CLAUDE_PROJECT_DIR` → **Claude Code**
   - 有 `.aider.conf.yml` → Aider
   - 有 `.cursorrules` → Cursor
   - 都没有 → 直接问用户「你正在用哪个 AI CLI（Claude Code / Codex / Aider / Cursor / 其它）？」

3. 记录结论：`CLI = claude-code` 或 `CLI = other`（aider/cursor/codex 都归 other）。下文 STEP 4 用这个变量分支。

---

## STEP 2：按项目状态走不同分支

### STEP 2a · Greenfield 分支

**目的**：从零和用户一起把项目意图结构化进 `docs/product.md` 和 `docs/product/*.md`，然后拆出 feature-list。

**做什么**：

1. **问用户**：「这个项目你想做什么？一两句话描述就行。」（这是 product-init-elicitor 的入口）

2. 加载并按下面任一种方式启动 product-init-elicitor：
   - 如果 CLI = claude-code：直接告诉用户「我会触发 `/product-init-elicitor` skill，开始问你一些问题来把想法结构化」。然后调用该 skill。
   - 如果 CLI = other：读 `<KIT>/ai-agnostic-prompts/product-init-elicitor.prompt.md` 全文，按它的提示对用户做结构化访谈。

3. 访谈结束后会得到一个产品总览结构。把它落到磁盘：
   ```bash
   mkdir -p docs/product docs/features
   ```
   - 写 `docs/product.md`（用 `<KIT>/methodology/templates/product.md.tmpl` 做骨架，填入访谈得到的内容）
   - 写每个模块的 `docs/product/NN-name.md`（用 `<KIT>/methodology/templates/product-module.md.tmpl` 做骨架）
   - 写空的 `docs/feature-list-revisions.json`：`{"revision_log": []}`

4. **逐模块 spec 细化**（可选但推荐）：对每个新建的模块文件，问用户「要不要现在把它细化到能拆 feature 的程度？」如果是，按 CLI 类型启动 product-spec-elicitor，把每个模块文件填充完。

5. **记录待拆解范围**：汇总已经确认的产品模块与细化结果。本阶段不生成 feature-list；必须等 STEP 3 创建 `docs/coding_rules.md` 后，再按技术约束拆解。

6. 完成后告知用户「greenfield 分支结束，进入 STEP 3 选技术栈」。

### STEP 2b · Legacy 分支

**目的**：把一个已经有几千上万行代码、没有产品文档的项目，反向工程出 `docs/product.md` 雏形和 feature-list（已实现的标 done，未来想做的标 pending）。

**做什么**：

1. **代码考古**（你自己读，不要让用户做）：
   ```bash
   ls
   cat README.md CHANGELOG.md 2>/dev/null | head -200
   git log --oneline | head -100
   find . -maxdepth 2 -type d ! -path "./node_modules*" ! -path "./.git*" ! -path "./venv*" ! -path "./target*"
   # 找最大的 5 个源文件，挨个读 100 行
   find . -maxdepth 4 -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.gd" -o -name "*.cs" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) ! -path "./node_modules/*" ! -path "./.git/*" ! -path "./venv/*" -exec wc -l {} \; 2>/dev/null | sort -rn | head -5
   ```

2. **产出"一页假设"**：基于上面材料，写一段 200 字左右的「这个项目我猜是干 X 的，主要由 Y / Z / W 几个模块组成，技术栈看着像 A+B」，呈给用户。**不要假装确定，所有判断都加「看起来 / 推测 / 可能」**。

3. **5-10 个 yes/no 问题给用户对齐**：把可能误判的地方挑出来问。例子：
   - 「`scripts/payment/` 看起来是支付流程，对吗？」
   - 「`legacy_v1/` 这个目录是已经废弃的旧版吗？」
   - 「你目前最痛的、想优先优化的部分是什么？」

4. **基于确认后的假设草拟 product.md**：用 `<KIT>/methodology/templates/product.md.tmpl` 骨架，每个反向工程出来的章节标 `[REVERSE-ENGINEERED]` 后缀，方便日后渐进精确化。

5. **按目录拆模块**：每个顶层源码目录（或核心子系统）建一个 `docs/product/NN-name.md`，同样标 `[REVERSE-ENGINEERED]`。先把现状写下来（不写未来计划），未来再用 product-change-standardizer 增量演化。

6. **准备追溯 feature-list 的素材（两阶段）**：
   - **Phase A · 追溯已完成**：把现有主要能力，按"用户能做到 X"的颗粒度整理成 **不超过 15 个** feature 候选。**不超过 15 的硬上限**：避免把 30k LOC 拆成 200 个无意义的小条目淹没用户。15 是上限不是下限，10 个就够也行。
   - **Phase B · 前瞻待办**：问用户「现在最想加什么功能 / 修什么 bug？列 3-5 个」，记录为 `pending` feature 候选。这是用户真正会推进的入口。
   - 此处只确认候选清单，不写 feature-list；实际文件在 STEP 3 创建 coding rules 后统一生成。

7. **记录代码气味入口**：如果用户希望首轮就有重构 backlog，记下该选择；等 STEP 3 生成 feature 文件后再执行扫描并写入对应 `notes`。

8. 完成后告知用户「legacy 分支结束，进入 STEP 3 选技术栈」。

---

## STEP 3：技术栈识别 + 选/写 coding-rules

**目的**：把 `docs/coding_rules.md` 装好。它有 4 层（协作契约 + 通用模式 + 引擎 + 语言），前两层 kit 已经写好，后两层要按项目技术栈装。

**做什么**：

1. **先识别再问**：
   ```bash
   ls package.json Cargo.toml pyproject.toml requirements.txt project.godot go.mod pom.xml build.gradle *.csproj 2>/dev/null
   cat package.json 2>/dev/null | head -30
   cat pyproject.toml 2>/dev/null | head -30
   ```

2. 把推测告诉用户，让其确认：「看起来引擎是 `<X>`、语言是 `<Y>`，对吗？」

3. **拼装 coding_rules.md**：
   ```bash
   mkdir -p docs/coding-rules
   cp <KIT>/methodology/templates/coding_rules.md.tmpl docs/coding_rules.md
   ```
   然后把 `{{ENGINE_NAME}}` 和 `{{LANGUAGE_NAME}}` 替换成用户确认的值。

4. **选/写引擎规则**：
   - 在 `<KIT>/coding-rules-library/engines/` 找对应文件
     - 找到了 → `cp <KIT>/coding-rules-library/engines/<engine>.md docs/coding-rules/engine-rules.md`
     - 如果拷的是 stub（文件里有「Stub 版本：未填充」标记）→ 问用户「我拷了 stub。要现在花 15 分钟一起填，还是先留 TODO 后续慢慢补？」选填则你按 stub 的章节挨个问关键问题，把答案写入。
     - 找不到 → `cp <KIT>/coding-rules-library/engines/_stub-template.md docs/coding-rules/engine-rules.md`，把 `{{NAME}}` 改成实际引擎名，引导用户填关键章节。
   - 对 `languages/` 做同样的事，生成 `docs/coding-rules/language-rules.md`。

5. **记录静态检查命令**：
   问用户：「我之后实现 feature 时，要跑哪个命令做静态检查？例如 `npm run typecheck` / `cargo check` / `mypy .` / `tsc --noEmit`。这个命令必须能快速反馈类型/语法错误，且能在 30 秒内完成。」
   把答案写入：
   ```bash
   mkdir -p docs
   cat > docs/methodology-config.json <<EOF
   {
     "static_check_cmd": "<用户答案>",
     "engine": "<X>",
     "language": "<Y>",
     "kit_version": "<KIT>/kit-version.txt 的内容",
     "bootstrap_at": "<ISO 时间戳>",
     "bootstrap_mode": "greenfield | legacy"
   }
   EOF
   ```
   验证：`python3 -m json.tool docs/methodology-config.json > /dev/null`

6. **生成 feature-list（必须在 coding rules 之后）**：
   - **greenfield**：按 CLI 类型启动 generate-feature-list，让它读取 `docs/product.md`、`docs/product/*.md` 与刚创建的 `docs/coding_rules.md`，输出 `docs/feature-list.json`、`docs/features/F0XX.json` 和 `docs/feature-list-revisions.json`。
   - **legacy**：基于 STEP 2b 已确认的候选清单生成同样三类文件。已实现能力全部标为 `done`，`completed_at` 填当前 ISO 时间戳，`notes` 写 `Implemented before bootstrap; reverse-engineered from code at commit <git rev-parse HEAD>`；前瞻待办标为 `pending`。
   - 生成后立即按 `methodology/02-feature-list-schema.md` 做 JSON、id ↔ 文件名、`meta.total_features` 和依赖方向自检。

7. **legacy 可选代码气味扫描**：如果用户在 STEP 2b 选择了首轮扫描，现在调用 pick-refactor-smell，把发现的 must_fix / suggest 写入对应追溯 feature 的 `notes`。

---

## STEP 4：安装 skill / prompt / hook

**目的**：让用户的 AI CLI 在这个项目里能识别并运行这套 skill。

### 如果 CLI = claude-code

```bash
mkdir -p .claude/skills .claude/hooks
cp -r <KIT>/claude-code/skills/* .claude/skills/
cp <KIT>/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py
```

**合并 settings.json**：
- 若 `.claude/settings.json` 不存在 → `cp <KIT>/claude-code/settings.example.json .claude/settings.json`
- 若存在 → 打开两个文件，把 `<KIT>/claude-code/settings.example.json` 里的 `hooks` 段并入；如有冲突让用户裁决。

提示用户：「Claude Code 安装完成。重启 Claude Code 让它发现新 skill，然后说『做下一个 feature』就能开始。」

### 如果 CLI = other

```bash
mkdir -p docs/methodology-prompts .git/hooks
cp <KIT>/ai-agnostic-prompts/*.md docs/methodology-prompts/
cp <KIT>/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

提示用户：「非 Claude Code CLI 安装完成。打开 `docs/methodology-prompts/00-how-to-use.md` 看『触发短语 → 用哪个 prompt 文件』速查表。**注意**：你的 CLI 没有 PreToolUse hook 能力，质量门由 `.git/hooks/commit-msg` 兜底——commit 时会校验 feature-list 的 done 状态，以及 commit message 是否包含该 feature 专属、`must_fix: 0` 的完整扫描证据行。」

---

## STEP 5：烟囱测试 + 验证

**目的**：跑一遍，确认装好的东西真的能用。

**做什么**：

1. **结构自检**（你跑，把输出给用户看）：
   ```bash
   ls docs/product.md docs/feature-list.json docs/feature-list-revisions.json docs/coding_rules.md docs/methodology-config.json
   ls docs/product/ docs/features/
   ls docs/coding-rules/
   # Claude Code 用户额外
   ls .claude/skills/ .claude/hooks/ 2>/dev/null
   # 非 Claude 用户额外
   ls docs/methodology-prompts/ .git/hooks/commit-msg 2>/dev/null
   ```
   每一行都应有输出。任何 missing 报告给用户，回到对应 STEP 修。

2. **JSON 合法性**：
   ```bash
   python3 -m json.tool docs/feature-list.json > /dev/null && echo "main index OK"
   python3 -m json.tool docs/feature-list-revisions.json > /dev/null && echo "revisions OK"
   python3 -m json.tool docs/methodology-config.json > /dev/null && echo "config OK"
   for f in docs/features/*.json; do python3 -m json.tool "$f" > /dev/null || echo "BAD: $f"; done
   ```

3. **id ↔ 文件名交叉检查**：
   ```bash
   python3 -c "
   import json, os, sys
   idx = json.load(open('docs/feature-list.json'))
   index_ids = {f['id'] for f in idx['features']}
   file_ids = {os.path.splitext(f)[0] for f in os.listdir('docs/features') if f.endswith('.json')}
   if index_ids != file_ids:
       print('MISMATCH')
       print('only in index:', index_ids - file_ids)
       print('only in files:', file_ids - index_ids)
       sys.exit(1)
   print('id consistency OK:', len(index_ids), 'features')
   "
   ```

4. **规则链通畅检查**：让用户随便挑一个 pending feature（或 legacy 模式下挑一个 done feature 做演练），按 CLI 类型启动 execute-next-feature，跑到「阶段 0 出关报告」就主动停（不要真的进入实现），看输出里是否引用了 `docs/coding-rules/engine-rules.md` 或 `docs/coding-rules/language-rules.md` 的行号。引用得出来 = 规则链通了。

5. **打印首条可用命令**：
   - Claude Code 用户：「现在你可以说『做下一个 feature』或显式触发 `/execute-next-feature` skill。」
   - 其他 CLI：「现在你可以让 AI 读 `docs/methodology-prompts/execute-next-feature.prompt.md` 并触发它。」

---

## STEP 6：交付总结

**做什么**：

向用户输出一段总结，包括：
1. 本次 bootstrap 走的是 greenfield 还是 legacy 分支。
2. 产生了哪些文件（按上面的 ls 结果列出）。
3. 当前 pending 的第一个可启动 feature 是什么。
4. 用户下一步该做什么（一句话指引）。
5. 友情提示：bootstrap 完成后，**本 BOOTSTRAP.md 文件不需要被检入用户项目**——它只是装配脚本，方法论的常驻参考是 `<KIT>/methodology/00-overview.md`。

然后停下，把控制权交回用户。**不要自动开始第一个 feature。**

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 用户的项目结构很特殊（monorepo、多语言混合）→ STEP 0/3 难判断 | 停下，让用户告诉你按哪个子目录走 |
| `<KIT>` 路径找不到 / 文件缺失 | 让用户检查 kit 是否完整解压 |
| STEP 4 装 hook 时 `.git/hooks/commit-msg` 已存在 | 不要覆盖，提示用户手工合并或备份 |
| STEP 5 烟囱测试任何一步失败 | 报告失败点，让用户决定继续还是回退 |
| 用户在中途打断说「先不做了」 | 完成当前已经开始写的 STEP，然后停。下次可从该 STEP 继续 |

---

## STEP 速查

```
STEP 0：探测项目状态（already-bootstrapped / greenfield / legacy）
STEP 1：探测 AI CLI（claude-code / other）
STEP 2：按项目状态分支
   2a greenfield → product-init → spec → generate-feature-list
   2b legacy → 代码考古 → 反推 product.md → 追溯 feature-list（Phase A done + Phase B pending）
STEP 3：识别技术栈 → 拼 docs/coding_rules.md + 装 engine/language 规则
STEP 4：按 CLI 类型装 skill/prompt/hook
STEP 5：烟囱测试 + 验证
STEP 6：交付总结，把控制权交回用户
```
