"""
ITERATION 1 (data + MCP): replaces the single hardcoded failure_log.json from 6C
with a real SQLite database covering multiple assets -- the kind of structured
internal data source an MCP server is actually meant to expose.
Run once: python3 setup_db.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "assets.db")

ASSETS = [
    # asset_id,     name,                dollars_per_hour
    ("PUMP-1",      "Feed Pump 1",       850),
    ("CONVEYOR-2",  "Belt Conveyor 2",   400),
    ("COMPRESSOR-3","Air Compressor 3",  1200),
    ("CHILLER-4",   "Process Chiller 4", 600),
]

FAILURES = {
    "PUMP-1":       [(420, 3.5), (280, 6), (510, 2), (190, 8.5)],
    "CONVEYOR-2":   [(600, 1), (720, 1.5), (500, 0.5)],
    "COMPRESSOR-3": [(150, 12), (200, 9), (90, 15)],
    "CHILLER-4":    [(300, 4), (250, 5)],
}

def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS failures")
    cur.execute("DROP TABLE IF EXISTS assets")
    cur.execute("""CREATE TABLE assets (
        asset_id TEXT PRIMARY KEY, name TEXT, dollars_per_hour REAL)""")
    cur.execute("""CREATE TABLE failures (
        id INTEGER PRIMARY KEY AUTOINCREMENT, asset_id TEXT,
        run_hours REAL, repair_hours REAL,
        FOREIGN KEY(asset_id) REFERENCES assets(asset_id))""")

    for asset_id, name, dph in ASSETS:
        cur.execute("INSERT INTO assets VALUES (?,?,?)", (asset_id, name, dph))
    for asset_id, rows in FAILURES.items():
        for run_hours, repair_hours in rows:
            cur.execute("INSERT INTO failures (asset_id, run_hours, repair_hours) VALUES (?,?,?)",
                        (asset_id, run_hours, repair_hours))
    conn.commit()
    conn.close()
    print(f"Created {DB_PATH} with {len(ASSETS)} assets and "
          f"{sum(len(v) for v in FAILURES.values())} failure records.")

if __name__ == "__main__":
    main()
