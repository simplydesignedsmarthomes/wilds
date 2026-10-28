"""Pull monsters, resource nodes and merchant stock into bestiary.js - the
reverse lookups the app has never had.

Every item card already answers "where does this come from?" by listing its
drop sources and the merchants who stock it, because build_storage.py reads
the wiki's dropsline/storeline buckets item-first. Nothing has ever answered
the other direction: what does THIS monster drop, what does THIS rock give
me, what is on THIS merchant's shelf. That's the same data read the other
way round, so no new source is needed - but it is the question you actually
have in front of you mid-fight, and the app couldn't answer it.

Three feeds, all keyed by source name so the "Found from" lines already on
every item card can become tappable:

  monsters   - Category:Monsters, stats from {{Infobox Monster}} (power
               level, health, weakness/resistance/immune, aggression,
               respawn, location, xp) plus the ==Attacks== list, plus drops.
  nodes      - Category:Resource nodes, stats from {{Infobox Resource Node}}
               (health, which tool it needs, respawn) plus drops.
  other      - the ~100 drop sources that are neither: region chests, farming
               plot yields, burial mounds, bird nests, reward packs. No
               infobox worth parsing, but they appear in "Found from" lines
               constantly, so they carry a name, an icon and their drops.
  merchants  - from the storeline bucket's own page names (there is no
               Category:Merchants), split into what they sell and what they
               buy.

Queries the wiki API directly rather than reading .research/wiki_buckets.json
or wiki_wikitext.json: this script is safe to run alongside a
fetch_wiki_data.py refresh, which rewrites those caches in place.

Anything the wiki marks {{Gone}} or files under Category:Discontinued
content is skipped, so this feed can't reintroduce content the item
catalogue just finished purging.

Writes bestiary.js (window.WILDS_BESTIARY). Re-run any time.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import clean, templates, _qty

API = "https://dragonwilds.runescape.wiki/api.php"
UA = "wilds-companion-data-refresh/1.0 (personal fan companion app)"


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


def fetch_category(name):
    out, cont = [], {}
    while True:
        d = get(dict({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + name,
                      "cmlimit": "500", "cmnamespace": "0", "format": "json",
                      "formatversion": "2"}, **cont))
        out.extend(m["title"] for m in d["query"]["categorymembers"])
        if "continue" not in d:
            break
        cont = d["continue"]
        time.sleep(0.3)
    return set(out)


def fetch_wikitext(titles):
    """title -> wikitext, following redirects so a source named by one page
    (e.g. a drop line citing a redirect) still resolves to the real text."""
    out = {}
    titles = sorted(titles)
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        d = get({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                 "redirects": "1", "format": "json", "formatversion": "2",
                 "titles": "|".join(chunk)})
        q = d.get("query", {})
        back = {r["to"]: r["from"] for r in q.get("redirects", [])}
        for p in q.get("pages", []):
            if "revisions" not in p:
                continue
            wt = p["revisions"][0]["slots"]["main"]["content"]
            out[p["title"]] = wt
            if p["title"] in back:
                out[back[p["title"]]] = wt
        time.sleep(0.4)
    return out


def fetch_image_urls(filenames):
    urls = {}
    names = sorted({n for n in filenames if n})
    for i in range(0, len(names), 50):
        chunk = names[i:i + 50]
        d = get({"action": "query", "prop": "imageinfo", "iiprop": "url", "format": "json",
                 "formatversion": "2", "titles": "|".join("File:" + n for n in chunk)})
        for p in d.get("query", {}).get("pages", []):
            if p.get("imageinfo"):
                urls[p["title"][len("File:"):]] = p["imageinfo"][0]["url"]
        time.sleep(0.4)
    return urls


# ---------- infobox parsing ----------

INFOBOX_RE = r"Infobox[ _].*"
GONE_RE = re.compile(r"\{\{\s*Gone\s*[|}]", re.I)


def infobox_of(wt, kind_re):
    for _, params, _, _ in templates(wt, kind_re):
        return params
    return None


def any_infobox(wt):
    for _, params, _, _ in templates(wt, INFOBOX_RE):
        return params
    return None


def image_file(params):
    """The bare "Foo.png" out of an infobox image param, which turns up as a
    plain filename, a [[File:...]] link, or either with a |size suffix."""
    raw = (params or {}).get("image") or (params or {}).get("image1") or ""
    raw = re.sub(r"^\s*\[\[\s*(?:File|Image):", "", raw, flags=re.I)
    raw = re.sub(r"\]\].*$", "", raw)
    raw = raw.split("|")[0]
    return clean(raw).strip()


def bullet_list(text):
    """The '* one per line' lists the wiki uses for attacks and xp tables.
    Only top-level bullets are kept - a '**' sub-bullet is detail about the
    line above it, which reads as a non-sequitur once flattened."""
    out = []
    for line in (text or "").splitlines():
        line = line.rstrip()
        if re.match(r"^\*[^*]", line):
            v = clean(line.lstrip("*").strip())
            if v:
                out.append(v)
    return out


def section_text(wt, heading):
    m = re.search(r"(?m)^==\s*%s\s*==\s*$" % re.escape(heading), wt)
    if not m:
        return ""
    rest = wt[m.end():]
    nxt = re.search(r"(?m)^==[^=].*?==\s*$", rest)
    return rest[:nxt.start()] if nxt else rest


def yesno(v):
    v = clean(v or "").strip()
    if not v:
        return ""
    return "Yes" if v.lower() in ("yes", "y", "true", "1") else ("No" if v.lower() in ("no", "n", "false", "0") else v)


# ---------- name resolution ----------

def storage_item_names():
    """Canonical item spellings, so a drop chip's name matches the catalogue
    entry the UI will link it to. Read defensively: storage.js is generated,
    and a concurrent build would make this a torn read - in which case we
    simply fall back to the wiki's own spelling rather than failing."""
    try:
        content = open(os.path.join(ROOT, "storage.js"), encoding="utf-8").read()
        m = re.search(r"window\.WILDS_STORAGE\s*=\s*(\[.*?\]);\s*window\.WILDS_STORAGE_MAX_STEP",
                      content, re.S)
        names = [it["name"] for cat in json.loads(m.group(1)) for it in cat["items"]]
        return {n.lower(): n for n in names}
    except Exception as e:
        print("  storage.js names unavailable (%s) - using wiki spellings" % e, file=sys.stderr)
        return {}


def main():
    print("fetching categories...", file=sys.stderr)
    monsters = fetch_category("Monsters")
    bosses = fetch_category("Bosses")
    nodes = fetch_category("Resource nodes")
    discontinued = fetch_category("Discontinued content")

    print("fetching buckets...", file=sys.stderr)
    drop_rows = fetch_bucket("dropsline", ["page_name", "item_name", "json"])
    store_rows = fetch_bucket("storeline", ["page_name", "sold_item", "sold_item_json"])

    # source page -> [drops], built once and shared by all three feeds
    drops_by_source = {}
    for row in drop_rows:
        try:
            j = json.loads(row.get("json") or "{}")
        except ValueError:
            continue
        src = clean(j.get("Dropped from") or row.get("page_name") or "")
        item = clean(j.get("Dropped item") or row.get("item_name") or "")
        if not src or not item:
            continue
        drop = {
            "name": item,
            "qty": clean(str(j.get("Drop Quantity") or "")).replace("–", "-"),
            "rarity": clean(str(j.get("Rarity") or "")),
        }
        lst = drops_by_source.setdefault(src, [])
        if drop not in lst:
            lst.append(drop)

    merchants = {}
    for row in store_rows:
        try:
            j = json.loads(row.get("sold_item_json") or "{}")
        except ValueError:
            continue
        seller = clean(j.get("Sold by") or row.get("page_name") or "")
        item = clean(row.get("sold_item") or "")
        if not seller or not item:
            continue
        entry = {"name": item, "cost": _qty(j.get("Cost")), "currency": clean(j.get("Currency") or "")}
        side = "buys" if (j.get("Mode") or "").strip().lower() == "buy" else "sells"
        lst = merchants.setdefault(seller, {"sells": [], "buys": []})[side]
        if entry not in lst:
            lst.append(entry)

    source_pages = set(drops_by_source)
    wanted = monsters | nodes | source_pages | set(merchants)
    print("fetching wikitext for %d pages..." % len(wanted), file=sys.stderr)
    pages = fetch_wikitext(wanted)

    def is_gone(name):
        wt = pages.get(name, "")
        return name in discontinued or bool(GONE_RE.search(wt))

    # A page in Category:Monsters carrying no infobox at all is an overview
    # or disambiguation page ("Monsters", "Skeleton", "Vault Guardians"),
    # not a creature - the same junk the item catalogue filters out.
    def is_overview(name):
        return any_infobox(pages.get(name, "")) is None

    skipped = sorted(n for n in wanted if is_gone(n))
    overviews = sorted(n for n in (monsters | nodes) if not is_gone(n) and is_overview(n))

    def excluded(name):
        return is_gone(name) or is_overview(name)

    # Every File: we'll need, resolved in one batched pass. An infobox can
    # name an image that was since renamed (Coal Node still points at
    # "Coal Deposit.png"), so always ask for the by-name file too and fall
    # back to it when the infobox's own choice doesn't resolve.
    want_files = set()
    infobox_file = {}
    for name in wanted:
        if is_gone(name):
            continue
        f = image_file(any_infobox(pages.get(name, "")))
        infobox_file[name] = f
        want_files.add(name + ".png")  # the wiki's own convention, same as _chip()'s fallback
        if f:
            want_files.add(f)
    for drops in drops_by_source.values():
        for d in drops:
            want_files.add(d["name"] + ".png")
    for m in merchants.values():
        for side in ("sells", "buys"):
            for e in m[side]:
                want_files.add(e["name"] + ".png")
    print("resolving %d images..." % len(want_files), file=sys.stderr)
    images = fetch_image_urls(want_files)

    canon = storage_item_names()

    def chip(entry):
        name = canon.get(entry["name"].lower(), entry["name"])
        out = dict(entry, name=name, img=images.get(entry["name"] + ".png", "") or images.get(name + ".png", ""))
        return out

    def drops_for(name):
        return [chip(d) for d in drops_by_source.get(name, [])]

    def img_for(name):
        return images.get(infobox_file.get(name, ""), "") or images.get(name + ".png", "")

    monsters_out = []
    for name in sorted(monsters):
        if excluded(name):
            continue
        wt = pages.get(name, "")
        p = infobox_of(wt, r"Infobox[ _]Monster") or {}
        rec = {
            "name": name,
            "kind": "monster",
            "img": img_for(name),
            "powerLevel": _qty(clean(p.get("power_level", ""))) if clean(p.get("power_level", "")) else "",
            "health": clean(p.get("health", "")),
            "race": clean(p.get("race", "")),
            "weakness": clean(p.get("weakness", "")),
            "resistance": clean(p.get("resistance", "")),
            "immune": clean(p.get("immune", "")),
            "aggressive": yesno(p.get("aggressive", "")),
            "respawn": clean(p.get("respawn", "")),
            "location": clean(p.get("location", "")),
            "xp": bullet_list(p.get("experience", "")),
            "attacks": bullet_list(section_text(wt, "Attacks")),
            "drops": drops_for(name),
        }
        if name in bosses:
            rec["boss"] = True
        monsters_out.append(rec)

    nodes_out = []
    for name in sorted(nodes):
        if excluded(name):
            continue
        wt = pages.get(name, "")
        p = infobox_of(wt, r"Infobox[ _]Resource[ _]Node") or {}
        nodes_out.append({
            "name": name,
            "kind": "node",
            "img": img_for(name),
            "health": clean(p.get("health", "")),
            "tool": clean(p.get("tool", "")),
            "respawn": clean(p.get("respawn", "")),
            "location": clean(p.get("location", "")),
            "drops": drops_for(name),
        })

    other_out = []
    for name in sorted(source_pages - monsters - nodes):
        if is_gone(name):
            continue
        other_out.append({
            "name": name,
            "kind": "other",
            "img": img_for(name),
            "drops": drops_for(name),
        })

    merchants_out = []
    for name in sorted(merchants):
        if is_gone(name):
            continue
        merchants_out.append({
            "name": name,
            "kind": "merchant",
            "img": img_for(name),
            "sells": [chip(e) for e in merchants[name]["sells"]],
            "buys": [chip(e) for e in merchants[name]["buys"]],
        })

    payload = {"monsters": monsters_out, "nodes": nodes_out,
               "other": other_out, "merchants": merchants_out}
    header = ("/* Generated by .research/fetch_bestiary_data.py from the RuneScape: Dragonwilds\n"
              "   Wiki's monster/resource-node pages and its drop and shop buckets.\n"
              "   Do not edit by hand. */\n")
    js = header + "window.WILDS_BESTIARY = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "bestiary.js"), "w", encoding="utf-8").write(js.replace("—", " - "))

    with_drops = sum(1 for m in monsters_out if m["drops"])
    with_attacks = sum(1 for m in monsters_out if m["attacks"])
    print("monsters: %d (%d with drops, %d with attack lists, %d bosses)" % (
        len(monsters_out), with_drops, with_attacks,
        sum(1 for m in monsters_out if m.get("boss"))), file=sys.stderr)
    print("nodes: %d (%d with drops)" % (
        len(nodes_out), sum(1 for n in nodes_out if n["drops"])), file=sys.stderr)
    print("other drop sources: %d" % len(other_out), file=sys.stderr)
    print("merchants: %d (%d stock lines)" % (
        len(merchants_out),
        sum(len(m["sells"]) + len(m["buys"]) for m in merchants_out)), file=sys.stderr)
    if skipped:
        print("skipped as discontinued/gone (%d): %s" % (len(skipped), ", ".join(skipped[:12])), file=sys.stderr)
    if overviews:
        print("skipped as overview/disambiguation pages (%d): %s" % (
            len(overviews), ", ".join(overviews)), file=sys.stderr)
    missing_img = [m["name"] for m in monsters_out + nodes_out if not m["img"]]
    if missing_img:
        print("no image (%d): %s" % (len(missing_img), ", ".join(missing_img[:12])), file=sys.stderr)


if __name__ == "__main__":
    main()
