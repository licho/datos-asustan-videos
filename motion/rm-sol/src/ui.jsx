import React from "react";
import { interpolate, staticFile } from "remotion";
import { clamp } from "./pieces.jsx";

export const fontCss = `@font-face{font-family:DQA;src:url(${staticFile("fonts/DejaVuSans-Bold.ttf")});}`;

export function Chip({ text, y, bg = "#e1232d", fg = "#fff", size = 56, k = 1 }) {
  if (k <= 0) return null;
  const s = 0.6 + 0.4 * Math.min(k, 1.15);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center",
      transform: `translateY(-50%) scale(${s})`, opacity: Math.min(1, k * 3) }}>
      <div style={{ background: bg, color: fg, fontFamily: "DQA", fontSize: size, lineHeight: 1,
        padding: `${size * 0.3}px ${size * 0.65}px`, borderRadius: size * 0.6, border: "6px solid #111", whiteSpace: "nowrap" }}>{text}</div>
    </div>
  );
}

// Subtítulos palabra por palabra (posición estándar del canal: y=1500)
export function Captions({ t, words }) {
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top: 1500, transform: "translateY(-50%)",
      display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: 22, rowGap: 4 }}>
      {words.map(([w, t0, hl], i) => {
        const k = interpolate(t, [t0, t0 + 0.12, t0 + 0.26], [0, 1.1, 1], clamp);
        const active = t >= t0 && (i === words.length - 1 || t < words[i + 1][1]);
        return (
          <span key={i} style={{ fontFamily: "DQA", fontSize: 66, lineHeight: 1.15, color: hl ? "#ffd400" : "#fff",
            WebkitTextStroke: "12px #111", paintOrder: "stroke fill", display: "inline-block",
            transform: `scale(${k}) translateY(${active ? -6 : 0}px)`, opacity: k > 0 ? 1 : 0 }}>{w}</span>
        );
      })}
    </div>
  );
}
