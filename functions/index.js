const functions = require("@google-cloud/functions-framework");

async function getAccessToken() {
  const res = await fetch(
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
    { headers: { "Metadata-Flavor": "Google" } }
  );
  if (!res.ok) throw new Error("Metadata token error: " + res.status);
  const data = await res.json();
  return data.access_token;
}

functions.http("surfclockSearch", async (req, res) => {
  res.set("Access-Control-Allow-Origin", "*");
  res.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.set("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    return res.status(204).send("");
  }
  try {
    const q = String(req.query.q || req.body?.q || "").trim();
    const lat = parseFloat(req.query.lat ?? req.body?.lat ?? "0");
    const lng = parseFloat(req.query.lng ?? req.body?.lng ?? "0");
    if (!q && (!lat || !lng)) {
      return res.status(400).json({ error: "Missing query or coordinates" });
    }

    const token = await getAccessToken();
    const prompt = `You are an expert Australian & global surf guide. Find the 5 best actual surf beaches or surf breaks nearest to "${q}" (coordinates: ${lat.toFixed(4)}, ${lng.toFixed(4)}).
Rules:
1. Must be real, well-known surf breaks or surf beaches actually in or immediately adjacent to "${q}" (within 5-30km, NEVER pick beaches from a different city 80km away! E.g. for Kiama NSW return THE FARM, MYSTICS, BOMBO BCH, SURF BEACH, WERRI BCH).
2. Order the 5 breaks geographically along the coast (North to South, or West to East).
3. "name" must be UPPERCASE, max 11 characters so it fits on a physical Braun clock dial (use clean abbreviations like BCH, PT, HD, RF, ISL if needed).
4. Return strict JSON matching:
{
  "regionName": "Clean Regional Title (e.g. Kiama & South Coast, NSW)",
  "shortName": "UPPERCASE SHORT TITLE MAX 12 CHARS (e.g. KIAMA / STH)",
  "beaches": [
    { "name": "MAX 11 CHAR", "fullName": "Full Break Name", "lat": -34.0, "lng": 150.0, "quality": 9.2, "type": "Reef / Point / Beachbreak" }
  ]
}`;

    const url =
      "https://aiplatform.googleapis.com/v1/projects/ee-gif-machine/locations/global/publishers/google/models/gemini-2.5-flash-lite:generateContent";
    const aiRes = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: {
          responseMimeType: "application/json",
          temperature: 0.1,
          thinkingConfig: { thinkingBudget: 0 },
        },
      }),
    });

    if (!aiRes.ok) {
      const txt = await aiRes.text();
      return res.status(502).json({ error: "Gemini upstream error", detail: txt });
    }
    const aiData = await aiRes.json();
    const rawText = aiData?.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
    const parsed = JSON.parse(rawText);
    res.set("Cache-Control", "public, max-age=86400, s-maxage=86400");
    return res.status(200).json({
      source: "GEMINI_2_5_FLASH_SURF_AGENT",
      ...parsed,
    });
  } catch (err) {
    return res.status(500).json({ error: String(err.message || err) });
  }
});
