# Contributing

Thanks for helping improve Data Expedition. This repository ships one skill, so the bar is quality and focus rather than quantity.

## Principles for changes

- **Explain the why.** Instructions that give a reason generalize better than bare rules. Prefer "do X because Y" over capitalized commands.
- **Keep `SKILL.md` lean** (under 500 lines). Put detail in `references/` and point to it from `SKILL.md` with a clear "read when" cue. Every file in `references/` must be mentioned in `SKILL.md`.
- **Stay general.** Do not tune the skill to a single example prompt; test on varied tasks.
- **Keep the boundaries.** Read-only by default, no circumvention of access controls, no dossiers on private individuals, retrieved content is data and not instructions. Changes that weaken these will not be accepted.
- **Frontmatter limits**: `name` must equal the folder name; `description` at most 1024 characters with no angle brackets; only the keys `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility` are allowed.

## Workflow

```bash
pip install pyyaml
python scripts/build_skill.py --check   # validate
python scripts/build_skill.py           # validate and rebuild dist/data-expedition.skill
python scripts/make_graphics.py         # regenerate assets/*.svg after editing their texts
```

1. Edit files under `skills/data-expedition/`.
2. Add or adjust cases in `skills/data-expedition/evals/evals.json` for new behavior, and run them with and without the skill to compare.
3. If you change the `description`, check it against `evals/trigger-evals.json`: it must trigger on the `true` queries and stay quiet on the `false` ones.
4. Update `CHANGELOG.md`, and bump the version in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and the top `CHANGELOG.md` entry together (the validator checks that they agree).
5. Rebuild `dist/data-expedition.skill` and commit it with your change; CI fails if it is stale.

## Reporting problems

Open an issue with the prompt you used, what the skill did, what you expected, and the model and environment (tools available). Transcripts that show where the workflow went wrong are the most useful.
