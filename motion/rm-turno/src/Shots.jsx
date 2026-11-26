// Tomas de cada línea de "El turno de noche" (3D real con Three.js dentro de Remotion).
import React from "react";
import { interpolate, Easing, useCurrentFrame, staticFile } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { Cam, Guard, Building, Reception, Corridor, Dust, useCanvasTexture, rnd } from "./World.jsx";
import { Chip } from "./ui.jsx";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };
const ease = Easing.inOut(Easing.cubic);
const L = (t, a, b, v0, v1, e = ease) => interpolate(t, [a, b], [v0, v1], { ...clamp, easing: e });
const lerp3 = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
const hand = (t, amp = 1) => [Math.sin(t * 1.3) * 0.02 * amp + Math.sin(t * 3.1) * 0.006 * amp, Math.sin(t * 1.7 + 1) * 0.015 * amp, 0];
const add = (a, b) => a.map((v, i) => v + b[i]);

// ---------- pantallitas verdes de los monitores ----------
function feedDraw(idx, t, opts = {}) {
  return (c, w, h) => {
    c.fillStyle = "#06140c"; c.fillRect(0, 0, w, h);
    c.strokeStyle = "rgba(120,255,170,.45)"; c.lineWidth = 3;
    // pasillo en perspectiva
    c.beginPath();
    c.moveTo(0, h); c.lineTo(w * 0.38, h * 0.42); c.lineTo(w * 0.62, h * 0.42); c.lineTo(w, h);
    c.moveTo(0, 0); c.lineTo(w * 0.38, h * 0.3); c.lineTo(w * 0.62, h * 0.3); c.lineTo(w, 0);
    c.rect(w * 0.38, h * 0.3, w * 0.24, h * 0.12); c.stroke();
    for (let k = 0; k < 4; k++) { const x = w * (0.1 + k * 0.08); c.strokeRect(x, h * 0.45 - k * 8, 18 - k * 3, 60 - k * 12); }
    if (opts.figure) { c.fillStyle = "rgba(10,20,14,.95)"; const fx = w * (0.48 + Math.sin(t * 0.7) * 0.06); c.fillRect(fx, h * 0.33, 22, 70); c.beginPath(); c.arc(fx + 11, h * 0.33 - 6, 11, 0, 7); c.fill(); }
    for (let k = 0; k < 900; k++) { c.fillStyle = `rgba(160,255,190,${rnd(k + Math.floor(t * 24) * 31, idx + 2) * 0.18})`; c.fillRect(rnd(k, idx + Math.floor(t * 24)) * w, rnd(k + 7, idx + Math.floor(t * 24)) * h, 2, 2); }
    c.fillStyle = "rgba(170,255,200,.9)"; c.font = "bold 26px DejaVu Sans Mono"; c.fillText(`CAM 0${idx + 1}${opts.label ? " · " + opts.label : ""}`, 14, 34);
    if (Math.floor(t * 2) % 2 === 0) { c.fillStyle = "#ff3b3b"; c.beginPath(); c.arc(w - 28, 26, 9, 0, 7); c.fill(); }
  };
}
function Screens({ t, on = 6, motion8 = false, children }) {
  const tex = [0, 1, 2, 3, 4, 5].map(i => useCanvasTexture(320, 200, feedDraw(i, t, i === 3 ? { label: "PISO 8", figure: motion8 } : {}), [i]));
  return children(tex.map((x, i) => (i < on ? x : null)));
}

// ---------- nota escrita a mano ----------
function Note({ t, position, rotation, scale = 1 }) {
  const tex = useCanvasTexture(512, 384, (c, w, h) => {
    c.fillStyle = "#efe6cf"; c.fillRect(0, 0, w, h);
    for (let k = 0; k < 9; k++) { c.strokeStyle = "rgba(90,120,170,.25)"; c.beginPath(); c.moveTo(0, 60 + k * 36); c.lineTo(w, 60 + k * 36); c.stroke(); }
    c.fillStyle = "#1d2440"; c.font = "italic 38px DejaVu Serif";
    ["Si escuchas que", "alguien te llama", "desde el piso 8,", "NO CONTESTES."].forEach((l, k) => c.fillText(l, 36 + (k % 2) * 6, 92 + k * 72));
    c.fillStyle = "rgba(120,80,40,.18)"; c.beginPath(); c.arc(w * 0.82, h * 0.78, 50, 0, 7); c.fill();
  }, []);
  return (
    <mesh position={position} rotation={rotation} scale={scale}>
      <planeGeometry args={[0.36, 0.27]} />
      <meshStandardMaterial map={tex} roughness={0.95} />
    </mesh>
  );
}

// ---------- ondas del intercomunicador ----------
function Waves({ t, position }) {
  return <group position={position} rotation={[0, Math.PI / 2, 0]}>{[0, 1, 2].map(k => {
    const p = (t * 0.8 + k / 3) % 1;
    return <mesh key={k} scale={0.3 + p * 1.4}><torusGeometry args={[0.3, 0.012, 6, 40]} /><meshBasicMaterial color="#ff4a4a" transparent opacity={(1 - p) * 0.8} /></mesh>;
  })}</group>;
}

// ---------- llaves ----------
function Keys({ position, t }) {
  return <group position={position} rotation={[0.3, t * 0.6, Math.sin(t * 4) * 0.3]}>
    <mesh><torusGeometry args={[0.05, 0.008, 8, 20]} /><meshStandardMaterial color="#c9b37a" metalness={0.9} roughness={0.25} /></mesh>
    {[0, 1, 2].map(k => <mesh key={k} position={[0.03 + k * 0.012, -0.07, 0]} rotation={[0, 0, 0.3 - k * 0.3]}><boxGeometry args={[0.018, 0.1, 0.005]} /><meshStandardMaterial color="#b8bcc4" metalness={0.9} roughness={0.2} /></mesh>)}
  </group>;
}

// ---------- lienzo 3D estándar ----------
function Stage({ children, fogNear = 4, fogFar = 26, bg = "#04060a", amb = 0.32 }) {
  return (
    <ThreeCanvas width={1080} height={1920} shadows style={{ background: bg }} gl={{ antialias: true }}>
      <color attach="background" args={[bg]} />
      <fog attach="fog" args={[bg, fogNear, fogFar]} />
      <ambientLight intensity={amb} color="#8fa6c8" />
      <hemisphereLight args={["#9fb8e0", "#1a1410", amb * 0.8]} />
      {children}
    </ThreeCanvas>
  );
}

// ---------- imagen de cámara de seguridad a pantalla completa ----------
function Cctv({ t, label, children, glitch = 0, zoomPx = 0 }) {
  const f = useCurrentFrame();
  const stamp = `02:${String(47 + Math.floor(t / 60)).padStart(2, "0")}:${String(Math.floor(t + 13) % 60).padStart(2, "0")}`;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#000" }}>
      <div style={{ position: "absolute", inset: 0, filter: `grayscale(1) sepia(.5) hue-rotate(70deg) saturate(1.9) contrast(1.35) brightness(1.15) blur(${0.6 + zoomPx}px)`,
        transform: glitch ? `translateX(${Math.sin(f * 7.3) * 18 * glitch}px)` : "none" }}>
        {children}
      </div>
      <svg width="1080" height="1920" style={{ position: "absolute", inset: 0, mixBlendMode: "screen", opacity: 0.22 }}>
        <filter id={`n${f}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 97} /><feColorMatrix type="saturate" values="0" /></filter>
        <rect width="1080" height="1920" filter={`url(#n${f})`} />
      </svg>
      <div style={{ position: "absolute", inset: 0, background: "repeating-linear-gradient(0deg, rgba(0,0,0,.28) 0 2px, transparent 2px 5px)" }} />
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,.75) 100%)" }} />
      <div style={{ position: "absolute", left: 70, top: 520, fontFamily: "DejaVu Sans Mono", fontWeight: 700, fontSize: 40, color: "#c8ffd8", textShadow: "0 0 8px #3f8" }}>{label}</div>
      <div style={{ position: "absolute", right: 70, top: 520, fontFamily: "DejaVu Sans Mono", fontWeight: 700, fontSize: 40, color: "#ff5050", opacity: Math.floor(t * 2) % 2 ? 0.25 : 1 }}>● REC</div>
      <div style={{ position: "absolute", left: 70, top: 1290, fontFamily: "DejaVu Sans Mono", fontWeight: 700, fontSize: 38, color: "#c8ffd8" }}>{stamp}</div>
      {glitch > 0 && <div style={{ position: "absolute", left: 0, right: 0, top: 700 + (f * 37) % 600, height: 30 + (f % 5) * 10, background: "rgba(200,255,220,.25)", mixBlendMode: "screen" }} />}
    </div>
  );
}

// ======================= tomas por línea =======================
// Cada función: ({t, dur}) => JSX (pantalla completa). Las de 3D usan <Stage>.
const recep = (t, extra = {}, cam) => (
  <Screens t={t} on={extra.on ?? 6} motion8={extra.motion8}>{scr => (
    <Stage fogFar={18}>
      <Cam {...cam} />
      <Reception t={t} screens={scr} {...extra} />
      <Dust t={t} center={[0, 2, -1]} spread={[6, 3, 4]} />
      {extra.children}
    </Stage>
  )}</Screens>
);

export const SHOTS = [
  // 0 Eres guardia… — edificio de noche
  ({ t, dur }) => (<>
    <Stage fogNear={14} fogFar={60} amb={0.25}>
      <Cam pos={add(lerp3([7, 2.2, 26], [3, 1.8, 17], L(t, 0, dur, 0, 1)), hand(t, .5))} look={[0, 6, 0]} fov={52} />
      <Building t={t} />
    </Stage>
    <Chip text="EL TURNO DE NOCHE" y={300} k={1} /></>),
  // 1 Tu turno comienza…
  ({ t, dur }) => (<>
    <Stage fogNear={10} fogFar={50} amb={0.25}>
      <Cam pos={add(lerp3([0, 1.7, 15], [0, 1.6, 9.5], L(t, 0, dur, 0, 1)), hand(t))} look={[0, 1.9, 0]} fov={50} />
      <Building t={t} />
    </Stage>
    <Chip text="11:00 PM → 7:00 AM" y={300} bg="#111" fg="#ffd400" size={52} k={1} /></>),
  // 2 Llegas, saludas… llaves
  ({ t, dur }) => recep(t, { on: 0, children: <>
      <Guard position={[0.6, 0, 1.2]} rotation={0.25} pale t={t} />
      <Keys position={lerp3([0.35, 1.25, 1.55], [0.05, 1.45, 3.1], L(t, dur * 0.45, dur * 0.9, 0, 1))} t={t} />
    </> }, { pos: add([0, 1.65, 3.8], hand(t)), look: [0.4, 1.55, 1], fov: 46 }),
  // 3 Pero hoy notas algo extraño… pálido, desesperado
  ({ t, dur }) => recep(t, { on: 0, children:
      <Guard position={lerp3([0.6, 0, 1.6], [4.2, 0, -2.6], L(t, dur * 0.45, dur, 0, 1, Easing.in(Easing.quad)))}
        rotation={t < dur * 0.45 ? 0.15 + Math.sin(t * 30) * 0.03 : 2.43} pale t={t} walk={t > dur * 0.45 ? 1 : 0} /> },
    { pos: add(lerp3([0.55, 1.74, 3.1], [0.2, 1.7, 3.8], L(t, dur * 0.4, dur, 0, 1)), hand(t, 1.5)), look: lerp3([0.6, 1.72, 1.6], [3.5, 1.4, -2], L(t, dur * 0.45, dur, 0, 1)), fov: 40 }),
  // 4 Tu trabajo es sencillo
  ({ t, dur }) => recep(t, { on: 6 }, { pos: add([Math.sin(L(t, 0, dur, -0.6, 0.6)) * 3.4, 1.9, Math.cos(L(t, 0, dur, -0.6, 0.6)) * 3.4 - 1.5], hand(t)), look: [0, 1.5, -1.6], fov: 48 }),
  // 5 Café, monitores, primera ronda
  ({ t, dur }) => recep(t, { on: Math.floor(L(t, dur * 0.3, dur * 0.75, 0, 6.99, Easing.linear)) },
    { pos: add(lerp3([1.4, 1.35, -0.5], [0.3, 1.75, 0.9], L(t, 0, dur, 0, 1)), hand(t)), look: lerp3([1.1, 1.1, -1.2], [0, 1.6, -1.85], L(t, 0, dur, 0, 1)), fov: 45 }),
  // 6 Todo está tranquilo. Demasiado tranquilo. — primera ronda por el pasillo
  ({ t, dur }) => (<Stage fogFar={20}>
    <Cam pos={add([0, 1.65, 2 - t * 0.9], hand(t, 1.4))} look={[0, 1.6, -20]} fov={55} />
    <Corridor t={t} /><Dust t={t} center={[0, 1.6, -4 - t]} />
  </Stage>),
  // 7 2:13 — movimiento en el piso 8 (imagen de cámara)
  ({ t, dur }) => (<>
    <Cctv t={t} label="CAM 08 · PISO 8">
      <Stage fogFar={18} amb={0.3}>
        <Cam pos={[1.3, 2.9, -4]} look={[0, 1.0, -12]} fov={60} />
        <Corridor t={t} figure={t > dur * 0.35 && t < dur * 0.65 ? <Guard position={[L(t, dur * 0.35, dur * 0.65, -1.2, 1.4, Easing.linear), 0, -12]} rotation={Math.PI / 2} t={t} walk={1} /> : null} />
      </Stage>
    </Cctv>
    <Chip text="2:13 AM" y={300} bg="#111" fg="#ff5050" size={56} k={1} /></>),
  // 8 Subes a revisar — pasillo del piso 8, POV mirando a los lados
  ({ t, dur }) => (<><Stage fogFar={18}>
    <Cam pos={add([0, 1.65, 1 - t * 0.6], hand(t, 1.6))} look={[Math.sin(t * 1.1) * 4, 1.5, -12]} fov={55} />
    <Corridor t={t} /><Dust t={t} />
  </Stage><Chip text="PISO 8" y={300} k={1} /></>),
  // 9 Entonces escuchas el sonido del ascensor
  ({ t, dur }) => (<Stage fogFar={22}>
    <Cam pos={add([0, 1.65, -8], hand(t))} look={[L(t, 0, dur * 0.6, -3, 0), 1.45, -22]} fov={L(t, 0, dur, 55, 42)} />
    <Corridor t={t} />
  </Stage>),
  // 10 Las puertas se abren lentamente
  ({ t, dur }) => (<Stage fogFar={22}>
    <Cam pos={add([0, 1.6, L(t, 0, dur, -16, -18.5)], hand(t, .6))} look={[0, 1.3, -23]} fov={46} />
    <Corridor t={t} doorsOpen={L(t, 0.1, dur, 0, 1, Easing.inOut(Easing.sin))} />
  </Stage>),
  // 11 Está vacío
  ({ t, dur }) => (<Stage fogFar={22}>
    <Cam pos={add([0, 1.55, L(t, 0, dur, -19.2, -19.8)], hand(t, .5))} look={[0, 1.25, -23]} fov={50} />
    <Corridor t={t} doorsOpen={1} />
  </Stage>),
  // 12 Alguien presiona el botón del piso 8 desde dentro
  ({ t, dur }) => (<Stage fogFar={22}>
    <Cam pos={add([-0.1, 1.25, -21.2], hand(t, .4))} look={[0.55, 1.12, -22.6]} fov={L(t, 0, dur, 40, 26)} />
    <Corridor t={t} doorsOpen={1} button8={L(t, dur * 0.45, dur * 0.55, 0, 1)} />
  </Stage>),
  // 13 Regresas a la recepción… una nota debajo del teclado
  ({ t, dur }) => recep(t, { on: 6, keyboardLift: L(t, dur * 0.45, dur * 0.8, 0, 1),
    children: <Note t={t} position={[0, 1.055, -1.15]} rotation={[-Math.PI / 2, 0, 0.1]} /> },
    { pos: add(lerp3([0, 1.9, 1.2], [0, 1.55, -0.45], L(t, 0, dur, 0, 1)), hand(t)), look: [0, 1.06, -1.15], fov: 50 }),
  // 14 Dice: «…no contestes»
  ({ t, dur }) => recep(t, { on: 6, keyboardLift: 1,
    children: <Note t={t} position={[0, 1.5, 0.05]} rotation={[-0.25, 0, Math.sin(t * 2) * 0.02]} /> },
    { pos: add([0, 1.6, 0.9], hand(t, .5)), look: [0, 1.5, 0.05], fov: 40 }),
  // 15 Te ríes nerviosamente
  ({ t, dur }) => recep(t, { on: 6, keyboardLift: 1, lightsFlicker: 1,
    children: <Note t={t} position={[0.1, 1.38, -0.2]} rotation={[-0.6, 0, 0.2 + Math.sin(t * 9) * 0.04]} /> },
    { pos: add([0.4, 1.75, 0.9], hand(t, 2.5)), look: [0, 1.4, -1], fov: 50 }),
  // 16 Hasta que escuchas tu propio nombre por el intercomunicador
  ({ t, dur }) => recep(t, { on: 6, intercom: Math.floor(t * 4) % 2 ? 1 : 0.3, children: <Waves t={t} position={[-4.7, 1.7, -1.6]} /> },
    { pos: add([-2.2, 1.75, 0.8], hand(t, 1.2)), look: lerp3([0, 1.5, -1.5], [-4.9, 1.7, -1.6], L(t, 0, 0.5, 0, 1, Easing.out(Easing.cubic))), fov: L(t, 0, dur, 50, 30) }),
  // 17 La voz viene del piso 8
  ({ t, dur }) => recep(t, { on: 6, intercom: 1, children: <Waves t={t} position={[-4.7, 1.7, -1.6]} /> },
    { pos: add([-3.2, 1.72, -1.6 + Math.sin(t) * 0.1], hand(t)), look: [-4.9, 1.7, -1.6], fov: 44 }),
  // 18 Abres las cámaras
  ({ t, dur }) => recep(t, { on: 6, motion8: true }, { pos: add(lerp3([0, 1.7, 0.7], [0, 1.72, -0.6], L(t, 0, dur, 0, 1)), hand(t)), look: [0, 1.72, -1.85], fov: 46 }),
];

// 19–24: la figura en la cámara del piso 8
const figureFeed = (t, dur, i) => {
  const fovs = { 19: [58, 55], 20: [55, 54], 21: [54, 30], 22: [26, 22], 23: [18, 15], 24: [15, 13] };
  const [f0, f1] = fovs[i];
  const look = i <= 20 ? [0, 1.2, -12] : i === 22 ? [0, 1.45, -12] : [0, 1.75, -12];
  const headUp = i < 24 ? 0 : L(t, 0.2, dur * 0.85, 0, 1, Easing.inOut(Easing.sin));
  return (
    <Cctv t={t} label="CAM 08 · PISO 8" glitch={i === 24 && t > dur * 0.8 ? 1 : 0} zoomPx={i >= 21 ? 0.6 : 0}>
      <Stage fogFar={20} amb={0.32}>
        <Cam pos={[1.2, 2.8, -5]} look={look} fov={L(t, 0, dur, f0, f1)} />
        <Corridor t={t} flicker={1} figure={<Guard position={[0, 0, -12]} rotation={0} t={t} headUp={headUp} double eyesGlow={i === 24 ? L(t, dur * 0.6, dur * 0.9, 0, 1) : 0} />} />
      </Stage>
    </Cctv>
  );
};
for (const i of [19, 20, 21, 22, 23, 24]) SHOTS[i] = ({ t, dur }) => figureFeed(t, dur, i);

// 25 Una voz detrás de ti
SHOTS[25] = ({ t, dur }) => recep(t, { on: 6, motion8: true, lightsFlicker: 1 },
  { pos: add([0, 1.7, -0.5 + L(t, 0, dur, 0, -0.15)], hand(t, 0.3)), look: [0, 1.72, -1.85], fov: L(t, 0, dur, 46, 40) });
// 26 Te giras (giro rápido)
SHOTS[26] = ({ t, dur }) => {
  const a = L(t, 0, Math.min(dur, 0.7), 0, Math.PI, Easing.inOut(Easing.quad));
  return recep(t, { on: 6 }, { pos: [0, 1.7, -0.5], look: [Math.sin(a) * 5, 1.6, -0.5 - Math.cos(a) * 5], fov: 52, roll: Math.sin(a) * 0.06 });
};
// 27 No hay nadie
SHOTS[27] = ({ t, dur }) => recep(t, { on: 6 }, { pos: add([0, 1.7, -0.5], hand(t, 0.6)), look: [L(t, 0, dur, -1.5, 1.5), 1.5, 5], fov: 54 });
// 28 Miras nuevamente el monitor
SHOTS[28] = ({ t, dur }) => {
  const a = L(t, 0, Math.min(dur, 0.8), Math.PI, 0, Easing.inOut(Easing.quad));
  return recep(t, { on: 6 }, { pos: [0, 1.7, -0.5], look: [Math.sin(a) * 5, 1.65, -0.5 - Math.cos(a) * 5], fov: L(t, 0, dur, 52, 34) });
};
// 29–33: la imagen de la "cámara del piso 8" que en realidad es la recepción
const recFeed = (t, dur, i) => {
  const label = i < 31 ? "CAM 08 · PISO 8" : i === 31 ? (Math.floor(t * 8) % 2 ? "CAM 08 · PISO 8" : "CAM 01 · REC███") : "CAM 01 · RECEPCIÓN";
  const sitter = i === 33 ? <Guard position={[0, 0, 0]} rotation={Math.PI} sit t={t} double headUp={L(t, 0.3, dur * 0.8, 0.2, 1)} eyesGlow={L(t, dur * 0.5, dur * 0.85, 0, 1)} /> : null;
  return (
    <Cctv t={t} label={label} glitch={i === 31 ? 1 : 0}>
      <Screens t={t} on={6}>{scr => (
        <Stage fogFar={18} amb={0.3}>
          <Cam pos={[3.6, 3.9, 2.8]} look={[0, 0.9, -0.6]} fov={L(t, 0, dur, i >= 32 ? 40 : 52, i >= 32 ? 34 : 48)} />
          <Reception t={t} screens={scr} chairGuard={sitter} />
        </Stage>
      )}</Screens>
    </Cctv>
  );
};
for (const i of [29, 30, 31, 32, 33]) SHOTS[i] = ({ t, dur }) => recFeed(t, dur, i);
// 34 ¿Aceptarías…? — los monitores se apagan uno por uno
SHOTS[34] = ({ t, dur }) => (<>
  {recep(t, { on: 6 - Math.floor(L(t, 0.3, 2.2, 0, 6.99, Easing.linear)) }, { pos: add([0, 1.8, 1.6], hand(t, .5)), look: [0, 1.6, -1.85], fov: 44 })}
  <div style={{ position: "absolute", left: 0, right: 0, top: 1230 + Math.abs(Math.sin(t * 4)) * 16, textAlign: "center", fontFamily: "DQA", fontSize: 70,
    color: "#fff", WebkitTextStroke: "12px #111", paintOrder: "stroke fill", opacity: L(t, 1.5, 2, 0, 1) }}>COMENTA ↓</div>
</>);
