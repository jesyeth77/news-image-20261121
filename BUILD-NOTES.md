# Build notes — news-image-20261121 (Manja lane)

- Bounty: `news-image-20261121` — "Sum up 21 November's world news in one image"
- Lane: Manja — make.fun @lively-stork-30, GitHub jesyeth77
- Payout wallet: `7gxEpy7iKTjms65gNT3yQFEtrbYRrfGfuGXHke4bYC5h`
- Built: Saturday, 21 November 2026 (WIB)
- Design: fresh "THE WORLD TODAY" front page — navy masthead band with brass
  rule, signal-red kickers, numbered story cards (01–04) in a 2x2 grid,
  "Also Today" strip, sources footer. Written fresh; not a copy of the
  20 Nov entry (different code structure, palette and layout).

## Image

- File: `assets/entry.png`
- Dimensions: 1024 × 1024
- Size: 131,838 bytes (≤ 1 MiB limit)
- SHA-256: `29058fc43f6cabd0bf559d28e16a0ea9c1abf1efa7fa03556ad30dbbfff09008`

## Verification

1. `python3 render.py` — produced `assets/entry.png`, 1024×1024,
   131,838 bytes, valid PNG. ✅
2. Visual read-back — masthead + date line, lead story (Russia's strike on
   Kyiv, missiles in Poland), four numbered stories (AI rout, ICJ Myanmar,
   Trump/Iran, Anthropic $2T), seven-item "Also Today" strip and sources
   footer all present; all headlines legible, no text overlap. One defect
   found and fixed in-session: first render overflowed the 1024px height
   (last two "Also Today" items + footer clipped); tightened grid rows and
   leading, re-rendered, everything fits. ✅
3. `python3 -S -P main.py` run twice — exit 0 both times; both outputs
   byte-identical (SHA-256 `29058fc4…f09008`), matching the baked asset. ✅
4. `main.py` was revised in-session after first writing (chunk-header
   parsing extracted into a `next_chunk` helper) and re-verified. ✅

## Recording

- `makefun record` REFUSED by the server for this bounty (HTTP 400):
  "news-image-20261121 does not take recorded transcripts: its entries
  upload their transcripts (a bundle or loose files) as the requirements
  say". So this bounty is NOT strict-transcripts — submit with --bundle,
  not --recording.

## Notes

- Repo creation is BLOCKED at this step: `gh` is not logged in on this VM
  and the repo does not exist yet (verified via ls-remote: "Repository not
  found"). Local git commit done; push + bundle + submit need the repo to
  exist first — parent to create it or hand off.
