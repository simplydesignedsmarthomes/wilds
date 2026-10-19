"""Pull the wiki's Update: namespace into updates.js for the app's Updates tab.

The Dragonwilds Wiki mirrors every official patch note, hotfix and dev post
into its own Update: namespace (one page per post) within the same day it
goes out, each headed by a {{UpdateHeader|date=...|category=...|link=...}}
template that carries the real date and, when there is one, a direct link to
the official Steam/Jagex post. That makes it both the simplest and the most
current single source for an in-app patch notes feed - no separate Steam
polling needed for the text itself.

For pictures: a post about a specific event sometimes embeds its own image
or a {{Youtube|id}} trailer, and those are used when present. Most routine
patch-note posts don't embed anything though, so every card also gets one of
the game's official Steam store screenshots (fetched once from Steam's public
appdetails API) as decoration, cycled so consecutive cards don't repeat.

Writes updates.js (window.WILDS_UPDATES, loaded up front - it's tiny).
Re-run any time; always reflects whatever the wiki currently has.
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import clean, templates

API = "https://dragonwilds.runescape.wiki/api.php"
UA = "wilds-companion-data-refresh/1.0 (personal fan companion app)"
MAX_UPDATES = 60
STEAM_APPID = "1374490"

def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"user-agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 3)

def list_update_pages(limit):
    """Newest-first Update: namespace pages, via recent-changes (cheap, one
    call per 500) rather than allpages (which isn't date-ordered). Returns
    page IDs, not titles - a post can get renamed after it's first created
    (seen in the wild: "Eye on Ashenfall 0 1.0.0" -> "Eye on Ashenfall -
    1.0.1 Update", with the old title left behind as a redirect, sometimes
    a stale/broken one pointing at neither the new title nor anywhere real).
    The page ID is the one thing a rename can't invalidate."""
    pageids, cont, seen = [], {}, set()
    while len(pageids) < limit:
        d = get(dict({"action": "query", "list": "recentchanges", "rcnamespace": "100",
                      "rctype": "new", "rclimit": "500", "rcprop": "title|timestamp|ids",
                      "rcdir": "older", "format": "json"}, **cont))
        for rc in d["query"]["recentchanges"]:
            if rc["pageid"] not in seen:
                seen.add(rc["pageid"])
                pageids.append(rc["pageid"])
        if "continue" not in d or len(pageids) >= limit:
            break
        cont = d["continue"]
    return pageids[:limit]

def fetch_contents(pageids):
    """pageid -> (current title, content) - fetched by ID so a post that's
    been renamed since it was first discovered still resolves to its real,
    current title and text instead of a stale or redirected one."""
    out = {}
    pageids = list(pageids)
    for i in range(0, len(pageids), 50):
        chunk = pageids[i:i + 50]
        d = get({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                 "format": "json", "formatversion": "2", "pageids": "|".join(str(p) for p in chunk)})
        for p in d["query"]["pages"]:
            if "revisions" in p:
                out[p["pageid"]] = (p["title"], p["revisions"][0]["slots"]["main"]["content"])
        time.sleep(0.4)
    return out

FILE_RE = re.compile(r"\[\[File:([^|\]]+)")

def fetch_image_urls(filenames):
    urls = {}
    names = sorted(set(filenames))
    for i in range(0, len(names), 50):
        chunk = names[i:i + 50]
        d = get({"action": "query", "prop": "imageinfo", "iiprop": "url", "format": "json", "formatversion": "2",
                 "titles": "|".join("File:" + n for n in chunk)})
        for p in d.get("query", {}).get("pages", []):
            if p.get("imageinfo"):
                urls[p["title"][len("File:"):]] = p["imageinfo"][0]["url"]
        time.sleep(0.4)
    return urls

def fetch_steam_gallery():
    """Official gameplay screenshots, straight from Steam's public store API
    - no key needed. Used as decoration on posts with no art of their own."""
    url = "https://store.steampowered.com/api/appdetails?appids=%s&l=english" % STEAM_APPID
    req = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
        app = d[STEAM_APPID]["data"]
        shots = [s["path_full"] for s in app.get("screenshots", [])]
        return shots or ([app["header_image"]] if app.get("header_image") else [])
    except Exception as e:
        print("  steam gallery unavailable: %s" % e, file=sys.stderr)
        return []

def strip_title(title):
    # "Update:0.12.0.5 is now live!" -> "0.12.0.5 is now live!"
    return title.split(":", 1)[1] if ":" in title else title

def main():
    pageids = list_update_pages(MAX_UPDATES)
    contents = fetch_contents(pageids)

    parsed, file_names = [], []
    for pid in pageids:
        found = contents.get(pid)
        if not found:
            continue
        title, wt = found
        if not wt or re.match(r"\s*#redirect", wt, re.I):
            continue
        header = None
        for _, p, _, _ in templates(wt, r"UpdateHeader"):
            header = p
            break
        youtube_id = None
        for _, p, _, _ in templates(wt, r"Youtube|YouTube"):
            youtube_id = p.get("1")
            break
        file_match = FILE_RE.search(wt)
        file_name = file_match.group(1).strip() if file_match else None
        if file_name:
            file_names.append(file_name)
        body = re.sub(r"\{\{UpdateHeader[^}]*\}\}", "", wt, count=1)
        body = re.sub(r"\{\{Youtube\|[^}]*\}\}", "", body, count=1, flags=re.I)
        summary = clean(body)[:400].strip()
        parsed.append({
            "title": strip_title(title), "date": (header or {}).get("date") or "",
            "category": (header or {}).get("category") or "",
            "officialUrl": (header or {}).get("link") or "",
            "wikiUrl": "https://dragonwilds.runescape.wiki/w/" + urllib.parse.quote(title.replace(" ", "_")),
            "summary": summary, "youtubeId": youtube_id, "_fileName": file_name,
        })

    image_urls = fetch_image_urls(file_names) if file_names else {}
    gallery = fetch_steam_gallery()

    rows, own_art = [], 0
    for i, u in enumerate(parsed):
        fname = u.pop("_fileName")
        own = image_urls.get(fname) if fname else None
        if own:
            own_art += 1
        u["image"] = own or (gallery[i % len(gallery)] if gallery else "")
        rows.append(u)

    header_js = ("/* Generated by .research/fetch_updates_data.py from the RuneScape: Dragonwilds\n"
                 "   Wiki's Update: namespace and Steam's public store API. Do not edit by hand. */\n")
    payload = {"discord": "https://discord.gg/rsdwwiki", "gallery": gallery, "updates": rows}
    js = header_js + "window.WILDS_UPDATES = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "updates.js"), "w", encoding="utf-8").write(js.replace("—", " - "))
    print("updates: %d, gallery: %d, with own art: %d, with youtube: %d" % (
        len(rows), len(gallery), own_art, sum(1 for r in rows if r.get("youtubeId"))), file=sys.stderr)

if __name__ == "__main__":
    main()
