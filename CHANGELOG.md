# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-03

### Added
- `data-expedition` skill: one skill, two modes (workspace/repository analysis and web research) sharing a common
  workflow: frame, depth tier, hypothesis-driven map, breadth-then-depth exploration, ledger, verification,
  saturation stopping rule, self-audit, structured report.
- References: `workspace-mode.md`, `web-mode.md`, `verification.md`, `report-templates.md`.
- Evals: six task evals and twenty trigger-description queries (`skills/data-expedition/evals/`).
- Packaging: Claude Code plugin manifest and marketplace, manual-install layout, prebuilt `dist/data-expedition.skill`,
  and `scripts/build_skill.py` for validation and deterministic builds.
- Documentation in English and Russian, MIT license, contribution guide, CI validation workflow.
