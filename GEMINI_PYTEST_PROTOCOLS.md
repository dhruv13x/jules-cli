# GEMINI_PYTEST_PROTOCOLS.md

## 🧪 Pytest Execution Protocols for Gemini

This file defines strict, deterministic workflows Gemini must follow when assisting with test execution, debugging, and repair. These rules ensure fast feedback loops, reliable fixes, and consistent testing discipline across the project.

---

## ✅ 1. Primary Directive

When working on tests:

> Always fix failing tests first before writing new tests or refactoring.

No optimization, cleanup, or redesign happens until the suite is green.

---

## ✅ 2. File‑Level Test Loop (Fast Feedback Mode)

When a test failure occurs in a specific file:

**Step 1** — Fix the failing test(s) inside the file.
- Debug only the relevant failure.
- Avoid touching unrelated code unless clearly necessary.

**Step 2** — Re-run pytest ONLY for that file:
```bash
pytest path/to/file.py
```

**Examples:**
```bash
pytest packages/platform_core/tests/task_manager/test_manager.py
pytest services/forwarder_bot/tests/ui/test_menus.py
```

**Step 3** — Repeat until this file passes 100%.

This ensures rapid iteration and prevents noise from unrelated failures.

---

## ✅ 3. Full Suite Verification

Once the file-level tests pass:
```bash
pytest
```

If failures appear elsewhere:
- Apply the same file-level loop to each failing file.

Gemini must never mark work as "complete" until the full suite is green.

---

## ✅ 4. Coverage-Awareness Protocol

After all failures are fixed:

**Step 1** — Identify modules with low or missing test coverage.
Focus areas:
- Critical runtime logic
- High-frequency code paths
- Error-handling logic
- Cache/database race‑condition surfaces

**Step 2** — Add missing tests.
Priority order:
1. Critical business logic
2. Public APIs/interfaces
3. Edge-case flows
4. Stability-related scenarios

**Step 3** — Re-run full pytest suite until all tests pass.

---

## ✅ 5. Continuous Testing Cycle

Gemini must follow this loop strictly:
```
fix → run file-level tests → repeat → full suite → coverage → repeat
```

This methodology guarantees:
- Fast iteration
- Accurate test isolation
- Minimal regression introduction
- Clean and predictable debugging workflow

---

## 🔒 Additional Guardrails

**Gemini must not:**
- Run global pytest after every small fix (only after file-level loop is green)
- Modify large sections of code when a localized fix is possible
- Skip tests or mark them xfail unless explicitly instructed
- Invent tests without verifying context
- Introduce refactors before a full green suite

**Gemini should:**
- Keep fixes minimal and targeted
- Provide entire corrected files when asked for a fix
- Explain root cause concisely (unless `--quick`)
- Highlight reliability risks if encountered

---
