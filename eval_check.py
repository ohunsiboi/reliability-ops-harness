"""
ITERATION 3: upgraded from 6C's single-criterion eval (does the memo contain
the right MTBF and cost figures?) to a multi-criterion rubric, plus a
cost-tier GUARDRAIL that flags high-cost memos for a higher approval tier
instead of routing every memo through the same single approval step.

Usage: python3 eval_check.py draft_memo.txt truth.json
Exit code 0 = full pass, 1 = fails one or more rubric criteria.
"""
import json, sys, re

GUARDRAIL_THRESHOLD = 40000  # above this, memo requires VP-tier approval, not just manager

def rubric_check(memo_text, truth):
    mtbf_str = str(truth["mtbf"])
    cost_str = f'{truth["totalCost"]:,}'

    checks = {
        "mtbf_figure_present": mtbf_str in memo_text,
        "cost_figure_present": (f'${cost_str}' in memo_text) or (cost_str in memo_text),
        "asset_identified": truth.get("asset_id", "") in memo_text or truth.get("name", "") in memo_text,
        "has_recommendation": bool(re.search(r"\b(request|recommend|approv|procure)\w*\b", memo_text, re.I)),
        "reasonable_length": 40 <= len(memo_text.split()) <= 200,
    }
    passed = all(checks.values())

    guardrail_tier = "VP_APPROVAL_REQUIRED" if (truth.get("totalCost") or 0) > GUARDRAIL_THRESHOLD else "MANAGER_APPROVAL"

    return {
        "checks": checks,
        "rubric_passed": passed,
        "guardrail_tier": guardrail_tier,
        "guardrail_threshold": GUARDRAIL_THRESHOLD
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 eval_check.py <draft_memo.txt> <truth.json>", file=sys.stderr)
        sys.exit(2)
    memo_text = open(sys.argv[1]).read()
    truth = json.load(open(sys.argv[2]))
    result = rubric_check(memo_text, truth)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["rubric_passed"] else 1)
