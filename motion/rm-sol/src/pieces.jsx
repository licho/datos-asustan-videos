// Piezas animadas del video del Sol (caricatura plana, contorno negro de 6 px).
import React from "react";
import { interpolate, Easing } from "remotion";
import * as A from "../../shared/art.mjs";

export const K = "#111111";
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };
export const ease = Easing.inOut(Easing.cubic);
export const lerp = (t, a, b, v0, v1, e = ease) => interpolate(t, [a, b], [v0, v1], { ...clamp, easing: e });
export const pop = (t, t0, d = 0.35) => interpolate(t, [t0, t0 + d * 0.6, t0 + d], [0, 1.12, 1], clamp);
export const Raw = ({ html, ...p }) => <g {...p} dangerouslySetInnerHTML={{ __html: html }} />;

// Números pseudoaleatorios deterministas
export const rnd = (i, s = 1) => { const x = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return x - Math.floor(x); };

// ---------- Espacio ----------
export function SpaceBg({ t, tint = 0 }) {
  return (
    <g>
      <defs>
        <linearGradient id="space" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#070a1f" /><stop offset="1" stopColor="#1b2350" />
        </linearGradient>
      </defs>
      <rect x={-400} y={-400} width={1880} height={2720} fill="url(#space)" />
      {[...Array(140)].map((_, i) => {
        const tw = 0.45 + 0.55 * Math.abs(Math.sin(t * (0.8 + rnd(i, 3) * 2) + i));
        return <circle key={i} cx={-300 + rnd(i) * 1680} cy={-300 + rnd(i, 2) * 2500} r={1.5 + rnd(i, 5) * 3.2} fill="#fff" opacity={tw * (1 - tint)} />;
      })}
    </g>
  );
}

// ---------- Tierra con cara ----------
export function Earth({ r = 150, mood = "happy", ice = 0, t = 0, blink = false }) {
  const s = r / 150;
  const eyesOpen = mood === "scared" ? 30 : 22;
  return (
    <g transform={`scale(${s})`}>
      <circle r={150} fill="#3b8fe0" stroke={K} strokeWidth={6 / s} />
      <path d="M-120,-40 Q-90,-110 -30,-100 Q0,-70 -30,-40 Q-60,-10 -100,10 Q-130,0 -120,-40Z M40,-120 Q100,-110 120,-60 Q100,-30 70,-50 Q40,-70 40,-120Z M20,60 Q70,40 110,70 Q90,120 40,125 Q10,100 20,60Z M-110,60 Q-80,50 -70,80 Q-90,110 -115,95Z"
        fill="#4cb860" stroke={K} strokeWidth={4} />
      <path d="M-150,0 A150,150 0 0 0 150,0 A150,135 0 0 1 -150,0Z" fill="#1d5fa8" opacity={0.35} />
      {/* hielo */}
      <g opacity={ice}>
        <circle r={150} fill="#dff3ff" stroke={K} strokeWidth={6} />
        <path d="M-110,-60 L-60,-20 L-80,30 M60,-100 L30,-40 L80,10 M-20,60 L30,110" stroke="#9fd3f0" strokeWidth={6} fill="none" />
        {[...Array(7)].map((_, i) => <path key={i} d={`M${-90 + i * 30},${128 - Math.abs(i - 3) * 14} l8,${28 + (i % 3) * 10} l8,${-28 - (i % 3) * 10}Z`} fill="#bfe8ff" stroke={K} strokeWidth={3} />)}
      </g>
      {/* cara */}
      <g transform="translate(0 -6)">
        <ellipse cx={-48} cy={-18} rx={24} ry={blink ? 3 : eyesOpen} fill="#fff" stroke={K} strokeWidth={5} />
        <ellipse cx={48} cy={-18} rx={24} ry={blink ? 3 : eyesOpen} fill="#fff" stroke={K} strokeWidth={5} />
        {!blink && <><circle cx={mood === "scared" ? -48 : -44} cy={-14} r={mood === "scared" ? 8 : 12} fill={K} /><circle cx={mood === "scared" ? 48 : 52} cy={-14} r={mood === "scared" ? 8 : 12} fill={K} /></>}
        {mood === "happy" && <path d="M-40,32 Q0,72 40,32" stroke={K} strokeWidth={9} fill="none" strokeLinecap="round" />}
        {mood === "scared" && <ellipse cx={0} cy={50} rx={22} ry={28} fill="#5a1a22" stroke={K} strokeWidth={5} />}
        {mood === "cold" && <>
          <rect x={-34} y={36} width={68} height={26} rx={6} fill="#fff" stroke={K} strokeWidth={5} />
          <path d="M-17,36 v26 M0,36 v26 M17,36 v26 M-34,49 h68" stroke={K} strokeWidth={3} />
        </>}
        {mood === "frozen" && <path d="M-36,46 L-18,38 L0,48 L18,38 L36,46" stroke={K} strokeWidth={7} fill="none" strokeLinejoin="round" />}
      </g>
    </g>
  );
}

// ---------- Luna con cara ----------
export function Moon({ r = 110, off = 0, t = 0 }) {
  const s = r / 110;
  const col = off > 0.5 ? "#55536a" : "#d9d9e0";
  return (
    <g transform={`scale(${s})`}>
      <circle r={110} fill="#e6e6ee" stroke={K} strokeWidth={6} />
      <circle r={110} fill="#4b4763" opacity={off} />
      {[[-50, -50, 18], [40, -60, 12], [55, 30, 20], [-30, 55, 10]].map(([x, y, cr], i) =>
        <circle key={i} cx={x} cy={y} r={cr} fill={col} stroke={K} strokeWidth={3} opacity={0.8} />)}
      <ellipse cx={-34} cy={-4} rx={14} ry={off > 0.5 ? 6 : 16} fill="#fff" stroke={K} strokeWidth={4} />
      <ellipse cx={34} cy={-4} rx={14} ry={off > 0.5 ? 6 : 16} fill="#fff" stroke={K} strokeWidth={4} />
      <circle cx={-34} cy={off > 0.5 ? 0 : -2} r={6} fill={K} /><circle cx={34} cy={off > 0.5 ? 0 : -2} r={6} fill={K} />
      {off > 0.5
        ? <><path d="M-18,44 Q0,34 18,44" stroke={K} strokeWidth={6} fill="none" strokeLinecap="round" />
          <ellipse cx={-62} cy={22} rx={16} ry={8} fill="#e0607a" opacity={0.8} /><ellipse cx={62} cy={22} rx={16} ry={8} fill="#e0607a" opacity={0.8} /></>
        : <path d="M-20,34 Q0,52 20,34" stroke={K} strokeWidth={6} fill="none" strokeLinecap="round" />}
    </g>
  );
}

// ---------- Sello ----------
export function Stamp({ text, k, color = "#e1232d", rot = -14, size = 74 }) {
  const w = text.length * size * 0.68 + 60;
  return (
    <g transform={`rotate(${rot}) scale(${1 + (1 - k) * 1.6})`} opacity={Math.min(1, k * 2)}>
      <rect x={-w / 2} y={-size * 0.85} width={w} height={size * 1.7} rx={14} fill="#fff" opacity={0.85} stroke={color} strokeWidth={10} />
      <text textAnchor="middle" dominantBaseline="central" fontFamily="DQA" fontSize={size} fill={color}>{text}</text>
    </g>
  );
}

// ---------- Termómetro (siempre a la izquierda) ----------
const THERMO_STOPS = [[15, 0.82], [0, 0.66], [-18, 0.5], [-73, 0.28], [-240, 0.02]];
export function thermoLevel(v) {
  for (let i = 0; i < THERMO_STOPS.length - 1; i++) {
    const [a, la] = THERMO_STOPS[i], [b, lb] = THERMO_STOPS[i + 1];
    if (v <= a && v >= b) return la + (lb - la) * (a - v) / (a - b);
  }
  return v > 15 ? 0.82 : 0.02;
}
export function Thermo({ value, k = 1, shake = 0 }) {
  const x = 92, top = 560, h = 560, lv = thermoLevel(value);
  const hot = value > 5;
  const fill = hot ? "#e1232d" : value > -30 ? "#3aa0e8" : "#7fd4ff";
  const label = `${value > 0 ? "" : value < 0 ? "−" : ""}${Math.abs(Math.round(value))}°C`;
  return (
    <g transform={`translate(${shake} 0) translate(${x} ${top + h / 2}) scale(${k}) translate(${-x} ${-(top + h / 2)})`} opacity={Math.min(1, k * 2)}>
      <rect x={x - 30} y={top} width={60} height={h} rx={30} fill="#fff" stroke={K} strokeWidth={6} />
      <rect x={x - 14} y={top + 16 + (h - 32) * (1 - lv)} width={28} height={(h - 32) * lv + 20} rx={14} fill={fill} />
      <circle cx={x} cy={top + h + 34} r={52} fill={fill} stroke={K} strokeWidth={6} />
      <circle cx={x - 16} cy={top + h + 18} r={12} fill="#fff" opacity={0.6} />
      {[...Array(9)].map((_, i) => <path key={i} d={`M${x + 8},${top + 40 + i * 58} h20`} stroke={K} strokeWidth={4} />)}
      <g transform={`translate(${x} ${top - 46})`}>
        <rect x={-78} y={-30} width={156} height={60} rx={14} fill={hot ? "#e1232d" : "#1b6fb8"} stroke={K} strokeWidth={5} />
        <text textAnchor="middle" dominantBaseline="central" fontFamily="DQA" fontSize={38} fill="#fff">{label}</text>
      </g>
    </g>
  );
}

// ---------- Escarcha en las orillas y nieve ----------
export function Frost({ k }) {
  if (k <= 0) return null;
  const crystal = (x, y, s, r) => (
    <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
      {[0, 60, 120].map(a => <path key={a} transform={`rotate(${a})`} d="M-60,0 H60 M-40,-14 L-28,0 L-40,14 M40,-14 L28,0 L40,14" stroke="#e8f7ff" strokeWidth={7} fill="none" strokeLinecap="round" />)}
    </g>
  );
  return (
    <g opacity={k}>
      <defs>
        <radialGradient id="frostG" cx=".5" cy=".5" r=".72">
          <stop offset=".6" stopColor="#cfefff" stopOpacity="0" /><stop offset="1" stopColor="#e8f7ff" stopOpacity=".85" />
        </radialGradient>
      </defs>
      <rect x={0} y={0} width={1080} height={1920} fill="url(#frostG)" />
      {crystal(40, 60, 1.2, 10)}{crystal(1030, 120, 1.0, 30)}{crystal(60, 1860, 1.1, 5)}{crystal(1020, 1840, 1.3, 20)}
      {crystal(160, 20, 0.6, 40)}{crystal(930, 30, 0.7, 0)}{crystal(20, 300, 0.7, 15)}{crystal(1060, 330, 0.6, 25)}
    </g>
  );
}
export function Snow({ t, k = 1, n = 70 }) {
  return (
    <g opacity={k}>
      {[...Array(n)].map((_, i) => {
        const sp = 60 + rnd(i, 7) * 90, x0 = rnd(i, 8) * 1180 - 50;
        const y = ((rnd(i, 9) * 2000 + t * sp) % 2000) - 40;
        const x = x0 + Math.sin(t * 1.3 + i) * 18;
        return <circle key={i} cx={x} cy={y} r={4 + rnd(i, 4) * 7} fill="#fff" stroke="#9fc6e0" strokeWidth={1.5} />;
      })}
    </g>
  );
}

// ---------- Personaje envuelto en cobija de tigre ----------
export function BlanketGuy({ t }) {
  const shiver = Math.sin(t * 48) * 3;
  const tiger = "#f39a2b";
  return (
    <g transform={`translate(${shiver} 0)`}>
      <path d="M-150,0 Q-170,-200 -120,-330 Q-60,-420 0,-420 Q60,-420 120,-330 Q170,-200 150,0 Z" fill={tiger} stroke={K} strokeWidth={6} strokeLinejoin="round" />
      {[[-120, -250, 20], [-110, -150, 10], [-130, -60, 25], [100, -280, -20], [115, -170, -10], [120, -70, -25], [-40, -120, 5], [30, -60, -5], [10, -200, 0]].map(([x, y, r], i) =>
        <path key={i} transform={`translate(${x} ${y}) rotate(${r})`} d="M-34,-6 Q0,-22 34,-6 Q0,6 -34,-6Z" fill={K} />)}
      <path d="M-60,-370 Q0,-330 60,-370" stroke={K} strokeWidth={6} fill="none" />
      <Raw html={A.guyHead("cold")} transform="translate(0 -392) scale(.95)" />
      <path d="M-110,-360 Q-60,-300 0,-312 Q60,-300 110,-360 Q120,-310 60,-280 Q0,-262 -60,-280 Q-120,-310 -110,-360Z" fill={tiger} stroke={K} strokeWidth={6} strokeLinejoin="round" />
      <path d="M-70,-300 Q-60,-290 -50,-298 M40,-296 Q52,-286 62,-298" stroke={K} strokeWidth={8} strokeLinecap="round" fill="none" />
      <Raw html={A.hand(-30, -270, 18) + A.hand(30, -270, 18)} />
      {/* vaho */}
      {[0, 1, 2].map(i => {
        const p = ((t * 0.7 + i / 3) % 1);
        return <circle key={i} cx={60 + p * 90} cy={-330 - p * 60} r={14 + p * 26} fill="#fff" opacity={(1 - p) * 0.75} stroke="#b8dcf0" strokeWidth={3} />;
      })}
    </g>
  );
}

// ---------- Plantas y árbol enojado ----------
export function Pot({ wilt, x }) {
  const col = interpolate(wilt, [0, 1], [0, 1]);
  const leaf = wilt > 0.5 ? "#8a6a3a" : "#4cb860";
  return (
    <g transform={`translate(${x} 0)`}>
      <path d={`M0,-120 Q${wilt * 50},-200 ${wilt * 90},${-230 + wilt * 110}`} stroke={K} strokeWidth={14} fill="none" strokeLinecap="round" />
      <path d={`M0,-120 Q${wilt * 50},-200 ${wilt * 90},${-230 + wilt * 110}`} stroke={leaf} strokeWidth={7} fill="none" strokeLinecap="round" />
      <g transform={`translate(${wilt * 90} ${-230 + wilt * 110}) rotate(${wilt * 120})`}>
        <ellipse cx={-26} cy={0} rx={30} ry={14} fill={leaf} stroke={K} strokeWidth={5} />
        <ellipse cx={26} cy={0} rx={30} ry={14} fill={leaf} stroke={K} strokeWidth={5} />
        <circle r={16} fill={wilt > 0.5 ? "#a07a50" : "#ff6f91"} stroke={K} strokeWidth={5} />
      </g>
      <path d="M-62,-130 L62,-130 L48,0 L-48,0 Z" fill="#c0643a" stroke={K} strokeWidth={6} strokeLinejoin="round" />
      <rect x={-70} y={-150} width={140} height={28} rx={8} fill="#d77a4a" stroke={K} strokeWidth={6} />
      {col > 0.6 && <path d="M-30,-80 l8,-8 l8,8 M10,-80 l8,-8 l8,8" stroke={K} strokeWidth={4} fill="none" />}
    </g>
  );
}
export function AngryTree({ t, snow = 1 }) {
  const strain = Math.sin(t * 20) * 2;
  return (
    <g transform={`translate(${strain} 0)`}>
      <path d="M-50,0 L-40,-260 Q0,-280 40,-260 L50,0 Z" fill="#7a5235" stroke={K} strokeWidth={6} strokeLinejoin="round" />
      <path d="M-20,-60 q10,-40 0,-80 M18,-120 q-8,-30 4,-60" stroke="#5b3b24" strokeWidth={6} fill="none" />
      <path d="M-200,-300 Q-230,-470 -90,-520 Q0,-600 100,-520 Q240,-480 200,-300 Q160,-220 0,-230 Q-160,-220 -200,-300Z" fill="#3d9a52" stroke={K} strokeWidth={6} strokeLinejoin="round" />
      <path d="M-180,-420 Q-120,-540 0,-560 Q120,-545 180,-420 Q100,-470 0,-470 Q-100,-470 -180,-420Z" fill="#f2faff" stroke={K} strokeWidth={5} opacity={snow} />
      <path d="M-110,-385 L-40,-350 M110,-385 L40,-350" stroke={K} strokeWidth={14} strokeLinecap="round" />
      <ellipse cx={-62} cy={-330} rx={22} ry={18} fill="#fff" stroke={K} strokeWidth={5} />
      <ellipse cx={62} cy={-330} rx={22} ry={18} fill="#fff" stroke={K} strokeWidth={5} />
      <circle cx={-56} cy={-326} r={9} fill={K} /><circle cx={56} cy={-326} r={9} fill={K} />
      <rect x={-46} y={-292} width={92} height={28} rx={8} fill="#fff" stroke={K} strokeWidth={5} />
      <path d="M-23,-292 v28 M0,-292 v28 M23,-292 v28" stroke={K} strokeWidth={3} />
      <path d="M150,-400 q16,22 0,34 q-16,-12 0,-34z" fill="#8fd3ff" stroke={K} strokeWidth={4} />
    </g>
  );
}

// ---------- Mar congelado en corte ----------
export function OceanCut({ t, iceK = 1 }) {
  return (
    <g>
      <defs>
        <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2b6cb0" /><stop offset="1" stopColor="#0d2350" />
        </linearGradient>
      </defs>
      <rect x={-300} y={820} width={1680} height={1200} fill="url(#water)" stroke={K} strokeWidth={6} />
      {/* rayos de luz tenues bajo el hielo */}
      {[0, 1, 2].map(i => <path key={i} d={`M${200 + i * 300},880 L${120 + i * 300},1300 L${260 + i * 300},1300 Z`} fill="#6fb6ff" opacity={0.08} />)}
      {/* hielo */}
      <g transform={`translate(0 ${(1 - iceK) * -140})`} opacity={iceK}>
        <path d="M-300,700 L1380,700 L1380,850 Q1200,880 1000,858 Q800,890 600,860 Q400,885 200,858 Q0,880 -300,852 Z" fill="#dff3ff" stroke={K} strokeWidth={6} />
        <path d="M120,720 L180,790 L150,840 M560,710 L520,780 L590,830 M880,720 L930,800" stroke="#9fd3f0" strokeWidth={6} fill="none" />
        <path d="M-300,700 Q100,660 400,690 Q700,670 1000,690 Q1200,672 1380,690 L1380,700 L-300,700Z" fill="#fff" stroke={K} strokeWidth={5} />
      </g>
      {/* pez tranquilo */}
      <g transform={`translate(${540 + Math.sin(t * 0.9) * 120} ${1100 + Math.sin(t * 1.7) * 20}) scale(${Math.cos(t * 0.9) > 0 ? 1 : -1} 1)`}>
        <path d="M-90,0 Q-40,-60 40,-40 Q90,-20 100,0 Q90,20 40,40 Q-40,60 -90,0Z" fill="#ff9f43" stroke={K} strokeWidth={6} />
        <path d="M-88,0 L-150,-44 L-136,0 L-150,44 Z" fill="#ff9f43" stroke={K} strokeWidth={6} strokeLinejoin="round" />
        <circle cx={52} cy={-10} r={15} fill="#fff" stroke={K} strokeWidth={4} /><circle cx={56} cy={-8} r={7} fill={K} />
        <path d="M70,18 Q82,24 92,14" stroke={K} strokeWidth={5} fill="none" strokeLinecap="round" />
        <path d="M-20,-36 Q0,-70 30,-40" fill="#ffb36b" stroke={K} strokeWidth={5} />
      </g>
      {[...Array(8)].map((_, i) => {
        const p = (t * 0.35 + rnd(i, 11)) % 1;
        return <circle key={i} cx={200 + rnd(i, 12) * 700 + Math.sin(t * 2 + i) * 10} cy={1280 - p * 400} r={6 + rnd(i, 13) * 10} fill="none" stroke="#bfe8ff" strokeWidth={4} opacity={1 - p} />;
      })}
      <path d="M-300,1290 Q100,1250 400,1280 Q800,1240 1380,1285 L1380,2000 L-300,2000Z" fill="#c2a46e" stroke={K} strokeWidth={6} />
    </g>
  );
}

// ---------- Cueva junto al volcán y casas ----------
export function Cave({ t }) {
  const glow = 0.75 + 0.25 * Math.sin(t * 3);
  return (
    <g>
      <rect x={-300} y={-300} width={1680} height={2600} fill="#4a3426" />
      {[...Array(6)].map((_, i) => <path key={i} d={`M-300,${300 + i * 210} Q200,${260 + i * 210} 540,${300 + i * 210} Q900,${340 + i * 210} 1380,${290 + i * 210}`} stroke="#5d4332" strokeWidth={30} fill="none" />)}
      <path d="M150,1300 Q120,820 540,720 Q960,820 930,1300 Z" fill="#2a1d16" stroke={K} strokeWidth={6} />
      <defs>
        <radialGradient id="lava" cx=".5" cy=".9" r=".7">
          <stop offset="0" stopColor="#ffb347" stopOpacity=".95" /><stop offset=".5" stopColor="#ff6a2a" stopOpacity=".45" /><stop offset="1" stopColor="#ff6a2a" stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse cx={420} cy={1300} rx={420} ry={420} fill="url(#lava)" opacity={glow} />
      <path d="M200,1300 Q300,1240 420,1270 Q540,1230 640,1300 Z" fill="#ff7a1a" stroke={K} strokeWidth={6} />
      <path d="M260,1290 Q320,1262 380,1282 M450,1270 Q520,1250 580,1290" stroke="#ffd23f" strokeWidth={8} fill="none" opacity={glow} />
      {[0, 1, 2, 3].map(i => {
        const p = (t * 0.6 + i / 4) % 1;
        return <circle key={i} cx={300 + i * 70 + Math.sin(t * 3 + i) * 12} cy={1250 - p * 220} r={6 + p * 4} fill="#ffd23f" opacity={1 - p} />;
      })}
    </g>
  );
}
export function WarmGuy({ t }) {
  // sentado en una roca, manos al calor
  const bob = Math.sin(t * 2) * 3;
  return (
    <g>
      <path d="M-130,0 Q-140,-150 -20,-185 Q120,-195 140,-80 Q150,0 130,0 Z" fill="#6b5446" stroke={K} strokeWidth={6} />
      <Raw html={A.legsSitting()} />
      <g transform={`translate(0 ${bob})`}>
        <Raw html={A.guyTorso()} />
        <Raw html={A.guyArm("M-70,-318 Q-120,-280 -170,-250") + A.hand(-176, -248) + A.guyArm("M70,-318 Q30,-270 -100,-262") + A.hand(-106, -262)} />
        <Raw html={A.guyStrings()} />
        <Raw html={A.guyHead("warm")} transform="translate(0 -395)" />
      </g>
    </g>
  );
}
export function House({ lit, t, i }) {
  const fl = lit ? 0.8 + 0.2 * Math.sin(t * 5 + i * 1.7) : 0;
  return (
    <g>
      <rect x={-60} y={-100} width={120} height={100} fill={lit ? "#e7d2b0" : "#9aa7b5"} stroke={K} strokeWidth={5} />
      <path d="M-78,-96 L0,-170 L78,-96 Z" fill={lit ? "#b8433a" : "#6d7a88"} stroke={K} strokeWidth={5} strokeLinejoin="round" />
      <path d="M-70,-104 L0,-168 L70,-104" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" />
      <rect x={-40} y={-74} width={34} height={30} fill={lit ? "#ffd166" : "#3a4552"} stroke={K} strokeWidth={4} opacity={lit ? fl : 1} />
      <rect x={10} y={-50} width={30} height={50} fill={lit ? "#8a5a3a" : "#55606c"} stroke={K} strokeWidth={4} />
      {lit && <path d={`M40,-150 q${8 + Math.sin(t * 2 + i) * 6},-20 0,-40 q${-8},-20 4,-40`} stroke="#ddd" strokeWidth={8} fill="none" opacity={0.7} strokeLinecap="round" />}
      {!lit && [0, 1, 2].map(j => <path key={j} d={`M${-50 + j * 30},-96 l6,22 l6,-22Z`} fill="#bfe8ff" stroke={K} strokeWidth={2} />)}
    </g>
  );
}

// ---------- Plutón presumido ----------
export function Pluto({ t }) {
  return (
    <g>
      <circle r={110} fill="#d8b99a" stroke={K} strokeWidth={6} />
      <path d="M-10,20 Q-60,-20 -40,40 Q-20,90 30,100 Q70,60 60,20 Q40,-10 -10,20Z" fill="#f3e3cf" stroke={K} strokeWidth={4} />
      <rect x={-78} y={-42} width={64} height={34} rx={10} fill={K} /><rect x={14} y={-42} width={64} height={34} rx={10} fill={K} />
      <path d="M-14,-30 h28" stroke={K} strokeWidth={8} />
      <path d="M-30,24 Q0,40 34,16" stroke={K} strokeWidth={7} fill="none" strokeLinecap="round" />
    </g>
  );
}

// ---------- Globo de diálogo ----------
export function Bubble({ x, y, w, text, size = 44, k = 1, tail = "left" }) {
  const lines = text.split("\n"); const h = lines.length * size * 1.2 + 44;
  const tx = tail === "left" ? -w / 2 + 50 : w / 2 - 50;
  return (
    <g transform={`translate(${x} ${y}) scale(${k})`} opacity={Math.min(1, k * 2)}>
      <path d={`M${tx - 20},${h / 2 - 4} L${tx - 40 * (tail === "left" ? 1 : -1)},${h / 2 + 50} L${tx + 24},${h / 2 - 4}Z`} fill="#fff" stroke={K} strokeWidth={6} strokeLinejoin="round" />
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={30} fill="#fff" stroke={K} strokeWidth={6} />
      <rect x={tx - 17} y={h / 2 - 10} width={38} height={14} fill="#fff" />
      {lines.map((l, i) => <text key={i} x={0} y={-h / 2 + 22 + size * 0.95 + i * size * 1.2} textAnchor="middle" fontFamily="DQA" fontSize={size} fill={K}>{l}</text>)}
    </g>
  );
}

// ---------- Celular con chat ----------
export function ChatPhone({ t, k = 1 }) {
  const msg2 = interpolate(t, [0.2, 0.6], [0, 1], clamp);
  return (
    <g transform={`scale(${k})`}>
      <rect x={-230} y={-400} width={460} height={800} rx={50} fill="#1d1d24" stroke={K} strokeWidth={8} />
      <rect x={-200} y={-360} width={400} height={720} rx={22} fill="#eef3f8" />
      <rect x={-200} y={-360} width={400} height={96} rx={22} fill="#2f9e6e" />
      <rect x={-200} y={-290} width={400} height={26} fill="#2f9e6e" />
      <g transform="translate(-140 -312)">
        <circle r={30} fill="#ffd23f" stroke={K} strokeWidth={4} />
        {[...Array(8)].map((_, i) => <path key={i} transform={`rotate(${i * 45})`} d="M0,-36 L0,-46" stroke={K} strokeWidth={5} strokeLinecap="round" />)}
        <circle cx={-9} cy={-4} r={4} fill={K} /><circle cx={9} cy={-4} r={4} fill={K} />
        <path d="M-9,8 Q0,16 9,8" stroke={K} strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
      <text x={-90} y={-322} fontFamily="DQA" fontSize={38} fill="#fff">Sol</text>
      <text x={-90} y={-288} fontFamily="DQA" fontSize={22} fill="#d8ffe8">en línea · siempre</text>
      <g transform={`translate(30 -150) scale(${msg2})`}>
        <rect x={-120} y={-50} width={290} height={100} rx={22} fill="#d6f5c9" stroke={K} strokeWidth={4} />
        <text x={-100} y={12} fontFamily="DQA" fontSize={34} fill={K}>¡Qué calor!</text>
        <path d="M110,26 l10,10 l18,-22 M126,26 l10,10 l18,-22" stroke="#2b8cf0" strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <g transform={`translate(-30 20) scale(${interpolate(t, [0.9, 1.3], [0, 1], clamp)})`}>
        <rect x={-160} y={-50} width={320} height={100} rx={22} fill="#fff" stroke={K} strokeWidth={4} />
        <text x={-140} y={-4} fontFamily="DQA" fontSize={32} fill={K}>Aquí sigo,</text>
        <text x={-140} y={34} fontFamily="DQA" fontSize={32} fill={K}>siempre.</text>
      </g>
    </g>
  );
}
