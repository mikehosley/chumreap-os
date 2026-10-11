# Forking Chumreap OS for your country

You are allowed to do this. That is the point.

Under the Apache License 2.0, you may take this code, modify it, and build a
business on it — including a for-profit business — without asking permission and
without paying anyone. Translate it, rebrand the interface, plug in your local
vendors, charge what the market bears. The license is the permission slip.

## How a local operator makes money on it

The software is free. The *operation* is the product. Proven shapes:

- **Operated service.** Run the home-mode or managed-property service in your city. Charge residents or families a monthly fee. This is the primary model — the code is maybe 10% of the business; the other 90% is staff, vendors, trust, and showing up.
- **Hosted SaaS.** Run the ledger and notification infrastructure for multiple small operators; charge per resident per month.
- **Deployment consulting.** Help other local operators get set up — localization, vendor contracting, staff training. The `deployment/` folder is your scope document.
- **Proprietary extensions.** Apache-2.0 (unlike copyleft licenses) lets you keep your own modifications private. Build closed add-ons on the open core if your market rewards it.

## The localization path

1. **Fill in `deployment/`.** Eleven blank templates plus the catch-all — tax, accounting, finance, legal, zoning, licensing, data privacy, employment, insurance, brand. Each names the professional who signs it. This is not optional; it is what makes the fork lawful where you live. (Example: in Turkey, your counsel maps KVKK data law and Turkish tax/accounting into these files.)
2. **Translate the resident interface.** Big buttons, local language(s), local food, local vendors.
3. **Contract local providers.** Pharmacies, clinics, markets, runners — the architecture routes to vendors; you supply them.
4. **Price for your market.** The tier model (real-time / daily diary / pattern analysis) is a suggestion, not a requirement.

## The brand rule

The code is free; the name is not. The Apache License does not grant trademark rights.
You may fork the code, but do not call your commercial service "Chumreap" (or present
it as affiliated with this project) without written permission. Pick your own name —
your market, your brand, your reputation.

## What we'd love (not required)

- Tell us you're out there. A link, an email, a pull request — we'd like to know.
- Contribute back what generalizes. Bug fixes, better QR patterns, a cleaner router — the core gets stronger for everyone.
- Join the operator list: add yourself to `OPERATORS.md` via pull request — it signals to the next fork that the pattern works somewhere real.

## What we require

- Keep the LICENSE file and the disclaimer notices intact in anything you distribute.
- Keep the `deployment/` folder (or its equivalent) in your fork. If you strip the localization scaffolding, say so plainly — your users deserve to know what you removed.

---

*The architecture wins when twenty countries run descendants of it and no one needed our permission. That's the strategy.*
