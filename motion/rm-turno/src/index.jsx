import { registerRoot, Composition } from "remotion";
import { Main, TL } from "./Main.jsx";
import { FPS } from "./script.js";
registerRoot(() => (
  <Composition id="Turno" component={Main} durationInFrames={Math.round(TL.total * FPS)} fps={FPS} width={1080} height={1920} defaultProps={{ voice: null }} />
));
