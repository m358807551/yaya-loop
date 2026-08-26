# Yaya Loop upgrade notes

> This guide is for target projects that were initialized from an earlier Yaya Loop Kit. The Kit follows semantic versioning through `kit-version.txt`.

- **MAJOR:** breaking workflow or schema change that requires an explicit migration
- **MINOR:** backward-compatible capability that a maintainer deliberately adopts
- **PATCH:** compatible fixes and documentation improvements

An upgrade changes the installed workflow integration. It must not silently rewrite the target project's Product, Feature history, Progress, or project-specific Coding Rules.

## Before upgrading

1. Read the version recorded by the target project:

   ```bash
   python3 -c "import json; print(json.load(open('docs/methodology-config.json'))['kit_version'])"
   ```

2. Read the new Kit version:

   ```bash
   cat <KIT>/kit-version.txt
   ```

3. Read the release notes below and inspect local changes to installed Skills, Prompts, Hooks, and Coding Rules before overwriting anything.
4. Commit or otherwise preserve the target project's current work. Do not begin an upgrade with unresolved changes.

## Back up the installed integration

Use an explicit backup location inside the target project and review it before continuing:

```bash
UPGRADE_STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p .backup-kit
cp -r .claude ".backup-kit/claude-$UPGRADE_STAMP" 2>/dev/null || true
cp -r docs/methodology-prompts ".backup-kit/prompts-$UPGRADE_STAMP" 2>/dev/null || true
cp .git/hooks/commit-msg ".backup-kit/commit-msg-$UPGRADE_STAMP" 2>/dev/null || true
```

Do not delete the backup until the upgraded project passes its own verification and a maintainer has accepted the result.

## Upgrade from v0.1.0 to v0.2.0

Version 0.2.0 makes canonical workflow sources English, adds a complete Simplified Chinese README entry point, and introduces an explicit `document_language` contract for durable project knowledge.

### 1. Resolve document_language before copying workflows

First check whether the target project already has a stored value:

```bash
python3 -c "import json; c=json.load(open('docs/methodology-config.json')); print(c.get('document_language', '<missing>'))"
```

If the value is present and valid, keep it. Conversation language must not replace it.

If the field is missing:

1. Inspect `docs/product.md` and the active module files linked from it.
2. Present the apparent dominant Product language only as a proposal.
3. Ask the maintainer to confirm a BCP 47 tag. The initially verified values are `en` and `zh-CN`; other tags are best-effort.
4. Add only the confirmed `document_language` field with a JSON-aware edit. Preserve every existing and unknown field.
5. Record in `docs/progress.md` that the field was added without translating existing documents.

The recommended path is to run the current [`BOOTSTRAP.md`](./BOOTSTRAP.md) through STEP 0.5 for the already-bootstrapped project classification, then continue with this guide.

Do not infer the value from country, IP address, timezone, operating-system locale, or Feature titles when Product documents are available. Do not translate, rename, or rewrite existing Product, Feature, revision, Progress, or history content during this compatibility step.

Changing an established document language is a separate, explicitly planned migration. Editing the configuration field alone is not a supported language migration; follow [`methodology/05-document-language.md`](./methodology/05-document-language.md).

### 2. Update the installed workflow integration

For Claude Code projects:

```bash
mkdir -p .claude/skills .claude/hooks
cp -r <KIT>/claude-code/skills/* .claude/skills/
cp <KIT>/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py
```

Merge `<KIT>/claude-code/settings.example.json` into an existing `.claude/settings.json`; do not replace unrelated project settings.

For Codex, Aider, Cursor, or another portable integration:

```bash
mkdir -p docs/methodology-prompts .git/hooks
cp <KIT>/ai-agnostic-prompts/*.md docs/methodology-prompts/
```

If `.git/hooks/commit-msg` already exists, compare and merge it manually instead of overwriting it. Otherwise:

```bash
cp <KIT>/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

The native Skills and portable Prompts contain the same canonical English workflow bodies. Their wrappers retain concise English and Chinese discovery text, while durable output follows the target project's confirmed `document_language`.

### 3. Review Coding Rules instead of replacing them

Do not overwrite a target project's filled `docs/coding_rules.md`, `docs/coding-rules/engine-rules.md`, or `docs/coding-rules/language-rules.md` with Kit templates or library stubs.

Review the v0.2.0 canonical rules and merge only changes that the project deliberately adopts. Project-specific architecture, validation commands, exceptions, and field-tested rules remain authoritative for that target project.

Do not copy `methodology/templates/*.tmpl` over established project documents. Templates are initialization sources, not upgrade patches. Do not copy `examples/` into the target project.

### 4. Verify before recording the new version

Run the target project's configured check and the structural checks below:

```bash
python3 -m json.tool docs/methodology-config.json > /dev/null
python3 -m json.tool docs/feature-list.json > /dev/null
python3 -m json.tool docs/feature-list-revisions.json > /dev/null
for feature_file in docs/features/*.json; do
  python3 -m json.tool "$feature_file" > /dev/null || exit 1
done
python3 -c "import json; value=json.load(open('docs/methodology-config.json')).get('document_language'); assert isinstance(value, str) and value.strip(); print(value)"
```

Then run the `static_check_cmd` stored in `docs/methodology-config.json`. Exercise the applicable scenarios from [`methodology/06-document-language-smoke-scenarios.md`](./methodology/06-document-language-smoke-scenarios.md), including a conversation whose language differs from `document_language`.

Confirm that:

- existing durable documents were not translated;
- new durable Product, Feature, revision, Progress, and handoff prose follows `document_language`;
- JSON keys, enums, Feature IDs, paths, placeholder prefixes, commit types, and gate evidence remain stable;
- the selected agent loads the upgraded workflow; and
- the Git Hook still blocks invalid completion evidence.

### 5. Record v0.2.0 only after verification

Use a JSON-aware edit that preserves every unknown field:

```bash
python3 -c "
import json
from datetime import datetime, timezone
from pathlib import Path

path = Path('docs/methodology-config.json')
config = json.loads(path.read_text(encoding='utf-8'))
config['kit_version'] = '0.2.0'
config['upgraded_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
"
python3 -m json.tool docs/methodology-config.json > /dev/null
```

Record the upgrade result, confirmed `document_language`, verification evidence, and any intentionally retained older content in Progress. The upgrade is not complete until a maintainer accepts the observable result.

## Rollback

If verification fails:

1. Stop before recording `kit_version: 0.2.0`.
2. Preserve the original failure output.
3. Restore only the integration files from the reviewed backup using explicit paths.
4. Keep Product, Feature, Progress, and project-specific Coding Rules unchanged.
5. Decide whether to repair the upgrade in a separate branch or remain on the previous Kit version.

Do not use destructive Git operations or force-push as an upgrade recovery mechanism.

## Release notes

### v0.2.0 · International project knowledge

- Established English as the single canonical language for executable Methodology, Skills, Prompts, templates, Coding Rules sources, Hooks, and default examples.
- Added complete, meaning-equivalent English and Simplified Chinese README entry points.
- Added persisted `document_language` behavior while keeping conversation language transient.
- Made Product, Feature, revision, Progress, and handoff prose follow the configured document language.
- Kept keys, enums, IDs, paths, placeholders, Conventional Commit types, and completion evidence stable across language modes.
- Added a confirmation-based compatibility path for existing projects without automatically translating established content.
- Added English, Simplified Chinese, conversation/document-language mismatch, and Legacy migration smoke scenarios.
- Added repository-wide compatibility, distribution-parity, link, JSON, and release checks without new runtime dependencies.

Explicit non-goals remain: translated executable workflow trees, a runtime message catalog, automatic translation of established projects, guaranteed support for every BCP 47 language, and full localization of every Hook message.

See [`docs/release-audit-v0.2.0.md`](./docs/release-audit-v0.2.0.md) for the acceptance-criterion evidence map.

### v0.1.0 · Initial release

- Introduced the Product, Feature, and Coding Rules document model.
- Added nine Claude Code Skills and nine portable Prompts.
- Added Claude Code pre/post tool gates and the Git commit-message gate.
- Added the initial Godot/GDScript field-tested rules and engine/language stubs.
- Added Greenfield and Legacy Bootstrap paths plus the first example projects.
