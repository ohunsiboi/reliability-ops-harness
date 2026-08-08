# How to run this (setup + exact prompts for recording)

## One-time setup
1. Put all files in one folder: `CLAUDE.md`, `metrics_lib.py`, `mcp_server.py`,
   `eval_check.py`, `setup_db.py`, `ITERATIONS.md`, `7A-Documentation.md`,
   and a `data/` subfolder (created by step 3).
2. Install the MCP SDK: `pip install mcp`
3. Build the database: `python3 setup_db.py`
   (You should see: "Created .../assets.db with 4 assets and 12 failure records.")
4. Register the MCP server with Claude Code, from inside this folder:
   ```
   claude mcp add reliability-db -- python3 mcp_server.py
   ```
5. Start Claude Code: `claude`
6. Confirm the server connected: type `/mcp` inside Claude Code and check
   `reliability-db` shows as connected with 3 tools.

## For the video — Segment 2 (live demo)
Paste this prompt:
```
Review every asset for spare-parts justification, following the workflow in CLAUDE.md exactly.
```
Narrate what's happening as it runs: the tool calls (list_assets, then
get_asset_metrics per asset), the skip decisions on low-cost assets, the
drafted memos on high-cost ones, the eval output, and the two different
approval-tier questions (MANAGER_APPROVAL vs VP_APPROVAL_REQUIRED). Approve or
decline each as prompted — type `yes` or `no`.

## For the video — Segment 3 (scaling vs 6C)
Open `ITERATIONS.md` on screen and walk through the three iterations while
pointing at the corresponding evidence on screen (the MCP tool list from
`/mcp`, the skip/escalate decisions from the loop, the 5-criterion eval output
and guardrail tier from the run you just did).

## For the video — Segment 4 (org pitch)
`7A-Documentation.md` has the ROI numbers and risk analysis written out —
use it as your talking points rather than reading it verbatim on screen.
