"""Chumreap OS — demo server. The cocktail-party loop:
scan QR -> action page -> tap -> event in ledger -> notification dispatched -> admin sees it live.
"""
import os, time, json
from flask import Flask, request, jsonify, Response
from chumreap.ledger import init_db, log_event, recent_events, last_id
from chumreap.notify import dispatch

app = Flask(__name__)
init_db()

# kit context -> the action page behind the QR code
CONTEXTS = {
    "door":   {"emoji": "🚪", "title": "I'm back",   "action": "checkin",
               "hint": "Tap when you're home.", "btn": "✅ I'm back"},
    "fridge": {"emoji": "🥛", "title": "Groceries", "action": "order_grocery",
               "hint": "Milk, eggs, bread — 30 seconds.", "btn": "🛒 Order groceries"},
    "menu":   {"emoji": "🍜", "title": "Food menu", "action": "order_food",
               "hint": "Tonight's dinner, no front desk.", "btn": "🍜 Order dinner"},
    "gym":    {"emoji": "🏋️", "title": "Gym",       "action": "gym",
               "hint": "Log the workout. Streaks live here.", "btn": "🏋️ Back from gym"},
}

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{emoji} {title} — Chumreap</title>
<style>body{{font-family:-apple-system,sans-serif;background:#f4f1ea;margin:0;padding:32px 20px;text-align:center}}
.card{{max-width:380px;margin:0 auto;background:#fff;border:3px solid #1f1b16;border-radius:20px;padding:28px}}
.emoji{{font-size:56px}}h1{{margin:12px 0 6px}}.hint{{color:#8a8175;margin-bottom:20px}}
button{{font-size:20px;font-weight:700;background:#1f1b16;color:#fff;border:none;border-radius:14px;padding:18px 28px;cursor:pointer;width:100%}}
.done{{display:none;background:#4c7a4f;color:#fff;border-radius:14px;padding:18px;margin-top:16px;font-weight:700}}
.kit{{margin-top:14px;font-size:12px;color:#8a8175}}</style></head><body>
<div class="card"><div class="emoji">{emoji}</div><h1>{title}</h1>
<div class="hint">{hint}</div>
<button onclick="fire()">{btn}</button>
<div class="done" id="done">✓ Logged — the house knows.</div>
<div class="kit">{kit} · scanned just now</div></div>
<script>function fire(){{fetch("/api/event",{{method:"POST",
headers:{{"Content-Type":"application/json"}},
body:JSON.stringify({{kit:"{kit}",ctx:"{ctx}",action:"{action}"}})}})
.then(r=>r.json()).then(d=>{{document.getElementById("done").style.display="block";}});}}</script>
</body></html>"""

ADMIN = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reception — Chumreap OS (live)</title>
<style>body{font-family:-apple-system,sans-serif;background:#f4f1ea;margin:0}
.bar{background:#1f1b16;color:#f4f1ea;padding:14px 20px;display:flex;justify-content:space-between;align-items:center}
.live{color:#7fd67f;font-size:13px}#log{max-width:720px;margin:0 auto;padding:16px}
.ev{background:#fff;border:2px solid #e2dccf;border-radius:12px;padding:12px 14px;margin-bottom:10px;font-size:15px}
.ev .t{color:#8a8175;font-size:12px}.ev .d{font-size:12px;color:#8a8175;margin-top:4px}</style></head><body>
<div class="bar"><b>🖥 Reception — live event ledger</b><span class="live">● LIVE</span></div>
<div id="log"></div>
<script>const log=document.getElementById("log");let last=0;
function fmt(ts){return new Date(ts*1000).toLocaleTimeString();}
function render(e){const d=document.createElement("div");d.className="ev";
d.innerHTML=`<b>${e.kit}</b> — ${e.action} <span class="t">${fmt(e.ts)} · ${e.ctx} · ${e.category}</span>
<div class="d">notified: ${(e.detail.notify||[]).map(n=>n.channel+":"+n.status).join(", ")||"—"}</div>`;
log.prepend(d);}
setInterval(()=>{fetch("/api/events?since="+last).then(r=>r.json()).then(a=>{a.reverse().forEach(e=>{render(e);last=Math.max(last,e.id);});});},1500);
fetch("/api/events").then(r=>r.json()).then(a=>{a.forEach(e=>{render(e);last=Math.max(last,e.id);});});</script>
</body></html>"""

@app.route("/k/<kit>/<ctx>")
def resolve(kit, ctx):
    c = CONTEXTS.get(ctx)
    if not c:
        return "unknown code", 404
    return PAGE.format(kit=kit, ctx=ctx, **c)

@app.route("/api/event", methods=["POST"])
def event():
    d = request.json or {}
    kit, ctx = d.get("kit", "?"), d.get("ctx", "?")
    action = d.get("action") or CONTEXTS.get(ctx, {}).get("action", "tap")
    category = d.get("category", "green")
    try:
        deliveries = dispatch(action, kit, category)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    ev = log_event(kit, ctx, action, category, {"notify": deliveries})
    return jsonify(ev)

@app.route("/api/events")
def events():
    since = int(request.args.get("since", 0))
    evs = recent_events(200)
    return jsonify([e for e in evs if e["id"] > since])

@app.route("/admin")
def admin():
    return ADMIN

@app.route("/api/stream")
def stream():
    def gen():
        seen = last_id()
        while True:
            evs = [e for e in recent_events(50) if e["id"] > seen]
            for e in evs:
                seen = max(seen, e["id"])
                yield f"data: {json.dumps(e)}\n\n"
            time.sleep(2)
    return Response(gen(), mimetype="text/event-stream")

@app.route("/")
def index():
    return jsonify({"ok": True, "service": "chumreap-os demo",
                    "try": "/k/DEMO-A/door", "admin": "/admin"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
