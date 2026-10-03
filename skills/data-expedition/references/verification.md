# Verification, fact-checking, and deep reasoning

How to decide what is true, how sure to be, and how to say it. Applies in both modes: a claim about code needs the same discipline as a claim about the world.

## Contents

1. Decompose the claim
2. Grade the evidence
3. Verdict labels
4. Confidence vocabulary
5. Hypothesis testing (deep reasoning protocol)
6. Common traps
7. Numbers, quotes, dates, versions
8. Conflicting sources
9. False premises and unanswerable questions
10. Red-team pass

## 1. Decompose the claim

Before checking anything, break the statement into **atomic, checkable parts**.

- Who, what, when, where, how much, compared to what, according to whom.
- **Scope words**: all / most / some, always / usually, ever / never, "the largest", "the first". These are where most claims break.
- **Presuppositions**: "Why did X fail?" presupposes that X failed. Check the presupposition first.
- **Definitions**: what counts as "a user", "a breach", "a company", "unused code". Disagreements are often definitional.
- **Time and version anchor**: true when, in which release, in which jurisdiction.
- **Type of claim**: factual (checkable), causal (needs more than correlation), predictive (cannot be verified, only assessed), evaluative or opinion (label as such).

Give each atomic part an ID and enter it in the claim ledger (`report-templates.md`).

## 2. Grade the evidence

For each piece of evidence, ask:

| Question | Why it matters |
|---|---|
| **Proximity**: is it first-hand (the original record, the code, the author) or relayed? | Each hop adds distortion |
| **Independence**: does it come from a different origin than the other evidence? | Ten repetitions of one source are one source |
| **Method**: is it transparent how the figure or statement was produced? | Unreproducible claims deserve less weight |
| **Expertise and incentive**: who is speaking, what do they gain? | Self-reporting and marketing are biased by default |
| **Recency**: is it current for what the claim needs? | Facts expire |
| **Corroboration**: do independent sources converge? Diagnostic evidence (that would look different if the claim were false) counts most | Fit with many hypotheses proves little |

Rules of thumb:
- A **primary document that directly states the thing** can settle a claim alone (for example the statute text, the file you read, the filing).
- Otherwise, **"verified" needs at least two independent origins** that did not copy each other.
- Evidence you observed in this session (read the file, ran the command, fetched the page) outranks recollection from training data. Background knowledge is a lead, not a citation.

## 3. Verdict labels

Use one status per claim in the ledger and the report:

| Label | Meaning |
|---|---|
| **Verified** | Settled by primary evidence or by independent corroboration; nothing credible contradicts it |
| **Supported** | Evidence favors it but falls short of the Verified bar (single good source, partial scope) |
| **Mixed / Disputed** | Credible evidence on both sides, or true in part; say which part |
| **Unverified** | Could not be confirmed or refuted with the available access; state what was tried |
| **Refuted** | Contradicted by primary evidence or by strong independent evidence |
| **Misleading** | Literally true (or partly) but framed to imply something the evidence does not support |
| **Opinion / Unfalsifiable** | Not a checkable factual claim; say so rather than rule on it |

## 4. Confidence vocabulary

Pair a status with a confidence level so the reader knows how hard to lean on it. Use these terms consistently:

| Term | Rough meaning |
|---|---|
| **Confirmed** | Directly observed or settled by primary evidence (>95%) |
| **Very likely** | Strong convergent evidence, no credible contrary signal (~85-95%) |
| **Likely** | Evidence favors it, some gaps (~65-85%) |
| **Toss-up** | Roughly balanced (~35-65%) |
| **Unlikely** | Evidence leans against (~15-35%) |
| **Very unlikely / Refuted** | Strong contrary evidence (<15%), or directly contradicted |
| **Cannot determine** | Not enough accessible evidence either way |

Use the full range; if everything is "likely", the labels carry no information. Separate **"I found no evidence of X"** (a statement about your search) from **"X does not exist"** (a statement about the world), and say which one you mean.

## 5. Hypothesis testing (deep reasoning protocol)

Use this for non-obvious questions: root causes, "why", attributions, anything where the first explanation could be wrong. Think deliberately here; this is where depth pays.

1. **State the question precisely** and what a satisfying answer would look like.
2. **Enumerate rival hypotheses**, including a boring one, an uncomfortable one, and "the premise is wrong". Aim for at least three when the problem is genuinely open.
3. **Derive predictions**: for each hypothesis, what would you expect to observe, and what would you not expect? Prefer **diagnostic** observations, the ones that separate hypotheses.
4. **Gather evidence aimed at the diagnostic predictions**, not just at confirming your favorite.
5. **Score**: put hypotheses against evidence (a small matrix: consistent / inconsistent / neutral). Eliminate by inconsistency rather than by accumulating confirmations.
6. **Cross-check by a second method**: re-derive the key result differently (another query, an independent source, a recomputation, a different code path). If the two disagree, you have found something.
7. **Look for contradictions** in your own picture. A fact that does not fit is the most valuable one; do not explain it away.
8. **Write down what would change your mind**, and check whether that evidence is obtainable.
9. **Conclude with calibrated confidence**, naming the strongest surviving rival.

Keep the working in the ledger, and keep it compact: hypotheses, the evidence table, the elimination reasoning.

## 6. Common traps

- **Circular sourcing**: many articles, one origin. Trace to the origin.
- **Stale facts**: office-holders, prices, versions, laws, APIs, availability. Check currency and give an "as of" date.
- **Version and scope drift**: the library changed, the law was amended, the page was edited, the jurisdiction differs.
- **Correlation presented as causation**; survivorship bias; cherry-picked windows or baselines; relative vs. absolute change; per-capita vs. totals; mean vs. median.
- **Unit and currency slips**: bits vs. bytes, million vs. billion in different languages and conventions, nominal vs. inflation-adjusted, fiscal vs. calendar year.
- **Misattributed or truncated quotes**: find the earliest instance and the full context.
- **Out-of-context media**: real image, wrong event; real clip, edited; synthetic content.
- **Press release as news**, **"studies show"** without a study, abstract-only reading, preprint reported as settled, retracted or corrected work still cited.
- **Satire and parody** mistaken for reporting.
- **Authority halo**: an expert outside their domain, a prestigious venue with a weak paper, a confident tone without evidence.
- **Anchoring and confirmation bias**: the first plausible answer acquires gravity. Counter it by searching for disconfirming evidence deliberately.
- **Code-specific**: trusting comments over behavior, a mock mistaken for the implementation, dead-looking code that is reached dynamically.

## 7. Numbers, quotes, dates, versions

- **Numbers**: recompute from the underlying data where you can; check units and orders of magnitude; reconcile discrepancies between sources by tracing each to its method and definition; keep the denominator with the percentage.
- **Quotes**: verbatim, with locator, and traced to the earliest and original-language source when it matters.
- **Dates**: pin publication, event, and retrieval dates; compute relative dates ("last year", "recently") against today's date; note timezone when it matters.
- **Versions**: pin the exact version, commit hash, or edition the claim concerns.

## 8. Conflicting sources

When sources disagree:

1. Check whether they are really talking about the same thing (scope, definition, period, version).
2. Trace each to its origin and method; prefer the one closer to the data and with transparent methods.
3. Check dates; the newer may supersede the older, or the older may be the original and the newer a garbled copy.
4. If it remains unresolved, report **both**, with your assessment of which is better supported and why, and mark the claim Disputed. Do not average, and do not silently choose.

## 9. False premises and unanswerable questions

- If the question rests on a false or unproven premise, say so first, show the evidence, then answer the corrected question.
- If the question cannot be answered with the access you have, say exactly what is missing and what would unblock it, then give the best partial answer clearly labeled as partial.
- Do not manufacture an answer to fill the shape of the question.

## 10. Red-team pass

Before delivering at Survey tier or above, spend a deliberate pass attacking your own conclusion:

- State the strongest case against it, as its best advocate would.
- Search specifically for evidence that would contradict the headline finding.
- Ask what an informed skeptic would check first, and check it.
- Re-read the scope words of each claim in the report against the evidence you actually have.
- For each remaining weak spot, either shore it up, downgrade the confidence, or move it to "limits and open questions".

Report the outcome of the red-team pass in one or two lines, even when it found nothing; that tells the reader the conclusion survived an attack.
