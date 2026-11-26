// Mundo 3D de "El turno de noche": edificio, recepción, pasillo del piso 8, elevador, guardias.
// Todo con figuras sencillas de Three.js (cajas, cilindros, cápsulas) y luces de terror.
import React, { useMemo, useLayoutEffect } from "react";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";

export const rnd = (i, s = 1) => { const x = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return x - Math.floor(x); };
const M = (color, extra = {}) => <meshStandardMaterial color={color} roughness={0.8} metalness={0.05} {...extra} />;
const Emit = (color, intensity = 1.5) => <meshStandardMaterial color={color} emissive={color} emissiveIntensity={intensity} toneMapped={false} />;

// ---------- Cámara controlada por la escena ----------
export function Cam({ pos, look, fov = 50, roll = 0 }) {
  // se aplica durante el render (antes de que Three dibuje el cuadro)
  const { camera } = useThree();
  camera.position.set(...pos);
  camera.up.set(Math.sin(roll), Math.cos(roll), 0);
  camera.lookAt(...look);
  camera.fov = fov; camera.near = 0.05; camera.far = 200;
  camera.updateProjectionMatrix();
  return null;
}

// ---------- Textura de lienzo dibujada en cada cuadro (pantallas, nota, cámaras) ----------
export function useCanvasTexture(w, h, draw, deps) {
  const { canvas, tex } = useMemo(() => {
    const canvas = document.createElement("canvas"); canvas.width = w; canvas.height = h;
    const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace;
    return { canvas, tex };
  }, [w, h]);
  const ctx = canvas.getContext("2d");
  draw(ctx, w, h);
  tex.needsUpdate = true;
  return tex;
}

// ---------- Guardia (uniforme azul marino, gorra) ----------
export function Guard({ position = [0, 0, 0], rotation = 0, pale = false, double = false, headUp = 1, sit = 0, walk = 0, t = 0, eyesGlow = 0 }) {
  const skin = pale ? "#d9d4cc" : "#e8b98f";
  const navy = "#1d2a4a";
  const sw = Math.sin(t * 8) * walk;
  const headTilt = (1 - headUp) * 0.75;
  const legY = sit ? 0.55 : 0.48;
  return (
    <group position={position} rotation={[0, rotation, 0]}>
      {/* piernas */}
      {sit ? (
        <>
          <mesh position={[-0.13, 0.55, 0.22]} rotation={[Math.PI / 2, 0, 0]} castShadow><capsuleGeometry args={[0.09, 0.38, 4, 10]} />{M("#121a30")}</mesh>
          <mesh position={[0.13, 0.55, 0.22]} rotation={[Math.PI / 2, 0, 0]} castShadow><capsuleGeometry args={[0.09, 0.38, 4, 10]} />{M("#121a30")}</mesh>
          <mesh position={[-0.13, 0.27, 0.45]} castShadow><capsuleGeometry args={[0.08, 0.38, 4, 10]} />{M("#121a30")}</mesh>
          <mesh position={[0.13, 0.27, 0.45]} castShadow><capsuleGeometry args={[0.08, 0.38, 4, 10]} />{M("#121a30")}</mesh>
        </>
      ) : (
        <>
          <mesh position={[-0.13, legY, 0]} rotation={[sw * 0.5, 0, 0]} castShadow><capsuleGeometry args={[0.09, 0.62, 4, 10]} />{M("#121a30")}</mesh>
          <mesh position={[0.13, legY, 0]} rotation={[-sw * 0.5, 0, 0]} castShadow><capsuleGeometry args={[0.09, 0.62, 4, 10]} />{M("#121a30")}</mesh>
        </>
      )}
      <group position={[0, sit ? 0.62 : 0.95, 0]}>
        {/* torso */}
        <mesh position={[0, 0.38, 0]} castShadow><capsuleGeometry args={[0.24, 0.42, 6, 14]} />{M(navy)}</mesh>
        <mesh position={[0, 0.14, 0]}><cylinderGeometry args={[0.25, 0.25, 0.07, 18]} />{M("#0b0b0e")}</mesh>
        <mesh position={[0.11, 0.55, 0.22]}><boxGeometry args={[0.08, 0.1, 0.02]} />{M("#d4af37", { metalness: 0.8, roughness: 0.3 })}</mesh>
        <mesh position={[-0.1, 0.55, 0.225]}><boxGeometry args={[0.12, 0.03, 0.02]} />{M("#ffffff")}</mesh>
        {/* brazos */}
        <mesh position={[-0.32, 0.32, 0]} rotation={[sit ? -0.9 : -sw * 0.4, 0, 0.12]} castShadow><capsuleGeometry args={[0.075, 0.45, 4, 10]} />{M(navy)}</mesh>
        <mesh position={[0.32, 0.32, 0]} rotation={[sit ? -0.9 : sw * 0.4, 0, -0.12]} castShadow><capsuleGeometry args={[0.075, 0.45, 4, 10]} />{M(navy)}</mesh>
        {/* cabeza */}
        <group position={[0, 0.78, 0]} rotation={[headTilt, 0, 0]}>
          <mesh castShadow><sphereGeometry args={[0.2, 24, 18]} />{M(skin)}</mesh>
          <mesh position={[0, 0.12, 0]}><cylinderGeometry args={[0.205, 0.21, 0.12, 22]} />{M(navy)}</mesh>
          <mesh position={[0, 0.07, 0.17]} rotation={[0.25, 0, 0]}><boxGeometry args={[0.3, 0.02, 0.16]} />{M("#0d1428")}</mesh>
          <mesh position={[-0.07, 0.0, 0.18]}><sphereGeometry args={[0.025, 10, 8]} />{eyesGlow > 0 ? Emit("#d9fff2", 2 * eyesGlow) : M("#111")}</mesh>
          <mesh position={[0.07, 0.0, 0.18]}><sphereGeometry args={[0.025, 10, 8]} />{eyesGlow > 0 ? Emit("#d9fff2", 2 * eyesGlow) : M("#111")}</mesh>
          <mesh position={[0, -0.03, 0.195]}><sphereGeometry args={[0.03, 10, 8]} />{M(pale ? "#cfc6bc" : "#d9a27a")}</mesh>
          <mesh position={[-0.07, 0.05, 0.175]} rotation={[0, 0, pale ? 0.35 : 0.1]}><boxGeometry args={[0.07, 0.014, 0.01]} />{M("#2a1d16")}</mesh>
          <mesh position={[0.07, 0.05, 0.175]} rotation={[0, 0, pale ? -0.35 : -0.1]}><boxGeometry args={[0.07, 0.014, 0.01]} />{M("#2a1d16")}</mesh>
          <mesh position={[0, -0.1, 0.17]}>{pale ? <sphereGeometry args={[0.022, 10, 8]} /> : <boxGeometry args={[0.07, 0.012, 0.01]} />}{M("#4a2a2a")}</mesh>
          {pale && <><mesh position={[-0.07, -0.025, 0.175]}><boxGeometry args={[0.05, 0.012, 0.005]} />{M("#8a7a90")}</mesh>
            <mesh position={[0.07, -0.025, 0.175]}><boxGeometry args={[0.05, 0.012, 0.005]} />{M("#8a7a90")}</mesh></>}
        </group>
      </group>
    </group>
  );
}

// ---------- Exterior: edificio de oficinas de noche ----------
export function Building({ t }) {
  const wins = [];
  for (let fl = 0; fl < 12; fl++) for (let c = 0; c < 7; c++) {
    const on = rnd(fl * 7 + c, 4) > 0.86 || (fl === 7 && c === 3);
    const flick = fl === 7 && c === 3 ? 0.6 + 0.4 * Math.abs(Math.sin(t * 13)) : 1;
    wins.push(<mesh key={`${fl}-${c}`} position={[-3 + c, 1.6 + fl * 1.15, 5.01]}><planeGeometry args={[0.7, 0.75]} />
      {on ? Emit(fl === 7 && c === 3 ? "#9fffd0" : "#ffd89a", 1.2 * flick) : M("#0e1420", { roughness: 0.2, metalness: 0.6 })}</mesh>);
  }
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[80, 80]} />{M("#191c24")}</mesh>
      <mesh position={[0, 0.06, 7.5]} receiveShadow><boxGeometry args={[30, 0.12, 4]} />{M("#2a2e38")}</mesh>
      <mesh position={[0, 7.5, 0]} castShadow receiveShadow><boxGeometry args={[8, 15, 10]} />{M("#2b3140")}</mesh>
      {wins}
      <mesh position={[0, 1.1, 5.02]}><planeGeometry args={[2.2, 2.2]} />{Emit("#7f9cc0", 0.22)}</mesh>
      <mesh position={[0, 2.35, 5.3]}><boxGeometry args={[2.8, 0.12, 0.8]} />{M("#1a1e28")}</mesh>
      {[-6, 6].map(x => (
        <group key={x} position={[x, 0, 8.6]}>
          <mesh position={[0, 2.2, 0]}><cylinderGeometry args={[0.06, 0.08, 4.4, 10]} />{M("#333")}</mesh>
          <mesh position={[0, 4.4, 0]}><sphereGeometry args={[0.22, 14, 10]} />{Emit("#ffcf8a", 2)}</mesh>
          <pointLight position={[0, 4.2, 0]} intensity={60} distance={16} decay={1.6} color="#ffbf70" />
        </group>
      ))}
      <mesh position={[9, 22, -30]}><sphereGeometry args={[2.2, 24, 18]} />{Emit("#e9eef8", 1.2)}</mesh>
      <pointLight position={[0, 1.4, 6.5]} intensity={9} distance={10} decay={1.6} color="#cfe8ff" />
      <directionalLight position={[10, 25, 20]} intensity={0.6} color="#9fb4ff" />
    </group>
  );
}

// ---------- Recepción con escritorio, monitores, silla ----------
export function Reception({ t, screens, chairGuard = null, mugSteam = 1, keyboardLift = 0, intercom = 0, lightsFlicker = 0 }) {
  const fl = lightsFlicker ? (Math.sin(t * 37) > 0.75 ? 0.3 : 1) : 1;
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[30, 30]} />{M("#2c3038")}</mesh>
      <mesh position={[0, 2.2, -3.2]} receiveShadow><boxGeometry args={[14, 4.4, 0.2]} />{M("#3a3f4a")}</mesh>
      <mesh position={[-5, 2.2, 1]} rotation={[0, Math.PI / 2, 0]}><boxGeometry args={[10, 4.4, 0.2]} />{M("#343944")}</mesh>
      <mesh position={[0, 4.4, 0]} rotation={[Math.PI / 2, 0, 0]}><planeGeometry args={[30, 30]} />{M("#1b1e24")}</mesh>
      {/* lámparas del techo */}
      {[-2, 2].map((x, i) => (
        <group key={x}>
          <mesh position={[x, 4.38, -0.5]}><boxGeometry args={[1.6, 0.04, 0.4]} />{Emit("#dff3ff", 1.4 * (i === 1 ? fl : 1))}</mesh>
          <pointLight position={[x, 4.1, -0.5]} intensity={45 * (i === 1 ? fl : 1)} distance={14} decay={1.5} color="#cfe6ff" castShadow={i === 0} />
        </group>
      ))}
      {/* escritorio */}
      <mesh position={[0, 0.5, -1.5]} castShadow receiveShadow><boxGeometry args={[3.4, 1.0, 1.0]} />{M("#4a3a2e")}</mesh>
      <mesh position={[0, 1.02, -1.5]} receiveShadow><boxGeometry args={[3.6, 0.06, 1.2]} />{M("#6b5442")}</mesh>
      {/* monitores 3x2 */}
      {[0, 1, 2, 3, 4, 5].map(i => {
        const x = -0.95 + (i % 3) * 0.95, y = 1.42 + Math.floor(i / 3) * 0.62;
        return (
          <group key={i} position={[x, y, -1.85]}>
            <mesh castShadow><boxGeometry args={[0.9, 0.58, 0.08]} />{M("#111")}</mesh>
            <mesh position={[0, 0, 0.045]}><planeGeometry args={[0.82, 0.5]} />
              {screens && screens[i] ? <meshStandardMaterial map={screens[i]} emissiveMap={screens[i]} emissive="#ffffff" emissiveIntensity={0.9} toneMapped={false} /> : M("#05070a")}
            </mesh>
          </group>
        );
      })}
      <pointLight position={[0, 1.7, -1.1]} intensity={screens ? 8 : 0} distance={4} decay={1.5} color="#9fffd0" />
      {/* teclado */}
      <group position={[0, 1.06 + keyboardLift * 0.18, -1.15]} rotation={[-keyboardLift * 0.5, 0, 0]}>
        <mesh castShadow><boxGeometry args={[0.7, 0.04, 0.22]} />{M("#202226")}</mesh>
        {[...Array(24)].map((_, k) => <mesh key={k} position={[-0.3 + (k % 12) * 0.055, 0.025, -0.05 + Math.floor(k / 12) * 0.08]}><boxGeometry args={[0.04, 0.015, 0.05]} />{M("#3a3c42")}</mesh>)}
      </group>
      {/* taza de café */}
      <group position={[1.1, 1.05, -1.2]}>
        <mesh castShadow><cylinderGeometry args={[0.07, 0.06, 0.15, 18]} />{M("#e9e4dc")}</mesh>
        <mesh position={[0.085, 0.01, 0]} rotation={[0, 0, Math.PI / 2]}><torusGeometry args={[0.04, 0.012, 8, 14]} />{M("#e9e4dc")}</mesh>
        {mugSteam > 0 && [0, 1, 2, 3].map(k => {
          const p = (t * 0.5 + k / 4) % 1;
          return <mesh key={k} position={[Math.sin(t * 2 + k) * 0.03, 0.1 + p * 0.35, 0]}><sphereGeometry args={[0.025 + p * 0.04, 8, 6]} /><meshStandardMaterial color="#ffffff" transparent opacity={(1 - p) * 0.35 * mugSteam} /></mesh>;
        })}
      </group>
      {/* silla de seguridad */}
      <group position={[0, 0, -0.2]}>
        <mesh position={[0, 0.5, 0]} castShadow><boxGeometry args={[0.6, 0.1, 0.55]} />{M("#15161a")}</mesh>
        <mesh position={[0, 0.95, 0.27]} castShadow><boxGeometry args={[0.58, 0.8, 0.08]} />{M("#15161a")}</mesh>
        <mesh position={[0, 0.25, 0]}><cylinderGeometry args={[0.04, 0.04, 0.45, 10]} />{M("#555")}</mesh>
        {[0, 1, 2, 3, 4].map(k => <mesh key={k} position={[Math.cos(k * 1.257) * 0.25, 0.04, Math.sin(k * 1.257) * 0.25]} rotation={[0, -k * 1.257, 0]}><boxGeometry args={[0.5, 0.04, 0.05]} />{M("#444")}</mesh>)}
        {chairGuard}
      </group>
      {/* intercomunicador en la pared lateral */}
      <group position={[-4.88, 1.7, -1.6]} rotation={[0, Math.PI / 2, 0]}>
        <mesh><boxGeometry args={[0.45, 0.6, 0.08]} />{M("#9aa0a8", { metalness: 0.5, roughness: 0.4 })}</mesh>
        {[...Array(5)].map((_, k) => <mesh key={k} position={[0, 0.12 - k * 0.05, 0.045]}><boxGeometry args={[0.3, 0.015, 0.01]} />{M("#333")}</mesh>)}
        <mesh position={[0.14, -0.2, 0.05]}><sphereGeometry args={[0.03, 10, 8]} />{intercom > 0 ? Emit("#ff2a2a", 3 * intercom) : M("#401010")}</mesh>
        {intercom > 0 && <pointLight position={[0, 0, 0.4]} intensity={2 * intercom} distance={2} color="#ff3030" />}
      </group>
      {/* paredes del frente y derecha */}
      <mesh position={[0, 2.2, 5.2]}><boxGeometry args={[14, 4.4, 0.2]} />{M("#363b46")}</mesh>
      <mesh position={[5.2, 2.2, 1]} rotation={[0, Math.PI / 2, 0]}><boxGeometry args={[10, 4.4, 0.2]} />{M("#30353f")}</mesh>
      {/* entrada de vidrio con la calle oscura */}
      <mesh position={[0, 1.5, 5.08]}><planeGeometry args={[3.2, 3]} />{M("#0b1220", { roughness: 0.1, metalness: 0.7 })}</mesh>
      {[-1.6, 0, 1.6].map(x => <mesh key={x} position={[x, 1.5, 5.0]}><boxGeometry args={[0.08, 3, 0.08]} />{M("#8a9099", { metalness: 0.8 })}</mesh>)}
      <mesh position={[0, 3.25, 5.0]}><boxGeometry args={[0.7, 0.22, 0.05]} />{Emit("#39ff7a", 1.2)}</mesh>
      <pointLight position={[0, 3.1, 4.6]} intensity={4} distance={4} color="#39ff7a" />
      {/* sillón de espera y planta */}
      <group position={[3.6, 0, 3]} rotation={[0, -Math.PI / 2, 0]}>
        <mesh position={[0, 0.3, 0]} castShadow><boxGeometry args={[2, 0.4, 0.8]} />{M("#3d2f2a")}</mesh>
        <mesh position={[0, 0.75, -0.32]} castShadow><boxGeometry args={[2, 0.6, 0.18]} />{M("#3d2f2a")}</mesh>
      </group>
      <group position={[-4.2, 0, 4.3]}>
        <mesh position={[0, 0.3, 0]}><cylinderGeometry args={[0.28, 0.22, 0.6, 16]} />{M("#5a4a3a")}</mesh>
        {[0, 1, 2, 3, 4].map(k => <mesh key={k} position={[Math.cos(k * 1.3) * 0.2, 1.0 + k * 0.08, Math.sin(k * 1.3) * 0.2]} rotation={[0.4, k * 1.3, 0.3]}><sphereGeometry args={[0.28, 10, 8]} />{M("#2f5a35")}</mesh>)}
      </group>
      {/* reloj de pared */}
      <group position={[2.6, 3.0, -3.08]}>
        <mesh rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.32, 0.32, 0.05, 24]} />{M("#e8e4da")}</mesh>
        <mesh position={[0, 0.08, 0.04]} rotation={[0, 0, -0.4]}><boxGeometry args={[0.03, 0.2, 0.01]} />{M("#111")}</mesh>
        <mesh position={[0.06, -0.08, 0.04]} rotation={[0, 0, 2.5]}><boxGeometry args={[0.02, 0.26, 0.01]} />{M("#111")}</mesh>
      </group>
      {/* puerta del fondo */}
      <mesh position={[4.2, 1.5, -3.05]}><boxGeometry args={[1.8, 3, 0.05]} /><meshStandardMaterial color="#9fc4e0" transparent opacity={0.25} metalness={0.9} roughness={0.05} /></mesh>
    </group>
  );
}

// ---------- Pasillo del piso 8 con elevador al fondo ----------
export function Corridor({ t, doorsOpen = 0, button8 = 0, figure = null, flicker = 1 }) {
  const lights = [];
  for (let k = 0; k < 6; k++) {
    const z = -k * 4;
    const on = k === 3 ? (Math.sin(t * 23 + 1) > 0.2 ? 1 : 0.15) * flicker : 1;
    lights.push(<group key={k}><mesh position={[0, 3.18, z]}><boxGeometry args={[0.5, 0.04, 1.6]} />{Emit("#e6f4ff", 1.3 * on)}</mesh>
      <pointLight position={[0, 2.9, z]} intensity={22 * on} distance={8} decay={1.5} color="#cfe6ff" /></group>);
  }
  const doors = [];
  for (let k = 0; k < 5; k++) for (const side of [-1, 1]) doors.push(
    <group key={`${k}${side}`} position={[side * 1.79, 1.1, -2 - k * 4]} rotation={[0, -side * Math.PI / 2, 0]}>
      <mesh><boxGeometry args={[1.0, 2.2, 0.06]} />{M("#5a4636")}</mesh>
      <mesh position={[0.36, 0, 0.05]}><sphereGeometry args={[0.04, 8, 6]} />{M("#c9b37a", { metalness: 0.8, roughness: 0.3 })}</mesh>
      <mesh position={[0, 0.85, 0.04]}><planeGeometry args={[0.28, 0.14]} />{M("#e8e2d0")}</mesh>
    </group>);
  const d = doorsOpen * 0.62;
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -10]} receiveShadow><planeGeometry args={[3.6, 26]} />{M("#4a4d52")}</mesh>
      {[-1.8, 1.8].map(x => <mesh key={x} position={[x, 1.6, -10]}><boxGeometry args={[0.1, 3.2, 26]} />{M("#5d6670")}</mesh>)}
      <mesh position={[0, 3.2, -10]} rotation={[Math.PI / 2, 0, 0]}><planeGeometry args={[3.6, 26]} />{M("#2a2d33")}</mesh>
      {lights}{doors}
      {/* elevador al fondo */}
      <group position={[0, 0, -22]}>
        <mesh position={[-1.25, 1.6, -0.05]}><boxGeometry args={[1.1, 3.2, 0.1]} />{M("#4b5059")}</mesh>
        <mesh position={[1.25, 1.6, -0.05]}><boxGeometry args={[1.1, 3.2, 0.1]} />{M("#4b5059")}</mesh>
        <mesh position={[0, 2.75, -0.05]}><boxGeometry args={[1.4, 0.9, 0.1]} />{M("#4b5059")}</mesh>
        <mesh position={[0, 1.15, -0.9]}><boxGeometry args={[1.4, 2.3, 1.6]} /><meshStandardMaterial color="#c8c0a8" emissive="#fff1c8" emissiveIntensity={0.08 * doorsOpen} side={THREE.BackSide} /></mesh>
        {doorsOpen > 0 && <pointLight position={[0, 2.0, -0.8]} intensity={7 * doorsOpen} distance={5} decay={1.5} color="#fff0c8" />}
        <mesh position={[-0.35 - d, 1.15, 0.03]}><boxGeometry args={[0.7, 2.3, 0.05]} />{M("#9aa0a8", { metalness: 0.7, roughness: 0.3 })}</mesh>
        <mesh position={[0.35 + d, 1.15, 0.03]}><boxGeometry args={[0.7, 2.3, 0.05]} />{M("#9aa0a8", { metalness: 0.7, roughness: 0.3 })}</mesh>
        <mesh position={[0, 2.5, 0.04]}><planeGeometry args={[0.5, 0.18]} />{Emit("#ff5a2a", 1)}</mesh>
        {/* botonera dentro del elevador */}
        <group position={[0.55, 1.2, -0.6]} rotation={[0, -Math.PI / 2, 0]}>
          <mesh><boxGeometry args={[0.3, 0.6, 0.03]} />{M("#777", { metalness: 0.7 })}</mesh>
          {[...Array(10)].map((_, k) => <mesh key={k} position={[(k % 2) * 0.12 - 0.06, 0.22 - Math.floor(k / 2) * 0.1, 0.02]}><circleGeometry args={[0.03, 14]} />
            {k === 7 && button8 > 0 ? Emit("#ffb03a", 3 * button8) : M("#ddd")}</mesh>)}
        </group>
      </group>
      {figure}
    </group>
  );
}

// Lluvia de polvo en el aire (motas que flotan con la luz)
export function Dust({ t, n = 60, center = [0, 1.6, -4], spread = [3, 2.5, 6] }) {
  return <group>{[...Array(n)].map((_, i) => (
    <mesh key={i} position={[center[0] + (rnd(i, 1) - 0.5) * spread[0] + Math.sin(t * 0.3 + i) * 0.1,
      center[1] + (rnd(i, 2) - 0.5) * spread[1] + Math.sin(t * 0.2 + i * 2) * 0.15, center[2] + (rnd(i, 3) - 0.5) * spread[2]]}>
      <sphereGeometry args={[0.008 + rnd(i, 4) * 0.008, 5, 4]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.35} />
    </mesh>))}</group>;
}
