// "El turno de noche" — guion de Luis (25 nov 2026), tal cual. [etiqueta, texto hablado, subtítulo con *resaltado*]
export const LINES = [
  ["whispers", "Eres guardia de seguridad en un edificio de oficinas.", "Eres *guardia de seguridad* en un edificio de oficinas."],
  ["serious", "Tu turno comienza a las once de la noche y termina a las siete de la mañana.", "Tu turno comienza a las *11 de la noche* y termina a las *7 de la mañana.*"],
  ["serious", "Llegas, saludas al guardia saliente y recibes las llaves.", "Llegas, saludas al guardia saliente y recibes *las llaves.*"],
  ["whispers", "Pero hoy notas algo extraño… está pálido y parece desesperado por irse.", "Pero hoy notas algo extraño… está *pálido* y parece *desesperado por irse.*"],
  ["confident", "Tu trabajo es sencillo: revisar las cámaras, recorrer los pasillos y asegurarte de que nadie entre.", "Tu trabajo es sencillo: revisar las cámaras, recorrer los pasillos y asegurarte de que *nadie entre.*"],
  ["serious", "Te preparas un café, enciendes los monitores y comienzas tu primera ronda.", "Te preparas un café, enciendes los monitores y comienzas tu *primera ronda.*"],
  ["whispers", "Todo está tranquilo. Demasiado tranquilo.", "Todo está tranquilo. *Demasiado tranquilo.*"],
  ["dramatically", "A las dos y trece de la madrugada, una cámara detecta movimiento en el piso ocho.", "A las *2:13* de la madrugada, una cámara detecta *movimiento en el piso 8.*"],
  ["serious", "Subes a revisar, pero no encuentras a nadie.", "Subes a revisar, pero *no encuentras a nadie.*"],
  ["whispers", "Entonces escuchas el sonido del ascensor.", "Entonces escuchas el sonido *del ascensor.*"],
  ["whispers", "Las puertas se abren lentamente.", "Las puertas se abren *lentamente.*"],
  ["serious", "Está vacío.", "Está *vacío.*"],
  ["dramatically", "O eso parece… porque alguien acaba de presionar el botón del piso ocho desde dentro.", "O eso parece… porque alguien acaba de presionar *el botón del piso 8* desde dentro."],
  ["serious", "Regresas a la recepción y encuentras una nota debajo del teclado.", "Regresas a la recepción y encuentras *una nota* debajo del teclado."],
  ["whispers", "Dice: «Si escuchas que alguien te llama desde el piso ocho, no contestes».", "Dice: «Si escuchas que alguien te llama desde el piso 8, *no contestes*»."],
  ["sarcastic", "Te ríes nerviosamente.", "Te ríes *nerviosamente.*"],
  ["dramatically", "Hasta que escuchas tu propio nombre por el intercomunicador.", "Hasta que escuchas *tu propio nombre* por el intercomunicador."],
  ["whispers", "La voz viene del piso ocho.", "La voz viene *del piso 8.*"],
  ["serious", "Abres las cámaras.", "Abres *las cámaras.*"],
  ["serious", "En el monitor aparece un hombre parado frente a una puerta.", "En el monitor aparece *un hombre* parado frente a una puerta."],
  ["whispers", "No se mueve.", "*No se mueve.*"],
  ["whispers", "Acercas la imagen.", "Acercas *la imagen.*"],
  ["whispers", "Lleva tu uniforme.", "Lleva *tu uniforme.*"],
  ["dramatically", "Tiene tu misma cara.", "Tiene *tu misma cara.*"],
  ["whispers", "Entonces, la figura levanta lentamente la cabeza y mira directamente a la cámara.", "Entonces, la figura levanta lentamente la cabeza y *mira directamente a la cámara.*"],
  ["dramatically", "En ese momento, escuchas una voz detrás de ti: «¿Por qué estás mirando las cámaras?».", "En ese momento, escuchas una voz *detrás de ti:* «¿Por qué estás mirando las cámaras?»."],
  ["serious", "Te giras.", "*Te giras.*"],
  ["whispers", "No hay nadie.", "*No hay nadie.*"],
  ["serious", "Miras nuevamente el monitor.", "Miras nuevamente *el monitor.*"],
  ["whispers", "La silla de seguridad aparece vacía.", "La silla de seguridad aparece *vacía.*"],
  ["whispers", "Y entonces entiendes algo…", "Y entonces *entiendes algo…*"],
  ["serious", "La cámara que estás viendo no está mostrando el piso ocho.", "La cámara que estás viendo *no está mostrando el piso 8.*"],
  ["dramatically", "Está mostrando la recepción.", "Está mostrando *la recepción.*"],
  ["dramatically", "Y alguien está sentado en tu silla.", "Y alguien está *sentado en tu silla.*"],
  ["mischievously", "¿Aceptarías trabajar el turno de noche?", "¿Aceptarías trabajar *el turno de noche?*"],
];

export const FPS = 30;
export const END = 3.0;
const WPS = 2.95;
const gapFor = (spoken) => (/[.…?»]$/.test(spoken) ? 0.45 : 0.3);
import timing from "./timing.json";

function words(sub) {
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
    const ws = words(sub); let start, dur, wt;
    if (timing.lines && timing.lines[i]) { ({ start, dur } = timing.lines[i]); wt = timing.lines[i].words; }
    else { start = t; dur = Math.max(1.3, spoken.split(/\s+/).length / WPS + gapFor(spoken)); }
    if (!wt || wt.length !== ws.length) {
      const total = ws.reduce((a, [w]) => a + w.length + 2, 0); let acc = 0; const speak = dur - 0.3;
      wt = ws.map(([w]) => { const s = (acc / total) * speak; acc += w.length + 2; return s; });
    }
    lines.push({ i, start, dur, words: ws.map(([w, hl], k) => [w, wt[k], hl]) });
    t = start + dur;
  });
  const last = lines[lines.length - 1]; last.dur += END;
  return { lines, total: last.start + last.dur };
}
