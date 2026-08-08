# 7A Capstone — Organizational Pitch (Segment 4 content)

## The problem, in leadership terms
Reliability engineers currently spend time on two things that don't need a
human: (1) pulling failure data and doing the MTBF/MTTR/cost math by hand or
in a spreadsheet, and (2) writing the justification memo to get spare-parts
budget approved. Neither step requires engineering judgment — the judgment is
in deciding whether the number is big enough to escalate, and in owning the
final "yes, send this" call. This system automates the first two and keeps a
human on the third.

## ROI — defensible estimate, not a guess
- **Time per justification memo today:** roughly 30–45 minutes (pull the log,
  do the math, draft the memo, format it for a manager) — a reasonable estimate
  for one asset's worth of ad hoc analysis and writing.
- **Time with this harness:** under 2 minutes of engineer time — reviewing the
  loop's output and typing "yes" or "no" at each escalation point. The
  calculation, drafting, and rubric checking run unattended.
- **At even 10 justification memos a month** across a facility with multiple
  asset lines, that's roughly **5–7 hours/month** returned to an engineer's
  actual job — inspection, root-cause work, PM planning — instead of
  spreadsheet-and-memo formatting.
- **Secondary ROI:** the guardrail tier means high-cost requests (>$40k) never
  get status quo manager-level sign-off by default — closing a governance gap
  that currently depends on someone remembering to escalate, not a system
  rule.
- These are conservative, hour-based estimates suitable for a first
  conversation with leadership — real validation would come from timing
  actual engineers on the current manual process for one quarter.

## Risk & implications — the stress test
- **Failure mode already demonstrated in 6C and reproducible here:** an LLM
  asked to compute MTBF/cost in its own reasoning instead of through the tool
  can silently produce numbers that look confident but don't match the
  verified source. The eval catches this — but only because it's independent
  of the model's own claim. If the eval script itself had a bug, that
  protection disappears silently. **Mitigation:** the eval script is small,
  unit-testable, and version-controlled separately from the agent's prompt,
  specifically so it can be audited on its own.
- **Guardrail threshold is a hardcoded number ($40,000).** In a real
  deployment this needs to be a config value owned by finance/ops, not a
  constant in a Python file an engineer can quietly edit. As built, nothing
  stops someone from changing that threshold to avoid VP-tier approval.
  **Mitigation:** the threshold should live outside the agent's own writable
  scope — e.g., a signed config or a value pulled from a system the requesting
  engineer doesn't have write access to.
- **The database is currently a static seed, not a live feed.** In production
  this would need to pull from a real CMMS/EAM system (e.g., SAP PM, Maximo),
  which means new integration risk and new failure modes (stale data, schema
  drift) that this build doesn't yet handle or guard against.
- **Who gets disrupted:** this doesn't remove headcount — it removes a
  specific low-judgment task from reliability engineers' week. The people
  most affected are actually **managers and VPs**, who will start receiving
  more consistently-formatted, consistently-justified requests more
  frequently, and will need to trust the harness's math rather than
  re-deriving it themselves. That trust has to be earned with visible
  guardrails (like the tier system here), not assumed.
- **What's still missing for a real deployment:** an audit log of every
  approval decision (who approved what, when, at what tier), a way to
  override or contest an auto-generated memo before it reaches a manager, and
  monitoring on the eval script itself so a change to its pass criteria is
  visible and reviewed, not silent.
