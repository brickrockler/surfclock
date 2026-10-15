/**
 * SURF CLOCK (SC-01) — FULL-STACK PACKAGE GENERATOR
 * Generates an end-to-end custom kit in browser memory using JSZip:
 * 1. 3D Print CAD/STLs with custom embossed dial & multi-material typography inlay
 * 2. ESP32-S3 Firmware with the 5 selected beaches & dial angles hardcoded in C++
 * 3. Cloudflare Worker Edge Backend with custom beach GPS coordinates & scoring pipeline
 * 4. Local Python Server with custom spots.json and static web UI assets
 * 5. Complete custom hardware build, wiring, and firmware flashing guide
 */

const COMPASS_DEG = {
  N: 0, NNE: 22.5, NE: 45, ENE: 67.5,
  E: 90, ESE: 112.5, SE: 135, SSE: 157.5,
  S: 180, SSW: 202.5, SW: 225, WSW: 247.5,
  W: 270, WNW: 292.5, NW: 315, NNW: 337.5
};

export function escapeCppString(str) {
  return String(str ?? "").replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

export function compassToDegrees(dirStr, defaultDeg = 90) {
  if (dirStr === null || dirStr === undefined || dirStr === "") return defaultDeg;
  if (typeof dirStr === "number") return Number.isNaN(dirStr) ? defaultDeg : ((dirStr % 360) + 360) % 360;
  const upper = String(dirStr).trim().toUpperCase();
  if (!upper) return defaultDeg;
  if (COMPASS_DEG[upper] != null) return COMPASS_DEG[upper];
  const parsed = parseFloat(upper);
  return Number.isNaN(parsed) ? defaultDeg : ((parsed % 360) + 360) % 360;
}

/**
 * Maps the 5 custom beaches from customizer state to clockwise dial positions (1 to 5):
 * Pos 1 = 12:00 (0°)   -> Slot 0
 * Pos 2 = 02:00 (60°)  -> Slot 2
 * Pos 3 = 04:00 (120°) -> Slot 4
 * Pos 4 = 08:00 (240°) -> Slot 3
 * Pos 5 = 10:00 (300°) -> Slot 1
 */
export function buildClockwiseSpots(beaches, region = {}) {
  const slotOrder = [0, 2, 4, 3, 1];
  const angles = [0, 60, 120, 240, 300];
  const hours = [12, 2, 4, 8, 10];

  const reg = region || {};
  const regSwellDeg = compassToDegrees(reg.swellDir, 135);
  const regWindDeg = compassToDegrees(reg.windDir, 270);
  const baseLat = typeof reg.lat === "number" && !Number.isNaN(reg.lat) ? reg.lat : -33.75;
  const baseLon =
    typeof reg.lon === "number" && !Number.isNaN(reg.lon)
      ? reg.lon
      : typeof reg.lng === "number" && !Number.isNaN(reg.lng)
      ? reg.lng
      : 151.30;

  return slotOrder.map((slotIdx, i) => {
    const rawBeach = (beaches && beaches[slotIdx]) || {};
    const name = String(rawBeach.name || `Beach ${i + 1}`).trim() || `Beach ${i + 1}`;
    const id = String(
      rawBeach.id ||
        name
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-|-$/g, "") ||
        `spot-${i + 1}`
    );
    const dial_text = name.toUpperCase();
    const angle = angles[i];
    const hour = hours[i];
    const rawLat = rawBeach.lat ?? baseLat;
    const rawLon = rawBeach.lng ?? rawBeach.lon ?? baseLon;
    const lat = Number.isFinite(Number(rawLat)) ? Number(rawLat) : -33.75;
    const lon = Number.isFinite(Number(rawLon)) ? Number(rawLon) : 151.30;

    // Calculate facing: beach faces towards open ocean
    let facing = 90;
    if (rawBeach.facing != null) {
      facing = compassToDegrees(rawBeach.facing, 90);
    } else if (rawBeach.openSwellDir != null) {
      facing = compassToDegrees(rawBeach.openSwellDir, 90);
    } else if (rawBeach.idealWindDir != null) {
      facing = (compassToDegrees(rawBeach.idealWindDir) + 180) % 360;
    } else if (reg.windDir && reg.windDir !== "OFFSHORE") {
      facing = (regWindDeg + 180) % 360;
    } else if (reg.swellDir) {
      facing = regSwellDeg;
    } else {
      facing = lon > 0 && lon < 170 && lat < 0 ? 90 : lon < -60 ? 250 : 90;
    }

    const offshore = (facing + 180) % 360;
    const windTol = Number(rawBeach.windTolerance ?? 35);
    const swellTol = Number(rawBeach.dirTolerance ?? 55);
    const wind_min = Math.round((offshore - windTol + 360) % 360);
    const wind_max = Math.round((offshore + windTol + 360) % 360);
    const swell_min = Math.round((facing - swellTol + 360) % 360);
    const swell_max = Math.round((facing + swellTol + 360) % 360);
    const ideal_period = Number(reg.swellPeriodS ?? 12);

    return {
      pos: i + 1,
      slot_index: slotIdx,
      id,
      name,
      dial_text,
      hour,
      angle_deg: angle,
      lat: Number(lat.toFixed(4)),
      lon: Number(lon.toFixed(4)),
      facing_deg: Math.round(facing),
      optimal_swell_dir_min: swell_min,
      optimal_swell_dir_max: swell_max,
      optimal_wind_dir_min: wind_min,
      optimal_wind_dir_max: wind_max,
      min_swell_m: 0.7,
      max_swell_m: 3.5,
      ideal_period_s: ideal_period,
      description: `Custom break at ${name} (${hour} o'clock, ${angle}°)`
    };
  });
}

/**
 * Customizes firmware include/config.h using function replacers so '$' in strings never triggers regex substitution bugs
 */
export function customizeConfigH(originalConfigH, regionOrOpts = {}, spots = []) {
  let modified = String(originalConfigH ?? "");
  const reg =
    typeof regionOrOpts === "string"
      ? { name: regionOrOpts, code: regionOrOpts }
      : Array.isArray(regionOrOpts)
      ? { spots: regionOrOpts }
      : regionOrOpts || {};

  const effSpots = Array.isArray(regionOrOpts) ? regionOrOpts : Array.isArray(spots) ? spots : [];
  const cleanName = escapeCppString(reg.name || "Custom Coastline");
  const cleanCode = escapeCppString(reg.code || "CUSTOM");

  if (reg.wifiSsid != null) {
    const safeSsid = escapeCppString(reg.wifiSsid);
    modified = modified.replace(/(#define\s+DEFAULT_WIFI_SSID\s+)"[^"]*"/, (_, p1) => `${p1}"${safeSsid}"`);
  }
  if (reg.wifiPass != null) {
    const safePass = escapeCppString(reg.wifiPass);
    modified = modified.replace(/(#define\s+DEFAULT_WIFI_PASS\s+)"[^"]*"/, (_, p1) => `${p1}"${safePass}"`);
  }
  if (reg.apiUrl != null) {
    const safeApi = escapeCppString(reg.apiUrl);
    modified = modified.replace(/(#define\s+DEFAULT_API_URL\s+)"[^"]*"/, (_, p1) => `${p1}"${safeApi}"`);
  }

  if (/#define\s+SURFCLOCK_REGION_NAME/.test(modified)) {
    modified = modified.replace(
      /(#define\s+SURFCLOCK_REGION_NAME\s+)"[^"]*"/,
      (_, p1) => `${p1}"${cleanName}"`
    );
  } else {
    modified += `\n#define SURFCLOCK_REGION_NAME "${cleanName}"\n#define SURFCLOCK_REGION_CODE "${cleanCode}"\n`;
  }

  if (effSpots.length > 0) {
    const spotComments = effSpots
      .map((s, idx) => `// Spot ${s.pos ?? idx + 1}: "${escapeCppString(s.name)}" (${escapeCppString(s.id || s.name)})`)
      .join("\n");
    modified += `${spotComments}\n`;
  }

  return modified;
}

/**
 * Injects custom hardcoded beach positions & angles into StepperController C++ source
 */
export function customizeStepperControllerCpp(originalCpp, spots = []) {
  const safeSpots = Array.isArray(spots) ? spots : [];
  const switchCasesPos = safeSpots
    .map((s, idx) => {
      const pos = s.pos ?? idx + 1;
      const angleNum = Number(s.angle_deg ?? s.angle ?? 0);
      const angleFloat = angleNum.toFixed(1);
      const stepVal = Math.round((angleNum / 360.0) * 2048);
      const hour = s.hour ?? 12;
      const safeName = escapeCppString(s.name);
      const safeId = escapeCppString(s.id || s.name);
      const extraCase = pos === 1 ? "        case 12:\n" : "";
      return `${extraCase}        case ${pos}:\n            angle = ${angleFloat}f; name = "${safeName}"; break;        // Step ${stepVal} (${hour}:00, id = "${safeId}")`;
    })
    .join("\n");

  const switchCasesCal = safeSpots
    .map((s, idx) => {
      const pos = s.pos ?? idx + 1;
      const angleNum = Number(s.angle_deg ?? s.angle ?? 0);
      const stepVal = Math.round((angleNum / 360.0) * 2048);
      const safeName = escapeCppString(s.name);
      const safeId = escapeCppString(s.id || s.name);
      const extraCase = pos === 1 ? "        case 12: " : "";
      return `        ${extraCase}case ${pos}:  step = ${stepVal}; name = "${safeName}"; break; // id = "${safeId}"`;
    })
    .join("\n");

  let modified = String(originalCpp ?? "");

  // Replace setBeachPosition switch block using function replacer
  const setBeachRegex = /(bool\s+StepperController::setBeachPosition\s*\(\s*int\s+pos\s*\)\s*\{[\s\S]*?switch\s*\(\s*pos\s*\)\s*\{)[\s\S]*?(\s*default:)/;
  if (setBeachRegex.test(modified)) {
    modified = modified.replace(setBeachRegex, (_, p1, p2) => `${p1}\n${switchCasesPos}\n${p2}`);
  }

  // Replace calibrateCurrentAsBeach switch block using function replacer
  const calBeachRegex = /(void\s+StepperController::calibrateCurrentAsBeach\s*\(\s*int\s+pos\s*\)\s*\{[\s\S]*?switch\s*\(\s*pos\s*\)\s*\{)[\s\S]*?(\s*default:)/;
  if (calBeachRegex.test(modified)) {
    modified = modified.replace(calBeachRegex, (_, p1, p2) => `${p1}\n${switchCasesCal}\n${p2}`);
  }
  return modified;
}

/**
 * Injects custom spots array into Cloudflare Worker JavaScript source
 */
export function customizeWorkerJs(originalJs, spots = []) {
  const safeSpots = Array.isArray(spots) ? spots : [];
  const spotsJs = JSON.stringify(
    safeSpots.map((s, idx) => ({
      pos: s.pos ?? idx + 1,
      id: s.id || String(s.name || `spot-${idx + 1}`).toLowerCase().replace(/[^a-z0-9]+/g, "-"),
      name: s.name,
      dial_text: s.dial_text || String(s.name || "").toUpperCase(),
      angle: s.angle_deg ?? s.angle ?? 0,
      lat: s.lat ?? -33.75,
      lon: s.lon ?? s.lng ?? 151.30,
      facing: s.facing_deg ?? s.facing ?? 90,
      swell_min: s.optimal_swell_dir_min ?? 45,
      swell_max: s.optimal_swell_dir_max ?? 145,
      wind_min: s.optimal_wind_dir_min ?? 235,
      wind_max: s.optimal_wind_dir_max ?? 305,
      min_s: s.min_swell_m ?? 0.7,
      max_s: s.max_swell_m ?? 3.5,
      period: s.ideal_period_s ?? 12
    })),
    null,
    2
  );

  const src = String(originalJs ?? "");
  const spotsRegex = /const\s+SPOTS\s*=\s*\[[\s\S]*?\];/;
  if (spotsRegex.test(src)) {
    return src.replace(spotsRegex, () => `const SPOTS = ${spotsJs};`);
  }
  return `const SPOTS = ${spotsJs};\n\n` + src;
}

/**
 * Generates Markdown Build & Calibration Guide tailored for the user's setup
 */
export function generateBuildGuideMarkdown({ region = {}, spots = [], colors = {} } = {}) {
  const reg = region || {};
  const cleanCode = (reg.code || "CUSTOM").replace(/[^A-Za-z0-9_-]/g, "_").toUpperCase();
  const safeSpots = Array.isArray(spots) && spots.length ? spots : buildClockwiseSpots([], reg);

  const fSw = colors?.bezel || { name: "Graphite Matte", hex: "#1A1A1A" };
  const dSw = colors?.dial || { name: "Chalk White", hex: "#F5F5F5" };
  const tSw = colors?.inlay || { name: "Laser Orange", hex: "#E85D26" };
  const hSw = colors?.hands || { name: "Anodized Orange", hex: "#E85D26" };

  return `# 🌊 SURF CLOCK (SC-01) — Custom Build & Setup Guide

**Target Coastline:** ${reg.name || "Custom Coastline"} (${cleanCode})  
**Generated On:** ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}  
**Open Source Repository:** [https://github.com/raphdixon/surfclock](https://github.com/raphdixon/surfclock)

---

## 🏄 Your 5 Clockwise Dial Beaches

| Position | Hour | Dial Angle | Beach Name | Lat, Lon | Facing | Offshore Wind |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: |
${safeSpots.map((s) => `| **${s.pos}** | ${s.hour}:00 | **${s.angle_deg}°** | **${s.name}** | \`${s.lat}, ${s.lon}\` | ${s.facing_deg}° | ${s.optimal_wind_dir_min}°–${s.optimal_wind_dir_max}° |`).join("\n")}
| **–** | 6:00 | **180°** | **Conditions Gauge** | Subdial Needle | – | 1.0 (Poor) to 10.0 (Epic) |

---

## 🎨 3D Print Setup (Selected Colorway)

- **Outer Bezel Chassis (\`01_outer_bezel_chassis.stl\`):** ${fSw.name} (${fSw.hex})
- **Dial Faceplate (\`02_custom_dial_faceplate_${cleanCode}.stl\`):** ${dSw.name} (${dSw.hex})
- **Dial Typography Inlay (\`02b_custom_typography_inlay_${cleanCode}.stl\`):** ${tSw.name} (${tSw.hex})
- **Pointer Hands (\`05_pointer_hands_28byj48_capped.stl\`):** ${hSw.name} (${hSw.hex})
- **Deck & Rear Cover (\`03_internal_engineering_deck.stl\` & \`04_rear_cover_usb.stl\`):** Any durable filament (PETG or PLA)

### Dual-Color Printing Note:
If you are printing on a single-nozzle 3D printer without an AMS / MMU:
1. Slice \`02_custom_dial_faceplate_${cleanCode}.stl\` at **0.20mm layer height**.
2. Add a pause / filament color change at **Z = 2.60mm**.
3. Swap filament from **${dSw.name}** to **${tSw.name}** to produce crisp raised 3D lettering!

---

## ⚡ Electronics & Wiring

No optical or magnetic sensors are required. Connect the ULN2003 stepper driver boards to the ESP32-S3:

### Motor 1 (Beach Pointer)
- \`IN1\` ➔ **GPIO 4**
- \`IN2\` ➔ **GPIO 5**
- \`IN3\` ➔ **GPIO 6**
- \`IN4\` ➔ **GPIO 7**
- \`+ (VCC)\` / \`- (GND)\` ➔ **5V (VBUS) / GND**

### Motor 2 (Conditions Gauge)
- \`IN1\` ➔ **GPIO 11**
- \`IN2\` ➔ **GPIO 12**
- \`IN3\` ➔ **GPIO 13**
- \`IN4\` ➔ **GPIO 14**
- \`+ (VCC)\` / \`- (GND)\` ➔ **5V (VBUS) / GND**

---

## 🔌 1-Command Firmware Flashing

1. Connect your ESP32-S3 via USB-C.
2. Open terminal in the \`firmware/\` folder:
   \`\`\`bash
   cd firmware
   pio run -t upload
   pio device monitor -b 115200
   \`\`\`
3. Set your Wi-Fi credentials directly in the serial monitor:
   \`\`\`text
   wifi "Your-SSID" "Your-Password"
   \`\`\`
4. Manually align the break pointer to **12 o'clock** (${safeSpots[0]?.name || "Beach 1"}) and the conditions needle to **1.0**, then lock them:
   \`\`\`text
   zero
   zero2
   \`\`\`
   The clock saves step 0 to persistent flash (NVS) and begins real-time telemetry updates!

---

## ☁️ Serverless Surf Telemetry Deployment

To deploy your serverless scoring engine for your 5 beaches:
\`\`\`bash
cd cloudflare-worker
npx wrangler deploy
\`\`\`
Point your clock to your newly deployed API:
\`\`\`text
api https://<your-worker>.workers.dev/api/surf
\`\`\`
`;
}

/**
 * Fetches static assets from relative path with fallback support
 */
async function fetchAssetBuffer(path) {
  try {
    const res = await fetch(path);
    if (res.ok) {
      return await res.arrayBuffer();
    }
  } catch (err) {
    console.warn(`[PackageGenerator] Could not fetch ${path}:`, err);
  }
  return null;
}

async function fetchAssetText(path) {
  try {
    const res = await fetch(path);
    if (res.ok) {
      return await res.text();
    }
  } catch (err) {
    console.warn(`[PackageGenerator] Could not fetch text ${path}:`, err);
  }
  return null;
}

/**
 * Builds the custom full-stack JSZip instance and returns { zip, zipFilename, cleanCode }
 */
export async function generateCustomProjectZip({ state, studio, onProgress = () => {} }) {
  if (typeof window !== "undefined" && typeof window.JSZip === "undefined" && typeof globalThis.JSZip === "undefined") {
    throw new Error("JSZip library not loaded. Please ensure jszip.min.js is present.");
  }

  const JSZipCtor = (typeof window !== "undefined" && window.JSZip) || globalThis.JSZip;
  const zip = new JSZipCtor();
  const region = state?.activeRegion || { name: "Custom Region", code: "CUSTOM" };
  const cleanCode = (region.code || "CUSTOM").replace(/[^A-Za-z0-9_-]/g, "_").toUpperCase();
  const rootFolderName = `SurfClock_${cleanCode}_Custom_Kit`;
  const root = zip.folder(rootFolderName);

  onProgress("Resolving 5 beach coordinates & angles...", 10);
  const spots = buildClockwiseSpots(state?.beaches, region);

  // 1. Generate Custom 3D STL files
  onProgress("Generating custom 3D dial faceplate & typography STL...", 25);
  const stlFolder = root.folder("stl");

  try {
    if (studio && typeof studio.generateCustomDialSTLBuffer === "function") {
      const customDialBuffer = studio.generateCustomDialSTLBuffer(true, cleanCode);
      stlFolder.file(`02_custom_dial_faceplate_${cleanCode}.stl`, customDialBuffer);

      const customInlayBuffer = studio.generateCustomDialSTLBuffer(false, cleanCode);
      stlFolder.file(`02b_custom_typography_inlay_${cleanCode}.stl`, customInlayBuffer);
    }
  } catch (err) {
    console.error("[PackageGenerator] Failed to generate custom STLs:", err);
  }

  // Fetch static base STLs
  onProgress("Packaging 3D printable mechanical CAD chassis...", 45);
  const staticStls = [
    { name: "01_outer_bezel_chassis.stl", url: "./downloads/stl/01_outer_bezel_chassis.stl" },
    { name: "03_internal_engineering_deck.stl", url: "./downloads/stl/03_internal_engineering_deck.stl" },
    { name: "04_rear_cover_usb.stl", url: "./downloads/stl/04_rear_cover_usb.stl" },
    { name: "05_pointer_hands_28byj48_capped.stl", url: "./downloads/stl/05_pointer_hands_28byj48_capped.stl" },
    { name: "06_snap_lock_pins.stl", url: "./downloads/stl/06_snap_lock_pins.stl" }
  ];

  await Promise.all(
    staticStls.map(async (file) => {
      const buf = await fetchAssetBuffer(file.url);
      if (buf) stlFolder.file(file.name, buf);
    })
  );

  // 2. Custom Firmware Generation
  onProgress("Hardcoding custom beaches into ESP32 firmware...", 65);
  const fwFolder = root.folder("firmware");
  const fwSrcFolder = fwFolder.folder("src");
  const fwIncFolder = fwFolder.folder("include");

  const [
    baseStepperCpp,
    baseStepperH,
    baseMainCpp,
    baseCliCpp,
    baseCliH,
    baseGaugeCpp,
    baseGaugeH,
    baseNetCpp,
    baseNetH,
    baseHallCpp,
    baseHallH,
    baseConfigH,
    basePlatformIni,
    baseArduinoIno
  ] = await Promise.all([
    fetchAssetText("./downloads/firmware/src/stepper_controller.cpp"),
    fetchAssetText("./downloads/firmware/src/stepper_controller.h"),
    fetchAssetText("./downloads/firmware/src/main.cpp"),
    fetchAssetText("./downloads/firmware/src/cli_handler.cpp"),
    fetchAssetText("./downloads/firmware/src/cli_handler.h"),
    fetchAssetText("./downloads/firmware/src/conditions_gauge.cpp"),
    fetchAssetText("./downloads/firmware/src/conditions_gauge.h"),
    fetchAssetText("./downloads/firmware/src/network_manager.cpp"),
    fetchAssetText("./downloads/firmware/src/network_manager.h"),
    fetchAssetText("./downloads/firmware/src/hall_sensor.cpp"),
    fetchAssetText("./downloads/firmware/src/hall_sensor.h"),
    fetchAssetText("./downloads/firmware/include/config.h"),
    fetchAssetText("./downloads/firmware/platformio.ini"),
    fetchAssetText("./downloads/firmware/sc01_esp32s3_firmware.ino")
  ]);

  if (baseStepperCpp) {
    const customStepperCpp = customizeStepperControllerCpp(baseStepperCpp, spots);
    fwSrcFolder.file("stepper_controller.cpp", customStepperCpp);
  }
  if (baseStepperH) fwSrcFolder.file("stepper_controller.h", baseStepperH);
  if (baseMainCpp) fwSrcFolder.file("main.cpp", baseMainCpp);
  if (baseCliCpp) fwSrcFolder.file("cli_handler.cpp", baseCliCpp);
  if (baseCliH) fwSrcFolder.file("cli_handler.h", baseCliH);
  if (baseGaugeCpp) fwSrcFolder.file("conditions_gauge.cpp", baseGaugeCpp);
  if (baseGaugeH) fwSrcFolder.file("conditions_gauge.h", baseGaugeH);
  if (baseNetCpp) fwSrcFolder.file("network_manager.cpp", baseNetCpp);
  if (baseNetH) fwSrcFolder.file("network_manager.h", baseNetH);
  if (baseHallCpp) fwSrcFolder.file("hall_sensor.cpp", baseHallCpp);
  if (baseHallH) fwSrcFolder.file("hall_sensor.h", baseHallH);
  if (baseConfigH) {
    fwIncFolder.file("config.h", customizeConfigH(baseConfigH, region, spots));
  }
  if (basePlatformIni) fwFolder.file("platformio.ini", basePlatformIni);
  if (baseArduinoIno) fwFolder.file("sc01_esp32s3_firmware.ino", baseArduinoIno);

  // 3. Custom Cloudflare Worker Generation
  onProgress("Configuring Surf Telemetry API with custom buoy coordinates...", 80);
  const workerFolder = root.folder("cloudflare-worker");
  const workerSrcFolder = workerFolder.folder("src");

  const [baseWorkerJs, baseWorkerPkg, baseWorkerToml] = await Promise.all([
    fetchAssetText("./downloads/cloudflare-worker/src/index.js"),
    fetchAssetText("./downloads/cloudflare-worker/package.json"),
    fetchAssetText("./downloads/cloudflare-worker/wrangler.toml")
  ]);

  if (baseWorkerJs) {
    const customWorkerJs = customizeWorkerJs(baseWorkerJs, spots);
    workerSrcFolder.file("index.js", customWorkerJs);
    workerFolder.file("worker.js", customWorkerJs);
  }
  if (baseWorkerPkg) workerFolder.file("package.json", baseWorkerPkg);
  if (baseWorkerToml) workerFolder.file("wrangler.toml", baseWorkerToml);

  // 4. Custom Server spots.json + static web UI files
  const serverFolder = root.folder("server");
  const serverStaticFolder = serverFolder.folder("static");
  serverFolder.file("spots.json", JSON.stringify(spots, null, 2));

  const [
    baseServerPy,
    baseScorerPy,
    baseStaticIndexHtml,
    baseStaticAppJs,
    baseStaticStylesCss
  ] = await Promise.all([
    fetchAssetText("./downloads/server/server.py"),
    fetchAssetText("./downloads/server/scorer.py"),
    fetchAssetText("./downloads/server/static/index.html"),
    fetchAssetText("./downloads/server/static/app.js"),
    fetchAssetText("./downloads/server/static/styles.css")
  ]);
  if (baseServerPy) serverFolder.file("server.py", baseServerPy);
  if (baseScorerPy) serverFolder.file("scorer.py", baseScorerPy);
  if (baseStaticIndexHtml) serverStaticFolder.file("index.html", baseStaticIndexHtml);
  if (baseStaticAppJs) serverStaticFolder.file("app.js", baseStaticAppJs);
  if (baseStaticStylesCss) serverStaticFolder.file("styles.css", baseStaticStylesCss);

  // 5. Documentation & Custom Build Guide
  onProgress("Generating custom build, wiring & flashing guide...", 90);
  const customGuideMd = generateBuildGuideMarkdown({
    region,
    spots,
    colors: state?.colors
  });
  root.file("SURF_CLOCK_CUSTOM_BUILD_GUIDE.md", customGuideMd);

  const [baseReadme, baseWiring, baseBomGuide] = await Promise.all([
    fetchAssetText("./downloads/README.md"),
    fetchAssetText("./downloads/docs/WIRING.md"),
    fetchAssetText("./downloads/docs/BUILD_AND_BOM_GUIDE.md")
  ]);
  if (baseReadme) root.file("README.md", baseReadme);
  const docsFolder = root.folder("docs");
  if (baseWiring) docsFolder.file("WIRING.md", baseWiring);
  if (baseBomGuide) {
    docsFolder.file("BUILD_AND_BOM_GUIDE.md", baseBomGuide);
    root.file("BUILD_AND_BOM_GUIDE.md", baseBomGuide);
  }

  return {
    zip,
    zipFilename: `SurfClock_${cleanCode}_Custom_Kit.zip`,
    cleanCode
  };
}

/**
 * Main entry point: Generates and downloads the complete custom full-stack ZIP package
 */
export async function downloadFullStackCustomKit({ state, studio, onProgress = () => {} }) {
  const { zip, zipFilename } = await generateCustomProjectZip({ state, studio, onProgress });

  onProgress("Compressing full-stack package...", 95);
  const zipBlob = await zip.generateAsync({
    type: "blob",
    compression: "DEFLATE",
    compressionOptions: { level: 6 }
  });

  const url = URL.createObjectURL(zipBlob);
  const a = document.createElement("a");
  a.href = url;
  a.download = zipFilename;
  document.body.appendChild(a);
  a.click();

  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 2500);

  onProgress("✅ Full-stack custom package ready!", 100);
  return zipFilename;
}
