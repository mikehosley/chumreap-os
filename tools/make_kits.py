"""Regenerate the printable demo QR kits against a live BASE_URL.

Usage: BASE_URL=http://192.168.1.50:5000 python tools/make_kits.py
Writes: ../kits/chumreap-demo-kits.html (print it, cut it, envelope it)
"""
import qrcode, io, base64, os

BASE = os.environ.get("BASE_URL", "http://localhost:5000").rstrip("/")
KITS = ["DEMO-A", "DEMO-B", "DEMO-C", "DEMO-D", "DEMO-E"]
CODES = [("door", "FRONT DOOR", "I'm back", "Tap in when you're home."),
         ("fridge", "REFRIGERATOR", "Groceries", "Milk, eggs, bread — 30 seconds."),
         ("menu", "KITCHEN TABLE", "Food menu", "Order dinner. No front desk needed."),
         ("gym", "GYM BAG", "Back from gym", "Log the workout. Streaks live here.")]

def qr_b64(payload):
    qr = qrcode.QRCode(box_size=5, border=2)
    qr.add_data(payload); qr.make(fit=True)
    buf = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

pages = []
for k in KITS:
    cards = "".join(
        f'<div class="card"><div class="ct"> {t}</div>'
        f'<img src="{qr_b64(f"{BASE}/k/{k}/{c}")}"><div class="cn">{n}</div>'
        f'<div class="cd">{d}</div></div>' for c, t, n, d in CODES)
    pages.append(f'''<div class="kit"><div class="kh">🔳 CHUMREAP OS — KIT {k[-1]}
<span class="tag">{k}</span></div><div class="grid">{cards}</div>
<div class="instr"><b>2-minute setup:</b> 1. Stick each code where it belongs.
2. Point your phone camera at any code — no app, no login.
3. Tell us where notifications go: <b>WhatsApp / Telegram / email</b>, your choice per event.</div></div>''')

html = ('''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Chumreap OS — Demo Kits</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:-apple-system,sans-serif;color:#2b2620}
.kit{page-break-after:always;padding:36px;max-width:800px;margin:0 auto}
.kh{font-size:22px;font-weight:800;border-bottom:3px solid #1f1b16;padding-bottom:10px;margin-bottom:18px}
.tag{font-size:13px;background:#c8a24b;padding:3px 10px;border-radius:12px;margin-left:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{border:2px solid #1f1b16;border-radius:14px;padding:16px;text-align:center}
.ct{font-size:11px;font-weight:700;letter-spacing:1px;color:#8a8175}
.card img{width:150px;height:150px;margin:10px auto;display:block}
.cn{font-size:18px;font-weight:700}.cd{font-size:13px;color:#8a8175;margin-top:4px}
.instr{margin-top:18px;background:#f4f1ea;border-radius:12px;padding:16px;font-size:14px;line-height:1.7}</style>
</head><body>''' + "".join(pages) + "</body></html>")

os.makedirs("kits", exist_ok=True)
open("kits/chumreap-demo-kits.html", "w").write(html)
print("wrote kits/chumreap-demo-kits.html for BASE_URL =", BASE)
