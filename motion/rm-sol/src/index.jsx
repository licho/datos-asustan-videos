import { registerRoot, Composition } from "remotion";
import { Gancho } from "./Gancho.jsx";
import { HOOK } from "../../shared/art.mjs";

const Root = () => (
  <Composition id="Gancho" component={Gancho} durationInFrames={Math.round(HOOK.dur * 30)}
    fps={30} width={1080} height={1920} />
);
registerRoot(Root);
