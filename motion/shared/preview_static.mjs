import * as A from "./art.mjs";
import fs from "fs";
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">${A.defs()}${A.sky()}
<g transform="translate(540 700)">${A.sun()}</g>${A.skylineFar()}${A.skylineNear()}${A.rooftop()}${A.tinaco()}${A.clothesline()}
<g transform="translate(810 1290) scale(1.12)">${A.guy()}</g>${A.vignette()}</svg>`;
fs.writeFileSync(process.argv[2], `<html><body style="margin:0">${svg}</body></html>`);
