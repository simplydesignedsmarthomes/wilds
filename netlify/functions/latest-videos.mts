/* Returns the N most recent video IDs for a YouTube channel, newest first.
 *
 *   GET /api/latest-videos?channelId=UC...&count=25
 *
 * Scrapes the channel's own /videos page (no API key, no quota) since the
 * public RSS feed caps out at 15 entries. Runs server-side so the browser
 * never has to fight YouTube's CORS policy, and the response is cached at
 * the edge for a few minutes so a burst of app opens doesn't hammer
 * YouTube on every single load.
 */

const ID_RE = /"videoId":"([A-Za-z0-9_-]{11})"/g;

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "public, max-age=600",
      "access-control-allow-origin": "*"
    }
  });
}

export default async (req: Request) => {
  const url = new URL(req.url);
  const channelId = (url.searchParams.get("channelId") || "").trim();
  const count = Math.min(50, Math.max(1, Number(url.searchParams.get("count")) || 25));

  if (!/^UC[A-Za-z0-9_-]{22}$/.test(channelId)) {
    return json({ error: "bad channelId" }, 400);
  }

  try {
    const res = await fetch(`https://www.youtube.com/channel/${channelId}/videos`, {
      headers: {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "accept-language": "en-US,en;q=0.9"
      }
    });
    if (!res.ok) return json({ error: "upstream " + res.status }, 502);

    const html = await res.text();
    const seen = new Set<string>();
    const ids: string[] = [];
    let m: RegExpExecArray | null;
    while ((m = ID_RE.exec(html)) && ids.length < count) {
      if (!seen.has(m[1])) {
        seen.add(m[1]);
        ids.push(m[1]);
      }
    }
    if (!ids.length) return json({ error: "no videos found" }, 502);
    return json({ ids, fetched: new Date().toISOString() });
  } catch (e) {
    return json({ error: "fetch failed" }, 502);
  }
};

export const config = { path: "/api/latest-videos" };
