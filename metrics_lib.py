"""
Ground-truth reliability math -- shared by the MCP server and the eval script.
Unchanged from 6C: this is deliberately the ONE place this calculation exists,
imported everywhere else needs it, so there is never a second implementation
to drift out of sync.
"""

def compute_metrics(failures, dollars_per_hour):
    """failures: list of {"runHours": float, "repairHours": float}"""
    n = len(failures)
    if n == 0:
        return {"mtbf": None, "mttr": None, "availability": None, "totalCost": None}
    total_run = sum(f["runHours"] for f in failures)
    total_repair = sum(f["repairHours"] for f in failures)
    mtbf = total_run / n
    mttr = total_repair / n
    availability = mtbf / (mtbf + mttr)
    total_cost = total_repair * dollars_per_hour
    return {
        "mtbf": round(mtbf, 1),
        "mttr": round(mttr, 1),
        "availability": round(availability * 1000) / 10,
        "totalCost": round(total_cost)
    }
