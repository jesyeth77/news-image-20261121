# news-image-20261121 — Manja lane

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jesyeth77/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jesyeth77/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One page that sums up **Saturday, 21 November 2026**'s world news in a single
1024×1024 image.

## Stories

- **Lead — Russia's huge overnight strike hits Kyiv, missiles land in Poland.**
  400+ drones and 110 missiles; at least eight killed in Kyiv, bridges and
  power crippled. Two Russian missiles and a suspected drone come down in
  Poland; PM Tusk calls it a deliberate provocation, NATO a grave violation.
  *(AP / France 24)*
- **AI stock rout pushes S&P 500 into correction** — US stocks fall 3.7% on
  Friday as AI and chip shares sell off.
- **ICJ: Myanmar committed genocide against the Rohingya** — Myanmar and China
  reject the ruling as unfair.
- **Trump weighs new Iran strikes as Israel presses** — and tells European
  leaders to withhold funding from Ukraine after his Putin summit.
- **Anthropic opens trading as a $2 trillion company** — among the world's most
  valuable public companies days after its record IPO.
- **Also today:** COP31 talks run past deadline over fossil fuels; pancreatic
  cancer pill trial — tumours undetectable in 1 in 12 patients; UK and EU sign
  biggest post-Brexit agreements; Gen Z protests spread across 25 European
  countries; FBI criminal database reportedly hacked; Mongolia's president
  resigns; Trump, Xi and Putin's Shenzhen summit — Xi at centre stage.

Sources: AP, Reuters, NYT, BBC, France 24, CBS News.

## How it works

- `data/news.json` — the stories, date line and sources.
- `render.py` — draws `assets/entry.png` (1024×1024, Pillow + bundled
  DejaVu fonts). Deterministic: no clock, network or randomness.
- `main.py` — pure Python 3 standard library. Copies the baked
  `assets/entry.png` to `/output/entry.png` and verifies it is a valid PNG
  within the bounty limits (≤1024×1024, ≤1 MiB) and byte-identical to the
  baked original (SHA-256 match).

## Run

```sh
python3 render.py   # regenerate assets/entry.png
python3 -S -P main.py  # write /output/entry.png and verify it
```

## Owner

- make.fun: **@lively-stork-30**
- GitHub: **jesyeth77**
- Payout wallet: `7gxEpy7iKTjms65gNT3yQFEtrbYRrfGfuGXHke4bYC5h`

MIT licensed — see `LICENSE`.
