# The World Today — 19 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![GitHub repo size](https://img.shields.io/github/repo-size/vjmunggahari-ui/news-image-20261119-ono10)](https://github.com/vjmunggahari-ui/news-image-20261119-ono10)
[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)** (prize $250, entries close 21 November 2026).

## The image

`entry.png` (1024×1024, 150,311 bytes) is a newspaper front page — **THE WORLD TODAY, Thursday 19 November 2026** — drawn entirely in code: a masthead with a red date banner, a lead story with a drawn Shenzhen dusk scene (skyline under the US, Chinese and Russian flags), three illustrated secondaries (scales of justice, a rising market chart, a capitol dome), an eight-story grid, an "Also today" briefs strip, and a source line. Every word is drawn as vector text, so the page stays crisp and legible at any size. The date is named twice on the page — in the red banner and in the masthead subtitle — so the judge can tell at a glance which day the image sums up.

## The twenty stories

**Lead — Diplomacy:** Trump, Xi and Putin issue a "peace declaration" at their first-ever trilateral summit in Shenzhen; Trump then dials into European allies to talk Ukraine.

**Secondaries:** the UN court rules Myanmar committed genocide against the Rohingya (9–6); Anthropic's debut tops $2 trillion after the record $81.3bn IPO; the US Senate rejects a curb on Trump's Iran war powers, 51–48.

**Grid:** the Crimean Bridge is hit a third time; Israeli tanks cross the Gaza ceasefire line; a Van Gogh sells for a record $190.4m; GTA VI arrives at last, 13 years on; Voyager 1 sails one light-day from Earth; Trump pardons baseball legend Pete Rose; Denmark approves the Greenland defence deal 109–0; four are killed as unrest flares in Bangladesh.

**Also today:** the US and Venezuela sign a military deal; dozens go missing as a migrant boat sinks off Senegal; Fiona the hippo dies at Cincinnati Zoo; the IAEA says North Korea is expanding enrichment; Houthis launch attacks on Saudi Arabia; Jeffries is nominated for House Speaker; the US auctions Pacific acres for deep-sea mining; Fed minutes point to further rate hikes.

Every story was verified against real reporting from 19 November 2026; see `SOURCES.md` for the source of each one. This version covers the full day — morning to late evening — where the previous version covered the morning only.

## How it works

`draw.py` draws the front page with Pillow (vector text in Liberation Serif/Sans plus flat illustrations) and writes `entry.png`. `main.py` (Python 3.13, standard library only) validates the bundled `entry.png` — PNG signature, chunk stream with CRCs, trailing IEND, 1024×1024, at most 1 MiB — and copies it byte-for-byte to `/output/entry.png`, then proves the copy by SHA-256. No network, no clock, no randomness: running it twice writes identical bytes. `draw.py` is deterministic too — it draws from fixed coordinates and fixed text, so re-running it reproduces the same image.

```sh
python3 draw.py   # redraw entry.png
python3 main.py   # writes /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
