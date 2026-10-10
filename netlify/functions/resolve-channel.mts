/* Resolve a pasted YouTube channel URL, @handle or bare name into the
 * canonical channel ID, display name and avatar, so the Videos tab's "Add
 * channel" box can show a confirmation card before adding it.
 *
 *   GET /api/resolve-channel?q=<url, @handle, bare name, or UC... id>
 *
 * No API key / quota: scrapes the channel's own page server-side (same
 * approach as latest-videos.mts) and reads the canonical link + og tags
 * every YouTube channel page carries, regardless of which URL shape got you
 * there.
 */

const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "public, max-age=3600", "access-control-allow-origin": "*" }
  });
}

function toChannelUrl(raw: string): string | null {
  let q = raw.trim();
  if (!q) return null;
  if (/^UC[A-Za-z0-9_-]{22}$/.test(q)) return `https://www.youtube.com/channel/${q}`;
  if (/^https?:\/\//i.test(q)) {
    // Strip a trailing /videos, /about, /featured etc - the plain channel
    // page carries the same canonical tag and is one less redirect.
    return q.replace(/\/(videos|streams|shorts|about|featured|community)\/?(\?.*)?$/i, "");
  }
  q = q.replace(/^@/, "");
  if (!/^[A-Za-z0-9_.-]{1,100}$/.test(q)) return null;
  return `https://www.youtube.com/@${q}`;
}

export default async (req: Request) => {
  const url = new URL(req.url);
  const channelUrl = toChannelUrl(url.searchParams.get("q") || "");
  if (!channelUrl) return json({ error: "Enter a channel URL, @handle or name" }, 400);

  try {
    const res = await fetch(channelUrl, { headers: { "user-agent": UA, "accept-language": "en-US,en;q=0.9" } });
    if (!res.ok) return json({ error: "Couldn't find that channel" }, 404);
    const html = await res.text();

    const idM = html.match(/<link rel="canonical" href="https:\/\/www\.youtube\.com\/channel\/(UC[A-Za-z0-9_-]{22})"/);
    if (!idM) return json({ error: "Couldn't find that channel" }, 404);
    const nameM = html.match(/<meta property="og:title" content="([^"]*)"/);
    const imgM = html.match(/<meta property="og:image" content="([^"]*)"/);

    return json({
      channelId: idM[1],
      name: nameM ? nameM[1].replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'") : idM[1],
      avatar: imgM ? imgM[1] : ""
    });
  } catch {
    return json({ error: "Couldn't reach YouTube" }, 502);
  }
};

export const config = { path: "/api/resolve-channel" };
