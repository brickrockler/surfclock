/**
 * SURF CLOCK (SC-01) — HIGH-PRECISION PROPORTIONAL DIN 1451 / BRAUN 3D STROKE ENGINE
 * Features:
 *   1. Smooth multi-segment spline/arc strokes for curved glyphs (B, C, D, G, J, O, P, Q, R, S, U, 0, 2, 3, 5, 6, 8, 9, ?)
 *   2. 10-sided beveled pillar caps at every stroke vertex (eliminating protruding corner boxes in macro zoom)
 *   3. Proportional DIN 1451 character advance widths (eliminating wide gaps around 'I' in PIPELINE / WAIMEA / HALEIWA / LANIAKEA)
 *   4. Procedural 12-tick upper radial index ring + lower 180° connected L-corner sub-dial arch (zero baked ghost text collision)
 *   5. Pure blank recessed dial faceplate & perimeter AO shadow frame builder
 */

import { DIAL_SLOTS } from "./surf_data.js?v=66";

// Helper to sample circular/elliptical arc segments [[u1,v1],[u2,v2]]
function arcSegs(cx, cy, rx, ry, degStart, degEnd, steps = 8) {
  const out = [];
  const r0 = (degStart * Math.PI) / 180.0;
  const r1 = (degEnd * Math.PI) / 180.0;
  for (let i = 0; i < steps; i++) {
    const t0 = r0 + ((r1 - r0) * i) / steps;
    const t1 = r0 + ((r1 - r0) * (i + 1)) / steps;
    out.push([
      [cx + Math.cos(t0) * rx, cy + Math.sin(t0) * ry],
      [cx + Math.cos(t1) * rx, cy + Math.sin(t1) * ry],
    ]);
  }
  return out;
}

export const CHAR_WIDTH_FACTORS = {
  I: 0.245,
  "0": 0.68,
  "1": 0.44,
  "2": 0.68,
  "3": 0.68,
  "4": 0.68,
  "5": 0.68,
  "6": 0.68,
  "7": 0.68,
  "8": 0.68,
  "9": 0.68,
  "?": 0.68,
  "&": 0.76,
  "+": 0.68,
  "'": 0.18,
  ".": 0.18,
  "-": 0.48,
  "/": 0.68,
  " ": 0.476,
  L: 0.68,
  F: 0.68,
  E: 0.68,
  T: 0.68,
  J: 0.64,
  P: 0.68,
  B: 0.68,
  R: 0.68,
  S: 0.68,
  C: 0.68,
  D: 0.68,
  G: 0.68,
  O: 0.68,
  Q: 0.68,
  U: 0.68,
  H: 0.68,
  N: 0.68,
  A: 0.68,
  V: 0.68,
  X: 0.68,
  Y: 0.68,
  Z: 0.68,
  K: 0.68,
  M: 0.78,
  W: 0.802,
};

export function getCharWidthFactor(ch) {
  return CHAR_WIDTH_FACTORS[ch] ?? 0.68;
}

export const FONT_STROKES = {
  A: [[[0.0, 0.0], [0.5, 1.0]], [[0.5, 1.0], [1.0, 0.0]], [[0.20, 0.30], [0.80, 0.30]]],
  B: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.68, 1.0]],
    [[0.68, 1.0], [0.96, 0.84]],
    [[0.96, 0.84], [0.96, 0.66]],
    [[0.96, 0.66], [0.68, 0.52]],
    [[0.68, 0.52], [0.0, 0.52]],
    [[0.68, 0.52], [1.0, 0.36]],
    [[1.0, 0.36], [1.0, 0.16]],
    [[1.0, 0.16], [0.70, 0.0]],
    [[0.70, 0.0], [0.0, 0.0]],
  ],
  C: [
    [[0.95, 0.82], [0.72, 1.0]],
    [[0.72, 1.0], [0.25, 1.0]],
    [[0.25, 1.0], [0.0, 0.75]],
    [[0.0, 0.75], [0.0, 0.25]],
    [[0.0, 0.25], [0.25, 0.0]],
    [[0.25, 0.0], [0.72, 0.0]],
    [[0.72, 0.0], [0.95, 0.18]],
  ],
  D: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.65, 1.0]],
    [[0.65, 1.0], [1.0, 0.74]],
    [[1.0, 0.74], [1.0, 0.26]],
    [[1.0, 0.26], [0.65, 0.0]],
    [[0.65, 0.0], [0.0, 0.0]],
  ],
  E: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.95, 1.0]],
    [[0.0, 0.50], [0.78, 0.50]],
    [[0.0, 0.0], [0.95, 0.0]],
  ],
  F: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.95, 1.0]],
    [[0.0, 0.48], [0.78, 0.48]],
  ],
  G: [
    [[0.95, 0.82], [0.72, 1.0]],
    [[0.72, 1.0], [0.25, 1.0]],
    [[0.25, 1.0], [0.0, 0.75]],
    [[0.0, 0.75], [0.0, 0.25]],
    [[0.0, 0.25], [0.25, 0.0]],
    [[0.25, 0.0], [0.82, 0.0]],
    [[0.82, 0.0], [1.0, 0.25]],
    [[1.0, 0.25], [1.0, 0.48]],
    [[1.0, 0.48], [0.52, 0.48]],
  ],
  H: [[[0.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [1.0, 1.0]], [[0.0, 0.50], [1.0, 0.50]]],
  I: [[[0.5, 0.0], [0.5, 1.0]]],
  J: [
    [[0.92, 1.0], [0.92, 0.26]],
    [[0.92, 0.26], [0.68, 0.0]],
    [[0.68, 0.0], [0.24, 0.0]],
    [[0.24, 0.0], [0.0, 0.22]],
  ],
  K: [[[0.0, 0.0], [0.0, 1.0]], [[0.98, 1.0], [0.06, 0.46]], [[0.34, 0.62], [1.0, 0.0]]],
  L: [[[0.0, 1.0], [0.0, 0.0]], [[0.0, 0.0], [0.92, 0.0]]],
  M: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.5, 0.22]],
    [[0.5, 0.22], [1.0, 1.0]],
    [[1.0, 1.0], [1.0, 0.0]],
  ],
  N: [[[0.0, 0.0], [0.0, 1.0]], [[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [1.0, 1.0]]],
  O: [
    [[0.25, 1.0], [0.75, 1.0]],
    [[0.75, 1.0], [1.0, 0.75]],
    [[1.0, 0.75], [1.0, 0.25]],
    [[1.0, 0.25], [0.75, 0.0]],
    [[0.75, 0.0], [0.25, 0.0]],
    [[0.25, 0.0], [0.0, 0.25]],
    [[0.0, 0.25], [0.0, 0.75]],
    [[0.0, 0.75], [0.25, 1.0]],
  ],
  P: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.72, 1.0]],
    [[0.72, 1.0], [1.0, 0.80]],
    [[1.0, 0.80], [1.0, 0.62]],
    [[1.0, 0.62], [0.72, 0.46]],
    [[0.72, 0.46], [0.0, 0.46]],
  ],
  Q: [
    [[0.25, 1.0], [0.75, 1.0]],
    [[0.75, 1.0], [1.0, 0.75]],
    [[1.0, 0.75], [1.0, 0.25]],
    [[1.0, 0.25], [0.75, 0.0]],
    [[0.75, 0.0], [0.25, 0.0]],
    [[0.25, 0.0], [0.0, 0.25]],
    [[0.0, 0.25], [0.0, 0.75]],
    [[0.0, 0.75], [0.25, 1.0]],
    [[0.60, 0.30], [1.08, -0.12]],
  ],
  R: [
    [[0.0, 0.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.72, 1.0]],
    [[0.72, 1.0], [1.0, 0.80]],
    [[1.0, 0.80], [1.0, 0.62]],
    [[1.0, 0.62], [0.72, 0.46]],
    [[0.72, 0.46], [0.0, 0.46]],
    [[0.58, 0.46], [1.0, 0.0]],
  ],
  S: [
    [[0.95, 0.85], [0.72, 1.0]],
    [[0.72, 1.0], [0.22, 1.0]],
    [[0.22, 1.0], [0.0, 0.76]],
    [[0.0, 0.76], [0.18, 0.54]],
    [[0.18, 0.54], [0.82, 0.44]],
    [[0.82, 0.44], [1.0, 0.22]],
    [[1.0, 0.22], [0.75, 0.0]],
    [[0.75, 0.0], [0.20, 0.0]],
    [[0.20, 0.0], [0.0, 0.16]],
  ],
  T: [[[0.5, 0.0], [0.5, 1.0]], [[0.0, 1.0], [1.0, 1.0]]],
  U: [
    [[0.0, 1.0], [0.0, 0.26]],
    [[0.0, 0.26], [0.25, 0.0]],
    [[0.25, 0.0], [0.75, 0.0]],
    [[0.75, 0.0], [1.0, 0.26]],
    [[1.0, 0.26], [1.0, 1.0]],
  ],
  V: [[[0.0, 1.0], [0.5, 0.0]], [[0.5, 0.0], [1.0, 1.0]]],
  W: [
    [[0.0, 1.0], [0.22, 0.0]],
    [[0.22, 0.0], [0.50, 0.68]],
    [[0.50, 0.68], [0.78, 0.0]],
    [[0.78, 0.0], [1.0, 1.0]],
  ],
  X: [[[0.0, 1.0], [1.0, 0.0]], [[0.0, 0.0], [1.0, 1.0]]],
  Y: [[[0.0, 1.0], [0.5, 0.48]], [[1.0, 1.0], [0.5, 0.48]], [[0.5, 0.48], [0.5, 0.0]]],
  Z: [[[0.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [0.0, 0.0]], [[0.0, 0.0], [1.0, 0.0]]],
  "0": [
    [[0.25, 1.0], [0.75, 1.0]],
    [[0.75, 1.0], [1.0, 0.75]],
    [[1.0, 0.75], [1.0, 0.25]],
    [[1.0, 0.25], [0.75, 0.0]],
    [[0.75, 0.0], [0.25, 0.0]],
    [[0.25, 0.0], [0.0, 0.25]],
    [[0.0, 0.25], [0.0, 0.75]],
    [[0.0, 0.75], [0.25, 1.0]],
  ],
  "1": [[[0.18, 0.76], [0.56, 1.0]], [[0.56, 1.0], [0.56, 0.0]], [[0.16, 0.0], [0.92, 0.0]]],
  "2": [
    [[0.06, 0.78], [0.28, 1.0]],
    [[0.28, 1.0], [0.76, 1.0]],
    [[0.76, 1.0], [0.96, 0.78]],
    [[0.96, 0.78], [0.96, 0.58]],
    [[0.96, 0.58], [0.04, 0.0]],
    [[0.04, 0.0], [0.98, 0.0]],
  ],
  "3": [
    [[0.08, 0.82], [0.28, 1.0]],
    [[0.28, 1.0], [0.76, 1.0]],
    [[0.76, 1.0], [0.96, 0.78]],
    [[0.96, 0.78], [0.72, 0.52]],
    [[0.72, 0.52], [0.40, 0.52]],
    [[0.72, 0.52], [0.98, 0.26]],
    [[0.98, 0.26], [0.76, 0.0]],
    [[0.76, 0.0], [0.24, 0.0]],
    [[0.24, 0.0], [0.04, 0.18]],
  ],
  "4": [[[0.72, 0.0], [0.72, 1.0]], [[0.72, 1.0], [0.04, 0.32]], [[0.04, 0.32], [0.96, 0.32]]],
  "5": [
    [[0.92, 1.0], [0.08, 1.0]],
    [[0.08, 1.0], [0.06, 0.54]],
    [[0.06, 0.54], [0.74, 0.54]],
    [[0.74, 0.54], [0.98, 0.32]],
    [[0.98, 0.32], [0.76, 0.0]],
    [[0.76, 0.0], [0.22, 0.0]],
    [[0.22, 0.0], [0.04, 0.18]],
  ],
  "6": [
    [[0.92, 0.82], [0.72, 1.0]],
    [[0.72, 1.0], [0.26, 1.0]],
    [[0.26, 1.0], [0.04, 0.74]],
    [[0.04, 0.74], [0.04, 0.24]],
    [[0.04, 0.24], [0.28, 0.0]],
    [[0.28, 0.0], [0.76, 0.0]],
    [[0.76, 0.0], [0.98, 0.24]],
    [[0.98, 0.24], [0.76, 0.50]],
    [[0.76, 0.50], [0.04, 0.50]],
  ],
  "7": [[[0.04, 1.0], [0.96, 1.0]], [[0.96, 1.0], [0.32, 0.0]]],
  "8": [
    ...arcSegs(0.50, 0.76, 0.41, 0.24, 0, 360, 12),
    ...arcSegs(0.50, 0.26, 0.45, 0.26, 0, 360, 12),
  ],
  "9": [
    ...arcSegs(0.48, 0.72, 0.44, 0.28, 0, 360, 12),
    [[0.92, 0.72], [0.92, 0.30]],
    ...arcSegs(0.48, 0.30, 0.44, 0.30, 0, -145, 7),
  ],
  "?": [
    [[0.08, 0.78], [0.28, 1.0]],
    [[0.28, 1.0], [0.76, 1.0]],
    [[0.76, 1.0], [0.98, 0.80]],
    [[0.98, 0.80], [0.98, 0.62]],
    [[0.98, 0.62], [0.50, 0.42]],
    [[0.50, 0.42], [0.50, 0.24]],
    [[0.50, 0.06], [0.50, 0.0]],
  ],
  "-": [[[0.12, 0.50], [0.88, 0.50]]],
  "+": [[[0.12, 0.50], [0.88, 0.50]], [[0.50, 0.16], [0.50, 0.84]]],
  "'": [[[0.50, 1.02], [0.42, 0.72]]],
  ".": [[[0.50, 0.10], [0.50, 0.0]]],
  "/": [[[0.10, 0.0], [0.90, 1.0]]],
  "&": [
    [[0.92, 0.0], [0.14, 0.74]],
    ...arcSegs(0.46, 0.78, 0.32, 0.22, 160, -30, 7),
    [[0.74, 0.66], [0.08, 0.32]],
    ...arcSegs(0.48, 0.24, 0.40, 0.24, 165, 340, 7),
  ],
  " ": [],
};

/**
 * Appends a 10-sided beveled circular joint/terminal pillar at (cx, cy) with radius r = sw * 0.5.
 * Ensures every stroke corner and terminal end is smoothly rounded with zero protruding box corners!
 */
function pushBeveledJointCap(positions, indices, cx, cy, r, zBack = -4.675, zFront = -3.965, flipZ = false) {
  const N = 10;
  const bevelInset = Math.min(0.065, r * 0.28);
  const rTop = Math.max(0.02, r - bevelInset);
  const zMid = flipZ ? zFront + bevelInset : zFront - bevelInset;

  const baseIdx = positions.length / 3;
  for (let i = 0; i < N; i++) {
    const a = (i / N) * Math.PI * 2.0;
    positions.push(cx + Math.cos(a) * r, cy + Math.sin(a) * r, zBack);
  }
  for (let i = 0; i < N; i++) {
    const a = (i / N) * Math.PI * 2.0;
    positions.push(cx + Math.cos(a) * r, cy + Math.sin(a) * r, zMid);
  }
  for (let i = 0; i < N; i++) {
    const a = (i / N) * Math.PI * 2.0;
    positions.push(cx + Math.cos(a) * rTop, cy + Math.sin(a) * rTop, zFront);
  }
  const centerTopIdx = positions.length / 3;
  positions.push(cx, cy, zFront);
  const centerBackIdx = positions.length / 3;
  positions.push(cx, cy, zBack);

  for (let i = 0; i < N; i++) {
    const i1 = (i + 1) % N;
    if (!flipZ) {
      indices.push(baseIdx + i, baseIdx + i1, baseIdx + N + i1);
      indices.push(baseIdx + i, baseIdx + N + i1, baseIdx + N + i);
      indices.push(baseIdx + N + i, baseIdx + N + i1, baseIdx + 2 * N + i1);
      indices.push(baseIdx + N + i, baseIdx + 2 * N + i1, baseIdx + 2 * N + i);
      // Top cap (+Z normal)
      indices.push(centerTopIdx, baseIdx + 2 * N + i, baseIdx + 2 * N + i1);
      // Bottom cap at zBack (-Z normal: 0, 0, -1) for watertight 2-manifold STL
      indices.push(centerBackIdx, baseIdx + i1, baseIdx + i);
    } else {
      indices.push(baseIdx + i, baseIdx + N + i1, baseIdx + i1);
      indices.push(baseIdx + i, baseIdx + N + i, baseIdx + N + i1);
      indices.push(baseIdx + N + i, baseIdx + 2 * N + i1, baseIdx + N + i1);
      indices.push(baseIdx + N + i, baseIdx + 2 * N + i, baseIdx + 2 * N + i1);
      // Front cap (-Z normal when flipped)
      indices.push(centerTopIdx, baseIdx + 2 * N + i1, baseIdx + 2 * N + i);
      // Back cap (+Z normal when flipped)
      indices.push(centerBackIdx, baseIdx + i, baseIdx + i1);
    }
  }
}

/**
 * Appends a single beveled 3D stroke prism segment strictly from (x1, y1) to (x2, y2)
 * with rounded 10-sided beveled end caps at both endpoints and watertight bottom caps at zBack.
 */
export function pushBeveledStrokeSegment(
  positions,
  indices,
  x1,
  y1,
  x2,
  y2,
  sw,
  zBack = -4.675,
  zFront = -3.965,
  withCaps = true,
  flipZ = false
) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const L = Math.hypot(dx, dy);
  const hw = sw * 0.5;
  if (L < 1e-5) {
    if (withCaps) pushBeveledJointCap(positions, indices, x1, y1, hw, zBack, zFront, flipZ);
    return;
  }

  const ux = dx / L;
  const uy = dy / L;
  const nx = -uy * hw;
  const ny = ux * hw;

  const b0 = [x1 - nx, y1 - ny];
  const b1 = [x2 - nx, y2 - ny];
  const b2 = [x2 + nx, y2 + ny];
  const b3 = [x1 + nx, y1 + ny];

  const bevelInset = Math.min(0.065, sw * 0.14);
  const nxIn = -uy * Math.max(0.02, hw - bevelInset);
  const nyIn = ux * Math.max(0.02, hw - bevelInset);

  const t0 = [x1 - nxIn, y1 - nyIn];
  const t1 = [x2 - nxIn, y2 - nyIn];
  const t2 = [x2 + nxIn, y2 + nyIn];
  const t3 = [x1 + nxIn, y1 + nyIn];

  const zMid = flipZ ? zFront + bevelInset : zFront - bevelInset;

  const baseIdx = positions.length / 3;
  for (const [px, py] of [b0, b1, b2, b3]) positions.push(px, py, zBack);
  for (const [px, py] of [b0, b1, b2, b3]) positions.push(px, py, zMid);
  for (const [px, py] of [t0, t1, t2, t3]) positions.push(px, py, zFront);

  for (let k = 0; k < 4; k++) {
    const k1 = (k + 1) % 4;
    if (!flipZ) {
      indices.push(baseIdx + k, baseIdx + k1, baseIdx + 4 + k1);
      indices.push(baseIdx + k, baseIdx + 4 + k1, baseIdx + 4 + k);
      indices.push(baseIdx + 4 + k, baseIdx + 4 + k1, baseIdx + 8 + k1);
      indices.push(baseIdx + 4 + k, baseIdx + 8 + k1, baseIdx + 8 + k);
    } else {
      indices.push(baseIdx + k, baseIdx + 4 + k1, baseIdx + k1);
      indices.push(baseIdx + k, baseIdx + 4 + k, baseIdx + 4 + k1);
      indices.push(baseIdx + 4 + k, baseIdx + 8 + k1, baseIdx + 4 + k1);
      indices.push(baseIdx + 4 + k, baseIdx + 8 + k, baseIdx + 8 + k1);
    }
  }
  if (!flipZ) {
    // Top cap at zFront (+Z normal)
    indices.push(baseIdx + 8, baseIdx + 9, baseIdx + 10);
    indices.push(baseIdx + 8, baseIdx + 10, baseIdx + 11);
    // Bottom cap at zBack (-Z normal: 0, 0, -1) for watertight 2-manifold STL
    indices.push(baseIdx + 0, baseIdx + 2, baseIdx + 1);
    indices.push(baseIdx + 0, baseIdx + 3, baseIdx + 2);
  } else {
    // Front cap when flipped (-Z normal)
    indices.push(baseIdx + 8, baseIdx + 10, baseIdx + 9);
    indices.push(baseIdx + 8, baseIdx + 11, baseIdx + 10);
    // Back cap when flipped (+Z normal)
    indices.push(baseIdx + 0, baseIdx + 1, baseIdx + 2);
    indices.push(baseIdx + 0, baseIdx + 2, baseIdx + 3);
  }

  if (withCaps) {
    pushBeveledJointCap(positions, indices, x1, y1, hw, zBack, zFront, flipZ);
    pushBeveledJointCap(positions, indices, x2, y2, hw, zBack, zFront, flipZ);
  }
}

/**
 * Measures proportional width of a string for a given capH and tracking.
 */
export function measureProportionalString(clean, capH, tracking) {
  let w = 0;
  for (let i = 0; i < clean.length; i++) {
    const cw = capH * getCharWidthFactor(clean[i]);
    w += cw;
    if (i < clean.length - 1) {
      w += capH * tracking;
    }
  }
  return w;
}

/**
 * Appends a centered proportional DIN 1451 3D string at (cx, cy).
 * Supports both front-facing (+Z) and rear-plaque-facing (-Z, xDir = -1, flipZ = true) text!
 */
export function add3DTextToArrays(
  text,
  cx,
  cy,
  capH,
  sw,
  positions,
  indices,
  maxW = 999.0,
  tracking = 0.30,
  zBack = -4.675,
  zFront = -3.965,
  xDir = 1.0
) {
  // Support both (text, cx, cy, ...) and (positions, indices, text, cx, cy, ...) argument orders
  if (Array.isArray(text) && Array.isArray(cx)) {
    return appendString3D(text, cx, cy, capH, sw, positions, indices, maxW, tracking, zBack, zFront, xDir);
  }
  const cleanText = String(text || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();
  return appendString3D(positions, indices, cleanText, cx, cy, capH, sw, maxW, tracking, zBack, zFront, xDir);
}

export function appendString3D(
  positions,
  indices,
  text,
  cx,
  cy,
  capH,
  sw,
  maxW = 999.0,
  tracking = 0.30,
  zBack = -4.675,
  zFront = -3.965,
  xDir = 1.0
) {
  const cleanText = String(text || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();
  const clean = cleanText.trim();
  if (!clean) return;

  let effCapH = capH;
  let effSw = sw;
  let effTracking = tracking;

  let totalW = measureProportionalString(clean, effCapH, effTracking);
  if (totalW > maxW) {
    effTracking = Math.max(0.20, tracking * (maxW / totalW));
    totalW = measureProportionalString(clean, effCapH, effTracking);
    if (totalW > maxW) {
      const scale = maxW / totalW;
      effCapH *= scale;
      effSw = Math.max(0.44, sw * Math.pow(scale, 0.85));
      totalW = measureProportionalString(clean, effCapH, effTracking);
    }
  }

  const flipZ = zFront < zBack;
  let cursor = -totalW * 0.5;
  const baseY = cy;

  for (let i = 0; i < clean.length; i++) {
    const ch = clean[i];
    const cw = effCapH * getCharWidthFactor(ch);
    const segs = FONT_STROKES[ch] || [];

    // Deduplicate vertex caps per character for speed & clean topology
    const cappedKeys = new Set();
    const hw = effSw * 0.5;

    for (const [[u1, v1], [u2, v2]] of segs) {
      const lx1 = cursor + (ch === "I" ? 0.5 : u1) * cw;
      const lx2 = cursor + (ch === "I" ? 0.5 : u2) * cw;
      const px1 = cx + lx1 * xDir;
      const py1 = baseY + v1 * effCapH;
      const px2 = cx + lx2 * xDir;
      const py2 = baseY + v2 * effCapH;

      pushBeveledStrokeSegment(positions, indices, px1, py1, px2, py2, effSw, zBack, zFront, false, flipZ);

      const k1 = `${px1.toFixed(2)},${py1.toFixed(2)}`;
      if (!cappedKeys.has(k1)) {
        cappedKeys.add(k1);
        pushBeveledJointCap(positions, indices, px1, py1, hw, zBack, zFront, flipZ);
      }
      const k2 = `${px2.toFixed(2)},${py2.toFixed(2)}`;
      if (!cappedKeys.has(k2)) {
        cappedKeys.add(k2);
        pushBeveledJointCap(positions, indices, px2, py2, hw, zBack, zFront, flipZ);
      }
    }

    cursor += cw + effCapH * effTracking;
  }
}

/**
 * Builds the complete Three.js BufferGeometry for:
 *   1. The 12 radial upper index ticks around (0, +25.3)
 *   2. The 5 dynamic beach labels around (0, +25.3)
 *   3. The lower 180° semi-circular sub-dial arch, L-corner leader tabs, and 9 radial ticks around (0, -78.2)
 *   4. The lower sub-dial labels (`NAH / YEAH / WORTH IT?` or `1 / 10 / CONDITIONS` or `FLAT / EPIC / SWELL`)
 */
export function buildDialTypographyGeometry(THREE, beachNames5, subdialMode = "worth_it", includeTicksAndArch = true) {
  const positions = [];
  const indices = [];

  const UPPER_Y = 25.3;
  const LOWER_Y = -78.2;

  if (includeTicksAndArch) {
    // 1. Exact Physical Clock 9 Upper Rounded-Pill Sector Ticks around (0, +25.3)
    const majorAngles = [-120, -60, 0, 60, 120];
    const minorAngles = [-90, -30, 30, 90];
    for (const deg of majorAngles) {
      const rad = (deg * Math.PI) / 180.0;
      const r0 = 35.5;
      const r1 = deg === 0 ? 42.6 : 42.0;
      const sw = deg === 0 ? 1.65 : 1.52;
      pushBeveledStrokeSegment(
        positions,
        indices,
        Math.sin(rad) * r0,
        UPPER_Y + Math.cos(rad) * r0,
        Math.sin(rad) * r1,
        UPPER_Y + Math.cos(rad) * r1,
        sw,
        -4.675,
        -3.965,
        true,
        false
      );
    }
    for (const deg of minorAngles) {
      const rad = (deg * Math.PI) / 180.0;
      pushBeveledStrokeSegment(
        positions,
        indices,
        Math.sin(rad) * 37.5,
        UPPER_Y + Math.cos(rad) * 37.5,
        Math.sin(rad) * 41.5,
        UPPER_Y + Math.cos(rad) * 41.5,
        1.22,
        -4.675,
        -3.965,
        true,
        false
      );
    }

    // 3. Exact Physical Clock Lower 180° Semi-Circular Sub-Dial Arch + 5 Inward Graduation Ticks around (0, -78.2)
    const ARCH_R = 31.375;
    const ARCH_STEPS = 72;
    for (let i = 0; i < ARCH_STEPS; i++) {
      const a0 = (-90.0 + (180.0 * i) / ARCH_STEPS) * (Math.PI / 180.0);
      const a1 = (-90.0 + (180.0 * (i + 1)) / ARCH_STEPS) * (Math.PI / 180.0);
      pushBeveledStrokeSegment(
        positions,
        indices,
        Math.sin(a0) * ARCH_R,
        LOWER_Y + Math.cos(a0) * ARCH_R,
        Math.sin(a1) * ARCH_R,
        LOWER_Y + Math.cos(a1) * ARCH_R,
        1.65,
        -4.675,
        -3.965,
        i === 0 || i === ARCH_STEPS - 1,
        false
      );
    }
    // 5 Inward Graduation Ticks at -90° (left foot), -45°, 0° (12 o'clock), +45°, +90° (right foot)
    const lowerTicks = [
      { deg: -90.0, len: 4.5, sw: 1.60 },
      { deg: -45.0, len: 3.6, sw: 1.35 },
      { deg: 0.0,   len: 4.4, sw: 1.55 },
      { deg: 45.0,  len: 3.6, sw: 1.35 },
      { deg: 90.0,  len: 4.5, sw: 1.60 },
    ];
    for (const lt of lowerTicks) {
      const rad = (lt.deg * Math.PI) / 180.0;
      const rOuter = 31.45;
      const rInner = 30.55 - lt.len;
      pushBeveledStrokeSegment(
        positions,
        indices,
        Math.sin(rad) * rOuter,
        LOWER_Y + Math.cos(rad) * rOuter,
        Math.sin(rad) * rInner,
        LOWER_Y + Math.cos(rad) * rInner,
        lt.sw,
        -4.675,
        -3.965,
        true,
        false
      );
    }
  }

  // 2. 5 Upper Beach Labels around Upper Shaft (0, +25.3) — Physical Clock Rounded-Pill Open DIN Typeface
  DIAL_SLOTS.forEach((slot, idx) => {
    const rawName = beachNames5 && beachNames5[idx] ? beachNames5[idx] : "LOCAL REEF";
    const sw = slot.strokeW || (idx === 0 ? 0.72 : 0.70);
    const tr = slot.tracking || (idx === 1 ? 0.31 : 0.42);
    appendString3D(positions, indices, rawName, slot.cx, slot.cy, slot.defaultCapH, sw, slot.maxW, tr);
  });

  // 4. Lower Sub-Dial Mode Labels around Lower Shaft (0, -78.2)
  if (subdialMode === "conditions") {
    appendString3D(positions, indices, "1", -44.5, -78.8, 3.85, 0.68, 24.0, 0.44);
    appendString3D(positions, indices, "10", 45.5, -78.8, 3.85, 0.68, 24.0, 0.44);
    appendString3D(positions, indices, "CONDITIONS", 0.0, -93.0, 3.65, 0.66, 72.0, 0.38);
  } else if (subdialMode === "swell") {
    appendString3D(positions, indices, "FLAT", -45.2, -78.8, 3.75, 0.68, 28.0, 0.42);
    appendString3D(positions, indices, "EPIC", 46.2, -78.8, 3.75, 0.68, 28.0, 0.42);
    appendString3D(positions, indices, "SWELL", 0.0, -93.0, 3.80, 0.68, 64.0, 0.44);
  } else {
    appendString3D(positions, indices, "NAH", -45.2, -78.8, 3.85, 0.68, 28.0, 0.46);
    appendString3D(positions, indices, "YEAH", 46.2, -78.8, 3.85, 0.68, 28.0, 0.46);
    appendString3D(positions, indices, "WORTH IT?", 0.0, -93.0, 3.80, 0.68, 72.0, 0.42);
  }

  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geom.setIndex(indices);
  const nonIndexed = geom.toNonIndexed();
  nonIndexed.computeVertexNormals();
  geom.dispose();
  return nonIndexed;
}

/**
 * Builds dynamic rear data plaque & IC chip markings facing -Z (readable from the rear camera at Z = -525!)
 * Remember: when looking from -Z toward +Z with +Y up, screen-right is -X (`xDir = -1.0`).
 */
export function buildRearPlaqueTypographyGeometry(THREE, regionTitle = "SYDNEY") {
  const positions = [];
  const indices = [];

  const shortRegion = (regionTitle || "SYDNEY").split(",")[0].trim().slice(0, 14).toUpperCase();
  const zBack = -17.15;
  const zFront = -17.92;

  // Left Plaque (from rear camera perspective: +X = +44.0)
  appendString3D(positions, indices, "SURF CLOCK // SC-01", 44.0, 83.2, 2.15, 0.38, 46.0, 0.26, zBack, zFront, -1.0);
  appendString3D(positions, indices, "OPEN SOURCE HARDWARE", 44.0, 78.8, 1.85, 0.34, 46.0, 0.26, zBack, zFront, -1.0);
  appendString3D(positions, indices, "DUAL 28BYJ-48 STEPPER", 44.0, 74.6, 1.75, 0.32, 46.0, 0.26, zBack, zFront, -1.0);

  // Right Plaque (from rear camera perspective: -X = -44.0) — dynamically displays selected region!
  appendString3D(
    positions,
    indices,
    `${shortRegion} TELEMETRY`,
    -44.0,
    83.2,
    2.15,
    0.38,
    46.0,
    0.26,
    zBack,
    zFront,
    -1.0
  );
  appendString3D(positions, indices, "ESP32-S3 // NVS RTC", -44.0, 78.8, 1.85, 0.34, 46.0, 0.26, zBack, zFront, -1.0);
  appendString3D(positions, indices, "BATCH 001 // VERIFIED", -44.0, 74.6, 1.75, 0.32, 46.0, 0.26, zBack, zFront, -1.0);

  // Un-mirrored IC laser markings on ESP32-S3 (+44) and dual ULN2003A (-44)
  appendString3D(positions, indices, "ESP32-S3", 44.0, -5.2, 1.95, 0.32, 22.0, 0.24, -21.4, -22.15, -1.0);
  appendString3D(positions, indices, "WROOM-1", 44.0, -8.4, 1.55, 0.28, 22.0, 0.24, -21.4, -22.15, -1.0);
  appendString3D(positions, indices, "ULN2003A", -44.0, 22.0, 1.65, 0.28, 20.0, 0.24, -21.4, -22.15, -1.0);
  appendString3D(positions, indices, "ULN2003A", -44.0, -52.0, 1.65, 0.28, 20.0, 0.24, -21.4, -22.15, -1.0);

  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geom.setIndex(indices);
  const nonIndexed = geom.toNonIndexed();
  nonIndexed.computeVertexNormals();
  geom.dispose();
  return nonIndexed;
}

/**
 * Builds a 100% pure, blank, surgical recessed dial faceplate (`X ∈ [-78.5, +78.5]`, `Y ∈ [-108.0, +108.0]`, `Z ∈ [-7.00, -4.60]`)
 * with zero pre-baked Sydney beach text, so Macro & Exploded views never show duplicate ghost letters!
 */
/**
 * Appends a rectangular plate section [xMin..xMax, yMin..yMax, zBack..zFront]
 * with a circular cylindrical through-hole at (cx, cy) of radius r.
 * Emits top (+Z), bottom (-Z), inner bore wall, and requested outer perimeter walls.
 */
function appendRectPlateWithHole(
  positions,
  indices,
  xMin,
  xMax,
  yMin,
  yMax,
  zBack,
  zFront,
  cx,
  cy,
  r,
  holeSegs = 32,
  emitTopWall = true,
  emitBottomWall = true
) {
  const angleSet = new Set();
  for (let i = 0; i < holeSegs; i++) {
    angleSet.add((i / holeSegs) * Math.PI * 2.0);
  }
  // Include exact angles to the 4 corners of the rectangle so outer segments lie strictly on straight edges
  const corners = [
    [xMax - cx, yMax - cy],
    [xMin - cx, yMax - cy],
    [xMin - cx, yMin - cy],
    [xMax - cx, yMin - cy],
  ];
  for (const [dx, dy] of corners) {
    let a = Math.atan2(dy, dx);
    if (a < 0) a += Math.PI * 2.0;
    angleSet.add(a);
  }
  const angles = Array.from(angleSet).sort((a, b) => a - b);
  const M = angles.length;

  const rayToRect = (a) => {
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    const tx = ca > 1e-8 ? (xMax - cx) / ca : ca < -1e-8 ? (xMin - cx) / ca : Infinity;
    const ty = sa > 1e-8 ? (yMax - cy) / sa : sa < -1e-8 ? (yMin - cy) / sa : Infinity;
    const t = Math.min(tx, ty);
    return [cx + ca * t, cy + sa * t];
  };

  for (let i = 0; i < M; i++) {
    const a0 = angles[i];
    const a1 = angles[(i + 1) % M];
    const c0x = cx + Math.cos(a0) * r;
    const c0y = cy + Math.sin(a0) * r;
    const c1x = cx + Math.cos(a1) * r;
    const c1y = cy + Math.sin(a1) * r;
    const [p0x, p0y] = rayToRect(a0);
    const [p1x, p1y] = rayToRect(a1);

    const base = positions.length / 3;
    // 0..3: front face (zFront)
    positions.push(c0x, c0y, zFront);
    positions.push(p0x, p0y, zFront);
    positions.push(p1x, p1y, zFront);
    positions.push(c1x, c1y, zFront);
    // 4..7: back face (zBack)
    positions.push(c0x, c0y, zBack);
    positions.push(p0x, p0y, zBack);
    positions.push(p1x, p1y, zBack);
    positions.push(c1x, c1y, zBack);

    // Front face (+Z normal)
    indices.push(base + 0, base + 1, base + 2);
    indices.push(base + 0, base + 2, base + 3);
    // Back face (-Z normal)
    indices.push(base + 4, base + 6, base + 5);
    indices.push(base + 4, base + 7, base + 6);
    // Inner cylindrical hole wall (inward normal toward hole center)
    indices.push(base + 4, base + 0, base + 3);
    indices.push(base + 4, base + 3, base + 7);

    // Outer perimeter wall (skip internal seam edge if shared between upper and lower halves)
    const midY = 0.5 * (p0y + p1y);
    const onTopEdge = Math.abs(p0y - yMax) < 1e-4 && Math.abs(p1y - yMax) < 1e-4;
    const onBottomEdge = Math.abs(p0y - yMin) < 1e-4 && Math.abs(p1y - yMin) < 1e-4;
    if ((onTopEdge && !emitTopWall) || (onBottomEdge && !emitBottomWall)) {
      continue;
    }
    indices.push(base + 5, base + 6, base + 2);
    indices.push(base + 5, base + 2, base + 1);
  }
}

export function buildPureDialFaceplateGeometry(THREE, forSTL = false) {
  if (!forSTL) {
    const geo = new THREE.BoxGeometry(168.4, 214.4, 2.4, 1, 1, 1);
    geo.translate(0.0, 0.0, -5.80); // Front face sits strictly at Z = -4.60, back face at Z = -7.00
    return geo;
  }

  // For 3D Printable STL Export: 167.0 x 212.0 x 2.4 mm plate with dual Ø9.0mm (R=4.5mm)
  // stepper shaft clearance through-holes at (0.0, +25.3 mm) and (0.0, -78.2 mm)!
  const halfW = 167.0 * 0.5;
  const halfH = 212.0 * 0.5;
  const zBack = -7.00;
  const zFront = -4.60;
  const ySplit = -26.45;
  const holeRadius = 4.5;

  const positions = [];
  const indices = [];

  // Upper half containing Upper Stepper shaft hole at (0.0, +25.3)
  appendRectPlateWithHole(
    positions,
    indices,
    -halfW,
    halfW,
    ySplit,
    halfH,
    zBack,
    zFront,
    0.0,
    25.3,
    holeRadius,
    36,
    true,
    false
  );

  // Lower half containing Lower Stepper shaft hole at (0.0, -78.2)
  appendRectPlateWithHole(
    positions,
    indices,
    -halfW,
    halfW,
    -halfH,
    ySplit,
    zBack,
    zFront,
    0.0,
    -78.2,
    holeRadius,
    36,
    false,
    true
  );

  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geom.setIndex(indices);
  const nonIndexed = geom.toNonIndexed();
  nonIndexed.computeVertexNormals();
  geom.dispose();
  return nonIndexed;
}

/**
 * Renders any string into an inline SVG string using the exact proportional FONT_STROKES clock typeface!
 */
export function renderGlyphSVG(text, { height = 14, strokeWidth = 2.0, tracking = 0.30, color = "currentColor" } = {}) {
  const clean = String(text || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();
  const charH = 10;
  const pad = strokeWidth * 1.2;
  const totalTextW = measureProportionalString(clean, charH, tracking);
  const totalW = Math.max(10, totalTextW + pad * 2);
  const totalH = charH + pad * 2;

  const paths = [];
  let cursor = pad;
  for (let i = 0; i < clean.length; i++) {
    const ch = clean[i];
    const cw = charH * getCharWidthFactor(ch);
    const segs = FONT_STROKES[ch] || [];
    for (const [[u1, v1], [u2, v2]] of segs) {
      const uu1 = ch === "I" ? 0.5 : u1;
      const uu2 = ch === "I" ? 0.5 : u2;
      const px1 = (cursor + uu1 * cw).toFixed(2);
      const py1 = (pad + (1.0 - v1) * charH).toFixed(2);
      const px2 = (cursor + uu2 * cw).toFixed(2);
      const py2 = (pad + (1.0 - v2) * charH).toFixed(2);
      paths.push(`M${px1} ${py1}L${px2} ${py2}`);
    }
    cursor += cw + charH * tracking;
  }

  return `<svg class="glyph-svg" viewBox="0 0 ${totalW.toFixed(1)} ${totalH.toFixed(1)}" style="height:${height}px;width:auto;display:inline-block;vertical-align:middle;overflow:visible;" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="${paths.join("")}" stroke="${color}" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

/**
 * Serializes one or more non-indexed or indexed THREE.BufferGeometry instances
 * into an industry-standard Binary .STL ArrayBuffer (ready for PrusaSlicer / Bambu Studio / Cura).
 * Shifts Z by +7.00mm so the back of the 2.40mm dial plate sits flat on the build plate at Z = 0.00mm,
 * the dial face sits at Z = 2.40mm, and the +0.60mm 3D raised typography sits at Z = 2.40..3.00mm!
 */
export function buildBinarySTLFromGeometries(geometries, headerLabel = "SC01_SURF_CLOCK_CUSTOM_DIAL", zShift = 7.0) {
  let totalTriangles = 0;
  const prepared = [];

  const tempNonIdx = [];
  for (const g of geometries) {
    if (!g) continue;
    const nonIdx = g.index ? g.toNonIndexed() : g;
    if (g.index) tempNonIdx.push(nonIdx);
    const pos = nonIdx.getAttribute("position");
    if (pos && pos.count >= 3) {
      totalTriangles += Math.floor(pos.count / 3);
      prepared.push(pos);
    }
  }

  const buffer = new ArrayBuffer(84 + totalTriangles * 50);
  const view = new DataView(buffer);

  // 80-byte ASCII header
  const cleanHeader = (headerLabel || "SC01_OPEN_SOURCE_STL").slice(0, 78);
  for (let i = 0; i < 80; i++) {
    view.setUint8(i, i < cleanHeader.length ? cleanHeader.charCodeAt(i) : 32);
  }
  view.setUint32(80, totalTriangles, true);

  let offset = 84;
  for (const pos of prepared) {
    const triCount = Math.floor(pos.count / 3);
    for (let t = 0; t < triCount; t++) {
      const i0 = t * 3;
      const i1 = i0 + 1;
      const i2 = i0 + 2;

      let az = pos.getZ(i0) + zShift; if (Math.abs(az) < 1e-5) az = 0.0;
      let bz = pos.getZ(i1) + zShift; if (Math.abs(bz) < 1e-5) bz = 0.0;
      let cz = pos.getZ(i2) + zShift; if (Math.abs(cz) < 1e-5) cz = 0.0;
      const ax = pos.getX(i0), ay = pos.getY(i0);
      const bx = pos.getX(i1), by = pos.getY(i1);
      const cx = pos.getX(i2), cy = pos.getY(i2);

      const ux = bx - ax, uy = by - ay, uz = bz - az;
      const vx = cx - ax, vy = cy - ay, vz = cz - az;
      let nx = uy * vz - uz * vy;
      let ny = uz * vx - ux * vz;
      let nz = ux * vy - uy * vx;
      const len = Math.hypot(nx, ny, nz) || 1.0;
      nx /= len; ny /= len; nz /= len;

      view.setFloat32(offset + 0, nx, true);
      view.setFloat32(offset + 4, ny, true);
      view.setFloat32(offset + 8, nz, true);

      view.setFloat32(offset + 12, ax, true);
      view.setFloat32(offset + 16, ay, true);
      view.setFloat32(offset + 20, az, true);

      view.setFloat32(offset + 24, bx, true);
      view.setFloat32(offset + 28, by, true);
      view.setFloat32(offset + 32, bz, true);

      view.setFloat32(offset + 36, cx, true);
      view.setFloat32(offset + 40, cy, true);
      view.setFloat32(offset + 44, cz, true);

      view.setUint16(offset + 48, 0, true);
      offset += 50;
    }
  }

  for (const ni of tempNonIdx) ni.dispose();
  return buffer;
}

/**
 * Generates a Binary .STL ArrayBuffer for the custom dial faceplate + raised typography (includeBasePlate = true, zShift = 7.0)
 * or standalone raised typography inlay (includeBasePlate = false, zShift = 4.675 so bottom sits at Z = 0.000mm).
 */
export function generateCustomDialSTLBuffer(
  includeBasePlate = true,
  regionCode = "CUSTOM",
  THREE = null,
  beachNames5 = ["LONG REEF", "QUEENSIE", "DEE WHY", "FRESHIE", "CURL CURL"],
  subdialMode = "worth_it"
) {
  const ThreeLib = THREE || globalThis.THREE;
  const cleanCode = (regionCode || "CUSTOM").replace(/[^A-Za-z0-9_-]/g, "_").toUpperCase();
  const typoGeo = buildDialTypographyGeometry(ThreeLib, beachNames5, subdialMode, true);
  const geoms = [];
  if (includeBasePlate) {
    geoms.push(buildPureDialFaceplateGeometry(ThreeLib, true));
  }
  geoms.push(typoGeo);

  const zShift = includeBasePlate ? 7.0 : 4.675;
  const stlBuffer = buildBinarySTLFromGeometries(
    geoms,
    `SC01_${cleanCode}_${beachNames5.join("_")}`,
    zShift
  );

  for (const g of geoms) {
    if (g && g.dispose) g.dispose();
  }
  return stlBuffer;
}

