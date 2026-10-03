# Workspace mode

Playbook for investigating a repository, working directory, or a pile of local files: relationships, code, audits, logs, datasets, anything the evidence of which lives on disk. Read `SKILL.md` first for the overall workflow; this file is the detailed technique.

## Contents

1. Orient: build the map before diving
2. Search discipline
3. Reading and tracing
4. Relationship mapping
5. "Why" questions: history and intent
6. Audits (checklists by type)
7. Data, logs, and structured files
8. Large workspaces
9. Evidence standard
10. Pitfalls

## 1. Orient: build the map before diving

Spend the first few minutes learning the terrain; it pays back many times over.

- **Layout**: list the top two or three levels of the tree. Identify source, tests, docs, config, scripts, infra, generated and vendored directories (`node_modules`, `vendor`, `dist`, `build`, `.venv`, `target`). Know what to skip and what to read.
- **Manifests and entry points**: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `Makefile`, `Dockerfile`, CI workflows, `main`/`index`/`app` files, CLI definitions, route tables, job schedulers.
- **Orientation docs**: README, CONTRIBUTING, ARCHITECTURE, ADRs, `docs/`, CLAUDE.md or similar. Treat them as claims to verify, not as truth; docs drift.
- **Size and language mix**: file counts and line counts per directory (`git ls-files | xargs wc -l` or equivalent) to decide the tier and the partitioning.
- **Recent activity**: `git log --oneline -n 30`, branches, tags, which areas change most. Hot areas deserve more scrutiny.
- **Tests**: where they live and what they cover. Tests are executable specifications; read them to learn intended behavior.

Record the orientation in the ledger as the initial coverage matrix: one row per significant module or directory.

## 2. Search discipline

A single grep for the obvious name finds a fraction of the real usages. For any "where is X used / defined / configured" question, sweep these axes:

- **Name variants**: `fooBar`, `foo_bar`, `FooBar`, `FOO_BAR`, `foo-bar`, plural and singular, abbreviations, prefixes and suffixes.
- **Definition vs. usage vs. re-export**: where it is declared, where it is imported, where it is aliased or wrapped.
- **Indirect references**: string keys, reflection, dynamic imports, dependency injection, decorators and annotations, plugin registries, route strings, feature flags, environment variables, CLI flags.
- **Non-code references**: configs (YAML, TOML, JSON, `.env.example`), SQL and migrations, schemas (OpenAPI, protobuf, GraphQL, JSON Schema), IaC (Terraform, Helm), CI definitions, docs, comments, test fixtures.
- **Other languages in the repo**: a Python service called from a TypeScript client by URL, a shell script that invokes a binary.
- **Git history**: removed or renamed things (`git log -S'symbol' --all`, `git log -G'regex'`, `git log --follow -- path`).

Use fast file-pattern and content search tools in parallel. Count matches, and when the count is large, partition by directory instead of skimming a truncated list. If a result list was truncated, say so in the ledger and narrow the search rather than assuming the rest is similar.

Interpreting empty results: zero matches means "not found with these patterns in these paths". Before reporting absence, try at least two alternative patterns and confirm the search covered the right directories (ignored files, hidden dirs, generated code, other branches). Record the exact patterns you tried.

## 3. Reading and tracing

- **Read whole files** for anything load-bearing, not only the matching lines. Context around a match routinely changes its meaning (guarded by a flag, dead branch, test-only path).
- **Trace in both directions**: callers up to the entry point, callees down to the side effect. For data flow, follow a value from where it enters (request, file, env, queue) to where it is stored, sent, or rendered; note every transformation and validation on the way.
- **Follow config into code and code into config**: a behavior often depends on a default defined three layers away.
- **Check the actual version in use**: lockfiles, pinned images, vendored copies. Behavior depends on the resolved version, not the manifest range.
- **Run things when it helps and is safe**: tests, type checks, linters, read-only commands, a small script to count or cross-check. Observed runtime behavior beats reasoning about code. Do not run anything that mutates state, hits production, or needs secrets unless the user asked. Report exactly what was run and its output.
- **Disagreement between sources** (docs vs. code, comment vs. behavior, test vs. implementation): code that actually executes wins as evidence of behavior; the disagreement itself is a finding.

## 4. Relationship mapping

When the task is "how does this fit together":

1. Identify the **nodes**: modules, services, packages, tables, queues, external APIs, config sources.
2. Identify the **edges** with their type: imports, calls, publishes/subscribes, reads/writes, deploys, depends-on. Note direction.
3. Mark **boundaries**: process boundaries, network hops, trust boundaries, ownership boundaries.
4. Look for **structure and anomalies**: cycles, god modules, layering violations, hidden coupling through shared state, files nobody imports, dependencies nobody uses, duplicated logic.
5. Present it as a short table of components with responsibilities plus a diagram when it clarifies (Mermaid `flowchart` or `sequenceDiagram` in a fenced block). Every edge in the diagram should be backed by a locator in the text.

Do not draw edges you inferred but did not see; mark inferred edges as such (dashed line, or a note).

## 5. "Why" questions: history and intent

Code shows what, history often shows why.

- `git blame` and `git log -L` for the lines in question; read the commit messages and linked issues or PRs.
- Search the issue tracker or PR discussions if tools allow (repository connectors), and docs/ADRs for decision records.
- Distinguish **intent** (stated by an author) from **behavior** (what the code does) from **your inference**. Label which one you are giving.
- If history is shallow (squashed, imported), say that intent could not be recovered and give the most plausible explanation with its confidence.

## 6. Audits (checklists by type)

Pick the types the request implies; for "audit everything" at Expedition tier, run all that apply. Each finding needs: location, what is wrong, why it matters, evidence, severity, and a suggested fix. Severity scale: **Critical** (exploitable or data-loss now), **High**, **Medium**, **Low**, **Info**. Include confidence separately from severity.

**Security**
- Secrets in code, history, configs, CI logs, examples (`git log -p -S` on suspicious patterns; mask values in the report).
- Injection surfaces: SQL, shell, template, path traversal, XSS, deserialization, SSRF, open redirects.
- AuthN/AuthZ: unprotected routes, missing ownership checks, role confusion, token handling, session settings.
- Crypto misuse: weak algorithms, hard-coded keys or IVs, home-made schemes, disabled TLS verification.
- Dependencies: known-vulnerable versions (cross-check advisories in Web mode), unpinned or typosquat-looking packages, install scripts.
- CI/CD and infra: overly broad workflow permissions, untrusted input in workflows, pinned vs. floating actions, public buckets, permissive IAM, containers running as root.

**Correctness and robustness**
- Error handling that swallows failures, unchecked returns, race conditions, off-by-one and boundary handling, time zone and encoding assumptions, resource leaks, retries without backoff or idempotency.

**Consistency and drift**
- Docs vs. code, config defaults vs. documented defaults, API schema vs. handlers, types vs. runtime validation, version numbers across manifests, changelog vs. tags.

**Dependencies and licensing**
- Unused, duplicated, or conflicting dependencies, abandoned packages, license compatibility, vendored code without attribution.

**Maintainability**
- Dead code and unreachable branches, duplicated logic, oversized units, circular dependencies, TODO/FIXME clusters, flaky or missing tests in critical paths.

**Performance**
- N+1 queries, unbounded loops or memory growth, blocking calls in async paths, missing indexes (check migrations), cache misuse. Only claim a hotspot if you can show the path; otherwise label it a suspicion.

**Data and schema**
- Nullable-vs-required mismatches, orphaned references, migrations that cannot roll back, PII stored or logged without need.

## 7. Data, logs, and structured files

For CSV, JSON, logs, SQLite, spreadsheets, and similar:

- **Profile first**: shape, columns and types, null rates, ranges, duplicates, encoding, time span. Do this before any conclusion.
- **Compute, don't eyeball**: use a script or shell/SQL for counts, groupings, joins. For any figure that appears in the report, compute it a second way (different tool or query) or sanity-check it against a known total.
- **Keep it reproducible**: record the exact command or query next to the result in the ledger.
- **State sampling honestly**: if you read a sample, say how large and how chosen, and do not extrapolate beyond what the sample supports.
- **Logs**: establish the time window and timezone, correlate by request/trace IDs, separate first failure from cascading failures, and look at what happened just before the earliest error.
- **Binary or opaque formats**: inspect headers and metadata before guessing; say when a format could not be parsed.

## 8. Large workspaces

- **Partition** by directory or concern, and give each partition an owner (yourself in sequence, or a subagent if permitted). Give each a self-contained brief and the evidence format required.
- **Prioritize** by risk and centrality: entry points, auth, data stores, money paths, recently changed hot spots, then the rest.
- **Sample deliberately** in the long tail, and say that you sampled; the coverage matrix should show which cells were fully read, skimmed, or skipped, and why.
- **Checkpoint** the ledger regularly so a context reset does not erase progress.

## 9. Evidence standard

- Cite as `path/to/file.ext:LINE` (or `:START-END`). Quote the decisive line or two verbatim; paraphrase the rest.
- For command output, give the command and the relevant excerpt.
- Pin the version: commit hash (`git rev-parse --short HEAD`) for repository claims that could change.
- Separate **observed** (read it, ran it), **inferred** (derived), and **not verified**. Never upgrade an inference to an observation in the report.
- Absence claims carry the search that supports them.

## 10. Pitfalls

- Reading a stale branch or a generated/vendored copy and attributing it to the live code.
- Trusting comments, docstrings, or README over the executing code.
- Missing dynamic usage (strings, reflection, config-driven wiring) and declaring something dead.
- Case-insensitive file systems, symlinks, and monorepos with several packages of the same name.
- Same identifier meaning different things in different modules.
- Truncated tool output taken as complete.
- Treating a test's mock as the real implementation.
- Quietly widening scope into a refactor: this skill investigates and reports; changes only when the user asks.
