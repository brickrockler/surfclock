/**
 * SURF CLOCK (SC-01) — GLOBAL SURF BREAK INTELLIGENCE & GEOCODING ENGINE
 * Combines:
 * 1. Curated database of 35+ world-class surf coastlines (~180 iconic breaks) with exact GPS,
 *    radial dial slot ordering (0°, -60°, +60°, -120°, +120°), optimal swell & conditions.
 * 2. Live global surf break catalog for nearest-5 radial coastline solver from ANY (lat, lng) on Earth.
 * 3. Live geocoding via Google Maps Places/Geocoder API (if key provided) + OpenStreetMap Photon/Nominatim
 *    + Overpass API beach lookup + Open-Meteo Marine API live swell telemetry.
 */

export const DIAL_SLOTS = [
  { index: 0, clock: "12:00", angleDeg: 0,    labelPos: "TOP CENTER",  cx: 0.0,   cy: 74.0,  maxW: 96.0,  defaultCapH: 4.25, strokeW: 0.72, tracking: 0.40 },
  { index: 1, clock: "10:00", angleDeg: -60,  labelPos: "UPPER LEFT",  cx: -58.8, cy: 48.2,  maxW: 39.2,  defaultCapH: 3.90, strokeW: 0.68, tracking: 0.38 },
  { index: 2, clock: "02:00", angleDeg: 60,   labelPos: "UPPER RIGHT", cx: 58.8,  cy: 48.2,  maxW: 39.2,  defaultCapH: 3.90, strokeW: 0.68, tracking: 0.38 },
  { index: 3, clock: "08:00", angleDeg: -120, labelPos: "LOWER LEFT",  cx: -58.2, cy: -5.2,  maxW: 39.5,  defaultCapH: 3.90, strokeW: 0.68, tracking: 0.38 },
  { index: 4, clock: "04:00", angleDeg: 120,  labelPos: "LOWER RIGHT", cx: 58.5,  cy: -5.2,  maxW: 39.5,  defaultCapH: 3.85, strokeW: 0.68, tracking: 0.36 },
];

export const CURATED_REGIONS = [
  {
    id: "nazare-pt",
    name: "Nazaré & Silver Coast, Portugal",
    shortName: "NAZARÉ, PT",
    code: "NAZ-PRT",
    country: "Portugal",
    isIconicGlobal: true,
    keywords: ["nazare", "nazaré", "praia do norte", "supertubos", "peniche", "ericeira", "coxos", "portugal"],
    lat: 39.609,
    lng: -9.086,
    swellHeightM: 4.2,
    swellPeriodS: 18,
    swellDir: "WNW",
    windKt: 6,
    windDir: "E",
    activeSlot: 0,
    worthItScore: 9.8,
    beaches: [
      { name: "PRAIA NORTE", lat: 39.609, lng: -9.086, quality: 9.9, swellDir: "WNW", type: "Submarine Canyon Giant" },
      { name: "SUPERTUBOS",  lat: 39.344, lng: -9.363, quality: 9.7, swellDir: "SW",  type: "Heavy European Pipeline" },
      { name: "COXOS REEF",  lat: 39.004, lng: -9.426, quality: 9.8, swellDir: "NW",  type: "World-Class Right Slab" },
      { name: "BALEAL BAY",  lat: 39.373, lng: -9.339, quality: 9.0, swellDir: "NNE", type: "North Headland Reef" },
      { name: "PEDRA BRNCA", lat: 38.976, lng: -9.419, quality: 9.3, swellDir: "W",   type: "Hollow Left Reef" },
    ],
  },
  {
    id: "jaws-maui",
    name: "Peahi (Jaws) & North Shore, Maui",
    shortName: "JAWS · MAUI",
    code: "JAW-MAU",
    country: "United States",
    isIconicGlobal: true,
    keywords: ["jaws", "peahi", "maui", "honolua", "hookipa", "lahaina", "maalaea", "hawaii"],
    lat: 20.943,
    lng: -156.298,
    swellHeightM: 3.9,
    swellPeriodS: 19,
    swellDir: "NNE",
    windKt: 9,
    windDir: "SSE",
    activeSlot: 0,
    worthItScore: 9.9,
    beaches: [
      { name: "JAWS PEAHI",  lat: 20.943, lng: -156.298, quality: 10.0, swellDir: "NNE", type: "Outer Deepwater Cathedral" },
      { name: "HONOLUA BAY", lat: 21.014, lng: -156.639, quality: 9.9,  swellDir: "NW",  type: "Hollow Cave Right Point" },
      { name: "HOOKIPA PT",  lat: 20.934, lng: -156.357, quality: 9.3,  swellDir: "ENE", type: "Tradewind Reef Peak" },
      { name: "MAALAEA",     lat: 20.793, lng: -156.510, quality: 9.5,  swellDir: "SSW", type: "Freight Train Fast Right" },
      { name: "LAHAINA HBR", lat: 20.871, lng: -156.679, quality: 8.9,  swellDir: "SW",  type: "Shallow Reef Wall" },
    ],
  },
  {
    id: "oahu-north",
    name: "Pipeline & North Shore, Oahu, Hawaii",
    shortName: "PIPELINE, HI",
    code: "HNL-NTH",
    country: "United States",
    isIconicGlobal: true,
    keywords: ["pipeline", "banzai", "oahu", "north shore", "waimea", "sunset beach", "haleiwa", "hawaii"],
    lat: 21.665,
    lng: -158.053,
    swellHeightM: 3.5,
    swellPeriodS: 18,
    swellDir: "NW",
    windKt: 10,
    windDir: "ENE",
    activeSlot: 0,
    worthItScore: 9.8,
    beaches: [
      { name: "PIPELINE",    lat: 21.665, lng: -158.053, quality: 10.0, swellDir: "NW",  type: "Shallow Cavern Reef" },
      { name: "WAIMEA BAY",  lat: 21.641, lng: -158.066, quality: 9.8,  swellDir: "NNW", type: "Iconic Big Wave Point" },
      { name: "SUNSET BCH",  lat: 21.678, lng: -158.041, quality: 9.6,  swellDir: "N",   type: "Deep Water West Peak" },
      { name: "HALEIWA",     lat: 21.595, lng: -158.105, quality: 9.3,  swellDir: "WNW", type: "Alii Reef Bowl" },
      { name: "LANIAKEA",    lat: 21.618, lng: -158.085, quality: 9.1,  swellDir: "NNE", type: "Long Right Reef" },
    ],
  },
  {
    id: "teahupoo-tahiti",
    name: "Teahupo'o & Tahiti Iti, Polynesia",
    shortName: "TEAHUPO'O",
    code: "THP-PYF",
    country: "French Polynesia",
    isIconicGlobal: true,
    keywords: ["teahupoo", "teahupo'o", "tahiti", "polynesia", "vairao", "taapuna", "papara"],
    lat: -17.847,
    lng: -149.267,
    swellHeightM: 3.3,
    swellPeriodS: 17,
    swellDir: "SSW",
    windKt: 7,
    windDir: "ENE",
    activeSlot: 0,
    worthItScore: 9.9,
    beaches: [
      { name: "TEAHUPOO",    lat: -17.847, lng: -149.267, quality: 10.0, swellDir: "SSW", type: "Heaviest Reef Pass on Earth" },
      { name: "VAIRAO PASS", lat: -17.808, lng: -149.292, quality: 9.4,  swellDir: "S",   type: "Deep Lagoon Barrier Left" },
      { name: "TAAPUNA",     lat: -17.619, lng: -149.619, quality: 9.5,  swellDir: "SW",  type: "Hollow West Lagoon Pass" },
      { name: "PAPARA BCH",  lat: -17.772, lng: -149.492, quality: 8.9,  swellDir: "SSE", type: "Black Sand Reef Peak" },
      { name: "MARAA PASS",  lat: -17.744, lng: -149.572, quality: 9.2,  swellDir: "WSW", type: "Outer Reef Left Barrel" },
    ],
  },
  {
    id: "mavericks-ca",
    name: "Mavericks & NorCal Coldwater, CA",
    shortName: "MAVERICKS",
    code: "MAV-CAL",
    country: "United States",
    isIconicGlobal: true,
    keywords: ["mavericks", "half moon bay", "pillar point", "ocean beach", "san francisco", "steamer lane", "california"],
    lat: 37.493,
    lng: -122.499,
    swellHeightM: 3.7,
    swellPeriodS: 18,
    swellDir: "W",
    windKt: 6,
    windDir: "E",
    activeSlot: 0,
    worthItScore: 9.6,
    beaches: [
      { name: "MAVERICKS",   lat: 37.493, lng: -122.499, quality: 9.9, swellDir: "W",   type: "Outer Coldwater Big Wave Ledge" },
      { name: "OCEAN BEACH", lat: 37.759, lng: -122.511, quality: 9.5, swellDir: "WNW", type: "Heavy Outer Sandbar Peaks" },
      { name: "STEAMER LN",  lat: 36.951, lng: -122.025, quality: 9.6, swellDir: "NW",  type: "Santa Cruz Cliff Point" },
      { name: "PLEASURE PT", lat: 36.963, lng: -121.966, quality: 9.3, swellDir: "SSW", type: "Kelp Bed Reef Wall" },
      { name: "RINCON PT",   lat: 34.373, lng: -119.477, quality: 9.7, swellDir: "WSW", type: "Queen of the Coast Right" },
    ],
  },
  {
    id: "bali-uluwatu",
    name: "Uluwatu & Bukit Peninsula, Bali",
    shortName: "ULUWATU",
    code: "DPS-IDN",
    country: "Indonesia",
    isIconicGlobal: true,
    keywords: ["uluwatu", "bali", "padang padang", "impossibles", "bingin", "canggu", "keramas", "indonesia"],
    lat: -8.814,
    lng: 115.088,
    swellHeightM: 2.8,
    swellPeriodS: 16,
    swellDir: "SW",
    windKt: 11,
    windDir: "ESE",
    activeSlot: 0,
    worthItScore: 9.7,
    beaches: [
      { name: "ULUWATU",     lat: -8.814, lng: 115.088, quality: 9.9, swellDir: "SW",  type: "Racetrack & Outside Corner" },
      { name: "PADANG",      lat: -8.811, lng: 115.103, quality: 9.9, swellDir: "SSW", type: "Balinese Pipeline Limestone" },
      { name: "IMPOSSIBLES", lat: -8.805, lng: 115.111, quality: 9.4, swellDir: "WSW", type: "Fast Long Left Reef" },
      { name: "BINGIN REEF", lat: -8.805, lng: 115.113, quality: 9.3, swellDir: "S",   type: "Mechanical Left Barrel" },
      { name: "KERAMAS",     lat: -8.598, lng: 115.337, quality: 9.5, swellDir: "SSE", type: "East Coast High-Perf Right" },
    ],
  },
  {
    id: "jbay-sa",
    name: "Jeffreys Bay & Supertubes, South Africa",
    shortName: "J-BAY, ZA",
    code: "JBY-ZAF",
    country: "South Africa",
    isIconicGlobal: true,
    keywords: ["j-bay", "jbay", "jeffreys bay", "supertubes", "south africa", "st francis", "boneyards"],
    lat: -34.049,
    lng: 24.931,
    swellHeightM: 2.9,
    swellPeriodS: 16,
    swellDir: "SSE",
    windKt: 9,
    windDir: "WSW",
    activeSlot: 0,
    worthItScore: 9.8,
    beaches: [
      { name: "SUPERTUBES",  lat: -34.049, lng: 24.931, quality: 10.0, swellDir: "SSE", type: "Fastest Right Point on Earth" },
      { name: "BONEYARDS",   lat: -34.043, lng: 24.932, quality: 9.3,  swellDir: "SE",  type: "Top of Point Reef Ledge" },
      { name: "MAGNA TUBES", lat: -34.038, lng: 24.933, quality: 9.2,  swellDir: "E",   type: "Heavy Wedge Barrel" },
      { name: "ST FRANCIS",  lat: -34.165, lng: 24.832, quality: 9.6,  swellDir: "ESE", type: "Bruce's Beauties Right" },
      { name: "MUIZENBERG",  lat: -34.109, lng: 18.471, quality: 8.6,  swellDir: "S",   type: "False Bay South Swell" },
    ],
  },
  {
    id: "gold-coast",
    name: "Superbank & Snapper Rocks, Australia",
    shortName: "SNAPPER, AU",
    code: "OOL-QLD",
    country: "Australia",
    isIconicGlobal: true,
    keywords: ["snapper", "snapper rocks", "superbank", "kirra", "gold coast", "coolangatta", "burleigh", "rainbow bay"],
    lat: -28.163,
    lng: 153.550,
    swellHeightM: 2.6,
    swellPeriodS: 14,
    swellDir: "ENE",
    windKt: 7,
    windDir: "SSE",
    activeSlot: 0,
    worthItScore: 9.6,
    beaches: [
      { name: "SNAPPER",     lat: -28.162, lng: 153.551, quality: 9.9, swellDir: "ENE", type: "2km Superbank Sand-Bottom Right" },
      { name: "KIRRA POINT", lat: -28.165, lng: 153.535, quality: 9.8, swellDir: "E",   type: "Hollow Freight Train Barrel" },
      { name: "RAINBOW BAY", lat: -28.164, lng: 153.548, quality: 9.4, swellDir: "NE",  type: "Greenmount Inside Section" },
      { name: "BURLEIGH HD", lat: -28.088, lng: 153.457, quality: 9.5, swellDir: "SE",  type: "Basalt Boulders Right Point" },
      { name: "DURANBAH",    lat: -28.168, lng: 153.552, quality: 9.2, swellDir: "ESE", type: "River Mouth Wedge A-Frames" },
    ],
  },
  {
    id: "sydney-icons",
    name: "Sydney Icons (Bondi, Bronte & Manly), NSW",
    shortName: "BONDI / SYD",
    code: "SYD-ICN",
    country: "Australia",
    isIconicGlobal: true,
    keywords: ["sydney icons", "bondi", "bronte", "tamarama", "maroubra", "manly"],
    lat: -33.891,
    lng: 151.276,
    swellHeightM: 1.9,
    swellPeriodS: 13,
    swellDir: "SSE",
    windKt: 8,
    windDir: "WNW",
    activeSlot: 2,
    worthItScore: 8.8,
    beaches: [
      { name: "BONDI",       lat: -33.891, lng: 151.276, quality: 9.2, swellDir: "SE",  type: "Iconic Crescent Bay" },
      { name: "MANLY",       lat: -33.797, lng: 151.288, quality: 9.1, swellDir: "ENE", type: "Queenscliff & Steyne" },
      { name: "BRONTE",      lat: -33.904, lng: 151.268, quality: 9.1, swellDir: "SSE", type: "South Reef & Express" },
      { name: "TAMARAMA",    lat: -33.900, lng: 151.270, quality: 9.3, swellDir: "E",   type: "Deep Water Wedge Reef" },
      { name: "MAROUBRA",    lat: -33.949, lng: 151.257, quality: 9.2, swellDir: "SSE", type: "Heavy Swell Magnet" },
    ],
  },
  {
    id: "sydney-north",
    name: "Sydney Northern Beaches, NSW",
    shortName: "SYDNEY NTH",
    code: "SYD-NTH",
    country: "Australia",
    keywords: ["northern beaches", "dee why", "long reef", "curl curl", "freshwater", "freshie", "queensie", "queenscliff", "narrabeen", "collaroy"],
    lat: -33.748,
    lng: 151.309,
    swellHeightM: 1.9,
    swellPeriodS: 13,
    swellDir: "SSE",
    windKt: 8,
    windDir: "WNW",
    activeSlot: 2,
    worthItScore: 8.2,
    beaches: [
      { name: "LONG REEF",   lat: -33.743, lng: 151.316, quality: 9.2, swellDir: "NE",  type: "Reef / Bombora" },
      { name: "QUEENSIE"   , lat: -33.785, lng: 151.290, quality: 8.7, swellDir: "ESE", type: "North End Bank" },
      { name: "DEE WHY",     lat: -33.754, lng: 151.299, quality: 9.4, swellDir: "SSE", type: "Right Point / Bowl" },
      { name: "FRESHIE",     lat: -33.779, lng: 151.291, quality: 8.5, swellDir: "E",   type: "Protected Wedge" },
      { name: "CURL CURL",   lat: -33.769, lng: 151.296, quality: 9.0, swellDir: "SE",  type: "Heavy Beachbreak" },
    ],
  },

  {
    id: "kiama-south-coast",
    name: "Kiama & Gerringong, South Coast NSW",
    shortName: "KIAMA / STH",
    code: "KIA-NSW",
    country: "Australia",
    keywords: ["kiama", "gerringong", "bombo", "minnamurra", "mystics", "werri", "jamberoo", "killalea", "the farm"],
    lat: -34.670,
    lng: 150.854,
    swellHeightM: 2.2,
    swellPeriodS: 14,
    swellDir: "SSE",
    windKt: 8,
    windDir: "WNW",
    activeSlot: 0,
    worthItScore: 9.3,
    beaches: [
      { name: "THE FARM",   lat: -34.602, lng: 150.861, quality: 9.5, type: "Killalea Right Point & Bowl" },
      { name: "MYSTICS",    lat: -34.614, lng: 150.858, quality: 9.4, type: "Minamurra Wedge Peak" },
      { name: "BOMBO BCH",  lat: -34.655, lng: 150.860, quality: 8.9, type: "Heavy Swell Magnet Beach" },
      { name: "KIAMA SURF", lat: -34.674, lng: 150.856, quality: 8.5, type: "Town Headland Cove" },
      { name: "WERRI BCH",  lat: -34.743, lng: 150.835, quality: 9.1, type: "North & South Point Reefs" },
    ],
  },
  {
    id: "sydney-east",
    name: "Sydney Eastern Suburbs, NSW",
    shortName: "BONDI / EAST",
    code: "SYD-EST",
    country: "Australia",
    keywords: ["eastern suburbs", "bondi beach", "north bondi", "bronte beach", "tamarama", "coogee", "maroubra", "clovelly", "randwick", "waverley", "paddington", "surry hills", "newtown", "redfern", "double bay", "rose bay"],
    lat: -33.904,
    lng: 151.268,
    swellHeightM: 1.8,
    swellPeriodS: 13,
    swellDir: "SE",
    windKt: 8,
    windDir: "WNW",
    activeSlot: 1,
    worthItScore: 8.6,
    beaches: [
      { name: "BONDI",     lat: -33.891, lng: 151.276, quality: 9.1, type: "Iconic Crescent Bay" },
      { name: "TAMARAMA",  lat: -33.900, lng: 151.270, quality: 9.3, type: "Deep Water Reef/Bank" },
      { name: "BRONTE",    lat: -33.904, lng: 151.268, quality: 9.1, type: "South Reef & Express" },
      { name: "COOGEE",    lat: -33.921, lng: 151.258, quality: 8.7, type: "Protected Eastern Bay" },
      { name: "MAROUBRA",  lat: -33.949, lng: 151.257, quality: 9.2, type: "Open Swell Magnet" },
    ],
  },
  {
    id: "byron-bay",
    name: "Byron Bay & Ballina, NSW",
    shortName: "BYRON BAY",
    code: "BYR-NSW",
    country: "Australia",
    lat: -28.643,
    lng: 153.612,
    swellHeightM: 2.1,
    swellPeriodS: 14,
    swellDir: "E",
    windKt: 6,
    windDir: "SW",
    activeSlot: 0,
    worthItScore: 9.1,
    beaches: [
      { name: "THE PASS",    lat: -28.638, lng: 153.626, quality: 9.6, type: "Long Right Point" },
      { name: "WATEGOS",     lat: -28.636, lng: 153.633, quality: 8.8, type: "Cruisy Point" },
      { name: "LENNOX HEAD", lat: -28.797, lng: 153.600, quality: 9.7, type: "World-Class Right" },
      { name: "TALLOWS",     lat: -28.653, lng: 153.628, quality: 8.6, type: "Punchy Beachbreak" },
      { name: "BROKEN HEAD", lat: -28.706, lng: 153.616, quality: 9.0, type: "Sand Bottom Point" },
    ],
  },
  {
    id: "torquay-bells",
    name: "Torquay & Surf Coast, VIC",
    shortName: "BELLS / VIC",
    code: "BEL-VIC",
    country: "Australia",
    lat: -38.368,
    lng: 144.283,
    swellHeightM: 2.6,
    swellPeriodS: 16,
    swellDir: "SW",
    windKt: 10,
    windDir: "NW",
    activeSlot: 0,
    worthItScore: 9.0,
    beaches: [
      { name: "BELLS BEACH", lat: -38.368, lng: 144.283, quality: 9.7, type: "Rincoe & Bowl Reef" },
      { name: "WINKIPOP",    lat: -38.365, lng: 144.289, quality: 9.6, type: "Fast Reef Wall" },
      { name: "JAN JUC",     lat: -38.348, lng: 144.307, quality: 8.5, type: "Cliffs Beachbreak" },
      { name: "TORQUAY PT",  lat: -38.340, lng: 144.325, quality: 8.3, type: "Longboard Point" },
      { name: "THIRTEENTH",  lat: -38.287, lng: 144.455, quality: 9.0, type: "Heavy Reef/Bank" },
    ],
  },
  {
    id: "margaret-river",
    name: "Margaret River, Western Australia",
    shortName: "MARGARET RVR",
    code: "MRV-WA",
    country: "Australia",
    lat: -33.972,
    lng: 114.982,
    swellHeightM: 3.1,
    swellPeriodS: 17,
    swellDir: "WSW",
    windKt: 9,
    windDir: "E",
    activeSlot: 2,
    worthItScore: 9.4,
    beaches: [
      { name: "MAIN BREAK",  lat: -33.972, lng: 114.982, quality: 9.6, type: "Powerful A-Frame Reef" },
      { name: "THE BOX",     lat: -33.966, lng: 114.985, quality: 9.5, type: "Mutant Right Slab" },
      { name: "NORTH POINT", lat: -33.861, lng: 114.982, quality: 9.8, type: "Deep Barrel Reef" },
      { name: "YALLINGUP",   lat: -33.640, lng: 115.012, quality: 8.9, type: "Outer Bombora Reef" },
      { name: "INJIDUP",     lat: -33.699, lng: 114.985, quality: 9.1, type: "Carparks Point" },
    ],
  },
  {
    id: "santa-cruz",
    name: "Santa Cruz, California",
    shortName: "SANTA CRUZ",
    code: "SCZ-CAL",
    country: "United States",
    lat: 36.951,
    lng: -122.025,
    swellHeightM: 2.3,
    swellPeriodS: 15,
    swellDir: "WNW",
    windKt: 5,
    windDir: "NNE",
    activeSlot: 0,
    worthItScore: 8.9,
    beaches: [
      { name: "STEAMER LN",  lat: 36.951, lng: -122.025, quality: 9.6, type: "Cliff Point Reef" },
      { name: "PLEASURE PT", lat: 36.963, lng: -121.966, quality: 9.4, type: "Kelp Bed Point" },
      { name: "THE HOOK",    lat: 36.960, lng: -121.970, quality: 9.0, type: "Fast Right Reef" },
      { name: "FOUR MILE",   lat: 36.966, lng: -122.123, quality: 8.8, type: "Wild North Coast Reef" },
      { name: "CAPITOLA",    lat: 36.971, lng: -121.951, quality: 8.4, type: "Jetties Right Point" },
    ],
  },
  {
    id: "malibu-la",
    name: "Malibu & Los Angeles, California",
    shortName: "MALIBU / LA",
    code: "MAL-CAL",
    country: "United States",
    lat: 34.036,
    lng: -118.678,
    swellHeightM: 1.6,
    swellPeriodS: 15,
    swellDir: "SSW",
    windKt: 4,
    windDir: "N",
    activeSlot: 0,
    worthItScore: 8.5,
    beaches: [
      { name: "FIRST POINT", lat: 34.036, lng: -118.678, quality: 9.7, type: "Cobblestone Right" },
      { name: "COUNTY LINE", lat: 34.051, lng: -118.964, quality: 8.9, type: "Point & Beachbreak" },
      { name: "TOPANGA PT",  lat: 34.039, lng: -118.583, quality: 8.8, type: "Canyon Cobble Point" },
      { name: "ZUMA BEACH",  lat: 34.017, lng: -118.823, quality: 8.5, type: "Hollow Closeout/Peak" },
      { name: "EL PORTO",    lat: 33.901, lng: -118.422, quality: 8.7, type: "Canyon Swell Magnet" },
    ],
  },
  {
    id: "san-clemente",
    name: "San Clemente & Trestles, California",
    shortName: "TRESTLES / OC",
    code: "SAN-CAL",
    country: "United States",
    lat: 33.382,
    lng: -117.589,
    swellHeightM: 1.8,
    swellPeriodS: 16,
    swellDir: "SW",
    windKt: 5,
    windDir: "ENE",
    activeSlot: 0,
    worthItScore: 9.3,
    beaches: [
      { name: "LOWERS",      lat: 33.382, lng: -117.589, quality: 9.9, type: "High-Perf Cobble A-Frame" },
      { name: "UPPERS",      lat: 33.386, lng: -117.592, quality: 9.3, type: "Fast Cobble Walls" },
      { name: "SAN ONOFRE",  lat: 33.373, lng: -117.568, quality: 9.0, type: "Old Man's Longboard" },
      { name: "T-STREET",    lat: 33.415, lng: -117.620, quality: 8.8, type: "Reef & Pier Bowl" },
      { name: "SALT CREEK",  lat: 33.479, lng: -117.724, quality: 9.1, type: "Gravels Point" },
    ],
  },
  {
    id: "san-diego",
    name: "Encinitas & La Jolla, San Diego, CA",
    shortName: "SAN DIEGO",
    code: "SAN-DIE",
    country: "United States",
    lat: 32.889,
    lng: -117.254,
    swellHeightM: 1.9,
    swellPeriodS: 14,
    swellDir: "WNW",
    windKt: 6,
    windDir: "E",
    activeSlot: 0,
    worthItScore: 8.8,
    beaches: [
      { name: "BLACKS BCH",  lat: 32.889, lng: -117.254, quality: 9.7, type: "Submarine Canyon Peak" },
      { name: "SWAMIS",      lat: 33.034, lng: -117.293, quality: 9.4, type: "Winter Right Reef" },
      { name: "WINDANSEA",   lat: 32.830, lng: -117.282, quality: 9.2, type: "Flat Rock Reef" },
      { name: "SEASIDE RF",  lat: 33.001, lng: -117.279, quality: 9.1, type: "Tabletop Left & Right" },
      { name: "CARDIFF RF",  lat: 33.014, lng: -117.281, quality: 8.8, type: "Kelp Reef River Mouth" },
    ],
  },
  {
    id: "montauk-ny",
    name: "Montauk & Long Island, New York",
    shortName: "MONTAUK NY",
    code: "MTK-NY",
    country: "United States",
    lat: 41.039,
    lng: -71.918,
    swellHeightM: 1.5,
    swellPeriodS: 11,
    swellDir: "ESE",
    windKt: 9,
    windDir: "NNW",
    activeSlot: 0,
    worthItScore: 7.8,
    beaches: [
      { name: "DITCH PLNS",  lat: 41.039, lng: -71.918, quality: 9.0, type: "Shale Reef Point" },
      { name: "TURTLE COVE", lat: 41.070, lng: -71.857, quality: 9.2, type: "Lighthouse Boulder Point" },
      { name: "TERRACE",     lat: 41.030, lng: -71.948, quality: 8.5, type: "Outer Sandbar" },
      { name: "FLYING PT",   lat: 40.885, lng: -72.345, quality: 8.6, type: "Hamptons Jetty Peak" },
      { name: "ROCKAWAY 90", lat: 40.583, lng: -73.816, quality: 8.3, type: "Urban Jetty Barrel" },
    ],
  },
  {
    id: "hossegor-fr",
    name: "Hossegor & Capbreton, SW France",
    shortName: "HOSSEGOR FR",
    code: "HOS-FRA",
    country: "France",
    lat: 43.666,
    lng: -1.444,
    swellHeightM: 2.4,
    swellPeriodS: 15,
    swellDir: "WNW",
    windKt: 7,
    windDir: "E",
    activeSlot: 0,
    worthItScore: 9.5,
    beaches: [
      { name: "LA GRAVIERE", lat: 43.666, lng: -1.444, quality: 9.8, type: "Canyon Dredge Barrel" },
      { name: "LA NORD",     lat: 43.670, lng: -1.445, quality: 9.4, type: "Outer Big Wave Bank" },
      { name: "ESTAGNOTS",   lat: 43.685, lng: -1.441, quality: 9.2, type: "Shifting Sand Peaks" },
      { name: "LA PISTE",    lat: 43.645, lng: -1.448, quality: 9.1, type: "Bunker Hollow Tubes" },
      { name: "GUETHARY",    lat: 43.426, lng: -1.612, quality: 9.3, type: "Parlementia Reef" },
    ],
  },
  {
    id: "ericeira-pt",
    name: "Ericeira & Peniche, Portugal",
    shortName: "ERICEIRA PT",
    code: "ERI-PRT",
    country: "Portugal",
    lat: 38.985,
    lng: -9.422,
    swellHeightM: 2.2,
    swellPeriodS: 14,
    swellDir: "NW",
    windKt: 8,
    windDir: "ENE",
    activeSlot: 2,
    worthItScore: 9.2,
    beaches: [
      { name: "RIBEIRA D'I", lat: 38.988, lng: -9.420, quality: 9.5, type: "Amphitheater Right Point" },
      { name: "COXOS",       lat: 39.004, lng: -9.426, quality: 9.8, type: "World-Class Urchin Slab" },
      { name: "SUPERTUBOS",  lat: 39.344, lng: -9.363, quality: 9.8, type: "Heavy Beach Barrel" },
      { name: "PEDRA BRNCA", lat: 38.976, lng: -9.419, quality: 9.2, type: "Hollow Left Reef" },
      { name: "NAZARE NTH",  lat: 39.609, lng: -9.086, quality: 9.6, type: "Submarine Canyon Peak" },
    ],
  },
  {
    id: "cornwall-uk",
    name: "Newquay & Cornwall, United Kingdom",
    shortName: "CORNWALL UK",
    code: "CRN-GBR",
    country: "United Kingdom",
    lat: 50.416,
    lng: -5.100,
    swellHeightM: 1.8,
    swellPeriodS: 13,
    swellDir: "WSW",
    windKt: 8,
    windDir: "SE",
    activeSlot: 0,
    worthItScore: 8.4,
    beaches: [
      { name: "FISTRAL BCH", lat: 50.416, lng: -5.100, quality: 9.1, type: "North & South Banks" },
      { name: "PORTHLEVEN",  lat: 50.082, lng: -5.316, quality: 9.5, type: "Shallow Harbor Reef" },
      { name: "WATERGATE",   lat: 50.444, lng: -5.041, quality: 8.8, type: "Two-Mile Open Beach" },
      { name: "SENNEN COVE", lat: 50.077, lng: -5.701, quality: 8.9, type: "Land's End Swell Magnet" },
      { name: "POLZEATH",    lat: 50.575, lng: -4.918, quality: 8.4, type: "Sheltered Bay Peaks" },
    ],
  },
  {
    id: "raglan-nz",
    name: "Raglan & West Coast, New Zealand",
    shortName: "RAGLAN NZ",
    code: "RAG-NZL",
    country: "New Zealand",
    lat: -37.822,
    lng: 174.812,
    swellHeightM: 2.3,
    swellPeriodS: 15,
    swellDir: "SW",
    windKt: 7,
    windDir: "E",
    activeSlot: 0,
    worthItScore: 9.4,
    beaches: [
      { name: "MANU BAY",    lat: -37.822, lng: 174.812, quality: 9.7, type: "Boulder Ledge Left" },
      { name: "WHALE BAY",   lat: -37.827, lng: 174.800, quality: 9.6, type: "Endless Boulders Left" },
      { name: "INDICATORS",  lat: -37.829, lng: 174.790, quality: 9.8, type: "Outer Point Wall" },
      { name: "PIHA BAR",    lat: -36.953, lng: 174.468, quality: 9.1, type: "Lion Rock Black Sand" },
      { name: "MURIWAI",     lat: -36.830, lng: 174.426, quality: 8.7, type: "Tasman Heavy Beach" },
    ],
  },
  {
    id: "chiba-jp",
    name: "Ichinomiya & Shonan, Japan",
    shortName: "CHIBA JAPAN",
    code: "CHB-JPN",
    country: "Japan",
    lat: 35.337,
    lng: 140.395,
    swellHeightM: 1.7,
    swellPeriodS: 12,
    swellDir: "ESE",
    windKt: 6,
    windDir: "WNW",
    activeSlot: 0,
    worthItScore: 8.3,
    beaches: [
      { name: "SHIDA SHITA", lat: 35.337, lng: 140.395, quality: 9.2, type: "Olympic Jetty Peak" },
      { name: "MALIBU KSTU", lat: 35.143, lng: 140.295, quality: 9.3, type: "Katsuura Reef Point" },
      { name: "HEBARA BCH",  lat: 35.166, lng: 140.342, quality: 8.9, type: "Typhoon Bay" },
      { name: "KAMAKURA",    lat: 35.305, lng: 139.515, quality: 8.6, type: "Shichirigahama Reef" },
      { name: "ONJUKU",      lat: 35.182, lng: 140.359, quality: 8.5, type: "White Sand Bay" },
    ],
  },
];

// Flatten all curated breaks + additional global breaks for arbitrary (lat, lng) nearest-5 solver
export const GLOBAL_BREAK_POOL = [];
CURATED_REGIONS.forEach((reg) => {
  reg.beaches.forEach((b) => {
    GLOBAL_BREAK_POOL.push({ ...b, regionName: reg.name, regionCode: reg.code });
  });
});

// Comprehensive Australian & Global Coastal Surf Atlas (50+ regional clusters)
export const REGIONAL_SURF_ATLAS = [
  {
    id: "kiama-south-coast",
    name: "Kiama & Gerringong, South Coast NSW",
    shortName: "KIAMA / STH",
    code: "KIA-NSW",
    country: "Australia",
    keywords: ["kiama", "gerringong", "bombo", "minnamurra", "mystics", "werri", "jamberoo", "kiama downs", "killalea", "the farm"],
    lat: -34.670,
    lng: 150.854,
    swellHeightM: 2.1,
    swellPeriodS: 13,
    swellDir: "SSE",
    worthItScore: 9.1,
    beaches: [
      { name: "THE FARM",   lat: -34.602, lng: 150.861, quality: 9.5, type: "Killalea Right Point & Bowl" },
      { name: "MYSTICS",    lat: -34.614, lng: 150.858, quality: 9.4, type: "Minamurra Wedge Peak" },
      { name: "BOMBO BCH",  lat: -34.655, lng: 150.860, quality: 8.8, type: "Heavy Swell Magnet Beach" },
      { name: "KIAMA SURF", lat: -34.674, lng: 150.856, quality: 8.4, type: "Town Headland Cove" },
      { name: "WERRI BCH",  lat: -34.743, lng: 150.835, quality: 9.1, type: "North & South Point Reefs" },
    ],
  },
  {
    id: "wollongong-illawarra",
    name: "Wollongong & Northern Illawarra, NSW",
    shortName: "WOLLONGONG",
    code: "WOL-NSW",
    country: "Australia",
    keywords: ["wollongong", "thirroul", "bulli", "sandon point", "austinmer", "corrimal", "port kembla", "shellharbour", "warilla", "stanwell park", "coalcliff"],
    lat: -34.424,
    lng: 150.893,
    swellHeightM: 2.0,
    swellPeriodS: 13,
    swellDir: "SE",
    worthItScore: 8.9,
    beaches: [
      { name: "SANDON PT",   lat: -34.331, lng: 150.927, quality: 9.6, type: "World-Class Right Point" },
      { name: "THIRROUL",    lat: -34.319, lng: 150.929, quality: 8.8, type: "Hollow Sandbar Peaks" },
      { name: "NORTH GONG",  lat: -34.414, lng: 150.901, quality: 8.6, type: "Town Beach & Reef" },
      { name: "PORT KEMBLA", lat: -34.492, lng: 150.908, quality: 8.9, type: "Clean South End Banks" },
      { name: "WARILLA BCH", lat: -34.552, lng: 150.871, quality: 8.7, type: "Windang Island A-Frames" },
    ],
  },
  {
    id: "shoalhaven-jervis-bay",
    name: "Shoalhaven & Jervis Bay, South Coast NSW",
    shortName: "JERVIS BAY",
    code: "JVB-NSW",
    country: "Australia",
    keywords: ["gerroa", "seven mile", "shoalhaven", "nowra", "culburra", "currarong", "jervis bay", "huskisson", "hyams", "booderee", "sussex inlet", "cudmirrah"],
    lat: -34.930,
    lng: 150.770,
    swellHeightM: 1.9,
    swellPeriodS: 13,
    swellDir: "SSE",
    worthItScore: 8.8,
    beaches: [
      { name: "SEVEN MILE",  lat: -34.773, lng: 150.812, quality: 8.7, type: "Gerroa Point Longboard" },
      { name: "CULBURRA",    lat: -34.926, lng: 150.774, quality: 8.8, type: "Crookhaven Headland" },
      { name: "WARRAIN BCH", lat: -34.945, lng: 150.781, quality: 9.0, type: "Punchy East Swell Bank" },
      { name: "CAVE BEACH",  lat: -35.158, lng: 150.692, quality: 9.3, type: "Booderee South-Swell Cove" },
      { name: "CUDMIRRAH",   lat: -35.206, lng: 150.562, quality: 9.1, type: "Sussex Reef & Sandbar" },
    ],
  },
  {
    id: "ulladulla-mollymook",
    name: "Ulladulla & Mollymook, South Coast NSW",
    shortName: "ULLADULLA",
    code: "ULL-NSW",
    country: "Australia",
    keywords: ["ulladulla", "mollymook", "bendalong", "manyana", "green island", "bawley point", "narrawallee", "milton", "burrill"],
    lat: -35.358,
    lng: 150.475,
    swellHeightM: 2.2,
    swellPeriodS: 14,
    swellDir: "SSE",
    worthItScore: 9.3,
    beaches: [
      { name: "GREEN ISL",   lat: -35.261, lng: 150.525, quality: 9.7, type: "Legendary Left Point Reef" },
      { name: "MANYANA",     lat: -35.253, lng: 150.529, quality: 9.1, type: "Hollow Beach & Reef" },
      { name: "MOLLYMOOK",   lat: -35.335, lng: 150.476, quality: 9.2, type: "Golf Course Reef" },
      { name: "RENNIES BCH", lat: -35.371, lng: 150.471, quality: 8.9, type: "Heavy Wedge Beachbreak" },
      { name: "BAWLEY PT",   lat: -35.518, lng: 150.402, quality: 9.4, type: "Guillotines Slab & Point" },
    ],
  },
  {
    id: "batemans-narooma-merimbula",
    name: "Eurobodalla & Far South Coast, NSW",
    shortName: "FAR STH NSW",
    code: "FSC-NSW",
    country: "Australia",
    keywords: ["batemans bay", "broulee", "malua bay", "moruya", "narooma", "dalmeny", "bermagui", "tathra", "merimbula", "pambula", "eden"],
    lat: -35.850,
    lng: 150.180,
    swellHeightM: 2.0,
    swellPeriodS: 13,
    swellDir: "SE",
    worthItScore: 8.8,
    beaches: [
      { name: "MALUA BAY",   lat: -35.794, lng: 150.231, quality: 8.8, type: "Protected Cove Peaks" },
      { name: "BROULEE",     lat: -35.855, lng: 150.178, quality: 9.0, type: "Pink Rocks Reef & Bank" },
      { name: "DALMENY",     lat: -36.159, lng: 150.132, quality: 8.9, type: "Headland Point & Beach" },
      { name: "NAROOMA BAR", lat: -36.214, lng: 150.141, quality: 9.3, type: "Breakwall & Outer Bar" },
      { name: "SHORT POINT", lat: -36.889, lng: 149.927, quality: 8.8, type: "Merimbula Reef & Wedge" },
    ],
  },
  {
    id: "cronulla-sutherland",
    name: "Cronulla & Sutherland Shire, NSW",
    shortName: "CRONULLA",
    code: "CRO-NSW",
    country: "Australia",
    keywords: ["cronulla", "wanda", "elouera", "kurnell", "sutherland", "caringbah", "miranda", "shark island"],
    lat: -34.055,
    lng: 151.155,
    swellHeightM: 2.1,
    swellPeriodS: 13,
    swellDir: "SSE",
    worthItScore: 9.1,
    beaches: [
      { name: "GREENHILLS",  lat: -34.031, lng: 151.178, quality: 8.9, type: "Open Ocean Sandbar" },
      { name: "WANDA BCH",   lat: -34.039, lng: 151.168, quality: 8.8, type: "Punchy Beachbreak" },
      { name: "ELOUERA",     lat: -34.045, lng: 151.162, quality: 9.1, type: "Fast Hollow Banks" },
      { name: "THE ALLEY",   lat: -34.052, lng: 151.157, quality: 9.0, type: "North Cronulla Rip Bowl" },
      { name: "SHARK ISL",   lat: -34.059, lng: 151.159, quality: 9.7, type: "World-Famous Right Slab" },
    ],
  },
  {
    id: "central-coast-nsw",
    name: "Central Coast (Avoca & Terrigal), NSW",
    shortName: "CENTRAL CST",
    code: "CCO-NSW",
    country: "Australia",
    keywords: ["central coast", "avoca", "terrigal", "gosford", "umina", "copacabana", "macmasters", "wamberal", "forresters", "shelly beach", "the entrance", "soldiers beach", "toukley", "batau bay"],
    lat: -33.465,
    lng: 151.438,
    swellHeightM: 2.0,
    swellPeriodS: 13,
    swellDir: "SSE",
    worthItScore: 9.0,
    beaches: [
      { name: "SOLDIERS",    lat: -33.301, lng: 151.568, quality: 9.0, type: "Norah Head Point & Bank" },
      { name: "SHELLY CC",   lat: -33.371, lng: 151.495, quality: 8.9, type: "Left & Right Sandbars" },
      { name: "FORRESTERS",  lat: -33.414, lng: 151.469, quality: 9.2, type: "Outer Reefs & Wedge" },
      { name: "NORTH AVOCA", lat: -33.458, lng: 151.441, quality: 9.1, type: "Consistent Beachbreak" },
      { name: "AVOCA POINT", lat: -33.471, lng: 151.439, quality: 9.4, type: "Rock Platform Point" },
    ],
  },
  {
    id: "newcastle-hunter",
    name: "Newcastle & Lake Macquarie, NSW",
    shortName: "NEWCASTLE",
    code: "NTL-NSW",
    country: "Australia",
    keywords: ["newcastle", "merewether", "bar beach", "dixon park", "nobbys", "stockton", "redhead", "dudley", "caves beach", "catherine hill bay", "lake macquarie", "port stephens", "anna bay", "birubi", "nelson bay"],
    lat: -32.935,
    lng: 151.770,
    swellHeightM: 2.2,
    swellPeriodS: 14,
    swellDir: "SSE",
    worthItScore: 9.3,
    beaches: [
      { name: "NOBBYS REEF", lat: -32.925, lng: 151.796, quality: 9.1, type: "Breakwall Right Reef" },
      { name: "NEWCASTLE",   lat: -32.930, lng: 151.788, quality: 9.0, type: "South End Skatepark Peak" },
      { name: "BAR BEACH",   lat: -32.941, lng: 151.771, quality: 8.9, type: "Protected City Bank" },
      { name: "MEREWETHER",  lat: -32.948, lng: 151.762, quality: 9.6, type: "Championship Reefs" },
      { name: "REDHEAD BCH", lat: -33.016, lng: 151.724, quality: 9.0, type: "Bluff Corner Wedge" },
    ],
  },
  {
    id: "mid-north-coast-nsw",
    name: "Seal Rocks, Forster & Crescent Head, NSW",
    shortName: "MID NTH CST",
    code: "MNC-NSW",
    country: "Australia",
    keywords: ["forster", "tuncurry", "seal rocks", "boomerang", "blueys", "pacific palms", "old bar", "taree", "port macquarie", "crescent head", "kempsey", "south west rocks", "scotts head", "nambucca"],
    lat: -31.850,
    lng: 152.750,
    swellHeightM: 2.0,
    swellPeriodS: 13,
    swellDir: "SE",
    worthItScore: 9.2,
    beaches: [
      { name: "CRESCENT HD", lat: -31.189, lng: 152.978, quality: 9.7, type: "Iconic Long Right Point" },
      { name: "DELICATE",    lat: -31.265, lng: 152.968, quality: 9.2, type: "Heavy A-Frame Beach" },
      { name: "FLYNNS BCH",  lat: -31.448, lng: 152.929, quality: 8.8, type: "Port Macquarie Reef/Bank" },
      { name: "BOOMERANG",   lat: -32.337, lng: 152.545, quality: 9.3, type: "Headland Framed Peaks" },
      { name: "TREACHERY",   lat: -32.445, lng: 152.528, quality: 9.4, type: "Seal Rocks Swell Magnet" },
    ],
  },
  {
    id: "coffs-yamba-angourie",
    name: "Yamba, Angourie & Coffs Coast, NSW",
    shortName: "YAMBA / COFFS",
    code: "YMB-NSW",
    country: "Australia",
    keywords: ["yamba", "angourie", "coffs", "coffs harbour", "sawtell", "emerald beach", "woolgoolga", "arrawarra", "minnie water", "brooms head", "iluka", "evans head", "grafton", "maclean"],
    lat: -29.850,
    lng: 153.260,
    swellHeightM: 2.1,
    swellPeriodS: 13,
    swellDir: "ESE",
    worthItScore: 9.3,
    beaches: [
      { name: "ANGOURIE PT", lat: -29.479, lng: 153.368, quality: 9.8, type: "National Surfing Reserve Point" },
      { name: "TURNERS BCH", lat: -29.431, lng: 153.366, quality: 8.9, type: "Yamba Breakwall Wedge" },
      { name: "MINNIE WTR",  lat: -29.776, lng: 153.302, quality: 8.8, type: "Back Beach Reef & Bank" },
      { name: "EMERALD BCH", lat: -30.159, lng: 153.195, quality: 8.7, type: "Headland Protected Peaks" },
      { name: "PARK BEACH",  lat: -30.292, lng: 153.144, quality: 8.9, type: "Coffs Harbour Main Break" },
    ],
  },
  {
    id: "noosa-sunshine-coast",
    name: "Noosa & Sunshine Coast, QLD",
    shortName: "NOOSA / SUN",
    code: "NSA-QLD",
    country: "Australia",
    keywords: ["noosa", "sunshine coast", "maroochydore", "mooloolaba", "coolum", "caloundra", "moffat", "alexandra headland", "peregian", "sunshine beach", "kawana", "noosa heads"],
    lat: -26.520,
    lng: 153.100,
    swellHeightM: 1.7,
    swellPeriodS: 12,
    swellDir: "ESE",
    worthItScore: 9.2,
    beaches: [
      { name: "FIRST POINT", lat: -26.382, lng: 153.092, quality: 9.6, type: "Perfect Peel Right Point" },
      { name: "TEA TREE",    lat: -26.377, lng: 153.101, quality: 9.7, type: "National Park Point" },
      { name: "COOLUM BCH",  lat: -26.528, lng: 153.095, quality: 8.9, type: "Punchy Beachbreak" },
      { name: "ALEX HEADS",  lat: -26.669, lng: 153.109, quality: 9.0, type: "The Bluff Right Reef" },
      { name: "MOFFAT PT",   lat: -26.789, lng: 153.145, quality: 9.2, type: "Long Right Headland" },
    ],
  },
  {
    id: "mornington-phillip-island",
    name: "Mornington Peninsula & Phillip Island, VIC",
    shortName: "MORNINGTON",
    code: "MPN-VIC",
    country: "Australia",
    keywords: ["mornington", "portsea", "sorrento", "rye", "gunnamatta", "st andrews", "flinders", "phillip island", "woolamai", "smiths beach", "inverloch", "venus bay", "melbourne"],
    lat: -38.450,
    lng: 145.020,
    swellHeightM: 2.3,
    swellPeriodS: 15,
    swellDir: "SW",
    worthItScore: 9.1,
    beaches: [
      { name: "PORTSEA",     lat: -38.332, lng: 144.708, quality: 9.0, type: "Heavy Back Beach Bowl" },
      { name: "RYE OCEAN",   lat: -38.402, lng: 144.812, quality: 8.9, type: "Offshore NNE Sandbars" },
      { name: "GUNNAMATTA",  lat: -38.445, lng: 144.868, quality: 9.3, type: "Consistent Swell Magnet" },
      { name: "SMITHS BCH",  lat: -38.506, lng: 145.252, quality: 8.8, type: "Protected Bay & Reefs" },
      { name: "WOOLAMAI",    lat: -38.545, lng: 145.342, quality: 9.5, type: "Powerful Pinnacles Beach" },
    ],
  },
  {
    id: "fleurieu-mid-coast-sa",
    name: "Middleton & Fleurieu Peninsula, SA",
    shortName: "FLEURIEU SA",
    code: "FLR-SA",
    country: "Australia",
    keywords: ["adelaide", "middleton", "victor harbor", "waitpinga", "goolwa", "seaford", "moana", "port elliot", "fleurieu", "robe", "yorke peninsula", "cactus"],
    lat: -35.530,
    lng: 138.700,
    swellHeightM: 2.0,
    swellPeriodS: 14,
    swellDir: "SW",
    worthItScore: 8.7,
    beaches: [
      { name: "SEAFORD RF",  lat: -35.188, lng: 138.468, quality: 8.8, type: "Mid Coast Reef Peak" },
      { name: "WAITPINGA",   lat: -35.631, lng: 138.502, quality: 9.2, type: "Powerful Southern Ocean Bank" },
      { name: "PARSONS BCH", lat: -35.636, lng: 138.468, quality: 9.1, type: "Heavy Left & Right Peaks" },
      { name: "CHITON RKS",  lat: -35.542, lng: 138.665, quality: 8.6, type: "Dumpers & Outer Bank" },
      { name: "MIDDLETON",   lat: -35.514, lng: 138.712, quality: 8.7, type: "Consistent Point & Beach" },
    ],
  },
  {
    id: "perth-yallingup-wa",
    name: "Perth, Mandurah & Yallingup, WA",
    shortName: "PERTH / WA",
    code: "PER-WA",
    country: "Australia",
    keywords: ["perth", "trigg", "scarborough", "cottesloe", "fremantle", "mandurah", "secret harbour", "yallingup", "dunsborough", "busselton", "lancelin", "geraldton", "kalbarri", "esperance", "albany", "denmark"],
    lat: -31.880,
    lng: 115.750,
    swellHeightM: 1.9,
    swellPeriodS: 14,
    swellDir: "WSW",
    worthItScore: 8.8,
    beaches: [
      { name: "TRIGG POINT", lat: -31.874, lng: 115.751, quality: 9.1, type: "Hollow Limestone Reef" },
      { name: "SCARBOROUGH", lat: -31.894, lng: 115.754, quality: 8.8, type: "Punchy Metro Beachbreak" },
      { name: "COTTESLOE",   lat: -31.994, lng: 115.751, quality: 8.6, type: "Cove & Groyne Left" },
      { name: "SECRET HBR",  lat: -32.408, lng: 115.744, quality: 8.7, type: "Consistent Southern Metro" },
      { name: "AVALON WA",   lat: -32.589, lng: 115.632, quality: 9.2, type: "Mandurah Left Reef" },
    ],
  },
  {
    id: "hobart-tasmania",
    name: "Hobart & South Arm, Tasmania",
    shortName: "HOBART TAS",
    code: "HBA-TAS",
    country: "Australia",
    keywords: ["hobart", "tasmania", "clifton beach", "park beach", "dodges ferry", "eaglehawk neck", "shipstern", "scamander", "bicheno", "marrawah", "launceston"],
    lat: -42.990,
    lng: 147.530,
    swellHeightM: 2.2,
    swellPeriodS: 15,
    swellDir: "SSW",
    worthItScore: 8.9,
    beaches: [
      { name: "PARK BEACH",  lat: -42.858, lng: 147.621, quality: 8.7, type: "Dodges Ferry Wedge" },
      { name: "CLIFTON BCH", lat: -42.998, lng: 147.528, quality: 9.1, type: "South Arm Swell Magnet" },
      { name: "GOATS BEACH", lat: -43.025, lng: 147.508, quality: 8.8, type: "Hollow Southern Peaks" },
      { name: "ROARING BCH", lat: -43.095, lng: 147.668, quality: 9.0, type: "Tasman Peninsula Bowl" },
      { name: "SHIPSTERN",   lat: -43.208, lng: 147.752, quality: 9.9, type: "Mutant Step Slab" },
    ],
  },
  {
    id: "raglan-auckland-nz",
    name: "Raglan & West Coast, New Zealand",
    shortName: "RAGLAN NZ",
    code: "RAG-NZL",
    country: "New Zealand",
    keywords: ["raglan", "manu bay", "piha", "muriwai", "auckland", "mount maunganui", "tauranga", "gisborne", "taranaki", "dunedin", "christchurch", "new zealand"],
    lat: -37.820,
    lng: 174.810,
    swellHeightM: 2.4,
    swellPeriodS: 15,
    swellDir: "SW",
    worthItScore: 9.6,
    beaches: [
      { name: "INDICATORS",  lat: -37.818, lng: 174.792, quality: 9.7, type: "2km Endless Left Point" },
      { name: "WHALE BAY",   lat: -37.822, lng: 174.801, quality: 9.5, type: "Ledge Boulders Left" },
      { name: "MANU BAY",    lat: -37.825, lng: 174.809, quality: 9.8, type: "Iconic Contest Point" },
      { name: "NGARUNUI",    lat: -37.808, lng: 174.838, quality: 8.6, type: "Black Sand Beachbreak" },
      { name: "RUAPUKE",     lat: -37.905, lng: 174.772, quality: 9.0, type: "Wild West Coast Peaks" },
    ],
  },
  {
    id: "cornwall-newquay-uk",
    name: "Newquay & North Cornwall, UK",
    shortName: "CORNWALL UK",
    code: "CRN-GBR",
    country: "United Kingdom",
    keywords: ["cornwall", "newquay", "fistral", "watergate", "perranporth", "polzeath", "bude", "croyde", "devon", "sennen", "st ives"],
    lat: 50.415,
    lng: -5.095,
    swellHeightM: 1.8,
    swellPeriodS: 12,
    swellDir: "WNW",
    worthItScore: 8.8,
    beaches: [
      { name: "WATERGATE",   lat: 50.444, lng: -5.041, quality: 8.9, type: "Wide Atlantic Beachbreak" },
      { name: "FISTRAL BCH", lat: 50.416, lng: -5.099, quality: 9.3, type: "UK Surf Capital Peaks" },
      { name: "CRANTOCK",    lat: 50.404, lng: -5.118, quality: 8.7, type: "River Gannel Sandbar" },
      { name: "PERRANPORTH", lat: 50.348, lng: -5.158, quality: 8.8, type: "3-Mile Exposed Atlantic" },
      { name: "SENNEN COVE", lat: 50.076, lng: -5.698, quality: 9.1, type: "Land's End Swell Magnet" },
    ],
  },
];

REGIONAL_SURF_ATLAS.forEach((reg) => {
  reg.beaches.forEach((b) => {
    GLOBAL_BREAK_POOL.push({ ...b, regionName: reg.name, regionCode: reg.code });
  });
});

const EXTRA_GLOBAL_BREAKS = [
  { name: "NOOSA FIRST", lat: -26.382, lng: 153.092, quality: 9.5, type: "Point" },
  { name: "TEA TREE",    lat: -26.377, lng: 153.101, quality: 9.6, type: "Point" },
  { name: "GRANITE BAY", lat: -26.375, lng: 153.111, quality: 9.2, type: "Point" },
  { name: "ALEX HEADS",  lat: -26.669, lng: 153.109, quality: 8.8, type: "Bluff" },
  { name: "MOFFAT PT",   lat: -26.789, lng: 153.145, quality: 9.0, type: "Point" },
  { name: "RINCON PT",   lat: 34.373,  lng: -119.477, quality: 9.8, type: "Queen of the Coast" },
  { name: "C STREET",    lat: 34.274,  lng: -119.305, quality: 9.0, type: "Cobble Point" },
  { name: "SANDSPIT",    lat: 34.403,  lng: -119.689, quality: 9.4, type: "Harbor Dredge Barrel" },
  { name: "EL CAPITAN",  lat: 34.456,  lng: -120.022, quality: 9.1, type: "Kelp Point" },
  { name: "JALAMA",      lat: 34.511,  lng: -120.502, quality: 8.9, type: "Tarantulas Reef" },
  { name: "OCEAN BEACH", lat: 37.759,  lng: -122.511, quality: 9.5, type: "Heavy Coldwater Bar" },
  { name: "MAVERICKS",   lat: 37.493,  lng: -122.499, quality: 9.9, type: "Outer Big Wave Reef" },
  { name: "LINDA MAR",   lat: 37.599,  lng: -122.502, quality: 8.2, type: "Pacifica Crescent" },
  { name: "BOLINAS",     lat: 37.904,  lng: -122.684, quality: 8.6, type: "Channel Patch" },
  { name: "STINSON BCH", lat: 37.898,  lng: -122.643, quality: 8.3, type: "Sandspit" },
  { name: "MUNDAKA",     lat: 43.408,  lng: -2.696,   quality: 9.9, type: "Rivermouth Left Barrel" },
  { name: "ZARAUTZ",     lat: 43.289,  lng: -2.165,   quality: 8.8, type: "Basque Beachbreak" },
  { name: "ZURRIOLA",    lat: 43.327,  lng: -1.974,   quality: 8.9, type: "San Sebastian Urban Peak" },
  { name: "SOPELANA",    lat: 43.389,  lng: -3.013,   quality: 8.7, type: "Cliff Bay" },
  { name: "BIARRITZ",    lat: 43.479,  lng: -1.563,   quality: 9.0, type: "Côte des Basques" },
  { name: "PAVONES",     lat: 8.385,   lng: -83.136,  quality: 9.8, type: "1km Left Point" },
  { name: "TAMARINDO",   lat: 10.299,  lng: -85.842,  quality: 8.7, type: "Rivermouth" },
  { name: "SANTA TERESA",lat: 9.643,   lng: -85.168,  quality: 9.2, type: "Jungle Beachbreak" },
  { name: "NOSARA",      lat: 9.969,   lng: -85.683,  quality: 9.0, type: "Guiones Peaks" },
  { name: "WITCHS ROCK", lat: 10.838,  lng: -85.823,  quality: 9.4, type: "Offshore A-Frame" },
  { name: "PUERTO ESC",  lat: 15.846,  lng: -97.061,  quality: 9.8, type: "Zicatela Mex Pipe" },
  { name: "PUNTA MITA",  lat: 20.768,  lng: -105.534, quality: 8.9, type: "La Lancha Reef" },
  { name: "SAYULITA",    lat: 20.869,  lng: -105.441, quality: 8.5, type: "Town Right Reef" },
  { name: "BARRA CRUZ",  lat: 15.826,  lng: -95.962,  quality: 9.6, type: "Sand-Bottom Right Point" },
  { name: "SALINA CRUZ", lat: 16.162,  lng: -95.199,  quality: 9.5, type: "Jetty Right Tube" },
  // Granular Sydney Upper & Lower Northern Beaches
  { name: "PALM BEACH",  lat: -33.599, lng: 151.325, quality: 9.1, type: "North Corner & Kiddies" },
  { name: "WHALE BCH",   lat: -33.612, lng: 151.329, quality: 9.2, type: "The Wedge Reef" },
  { name: "AVALON",      lat: -33.636, lng: 151.332, quality: 9.4, type: "North & South Avalon" },
  { name: "BILGOLA",     lat: -33.647, lng: 151.327, quality: 8.8, type: "Headland Pocket Bank" },
  { name: "NEWPORT",     lat: -33.656, lng: 151.324, quality: 9.1, type: "Newport Peak & Reef" },
  { name: "MONA VALE",   lat: -33.678, lng: 151.319, quality: 9.0, type: "Basin & Bongin Reef" },
  { name: "WARRIEWOOD",  lat: -33.694, lng: 151.311, quality: 8.9, type: "Cliff Corner Wedge" },
  { name: "NARRABEEN",   lat: -33.714, lng: 151.304, quality: 9.6, type: "Iconic North Narrabeen Alley" },
  { name: "LONG REEF",   lat: -33.743, lng: 151.316, quality: 9.2, type: "Outer Reef & Bombora" },
  { name: "DEE WHY",     lat: -33.754, lng: 151.299, quality: 9.4, type: "Right Point & Bowl" },
  { name: "CURL CURL",   lat: -33.769, lng: 151.296, quality: 9.1, type: "Heavy Beachbreak" },
  { name: "FRESHIE",     lat: -33.779, lng: 151.291, quality: 8.8, type: "Protected Wedge" },
  { name: "QUEENSIE",    lat: -33.785, lng: 151.290, quality: 8.9, type: "North End Bombora & Bank" },
  { name: "MANLY",       lat: -33.797, lng: 151.288, quality: 9.2, type: "South Steyne & Bower Reef" },
  // Granular Sydney Eastern Suburbs & Sutherland
  { name: "BONDI",       lat: -33.891, lng: 151.276, quality: 9.2, type: "Iconic Crescent Bay" },
  { name: "TAMARAMA",    lat: -33.900, lng: 151.270, quality: 9.3, type: "Deepwater Wedge & Reef" },
  { name: "BRONTE",      lat: -33.904, lng: 151.268, quality: 9.1, type: "South Reef & Express" },
  { name: "COOGEE",      lat: -33.921, lng: 151.258, quality: 8.9, type: "Wedding Cake Island Peaks" },
  { name: "MAROUBRA",    lat: -33.949, lng: 151.257, quality: 9.2, type: "Skatepark & South Reef" },
  { name: "GREENHILLS",  lat: -34.031, lng: 151.178, quality: 8.9, type: "Open Ocean Sandbar" },
  { name: "WANDA BCH",   lat: -34.039, lng: 151.168, quality: 8.9, type: "Punchy Beachbreak" },
  { name: "ELOUERA",     lat: -34.045, lng: 151.162, quality: 9.1, type: "Fast Hollow Banks" },
  { name: "THE ALLEY",   lat: -34.052, lng: 151.157, quality: 9.0, type: "North Cronulla Rip Bowl" },
  { name: "SHARK ISL",   lat: -34.059, lng: 151.159, quality: 9.7, type: "World-Famous Right Slab" },
  { name: "GARIE BEACH", lat: -34.171, lng: 151.066, quality: 9.1, type: "Royal National Park Bank" },
  { name: "STANWELL PK", lat: -34.231, lng: 150.992, quality: 8.9, type: "Heavy Beachbreak" },
  // Granular Los Angeles / Venice / Santa Monica / Orange County
  { name: "VENICE BRKW", lat: 33.985,  lng: -118.475, quality: 9.0, type: "Venice Breakwater Peak" },
  { name: "SANTA MONCA", lat: 34.009,  lng: -118.497, quality: 8.6, type: "Bay Street Sandbar" },
  { name: "SUNSET PT",   lat: 34.039,  lng: -118.554, quality: 8.9, type: "Point & Beachbreak" },
  { name: "MANHATTAN",   lat: 33.884,  lng: -118.414, quality: 8.9, type: "Pier Bowl Sandbar" },
  { name: "HERMOSA",     lat: 33.862,  lng: -118.404, quality: 8.7, type: "South Bay Beachbreak" },
  { name: "HUNTINGTON",  lat: 33.655,  lng: -118.005, quality: 9.2, type: "Surf City Pier Northside" },
  { name: "NEWPORT JTY", lat: 33.596,  lng: -117.905, quality: 9.3, type: "56th St & The Wedge" },
  { name: "THE WEDGE",   lat: 33.593,  lng: -117.882, quality: 9.5, type: "Mutant Jetty Sidewash" },
];
EXTRA_GLOBAL_BREAKS.forEach((b) => GLOBAL_BREAK_POOL.push(b));

export const ALL_KNOWN_REGIONS = [...CURATED_REGIONS, ...REGIONAL_SURF_ATLAS];

// Optional client-supplied Gemini API key (no hardcoded key in public repository)
function getOptionalGeminiKey() {
  try {
    return (typeof window !== "undefined" && (window.SURF_CLOCK_GEMINI_KEY || localStorage.getItem("SURF_CLOCK_GEMINI_KEY"))) || "";
  } catch (_) {
    return "";
  }
}

export function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371.0;
  const dLat = ((lat2 - lat1) * Math.PI) / 180.0;
  const dLon = ((lon2 - lon1) * Math.PI) / 180.0;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180.0) *
      Math.cos((lat2 * Math.PI) / 180.0) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function formatDialBeachName(raw) {
  const norm = String(raw || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  if (!norm.trim()) return "";
  let str = norm
    .toUpperCase()
    .replace(/['’`]/g, "'")
    .replace(/\bBEACH\b/g, "BCH")
    .replace(/\bPOINT\b/g, "PT")
    .replace(/\bHEADLAND\b/g, "HD")
    .replace(/\bHEADS?\b/g, "HD")
    .replace(/\bISLAND\b/g, "ISL")
    .replace(/\bHARBOUR\b/g, "HBR")
    .replace(/\bHARBOR\b/g, "HBR")
    .replace(/\bSAINT\b/g, "ST")
    .replace(/\bMOUNT\b/g, "MT")
    .replace(/[^A-Z0-9 ?\-'./&+]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  if (!str) return "";
  if (str.length > 12) {
    str = str.replace(/\s+(BCH|PT|HD|RF)$/, "").trim();
  }
  if (str.length > 12) {
    str = str.slice(0, 12).trim();
  }
  return str;
}

/**
 * Generates 5 normalized dial beaches for a coastline region.
 * Preserves 0° equator/prime-meridian coordinates and 0° North swell/wind bearings via nullish coalescing (??),
 * while defaulting missing/invalid region coordinates to Sydney Northern Beaches (-33.75, 151.30).
 */
export function generate5BeachesForCoastline(region, customBeaches = null) {
  const hasValidLat = region && typeof region.lat === "number" && !Number.isNaN(region.lat);
  const rawRegLon = region ? (typeof region.lon === "number" ? region.lon : region.lng) : undefined;
  const hasValidLon = typeof rawRegLon === "number" && !Number.isNaN(rawRegLon);

  const baseLat = hasValidLat && hasValidLon ? region.lat : -33.75;
  const baseLon = hasValidLat && hasValidLon ? rawRegLon : 151.30;

  const sourceBeaches =
    Array.isArray(customBeaches) && customBeaches.length > 0
      ? customBeaches
      : Array.isArray(region?.beaches) && region.beaches.length > 0
      ? region.beaches
      : CURATED_REGIONS[0].beaches;

  return Array.from({ length: 5 }, (_, i) => {
    const b = sourceBeaches[i] || {};
    const lat = Number(b.lat ?? baseLat);
    const lon = Number(b.lon ?? b.lng ?? baseLon);
    const openSwellDir = Number(b.openSwellDir ?? region?.openSwellDir ?? 135);
    const dirTolerance = Number(b.dirTolerance ?? 45);
    const windOffshore = Number(b.windOffshore ?? region?.windOffshore ?? 270);
    const windTolerance = Number(b.windTolerance ?? 45);
    const quality = Number(b.quality ?? 8.6);
    const formattedName = formatDialBeachName(b.name);
    return {
      ...b,
      name: formattedName || `BEACH ${i + 1}`,
      lat,
      lon,
      lng: lon,
      openSwellDir,
      dirTolerance,
      windOffshore,
      windTolerance,
      quality,
      type: b.type || "Coastal Surf Break",
    };
  });
}

/**
 * Queries Gemini 3.1 Flash Lite to intelligently find the 5 best actual surf beaches near any location on Earth
 */
export async function queryGemini5BestSurfBeaches(placeLabel, lat, lng) {
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 4500);
    const coordHint = (lat != null && lng != null && (lat !== 0 || lng !== 0))
      ? ` (approx coordinates: ${Number(lat).toFixed(4)}, ${Number(lng).toFixed(4)})`
      : "";
    const prompt = `You are an expert Australian & global surf guide. Find the 5 best actual surf beaches or surf breaks nearest to "${placeLabel}"${coordHint}.
Rules:
1. Must be real, well-known surf breaks or surf beaches actually in or immediately adjacent to "${placeLabel}" (within 5-30km, NEVER pick beaches from a distant city 80km away! E.g. for Kiama NSW return THE FARM, MYSTICS, BOMBO BCH, KIAMA SURF, WERRI BCH).
2. Order the 5 breaks geographically along the coast (North to South, or West to East).
3. "name" must be UPPERCASE, max 11 characters so it fits on a physical Braun clock dial (use clean abbreviations like BCH, PT, HD, RF, ISL if needed).
4. Return strict JSON:
{
  "regionName": "Clean Regional Title (e.g. Kiama & South Coast, NSW)",
  "shortName": "UPPERCASE SHORT TITLE MAX 12 CHARS (e.g. KIAMA / STH)",
  "lat": -34.67,
  "lng": 150.85,
  "beaches": [
    { "name": "MAX 11 CHAR", "lat": -34.60, "lng": 150.86, "quality": 9.3, "type": "Reef / Point / Beachbreak" }
  ]
}`;

    const apiKey = getOptionalGeminiKey();
    if (!apiKey) return null;
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key=${apiKey}`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: ctrl.signal,
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          responseMimeType: "application/json",
          temperature: 0.1,
        },
      }),
    });
    clearTimeout(timer);
    if (!res.ok) return null;
    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) return null;
    const parsed = JSON.parse(text);
    if (!Array.isArray(parsed.beaches) || parsed.beaches.length < 5) return null;
    const beaches = parsed.beaches.slice(0, 5).map((b, i) => ({
      name: formatDialBeachName(b.name || `BREAK ${i + 1}`) || `BREAK ${i + 1}`,
      lat: Number(b.lat ?? lat ?? -33.8),
      lng: Number(b.lng ?? lng ?? 151.2),
      quality: Number(Math.min(9.9, Math.max(6.8, Number(b.quality ?? 8.6))).toFixed(1)),
      type: b.type || "Surf Break",
      distKm: (lat != null && lng != null && b.lat != null && b.lng != null) ? haversineKm(lat, lng, Number(b.lat), Number(b.lng)) : i * 2.5,
    }));
    const rLat = Number(lat ?? parsed.lat ?? beaches[0].lat);
    const rLng = Number(lng ?? parsed.lng ?? beaches[0].lng);
    const shortName = (parsed.shortName || placeLabel.split(",")[0] || "CUSTOM").toUpperCase().slice(0, 12);
    const codePrefix = shortName.replace(/[^A-Z]/g, "").slice(0, 3).padEnd(3, "X");
    return {
      region: {
        id: "gemini-loc-" + codePrefix.toLowerCase(),
        name: parsed.regionName || placeLabel,
        shortName,
        code: `${codePrefix}-GEM`,
        lat: rLat,
        lng: rLng,
        swellHeightM: 2.0,
        swellPeriodS: 13,
        swellDir: "SSE",
        windKt: 7,
        windDir: "OFFSHORE",
        activeSlot: 0,
        worthItScore: Number(Math.max(...beaches.map((b) => b.quality)).toFixed(1)),
      },
      beaches,
      source: "GEMINI_AI_SURF_SEARCH",
    };
  } catch (_) {
    return null;
  }
}

/**
 * Detects whether a search string looks like a street address, unit number, or postcode query
 */
export function isLikelyStreetAddress(query) {
  const q = String(query || "").trim();
  if (!q) return false;
  if (/^\d+[a-zA-Z]?\s+\S+/.test(q)) return true;
  if (/^\d+\/\d+\s+\S+/.test(q)) return true;
  if (/\b(st|street|rd|road|ave|avenue|parade|pde|dr|drive|ln|lane|way|blvd|boulevard|ct|court|pl|place|cres|crescent|hwy|highway|terrace|tce|close|cl|circuit|cct|esplanade|esp)\b/i.test(q)) {
    return true;
  }
  return false;
}

/**
 * Extracts a clean locality / suburb / town short title (<= 12 chars) from any street address or place label
 */
export function extractLocalityShortName(placeLabel) {
  const raw = String(placeLabel || "").trim();
  if (!raw) return "LOCAL COAST";
  const parts = raw.split(",").map((s) => s.trim()).filter(Boolean);
  // If first part is a street address (e.g. "42 Fletcher Street" or "15"), prefer the suburb/neighborhood in part[1]
  for (const part of parts) {
    if (/^\d+$/.test(part)) continue;
    if (/^\d+[a-zA-Z\-\/]*\s+/.test(part)) continue;
    if (isLikelyStreetAddress(part)) continue;
    if (/^(new south wales|nsw|victoria|vic|queensland|qld|western australia|wa|south australia|sa|tasmania|tas|australia|united states|usa|united kingdom|uk|california|ca)$/i.test(part)) {
      continue;
    }
    const cleaned = part.replace(/\b\d{4,5}\b/g, "").trim();
    if (cleaned.length >= 2) {
      return formatDialBeachName(cleaned).slice(0, 12) || cleaned.toUpperCase().slice(0, 12);
    }
  }
  // Fallback: strip leading house numbers and street suffix from parts[0]
  const stripped = parts[0]
    .replace(/^\d+[a-zA-Z\-\/]*\s+/, "")
    .replace(/\b(street|st|road|rd|avenue|ave|parade|pde|drive|dr|lane|ln|boulevard|blvd|place|pl|court|ct|crescent|cres)\b/gi, "")
    .trim();
  return (stripped || parts[0] || "LOCAL").toUpperCase().slice(0, 12);
}

/**
 * Multi-provider CORS street address & place geocoder (ArcGIS World Geocoder + Komoot Photon + OSM Nominatim).
 * Works in the browser with zero API keys for any residential home address, street, suburb, postcode, or beach on Earth.
 */
function getBrowserLocationBias() {
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
  const houseMatch = q.match(/^(\d+[a-zA-Z]?)\s+/);
  const requestedHouseNum = houseMatch ? houseMatch[1].toLowerCase() : null;

  const qTokens = q
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
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
    merged = merged.filter((c) => (c._tokenRatio || 0) >= Math.max(0.6, bestTokenRatio - 0.15));
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

/**
 * Fetches live named beaches & surf spots from OpenStreetMap Overpass API + Wikipedia GeoSearch
 * when an address is on a coastline outside our static break catalog.
 */
async function fetchLiveOsmAndWikiBeaches(lat, lng) {
  if (lat == null || lng == null || (lat === 0 && lng === 0)) return [];
  const results = [];

  const wikiPromise = (async () => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 3200);
    try {
      const wUrl = `https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=${lat}|${lng}&gsradius=10000&gslimit=50&format=json&origin=*`;
      const wRes = await fetch(wUrl, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!wRes.ok) return [];
      const wData = await wRes.json();
      const out = [];
      for (const item of wData?.query?.geosearch || []) {
        const title = item.title || "";
        if (!/beach|point|bay|reef|head|cove|island|surf/i.test(title)) continue;
        if (/station|school|church|railway|council|electoral|highway|hotel|park|hospital|cemetery|club/i.test(title)) continue;
        const clean = formatDialBeachName(title.replace(/\(.*?\)/g, "").split(",")[0]);
        if (clean.length < 3) continue;
        const dKm = haversineKm(lat, lng, item.lat, item.lon);
        out.push({
          name: clean,
          lat: Number(item.lat),
          lng: Number(item.lon),
          distKm: dKm,
          quality: Number(Math.min(9.3, Math.max(7.5, 8.9 - dKm * 0.03)).toFixed(1)),
          type: "Local Coastal Break",
        });
      }
      return out;
    } catch (_) {
      clearTimeout(timer);
      return [];
    }
  })();

  const overpassPromise = (async () => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 3600);
    try {
      const query = `[out:json][timeout:3];(node["natural"="beach"]["name"](around:30000,${lat},${lng});way["natural"="beach"]["name"](around:30000,${lat},${lng});node["sport"="surfing"]["name"](around:35000,${lat},${lng}););out center 40;`;
      const oUrl = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;
      const oRes = await fetch(oUrl, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!oRes.ok) return [];
      const oData = await oRes.json();
      const out = [];
      for (const el of oData?.elements || []) {
        const rawName = el?.tags?.["name:en"] || el?.tags?.name || "";
        if (!rawName) continue;
        if (/dog|nudist|private|hotel|resort|boat|ramp|ferry/i.test(rawName)) continue;
        const bLat = Number(el.lat ?? el?.center?.lat);
        const bLng = Number(el.lon ?? el?.center?.lon);
        if (Number.isNaN(bLat) || Number.isNaN(bLng)) continue;
        const clean = formatDialBeachName(rawName);
        if (clean.length < 3) continue;
        const dKm = haversineKm(lat, lng, bLat, bLng);
        const isSurfTag = el?.tags?.sport === "surfing";
        out.push({
          name: clean,
          lat: bLat,
          lng: bLng,
          distKm: dKm,
          quality: Number(Math.min(9.5, Math.max(7.6, (isSurfTag ? 9.2 : 8.7) - dKm * 0.025)).toFixed(1)),
          type: isSurfTag ? "Mapped Surf Break" : "Local Coastal Beach",
        });
      }
      return out;
    } catch (_) {
      clearTimeout(timer);
      return [];
    }
  })();

  const [wList, oList] = await Promise.all([wikiPromise, overpassPromise]);
  results.push(...oList, ...wList);
  return results;
}

export async function resolve5BestLocalBeaches(lat, lng, placeLabel = "") {
  let targetLat = (lat != null && !Number.isNaN(Number(lat))) ? Number(lat) : 0;
  let targetLng = (lng != null && !Number.isNaN(Number(lng))) ? Number(lng) : 0;
  let resolvedLabel = String(placeLabel || "").trim();

  // 1. If coordinates are missing or (0, 0), geocode the typed address/query first!
  if ((targetLat === 0 && targetLng === 0) && resolvedLabel.length >= 2) {
    const geocoded = await geocodeAddressCandidates(resolvedLabel, 1);
    if (geocoded.length > 0) {
      targetLat = geocoded[0].lat;
      targetLng = geocoded[0].lng;
      resolvedLabel = geocoded[0].label || resolvedLabel;
    }
  }

  const qLower = resolvedLabel.toLowerCase();
  const isStreetAddr = isLikelyStreetAddress(resolvedLabel);

  // 2. Only match a static regional preset directly if the user searched a regional name (NOT a street address)
  //    and the region center is within 8km of the target coordinates.
  if (!isStreetAddr) {
    for (const reg of ALL_KNOWN_REGIONS) {
      const dist = (targetLat !== 0 || targetLng !== 0) ? haversineKm(targetLat, targetLng, reg.lat, reg.lng) : 999;
      const exactNameMatch = reg.name.toLowerCase() === qLower || reg.shortName.toLowerCase() === qLower;
      if (exactNameMatch || dist <= 4.5) {
        return {
          region: { ...reg },
          beaches: reg.beaches.map((b) => ({
            ...b,
            distKm: (targetLat !== 0 || targetLng !== 0) ? haversineKm(targetLat, targetLng, b.lat, b.lng) : 2.0,
          })),
          source: "CURATED_SURF_ATLAS",
        };
      }
    }
  }

  // 3. Optional Gemini AI Search if key is configured
  const geminiResult = await queryGemini5BestSurfBeaches(
    resolvedLabel || `${targetLat.toFixed(3)}, ${targetLng.toFixed(3)}`,
    targetLat,
    targetLng
  );
  if (geminiResult && geminiResult.beaches?.length === 5) {
    return geminiResult;
  }

  // 4. Build deduplicated candidate pool from GLOBAL_BREAK_POOL around (targetLat, targetLng)
  const poolMap = new Map();
  for (const rawBreak of GLOBAL_BREAK_POOL) {
    const formattedName = formatDialBeachName(rawBreak.name);
    if (!formattedName) continue;
    const dKm = (targetLat !== 0 || targetLng !== 0)
      ? haversineKm(targetLat, targetLng, rawBreak.lat, rawBreak.lng)
      : 999;
    const existing = poolMap.get(formattedName);
    if (!existing || dKm < existing.distKm || (Math.abs(dKm - existing.distKm) < 1.0 && (rawBreak.quality ?? 8.5) > (existing.quality ?? 8.5))) {
      poolMap.set(formattedName, {
        ...rawBreak,
        name: formattedName,
        distKm: dKm,
        quality: Number(rawBreak.quality ?? 8.6),
      });
    }
  }

  let allCandidates = Array.from(poolMap.values()).sort((a, b) => a.distKm - b.distKm);
  const closePoolCount = allCandidates.filter((c) => c.distKm <= 25.0).length;

  // 5. If fewer than 5 curated breaks exist within 25km of this address, query live OSM Overpass + Wikipedia beaches
  if (closePoolCount < 5 && (targetLat !== 0 || targetLng !== 0)) {
    const liveBeaches = await fetchLiveOsmAndWikiBeaches(targetLat, targetLng);
    for (const lb of liveBeaches) {
      if (!poolMap.has(lb.name)) {
        poolMap.set(lb.name, lb);
      }
    }
    allCandidates = Array.from(poolMap.values()).sort((a, b) => a.distKm - b.distKm);
  }

  // 6. Select the 5 Best Local Surf Beaches using adaptive coastal radius + surf quality weighting
  const minDistKm = allCandidates.length > 0 ? allCandidates[0].distKm : 0;
  // Tight local coastal cluster (within 9.5km of the nearest beach to the home address)
  let localCluster = allCandidates.filter((c) => c.distKm <= Math.max(9.5, minDistKm + 9.0));
  if (localCluster.length < 5) {
    localCluster = allCandidates.filter((c) => c.distKm <= Math.max(22.0, minDistKm + 18.0));
  }
  if (localCluster.length < 5) {
    localCluster = allCandidates.slice(0, 10);
  }

  // Score each candidate in the local cluster by Surf Quality minus a gentle distance penalty from the nearest beach
  const rankedCluster = localCluster
    .map((c) => ({
      ...c,
      _localScore: (c.quality ?? 8.5) - Math.max(0, c.distKm - minDistKm) * 0.16,
    }))
    .sort((a, b) => b._localScore - a._localScore);

  const top5 = rankedCluster.slice(0, 5);
  // Sort the 5 local beaches geographically North-to-South along the coast so the radial dial reads naturally
  top5.sort((a, b) => b.lat - a.lat);

  // Determine which of the 5 slots is the best/closest break to point to initially
  let bestSlot = 0;
  let bestSlotScore = -999;
  top5.forEach((b, idx) => {
    const s = (b.quality ?? 8.5) - Math.max(0, b.distKm - minDistKm) * 0.12;
    if (s > bestSlotScore) {
      bestSlotScore = s;
      bestSlot = idx;
    }
  });

  const localityShort = extractLocalityShortName(resolvedLabel);
  const codePrefix = localityShort
    .replace(/[^A-Z]/g, "")
    .slice(0, 3)
    .padEnd(3, "X");

  return {
    region: {
      id: "custom-loc-" + codePrefix.toLowerCase(),
      name: resolvedLabel || `${targetLat.toFixed(3)}°, ${targetLng.toFixed(3)}°`,
      shortName: localityShort,
      code: `${codePrefix}-LOC`,
      lat: targetLat,
      lng: targetLng,
      swellHeightM: 1.9,
      swellPeriodS: 13,
      swellDir: "SSE",
      windKt: 8,
      windDir: "OFFSHORE",
      activeSlot: bestSlot,
      worthItScore: Number(Math.max(...top5.map((b) => b.quality ?? 8.6)).toFixed(1)),
    },
    beaches: top5,
    source: "LOCAL_COASTAL_SOLVER",
  };
}

export async function fetchLiveMarineTelemetry(lat, lng) {
  try {
    const url = `https://marine-api.open-meteo.com/v1/marine?latitude=${lat.toFixed(4)}&longitude=${lng.toFixed(4)}&current=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_period`;
    const res = await fetch(url);
    if (!res.ok) return null;
    const data = await res.json();
    const cur = data.current;
    if (!cur || cur.wave_height == null) return null;
    const h = Number(cur.swell_wave_height ?? cur.wave_height ?? 1.6);
    const p = Number(cur.swell_wave_period ?? cur.wave_period ?? 12);
    const deg = Number(cur.wave_direction ?? 135);
    const dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
    const dirStr = dirs[Math.round(((deg % 360) / 22.5)) % 16];
    const energyScore = Math.min(9.8, Math.max(2.2, h * 2.4 + (p - 7) * 0.38));
    return {
      swellHeightM: Number(h.toFixed(1)),
      swellPeriodS: Math.round(p),
      swellDir: dirStr,
      worthItScore: Number(energyScore.toFixed(1)),
      live: true,
    };
  } catch (_) {
    return null;
  }
}

export async function searchLocationsAutocomplete(query) {
  const q = (query || "").trim();
  if (!q) {
    return ALL_KNOWN_REGIONS.slice(0, 9).map((r) => ({
      label: r.name,
      sublabel: `${r.beaches.map((b) => b.name).join(" · ")}`,
      lat: r.lat,
      lng: r.lng,
      regionId: r.id,
      badge: "CURATED",
    }));
  }

  const qLower = q.toLowerCase();
  const isStreet = isLikelyStreetAddress(q);
  const localMatches = [];
  const seenLabels = new Set();

  // Only match curated regions / breaks by substring if the user is NOT typing a residential street address
  if (!isStreet) {
    for (const r of ALL_KNOWN_REGIONS) {
      const beachStr = r.beaches.map((b) => b.name).join(" ");
      const kwStr = Array.isArray(r.keywords) ? r.keywords.join(" ") : "";
      if (
        r.name.toLowerCase().includes(qLower) ||
        r.shortName.toLowerCase().includes(qLower) ||
        (r.country && r.country.toLowerCase().includes(qLower)) ||
        beachStr.toLowerCase().includes(qLower) ||
        kwStr.toLowerCase().includes(qLower)
      ) {
        seenLabels.add(r.name.toLowerCase());
        localMatches.push({
          label: r.name,
          sublabel: r.beaches.map((b) => b.name).join(" · "),
          lat: r.lat,
          lng: r.lng,
          regionId: r.id,
          badge: "5 BEST BREAKS",
        });
      }
    }

    for (const b of GLOBAL_BREAK_POOL) {
      if (b.name.toLowerCase().includes(qLower) || (b.type && b.type.toLowerCase().includes(qLower))) {
        const lbl = `${b.name}${b.regionName ? " — " + b.regionName : " Coastal Break"}`;
        if (!seenLabels.has(lbl.toLowerCase())) {
          seenLabels.add(lbl.toLowerCase());
          localMatches.push({
            label: lbl,
            sublabel: `${b.type || "Surf Break"} · Nearest 5 Local Breaks`,
            lat: b.lat,
            lng: b.lng,
            regionId: null,
            badge: "SURF BREAK",
          });
        }
      }
    }
  }

  let remoteMatches = [];
  if (q.length >= 2) {
    remoteMatches = await geocodeAddressCandidates(q, 6);
  }

  if (q.length >= 3 && localMatches.length === 0 && remoteMatches.length === 0) {
    remoteMatches.push({
      label: q,
      sublabel: `Find 5 best local surf beaches near "${q}"`,
      lat: 0,
      lng: 0,
      regionId: null,
      badge: "📍 SEARCH ADDRESS",
    });
  }

  const ordered = isStreet ? [...remoteMatches, ...localMatches] : [...localMatches, ...remoteMatches];
  const combined = [];
  const dedup = new Set();
  for (const item of ordered) {
    const key = (item.label || "").toLowerCase();
    if (!key || dedup.has(key)) continue;
    dedup.add(key);
    combined.push(item);
  }
  return combined.slice(0, 6);
}
