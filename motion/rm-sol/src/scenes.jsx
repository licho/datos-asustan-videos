// Escenas del video "¿Qué pasaría si el Sol se apagara?". Cada escena recibe t (segundos dentro de la línea) y dur.
import React, { useMemo } from "react";
import { interpolate, Easing } from "remotion";
import * as A from "../../shared/art.mjs";
import { K, clamp, ease, lerp, pop, Raw, rnd, SpaceBg, Earth, Moon, Stamp, Frost, Snow, BlanketGuy, Pot, AngryTree,
  OceanCut, Cave, WarmGuy, House, Pluto, Bubble, ChatPhone } from "./pieces.jsx";
import { Chip } from "./ui.jsx";
import { Gancho } from "./Gancho.jsx";

const STATIC = {
  defs: A.defs(), sky: A.sky(), far: A.skylineFar(), near: A.skylineNear(), roof: A.rooftop(), tinaco: A.tinaco(),
  line: A.clothesline(), vig: A.vignette(),
};
const cam = (s, fx = 540, fy = 960, dx = 0, dy = 0) => `translate(${540 + dx} ${960 + dy}) scale(${s}) translate(${-fx} ${-fy})`;
const Frame = ({ children, overlay }) => (
  <>
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute" }}>
      <Raw html={STATIC.defs} />
      {children}
      <Raw html={STATIC.vig} />
    </svg>
    {overlay}
  </>
);
const SunSvg = ({ on = 1, t = 0 }) => {
  const html = useMemo(() => A.sun(165), []);
  const h = html
    .replace('id="sunOn"', `id="sunOn" opacity="${on}"`)
    .replace('id="sunOff" opacity="0"', `id="sunOff" opacity="${1 - on}"`)
    .replace('id="sunRays"', `id="sunRays" opacity="${on}" transform="rotate(${t * 14})"`)
    .replace('id="sunGlow"', `id="sunGlow" opacity="${on}"`);
  return <Raw html={h} />;
};
// Azotea (de día o de noche)
function Rooftop({ t, night = 0, children, camT = "" }) {
  return (
    <g transform={camT}>
      <Raw html={STATIC.sky} />
      <rect x={-300} y={-300} width={1680} height={2520} fill="#0a0f2e" opacity={night * 0.82} />
      {night > 0 && [...Array(60)].map((_, i) => <circle key={i} cx={rnd(i) * 1080} cy={rnd(i, 2) * 1000} r={2 + rnd(i, 3) * 2.5} fill="#fff" opacity={night * (0.5 + 0.5 * Math.sin(t * 2 + i))} />)}
      <Raw html={STATIC.far} transform={`translate(${-8 * t} 0)`} />
      <Raw html={STATIC.near} transform={`translate(${-16 * t} 0)`} />
      <rect x={-300} y={900} width={1680} height={400} fill="#0a0f2e" opacity={night * 0.55} />
      <Raw html={STATIC.roof} />
      <rect x={-300} y={1290} width={1680} height={700} fill="#0a0f2e" opacity={night * 0.35} />
      {children}
    </g>
  );
}

// ---------- 0. Gancho ----------
export const S0 = () => <Gancho bare />;

// ---------- 1. Hice la cuenta ----------
export function S1({ t, dur }) {
  const z = lerp(t, 0, dur, 1.08, 1.0);
  const orbitA = -0.6 + t * 0.12;
  const ex = 540 + Math.cos(orbitA) * 330, ey = 980 + Math.sin(orbitA) * 160;
  return (
    <Frame overlay={<><Chip text="HICE LA CUENTA" y={300} k={pop(t, 0)} />
      <Chip text="00:00" y={420} bg="#111" fg="#ffd400" size={52} k={pop(t, 0.4)} /></>}>
      <g transform={cam(z)}>
        <SpaceBg t={t} />
        <ellipse cx={540} cy={980} rx={330} ry={160} fill="none" stroke="#6c7bb8" strokeWidth={5} strokeDasharray="18 16" />
        <g transform="translate(540 980) scale(.62)"><SunSvg t={t} /></g>
        <g filter="url(#dropS)" transform={`translate(${ex} ${ey})`}><Earth r={88} mood="happy" t={t} blink={t % 2.2 < 0.12} /></g>
      </g>
    </Frame>
  );
}

// ---------- 2. La luz sigue llegando (tren de luz) ----------
export function S2({ t, dur }) {
  const secs = Math.min(500, Math.floor(lerp(t, 0.2, dur - 0.3, 0, 500, Easing.linear)));
  const clock = `${String(Math.floor(secs / 60)).padStart(2, "0")}:${String(secs % 60).padStart(2, "0")}`;
  const sx = 230, sy = 780, exx = 850, eyy = 1130;
  const ang = Math.atan2(eyy - sy, exx - sx) * 180 / Math.PI;
  const len = Math.hypot(exx - sx, eyy - sy) - 120;
  const prog = lerp(t, 0, dur, 0, 1, Easing.linear);
  const n = 6;
  return (
    <Frame overlay={<><Chip text="8 MIN 20 S" y={300} k={pop(t, 0)} />
      <Chip text={clock} y={420} bg="#111" fg="#ffd400" size={52} k={1} /></>}>
      <SpaceBg t={t} />
      <g transform={`translate(${sx} ${sy}) scale(.55)`}><SunSvg on={0} t={t} /></g>
      <g filter="url(#dropS)" transform={`translate(${exx} ${eyy})`}><Earth r={100} mood="happy" t={t} blink={t % 2.4 < 0.12} /></g>
      {/* vías */}
      <g transform={`translate(${sx} ${sy}) rotate(${ang})`}>
        <path d={`M110,0 H${len + 90}`} stroke="#4a5590" strokeWidth={6} strokeDasharray="14 14" />
        {[...Array(n)].map((_, i) => {
          const p = prog * 1.35 - i * 0.14; // el último vagón llega al final
          if (p < 0 || p > 1.02) return null;
          const x = 120 + p * len;
          const last = i === n - 1;
          return (
            <g key={i} transform={`translate(${x} 0)`}>
              <rect x={-55} y={-34} width={110} height={68} rx={16} fill={last ? "#ffb703" : "#ffe066"} stroke={K} strokeWidth={5} />
              <circle cx={-28} cy={36} r={12} fill="#333" stroke={K} strokeWidth={4} /><circle cx={28} cy={36} r={12} fill="#333" stroke={K} strokeWidth={4} />
              <circle r={70} fill="url(#photon)" opacity={0.5} />
              {last && <text y={10} textAnchor="middle" fontFamily="DQA" fontSize={24} fill={K} transform="rotate(0)">ÚLTIMO</text>}
            </g>
          );
        })}
      </g>
    </Frame>
  );
}

// ---------- 3. Apagón total: la Tierra sale disparada ----------
export function S3({ t, dur }) {
  const dark = lerp(t, 0, 0.5, 0, 1);
  const go = lerp(t, 1.4, dur, 0, 1, Easing.in(Easing.quad));
  const ex = 760 + go * 900, ey = 900 - go * 520;
  const fx = 540 + (ex - 760) * 0.85, fy = 960 + (ey - 900) * 0.85;
  return (
    <Frame overlay={<Chip text="APAGÓN TOTAL" y={300} k={pop(t, 0)} />}>
      <g transform={cam(1, fx, fy)}>
        <SpaceBg t={t} />
        <circle cx={540} cy={900} r={230} fill="none" stroke="#6c7bb8" strokeWidth={5} strokeDasharray="18 16" opacity={1 - go} />
        <g transform="translate(540 900) scale(.5)"><SunSvg on={0} t={t} /></g>
        <path d={`M760,900 L${760 + 1200},${900 - 693}`} stroke="#ffd400" strokeWidth={6} strokeDasharray="20 18" opacity={lerp(t, 0.8, 1.3, 0, 0.8)} />
        {go > 0.02 && [0, 1, 2, 3].map(i => <path key={i} d={`M${ex - 180 - i * 30},${ey + 40 + i * 30} l-${120 + i * 40},${70 + i * 22}`} stroke="#fff" strokeWidth={8} strokeLinecap="round" opacity={0.6} />)}
        <g filter="url(#dropS)" transform={`translate(${ex} ${ey}) rotate(${go * 300})`}><Earth r={95} t={t} mood={go > 0.01 ? "scared" : "happy"} /></g>
      </g>
      <rect x={0} y={0} width={1080} height={1920} fill="#000" opacity={0.35 * dark} />
    </Frame>
  );
}

// ---------- 4. La Luna se apaga ----------
export function S4({ t, dur }) {
  const off = lerp(t, 0.5, 1.0, 0, 1);
  return (
    <Frame overlay={<Chip text="LA LUNA TAMBIÉN" y={300} k={pop(t, 0)} />}>
      <SpaceBg t={t} />
      <g transform="translate(820 600) scale(.4)"><Earth r={95} mood="scared" /></g>
      <g filter="url(#dropS)" transform={`translate(520 ${900 + Math.sin(t * 2) * 10})`}><Moon r={230} off={off} /></g>
      <g transform="translate(540 1230)"><Stamp text="PRESTADO" k={lerp(t, dur * 0.55, dur * 0.55 + 0.25, 0, 1, Easing.out(Easing.back(2)))} /></g>
    </Frame>
  );
}

// ---------- 5. Día tres ----------
export function S5({ t, dur }) {
  const ice = lerp(t, 0.2, dur, 0, 0.8);
  return (
    <Frame overlay={<><Chip text="DÍA 3" y={300} k={pop(t, 0)} />
      <Chip text="−20 °C POR DÍA" y={420} bg="#1b6fb8" size={46} k={pop(t, dur * 0.5)} /></>}>
      <g transform={cam(lerp(t, 0, dur, 1, 1.12))}>
        <SpaceBg t={t} />
        <g filter="url(#dropS)" transform="translate(560 920)"><Earth r={280} t={t} mood={ice > 0.3 ? "cold" : "scared"} ice={ice} /></g>
      </g>
      <Frost k={lerp(t, 0.3, dur, 0, 0.75)} />
    </Frame>
  );
}

// ---------- 6. Semana uno: cobija de tigre ----------
export function S6({ t, dur }) {
  return (
    <Frame overlay={<Chip text="SEMANA 1" y={300} k={pop(t, 0)} />}>
      <Rooftop t={t} night={1} camT={cam(lerp(t, 0, dur, 1.0, 1.1), 560, 1000)}>
        <Raw html={STATIC.tinaco} />
        <rect x={-300} y={1278} width={1680} height={20} fill="#f2faff" stroke={K} strokeWidth={4} />
        <ellipse cx={580} cy={1292} rx={170} ry={20} fill="#000" opacity={0.3} /><g filter="url(#dropS)" transform="translate(580 1290)"><BlanketGuy t={t} /></g>
      </Rooftop>
      <Snow t={t} />
      <Frost k={0.7} />
    </Frame>
  );
}

// ---------- 7. Plantas y árboles ----------
export function S7({ t, dur }) {
  const half = dur * 0.45;
  const wilt = lerp(t, 0.2, half, 0, 1);
  const treeK = lerp(t, half, half + 0.45, 0, 1, Easing.out(Easing.back(1.6)));
  return (
    <Frame overlay={<Chip text={t < half ? "SEMANAS" : "DÉCADAS"} y={300} k={1} />}>
      <Rooftop t={t} night={0.9}>
        <rect x={-300} y={1278} width={1680} height={20} fill="#f2faff" stroke={K} strokeWidth={4} />
        <g transform={`translate(0 1290)`}><Pot x={290} wilt={wilt} /><Pot x={450} wilt={Math.max(0, wilt - 0.15) / 0.85} /></g>
        <g filter="url(#dropS)" transform={`translate(790 1290) scale(${0.9 * treeK})`}><AngryTree t={t} /></g>
      </Rooftop>
      <Snow t={t} n={45} />
      <Frost k={0.6} />
    </Frame>
  );
}

// ---------- 8. Año uno: mar congelado ----------
export function S8({ t, dur }) {
  return (
    <Frame overlay={<><Chip text="AÑO 1" y={300} k={pop(t, 0)} />
      <Chip text="AGUA LÍQUIDA ABAJO" y={420} bg="#1b6fb8" size={46} k={pop(t, dur * 0.45)} /></>}>
      <g transform={cam(lerp(t, 0, dur, 1.05, 1.0))}>
        <rect x={-300} y={-300} width={1680} height={1100} fill="#1a2040" />
        {[...Array(50)].map((_, i) => <circle key={i} cx={rnd(i) * 1080} cy={rnd(i, 2) * 650} r={2 + rnd(i, 3) * 2} fill="#fff" opacity={0.7} />)}
        <OceanCut t={t} iceK={lerp(t, 0, 0.7, 0.2, 1)} />
      </g>
      <Snow t={t} n={30} k={0.8} />
      <Frost k={0.75} />
    </Frame>
  );
}

// ---------- 9. Humanos: cueva y casas ----------
export function S9({ t, dur }) {
  const cut = dur * 0.42;
  const pan = lerp(t, cut - 0.25, cut + 0.35, 0, 1);
  return (
    <Frame overlay={t < cut ? <Chip text="BAJO TIERRA" y={300} k={pop(t, 0)} /> :
      <><Chip text="ISLANDIA" y={300} k={pop(t, cut)} /><Chip text="9 DE CADA 10 CASAS" y={420} bg="#111" fg="#ffd400" size={48} k={pop(t, cut + 0.5)} /></>}>
      <g transform={`translate(0 ${-pan * 1920})`}>
        <g><Cave t={t} /><g filter="url(#dropS)" transform="translate(700 1290)"><WarmGuy t={t} /></g></g>
        <g transform="translate(0 1920)">
          <rect x={0} y={0} width={1080} height={1920} fill="#141b3d" />
          {[...Array(50)].map((_, i) => <circle key={i} cx={rnd(i) * 1080} cy={rnd(i, 2) * 700} r={2 + rnd(i, 3) * 2} fill="#fff" opacity={0.6} />)}
          <path d="M-100,820 L200,520 L380,700 L600,480 L900,760 L1180,560 L1180,1300 L-100,1300Z" fill="#3c4a6e" stroke={K} strokeWidth={6} />
          <path d="M150,570 L200,520 L250,570 M550,530 L600,480 L650,530" stroke="#fff" strokeWidth={14} fill="none" strokeLinecap="round" />
          <rect x={-100} y={1290} width={1280} height={700} fill="#eef6ff" stroke={K} strokeWidth={6} />
          {[...Array(10)].map((_, i) => {
            const col = i % 5, row = Math.floor(i / 5);
            const k = lerp(t, cut + 0.2 + i * 0.08, cut + 0.5 + i * 0.08, 0, 1, Easing.out(Easing.back(2)));
            return <g key={i} transform={`translate(${215 + col * 178} ${1000 + row * 260}) scale(${k})`}><House lit={i !== 7} t={t} i={i} /></g>;
          })}
        </g>
      </g>
    </Frame>
  );
}

// ---------- 10. Al final: más frío que Plutón ----------
export function S10({ t, dur }) {
  return (
    <Frame overlay={<Chip text="AL FINAL" y={300} k={pop(t, 0)} />}>
      <SpaceBg t={t} />
      <g transform={`translate(${360 + Math.sin(t * 40) * (t < 0.6 ? 3 : 0)} 960)`}><g filter="url(#dropS)"><Earth r={200} mood="frozen" ice={1} t={t} /></g></g>
      <g transform={`translate(840 ${760 + Math.sin(t * 2) * 12}) scale(${pop(t, dur * 0.4) * 1.15})`} filter="url(#dropS)"><Pluto t={t} /></g>
      <Bubble x={720} y={520} w={420} text={"¿Y ahora quién\nes el frío?"} size={40} k={pop(t, dur * 0.5)} tail="right" />
      <Frost k={0.9} />
    </Frame>
  );
}

// ---------- 11. El Sol nunca te deja en visto ----------
export function S11({ t, dur }) {
  const zoom = lerp(t, dur * 0.35, dur * 0.35 + 0.6, 0, 1);
  const hot = useMemo(() => A.guy(), []);
  return (
    <Frame overlay={<Chip text={t < dur * 0.35 ? "¿MUCHO CALOR?" : "NUNCA EN VISTO"} y={300} k={1} />}>
      <Rooftop t={t} night={0} camT={cam(1 + zoom * 0.4, 540 + zoom * 230, 960 + zoom * 30)}>
        <g transform="translate(540 700)"><SunSvg t={t} /></g>
        <Raw html={STATIC.tinaco} />
        <g filter="url(#dropS)" transform="translate(810 1290) scale(1.12)"><Raw html={hot} /></g>
        <path d="M880,800 q12,20 0,30 q-12,-10 0,-30z M720,820 q10,16 0,24 q-10,-8 0,-24z" fill="#8fd3ff" stroke={K} strokeWidth={4} opacity={1 - zoom} />
      </Rooftop>
      <g transform={`translate(540 ${lerp(t, dur * 0.4, dur * 0.4 + 0.5, 2500, 900, Easing.out(Easing.back(1.4)))})`}>
        <g filter="url(#dropS)"><ChatPhone t={t - dur * 0.45} k={0.95} /></g>
      </g>
    </Frame>
  );
}

// ---------- 12. Cierre ----------
export function S12({ t, dur }) {
  const wink = t > 0.8 && t < 1.3;
  const html = useMemo(() => A.sun(165), []);
  const sunH = html.replace('id="sunRays"', `id="sunRays" transform="rotate(${t * 14})"`)
    .replace('<g id="sunEyes">', wink ? '<g id="sunEyes" transform="translate(0 -24) scale(1 .12) translate(0 24)">' : '<g id="sunEyes">');
  const b = Math.abs(Math.sin(t * 4)) * 18;
  return (
    <Frame overlay={<>
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center", fontFamily: "DQA", fontSize: 76, lineHeight: 1.15,
        color: "#fff", WebkitTextStroke: "14px #111", paintOrder: "stroke fill" }}>¿TÚ DÓNDE<br /><span style={{ color: "#ffd400" }}>TE ESCONDERÍAS?</span></div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1210 + b, textAlign: "center", fontFamily: "DQA", fontSize: 72,
        color: "#fff", WebkitTextStroke: "12px #111", paintOrder: "stroke fill" }}>COMENTA ↓</div></>}>
      <Rooftop t={t} night={0}>
        <g transform={`translate(540 ${860 + Math.sin(t * 2.5) * 10}) scale(${pop(t, 0, 0.5)})`}><Raw html={sunH} /></g>
      </Rooftop>
    </Frame>
  );
}

export const SCENES = [S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12];
// Temperatura que marca el termómetro en cada línea: [inicio, fin] (null = oculto)
export const TEMPS = [null, [15, 15], [15, 15], [15, 12], [12, 8], [8, -5], [-5, -18], [-18, -35], [-35, -73], [-73, -73], [-73, -240], null, null];
