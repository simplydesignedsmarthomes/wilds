"""One canonical shape for every item's detail, built from the wiki's own
structured data (see fetch_wiki_data.py) rather than from whichever research
pass happened to catch an item. Earlier passes each serialized recipes their
own way (at least eight formats) and armour alone carried three label
schemes, so the app rendered items inconsistently. Everything below produces:

  detail = {
    "stats":   [{"label", "value"}],       canonical labels, canonical order
    "recipes": [{"station", "skills": [{"name","xp"}], "materials": [chip],
                 "output": chip, "unlock"}],
    "usedIn":  [chip + "station"],          inverted from every recipe
    "sources": [{"source", "qty", "rarity"}],
    "shops":   [{"seller", "mode", "cost", "currency"}],
    "perks":   [{"name", "desc"}],
    "description": "intro\\n\\n(Journal)\\njournal",
  }
  chip = {"name", "qty", "img"}
"""
import html, json, os, re
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- wikitext template parsing ----------

def _match_close(wt, j):
    depth, p = 0, j
    while p < len(wt):
        if wt.startswith("{{", p):
            depth += 1; p += 2; continue
        if wt.startswith("}}", p):
            depth -= 1; p += 2
            if depth == 0:
                return p
            continue
        p += 1
    return len(wt)

def _split_params(body):
    parts, dt, dl, cur, i = [], 0, 0, "", 0
    while i < len(body):
        two = body[i:i + 2]
        if two == "{{": dt += 1; cur += two; i += 2; continue
        if two == "}}": dt -= 1; cur += two; i += 2; continue
        if two == "[[": dl += 1; cur += two; i += 2; continue
        if two == "]]": dl -= 1; cur += two; i += 2; continue
        if body[i] == "|" and dt == 0 and dl == 0:
            parts.append(cur); cur = ""
        else:
            cur += body[i]
        i += 1
    parts.append(cur)
    params, pos = {}, 0
    for p in parts[1:]:
        if "=" in p and not p.lstrip().startswith("{{"):
            k, v = p.split("=", 1)
            params[k.strip().lower()] = v.strip()
        else:
            pos += 1
            params[str(pos)] = p.strip()
    return params

def templates(wt, name_re):
    out, i = [], 0
    while True:
        j = wt.find("{{", i)
        if j < 0:
            return out
        m = re.match(r"\s*([^|{}\n]+)", wt[j + 2:])
        name = m.group(1).strip() if m else ""
        end = _match_close(wt, j)
        if re.fullmatch(name_re, name, re.I):
            out.append((name, _split_params(wt[j + 2:end - 2]), j, end))
            i = end
        else:
            i = j + 2

def _template_text(m):
    # Inline templates like {{plink|Ash Logs}} or {{RSL|Lowerniel Drakan|Lord
    # Drakan}}: the last positional argument is the text the wiki displays.
    args = [x for x in m.group(2).split("|") if "=" not in x]
    return args[-1] if args else ""

def clean(v, keep_paragraphs=False):
    if not v:
        return ""
    v = re.sub(r"<!--.*?-->", "", v, flags=re.S)
    v = re.sub(r"<ref[^>]*/>", "", v)
    v = re.sub(r"<ref[^>]*>.*?</ref>", "", v, flags=re.S)
    # Magic words (__NOTOC__, __TOC__, ...) carry no reader-facing meaning,
    # so they're just dropped; "==Heading==" section markup keeps its text
    # (still a real sentence worth reading) but loses the == fencing, which
    # otherwise shows up verbatim in a stripped-down summary like the
    # Updates tab's.
    v = re.sub(r"__[A-Z]+__", "", v)
    v = re.sub(r"^\s*=+\s*(.*?)\s*=+\s*$", r"\1", v, flags=re.M)
    v = re.sub(r"<br\s*/?>", "\n" if keep_paragraphs else "; ", v, flags=re.I)
    v = re.sub(r"\[\[(?:File|Image):[^\]]*\]\]", "", v, flags=re.I)
    v = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", v)
    v = re.sub(r"\[\[([^\]]+)\]\]", r"\1", v)
    v = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", v)
    for _ in range(6):
        v2 = re.sub(r"\{\{\s*sic\s*\}\}", "", v, flags=re.I)
        v2 = re.sub(r"\{\{([^{}|]+)\|([^{}]*)\}\}", _template_text, v2)
        v2 = re.sub(r"\{\{[^{}]*\}\}", "", v2)
        if v2 == v:
            break
        v = v2
    v = re.sub(r"'''?", "", v)
    v = re.sub(r"<[^>]+>", "", v)
    v = html.unescape(v).replace(" ", " ")
    v = re.sub(r"\s*—\s*", " - ", v)
    if keep_paragraphs:
        paras = [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", v)]
        return "\n\n".join(p.replace("\n", " ") for p in paras if p)
    return re.sub(r"\s+", " ", v).strip(" ;")

# ---------- stats ----------

STAT_MAP = {
    "item_type": "Type", "type": "Type",
    "power": "Power level",
    "damagetype": "Damage type",
    "attackstyle": "Attack style",
    "basedmg": "Base damage", "base damage": "Base damage",
    "runedamage": "Rune damage",
    "additionaldmg": "Additional damage",
    "damagemulti": "Damage multiplier",
    "criticalchance": "Critical chance",
    "reloadspeed": "Reload speed",
    "combo": "Attack combo",
    "block": "Block",
    "specialaction": "Special action",
    "specialeffect": "Special effect", "special effect": "Special effect",
    "meleedefence": "Melee defence",
    "rangeddefence": "Ranged defence", "rangedefence": "Ranged defence",
    "magicdefence": "Magic defence",
    "setbonus1": "Set bonus 1", "setbonus2": "Set bonus 2", "setbonus3": "Set bonus 3",
    "carryweight": "Carry weight",
    "digvalue": "Dig value",
    "sustenance": "Sustenance",
    "health": "Health",
    "hydration": "Hydration",
    "duration": "Duration",
    "compostvalue": "Compost value",
    "resist shocked buildup": "Shock resistance",
    "durability": "Durability", "durabiliity": "Durability",
    "repaircost": "Repair cost",
    "weight": "Weight",
    "stacklimit": "Stack limit",
    "description": "Description",
    "catalogue": "Build category",
    "location": "Location",
    "respawn": "Respawn time",
    "source": "Source",
}
STAT_ORDER = [
    "Type", "Power level", "Released", "Versions",
    "Damage type", "Attack style", "Base damage", "Rune damage", "Additional damage",
    "Damage multiplier", "Critical chance", "Reload speed", "Attack combo", "Block",
    "Special action", "Special effect",
    "Melee defence", "Ranged defence", "Magic defence",
    "Set bonus 1", "Set bonus 2", "Set bonus 3",
    "Carry weight", "Dig value",
    "Sustenance", "Health", "Hydration", "Duration", "Shock resistance", "Compost value",
    "Durability", "Repair cost", "Weight", "Stack limit",
    "Build category", "Location", "Respawn time", "Source", "Removed in",
    "Description",
]
# Template plumbing, not facts about the item.
IGNORED_PARAMS = {"name", "image", "imagesizeh", "update", "release", "collection", "1",
                  "removalupdate", "perk", "perkdesc"}
STAT_TEMPLATES = r"Infobox (Item|Weapon|Armour|Trinket|Tool|Build|Perk|Resource Node)"

unknown_params = {}

# Just the date - the wiki's own "update" param is whatever patch/devblog
# name or promo blurb ("Our 1.0 Release is live!", "0.12 - Known Issues and
# Vital Information") was attached at the time, not a fact worth repeating.
def _release(p, n=""):
    return clean(p.get("release" + n, ""))

def parse_stats(wt):
    stats = {}
    infoboxes = templates(wt, STAT_TEMPLATES)
    for name, p, _, _ in infoboxes:
        versions = [clean(p[k]) for k in sorted(p) if re.fullmatch(r"version\d+", k) and clean(p[k])]
        if versions and "Versions" not in stats:
            stats["Versions"] = ", ".join(versions)
        if (p.get("release") or p.get("release1")) and "Released" not in stats:
            stats["Released"] = _release(p) if p.get("release") else _release(p, "1")
        if p.get("removalupdate"):
            stats["Removed in"] = clean(p["removalupdate"])
        for k, v in p.items():
            base = re.sub(r"1$", "", k) if re.fullmatch(r"[a-z_ ]+1", k) else k
            if k in IGNORED_PARAMS or re.fullmatch(r"(version|name|image|release|update)\d+", k):
                continue
            if re.fullmatch(r"[a-z_ ]+[2-9]", k) and not k.startswith("setbonus"):
                continue  # later versions' copies of a field; version 1 is the base item
            if re.fullmatch(r"perk\d*|perkdesc\d*", k):
                continue
            label = STAT_MAP.get(base) or STAT_MAP.get(k)
            if not label:
                unknown_params.setdefault(name + ":" + k, 0)
                unknown_params[name + ":" + k] += 1
                continue
            val = clean(v)
            if not val or label in stats:
                continue
            if label == "Weight" and re.fullmatch(r"[\d.]+", val):
                val += " kg"
            stats[label] = val
    return [{"label": l, "value": stats[l]} for l in STAT_ORDER if l in stats]

def parse_perks(wt):
    perks = []
    for _, p, _, _ in templates(wt, r"Infobox Bonus Perk"):
        for suffix in ["", "1", "2", "3"]:
            n, d = clean(p.get("perk" + suffix, "")), clean(p.get("perkdesc" + suffix, ""))
            if n and not any(x["name"] == n for x in perks):
                perks.append({"name": n, "desc": d})
    return perks

def parse_description(wt):
    head = re.split(r"\n==[^=]", wt, maxsplit=1)[0]
    for _, _, s, e in sorted(templates(head, r"[^|{}\n]+"), key=lambda t: -t[2]):
        head = head[:s] + head[e:]
    intro = clean(head, keep_paragraphs=True)
    journals = [clean(p.get("1", ""), keep_paragraphs=True) for _, p, _, _ in templates(wt, r"journal entry")]
    journals = [j for j in journals if j]
    out = intro
    if journals:
        out = (out + "\n\n" if out else "") + "(Journal)\n" + "\n\n".join(journals)
    return out

# ---------- bucket indexes ----------

FILE_RE = re.compile(r"\[\[File:([^|\]]+)")

# Spelling mismatches inside the wiki's own recipe templates, mapped to the
# name the actual item page uses, so the chip shows the right icon and name.
NAME_ALIASES = {"Garou Artifact": "Garou Artefact"}

def _qty(v):
    if v in (None, ""):
        return 1
    try:
        f = float(str(v).replace(",", ""))
        return int(f) if f.is_integer() else f
    except ValueError:
        return str(v)

def _load_cache(name, default):
    # These three are gitignored scrape caches, regenerated by
    # fetch_wiki_data.py - never committed, and never present on a brand
    # new checkout. run_pipeline.py's first build_storage.py pass runs
    # BEFORE fetch_wiki_data.py on purpose (so newly-discovered item names
    # exist for it to go fetch), which on a fresh CI runner means this is
    # the very first time WikiData() is ever constructed there - treat a
    # missing cache as "nothing scraped yet" rather than crashing; that
    # first pass's job is just to seed names, and the second pass (after
    # fetch_wiki_data.py has run) re-populates everything for real.
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return default
    return json.load(open(path, encoding="utf-8"))

class WikiData:
    def __init__(self):
        b = _load_cache("wiki_buckets.json", {"recipe": [], "dropsline": [], "storeline": []})
        w = _load_cache("wiki_wikitext.json", {"pages": {}, "redirects": {}})
        self.images = _load_cache("wiki_images.json", {})
        self.pages, self.redirects = w["pages"], w["redirects"]
        self.recipes_by_output, self.used_in = OrderedDict(), OrderedDict()
        seen = set()
        for row in b["recipe"]:
            try:
                j = json.loads(row.get("json") or "{}")
            except ValueError:
                continue
            out = j.get("output") if isinstance(j.get("output"), dict) else {}
            out_name = (out.get("name") or (j.get("outputs") or [None])[0] or "").strip()
            if not out_name:
                continue
            mats = [self._chip(m.get("name"), m.get("quantity"), m.get("image")) for m in (j.get("materials") or [])]
            mats = [m for m in mats if m["name"]]
            rec = {
                "station": (j.get("facility") or "").strip(),
                "skills": [{"name": (s.get("name") or "").strip(), "xp": _qty(s.get("experience"))}
                           for s in (j.get("skills") or []) if s.get("name")],
                "materials": mats,
                "output": self._chip(out_name, out.get("quantity"), out.get("image")),
                "unlock": clean(j.get("recipe") or ""),
            }
            self._add_recipe(rec, seen)
        # Some recipe templates are marked `bucket = no` (variant or removed
        # recipes the wiki keeps out of its central table). They're the same
        # {{Recipe}} template with the same fields, so read them straight off
        # the page and they come out identical to the bucket-fed ones.
        for title, wt in self.pages.items():
            for _, p, _, _ in templates(wt, r"Recipe"):
                if p.get("bucket", "").strip().lower() != "no":
                    continue
                rec = self._recipe_from_template(p, title)
                if rec:
                    self._add_recipe(rec, seen)
        self.sources = OrderedDict()
        for row in b["dropsline"]:
            try:
                j = json.loads(row.get("json") or "{}")
            except ValueError:
                continue
            item = (j.get("Dropped item") or row.get("item_name") or "").strip()
            src = {"source": clean(j.get("Dropped from") or row.get("page_name") or ""),
                   "qty": clean(str(j.get("Drop Quantity") or "")).replace("–", "-"),
                   "rarity": clean(str(j.get("Rarity") or ""))}
            lst = self.sources.setdefault(item.lower(), [])
            if src["source"] and src not in lst:
                lst.append(src)
        self.shops = OrderedDict()
        for row in b["storeline"]:
            try:
                j = json.loads(row.get("sold_item_json") or "{}")
            except ValueError:
                continue
            shop = {"seller": clean(j.get("Sold by") or row.get("page_name") or ""),
                    "mode": j.get("Mode") or "", "cost": _qty(j.get("Cost")),
                    "currency": clean(j.get("Currency") or "")}
            lst = self.shops.setdefault((row.get("sold_item") or "").strip().lower(), [])
            if shop not in lst:
                lst.append(shop)

    def _add_recipe(self, rec, seen):
        out_name = rec["output"]["name"]
        sig = (out_name.lower(), rec["station"], tuple((m["name"], str(m["qty"])) for m in rec["materials"]))
        if sig in seen:
            return
        seen.add(sig)
        self.recipes_by_output.setdefault(out_name.lower(), []).append(rec)
        for m in rec["materials"]:
            lst = self.used_in.setdefault(m["name"].lower(), [])
            if not any(u["name"] == out_name and u["station"] == rec["station"] for u in lst):
                lst.append(dict(rec["output"], station=rec["station"]))

    def _recipe_from_template(self, p, page_title):
        mats = []
        for i in range(1, 13):
            n = clean(p.get("mat%d" % i, ""))
            if n:
                mats.append(self._chip(n, p.get("mat%dqty" % i), "", p.get("mat%dpic" % i)))
        out_name = clean(p.get("output1", "")) or page_title
        skill = clean(p.get("skill", ""))
        return {
            "station": clean(p.get("facility", "")),
            "skills": [{"name": skill, "xp": _qty(clean(p.get("skillxp", "")) or 0)}] if skill else [],
            "materials": mats,
            "output": self._chip(out_name, p.get("output1qty"), "", p.get("output1pic")),
            "unlock": clean(p.get("recipe", "")),
        }

    def _chip(self, name, qty, image, pic=None):
        name = clean(name or "")
        if name in NAME_ALIASES:
            name, image = NAME_ALIASES[name], ""
        files = FILE_RE.findall(image or "")
        img = self.images.get(files[0].strip()) if files else ""
        if not img and pic:
            img = self.images.get(clean(pic) + ".png", "")
        if not img and name:
            img = self.images.get(name + ".png", "")
        return {"name": name, "qty": _qty(qty), "img": img or ""}

    def item_image(self, name):
        wt = self.page_for(name)
        for _, p, _, _ in templates(wt, STAT_TEMPLATES):
            f = re.sub(r"^\s*\[\[File:|\]\].*$|\|.*$", "", p.get("image") or p.get("image1") or "").strip()
            if f and self.images.get(f):
                return self.images[f]
        return ""

    def page_for(self, name):
        if name in self.pages:
            return self.pages[name]
        target = self.redirects.get(name)
        return self.pages.get(target, "") if target else ""

    def _keys(self, name):
        ks = [name.lower()]
        t = self.redirects.get(name)
        if t and t.lower() not in ks:
            ks.append(t.lower())
        bare = re.sub(r"\s*\(Removed\)$", "", name, flags=re.I)
        if bare.lower() not in ks:
            ks.append(bare.lower())
        return ks

    def lookup(self, index, name):
        for k in self._keys(name):
            if k in index:
                return index[k]
        return []

    def detail(self, name, fallback_description=""):
        wt = self.page_for(name)
        stats = parse_stats(wt) if wt else []
        if wt and re.search(r"\{\{\s*Future content", wt, re.I):
            stats = [s for s in stats if s["label"] != "Type"]
            stats.insert(0, {"label": "Type", "value": "Upcoming (not in the game yet)"})
        if wt and not any(s["label"] == "Type" for s in stats):
            # Buff, resource-node and buildable pages carry no item_type; name
            # the kind of page they are so every entry still leads with a Type.
            kinds = {"Perk": "Perk", "Resource Node": "Resource node", "Build": "Buildable"}
            for tname, _, _, _ in templates(wt, STAT_TEMPLATES):
                k = kinds.get(tname.replace("Infobox ", ""))
                if k:
                    stats.insert(0, {"label": "Type", "value": k})
                    break
        return {
            "stats": stats,
            "recipes": self.lookup(self.recipes_by_output, name),
            "usedIn": self.lookup(self.used_in, name),
            "sources": self.lookup(self.sources, name),
            "shops": self.lookup(self.shops, name),
            "perks": parse_perks(wt) if wt else [],
            "description": (parse_description(wt) if wt else "") or fallback_description,
        }
