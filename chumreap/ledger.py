"""Append-only event ledger (SQLite). The compliance exhibit."""
import sqlite3, time, json, os

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ledger.db")

def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = _conn()
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL NOT NULL,
        kit TEXT NOT NULL,
        ctx TEXT NOT NULL,
        action TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'green',
        detail TEXT DEFAULT '{}'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS kits (
        kit TEXT PRIMARY KEY,
        label TEXT,
        active INTEGER DEFAULT 1
    )""")
    for k in ["DEMO-A", "DEMO-B", "DEMO-C", "DEMO-D", "DEMO-E"]:
        c.execute("INSERT OR IGNORE INTO kits (kit, label) VALUES (?, ?)", (k, f"Apartment {k[-1]}"))
    c.commit()
    c.close()

def _conn():
    return sqlite3.connect(DB, timeout=10.0)

def log_event(kit, ctx, action, category="green", detail=None):
    c = _conn()
    ts = time.time()
    cur = c.execute("INSERT INTO events (ts, kit, ctx, action, category, detail) VALUES (?,?,?,?,?,?)",
                    (ts, kit, ctx, action, category, json.dumps(detail or {})))
    eid = cur.lastrowid
    c.commit()
    c.close()
    return {"id": eid, "ts": ts, "kit": kit, "ctx": ctx, "action": action,
            "category": category, "detail": detail or {}}

def recent_events(limit=50):
    c = _conn()
    rows = c.execute(
        "SELECT id, ts, kit, ctx, action, category, detail FROM events ORDER BY id DESC LIMIT ?",
        (limit,)).fetchall()
    c.close()
    return [{"id": r[0], "ts": r[1], "kit": r[2], "ctx": r[3], "action": r[4],
             "category": r[5], "detail": json.loads(r[6])} for r in rows]

def last_id():
    c = _conn()
    r = c.execute("SELECT MAX(id) FROM events").fetchone()
    c.close()
    return r[0] or 0
