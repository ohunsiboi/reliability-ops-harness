"""
Quick way to actually SEE the database contents in the terminal --
useful for showing the data on screen during the video, since assets.db
itself isn't something you can double-click open.
Usage: python3 view_db.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "assets.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=== ASSETS ===")
for row in cur.execute("SELECT asset_id, name, dollars_per_hour FROM assets"):
    print(f"{row[0]:15s} {row[1]:20s} ${row[2]:.0f}/hr downtime cost")

print("\n=== FAILURE LOG ===")
for row in cur.execute("SELECT asset_id, run_hours, repair_hours FROM failures ORDER BY asset_id"):
    print(f"{row[0]:15s} ran {row[1]:6.1f} hrs, repair took {row[2]:5.1f} hrs")

conn.close()
