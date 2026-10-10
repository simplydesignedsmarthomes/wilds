"""Pull the wiki's own structured data, so every item's detail comes from one
uniform source instead of whichever research pass happened to catch it.

  - Bucket tables (the wiki's structured data store, the same data its own
    recipe/drop/shop tables render from): recipe, dropsline, storeline,
    infobox_item, item_perks.
  - Raw wikitext for every item page in storage (50 pages per request), for
    the {{Infobox Weapon}} / {{Infobox Armour}} stats the buckets don't carry.
  - Real image URLs for every file referenced by a recipe material/output, so
    every recipe chip gets the wiki's own icon even for things (building
    pieces etc.) that aren't items in this app.

Writes .research/wiki_buckets.json, .research/wiki_wikitext.json,
.research/wiki_images.json. Re-run before build_storage.py to refresh.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = "https://dragonwilds.runescape.wiki/api.php"
UA = "wilds-companion-data-refresh/1.0 (personal fan companion app)"

def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"user-agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 3)

BUCKETS = {
    "recipe": ["page_name", "output", "uses_facility", "json"],
    "dropsline": ["page_name", "item_name", "json"],
    "storeline": ["page_name", "sold_item", "sold_item_json"],
    "infobox_item": ["page_name", "item_name", "json"],
    "item_perks": ["page_name", "item_name", "item_perk", "json"],
}

def fetch_bucket(name, fields):
    rows, offset, page = [], 0, 500
    sel = ",".join("'%s'" % f for f in fields)
    while True:
        q = "bucket('%s').select(%s).limit(%d).offset(%d).run()" % (name, sel, page, offset)
        d = get({"action": "bucket", "format": "json", "query": q})
        if "error" in d:
            raise RuntimeError("%s: %s" % (name, d["error"]))
        batch = d.get("bucket", [])
        rows.extend(batch)
        if len(batch) < page:
            break
        offset += page
        time.sleep(0.4)
    return rows

def storage_item_names():
    content = open(os.path.join(ROOT, "storage.js"), encoding="utf-8").read()
    m = re.search(r"window\.WILDS_STORAGE\s*=\s*(\[.*?\]);\s*window\.WILDS_STORAGE_MAX_STEP", content, re.S)
    return [it["name"] for cat in json.loads(m.group(1)) for it in cat["items"]]

def fetch_wikitext(titles):
    out, redirects = {}, {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        d = get({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                 "format": "json", "formatversion": "2", "redirects": "1", "titles": "|".join(chunk)})
        q = d.get("query", {})
        for r in q.get("redirects", []):
            redirects[r["from"]] = r["to"]
        for n in q.get("normalized", []):
            redirects.setdefault(n["from"], n["to"])
        for p in q.get("pages", []):
            if "revisions" in p:
                out[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
        time.sleep(0.4)
        print("  wikitext %d/%d" % (min(i + 50, len(titles)), len(titles)), file=sys.stderr)
    return out, redirects

FILE_RE = re.compile(r"\[\[File:([^|\]]+)")

def fetch_image_urls(filenames):
    urls = {}
    names = sorted(set(filenames))
    for i in range(0, len(names), 50):
        chunk = names[i:i + 50]
        d = get({"action": "query", "prop": "imageinfo", "iiprop": "url", "format": "json", "formatversion": "2",
                 "titles": "|".join("File:" + n for n in chunk)})
        q = d.get("query", {})
        norm = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for p in q.get("pages", []):
            if p.get("imageinfo"):
                title = p["title"]
                original = norm.get(title, title)
                urls[original[len("File:"):]] = p["imageinfo"][0]["url"]
                urls[title[len("File:"):]] = p["imageinfo"][0]["url"]
        time.sleep(0.4)
        print("  images %d/%d" % (min(i + 50, len(names)), len(names)), file=sys.stderr)
    return urls

def main():
    buckets = {}
    for name, fields in BUCKETS.items():
        rows = fetch_bucket(name, fields)
        buckets[name] = rows
        print("bucket %s: %d rows" % (name, len(rows)), file=sys.stderr)
    json.dump(buckets, open(os.path.join(HERE, "wiki_buckets.json"), "w"), ensure_ascii=False)

    titles = sorted(set(storage_item_names()))
    wikitext, redirects = fetch_wikitext(titles)
    json.dump({"pages": wikitext, "redirects": redirects},
              open(os.path.join(HERE, "wiki_wikitext.json"), "w"), ensure_ascii=False)
    print("wikitext: %d pages, %d redirects" % (len(wikitext), len(redirects)), file=sys.stderr)

    files = []
    # Every item's own infobox picture, so item icons come from one place.
    for text in wikitext.values():
        for m in re.finditer(r"\|\s*image1?\s*=\s*([^|\n}]+)", text):
            f = re.sub(r"^\s*\[\[File:|\]\].*$|\|.*$", "", m.group(1)).strip()
            if f:
                files.append(f)
        # Recipe templates marked bucket=no never reach the recipe bucket, so
        # their materials' icons have to be resolved by name here instead.
        for m in re.finditer(r"\|\s*(?:mat\d+|output\d+)\s*=\s*([^|\n}]+)", text):
            files.append(m.group(1).strip() + ".png")
        for m in re.finditer(r"\|\s*(?:mat|output)\d+pic\s*=\s*([^|\n}]+)", text):
            files.append(m.group(1).strip() + ".png")
    for row in buckets["recipe"]:
        try:
            j = json.loads(row.get("json") or "{}")
        except ValueError:
            continue
        for mat in j.get("materials", []) or []:
            files += FILE_RE.findall(mat.get("image") or "")
        out = j.get("output") or {}
        if isinstance(out, dict):
            files += FILE_RE.findall(out.get("image") or "")
    urls = fetch_image_urls([f.strip() for f in files])
    json.dump(urls, open(os.path.join(HERE, "wiki_images.json"), "w"), ensure_ascii=False)
    print("images resolved: %d" % len(urls), file=sys.stderr)

if __name__ == "__main__":
    main()
