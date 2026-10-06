/* Paginated video IDs for a YouTube channel, newest first.
 *
 *   GET /api/latest-videos?channelId=UC...                  -> first page
 *   GET /api/latest-videos?channelId=UC...&cursor=<opaque>  -> next page
 *
 * First page scrapes the channel's own /videos page (no API key, no
 * quota). Every page YouTube serves there also embeds a continuation
 * token for the next batch - the same mechanism the site's own infinite
 * scroll uses - so subsequent pages replay that as a POST to YouTube's
 * internal browse endpoint. `cursor` is opaque to the client: it's just
 * the token/apiKey/clientVersion bundle needed to ask for the next
 * batch, base64'd. A null `cursor` in the response means there are no
 * more videos to load. Runs server-side so the browser never has to
 * fight YouTube's CORS policy.
 */

const THUMB_ID_RE = /\/vi\/([A-Za-z0-9_-]{11})\//g;
// The initial HTML page is minified, but the continuation endpoint's JSON
// response comes back pretty-printed (newlines and spaces between every
// token) - so this can't assume compact "key":"value" with no whitespace.
const CONTINUATION_RE = /"trigger"\s*:\s*"CONTINUATION_TRIGGER_ON_ITEM_SHOWN"[\s\S]*?"continuationCommand"\s*:\s*\{\s*"token"\s*:\s*"([^"]+)"/;
const API_KEY_RE = /"INNERTUBE_API_KEY"\s*:\s*"([^"]+)"/;
const CLIENT_VERSION_RE = /"INNERTUBE_CONTEXT_CLIENT_VERSION"\s*:\s*"([^"]+)"/;
const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";

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

function extractIds(text: string): string[] {
  const seen = new Set<string>();
  const ids: string[] = [];
  let m: RegExpExecArray | null;
  THUMB_ID_RE.lastIndex = 0;
  while ((m = THUMB_ID_RE.exec(text))) {
    if (!seen.has(m[1])) {
      seen.add(m[1]);
      ids.push(m[1]);
    }
  }
  return ids;
}

type Cursor = { token: string; apiKey: string; clientVersion: string };

function encodeCursor(c: Cursor): string {
  return Buffer.from(JSON.stringify(c)).toString("base64url");
}
function decodeCursor(s: string): Cursor | null {
  try {
    const c = JSON.parse(Buffer.from(s, "base64url").toString("utf-8"));
    if (c && typeof c.token === "string" && typeof c.apiKey === "string" && typeof c.clientVersion === "string") return c;
  } catch {}
  return null;
}

export default async (req: Request) => {
  const url = new URL(req.url);
  const channelId = (url.searchParams.get("channelId") || "").trim();
  const cursorParam = url.searchParams.get("cursor");

  if (!/^UC[A-Za-z0-9_-]{22}$/.test(channelId)) {
    return json({ error: "bad channelId" }, 400);
  }

  try {
    if (!cursorParam) {
      const res = await fetch(`https://www.youtube.com/channel/${channelId}/videos`, {
        headers: { "user-agent": UA, "accept-language": "en-US,en;q=0.9" }
      });
      if (!res.ok) return json({ error: "upstream " + res.status }, 502);
      const html = await res.text();

      const ids = extractIds(html);
      if (!ids.length) return json({ error: "no videos found" }, 502);

      const tokenM = html.match(CONTINUATION_RE);
      const apiKeyM = html.match(API_KEY_RE);
      const clientVerM = html.match(CLIENT_VERSION_RE);
      const cursor = tokenM && apiKeyM && clientVerM
        ? encodeCursor({ token: tokenM[1], apiKey: apiKeyM[1], clientVersion: clientVerM[1] })
        : null;

      return json({ ids, cursor, fetched: new Date().toISOString() });
    }

    const cursor = decodeCursor(cursorParam);
    if (!cursor) return json({ error: "bad cursor" }, 400);

    const res = await fetch(`https://www.youtube.com/youtubei/v1/browse?key=${cursor.apiKey}`, {
      method: "POST",
      headers: { "content-type": "application/json", "user-agent": UA },
      body: JSON.stringify({
        context: { client: { clientName: "WEB", clientVersion: cursor.clientVersion } },
        continuation: cursor.token
      })
    });
    if (!res.ok) return json({ error: "upstream " + res.status }, 502);
    const text = await res.text();

    const ids = extractIds(text);
    const tokenM = text.match(CONTINUATION_RE);
    const nextCursor = tokenM ? encodeCursor({ token: tokenM[1], apiKey: cursor.apiKey, clientVersion: cursor.clientVersion }) : null;

    return json({ ids, cursor: nextCursor, fetched: new Date().toISOString() });
  } catch (e) {
    return json({ error: "fetch failed" }, 502);
  }
};

export const config = { path: "/api/latest-videos" };
