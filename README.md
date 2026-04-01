# 🎬 Stream Link Generator

Find working stream links for any movie or TV show, straight from your terminal.

---

## Requirements

- Python 3
- `requests` library

---

## Installation

```bash
python3 -m pip install requests
```

---

## Usage

```bash
python3 Streamlinks.py
```

The script will ask you a few questions:

```
→ Movie or Show? (m/s):
→ Title name?:
→ Season number?:     ← shows only
→ Episode number?:    ← shows only
```

---

## Examples

**Movie:**
```
→ Movie or Show? (m/s): m
→ Title name?: Interstellar

[✓] Found: Interstellar (2014) [tt0816692]

── Working Links ──
[✓] vidsrc.to
    https://vidsrc.to/embed/movie/tt0816692

[✓] vidsrcme.ru
    https://vidsrcme.ru/embed/movie?imdb=tt0816692

[✓] embed.su
    https://embed.su/embed/movie/tt0816692
```

**TV Show:**
```
→ Movie or Show? (m/s): s
→ Title name?: Breaking Bad
→ Season number?: 3
→ Episode number?: 7

[✓] Found: Breaking Bad (2008) [tt0903747]
    → S03E07

── Working Links ──
[✓] vidsrc.to
    https://vidsrc.to/embed/tv/tt0903747/3/7

[✓] vidsrcme.ru
    https://vidsrcme.ru/embed/tv?imdb=tt0903747&sea=3&epi=7
```

---

## Sources

| Source | Movie format | TV format |
|---|---|---|
| vidsrc.to | `/embed/movie/{id}` | `/embed/tv/{id}/{s}/{e}` |
| vidsrcme.ru | `/embed/movie?imdb={id}` | `/embed/tv?imdb={id}&sea={s}&epi={e}` |
| embed.su | `/embed/movie/{id}` | `/embed/tv/{id}/{s}/{e}` |

---

## Troubleshooting

**`ModuleNotFoundError: requests`**
```bash
python3 -m pip install requests
```

**Title not found**
Try a shorter name — e.g. `Suits` instead of `Suits Season 1`.

**No working links**
The content may be too new for a digital release, or the sources are temporarily down. Try again later.

---

## Notes

- Uses the free [OMDB API](http://www.omdbapi.com/) for IMDb lookups — no API key needed for basic searches.
- Each link is verified with a live `HEAD` request before being shown.
- Only `[✓]` working links are printed.
