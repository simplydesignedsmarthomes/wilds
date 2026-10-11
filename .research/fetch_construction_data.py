"""Pull the Build Menu catalogue into construction.js for the app's
Construction tab, grouped exactly the way the game's own Build Menu groups
it - not a guess at categories, but the wiki's own transcription of the real
menu (RuneScape: Dragonwilds Wiki, "Buildings" page, "List of buildings"
section): Category -> Subcategory -> an optional material-set group (Cabin,
Cottage, Castle, Kharidian, colour variants, faction banners, ...) -> items.
That last level is exactly where a structural piece's different material
styles live (a Cabin wall costs logs, a Castle wall costs stone block - same
slot in the menu, different recipe), so the recipe bucket is read directly
here rather than through WikiData's de-duplicated lookup, which would only
keep one style per item.

Writes construction.js (window.WILDS_CONSTRUCTION):
  [{key, label, subcats: [{key, label, groups: [{label, items: [
      {name, img, materials: [chip], skills: [{name, xp}]}
  ]}]}]}]

Re-run any time; always reflects whatever is currently in wiki_buckets.json
(run fetch_wiki_data.py first) and the wiki's current Buildings page.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import WikiData, clean, templates, _qty

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

def fetch_buildings_page():
    d = get({"action": "query", "titles": "Buildings", "prop": "revisions", "rvprop": "content",
             "rvslots": "main", "format": "json", "formatversion": "2"})
    return d["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]

STYLE_RE = re.compile(r"\(([^)]+)\)\.png$", re.I)

def build_recipe_index(wiki, rows):
    """(page_name, style_or_None) -> recipe, read straight off the bucket rows
    so every material-set variant survives, not just one per item."""
    idx = {}
    for row in rows:
        try:
            j = json.loads(row.get("json") or "{}")
        except ValueError:
            continue
        out = j.get("output") if isinstance(j.get("output"), dict) else {}
        out_name = (out.get("name") or row["page_name"] or "").strip()
        if not out_name:
            continue
        mats = [wiki._chip(m.get("name"), m.get("quantity"), m.get("image")) for m in (j.get("materials") or [])]
        mats = [m for m in mats if m["name"]]
        m = STYLE_RE.search(out.get("image") or "")
        style = clean(m.group(1)) if m else None
        rec = {
            "img": wiki._chip(out_name, out.get("quantity"), out.get("image"))["img"],
            "materials": mats,
            "skills": [{"name": clean(s.get("name") or ""), "xp": _qty(s.get("experience"))}
                       for s in (j.get("skills") or []) if s.get("name")],
        }
        idx.setdefault((row["page_name"], style), rec)
    return idx

def resolve(idx, raw_name, link_target, style):
    candidates = [(raw_name, style), (raw_name, None), (link_target, style), (link_target, None)]
    # Some entries carry more than one trailing "(Tag)" (e.g. a Kharidian
    # piece that also comes in a colour: "... (Kharidian) (Blue)") - our
    # recipe data only tags the outermost one, so peel them off one at a
    # time and try each remaining tag against the fully bare name too.
    base = raw_name
    while True:
        m = re.match(r"^(.*?)\s*\(([^)]+)\)$", base)
        if not m:
            break
        base, tag = m.group(1).strip(), m.group(2).strip()
        candidates.append((base, tag))
    candidates.append((base, None))
    for key in candidates:
        if key in idx:
            return idx[key]
    return None

def flexbox_entries(params):
    """Yields (group_label_or_None, display_name, link_target, style) for one
    {{Flexbox}} call - either the object/link/caption named form (structural
    style variants) or a plain pipe-separated name list with "break"/
    "break:Label" dividers (everything else)."""
    obj_idxs = sorted(int(re.match(r"object(\d+)$", k).group(1)) for k in params if re.match(r"object\d+$", k))
    if obj_idxs:
        group = None
        lead = params.get("1", "")
        if lead.strip().lower().startswith("break:"):
            group = clean(lead.split(":", 1)[1])
        for i in obj_idxs:
            obj = params.get("object%d" % i, "")
            link = params.get("link%d" % i, "")
            caption = params.get("caption%d" % i, "")
            page, _, anchor = link.partition("#")
            name = clean(caption) or clean(obj)
            if name:
                yield (group, name, clean(page) or clean(obj), clean(anchor) or None)
        return
    group, i = None, 1
    while str(i) in params:
        v = params[str(i)].strip()
        low = v.lower()
        if low == "break":
            pass
        elif low.startswith("break:"):
            group = clean(v.split(":", 1)[1])
        elif v:
            name = clean(v)
            if name:
                yield (group, name, name, None)
        i += 1

def parse_buildings_page(wt):
    start = wt.index("==List of buildings==")
    body = wt[start:]
    end_m = re.search(r"(?m)^==[^=].*?==\s*$", body[len("==List of buildings=="):])
    if end_m:
        body = body[:len("==List of buildings==") + end_m.start()]

    cats = []
    cat_ms = list(re.finditer(r"(?m)^===([^=\n]+)===\s*$", body))
    for ci, cm in enumerate(cat_ms):
        cat_label = clean(cm.group(1))
        c_end = cat_ms[ci + 1].start() if ci + 1 < len(cat_ms) else len(body)
        cat_text = body[cm.end():c_end]
        subcats = []
        sub_ms = list(re.finditer(r"(?m)^====([^=\n]+)====\s*$", cat_text))
        for si, sm in enumerate(sub_ms):
            sub_label = clean(sm.group(1))
            s_end = sub_ms[si + 1].start() if si + 1 < len(sub_ms) else len(cat_text)
            sub_text = cat_text[sm.end():s_end]
            entries = []
            for _, params, _, _ in templates(sub_text, r"Flexbox"):
                entries.extend(flexbox_entries(params))
            subcats.append((sub_label, entries))
        cats.append((cat_label, subcats))
    return cats

def slugify(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")

def main():
    wiki = WikiData()
    b = json.load(open(os.path.join(HERE, "wiki_buckets.json"), encoding="utf-8"))
    build_rows = [r for r in b["recipe"] if r.get("uses_facility") and "Build Menu" in str(r["uses_facility"])]
    recipe_idx = build_recipe_index(wiki, build_rows)

    page_wt = fetch_buildings_page()
    cats = parse_buildings_page(page_wt)

    out, total, missed = [], 0, []
    seen_names = set()
    for cat_label, subcats in cats:
        sub_out = []
        for sub_label, entries in subcats:
            by_group = {}
            for group_label, name, link_target, style in entries:
                rec = resolve(recipe_idx, name, link_target, style)
                if not rec:
                    missed.append("%s / %s: %s" % (cat_label, sub_label, name))
                    continue
                item = dict(rec, name=name)
                by_group.setdefault(group_label or "", []).append(item)
                seen_names.add(link_target)
            # A lone group named after its own subcategory ("Basic survival"
            # containing a "Basic Survival" group) is just the wiki's own
            # redundant labelling - collapse it to ungrouped.
            if len(by_group) == 1:
                only_label = next(iter(by_group))
                if only_label.strip().lower() == sub_label.strip().lower():
                    by_group[""] = by_group.pop(only_label)
            groups = [{"label": g, "items": items} for g, items in by_group.items() if items]
            if groups:
                # A representative icon for the tile itself - whichever of
                # this subcategory's own items has one, same personal-touch
                # idea as the chest and station icons.
                sub_img = next((it["img"] for g in groups for it in g["items"] if it.get("img")), "")
                sub_out.append({"key": slugify(sub_label), "label": sub_label, "groups": groups, "img": sub_img})
                total += sum(len(g["items"]) for g in groups)
        if sub_out:
            cat_img = next((s["img"] for s in sub_out if s.get("img")), "")
            out.append({"key": slugify(cat_label), "label": cat_label, "subcats": sub_out, "img": cat_img})

    header = ("/* Generated by .research/fetch_construction_data.py from the RuneScape: Dragonwilds\n"
              "   Wiki's Buildings page and Build Menu recipes. Do not edit by hand. */\n")
    js = header + "window.WILDS_CONSTRUCTION = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "construction.js"), "w", encoding="utf-8").write(js.replace("—", " - "))

    all_build_names = {r["page_name"] for r in build_rows}
    uncovered = sorted(all_build_names - seen_names)
    print("construction items: %d across %d categories (%d subcats)" % (
        total, len(out), sum(len(c["subcats"]) for c in out)), file=sys.stderr)
    if missed:
        print("unresolved menu entries (%d):" % len(missed), file=sys.stderr)
        for m in missed[:40]:
            print("  " + m, file=sys.stderr)
    print("Build Menu items never listed on the Buildings page (%d):" % len(uncovered), file=sys.stderr)
    for n in uncovered[:40]:
        print("  " + n, file=sys.stderr)

if __name__ == "__main__":
    main()
