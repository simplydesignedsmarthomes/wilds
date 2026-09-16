import { getStore } from "@netlify/blobs";

/* Sync endpoint. One blob per sync code, no accounts and no personal data.
 *
 *   GET  /api/sync?code=WILDS-XXXX-XXXX   -> stored progress, or 404
 *   PUT  /api/sync?code=WILDS-XXXX-XXXX   -> stores the JSON body
 *
 * There is deliberately no list endpoint, so codes cannot be enumerated. A
 * code is the only credential, which is the trade for having no signup.
 * Worst case for a leaked code is somebody reading or overwriting skill
 * levels and checklists.
 */

const CODE = /^WILDS-[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{4}-[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{4}$/;
const MAX_BYTES = 128 * 1024;   // skills + checks is a few KB; this is generous

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET,PUT,OPTIONS",
      "access-control-allow-headers": "content-type"
    }
  });
}

export default async (req: Request) => {
  if (req.method === "OPTIONS") return json({ ok: true });

  const code = (new URL(req.url).searchParams.get("code") || "").toUpperCase().trim();
  if (!CODE.test(code)) return json({ error: "bad code" }, 400);

  const store = getStore("wilds-sync");

  if (req.method === "GET") {
    try {
      const data = await store.get(code, { type: "json" });
      if (!data) return json({ error: "not found" }, 404);
      return json(data);
    } catch {
      return json({ error: "read failed" }, 500);
    }
  }

  if (req.method === "PUT") {
    const raw = await req.text();
    if (raw.length > MAX_BYTES) return json({ error: "too large" }, 413);

    let body: any;
    try { body = JSON.parse(raw); }
    catch { return json({ error: "bad json" }, 400); }
    if (!body || typeof body !== "object") return json({ error: "bad body" }, 400);

    // Only these keys are ever stored. Anything else the client sends is dropped,
    // so a compromised client cannot turn this into general purpose storage.
    const clean = {
      v: 1,
      updated: new Date().toISOString(),
      skills: sanitiseLevels(body.skills),
      quests: sanitiseFlags(body.quests),
      achievements: sanitiseFlags(body.achievements),
      bestiary: sanitiseFlags(body.bestiary)
    };

    try {
      await store.setJSON(code, clean);
      return json({ ok: true, updated: clean.updated });
    } catch {
      return json({ error: "write failed" }, 500);
    }
  }

  return json({ error: "method not allowed" }, 405);
};

function sanitiseLevels(o: any) {
  const out: Record<string, number> = {};
  if (!o || typeof o !== "object") return out;
  for (const k of Object.keys(o).slice(0, 40)) {
    if (k.length > 40) continue;
    const n = Number(o[k]);
    if (Number.isFinite(n) && n > 0) out[k] = Math.min(99, Math.max(1, Math.round(n)));
  }
  return out;
}

function sanitiseFlags(o: any) {
  const out: Record<string, true> = {};
  if (!o || typeof o !== "object") return out;
  for (const k of Object.keys(o).slice(0, 600)) {
    if (k.length > 120) continue;
    if (o[k]) out[k] = true;
  }
  return out;
}

export const config = { path: "/api/sync" };
