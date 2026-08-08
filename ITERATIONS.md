# Iterations — 6C to 7A Capstone (Path A)

Three meaningful iterations, each a real capability change, not a cosmetic pass.

## Iteration 1 — MCP server + real multi-asset data (was: one hardcoded JSON file)
**6C:** `failure_log.json` — one asset, one file, no query surface. Claude Code
read it directly with no tool boundary around it.
**7A:** `assets.db` — a real SQLite database with 4 assets (12 failure records),
queried through a real MCP server (`mcp_server.py`) exposing three tools:
`list_assets`, `get_asset_metrics`, `get_failure_log`. Verified working via a
live JSON-RPC handshake and an actual tool call over stdio (not just "the
functions run in Python" — the protocol layer itself was tested).
**Why it matters:** this is the difference between "the agent reads a file you
handed it" and "the agent has a queryable interface into a real data source,"
which is the entire point of MCP as a harness element.

## Iteration 2 — Agent loop (was: a single calculate → draft → approve pass)
**6C:** one asset in, one memo out, no decision-making about *whether* to act.
**7A:** the workflow in `CLAUDE.md` has Claude Code loop across every asset
returned by `list_assets()`, querying each one's verified cost and deciding
whether it clears a $15,000 escalation threshold. Assets below threshold are
explicitly skipped (a real decision, narrated live); assets above threshold
get a full draft → eval → approval cycle. With this dataset that means
COMPRESSOR-3 ($43,200) and PUMP-1 ($17,000) get escalated, while CHILLER-4
($5,400) and CONVEYOR-2 ($1,200) get skipped — a genuine plan-act-observe
cycle with a visible branch, not a fixed script.

## Iteration 3 — Deeper eval + cost-tier guardrail (was: two-field number match)
**6C:** the eval checked exactly two things — does the memo contain the right
MTBF and the right cost figure.
**7A:** `eval_check.py` checks five criteria (MTBF present, cost present,
asset correctly identified, a recommendation is actually made, length is in a
professional range) and adds a **guardrail**: any memo whose verified cost
exceeds $40,000 is automatically tagged `VP_APPROVAL_REQUIRED` instead of the
standard `MANAGER_APPROVAL` tier — a scope-limit guardrail that changes what
the human-in-the-loop checkpoint actually asks for, not just whether one exists.

## What this demonstrates together
None of these three iterations is meaningful alone — the loop only matters
because there's real multi-asset data to loop over (Iteration 1), the eval
only matters because the loop produces multiple memos that need independent
checking (Iteration 2), and the guardrail tier only matters because the eval
already knows the verified cost to route on (Iteration 3). They compound.
