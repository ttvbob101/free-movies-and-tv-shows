#!/home/codespace/.python/current/bin/python3
"""
Stream Link Generator
Uses OMDB API (no special library needed) + requests only
"""

import sys
import json

try:
    import requests
except ImportError:
    print("[!] Missing: pip install requests")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
# Free OMDB API key (public demo key - works for basic searches)
OMDB_API_KEY = "trilogy"   # fallback public key
OMDB_URL     = "http://www.omdbapi.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/110.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.google.com/",
}
TIMEOUT = 8


# ── IMDb lookup via OMDB ──────────────────────────────────────────────────────
def search_omdb(title: str, is_show: bool) -> dict | None:
    """Search OMDB for a title and return the result dict, or None."""
    media_type = "series" if is_show else "movie"
    try:
        resp = requests.get(
            OMDB_URL,
            params={"apikey": OMDB_API_KEY, "t": title, "type": media_type},
            timeout=TIMEOUT,
        )
        data = resp.json()
        if data.get("Response") == "True":
            return data
        # Try a broader search if exact match fails
        resp2 = requests.get(
            OMDB_URL,
            params={"apikey": OMDB_API_KEY, "s": title, "type": media_type},
            timeout=TIMEOUT,
        )
        data2 = resp2.json()
        if data2.get("Response") == "True" and data2.get("Search"):
            # Fetch full details for the first result
            first_id = data2["Search"][0]["imdbID"]
            resp3 = requests.get(
                OMDB_URL,
                params={"apikey": OMDB_API_KEY, "i": first_id},
                timeout=TIMEOUT,
            )
            return resp3.json()
    except requests.RequestException as exc:
        print(f"\n  [!] Network error during lookup: {exc}")
    return None


# ── Link builders ─────────────────────────────────────────────────────────────
def build_links(imdb_id: str, season: int = None, episode: int = None) -> dict:
    is_show = season is not None and episode is not None
    if is_show:
        s, e = season, episode
        return {
            "vidsrc.to"  : f"https://vidsrc.to/embed/tv/{imdb_id}/{s}/{e}",
            "vidsrcme.ru": f"https://vidsrcme.ru/embed/tv?imdb={imdb_id}&sea={s}&epi={e}",
            "embed.su"   : f"https://embed.su/embed/tv/{imdb_id}/{s}/{e}",
        }
    return {
        "vidsrc.to"  : f"https://vidsrc.to/embed/movie/{imdb_id}",
        "vidsrcme.ru": f"https://vidsrcme.ru/embed/movie?imdb={imdb_id}",
        "embed.su"   : f"https://embed.su/embed/movie/{imdb_id}",
    }


# ── Live validation ───────────────────────────────────────────────────────────
def check_link(url: str) -> bool:
    try:
        r = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return r.status_code == 200
    except requests.RequestException:
        return False


# ── UI helpers ────────────────────────────────────────────────────────────────
def banner():
    print("\033[96m")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║     🎬  Stream Link Generator  📺        ║")
    print("  ╚══════════════════════════════════════════╝")
    print("\033[0m")

def ask(prompt: str) -> str:
    try:
        return input(f"  \033[93m→\033[0m {prompt} ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Goodbye!")
        sys.exit(0)

def ask_int(prompt: str) -> int:
    while True:
        raw = ask(prompt)
        try:
            v = int(raw)
            if v >= 1:
                return v
            raise ValueError
        except ValueError:
            print("  \033[91m[!] Enter a positive whole number.\033[0m")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    banner()

    # Movie or show?
    while True:
        kind = ask("Movie or Show? (m/s):").lower()
        if kind in ("m", "movie"):
            is_show = False
            break
        elif kind in ("s", "show", "series", "tv"):
            is_show = True
            break
        else:
            print("  \033[91m[!] Type m for movie or s for show.\033[0m")

    name = ask("Title name?:")
    if not name:
        print("  [!] No title entered.")
        sys.exit(1)

    season = episode = None
    if is_show:
        season  = ask_int("Season number?:")
        episode = ask_int("Episode number?:")

    # Lookup
    print(f"\n  \033[90m[~] Looking up \"{name}\" on OMDB…\033[0m")
    try:
        result = search_omdb(name, is_show)
    except Exception as exc:
        print(f"  \033[91m[!] Error: {exc}\033[0m")
        sys.exit(1)

    if not result:
        print("  \033[91m[✗] Title not found. Check spelling or try a shorter name.\033[0m\n")
        sys.exit(1)

    imdb_id    = result.get("imdbID", "")
    title_name = result.get("Title", name)
    year       = result.get("Year", "")

    print(f"  \033[92m[✓] Found:\033[0m {title_name} ({year})  [{imdb_id}]")
    if is_show:
        print(f"  \033[90m    → S{season:02d}E{episode:02d}\033[0m")

    # Build + validate
    links = build_links(imdb_id, season, episode)
    print(f"\n  \033[90m[~] Checking {len(links)} sources…\033[0m\n")

    working = []
    for source, url in links.items():
        print(f"      {source}…", end=" ", flush=True)
        if check_link(url):
            print("\033[92m✓\033[0m")
            working.append((source, url))
        else:
            print("\033[91m✗\033[0m")

    # Output
    print()
    if working:
        print("  \033[92m── Working Links ──\033[0m\n")
        for source, url in working:
            print(f"  \033[92m[✓] {source}\033[0m")
            print(f"      \033[94m{url}\033[0m\n")
    else:
        print("  \033[91m[✗] No working links found.\033[0m")
        print("  • Check spelling  • Content may be too new for streaming\n")


if __name__ == "__main__":
    main()
