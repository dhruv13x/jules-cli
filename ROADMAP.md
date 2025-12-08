# Strategic ROADMAP.md

This document outlines the strategic roadmap for `jules-cli` (V3.0), balancing innovation, stability, and technical debt management.

---

## 🏁 Phase 0: The Core (Stability & Debt)
**Goal**: Solid foundation and reliable tooling.

- [x] **Testing**: Coverage > 80% `[Debt]` `S`
    - Current coverage is >89%.
- [x] **CI/CD**: Linting, Type Checking (mypy) `[Debt]` `M`
    - `ruff`, `black`, and `mypy` configured.
- [x] **Documentation**: Comprehensive README `[Debt]` `M`
    - "Gold Standard V3" structure implemented.
- [ ] **Refactoring**: Pay down critical technical debt `[Debt]` `L`
    - [ ] Fix flaky tests in `tests/git/` (currently ignored/timeout).
    - [ ] Improve `doctor` command test isolation (environment dependency).
    - [ ] Standardize mocking across test suite.

## 🚀 Phase 1: The Standard (Feature Parity)
**Goal**: Competitiveness and User Experience.

- [x] **UX**: CLI improvements, Error messages `[Feat]` `M`
    - Implemented modular command architecture and robust error handling.
- [x] **Config**: Robust settings management `[Feat]` `S`
    - TOML-based config and environment variable support.
- [x] **Performance**: Async, Caching `[Feat]` `M`
    - Session ID and artifact caching implemented.
- [ ] **TUI**: Advanced Dashboard improvements `[Feat]` `M`
    - Enhance `textual` based UI for complex sessions.

## 🔌 Phase 2: The Ecosystem (Integration)
**Goal**: Interoperability and Extensibility.

- [ ] **API**: Public Python API Stability `[Feat]` `L` *Requires Phase 1*
    - Stabilize `jules_cli.core` for external usage.
- [ ] **Plugins**: Extension system `[Feat]` `XL` *Requires Phase 1*
    - Design and implement plugin architecture for community extensions.
- [ ] **Webhooks**: Real-time notifications `[Feat]` `M`
    - Support for Slack/Discord integration.
- [ ] **IDE**: VS Code / JetBrains Extensions `[Feat]` `L`
    - Wrappers for CLI functionality.

## 🔮 Phase 3: The Vision (Innovation)
**Goal**: Market Leader and Autonomous Operations.

- [ ] **AI**: Deep LLM Integration (Agents) `[Feat]` `XL` *Requires Phase 2*
    - Multi-agent orchestration (Architect, QA, Security).
- [ ] **Cloud**: K8s/Docker containerization support `[Feat]` `L`
    - Native support for containerized environments.
- [ ] **Self-Healing**: Autonomous CI/CD pipelines `[Feat]` `XL`
    - Automatically analyze and fix pipeline failures.

---

**Legend:**
- `[Debt]`: Technical Debt / Maintenance
- `[Feat]`: New Feature
- `[Bug]`: Bug Fix
- **S/M/L/XL**: Effort Estimate (T-Shirt Sizing)
