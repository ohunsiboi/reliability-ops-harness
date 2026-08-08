# Reliability Ops Harness — Capstone (7A, Path A extending 6C)

## What changed since 6C
6C handled ONE asset from ONE hardcoded JSON file, with a single-criterion eval
and a single approval step. This build queries a real multi-asset database
through a real MCP server, loops across assets to decide which ones warrant
escalation, applies a deeper rubric eval, and routes approval through one of
two tiers depending on cost. See ITERATIONS.md for the full before/after.

## Tools available (via the reliability-db MCP server)
- `list_assets()` — every asset in the database
- `get_asset_metrics(asset_id)` — the ONLY source of truth for MTBF/MTTR/availability/cost for one asset. Never estimate these yourself.
- `get_failure_log(asset_id)` — raw failure rows for one asset, if needed

## The escalation loop (agent loop element)
When the user asks you to review assets for spare-parts justification:

1. Call `list_assets()` to get every asset.
2. For each asset, in order:
   a. Call `get_asset_metrics(asset_id)` to get verified numbers.
   b. If `totalCost < 15000` (the escalation threshold): **skip this asset** — say
      so briefly, don't draft a memo for it, and move to the next one. This is
      a real decision point, not a formality — narrate why you're skipping it.
   c. If `totalCost >= 15000`: draft a 3–4 sentence justification memo citing
      the asset name/id and the exact verified figures. Save it to
      `draft_memo_<asset_id>.txt`.
   d. Run `python3 eval_check.py draft_memo_<asset_id>.txt truth_<asset_id>.json`
      (first write `truth_<asset_id>.json` from the tool's own output) to get
      the rubric result AND the guardrail tier.
   e. Report the rubric result to the user.
   f. If `rubric_passed` is false: say which check failed, redraft once
      addressing it, and re-run the eval. Do not loop more than once per asset.
   g. If `rubric_passed` is true: check `guardrail_tier`.
      - `MANAGER_APPROVAL`: ask "Approve this memo for manager sign-off? (yes/no)"
      - `VP_APPROVAL_REQUIRED`: say explicitly that this exceeds the $40,000
        guardrail threshold and requires VP-tier approval, then ask
        "Approve this memo for VP-tier sign-off? (yes/no)"
      Do NOT create `approved_memo_<asset_id>.txt` until the user says yes.
3. After all assets are checked, summarize: how many were skipped, how many
   were escalated, and at which approval tier each escalated one landed.

## If asked to demonstrate the 6C failure mode for comparison
Skip the tool for one asset — calculate its metrics yourself, in your own
reasoning, from `get_failure_log(asset_id)` instead of `get_asset_metrics`.
Draft a memo from your own numbers, then still run the real eval against the
real tool's truth file to show whether your mental math drifted.
