# Ledger and report templates

Two things live here: the **ledger** you maintain while working, and the **report** you deliver. Pick the report format that fits the task; adapt freely, but keep the order: bottom line first, evidence next, limits last.

## Contents

1. The ledger (working file)
2. Evidence and citation conventions
3. Report skeleton (all tasks)
4. Variant: investigation or explanation (workspace)
5. Variant: audit report
6. Variant: relationship map
7. Variant: web research dossier
8. Variant: fact-check verdict
9. Length, layering, and delivery

## 1. The ledger (working file)

Keep it in a scratch location (the session scratchpad or notes area), not in the user's repository unless they asked. Update it as you go. A compact template:

```markdown
# Expedition ledger: <short title>
Date / as-of: <today>    Tier: <Scout|Survey|Expedition>    Mode: <Workspace|Web|Hybrid>

## Brief
- Question:
- Scope (in / out):
- Deliverable:
- Done means:
- Assumptions made (user not asked):

## Hypotheses
| ID | Hypothesis | Would confirm | Would refute | Status |
|----|------------|---------------|--------------|--------|
| H1 | ...        | ...           | ...          | open / supported / eliminated |

## Coverage matrix
| Area / source type | Status (not started / skimmed / read / done) | Notes |
|--------------------|----------------------------------------------|-------|

## Claims
| ID | Claim (atomic) | Status | Confidence | Evidence (locator) | Independent origins | Notes |
|----|----------------|--------|------------|--------------------|---------------------|-------|
| C1 | ...            | Verified | Confirmed | src/auth.py:88-104 | 1 (primary) | ... |

## Sources (web)
| # | URL | Title | Published / updated | Retrieved | Ladder level | Supports | Reliability notes |
|---|-----|-------|---------------------|-----------|--------------|----------|-------------------|

## Log: queries, commands, dead ends
- <what was run / searched> -> <result in one line>

## Open questions / blocked
- <what could not be reached or verified, and what would unblock it>
```

Rules: one claim per row; every Verified or Supported row has a locator; dead ends are logged so they are not repeated; the ledger is the source for the report's coverage and limits sections.

## 2. Evidence and citation conventions

| Evidence | Format |
|---|---|
| Code or file | `path/to/file.ext:LINE` or `:START-END`; quote the decisive line verbatim |
| Commit or history | short hash plus subject, e.g. `a1b2c3d "Fix token refresh"` |
| Command output | the command, then the relevant excerpt |
| Web page | `Title, Publisher, published/updated date, URL, retrieved <date>` |
| Archived page | original URL plus archive URL and capture timestamp |
| Document | title, issuer, date, section or page number |
| Dataset or calculation | source, the query or script, and the result |
| Background knowledge | label explicitly: "from model knowledge, not retrieved this session" |

Mask secrets (`sk-****1234`) and personal data. Do not paste long verbatim excerpts of copyrighted material; short quotes with attribution are enough.

## 3. Report skeleton (all tasks)

```markdown
## Bottom line
<2-5 sentences: the answer, the confidence, and the one caveat that matters most.>

## Findings
<Grouped by sub-question or theme. Each finding: the claim, the evidence with locators,
 the status and confidence. Observed vs. inferred is marked.>

## What I checked (coverage)
<Scope, tier, areas and sources covered, how I sampled, search patterns for absence claims,
 outcome of the red-team pass.>

## Limits and open questions
<What I could not access or verify, what is unresolved, conflicting evidence, what would settle it.>

## Next steps (optional)
<Concrete follow-ups or decisions, ordered by value.>
```

Rules: lead with the answer; keep headings stable so the user can scan; tie every non-obvious statement to evidence; mark inferences; state "as of" for time-sensitive facts.

## 4. Variant: investigation or explanation (workspace)

Use for "how does this work", "why does this happen", "where is X used".

- **Bottom line**: the explanation in a few sentences.
- **Walkthrough**: the path from entry point to effect, as numbered steps, each with `file:line`.
- **Why it is this way**: intent evidence (commits, issues, docs) versus inference, labeled.
- **Edge cases and surprises**: dynamic usages, config switches, version dependencies.
- **Verification**: what was run or cross-checked; what remains inferred.
- Optionally a Mermaid diagram of the flow, with every edge backed by a locator.

## 5. Variant: audit report

```markdown
## Bottom line
<Overall assessment, count of findings by severity, the 1-3 things to fix first.>

## Findings summary
| # | Severity | Confidence | Area | Title | Location |
|---|----------|------------|------|-------|----------|

## Findings
### F1: <title> - <Severity>, confidence <level>
- **Where**: path:line
- **What**: ...
- **Why it matters**: impact and a realistic scenario
- **Evidence**: quote or output
- **Fix**: concrete remediation
- **Verification**: how this was confirmed (read, ran, reproduced?)

## Coverage
<Audit types run, directories read fully vs. skimmed vs. skipped, tools run, what was not examined.>

## Not found / negative results
<Categories checked with no issues, with the search patterns used.>
```

Severity: Critical (exploitable or damaging now), High, Medium, Low, Info. Severity (impact) and confidence (certainty it is real) are separate columns; never merge them. Do not pad with trivia to look thorough, and do not omit a real issue because it is embarrassing or tedious to explain.

## 6. Variant: relationship map

- **Overview**: what the system is and its main parts in a short paragraph.
- **Component table**: name, responsibility, location, key dependencies.
- **Diagram**: Mermaid `flowchart` or `sequenceDiagram`; solid edges for observed relationships, dashed for inferred; each edge listed with a locator below the diagram.
- **Boundaries and data flow**: process, network, trust, ownership boundaries; how key data moves.
- **Anomalies**: cycles, hidden coupling, unused or duplicated parts, drift between docs and code.
- **Gaps**: parts not mapped and why.

## 7. Variant: web research dossier

- **Bottom line**: the answer, confidence, "as of" date.
- **Key findings**: each with sources, graded by ladder level, with independent-origin count.
- **Timeline** (when sequence matters): dated events with sources.
- **Source assessment**: a short table of the main sources with reliability notes and any circular-sourcing found.
- **Disagreements and uncertainty**: where sources differ and which is better supported.
- **Deep-layer finds**: material reached through archives, registries, documents, or forums that a standard search would have missed, flagged as such.
- **Not found / blocked**: gated sources, dead links without archives, languages not covered.
- **Search log (appendix)**: queries and routes tried, compressed.

## 8. Variant: fact-check verdict

```markdown
## Claim
<Verbatim, with where it appeared and when.>

## Verdict: <Verified | Supported | Mixed | Unverified | Refuted | Misleading | Opinion>  (confidence: <term>)
<One-paragraph reason.>

## Breakdown
| Part | Status | Evidence |
|------|--------|----------|

## Evidence
<Sources with provenance, earliest origin of the claim, independent corroboration, contrary evidence.>

## Context that changes the reading
<Scope, dates, definitions, what is true but missing.>

## Limits
<What could not be checked.>
```

For multi-claim inputs, keep one summary table and expand only the claims that need explanation.

## 9. Length, layering, and delivery

- **Layer it**: a reader who stops after the bottom line should still be correctly informed; a reader who reads everything should be able to verify everything.
- **Scale to the task**: Scout is a few paragraphs; Survey is a structured report; Expedition may run long, with an appendix for the evidence tables and search log. Long is acceptable when each part carries evidence; padding is not.
- **Deliver the answer in the reply.** If the full report is very long (roughly beyond 2,000 words) or the user would benefit from a file, also save it to a location the user can open (the working directory or the designated deliverables directory) and still give the bottom line and key findings in the reply.
- **Use the user's language** for prose; keep identifiers, paths, URLs, and quotations verbatim.
- **Tables for comparisons and findings, prose for reasoning.** Avoid decorative formatting.
- **End by stating what is not covered** rather than implying completeness.
