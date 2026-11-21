// Guion "¿Qué pasaría si el Sol se apagara?" (aprobado 21 nov 2026).
// [etiqueta de voz, texto hablado, subtítulo con *resaltado*]
export const LINES = [
  ["mischievously", "Si el Sol se apaga ahorita… tardarías ocho minutos en enterarte.", "Si el Sol *se apaga* ahorita… tardarías *ocho minutos* en enterarte."],
  ["confident", "Hice la cuenta de qué pasaría, minuto a minuto.", "Hice la cuenta de qué pasaría, *minuto a minuto.*"],
  ["serious", "Durante ocho minutos y veinte segundos, nada: la luz que ya venía en camino sigue llegando.", "Durante *ocho minutos y veinte segundos*, nada: la luz que ya venía en camino *sigue llegando.*"],
  ["dramatically", "Luego, apagón total. Y la Tierra sale disparada en línea recta, como canica en piso encerado.", "Luego, *apagón total.* Y la Tierra sale disparada *en línea recta*, como canica en piso encerado."],
  ["sarcastic", "La Luna también se apaga: solo brillaba de prestado.", "La Luna también se apaga: solo brillaba *de prestado.*"],
  ["serious", "Día tres: todo el planeta bajo cero. Se enfría unos veinte grados por día.", "*Día tres:* todo el planeta *bajo cero.* Se enfría unos *veinte grados por día.*"],
  ["sarcastic", "Semana uno: menos dieciocho grados. Ni la cobija de tigre de tu abuela te salva.", "*Semana uno: menos dieciocho grados.* Ni la cobija de tigre de tu abuela te salva."],
  ["mischievously", "Las plantas mueren en semanas. Los árboles grandes aguantan décadas… de puro coraje.", "Las plantas *mueren en semanas.* Los árboles grandes aguantan *décadas…* de puro coraje."],
  ["serious", "Año uno: setenta y tres bajo cero. El mar se congela por arriba, pero ese hielo protege el agua de abajo por cientos de miles de años.", "*Año uno: setenta y tres bajo cero.* El mar se congela por arriba, pero ese hielo *protege el agua de abajo* por cientos de miles de años."],
  ["confident", "¿Y los humanos? Bajo tierra, junto a los volcanes. Islandia ya calienta casi nueve de cada diez casas con el calor de la Tierra.", "¿Y los humanos? *Bajo tierra, junto a los volcanes.* Islandia ya calienta casi *nueve de cada diez casas* con el calor de la Tierra."],
  ["dramatically", "Al final, el planeta llegaría a doscientos cuarenta bajo cero. Más frío que Plutón.", "Al final, el planeta llegaría a *doscientos cuarenta bajo cero.* Más frío que *Plutón.*"],
  ["mischievously", "Así que la próxima vez que te quejes del calor… acuérdate: el Sol es el único que nunca te ha dejado en visto.", "Así que la próxima vez que te quejes del calor… acuérdate: el Sol es el único que *nunca te ha dejado en visto.*"],
  ["excited", "¿Tú dónde te esconderías? Te leo abajo.", "¿Tú dónde te esconderías? *Te leo abajo.*"],
];

export const FPS = 30;
export const END = 3.0;            // cierre en silencio al final
const WPS = 2.95, GAP = 0.35;       // ritmo estimado de la voz (se reemplaza con la voz real)

// Tiempos: si existe timing.json (de la voz real) se usa; si no, se estima por palabras.
import timing from "./timing.json";

function words(sub) {
  // ["palabra", resaltada]
  const out = []; let hl = false;
  for (const tok of sub.split(/(\*)/)) {
    if (tok === "*") { hl = !hl; continue; }
    for (const w of tok.split(/\s+/).filter(Boolean)) out.push([w, hl]);
  }
  return out;
}

export function buildTimeline() {
  let t = 0; const lines = [];
  LINES.forEach(([, spoken, sub], i) => {
    const ws = words(sub);
    let start, dur, wt;
    if (timing.lines && timing.lines[i]) {
      ({ start, dur } = timing.lines[i]); wt = timing.lines[i].words;
    } else {
      start = t; dur = Math.max(i === 0 ? 4.4 : 2.6, spoken.split(/\s+/).length / WPS + GAP);
    }
    if (!wt || wt.length !== ws.length) {
      // reparte el tiempo de la línea según el largo de cada palabra
      const total = ws.reduce((a, [w]) => a + w.length + 2, 0); let acc = 0;
      const speak = dur - GAP;
      wt = ws.map(([w]) => { const s = (acc / total) * speak; acc += w.length + 2; return s; });
    }
    lines.push({ i, start, dur, words: ws.map(([w, hl], k) => [w, wt[k], hl]) });
    t = start + dur;
  });
  const last = lines[lines.length - 1];
  last.dur += END;
  return { lines, total: last.start + last.dur };
}
