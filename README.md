# The World Today — 19 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![GitHub repo size](https://img.shields.io/github/repo-size/vjmunggahari-ui/news-image-20261119-ono10)](https://github.com/vjmunggahari-ui/news-image-20261119-ono10)
[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)** (prize $250, entries close 21 November 2026).

## The image

`entry.png` (1024×1024, 134 KB) is a newspaper front page — **THE WORLD TODAY, Thursday 19 November 2026** — drawn entirely in code: a masthead, a lead story with a drawn Shenzhen dusk scene (skyline under the US, Chinese and Russian flags), two illustrated secondaries, a six-story grid, an "Also today" briefs strip, and a source line. Every word is drawn as vector text, so the page stays crisp and legible at any size.

## The thirteen stories

**Lead — Diplomacy:** Trump, Xi and Putin gather in Shenzhen for trilateral talks at the APEC summit.

**Secondaries:** US and Iran trade fire again as Gulf attacks widen; the Crimean Bridge is attacked again.

**Grid:** the UN court's historic Rohingya genocide verdict on Myanmar; a Van Gogh sells for a record $190.4m; Anthropic raises $81.3bn in the biggest IPO ever; GTA VI arrives at last, 13 years on; Voyager 1 sails one light-day from Earth; Israeli tanks cross the Gaza ceasefire line.

**Also today:** India–Japan 2+2 defence talks; US–Venezuela military ties restored; North Korea fires missiles after US drills; Fed minutes point to further rate hikes.

Every story was verified against real reporting from 19 November 2026; see `SOURCES.md` for the source of each one.

## How it works

`main.py` (Python 3.13, standard library only) validates the bundled `entry.png` — PNG signature, chunk stream, trailing IEND, 1024×1024, at most 1 MiB — and copies it byte-for-byte to `/output/entry.png`, then proves the copy by SHA-256. No network, no clock, no randomness: running it twice writes identical bytes.

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
