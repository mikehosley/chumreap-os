# Chumreap OS — sandbox (international edition)

> This repo is the **international edition**: the jurisdiction-neutral core, for global
> release. The Cambodia deployment — localized vendors, real operations, the beta
> channel — is kept private and is not part of this repo.

The working demo behind the cocktail party. One loop, ruthlessly small:

**scan QR → action page → tap → event in ledger → notification dispatched → admin sees it live.**

## Disclaimer

Published **for illustration** as a reference implementation. No claim is made — and none should be inferred — about its **suitability for any particular project**, deployment, or use case. Nothing here is legal, medical, or regulatory advice. This is a **global public release**: privacy, health-data, and care-service laws vary by jurisdiction, and you are solely responsible for determining compliance with the laws that apply to you, including engaging qualified counsel where needed. The software is provided "as is" under the Apache License 2.0, without warranties of any kind.

**Real-world implementation has real-world consequences.** This is a reference design, not a business plan. Actually deploying it — housing residents, handling money, coordinating services — may create **tax obligations** (income, property, business, or other taxes, depending on your jurisdiction and how you structure it) and may require **licenses, permits, or regulatory approvals** (business licensing, care-service rules, data protection, zoning and land use, food handling, transport, employment — the list depends entirely on what you build and where). Before implementing anything described here in a real setting, consult **qualified professionals for your particular application**: an accountant or tax advisor, a finance professional, legal counsel, and the relevant zoning, planning, and licensing authorities — plus anyone else whose domain touches what you're building. The author is none of these, and this project is not a substitute for any of them.

## Free, changeable, jurisdiction-neutral

**Free:** use it, modify it, distribute it — including commercially — at no charge, under the Apache License 2.0. No permission needed, no royalties, no gatekeeper.

**Changeable:** fork it and adapt it to your locality — your language, your vendors, your notification channels, your documents. That is the intended use, not a violation of it.

**Jurisdiction-neutral by design:** this architecture deliberately encodes no country's regulatory requirements and attempts to satisfy none of them — that is a design choice, not an oversight, and not an invitation to evade the law. Every deployment **must** supply its own compliance layer: local counsel, local consent documents, local data-handling rules. The author makes **no claim of suitability for any particular region, state, local, or national government**. What fits Phnom Penh may not satisfy California; nothing here tells you otherwise. Adapt it, have counsel review it, own the result.

**Start with the `deployment/` folder.** It contains eleven blank localization templates — tax, accounting, finance, legal, zoning & planning, licensing, data privacy, employment, insurance, brand/domain — plus a twelfth, `OTHER.md`, as the catch-all. Each names the qualified professional who fills it in and ends with a sign-off block. The software is not deployable with that folder empty; that is deliberate.

**Want to run this as a business in your country?** Read `FORKING.md`. The license already permits commercial forks — no permission, no royalties. The code is free; the name isn't.

## Run it

```bash
pip install -r requirements.txt
python server.py
```

- Resident page: http://localhost:5000/k/DEMO-A/door (also `/fridge`, `/menu`, `/gym`; kits `DEMO-A`–`DEMO-E`)
- Admin (live): http://localhost:5000/admin
- API: `POST /api/event` `{kit, ctx, action}`, `GET /api/events`

## The loop, end to end

```bash
curl -X POST localhost:5000/api/event -H 'Content-Type: application/json' \
  -d '{"kit":"DEMO-A","ctx":"door","action":"checkin"}'
# → event logged, notification dispatched (log channel), visible at /admin
```

## Notification routing

`routes.json` maps event → list of `[channel, recipient]`. Channels: `log` (working),
`whatsapp` / `telegram` / `email` (stubbed — see `chumreap/notify.py` for the
credential TODOs). Rule enforced in code: non-green categories are **blocked**
from Meta pipes.

## What's real / what's stubbed

- Real: QR resolution, action pages, append-only ledger (SQLite), live admin feed, dispatcher, channel rules.
- Stubbed: WhatsApp/Telegram/email delivery (prints to console until credentials are set).

## Phone demo

Phones need to reach the server: run it on your LAN (`BASE_URL=http://<your-lan-ip>:5000`)
and regenerate the kit QR codes against that URL, or put it behind a tunnel.
Generate kits with `python tools/make_kits.py`; the codes are placeholders until
they point at your public URL.

## License

Apache-2.0. See LICENSE. Open from inception: prototype/alpha reference implementation.
