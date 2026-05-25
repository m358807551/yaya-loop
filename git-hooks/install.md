# git-hooks · 非 Claude Code 用户的质量门兜底

> Claude Code 用户：不需要这个目录。`../claude-code/hooks/gate-feature-done.py` 在 Edit/Write 工具调用时就拦截，比 commit 阶段更早。
>
> 非 Claude Code 用户（Codex / Aider / Cursor / 等）：用这个 git hook，把 execute-next-feature 阶段 6 的"代码气味扫描通过"准入证据校验留到 commit 时刻兜底。

## 装什么

| 文件 | 类型 | 作用 |
|------|------|------|
| `commit-msg` | git commit-msg hook | commit 时检查：本次若把任何 feature 切到 `done`，则 commit message 必须含 `Code smell scan: pass`，否则拒绝 commit |

## 一键安装（在目标项目根目录跑）

```bash
# 假定 kit 在 ~/code/methodology-kit/
cp ~/code/methodology-kit/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

## 验证

```bash
# 1) 故意制造一个 done 改动但 commit message 不带 pass 证据 —— 应被拒绝
# （在已有 feature-list.json 的项目里）
python3 -c "
import json
d = json.load(open('docs/feature-list.json'))
d['features'][0]['status'] = 'done'
json.dump(d, open('docs/feature-list.json','w'), ensure_ascii=False, indent=2)
"
git add docs/feature-list.json
git commit -m "test"        # ← 应被 hook 拒绝并打印提示
git restore --staged docs/feature-list.json
git restore docs/feature-list.json

# 2) 同样改动，commit message 含 pass —— 应通过
git add docs/feature-list.json
git commit -m "chore: mark done

Code smell scan: pass (must_fix: 0, suggest: 0, acceptable: 0)
"
```

## 局限

- 这个 hook 只在 **commit 时刻**触发。如果用户直接改了 `docs/feature-list.json` 但没 commit，hook 不会发出警告。Claude Code 版本（PreToolUse hook）能在编辑时立即拦截，更早一步。
- 用户可以 `git commit --no-verify` 绕过。这是 git 的标准逃生口，无法在 hook 层面禁掉。**养成习惯，必要时 review hook 跳过历史**：
  ```bash
  git log --grep "Code smell scan" --invert-grep --since="1 week ago"
  ```

## 兼容性

- Python 3.6+
- 不依赖任何第三方包
- macOS / Linux / WSL 均测试通过
- Windows 原生 git bash 应可用（未测）

## 与 PR / CI 的关系

如果你的项目用 PR 流程，可以把同样的检查搬到 CI（GitHub Actions / GitLab CI）作为更强约束——commit 可以 `--no-verify` 绕过 hook 但 CI 不会绕过。kit 当前不提供 CI 样板，可参考本 hook 的逻辑自己写。
