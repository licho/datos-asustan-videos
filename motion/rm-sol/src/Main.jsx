import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, Easing, Audio, staticFile } from "remotion";
import { buildTimeline, FPS } from "./script.js";
import { SCENES, TEMPS } from "./scenes.jsx";
import { Captions, fontCss } from "./ui.jsx";
import { Thermo, clamp } from "./pieces.jsx";

export const TL = buildTimeline();

function Line({ L }) {
  const f = useCurrentFrame(); const t = f / FPS;
  const Scene = SCENES[L.i];
  // pequeño "whip" de entrada en cada corte (excepto el gancho)
  const inK = L.i === 0 ? 1 : interpolate(t, [0, 0.18], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill style={{ perspective: 1600, opacity: 0.3 + 0.7 * inK }}>
      <AbsoluteFill style={{ transform: `scale(${1.1 - 0.06 * inK}) rotateY(${Math.sin(t * 0.55 + L.i) * 2.2}deg) rotateX(${Math.cos(t * 0.4 + L.i) * 1.4}deg)` }}>
      <Scene t={t} dur={L.dur} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

function Overlay() {
  const f = useCurrentFrame(); const t = f / FPS;
  const L = TL.lines.find(l => t >= l.start && t < l.start + l.dur) || TL.lines[TL.lines.length - 1];
  const lt = t - L.start;
  const tp = TEMPS[L.i];
  const first = TL.lines[1].start;
  let thermo = null;
  if (tp) {
    const v = interpolate(lt, [0.2, Math.max(0.5, L.dur - 0.3)], tp, { ...clamp, easing: Easing.inOut(Easing.cubic) });
    const k = interpolate(t, [first, first + 0.35], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
    const shake = L.i === 10 && lt > L.dur * 0.6 ? Math.sin(t * 70) * 5 : 0;
    thermo = <svg width={1080} height={1920} style={{ position: "absolute" }}><Thermo value={v} k={k} shake={shake} /></svg>;
  }
  return (
    <AbsoluteFill>
      {thermo}
      <Captions t={lt} words={L.words} />
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
