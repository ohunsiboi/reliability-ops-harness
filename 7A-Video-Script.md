# 7A Capstone Video Transcript
### "Reliability Ops Harness — Multi-Asset Escalation System"
Target length: 10–15 minutes. Four segments per the brief. Bracketed notes are
stage directions. ``` code blocks ``` are exact things to paste into the
Claude Code terminal — nowhere else.

## Before you hit record
- Run the one-time setup from RUN_INSTRUCTIONS.md (install mcp, run setup_db.py,
  `claude mcp add`, start `claude`, confirm with `/mcp`) BEFORE recording.
- Have ITERATIONS.md and 7A-Documentation.md open in another window to
  reference during Segments 3 and 4.

---

### Segment 1 — Reintroduce + declare path — [0:00–0:30]
**[Face on camera]**

Hey, I'm [Your Name], reliability engineer. This is my capstone — **Path A**,
extending the Reliability Ops Harness I built in 6C. My 6C build worked, but
it was intentionally small: one asset, one file, one pass. This week I scaled
it into something closer to what an actual multi-asset facility would need.

### Segment 2 — Live demo, end to end — [0:30–4:30]
**[Screen share — terminal, Claude Code already connected to the reliability-db MCP server]**

Let me run the whole thing. This system now covers four real equipment
assets in a real database, not one hardcoded file.

**[Paste this into Claude Code:]**
```
Review every asset for spare-parts justification, following the workflow in CLAUDE.md exactly.
```

*(Narrate as it runs, don't read code — narrate what it's doing for a human:)*

Watch it start by listing every asset from the database — that's a real MCP
tool call, `list_assets`, not a fixed list in a prompt. Now it's checking each
one's verified cost. This one's below the $15,000 escalation threshold, so
it's skipping it — that's a real decision, not a formality. Now it's found one
above threshold, drafting a memo, running the eval... and here's the rubric
result, five criteria this time, not two.

**[Approve/decline prompts as they come up — narrate the tier difference:]**

Notice this one's asking for manager-level approval, but this other one —
because it crossed $40,000 — is explicitly asking for VP-tier approval
instead. That's the guardrail routing differently based on the real number,
not a fixed approval step.

**[Let it finish all four assets, then:]**

And there's the summary — how many assets got skipped, how many escalated,
and at which tier. That's the whole system, end to end, on real multi-asset
data.

### Segment 3 — Scaling / robustness vs 6C — [4:30–8:30]
**[Screen share — ITERATIONS.md on screen]**

Here's specifically what's bigger than 6C, in three iterations.

**Iteration one — real data plus a real MCP server.** 6C read one JSON file
directly. This build has an actual SQLite database with four assets, and a
real MCP server sitting in front of it — `list_assets`, `get_asset_metrics`,
`get_failure_log`. I didn't just claim this works — I tested the protocol
layer directly with a JSON-RPC handshake before ever touching Claude Code,
confirmed the tool schemas, and confirmed a real tool call returns the right
numbers. **[show `/mcp` output confirming 3 connected tools]**

**Iteration two — an actual agent loop.** 6C was one asset in, one memo out,
no decision-making. This build loops across every asset, checks its real
cost against a threshold, and branches — skip or escalate — for each one.
You just watched that happen live: two assets skipped, two escalated. That's
plan, act, observe, repeat, not a single pass.

**Iteration three — a deeper eval and a real guardrail.** 6C's eval checked
two things: is the MTBF right, is the cost right. This eval checks five —
adds asset identification, whether a recommendation is actually made, and a
length sanity check. And it feeds a guardrail: cross $40,000 and the approval
tier itself changes, from manager to VP. That's not a bigger checklist for
its own sake — it's routing a real decision differently based on real risk.

**[Say clearly:]** None of these three matter alone. The loop only matters
because there's real data to loop over. The eval only matters because the
loop can produce more than one memo needing independent checking. The
guardrail only matters because the eval already knows the verified cost to
route on. They compound into something more robust than any one of them
would be by itself.

### Segment 4 — Organizational pitch: ROI, risk, implications — [8:30–13:00]
**[Face on camera, or screen share on 7A-Documentation.md as reference]**

Now let me pitch this to leadership, and then stress-test my own pitch.

**The problem:** reliability engineers spend real time on two things that
don't need engineering judgment — pulling failure data and doing the math,
and writing the justification memo. The judgment is only in deciding whether
a number is big enough to escalate, and in the final approval. This system
automates the first two and keeps a human on the third.

**The ROI:** a justification memo today takes roughly 30 to 45 minutes of an
engineer's time — pulling the log, doing the math by hand or in a
spreadsheet, drafting and formatting the memo. With this harness, that drops
to under two minutes of actual engineer time: reviewing the loop's output and
approving or declining at each escalation point. At even ten memos a month
across a facility with multiple asset lines, that's five to seven hours a
month back for actual reliability work instead of spreadsheet formatting.
These are conservative, hour-based estimates — a real rollout would validate
them by timing engineers on the current manual process for a quarter first.

**Now the stress test — where this could actually fail.**

First: the eval is what catches drift between what the model claims and
what's actually true — I demonstrated that failure mode back in 6C. But the
eval script itself is unaudited beyond what I've tested here. If it had a
bug, that protection fails silently. It needs to be small, version-controlled,
and reviewed on its own, separately from the agent's prompt.

Second: that $40,000 guardrail threshold is a hardcoded number in a Python
file right now. Nothing stops someone from quietly editing it to avoid
VP-tier approval. In a real deployment, that threshold needs to live outside
the requesting engineer's own write access — a signed config, or a value
pulled from a system they don't control.

Third: this database is a static seed today, not a live feed from a real
CMMS system. Wiring it to something like SAP PM or Maximo is new integration
risk this build doesn't handle yet — stale data, schema drift, all of that.

And who actually gets disrupted: not reliability engineers' headcount — this
removes a low-judgment task from their week, not their job. The bigger shift
is on managers and VPs, who'll start seeing more consistently-formatted
requests, more often, and will need to trust the harness's numbers rather
than re-deriving them by hand. That trust has to be earned with visible
guardrails like the tier system here — not assumed.

What's still missing before this is really production-ready: an audit log of
every approval decision, a way to contest or override a memo before it
reaches a manager, and monitoring on the eval script itself so a change to
its criteria is visible, not silent.

Thanks for watching.

---

## Delivery notes
- Segment lengths above total ~12–13 minutes with narration — trim Segment 4
  slightly if you're running long; it has the most cuttable material without
  losing required content (ROI number + at least 2 risks + who's disrupted
  covers the rubric).
- The live demo (Segment 2) is unscripted in outcome — the loop's actual skip/
  escalate decisions depend on the real data, which you already verified
  produces two skips and two escalations (one at each guardrail tier). If you
  changed the database, re-check this before recording.
- Don't narrate code syntax anywhere — narrate what the system is doing for a
  human, per the brief's explicit instruction.
