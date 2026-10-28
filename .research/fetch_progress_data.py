"""Pull the two progression feeds the app's Progress tab can check off or
read against: Steam achievements, and the full per-level skill tables.

Both are additive to what's already there. level-unlocks.js stays the
hand-curated milestone list (with its own deliberately friendlier wording -
"Skillcape" where the wiki says "Cape"); this script does NOT touch it and
does not try to supersede it. What it adds is the wiki's own complete
<Skill>/Level up table subpage, every level rather than the milestones, so
the app can answer "what exactly do I get at 73" instead of only "what are
the big unlocks".

Those subpages come in two shapes and both are handled here:
  Level | Unlock                       (10 skills - the milestone cell says
                                        "'''Unlock:''' [[Name]]" then a
                                        "Description:" line, and every other
                                        level repeats one filler passive)
  Level | Ability | Type | Description (Agility and Runecrafting, which also
                                        type each entry Recipe/Passive/Spell/
                                        Ability/Unlock/Shortcut)
Either way the one passive that simply repeats on most levels is lifted out
as the skill's "perLevel" rather than written out ~80 times.

Steam achievements are one page each, all carrying {{Infobox Steam
achievement}}, listed in display order by the Steam Achievements hub page.
Each is tagged with a group and tier derived from its own internal
achievementname id (MiningNovice -> Mining/Novice, DefeatVelgar -> Bosses,
Ghornfell_QuestAchievement -> Region quests), so the app can group them
however it likes without re-deriving that.

Writes achievements.js (window.WILDS_ACHIEVEMENTS) and skill-tables.js
(window.WILDS_SKILL_TABLES). Re-run any time; always reflects the wiki as
it currently stands.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import clean, templates

API = "https://dragonwilds.runescape.wiki/api.php"
UA = "wilds-companion-data-refresh/1.0 (personal fan companion app)"

# Same order skills.js uses, so the two line up without the app re-sorting.
SKILLS = ["Attack", "Magic", "Ranged", "Mining", "Woodcutting", "Artisan",
          "Construction", "Cooking", "Runecrafting", "Farming", "Fishing", "Agility"]

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

def fetch_pages(titles):
    """title -> wikitext, batched at MediaWiki's own 50-title limit."""
    out, titles = {}, list(titles)
    for i in range(0, len(titles), 50):
        d = get({"action": "query", "titles": "|".join(titles[i:i + 50]), "prop": "revisions",
                 "rvprop": "content", "rvslots": "main", "format": "json", "formatversion": "2"})
        for p in d["query"]["pages"]:
            if "revisions" in p:
                out[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
        time.sleep(0.4)
    return out

def fetch_image_urls(filenames):
    urls, names = {}, sorted(set(n for n in filenames if n))
    for i in range(0, len(names), 50):
        d = get({"action": "query", "prop": "imageinfo", "iiprop": "url", "format": "json",
                 "formatversion": "2", "titles": "|".join("File:" + n for n in names[i:i + 50])})
        for p in d.get("query", {}).get("pages", []):
            if p.get("imageinfo"):
                urls[p["title"][len("File:"):]] = p["imageinfo"][0]["url"]
        time.sleep(0.4)
    return urls

# ---------- wikitable ----------

def first_table(wt):
    """The page's first {| ... |} block. The skill pages that carry a second
    table (Cooking's burn-chance breakdown) only ever want the first."""
    start = wt.find("{|")
    if start < 0:
        return ""
    depth, i = 0, start
    while i < len(wt):
        if wt.startswith("{|", i):
            depth += 1
            i += 2
        elif wt.startswith("|}", i):
            depth -= 1
            i += 2
            if depth == 0:
                return wt[start:i]
        else:
            i += 1
    return wt[start:]

def table_rows(tbl):
    """Each |- separated row as a list of raw cell strings. A line that
    doesn't open with | or ! continues the cell above it, which is what
    carries the "Description:" second line in the two-column tables."""
    rows = []
    for chunk in re.split(r"^\s*\|-.*$", tbl, flags=re.M)[1:]:
        cells = []
        for line in chunk.split("\n"):
            s = line.strip()
            if s in ("", "|}") or s.startswith("{|"):
                continue
            if s.startswith("!"):
                cells.extend(p.strip() for p in s.lstrip("!").split("!!"))
            elif s.startswith("|"):
                cells.extend(p.strip() for p in s[1:].split("||"))
            elif cells:
                cells[-1] += "\n" + s
        if cells:
            rows.append(cells)
    return rows

def header_cells(tbl):
    """Every ! header cell, whether the table writes them on one line
    ("! Level !! Unlock") or one per line, as Agility and Runecrafting do."""
    out = []
    for line in tbl.split("\n"):
        s = line.strip()
        if s.startswith("!"):
            out.extend(clean(p).lower() for p in s.lstrip("!").split("!!"))
        elif out and s.startswith("|-"):
            break
    return out

# ---------- skill level tables ----------

UNLOCK_RE = re.compile(r"'''\s*Unlock\s*:?\s*'''\s*:?\s*(.*)", re.I)
# Some tables italicise the label ("''Description:''"), some don't.
DESC_RE = re.compile(r"^\s*'*\s*Description\s*:?\s*'*\s*(.*)", re.I | re.M)

def parse_two_col(cells):
    """Level | Unlock. Returns (name, type, desc) - name empty for the filler
    passive rows, which the caller folds into perLevel."""
    body = cells[1] if len(cells) > 1 else ""
    m = UNLOCK_RE.search(body)
    if not m:
        # Artisan, Farming and Fishing skip the "Unlock:" label and just
        # write "[[Thing]] unlocked". A link, or that trailing word on its
        # own, is the giveaway - the scaling filler ("+0.3% seed recovery
        # chance") has neither.
        txt = clean(body)
        if "[[" in body or re.search(r"\bunlocked$", txt, re.I):
            return re.sub(r"\s+unlocked$", "", txt, flags=re.I), "Unlock", ""
        return "", "", txt
    name = clean(m.group(1).split("\n")[0])
    # "[[Mighty Oak]] unlocked" - the trailing verb isn't part of the name.
    name = re.sub(r"\s+unlocked$", "", name, flags=re.I)
    d = DESC_RE.search(body)
    desc = clean(d.group(1)) if d else ""
    if not desc:
        # No "Description:" line - whatever follows the unlock is the blurb.
        rest = body[m.end():].strip()
        desc = clean(rest)
    return name, "Unlock", desc

def parse_four_col(cells):
    name = clean(cells[1]) if len(cells) > 1 else ""
    typ = clean(cells[2]) if len(cells) > 2 else ""
    desc = clean(cells[3]) if len(cells) > 3 else ""
    return name, typ, desc

def parse_skill_table(wt):
    tbl = first_table(wt)
    if not tbl:
        return None
    four = len(header_cells(tbl)) >= 4
    always, entries = [], []
    for cells in table_rows(tbl):
        lvl_raw = clean(cells[0]) if cells else ""
        if not lvl_raw:
            continue
        name, typ, desc = parse_four_col(cells) if four else parse_two_col(cells)
        if lvl_raw.lower() == "all":
            # Agility states its global passive as a single "All" row.
            always.append({"desc": desc or name, "from": 1, "to": 99})
            continue
        if not re.fullmatch(r"\d+", lvl_raw):
            continue
        entries.append({"level": int(lvl_raw), "name": name, "type": typ, "desc": desc})
    entries.sort(key=lambda e: e["level"])

    # Separate real unlocks from the per-level scaling that just repeats.
    # In the two-column tables an unlock is exactly a row that carried the
    # "'''Unlock:'''" marker, so anything nameless is scaling (and a blank
    # cell, as Construction uses, is simply nothing at that level). The
    # four-column tables name their filler too, so there it's the one
    # name/description pairing that recurs on most levels.
    if four:
        counts = {}
        for e in entries:
            counts[(e["name"], e["desc"])] = counts.get((e["name"], e["desc"]), 0) + 1
        top = max(counts, key=lambda k: counts[k]) if counts else None
        is_filler = (lambda e: (e["name"], e["desc"]) == top) if top and counts[top] >= 15 else (lambda e: False)
    else:
        is_filler = lambda e: not e["name"]

    rows = [e for e in entries if not is_filler(e)]
    # A few unlocks are listed twice a level apart, once properly and once as
    # bare text - keep whichever copy actually carries the description.
    best = {}
    for e in rows:
        k = re.sub(r"\W", "", e["name"]).lower()
        if k and (k not in best or len(e["desc"]) > len(best[k]["desc"])):
            best[k] = e
    rows = sorted(best.values(), key=lambda e: e["level"]) if best else rows
    # Cooking's scaling changes text every power tier, so record each
    # distinct one with the span of levels it covers rather than assuming
    # a single passive across the whole skill.
    spans = {}
    for e in entries:
        # A blank cell, or a literal "None", means nothing happens at that
        # level - not a passive worth reporting.
        if not is_filler(e) or e["desc"].strip().lower() in ("", "none", "-"):
            continue
        # Keyed loosely so a stray typo ("-0.5%attack" vs "-0.5% attack")
        # doesn't split one passive into two spans.
        key = re.sub(r"\W", "", e["desc"]).lower()
        s = spans.setdefault(key, {"desc": e["desc"], "from": e["level"], "to": e["level"]})
        s["from"] = min(s["from"], e["level"])
        s["to"] = max(s["to"], e["level"])
    per_level = always + sorted(spans.values(), key=lambda s: s["from"])
    return {"perLevel": per_level, "rows": rows}

def build_skill_tables():
    pages = fetch_pages(s + "/Level up table" for s in SKILLS)
    out = {}
    for s in SKILLS:
        wt = pages.get(s + "/Level up table")
        if not wt:
            print("  no level up table: %s" % s, file=sys.stderr)
            continue
        parsed = parse_skill_table(wt)
        if parsed:
            out[s] = parsed
    header = ("/* Generated by .research/fetch_progress_data.py from each skill's own\n"
              "   <Skill>/Level up table page on the RuneScape: Dragonwilds Wiki. The\n"
              "   complete per-level list; level-unlocks.js remains the curated\n"
              "   milestone view. Do not edit by hand. */\n")
    js = header + "window.WILDS_SKILL_TABLES = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "skill-tables.js"), "w", encoding="utf-8").write(js.replace("—", " - "))
    for s in SKILLS:
        if s in out:
            pl = out[s]["perLevel"]
            print("  %-13s %3d unlocks  %d per-level: %s" % (
                s, len(out[s]["rows"]), len(pl), (pl[0]["desc"][:44] if pl else "-")), file=sys.stderr)
    return out

# ---------- steam achievements ----------

TIERS = ("Novice", "Veteran", "Mastery")

def achievement_group(ach_id, skills):
    """Group/tier straight off the internal id the infobox carries."""
    if not ach_id:
        return "Other", ""
    if ach_id.startswith("Defeat"):
        return "Bosses", ""
    if ach_id.endswith("_QuestAchievement"):
        return "Region quests", ""
    for t in TIERS:
        if ach_id.endswith(t):
            stem = ach_id[:-len(t)]
            if stem in skills:
                return stem, t
            return "Hidden", t     # Hidden1Novice and friends
    return "Other", ""

HUB_ROW_RE = re.compile(r'data-rowid="([^"]+)"')

def build_achievements():
    d = get({"action": "query", "list": "categorymembers", "cmtitle": "Category:Steam achievements",
             "cmlimit": "500", "format": "json", "formatversion": "2"})
    titles = [m["title"] for m in d["query"]["categorymembers"] if m["title"] != "Steam Achievements"]
    pages = fetch_pages(titles)

    hub = fetch_pages(["Steam Achievements"]).get("Steam Achievements", "")
    hub_order = {rid: i for i, rid in enumerate(HUB_ROW_RE.findall(hub))}

    skills = set(SKILLS)
    rows, files = [], []
    for title in titles:
        wt = pages.get(title)
        if not wt:
            continue
        params = {}
        for _, p, _, _ in templates(wt, r"Infobox Steam achievement"):
            params = p
            break
        if not params:
            continue
        name = clean(params.get("name")) or title
        img_file = (params.get("image") or "").strip()
        ach_id = (params.get("achievementname") or "").strip()
        group, tier = achievement_group(ach_id, skills)
        if img_file:
            files.append(img_file)
        rows.append({
            "name": name, "_file": img_file, "desc": clean(params.get("description")),
            "id": ach_id, "group": group, "tier": tier,
            "release": clean(params.get("release")), "update": clean(params.get("update")),
            "wikiUrl": "https://dragonwilds.runescape.wiki/w/" + urllib.parse.quote(title.replace(" ", "_")),
        })

    urls = fetch_image_urls(files)
    for r in rows:
        r["img"] = urls.get(r.pop("_file"), "")

    # The hub page's own table order (every Novice, then Veteran, ...) is the
    # order players see on Steam; anything not in it trails alphabetically.
    rows.sort(key=lambda r: (hub_order.get(r["id"], len(hub_order)), r["name"]))

    # Groups in a sensible reading order: the twelve skills as skills.js has
    # them, then the cross-cutting ones.
    seen = {r["group"] for r in rows}
    order = [s for s in SKILLS if s in seen] + [g for g in ("Bosses", "Region quests", "Hidden", "Other") if g in seen]
    groups = [{"key": g, "count": sum(1 for r in rows if r["group"] == g)} for g in order]

    header = ("/* Generated by .research/fetch_progress_data.py from the RuneScape: Dragonwilds\n"
              "   Wiki's Steam achievement pages. Do not edit by hand. */\n")
    payload = {"groups": groups, "achievements": rows}
    js = header + "window.WILDS_ACHIEVEMENTS = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "achievements.js"), "w", encoding="utf-8").write(js.replace("—", " - "))
    print("  achievements: %d, with icon: %d, groups: %d" % (
        len(rows), sum(1 for r in rows if r["img"]), len(groups)), file=sys.stderr)
    missing = [r["name"] for r in rows if not r["id"]]
    if missing:
        print("  no achievementname on the wiki (grouped Other): %s" % ", ".join(missing), file=sys.stderr)
    return payload

def main():
    print("skill level tables:", file=sys.stderr)
    build_skill_tables()
    print("steam achievements:", file=sys.stderr)
    build_achievements()

if __name__ == "__main__":
    main()
