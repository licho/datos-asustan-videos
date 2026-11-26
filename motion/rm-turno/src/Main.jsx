import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate, Audio, staticFile } from "remotion";
import { buildTimeline, FPS } from "./script.js";
import { SHOTS } from "./Shots.jsx";
import { Captions, fontCss } from "./ui.jsx";

export const TL = buildTimeline();
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };

function Line({ L }) {
  const f = useCurrentFrame(); const t = f / FPS;
  const Shot = SHOTS[L.i];
  const fadeIn = L.i === 0 ? 1 : interpolate(t, [0, 0.15], [0.2, 1], clamp);
  return <AbsoluteFill style={{ opacity: fadeIn }}><Shot t={t} dur={L.dur} /></AbsoluteFill>;
}

function Overlay() {
  const f = useCurrentFrame(); const t = f / FPS;
  const L = TL.lines.find(l => t >= l.start && t < l.start + l.dur) || TL.lines[TL.lines.length - 1];
  return (
    <AbsoluteFill>
      {/* grano de película y viñeta para todo el video */}
      <svg width="1080" height="1920" style={{ position: "absolute", inset: 0, opacity: 0.09, mixBlendMode: "screen" }}>
        <filter id={`g${f}`}><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed={f % 89} /><feColorMatrix type="saturate" values="0" /></filter>
        <rect width="1080" height="1920" filter={`url(#g${f})`} />
      </svg>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 45%, transparent 50%, rgba(0,0,0,.6) 100%)" }} />
      <Captions t={t - L.start} words={L.words} />
    </AbsoluteFill>
  );
}

export const Main = ({ voice }) => (
  <AbsoluteFill style={{ background: "#000" }}>
    <style>{fontCss}</style>
    {TL.lines.map(L => (
      <Sequence key={L.i} from={Math.round(L.start * FPS)} durationInFrames={Math.round(L.dur * FPS)}>
        <Line L={L} />
      </Sequence>
    ))}
    <Overlay />
    {voice && <Audio src={staticFile(voice)} />}
  </AbsoluteFill>
);
