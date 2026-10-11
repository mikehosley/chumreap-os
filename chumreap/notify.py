"""Notification dispatcher. Channel-agnostic: the router decides WHAT goes WHERE.

Channels: log (working), whatsapp (stub — needs Cloud API credentials),
telegram (stub — needs bot token), email (stub — needs SMTP).
Green-tier activity data only on Meta pipes. Clinical data never enters.
"""
import json, os

HERE = os.path.dirname(__file__)
ROUTES_FILE = os.path.join(os.path.dirname(HERE), "routes.json")

# event action -> list of (channel, recipient)
DEFAULT_ROUTES = {
    "checkin": [("log", "console")],
    "gym": [("log", "console")],
    "order_food": [("log", "console")],
    "order_grocery": [("log", "console")],
}

def load_routes():
    if os.path.exists(ROUTES_FILE):
        return json.load(open(ROUTES_FILE))
    return DEFAULT_ROUTES

HUMAN_LABELS = {
    "checkin": "is home",
    "gym": "is back from the gym",
    "order_food": "ordered dinner",
    "order_grocery": "ordered groceries",
}

def dispatch(action, kit, category="green"):
    """Route a fired event to its configured recipients. Returns delivery log."""
    if category == "red":
        raise ValueError("red-tier events must never enter the dispatcher")
    routes = load_routes()
    deliveries = []
    label = HUMAN_LABELS.get(action, action)
    for channel, recipient in routes.get(action, [("log", "console")]):
        if channel in ("whatsapp", "messenger") and category != "green":
            deliveries.append({"channel": channel, "recipient": recipient,
                               "status": "blocked", "reason": "non-green tier barred from Meta pipes"})
            continue
        fn = {"log": _send_log, "whatsapp": _send_whatsapp,
              "telegram": _send_telegram, "email": _send_email}.get(channel, _send_log)
        deliveries.append(fn(recipient, f"{kit} {label}", category))
    return deliveries

def _send_log(recipient, text, category):
    print(f"[notify/log] {text} (category={category})", flush=True)
    return {"channel": "log", "recipient": recipient, "status": "sent"}

def _send_whatsapp(recipient, text, category):
    # TODO: WhatsApp Cloud API — needs WHATSAPP_TOKEN, WHATSAPP_PHONE_ID env vars
    # and a Meta-approved template for proactive messages.
    print(f"[notify/whatsapp:STUB] to={recipient} text={text!r}", flush=True)
    return {"channel": "whatsapp", "recipient": recipient, "status": "stubbed",
            "todo": "set WHATSAPP_TOKEN + WHATSAPP_PHONE_ID, get template approved"}

def _send_telegram(recipient, text, category):
    # TODO: Telegram Bot API — needs TELEGRAM_BOT_TOKEN env var.
    print(f"[notify/telegram:STUB] to={recipient} text={text!r}", flush=True)
    return {"channel": "telegram", "recipient": recipient, "status": "stubbed",
            "todo": "set TELEGRAM_BOT_TOKEN"}

def _send_email(recipient, text, category):
    # TODO: SMTP — needs SMTP_* env vars.
    print(f"[notify/email:STUB] to={recipient} text={text!r}", flush=True)
    return {"channel": "email", "recipient": recipient, "status": "stubbed",
            "todo": "set SMTP_HOST/USER/PASS"}
