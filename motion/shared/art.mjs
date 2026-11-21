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
  // origen = pies sobre el piso (x, 1290); escala 1 ≈ 300 px de alto sentado
  return `<g id="guy">
    <g id="chair">
      <path d="M-95,-150 L-110,0 M95,-150 L110,0 M-80,-150 L-70,-10 M80,-150 L70,-10" stroke="${C.ink}" stroke-width="16" stroke-linecap="round"/>
      <path d="M-95,-150 L-110,0 M95,-150 L110,0" stroke="${C.chair}" stroke-width="8" stroke-linecap="round"/>
      <rect x="-105" y="-172" width="210" height="34" rx="10" fill="${C.chair}" stroke="${C.ink}" stroke-width="${S}"/>
      <path d="M60,-172 L80,-360 Q20,-390 -40,-365 L-60,-172" fill="${C.chair}" stroke="${C.ink}" stroke-width="${S}"/>
      <path d="M-20,-330 H40 M-25,-290 H50 M-30,-250 H55" stroke="#d7d7d0" stroke-width="10" stroke-linecap="round"/>
    </g>
    <g id="guyBody">
      <rect x="-62" y="-128" width="40" height="112" rx="16" fill="${C.skin}" stroke="${C.ink}" stroke-width="${S}"/>
      <rect x="22" y="-128" width="40" height="112" rx="16" fill="${C.skin}" stroke="${C.ink}" stroke-width="${S}"/>
      <path d="M-80,-186 L80,-186 L78,-112 L8,-112 L0,-140 L-8,-112 L-78,-112 Z" fill="${C.shorts}" stroke="${C.ink}" stroke-width="${S}" stroke-linejoin="round"/>
      <path d="M-82,-2 h66 M16,-2 h66" stroke="${C.ink}" stroke-width="18" stroke-linecap="round"/>
      <path d="M-82,-2 h66 M16,-2 h66" stroke="#2a7fd0" stroke-width="9" stroke-linecap="round"/>
      <path d="M-80,-170 Q-90,-330 0,-340 Q90,-330 80,-170 Z" fill="${C.shirt}" stroke="${C.ink}" stroke-width="${S}" stroke-linejoin="round"/>
      <ellipse cx="0" cy="-185" rx="74" ry="26" fill="#2e8a4b" opacity=".6"/>
      <g id="guyHead" transform="translate(0 -395)">
        ${ell(0, 0, 62, 66, C.skin)}
        <path d="M-60,-14 Q-62,-78 0,-74 Q58,-80 62,-12 Q40,-46 0,-44 Q-34,-48 -60,-14Z" fill="#2b1d14" stroke="${C.ink}" stroke-width="5"/>
        ${ell(-64, 8, 12, 18, C.skin)}${ell(64, 8, 12, 18, C.skin)}
        <g id="guyEyes"><path d="M-34,10 q12,8 24,0 M10,10 q12,8 24,0" stroke="${C.ink}" stroke-width="7" fill="none" stroke-linecap="round"/></g>
        <path d="M-4,18 q8,14 0,22" stroke="${C.skinSh}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M-40,40 Q0,30 40,40 Q36,50 0,46 Q-36,50 -40,40Z" fill="#2b1d14"/>
        <path id="guySmile" d="M-20,52 Q0,64 20,52" stroke="${C.ink}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path id="guyLaugh" opacity="0" d="M-24,50 Q0,82 24,50 Z" fill="#7a1f24" stroke="${C.ink}" stroke-width="5"/>
      </g>
      <g id="guyArms">
        <path d="M-70,-300 Q-110,-200 -40,-210" stroke="${C.ink}" stroke-width="40" fill="none" stroke-linecap="round"/>
        <path d="M-70,-300 Q-110,-200 -40,-210" stroke="${C.shirt}" stroke-width="28" fill="none" stroke-linecap="round"/>
        <path d="M70,-300 Q110,-200 40,-210" stroke="${C.ink}" stroke-width="40" fill="none" stroke-linecap="round"/>
        <path d="M70,-300 Q110,-200 40,-210" stroke="${C.shirt}" stroke-width="28" fill="none" stroke-linecap="round"/>
        <circle id="phoneGlow" cx="0" cy="-240" r="110" fill="url(#phoneGlow)"/>
        <rect x="-30" y="-295" width="60" height="100" rx="10" fill="#1d1d24" stroke="${C.ink}" stroke-width="5"/>
        <rect x="-22" y="-285" width="44" height="78" rx="4" fill="#9fd8ff"/>
        ${ell(-36, -213, 17, 15, C.skin)}${ell(36, -213, 17, 15, C.skin)}
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
