import pathlib, re

surf_path = pathlib.Path("/Users/jcolley/surf_clock/web_customizer/surf_data.js")
code = surf_path.read_text(encoding="utf-8")

start_marker = "export async function geocodeAddressCandidates(query, limit = 6) {"
end_marker = "/**\n * Fetches live named beaches & surf spots"
idx_s = code.find(start_marker)
idx_e = code.find(end_marker)
assert idx_s != -1 and idx_e != -1, f"Markers not found: {idx_s}, {idx_e}"

new_geocoder = """function getBrowserLocationBias() {
  try {
    const tz = (typeof Intl !== "undefined" && Intl.DateTimeFormat().resolvedOptions().timeZone) || "Australia/Sydney";
    const tzMap = {
      "Australia/Sydney": { lat: -33.8688, lng: 151.2093 },
      "Australia/Melbourne": { lat: -37.8136, lng: 144.9631 },
      "Australia/Brisbane": { lat: -27.4698, lng: 153.0251 },
      "Australia/Perth": { lat: -31.9505, lng: 115.8605 },
      "Australia/Adelaide": { lat: -34.9285, lng: 138.6007 },
      "Australia/Hobart": { lat: -42.8821, lng: 147.3272 },
      "Pacific/Auckland": { lat: -36.8485, lng: 174.7633 },
      "Pacific/Honolulu": { lat: 21.3069, lng: -157.8583 },
      "America/Los_Angeles": { lat: 34.0522, lng: -118.2437 },
      "America/New_York": { lat: 40.7128, lng: -74.0060 },
      "Europe/London": { lat: 51.5072, lng: -0.1276 },
      "Europe/Lisbon": { lat: 38.7223, lng: -9.1393 },
      "Europe/Paris": { lat: 43.4832, lng: -1.5586 },
      "Europe/Madrid": { lat: 43.3183, lng: -1.9812 },
      "Asia/Makassar": { lat: -8.6500, lng: 115.2167 },
      "Asia/Tokyo": { lat: 35.6762, lng: 139.6503 },
    };
    return tzMap[tz] || { lat: -33.8688, lng: 151.2093 };
  } catch (_) {
    return { lat: -33.8688, lng: 151.2093 };
  }
}

export async function geocodeAddressCandidates(query, limit = 6) {
  const q = String(query || "").trim();
  if (q.length < 2) return [];

  const bias = getBrowserLocationBias();
  const houseMatch = q.match(/^(\\d+[a-zA-Z]?)\\s+/);
  const requestedHouseNum = houseMatch ? houseMatch[1].toLowerCase() : null;

  const qTokens = q
    .toLowerCase()
    .replace(/[^a-z0-9\\s]/g, " ")
    .split(/\\s+/)
    .filter((t) => t.length >= 2 && !/^(st|street|rd|road|ave|avenue|dr|drive|ln|lane|pl|place|ct|court|pde|parade|blvd|boulevard|the)$/.test(t));

  const computeTokenMatch = (label, extraText = "") => {
    if (qTokens.length === 0) return 1.0;
    const hay = `${label} ${extraText}`.toLowerCase();
    let hits = 0;
    for (const tok of qTokens) {
      if (hay.includes(tok)) hits += 1;
    }
    return hits / qTokens.length;
  };

  const scoreCandidate = (label, extraText = "", baseScore = 85) => {
    const tokenRatio = computeTokenMatch(label, extraText);
    const hasLocality = label.includes(",");
    return baseScore * 0.35 + tokenRatio * 65 + (hasLocality ? 8 : -15);
  };

  const fetchArcGIS = async () => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 3200);
    try {
      const url = `https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&maxLocations=${limit}&location=${bias.lng},${bias.lat}&outFields=Match_addr,Addr_type,StAddr,Nbrhd,City,Subregion,Region,Country&SingleLine=${encodeURIComponent(q)}`;
      const res = await fetch(url, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!res.ok) return [];
      const data = await res.json();
      const out = [];
      for (const c of data.candidates || []) {
        const lat = Number(c?.location?.y);
        const lng = Number(c?.location?.x);
        if (Number.isNaN(lat) || Number.isNaN(lng)) continue;
        const attr = c.attributes || {};
        const rawAddr = String(c.address || attr.Match_addr || "").trim();
        if (!rawAddr) continue;
        if (!rawAddr.includes(",") && !attr.City && !attr.Nbrhd && !attr.Region && qTokens.length >= 2) {
          continue;
        }
        const extra = `${attr.Nbrhd || ""} ${attr.City || ""} ${attr.Subregion || ""} ${attr.Region || ""} ${attr.Country || ""}`;
        const tokenRatio = computeTokenMatch(rawAddr, extra);
        const locality = attr.Nbrhd || attr.City || attr.Subregion || attr.Region || rawAddr.split(",")[0];
        const isAddr = /PointAddress|StreetAddress|StreetInt|Subaddress|StreetName/i.test(attr.Addr_type || "") || isLikelyStreetAddress(rawAddr);
        out.push({
          label: rawAddr,
          sublabel: `5 Best Local Surf Beaches near ${locality}`,
          lat,
          lng,
          regionId: null,
          badge: isAddr ? "📍 HOME ADDRESS" : "📍 LOCATION",
          _tokenRatio: tokenRatio,
          _rank: scoreCandidate(rawAddr, extra, Number(c.score || 90)) + 4,
        });
      }
      return out;
    } catch (_) {
      clearTimeout(timer);
      return [];
    }
  };

  const fetchPhoton = async () => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 3200);
    try {
      const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(q)}&lat=${bias.lat}&lon=${bias.lng}&limit=${limit}&lang=en`;
      const res = await fetch(url, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!res.ok) return [];
      const data = await res.json();
      const out = [];
      for (const feat of data.features || []) {
        const coords = feat?.geometry?.coordinates;
        if (!Array.isArray(coords) || coords.length < 2) continue;
        const [lng, lat] = coords.map(Number);
        if (Number.isNaN(lat) || Number.isNaN(lng)) continue;
        const p = feat.properties || {};
        // If user typed a specific house number (e.g. 75), skip Photon results with a different house number (e.g. 88)
        if (requestedHouseNum && p.housenumber && String(p.housenumber).toLowerCase() !== requestedHouseNum) {
          continue;
        }
        const streetPart = p.housenumber && p.street
          ? `${p.housenumber} ${p.street}`
          : (p.street || p.name || "");
        const suburbPart = p.suburb || p.district || p.locality || "";
        const cityPart = p.city || p.town || p.county || "";
        const statePart = p.state || "";
        const countryPart = p.country || "";
        const parts = [streetPart, suburbPart, cityPart, statePart, countryPart].filter(Boolean);
        const dedupParts = [];
        for (const pt of parts) {
          if (!dedupParts.some((existing) => existing.toLowerCase() === pt.toLowerCase())) {
            dedupParts.push(pt);
          }
        }
        const label = dedupParts.join(", ");
        if (!label) continue;
        const extra = `${p.postcode || ""} ${p.name || ""}`;
        const tokenRatio = computeTokenMatch(label, extra);
        const locality = suburbPart || cityPart || p.name || dedupParts[0];
        const isAddr = Boolean(p.housenumber || p.street || p.type === "house" || p.type === "street");
        out.push({
          label,
          sublabel: `5 Best Local Surf Beaches near ${locality}`,
          lat,
          lng,
          regionId: null,
          badge: isAddr ? "📍 HOME ADDRESS" : "📍 LOCATION",
          _tokenRatio: tokenRatio,
          _rank: scoreCandidate(label, extra, isAddr ? 88 : 82),
        });
      }
      return out;
    } catch (_) {
      clearTimeout(timer);
      return [];
    }
  };

  const fetchNominatim = async () => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 3200);
    try {
      const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&limit=4&q=${encodeURIComponent(q)}`;
      const res = await fetch(url, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!res.ok) return [];
      const data = await res.json();
      const out = [];
      for (const item of data || []) {
        const lat = Number(item.lat);
        const lng = Number(item.lon);
        if (Number.isNaN(lat) || Number.isNaN(lng)) continue;
        const a = item.address || {};
        if (requestedHouseNum && a.house_number && String(a.house_number).toLowerCase() !== requestedHouseNum) {
          continue;
        }
        const street = a.house_number && a.road ? `${a.house_number} ${a.road}` : (a.road || item.name || "");
        const suburb = a.suburb || a.neighbourhood || a.village || a.town || "";
        const city = a.city || a.municipality || a.county || "";
        const state = a.state || "";
        const country = a.country || "";
        const parts = [street, suburb, city, state, country].filter(Boolean);
        const dedup = [];
        for (const pt of parts) {
          if (!dedup.some((e) => e.toLowerCase() === pt.toLowerCase())) dedup.push(pt);
        }
        const label = dedup.join(", ") || String(item.display_name || "").split(",").slice(0, 4).join(", ");
        if (!label) continue;
        const extra = item.display_name || "";
        const tokenRatio = computeTokenMatch(label, extra);
        const locality = suburb || city || dedup[0];
        out.push({
          label,
          sublabel: `5 Best Local Surf Beaches near ${locality}`,
          lat,
          lng,
          regionId: null,
          badge: a.house_number || a.road ? "📍 HOME ADDRESS" : "📍 LOCATION",
          _tokenRatio: tokenRatio,
          _rank: scoreCandidate(label, extra, 88),
        });
      }
      return out;
    } catch (_) {
      clearTimeout(timer);
      return [];
    }
  };

  const [arcResults, photonResults, nomResults] = await Promise.all([
    fetchArcGIS(),
    fetchPhoton(),
    fetchNominatim(),
  ]);

  let merged = [...arcResults, ...photonResults, ...nomResults].sort((a, b) => (b._rank || 0) - (a._rank || 0));
  const bestTokenRatio = merged.reduce((m, c) => Math.max(m, c._tokenRatio || 0), 0);
  if (bestTokenRatio >= 0.75) {
    merged = merged.filter((c) => (c._tokenRatio || 0) >= Math.max(0.6, bestTokenRatio - 0.34));
  }

  const unique = [];
  for (const cand of merged) {
    const normLbl = cand.label.toLowerCase().replace(/[^a-z0-9]/g, "");
    const isDup = unique.some(
      (u) =>
        u.label.toLowerCase().replace(/[^a-z0-9]/g, "") === normLbl ||
        (haversineKm(u.lat, u.lng, cand.lat, cand.lng) < 0.18 && normLbl.slice(0, 12) === u.label.toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 12))
    );
    if (!isDup) {
      unique.push(cand);
    }
    if (unique.length >= limit) break;
  }
  return unique;
}

"""

code = code[:idx_s] + new_geocoder + code[idx_e:]
surf_path.write_text(code, encoding="utf-8")

# Bump all ?v=XX to ?v=66 across web_customizer
wc_dir = pathlib.Path("/Users/jcolley/surf_clock/web_customizer")
for p in list(wc_dir.glob("*.html")) + list(wc_dir.glob("*.js")):
    txt = p.read_text(encoding="utf-8")
    new_txt = re.sub(r"\?v=\d+", "?v=66", txt)
    if new_txt != txt:
        p.write_text(new_txt, encoding="utf-8")
        print("Bumped ?v=66 in", p.name)
