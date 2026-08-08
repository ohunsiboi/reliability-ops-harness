"""
ITERATION 1: a real MCP server exposing the reliability database to Claude Code /
Claude Desktop for conversational, multi-asset query -- replacing 6C's single
hardcoded failure_log.json with a proper structured data source and a real
tool-use surface an agent can explore, not just one fixed file it's handed.

Run standalone to sanity-check: python3 mcp_server.py
Register with Claude Code: claude mcp add reliability-db -- python3 mcp_server.py
"""
import sqlite3, os
from mcp.server.mcpserver import MCPServer
from metrics_lib import compute_metrics

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "assets.db")

mcp = MCPServer("reliability-db", description="Query equipment reliability data (MTBF/MTTR/cost) across assets.")

def _conn():
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def list_assets() -> list[dict]:
    """List every asset in the reliability database with its id, name, and hourly downtime cost rate."""
    conn = _conn()
    rows = conn.execute("SELECT asset_id, name, dollars_per_hour FROM assets").fetchall()
    conn.close()
    return [{"asset_id": r[0], "name": r[1], "dollars_per_hour": r[2]} for r in rows]

@mcp.tool()
def get_failure_log(asset_id: str) -> list[dict]:
    """Get the raw failure log (run hours, repair hours) for one asset by asset_id."""
    conn = _conn()
    rows = conn.execute(
        "SELECT run_hours, repair_hours FROM failures WHERE asset_id = ?", (asset_id,)
    ).fetchall()
    conn.close()
    return [{"runHours": r[0], "repairHours": r[1]} for r in rows]

@mcp.tool()
def get_asset_metrics(asset_id: str) -> dict:
    """Compute verified MTBF, MTTR, availability, and total downtime cost for one asset by asset_id.
    This is the ONLY source of truth for these numbers -- never estimate them, always call this."""
    conn = _conn()
    asset = conn.execute(
        "SELECT name, dollars_per_hour FROM assets WHERE asset_id = ?", (asset_id,)
    ).fetchone()
    if asset is None:
        conn.close()
        return {"error": f"No asset with id {asset_id}"}
    name, dph = asset
    rows = conn.execute(
        "SELECT run_hours, repair_hours FROM failures WHERE asset_id = ?", (asset_id,)
    ).fetchall()
    conn.close()
    failures = [{"runHours": r[0], "repairHours": r[1]} for r in rows]
    metrics = compute_metrics(failures, dph)
    metrics["asset_id"] = asset_id
    metrics["name"] = name
    return metrics

if __name__ == "__main__":
    mcp.run()
