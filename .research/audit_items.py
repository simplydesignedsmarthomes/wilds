"""Item-by-item audit of storage.js: every item must come out of the build in
the same canonical shape (see normalize_detail.py). Also diffs against the
previous committed storage.js, so a recipe the old data had but the new data
lost gets flagged instead of silently disappearing.

  python3 .research/audit_items.py            summary + every flagged item
  python3 .research/audit_items.py --all      one line per item, all 1061
  python3 .research/audit_items.py --json F   also write {name: [flags]} for every flagged item to F
"""
import json, re, subprocess, sys, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, ".research"))
from normalize_detail import STAT_ORDER

def load(text):
    m = re.search(r"window\.WILDS_STORAGE\s*=\s*(\[.*?\]);\s*window\.WILDS_STORAGE_MAX_STEP", text, re.S)
    return json.loads(m.group(1))

new = load(open(os.path.join(ROOT, "storage.js"), encoding="utf-8").read())
try:
    old = load(subprocess.check_output(["git", "show", "HEAD:storage.js"], cwd=ROOT).decode("utf-8"))
except Exception:
    old = []
old_by = {it["name"]: it for c in old for it in c["items"]}
RECIPEISH = re.compile(r"recipe|material|facility|crafting station|output", re.I)

problems, rows = Counter(), []
for cat in new:
    for it in cat["items"]:
        d, flags = it.get("detail") or {}, []
        keys = set(d)
        if keys != {"stats", "recipes", "usedIn", "sources", "shops", "perks", "description"}:
            flags.append("schema")
        labels = [s["label"] for s in d.get("stats", [])]
        if any(l not in STAT_ORDER for l in labels):
            flags.append("odd-label")
        if "Type" not in labels:
            flags.append("no-type")
        for r in d.get("recipes", []):
            if not r.get("station"):
                flags.append("recipe-no-station")
            if not r.get("output", {}).get("img"):
                flags.append("recipe-output-no-icon")
            if any(not m.get("img") for m in r.get("materials", [])):
                flags.append("material-no-icon")
        if any(not u.get("img") for u in d.get("usedIn", [])):
            flags.append("usedin-no-icon")
        if not d.get("description"):
            flags.append("no-description")
        if not it.get("img"):
            flags.append("no-item-image")
        o = old_by.get(it["name"])
        if o and not d.get("recipes"):
            had = [r for r in (o.get("detail") or {}).get("infobox", [])
                   if RECIPEISH.search(r["label"]) and not re.search(r"product|unlock", r["label"], re.I)]
            if had:
                flags.append("LOST-RECIPE")
        if "—" in json.dumps(it, ensure_ascii=False):
            flags.append("em-dash")
        flags = sorted(set(flags))
        for f in flags:
            problems[f] += 1
        rows.append((cat["key"], it["name"], len(d.get("stats", [])), len(d.get("recipes", [])),
                     len(d.get("usedIn", [])), len(d.get("sources", [])), len(d.get("shops", [])), flags))

total = len(rows)
print("audited %d items" % total)
print("items with recipes: %d | used-in: %d | drop sources: %d | shops: %d | perks: %d" % (
    sum(1 for r in rows if r[3]), sum(1 for r in rows if r[4]), sum(1 for r in rows if r[5]),
    sum(1 for r in rows if r[6]),
    sum(1 for c in new for it in c["items"] if it["detail"]["perks"])))
print("flags:", dict(problems) or "none")
show_all = "--all" in sys.argv
for r in rows:
    if show_all or r[7]:
        print("%-9s %-38s stats=%-2d recipes=%-2d usedIn=%-3d sources=%-2d shops=%-2d %s" % (
            r[0], r[1][:38], r[2], r[3], r[4], r[5], r[6], ",".join(r[7])))

if "--json" in sys.argv:
    out_path = sys.argv[sys.argv.index("--json") + 1]
    flagged = {name: flags for _, name, *_rest, flags in rows if flags}
    json.dump(flagged, open(out_path, "w", encoding="utf-8"), sort_keys=True, indent=1)
