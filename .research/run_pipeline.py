"""Orchestrates one full data-refresh cycle for the update-check workflow.

  1. Is there a newer Update: page on the wiki than last_update_seen.json?
     If not, exit 0 immediately (nothing else runs - cheap and polite).
  2. discover_new_items.py - file any brand-new item the wiki added.
  3. build_storage.py (pass 1) - so new names exist for step 4 to fetch.
  4. fetch_wiki_data.py - refresh buckets/wikitext/images, including new items.
  5. fetch_map_data.py, fetch_updates_data.py - refresh the rest of the data.
  6. build_storage.py (pass 2) - now fully hydrated.
  7. audit_items.py --json, diffed against audit_baseline.json.
  8. Write .research/_ci_result.json: {"changed": bool, "needsReview": bool,
     "summary": str} for the workflow to act on, and advance
     last_update_seen.json / audit_baseline.json when publishing clean.

Everything here is deterministic Python - no judgement calls. The one place
this intentionally stops short is a new item with an ambiguous type (see
discover_new_items.py) or a brand-new audit flag; those always come back as
needsReview so a person decides, instead of a guess going live unreviewed.
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request

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
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 3)

def run(*args):
    print("+ " + " ".join(args), file=sys.stderr)
    subprocess.check_call([sys.executable] + list(args), cwd=ROOT)

def newest_update_pages():
    d = get({"action": "query", "list": "recentchanges", "rcnamespace": "100", "rctype": "new",
             "rclimit": "20", "rcprop": "title|timestamp|ids", "format": "json"})
    return d["query"]["recentchanges"]

def write_result(changed, needs_review, summary):
    json.dump({"changed": changed, "needsReview": needs_review, "summary": summary},
               open(os.path.join(HERE, "_ci_result.json"), "w"), indent=1)
    print(summary, file=sys.stderr)

def main():
    seen_path = os.path.join(HERE, "last_update_seen.json")
    seen = json.load(open(seen_path, encoding="utf-8")) if os.path.exists(seen_path) else {"pageid": 0}

    recent = newest_update_pages()
    fresh = [p for p in recent if p["pageid"] > seen.get("pageid", 0)]
    if not fresh:
        write_result(False, False, "No new Update: pages since \"%s\"." % seen.get("title", "(none)"))
        return

    fresh.sort(key=lambda p: p["timestamp"])
    titles = [p["title"] for p in fresh]
    print("new update pages: %s" % ", ".join(titles), file=sys.stderr)

    run(".research/discover_new_items.py")
    review = json.load(open(os.path.join(HERE, "needs-review.json"), encoding="utf-8"))

    run(".research/build_storage.py")
    run(".research/fetch_wiki_data.py")
    run(".research/fetch_map_data.py")
    run(".research/fetch_updates_data.py")
    run(".research/build_storage.py")

    audit_out = os.path.join(HERE, "_audit_run.json")
    run(".research/audit_items.py", "--json", audit_out)
    flagged = json.load(open(audit_out, encoding="utf-8"))
    baseline_path = os.path.join(HERE, "audit_baseline.json")
    baseline = json.load(open(baseline_path, encoding="utf-8")) if os.path.exists(baseline_path) else {}
    new_flags = {name: fl for name, fl in flagged.items()
                 if fl != baseline.get(name) and not set(fl) <= set(baseline.get(name, []))}
    os.remove(audit_out)

    newest = max(fresh, key=lambda p: p["pageid"])
    json.dump({"pageid": newest["pageid"], "title": newest["title"], "timestamp": newest["timestamp"]},
              open(seen_path, "w"), indent=1)

    lines = ["Triggered by: " + ", ".join(titles)]
    if review:
        lines.append("%d new item(s) need a chest assigned by hand:" % len(review))
        lines += ["  - %s (%s) - %s" % (r["name"], r["type"], r["wikiUrl"]) for r in review]
    if new_flags:
        lines.append("%d item(s) have a new audit flag:" % len(new_flags))
        lines += ["  - %s: %s" % (n, ",".join(f)) for n, f in sorted(new_flags.items())]
    needs_review = bool(review or new_flags)
    if not needs_review:
        json.dump(flagged, open(baseline_path, "w", encoding="utf-8"), sort_keys=True, indent=1)
        lines.append("Clean - publishing straight to main.")
    else:
        lines.append("Needs a look before this goes live - opening a pull request instead.")
    write_result(True, needs_review, "\n".join(lines))

if __name__ == "__main__":
    main()
