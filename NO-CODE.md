# No-code family mode

Run the Chumreap loop without running any server. The family writes no code and
installs nothing; one technically-inclined person (or a small operator) does a
one-time setup, and from then on it just runs.

## The pieces (all free tier)

1. **QR codes** — print one per station: fridge, front door, pill box. Each encodes a
   short text code shaped like `CHUMREAP:HOME:FRIDGE:GROCERY`
   (`project:site:station:action`). Any free QR generator works; the code is just text.
2. **A Google Form** — one required question, "Code". Build a prefilled link per QR
   code so the resident only has to tap Submit. Responders don't need a Google account.
3. **A Google Sheet** — three tabs:
   - `Codes`: every valid code, who it belongs to, whether it's active, its alert tier,
     and a human-readable label. This tab is the behavioral source of truth.
   - `People`: family members, how to reach them, and which alert tiers each opts into.
   - `Ledger`: the append-only event log — timestamp, who, what, tier, code.
4. **A watcher** — a small scheduled script (every 5 minutes is plenty) that reads new
   form responses, validates each code against the `Codes` tab, appends valid events to
   `Ledger`, and sends the family a digest. Any free scheduler works: a cron job, a
   scheduled GitHub Action, Google Apps Script on a timer.
5. **The family chat** — the digest lands wherever the family already is (WhatsApp,
   Telegram, email). No new app, no new account.

## The rules that keep it safe

- The resident's page says plainly: **notification log, not emergency service.** Help
  codes say "scan, then CALL" with the building or front-desk number next to them.
- Unknown or deactivated codes never become ledger rows; they're quarantined for review.
- **Silence watches**: pick the two or three absences that matter (morning meds,
  return-home by night) and their hours. The watcher nudges the family when a scan
  *doesn't* happen — absence is the signal.
- One code per station per resident. Revoke by flipping that code's Active cell to N —
  nothing to reprint, nothing to redistribute.
- Protect the ledger's event columns so only the watcher writes them; keep a notes
  column the family can annotate.

## When to graduate to the server

When one watcher serves many families, or you want per-building routing, a live admin
feed, and an API — run `server.py` in this repo. Same loop, more control. The sheet
can remain the source of truth either way.

## What this mode deliberately does not do

No medical advice, no emergency dispatch, no money handling, no medication management.
It logs and routes; licensed humans do the rest. If your deployment needs any of those,
that work — and its licenses — sits outside this project by design.
