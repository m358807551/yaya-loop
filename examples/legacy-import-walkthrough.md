# Adopting Yaya Loop in a legacy project · Narrative walkthrough

> This fictional but realistic walkthrough shows how the legacy branch in BOOTSTRAP.md works for a Django web application that has been in development for more than a year. It demonstrates:
>
> 1. what an established project typically goes through during adoption;
> 2. what a reverse-engineered Product specification looks like; and
> 3. how to reconstruct a useful Feature history without drowning in historical detail.
>
> The AI's exact questions will vary by project. The exchange below is representative.

---

## Example project

- **Name:** `OrderForge`
- **Stack:** Django 4, PostgreSQL, Celery, Redis, server-rendered templates, and a small amount of HTMX
- **Scale:** About 20,000 lines of Python, 14 months of development, and four developers
- **Business:** B2B order management covering customer orders, inventory allocation, shipping integrations, and invoice generation
- **Current documentation:** No Product specification; the README only explains setup; TODOs are scattered across Linear and code comments
- **Current pain:** New developers need about a week to understand module boundaries. Feature work requires repeated coordination across four people, while risky service code is rarely refactored.

---

## Step 0 · Detect the project state

The AI performs read-only discovery:

```console
$ ls docs/product.md docs/feature-list.json 2>/dev/null
# no output

$ git log --oneline | wc -l
1247

$ find . -maxdepth 3 -type f -name "*.py" | wc -l
312
```

It reports:

> This is an existing codebase with 312 Python files and 1,247 commits. I will use the legacy reverse-engineering path. I will not rewrite existing Product or Feature documents unless you explicitly authorize replacement.

If the repository already contained Yaya Loop state, Bootstrap would preserve it and use the upgrade or continuation path instead of silently regenerating it.

---

## Step 1 · Resolve the agent and document language

The user is running Bootstrap through Codex, so the selected integration is the portable Prompt workflow.

The AI also confirms the language for durable project knowledge:

> Which language should Product, Feature, Progress, and other generated project prose use?

The user chooses English. Bootstrap records a stable language-neutral value:

```json
{
  "document_language": "en"
}
```

Conversation language may change later without changing this stored setting. JSON keys, Feature IDs, statuses, evidence markers, paths, and commands remain in their canonical machine form regardless of the selected document language.

---

## Step 2 · Reverse-engineer the existing system

### 2.1 Read-only code archaeology

The AI gathers evidence before asking the user to correct its model:

```console
$ sed -n '1,80p' README.md
# setup, Docker Compose, and environment variables; no business overview

$ git log --oneline -100
# representative commits:
# feat: add invoice PDF export
# fix: stock deduction race condition
# feat: webhook for SF Express
# refactor: split order_service.py

$ find . -maxdepth 2 -type d
# apps/orders apps/inventory apps/customers apps/shipping
# apps/invoicing apps/reporting api/v1 api/v2 tasks utils
# templates static config docker tests

$ find . -maxdepth 4 -type f -name "*.py" -exec wc -l {} \; | sort -rn | head -5
# 1832  apps/orders/services/order_service.py
# 1421  apps/inventory/services/stock_service.py
# 1108  apps/shipping/services/shipping_service.py
#  892  apps/invoicing/services/invoice_generator.py
#  654  apps/customers/services/customer_service.py
```

This audit is evidence gathering, not authorization to modify application code.

### 2.2 Present a one-page hypothesis

The AI summarizes its current understanding and makes uncertainty explicit:

> **Working hypothesis:** OrderForge is a B2B order-management system organized around six Django applications:
>
> - `orders` — order creation and the order state machine; probably the core domain
> - `inventory` — stock management and allocation, including earlier race-condition fixes
> - `customers` — customer master data
> - `shipping` — carrier integration, including an SF Express webhook
> - `invoicing` — invoice generation and PDF export
> - `reporting` — reporting and data export
>
> The repository contains both API v1 and v2, which may indicate an incomplete migration. Celery tasks appear to handle asynchronous domain work, but their ownership is not yet clear.
>
> Please correct these assumptions:
>
> 1. Is `apps/orders/` the core domain?
> 2. Is API v1 still serving clients, or is it retained only for compatibility?
> 3. Is `apps/reporting/` functional or only a skeleton?
> 4. Which applications own the Celery tasks?
> 5. Which area is currently the most painful to change?
> 6. Is significant work in progress outside the current branch?
> 7. Is any code operational but considered too risky to touch?
> 8. Should this first pass cover all six applications or only the core domains?
> 9. Is `apps/legacy/` still active?
> 10. Should Product describe core use cases or every API endpoint?

The user confirms that orders is the core, API v1 remains only for compatibility, reporting is a skeleton, inventory concurrency is the largest risk, and the first pass should cover the five operational domains rather than reporting or legacy code.

### 2.3 Draft the Product overview

The AI renders the canonical Product structure in the configured document language and marks inferred claims as `[REVERSE-ENGINEERED]`:

```markdown
# OrderForge · Reverse-engineered baseline

> Current version: **V1.0 · In production for 14 months** [REVERSE-ENGINEERED]

## One-line positioning [REVERSE-ENGINEERED]

A B2B order-management system covering the path from customer order creation through shipping and invoicing. [REVERSE-ENGINEERED]

## Target users [REVERSE-ENGINEERED]

- **Primary users:** B2B sales operations staff and customer purchasing teams [REVERSE-ENGINEERED]
- **Usage context:** High-frequency daily use in sessions lasting 5–30 minutes [REVERSE-ENGINEERED]

## Core loop [REVERSE-ENGINEERED]

1. A salesperson or customer creates an order (`apps/orders`).
2. The system validates and allocates inventory (`apps/inventory`).
3. The order moves to carrier assignment (`apps/shipping`, including SF Express).
4. Shipment completion triggers invoice generation (`apps/invoicing`).
5. State changes schedule asynchronous notifications through Celery (`tasks/`).

## Module list [REVERSE-ENGINEERED]

| No. | File | Module | Status |
| --- | --- | --- | --- |
| 01 | [01-customers.md](./product/01-customers.md) | Customer master data | done |
| 02 | [02-orders.md](./product/02-orders.md) | Order core | done |
| 03 | [03-inventory.md](./product/03-inventory.md) | Inventory | done |
| 04 | [04-shipping.md](./product/04-shipping.md) | Shipping integrations | done |
| 05 | [05-invoicing.md](./product/05-invoicing.md) | Invoicing | done |

## Module dependencies [REVERSE-ENGINEERED]

01-customers → 02-orders → 03-inventory
                     ├→ 04-shipping
                     └→ 05-invoicing

## Visual direction [REVERSE-ENGINEERED]

OrderForge uses the existing server-rendered operations interface. Bootstrap records the current interface without introducing a visual redesign.

## Audio direction [REVERSE-ENGINEERED]

OrderForge has no application audio and no current requirement for sound cues.

## Change history

- 2026-05-25: Created through the Yaya Loop legacy Bootstrap path at commit `<git rev-parse HEAD>`.
```

### 2.4 Recover module specifications

For each of the five selected domains, the AI reads relevant models, services, tests, and external interfaces before creating `docs/product/0N-*.md`. Dependency order determines the stable numbers: customers, orders, inventory, shipping, then invoicing.

Every reconstructed module retains the complete canonical section set in template order. Inferred headings carry the uncertainty marker, while an inapplicable section keeps its heading and states why it does not apply:

```markdown
## Module positioning [REVERSE-ENGINEERED]
## Functional flow [REVERSE-ENGINEERED]
## Data model [REVERSE-ENGINEERED]
## State machine (if applicable) [REVERSE-ENGINEERED]
## UI sketch [REVERSE-ENGINEERED]
## Audio entries [REVERSE-ENGINEERED]
## Numeric rules [REVERSE-ENGINEERED]
## Acceptance criteria [REVERSE-ENGINEERED]
## Edge cases [REVERSE-ENGINEERED]
## Change history [REVERSE-ENGINEERED]
```

For example, a backend-only module can say `Not applicable; this module has no direct UI` under UI sketch and `Not applicable; OrderForge has no application audio` under Audio entries. It does not delete either section.

Unverified claims remain marked `[REVERSE-ENGINEERED]`. The AI does not invent future functionality or silently convert TODO comments into requirements. Future changes must enter through the Product-change workflow.

### 2.5 Reconstruct a bounded Feature history

The history is recovered in two phases.

**Phase A: representative completed capabilities.** The user and AI choose no more than 15 milestones that explain the current system without recreating every historical commit:

| ID | Title | Source | Notes |
| --- | --- | --- | --- |
| F001 | Create the Django skeleton and PostgreSQL integration | infrastructure | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F002 | Add customer master-data CRUD | product/01-customers.md#data-model-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F003 | Add order creation and the base state machine | product/02-orders.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F004 | Extend order states from payment through completion | product/02-orders.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F005 | Add the inventory model and basic allocation | product/03-inventory.md#data-model-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F006 | Make inventory allocation transaction-safe | product/03-inventory.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F007 | Integrate the SF Express webhook | product/04-shipping.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F008 | Generate shipping orders | product/04-shipping.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F009 | Generate invoice PDFs | product/05-invoicing.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F010 | Send invoices asynchronously through Celery | product/05-invoicing.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F011 | Provide the API v1 endpoints | infrastructure | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. Obsolete but retained for client compatibility. |
| F012 | Introduce API v2 | infrastructure | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F013 | Add customer authentication and permissions | product/01-customers.md#functional-flow-reverse-engineered | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F014 | Customize the sales administration UI | infrastructure | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |
| F015 | Add structured logging and Sentry monitoring | infrastructure | Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`. |

Completed milestones receive `done` status and evidence tied to historical commits where possible. Bootstrap does not pretend that they passed the current execution loop retroactively.

**Phase B: confirmed future work.** Only work explicitly confirmed by the user becomes pending Features:

| ID | Title | Source | Status |
| --- | --- | --- | --- |
| F016 | Replace database inventory locking with a Redis distributed lock | product/03-inventory.md#functional-flow-reverse-engineered | pending |
| F017 | Export orders to Excel as the first reporting capability | product/02-orders.md#functional-flow-reverse-engineered | pending |
| F018 | Retry failed SF Express webhook deliveries | product/04-shipping.md#functional-flow-reverse-engineered | pending |

The resulting `docs/feature-list.json`, `docs/features/F0XX.json`, and `docs/feature-list-revisions.json` follow the same schema as a greenfield project. IDs, statuses, dependency references, and evidence markers remain canonical; descriptions and acceptance criteria use `document_language`.

### 2.6 Record known code smells without blocking adoption

An optional read-only smell selection pass finds candidates such as:

```text
High severity
- apps/orders/services/order_service.py: 1,832 lines and multiple responsibilities
  Candidate split: order creation, order state transitions, and order queries

Medium severity
- apps/inventory/services/stock_service.py: 1,421 lines and growing coupling
- apps/shipping/services/shipping_service.py: four hard-coded SF Express endpoints

Acceptable for now
- Several direct datetime.now() calls make time-dependent tests harder, but do not currently justify an adoption-blocking refactor
```

Confirmed findings go to the smell backlog or the relevant Feature notes. They do not silently become `must_fix` findings for already completed historical Features.

---

## Step 3 · Create project-specific Coding Rules

Bootstrap identifies Django and Python, then renders the four-layer Coding Rules structure:

- Layers 1 and 2 define collaboration, architecture, verification, acceptance, and evidence gates.
- The platform layer starts from `coding-rules-library/engines/backend-service.md` and is refined against the repository.
- The language layer starts from `coding-rules-library/languages/python.md` and is refined against the project's real Python conventions.

Project-specific facts—Django transaction boundaries, Celery retry policy, API compatibility, migration safety, and test commands—belong in the target project's `docs/coding_rules.md` and referenced rule files. The kit's canonical workflow sources are not copied into a translated parallel tree.

The user confirms the automated verification command:

```text
mypy . && ruff check . && pytest
```

Bootstrap stores it as `static_check_cmd` rather than assuming that generic Python commands are sufficient.

---

## Step 4 · Initialize Progress and handoff state

The AI creates `docs/progress.md` in English. It records:

- the reverse-engineering anchor commit;
- which modules were inspected;
- which claims remain `[REVERSE-ENGINEERED]`;
- the first pending Feature, F016;
- important repository-specific constraints; and
- any unresolved questions that the next session must not guess about.

This creates durable handoff context without dumping the entire Git history into every future session.

---

## Steps 5–6 · Install the integration and run smoke checks

For Codex or another portable agent, Bootstrap installs the required files from `ai-agnostic-prompts/` and the Git gate from `git-hooks/commit-msg` according to the repository's installation guide. A Claude Code project would use the corresponding native Skills and Hooks.

The smoke checks verify that:

1. all generated JSON parses;
2. Feature index IDs match detail filenames and detail IDs;
3. dependencies refer to existing earlier Features;
4. Product links and Coding Rules references resolve;
5. `document_language` and `static_check_cmd` are persisted;
6. the selected agent can load the workflow entrypoint; and
7. the Git Hook reports actionable English errors without changing existing Git history.

Bootstrap does not automatically start F016, commit unrelated working-tree changes, switch branches, force-push, or rewrite application code.

---

## The first week after adoption

1. **Refine recovered knowledge incrementally.** When a developer works in a service, verify the corresponding Product module and remove `[REVERSE-ENGINEERED]` only from claims that have been confirmed.
2. **Run F016 through the complete execution loop.** This is the first real Feature under Yaya Loop and will expose any Coding Rules that conflict with established project practice.
3. **Review the smell backlog weekly.** Select one justified refactor at a time instead of turning adoption into an unbounded cleanup project.
4. **Route new requests through Product first.** Product changes update the durable requirement source before Feature synchronization; they do not jump directly from chat into code.

---

## What a successful first 30 days should improve

- New developers build a useful domain model from Product and module documents instead of reconstructing it entirely from service code.
- Product changes identify affected modules before implementation begins.
- Feature scope and acceptance criteria reduce cross-team ambiguity.
- Refactors are selected from recorded evidence rather than whichever large file is most annoying that day.
- AI sessions inherit stable Product, Feature, Coding Rules, Progress, and language context from the repository.

These are goals to measure, not guaranteed numerical outcomes. The team should compare onboarding time, escaped defects, and Feature cycle time against its own baseline.

---

## Common adoption mistakes

1. **Reconstructing history too finely.** Turning a 20,000-line system into 50 or more completed Features creates a museum nobody maintains. Keep the retrospective set small and representative.
2. **Trying to perfect Product in one pass.** `[REVERSE-ENGINEERED]` is an explicit uncertainty marker. Refine it as real work touches each domain.
3. **Treating code comments as approved requirements.** A TODO is evidence to discuss, not automatic Product scope.
4. **Translating stable machine fields.** Keep JSON keys, IDs, statuses, evidence markers, paths, and commands canonical even when project prose uses another language.
5. **Letting adoption rewrite existing behavior.** Bootstrap documents and configures the current project; behavior changes belong in separately approved Features.
6. **Forcing the workflow on everyone at once.** Start with one or two core maintainers, learn where the rules need project-specific refinement, and expand deliberately.
7. **Interrupting an urgent production fix.** Pause Bootstrap, handle the incident through the project's current safe process, then resume from recorded Progress state.
