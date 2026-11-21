import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, staticFile } from "remotion";
import * as A from "../../shared/art.mjs";

// Cada pieza estática se dibuja una vez; la animación solo cambia transformaciones y opacidades.
const svgPart = (html) => ({ __html: html });
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };
const ease = Easing.inOut(Easing.cubic);

// Pieza con partes animables: reemplaza atributos de grupos por id dentro del texto SVG.
function withAttrs(html, map) {
  let out = html;
  for (const [id, attrs] of Object.entries(map)) {
    const a = Object.entries(attrs).map(([k, v]) => `${k}="${v}"`).join(" ");
    out = out.replace(new RegExp(`id="${id}"( transform="[^"]*")?( opacity="[^"]*")?`), `id="${id}" ${a}`);
  }
  return out;
}

const fontCss = `@font-face{font-family:DQA;src:url(${staticFile("fonts/DejaVuSans-Bold.ttf")});}`;

function Chip({ text, y, bg, fg, size = 56, k }) {
  const s = 0.6 + 0.4 * k;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center",
      transform: `translateY(-50%) scale(${s})`, opacity: Math.min(1, k * 3) }}>
      <div style={{ background: bg, color: fg, fontFamily: "DQA", fontSize: size, lineHeight: 1,
        padding: `${size * 0.3}px ${size * 0.65}px`, borderRadius: size * 0.6, border: "6px solid #111", whiteSpace: "nowrap" }}>{text}</div>
    </div>
  );
}

export const Gancho = ({ bare = false }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const H = A.HOOK; const clic = H.clic;

  // --- cámara: empuje suave, sacudida en el clic, luego viaja hacia el señor
  const push = interpolate(t, [0, clic], [1.0, 1.06], { ...clamp, easing: ease });
  const travel = interpolate(t, [2.3, 5.0], [0, 1], { ...clamp, easing: ease });
  const scale = push + travel * 0.14;
  const fx = 540 + travel * 170, fy = 960 + travel * 40;
  const shakeK = interpolate(t, [clic, clic + 0.35], [1, 0], clamp);
  const shx = Math.sin(t * 90) * 14 * shakeK, shy = Math.cos(t * 77) * 10 * shakeK;
  const cam = `translate(${540 + shx} ${960 + shy}) scale(${scale}) translate(${-fx} ${-fy})`;

  // --- sol
  const offK = interpolate(t, [clic, clic + 0.12], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const squash = interpolate(t, [clic - 0.18, clic, clic + 0.12, clic + 0.3], [0, 1, -0.6, 0], clamp);
  const sunSX = 1 + 0.07 * squash, sunSY = 1 - 0.07 * squash;
  const pulse = 1 + 0.03 * Math.sin(t * 5);
  const blink = (t > 0.8 && t < 0.95) ? 0.12 : 1;
  const shiver = offK > 0.9 ? Math.sin(t * 60) * 3 : 0;
  const sunHtml = useMemo(() => A.sun(165), []);
  const sun = withAttrs(sunHtml, {
    sunGlow: { transform: `scale(${pulse * (1 - 0.6 * offK)})`, opacity: (1 - offK).toFixed(3) },
    sunRays: { transform: `rotate(${t * 14}) scale(${1 - 0.75 * offK})`, opacity: (1 - offK).toFixed(3) },
    sunOn: { opacity: (1 - offK).toFixed(3) },
    sunOff: { opacity: offK.toFixed(3) },
    sunEyes: { transform: `translate(0 -24) scale(1 ${blink}) translate(0 24)` },
  });

  const flashK = interpolate(t, [clic, clic + 0.35], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const flashOp = interpolate(t, [clic, clic + 0.04, clic + 0.35], [0, 0.7, 0], clamp);
  // --- "¡CLIC!"
  const clicK = spring({ frame: f - Math.round(clic * fps), fps, config: { damping: 9, stiffness: 180 } });
  const clicOp = interpolate(t, [clic, clic + 0.05, clic + 0.9, clic + 1.15], [0, 1, 1, 0], clamp);

  // --- fotones que siguen viajando
  const phOn = interpolate(t, [clic + 0.25, clic + 0.6], [0, 1], clamp);
  const photons = [...Array(7)].map((_, i) => {
    const p = ((t - clic) * 0.75 + i / 7) % 1; const q = A.beamAt(p);
    const op = phOn * Math.min(1, p * 6, (1 - p) * 6);
    return <circle key={i} cx={q.x} cy={q.y} r={24 + 6 * Math.sin(t * 9 + i)} fill="url(#photon)" opacity={op} />;
  });

  // --- señor: respira, desliza el dedo, se ríe del celular
  const laughing = t > 3.55 && t < 4.6;
  const bob = laughing ? Math.abs(Math.sin((t - 3.55) * 14)) * -10 : Math.sin(t * 2.2) * 3;
  const guyHtml = useMemo(() => A.guy(), []);
  const guy = withAttrs(guyHtml, {
    guyHead: { transform: `translate(0 ${-395 + bob * 0.6}) rotate(${laughing ? Math.sin(t * 14) * 4 : Math.sin(t * 1.3) * 2})` },
    guySmile: { opacity: laughing ? 0 : 1 },
    guyLaugh: { opacity: laughing ? 1 : 0 },
    guyArms: { transform: `translate(0 ${bob * 0.5 + Math.sin(t * 6) * 2})` },
    phoneGlow: { opacity: (0.75 + 0.25 * Math.sin(t * 7)).toFixed(3) },
  });

  // --- tendedero
  const line = useMemo(() => A.clothesline(), []);
  const lineAnim = [1, 2, 3].reduce((h, i) =>
    h.replace(`id="cloth${i}" transform="translate(`, `id="cloth${i}" data-a="" transform="rotate(${(Math.sin(t * 2.4 + i) * 5).toFixed(2)} ${[385, 488, 585][i - 1]} 960) translate(`), line);

  const statics = useMemo(() => ({ defs: A.defs(), sky: A.sky(), far: A.skylineFar(), near: A.skylineNear(),
    roof: A.rooftop(), tinaco: A.tinaco(), vig: A.vignette() }), []);

  // --- letreros y subtítulos
  const chip1K = interpolate(t, [0, 0.25], [0.85, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  const chip2K = spring({ frame: f - Math.round((clic + 0.55) * fps), fps, config: { damping: 10 } });
  const secs = 20 - Math.max(0, Math.floor(t - (clic + 0.55)));
  const timer = `TE ENTERAS EN 8:${String(secs).padStart(2, "0")}`;

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <style>{fontCss}</style>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute" }}>
        <g dangerouslySetInnerHTML={svgPart(statics.defs)} />
        <g transform={cam}>
          <g dangerouslySetInnerHTML={svgPart(statics.sky)} />
          <g transform={`translate(540 700) scale(${sunSX} ${sunSY}) translate(${shiver} 0)`} dangerouslySetInnerHTML={svgPart(sun)} />
          <circle cx={540} cy={700} r={165 + 140 * flashK} fill="#fffbe6" opacity={flashOp} />
          <g transform={`translate(${-12 * t} 0)`} dangerouslySetInnerHTML={svgPart(statics.far)} />
          <g transform={`translate(${-26 * t} 0)`} dangerouslySetInnerHTML={svgPart(statics.near)} />
          <g dangerouslySetInnerHTML={svgPart(statics.roof)} />
          <g dangerouslySetInnerHTML={svgPart(statics.tinaco)} />
          <g dangerouslySetInnerHTML={svgPart(lineAnim)} />
          <g transform="translate(810 1290) scale(1.12)" dangerouslySetInnerHTML={svgPart(guy)} />
          <g>{photons}</g>
          <g transform={`translate(255 600) rotate(-12) scale(${clicK})`} opacity={clicOp}>
            <text textAnchor="middle" dominantBaseline="middle" fontFamily="DQA" fontSize="110" fill={A.C.yel}
              stroke="#111" strokeWidth="16" paintOrder="stroke" strokeLinejoin="round">¡CLIC!</text>
          </g>
        </g>
        <g dangerouslySetInnerHTML={svgPart(statics.vig)} />
      </svg>
      <Chip text={H.chip1} y={300} bg={A.C.red} fg="#fff" k={chip1K} />
      {t > clic + 0.5 && <Chip text={timer} y={420} bg="#111" fg={A.C.yel} size={48} k={chip2K} />}
      {!bare && <Captions t={t} words={H.words} />}
    </AbsoluteFill>
  );
};

function Captions({ t, words }) {
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top: 1500, transform: "translateY(-50%)",
      display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: 22, rowGap: 4 }}>
      {words.map(([w, t0, hl], i) => {
        const k = interpolate(t, [t0, t0 + 0.12, t0 + 0.26], [0, 1.1, 1], clamp);
        const active = t >= t0 && (i === words.length - 1 || t < words[i + 1][1]);
        return (
          <span key={i} style={{ fontFamily: "DQA", fontSize: 70, lineHeight: 1.15, color: hl ? A.C.yel : "#fff",
            WebkitTextStroke: "12px #111", paintOrder: "stroke fill", display: "inline-block",
            transform: `scale(${k}) translateY(${active ? -6 : 0}px)`, opacity: k > 0 ? 1 : 0 }}>{w}</span>
        );
      })}
    </div>
  );
}
