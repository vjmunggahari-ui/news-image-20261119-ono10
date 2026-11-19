# The World Today — 19 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![GitHub repo size](https://img.shields.io/github/repo-size/vjmunggahari-ui/news-image-20261119-ono10)](https://github.com/vjmunggahari-ui/news-image-20261119-ono10)
[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vjmunggahari-ui/news-image-20261119-ono10/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)** (prize $250, entries close 21 November 2026).

## The image

`entry.png` (1024×1024) is a newspaper front page — **THE WORLD TODAY, Thursday 19 November 2026** — with one hero photograph (Earth at dawn above a storm system, generated with an image model) and eight verified headlines from the day. All text is drawn programmatically, so every word is crisp and legible.

## The eight stories (all verified against real reporting)

1. **Culture** — GTA VI launches worldwide after a 13-year wait (Associated Press)
2. **Middle East** — US and Iran trade fire again as Gulf attacks widen
3. **Europe** — EU proposes €45bn loan to keep Ukraine funded (Financial Times)
4. **Space** — Voyager 1 reaches one light-day from Earth (NASA)
5. **United States** — Democrats nominate Jeffries for Speaker, 251–11 (USA Today)
6. **Diplomacy** — Trump, Xi and Putin to meet in Shenzhen today (APEC summit)
7. **Asia** — Cyclone Akvan bears down on India's east coast (The Hindu)
8. **Technology** — Nvidia halts H-series chip shipments to China

Sources for each headline are listed in [SOURCES.md](SOURCES.md).

## How it works

`main.py` copies the bundled `entry.png` to `/output/entry.png`. No network,
no randomness — running it twice writes identical bytes.

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
