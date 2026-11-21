import { registerRoot, Composition } from "remotion";
import { Gancho } from "./Gancho.jsx";
import { Main, TL } from "./Main.jsx";
import { HOOK } from "../../shared/art.mjs";
import { FPS } from "./script.js";

const Root = () => (
  <>
    <Composition id="Gancho" component={Gancho} durationInFrames={Math.round(HOOK.dur * 30)} fps={30} width={1080} height={1920} />
    <Composition id="Sol" component={Main} durationInFrames={Math.round(TL.total * FPS)} fps={FPS} width={1080} height={1920}
      defaultProps={{ voice: null }} />
  </>
);
registerRoot(Root);
