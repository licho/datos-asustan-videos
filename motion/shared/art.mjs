// Dibujos del canal en SVG (caricatura plana, contorno negro), compartidos por Remotion y HyperFrames.
// Cada función regresa un texto SVG con grupos con id para poder animarlos por separado.
// Coordenadas en el lienzo vertical 1080x1920. Zonas: letreros y=300/420 · acción 480–1320 · piso ~1290 · subtítulos 1500.

export const W = 1080, H = 1920;
export const C = {
  ink: "#111111", white: "#ffffff", yel: "#ffd400", red: "#e1232d",
  skin: "#f1c27d", skinSh: "#d9a560", sun: "#ffd23f", sunSh: "#f4a623", sunOff: "#4b4763", sunOffSh: "#36324a",
  skyTop: "#4f9be0", skyBot: "#ffd9a0", far: "#8fa9c9", near: "#6c7fa3", wall: "#5b4f4a", wallDark: "#4a403b",
  roof: "#b9a493", roofSh: "#9c8878", shirt: "#3aa35b", shorts: "#2f4f8f", chair: "#f4f4f0",
};
const S = 6; // grosor de contorno

const ell = (cx, cy, rx, ry, fill, extra = "") =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" stroke="${C.ink}" stroke-width="${S}" ${extra}/>`;

// ---------- Fondo: cielo + ciudad lejana (dos capas para paralaje) ----------
export function defs() {
  return `<defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${C.skyTop}"/><stop offset="1" stop-color="${C.skyBot}"/>
    </linearGradient>
    <radialGradient id="sunGlow"><stop offset="0" stop-color="#fff3b0" stop-opacity=".95"/>
      <stop offset=".45" stop-color="#ffd23f" stop-opacity=".45"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
    <radialGradient id="phoneGlow"><stop offset="0" stop-color="#bfe6ff" stop-opacity=".8"/>
      <stop offset="1" stop-color="#bfe6ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="photon"><stop offset="0" stop-color="#fffbe0"/><stop offset=".5" stop-color="#ffd23f" stop-opacity=".9"/>
      <stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
    <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
  </defs>`;
}

export function sky() {
  return `<rect id="sky" x="-300" y="-300" width="${W + 600}" height="${H + 600}" fill="url(#sky)"/>`;
}

function buildings(y0, color, seed, minH, maxH, winColor) {
  let x = -260, out = "", k = seed;
  const rnd = () => ((k = (k * 9301 + 49297) % 233280) / 233280); // determinista
  while (x < W + 260) {
    const w = 90 + rnd() * 110, h = minH + rnd() * (maxH - minH);
    out += `<rect x="${x.toFixed(1)}" y="${(y0 - h).toFixed(1)}" width="${w.toFixed(1)}" height="${(h + 400).toFixed(1)}" fill="${color}" stroke="${C.ink}" stroke-width="4"/>`;
    if (winColor) for (let wy = y0 - h + 22; wy < y0 - 18; wy += 38)
      for (let wx = x + 16; wx < x + w - 22; wx += 30)
        if (rnd() > .35) out += `<rect x="${wx.toFixed(1)}" y="${wy.toFixed(1)}" width="12" height="18" fill="${winColor}" opacity=".85"/>`;
    x += w + 6;
  }
  return out;
}
export function skylineFar() { return `<g id="far">${buildings(1300, C.far, 7, 140, 300, null)}</g>`; }
export function skylineNear() { return `<g id="near">${buildings(1300, C.near, 21, 70, 190, "#ffe9a8")}</g>`; }

// ---------- Azotea mexicana: pretil, tinaco, tendedero ----------
export function rooftop() {
  return `<g id="roof">
    <rect x="-300" y="1290" width="${W + 600}" height="900" fill="${C.wall}" stroke="${C.ink}" stroke-width="${S}"/>
    <rect x="-300" y="1290" width="${W + 600}" height="34" fill="${C.roof}" stroke="${C.ink}" stroke-width="${S}"/>
    <rect x="-300" y="1324" width="${W + 600}" height="14" fill="${C.roofSh}"/>
    ${[...Array(9)].map((_, i) => `<rect x="${-200 + i * 170}" y="1420" width="60" height="70" rx="6" fill="${C.wallDark}" opacity=".7"/>`).join("")}
  </g>`;
}
export function tinaco(x = 170, y = 1290) {
  return `<g id="tinaco" transform="translate(${x} ${y})">
    <rect x="-70" y="-60" width="140" height="60" fill="#8c8c8c" stroke="${C.ink}" stroke-width="${S}"/>
    <path d="M-80,-60 L-80,-250 Q0,-290 80,-250 L80,-60 Z" fill="#2b2b2b" stroke="${C.ink}" stroke-width="${S}"/>
    <path d="M-80,-200 Q0,-232 80,-200 M-80,-140 Q0,-172 80,-140" fill="none" stroke="#444" stroke-width="8"/>
    ${ell(0, -268, 40, 14, "#3a3a3a")}
    <path d="M-56,-235 Q-50,-120 -58,-80" stroke="#666" stroke-width="10" fill="none" stroke-linecap="round"/>
  </g>`;
}
export function clothesline() {
  // poste izq (tinaco) a poste der; prendas cuelgan de pinzas y se mecen (grupos cloth1..3)
  const cloth = (id, x, color, shape) => `<g id="${id}" transform="translate(${x} 960)"><g class="sway">${shape(color)}</g></g>`;
  const shirt = c => `<path d="M-50,0 L-80,30 L-62,52 L-45,40 L-45,120 L45,120 L45,40 L62,52 L80,30 L50,0 Q0,22 -50,0Z" fill="${c}" stroke="${C.ink}" stroke-width="5"/>`;
  const sock = c => `<path d="M-18,0 L18,0 L18,76 Q20,98 48,98 Q60,104 56,118 L-6,118 Q-18,112 -18,96 Z" fill="${c}" stroke="${C.ink}" stroke-width="5"/>`;
  const towel = c => `<rect x="-55" y="0" width="110" height="150" fill="${c}" stroke="${C.ink}" stroke-width="5"/><path d="M-55,120 H55" stroke="#fff" stroke-width="8" opacity=".7"/>`;
  return `<g id="line">
    <rect x="296" y="930" width="14" height="362" fill="#7a5c3e" stroke="${C.ink}" stroke-width="4"/>
    <rect x="652" y="930" width="14" height="362" fill="#7a5c3e" stroke="${C.ink}" stroke-width="4"/>
    <path d="M303,960 Q480,1000 659,960" stroke="${C.ink}" stroke-width="4" fill="none"/>
    ${cloth("cloth1", 385, "#e85d75", shirt)}${cloth("cloth2", 488, "#ffcf3a", sock)}${cloth("cloth3", 585, "#5ec2d9", towel)}
  </g>`;
}

// ---------- Sol con cara (encendido y apagado) ----------
export function sun(r = 170) {
  const rays = [...Array(12)].map((_, i) => {
    const a = i * 30;
    return `<path transform="rotate(${a})" d="M-30,${-r - 18} L0,${-r - 92} L30,${-r - 18} Z" fill="${C.sun}" stroke="${C.ink}" stroke-width="${S}" stroke-linejoin="round"/>`;
  }).join("");
  const eyes = (open) => `
    <g id="sunEyes">
      ${ell(-62, -28, 30, 38, C.white)}${ell(62, -28, 30, 38, C.white)}
      <circle cx="-56" cy="-20" r="15" fill="${C.ink}"/><circle cx="68" cy="-20" r="15" fill="${C.ink}"/>
      <circle cx="-51" cy="-27" r="5" fill="#fff"/><circle cx="73" cy="-27" r="5" fill="#fff"/>
    </g>`;
  return `<g id="sun">
    <circle id="sunGlow" r="${r * 2.6}" fill="url(#sunGlow)"/>
    <g id="sunRays">${rays}</g>
    <g id="sunOn">
      <circle r="${r}" fill="${C.sun}" stroke="${C.ink}" stroke-width="${S}"/>
      <path d="M${-r * .72},${r * .35} A${r},${r} 0 0 0 ${r * .72},${r * .35} A${r * 1.05},${r * .95} 0 0 1 ${-r * .72},${r * .35}Z" fill="${C.sunSh}" opacity=".55"/>
      ${ell(-100, 40, 26, 14, "#ff8a5c", 'stroke="none"')}${ell(100, 40, 26, 14, "#ff8a5c", 'stroke="none"')}
      ${eyes(true)}
      <path id="sunSmile" d="M-58,45 Q0,105 58,45" fill="none" stroke="${C.ink}" stroke-width="10" stroke-linecap="round"/>
    </g>
    <g id="sunOff" opacity="0">
      <circle r="${r}" fill="${C.sunOff}" stroke="${C.ink}" stroke-width="${S}"/>
      <path d="M${-r * .72},${r * .35} A${r},${r} 0 0 0 ${r * .72},${r * .35} A${r * 1.05},${r * .95} 0 0 1 ${-r * .72},${r * .35}Z" fill="${C.sunOffSh}" opacity=".7"/>
      ${ell(-62, -28, 36, 44, C.white)}${ell(62, -28, 36, 44, C.white)}
      <circle cx="-62" cy="-28" r="11" fill="${C.ink}"/><circle cx="62" cy="-28" r="11" fill="${C.ink}"/>
      <path d="M-100,-92 L-30,-78 M100,-92 L30,-78" stroke="${C.ink}" stroke-width="10" stroke-linecap="round"/>
      ${ell(0, 70, 26, 34, "#2a2638")}
      <path d="M128,-60 q14,22 0,34 q-14,-12 0,-34z" fill="#8fd3ff" stroke="${C.ink}" stroke-width="4"/>
    </g>
  </g>`;
}

// ---------- Señor en silla de plástico viendo el celular ----------
export function guy() {
  // Señor de azotea: camiseta de tirantes, panza, bigote, chanclas. Origen = pies en el piso; cabeza en y=-395.
  const k = C.ink, sk = C.skin, sh = C.skinSh, hair = "#2b1d14", tank = "#f4f1ea", tankSh = "#d9d3c4", shorts = "#4f6fa3";
  const limb = (d, w = 34) => `<path d="${d}" stroke="${k}" stroke-width="${w + 12}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" stroke="${sk}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
  return `<g id="guy">
    <g id="chair">
      <path d="M-104,-178 L-128,0 M104,-178 L128,0 M-86,-178 L-96,-6 M86,-178 L96,-6" stroke="${k}" stroke-width="18" stroke-linecap="round"/>
      <path d="M-104,-178 L-128,0 M104,-178 L128,0 M-86,-178 L-96,-6 M86,-178 L96,-6" stroke="${C.chair}" stroke-width="8" stroke-linecap="round"/>
      <path d="M-100,-178 L-114,-372 Q0,-404 114,-372 L100,-178 Z" fill="${C.chair}" stroke="${k}" stroke-width="${S}" stroke-linejoin="round"/>
      <path d="M-70,-356 L-64,-300 M-35,-364 L-32,-300 M0,-366 L0,-300 M35,-364 L32,-300 M70,-356 L64,-300" stroke="#d9d9d2" stroke-width="10" stroke-linecap="round"/>
      <rect x="-150" y="-282" width="58" height="22" rx="10" fill="${C.chair}" stroke="${k}" stroke-width="5"/>
      <rect x="92" y="-282" width="58" height="22" rx="10" fill="${C.chair}" stroke="${k}" stroke-width="5"/>
      <path d="M-128,-262 L-118,-190 M128,-262 L118,-190" stroke="${k}" stroke-width="16" stroke-linecap="round"/>
      <path d="M-128,-262 L-118,-190 M128,-262 L118,-190" stroke="${C.chair}" stroke-width="7" stroke-linecap="round"/>
      <rect x="-122" y="-196" width="244" height="30" rx="12" fill="${C.chair}" stroke="${k}" stroke-width="${S}"/>
    </g>
    <g id="guyBody">
      <!-- piernas y chanclas -->
      <rect x="-82" y="-130" width="46" height="118" rx="20" fill="${sk}" stroke="${k}" stroke-width="${S}"/>
      <rect x="36" y="-130" width="46" height="118" rx="20" fill="${sk}" stroke="${k}" stroke-width="${S}"/>
      <path d="M-50,-120 v92 M68,-120 v92" stroke="${sh}" stroke-width="8" stroke-linecap="round" opacity=".7"/>
      ${ell(-62, -4, 40, 11, "#2a7fd0")}${ell(62, -4, 40, 11, "#2a7fd0")}
      <path d="M-82,-8 Q-62,-30 -42,-8 M42,-8 Q62,-30 82,-8" stroke="${k}" stroke-width="12" fill="none" stroke-linecap="round"/>
      <path d="M-82,-8 Q-62,-30 -42,-8 M42,-8 Q62,-30 82,-8" stroke="#2a7fd0" stroke-width="6" fill="none" stroke-linecap="round"/>
      <!-- short -->
      <path d="M-98,-190 L98,-190 L104,-118 L16,-114 L0,-140 L-16,-114 L-104,-118 Z" fill="${shorts}" stroke="${k}" stroke-width="${S}" stroke-linejoin="round"/>
      <path d="M-60,-150 l10,30 M60,-150 l-10,30" stroke="#3d5888" stroke-width="7" stroke-linecap="round"/>
      <!-- cuello y camiseta de tirantes con panza -->
      <rect x="-28" y="-352" width="56" height="40" fill="${sk}" stroke="${k}" stroke-width="${S}"/>
      <path d="M-84,-334 Q-100,-300 -104,-262 Q-122,-208 -96,-180 L96,-180 Q122,-208 104,-262 Q100,-300 84,-334 Q44,-322 0,-318 Q-44,-322 -84,-334 Z"
        fill="${tank}" stroke="${k}" stroke-width="${S}" stroke-linejoin="round"/>
      <path d="M-84,-334 Q-62,-292 -40,-330 Q0,-262 40,-330 Q62,-292 84,-334" fill="${sk}" stroke="${k}" stroke-width="5" stroke-linejoin="round"/>
      <path d="M-98,-238 Q0,-170 98,-238 L96,-182 L-96,-182 Z" fill="${tankSh}" opacity=".8"/>
      <path d="M-8,-214 q8,6 16,0" stroke="${k}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <g id="guyHead" transform="translate(0 -395)">
        <!-- cabeza: papada, orejas, entradas -->
        ${ell(-66, 6, 13, 19, sk)}${ell(66, 6, 13, 19, sk)}
        <path d="M-66,0 Q-70,-74 0,-76 Q70,-74 66,0 Q68,58 34,70 Q0,84 -34,70 Q-68,58 -66,0 Z" fill="${sk}" stroke="${k}" stroke-width="${S}"/>
        <path d="M-34,66 Q0,80 34,66" stroke="${sh}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M-68,-4 Q-74,-44 -48,-60 Q-58,-34 -56,-10 Z M68,-4 Q74,-44 48,-60 Q58,-34 56,-10 Z" fill="${hair}" stroke="${k}" stroke-width="4" stroke-linejoin="round"/>
        <path d="M-34,-70 Q-6,-86 30,-68 M-26,-62 Q0,-74 22,-60" stroke="${hair}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse cx="-30" cy="-52" rx="12" ry="6" fill="#fff" opacity=".35"/>
        <!-- cejas, ojos viendo el celular (abajo a la izquierda), párpados caídos -->
        <path d="M-46,-26 Q-28,-38 -8,-28 M8,-28 Q28,-38 46,-26" stroke="${hair}" stroke-width="11" fill="none" stroke-linecap="round"/>
        <g id="guyEyes">
          ${ell(-26, -4, 15, 13, C.white)}${ell(26, -4, 15, 13, C.white)}
          <circle cx="-31" cy="2" r="7" fill="${k}"/><circle cx="21" cy="2" r="7" fill="${k}"/>
          <path d="M-42,-6 Q-26,-20 -10,-6 Z M10,-6 Q26,-20 42,-6 Z" fill="${sk}" stroke="${k}" stroke-width="4" stroke-linejoin="round"/>
        </g>
        <!-- nariz y bigote -->
        <path d="M-4,4 Q-20,22 -4,30 Q8,34 16,26 Q22,14 6,4" fill="${sh}" stroke="${k}" stroke-width="5" stroke-linejoin="round"/>
        <path d="M-44,46 Q-40,28 -16,30 Q0,34 16,30 Q40,28 44,46 Q30,40 16,44 Q0,48 -16,44 Q-30,40 -44,46 Z" fill="${hair}" stroke="${k}" stroke-width="4" stroke-linejoin="round"/>
        <path id="guySmile" d="M-14,54 Q0,62 14,54" stroke="${k}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <g id="guyLaugh" opacity="0">
          <path d="M-22,48 Q0,86 22,48 Z" fill="#7a1f24" stroke="${k}" stroke-width="5" stroke-linejoin="round"/>
          <path d="M-10,66 Q0,60 10,66 Q4,76 -4,74 Z" fill="#e2626b"/>
        </g>
        ${ell(-46, 26, 12, 7, "#ef9a7a", 'stroke="none" opacity=".7"')}${ell(46, 26, 12, 7, "#ef9a7a", 'stroke="none" opacity=".7"')}
      </g>
      <g id="guyArms">
        <circle id="phoneGlow" cx="-38" cy="-300" r="78" fill="url(#phoneGlow)"/>
        <!-- brazo derecho rascándose la panza -->
        ${limb("M84,-316 Q128,-268 118,-232 Q96,-214 64,-214")}
        ${ell(60, -214, 21, 17, sk)}
        <path d="M46,-222 h-10 M46,-212 h-12 M48,-202 h-10" stroke="${k}" stroke-width="4" stroke-linecap="round"/>
        <!-- brazo izquierdo con el celular -->
        ${limb("M-84,-316 Q-128,-262 -112,-238 Q-82,-222 -44,-262")}
        <g transform="rotate(-12 -38 -300)">
          <rect x="-64" y="-346" width="52" height="88" rx="10" fill="#1d1d24" stroke="${k}" stroke-width="5"/>
          <rect x="-57" y="-337" width="38" height="68" rx="4" fill="#9fd8ff"/>
          <rect x="-50" y="-328" width="24" height="7" rx="3" fill="#fff" opacity=".8"/>
          <rect x="-50" y="-314" width="18" height="7" rx="3" fill="#fff" opacity=".6"/>
        </g>
        ${ell(-44, -262, 20, 17, sk)}
        ${ell(-24, -292, 9, 13, sk, 'transform="rotate(-20 -24 -292)"')}
      </g>
    </g>
  </g>`;
}

// ---------- Luz que sigue viajando (puntos) ----------
export function photons(n = 7) {
  return `<g id="photons">${[...Array(n)].map((_, i) => `<circle class="ph" id="ph${i}" r="26" fill="url(#photon)" opacity="0"/>`).join("")}</g>`;
}

export function vignette() {
  return `<rect x="0" y="0" width="${W}" height="${H}" fill="url(#vig)" pointer-events="none"/>`;
}

// Recorrido de la luz: del sol (540,720) a la cara del señor; regresa x,y para un avance 0..1
export const BEAM = { x0: 540, y0: 700, x1: 800, y1: 880 };
export const beamAt = p => ({ x: BEAM.x0 + (BEAM.x1 - BEAM.x0) * p, y: BEAM.y0 + (BEAM.y1 - BEAM.y0) * p - Math.sin(p * Math.PI) * 60 });

// ---------- Guion del gancho (palabras con tiempo estimado; se reemplaza por la voz real) ----------
export const HOOK = {
  dur: 5.0,
  chip1: "¿Y SI EL SOL SE APAGA?",
  words: [
    ["Si", .15], ["el", .30], ["Sol", .45], ["se", .70, 1], ["apaga", .85, 1], ["ahorita…", 1.15],
    ["tardarías", 1.95], ["ocho", 2.50, 1], ["minutos", 2.80, 1], ["en", 3.20], ["enterarte.", 3.35],
  ],
  clic: 1.35,
};
