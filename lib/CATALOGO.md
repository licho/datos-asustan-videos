# Catálogo de la librería (`lib/`)

Generado con `python3 -m lib.catalogo`. Para un video nuevo: copia un spec de `specs/`, cambia LINES/SCENES/SFX y usa `python3 -m lib.produce SPEC texto|preview|sinvoz|final VOZ.mp3`.

Escenarios: `lib/escenarios.py` (piso, rango de pies y zona libre de cada fondo; guía visual en `lib/escenarios.png`). Revisión automática: `python3 -m lib.produce SPEC check` (también corre sola antes de cada render).

Zonas seguras (1080x1920): letreros y=300/420 · acción 480–1320 · piso 1300 · subtítulos 1500 (no poner nada entre 1380 y 1640).


## lib.core

- `grad(top, bot)` — Fondo degradado (cacheado). Devuelve copia lista para dibujar.
- `canvas(bg)` — bg puede ser Image (se copia) o tupla de 2 colores (degradado).
- `bubble(d, x, y, text, size=52, tail=None, maxw=760, fill=WHITE, fg=BLK)` — Globo de diálogo centrado en (x,y). tail=(x,y) punta hacia quien habla (arriba o abajo).
- `calendar(d, cx, cy, day, label='DÍA', col=(240, 150, 40), sc=0.7)`
- `gauge(d, cx, cy, r, val, vmax, label, fg=WHITE)`
- `confetti(d, t, n=60, seed=7)`
- `speedlines(d, t, n=26, col=WHITE, y0=250, y1=1350, seed=2)`
- `sparkles(d, t, n=24, box=(80, 300, 1000, 1250), col=YEL, seed=3)`
- `follow_btn(d, lt, y=1250, delay=1.5, text='SÍGUEME')` — Botón SÍGUEME que aparece con rebote.
- `stamp(img, draw_fn, x, y, size=900, angle=0.0, flip=False, **kw)` — Dibuja cualquier personaje en una capa aparte y la pega rotada/volteada.
- `shake_arr(arr, t, amp)`

## lib.audio

- `lp(x, a)`
- `env(self, n, a=0.005, r=None)`
- `tone(self, f, d, w='sin')`
- `noise(self, d)`
- `add(self, st, sig, g=1.0, raw=False)`
- `pop(self, st, g=0.3, f0=300, f1=900, d=0.1)`
- `ding(self, st, g=0.2, f=1568)`
- `whoosh(self, st, g=0.35)`
- `buzzer(self, st, g=0.3)`
- `boing(self, st, g=0.3)`
- `thud(self, st, g=0.9)`
- `sting(self, st, g=0.4, d=2.0)`
- `jingle(self, st, g=0.12, notes=(523, 659, 784, 1047), gap=0.12)`
- `sadtrom(self, st, g=0.12)`
- `rumble(self, st, d=2.0, g=0.8)`
- `splat(self, st, g=0.6)`
- `skid(self, st, g=0.5)`
- `alarm(self, st, n=10, g=0.07)`
- `buzz(self, a, b, g=0.06, f0=220)`
- `whine(self, st, dur=1.5, g=0.07, f0=620)` — Zumbido de mosquito (agudo con vibrato), dur en segundos reales.
- `fx(self, name, st, **kw)`
- `music(self, style='bass', quiet=(), loud_from=None)` — style: bass | chiptune | pad | waltz. quiet=[(v0,v1)] silencios; loud_from=v sube volumen al final.
- `render(self, out_wav, voice_path=None)`
- `lp(x, a)`

## lib.personajes

- `alien_cw(d, x, y, s=1.0, t=0.0, mood='blank', arms='down', blink=False, antenna=True)` · reel15
- `alux(d, x, y, s=1.0, t=0.0, mood='grin', face=1, arm=None, shade=1.0)` · reel4 — Original cartoon alux: small Maya guardian in white clothes with embroidered border and red headband.
- `bacteria(d, x, y, s, t, kind='green', suitcase=False, shades=False)` · reel26
- `bear(d, x, y, big=2, kind='brown', frame=0, mood='normal')` · oso
- `bee(d, x, y, angry=False)` · mision003
- `blob(d, cx, cy, r, t)` · reel15
- `cat(d, x, y, s)` · reel17
- `cow(d, x, y, s)` · reel25
- `creature(d, cx, cy, r, t, mood='neutral', napkin=False)` · reel24
- `crouch_guy(d, x, y, s, t)` · reel13
- `cthulhu(d, x, y, s=1.0, t=0.0, eyes=1.0, wings=True, sleep=False, shade=1.0)` · reel3
- `dino(d, x, y, s, t, sign=None)` · reel13
- `doc(d, cx, cy, w, h, lines, t0, t, title=None)` · reel14
- `dog(d, x, y, s, t, kind=0, bow=False)` · reel17
- `doppel(d, x, y, s, t, mood='smile', glow=1.0, point=False)` · reel9
- `employee(d, x, y, s, t)` · reel8
- `face(d, cx, cy, r, mood='happy')` · reel23
- `fly(d, x, y, s, t, phase=0)` · reel12
- `germ(d, x, y, r, kind, t=0.0, phase=0.0, shade=1.0)` · reel2
- `guy(d, x, y, s=1.0, mood='neutral', arms='down', look=0.0, t=0.0, hoodie=(240, 120, 40))` · reel
- `hero_pixel(d, x, y, scared=False, frame=0, big=2)` · mision002
- `lion(d, x, y, s=1.0, t=0.0, mood='neutral')` · lib.animales — León sentado de frente; y = piso.
- `listeria(d, x, y, s, t)` · reel26
- `mite(d, x, y, s=1.0, t=0.0, phase=0.0, mood='grin', shade=1.0, dizzy=False)` · reel5
- `mold(d, cx, cy, r, k, t, seed=1)` · reel26
- `mosquito(d, x, y, s=1.0, t=0.0, flip=False, female=False, mask=False, hat=False, mood='normal', fly=True)` · lib.animales — Mosquito (patrón rayado tipo Aedes). mood: normal | angry | happy. Centro en el tórax.
- `person(d, cx, cy, s, col)` · reel2
- `president(d, x, y, s, t)` · reel24
- `roach(d, cx, cy, s, t, head=True, walk=True, wings=0.0, face='neutral', flip=False)` · reel27
- `roach_head(d, x, y, s, t, blink=True)` · reel27
- `scientist(d, x, y, s, t, mood='neutral')` · reel24
- `shark(d, x, y, s=1.0, t=0.0, flip=False, mood='neutral')` · lib.animales — Tiburón de lado. mood: neutral | cry | grin. Centro del cuerpo.
- `sick_guy(d, x, y, s, t)` · reel26
- `snake(d, x, y, s=1.0, t=0.0, flip=False, mood='neutral')` · lib.animales — Serpiente enroscada; y = piso.
- `soul(d, x, y, t, s=1.0)` · ofrenda
- `sponge(d, cx, cy, s, t=0.0, mood='smug', dirt=0.0, wet=0.0, sparkle=False)` · reel16
- `stamp_guy(img, x, y, s, ang, mood='scared', arms='up', t=0.0, hoodie=(240, 120, 40))` · reel25
- `swarm(d, cx, cy, t, n=24, spread=14, angry=False, seed=7)` · mision003
- `taquero(d, x, y, s, t, mood='neutral', arms='down')` · reel24
- `tentacle(d, x0, y0, length, ang, t, w0, col, phase=0.0, curl=1.0)` · reel3
- `vampire(d, x, y, s=1.0, t=0.0, mood='smug', outfit='cape', eyes_glow=0.0, arms='down', hat=None)` · reel14
- `wolf(d, x, y, s=1.0, t=0.0, mood='smug', outfit='shirt', arms='down', hat=None, howl=False)` · reel17
- `zomb(d, x, y, s=1.0, t=0.0, mood='blank', arms='out', outfit='office', hat=None, arm_off=False)` · reel18
- `zombie(d, x, y, s=1.0, t=0.0, face=-1, shade=1.0, glow=False)` · reel

## lib.props

- `asteroid(d, cx, cy, r, t=0.0, face='angry', fire=0.0, ang=-2.4)` · reel13
- `backpack(d, x, y, big=2, fill=0, closed=False)` · alien
- `balloons(d, x, y, t=0.0, n=3, s=1.0, seed=4, cols=((230, 60, 80), (60, 140, 230), (250, 200, 40), (120, 200, 90)))` · lib.objetos — Racimo de globos atado en (x, y).
- `banana(d, x, y, s, rot=0.0)` · reel12
- `bed(d, x, y, s=1.0, dirty=0.0)` · reel12
- `big_toilet(d, cx, base, s=1.0)` · reel7
- `blood_bag(d, x, y, s, col=(190, 20, 40), empty=False)` · reel14
- `boat(d, x, y, s=1.0, t=0.0, with_guy=True, mood='neutral', tilt=0.0)` · reel3
- `book(d, cx, cy, s)` · reel3
- `bottle(d, x, y, s)` · reel2
- `bucket(d, x, y, s=1.0, water=True, larvae=0.0, t=0.0)` · lib.objetos — Cubeta; y = piso.
- `building(d, x, y, w, h, col, rng, lit=False)` · reel25
- `bus(d, x, y, s)` · reel13
- `cactus(d, x, y, s=1)` · mision002
- `cake(d, x, y, s=1.0, t=0.0, text='')` · lib.objetos — Pastel con velas; y = base.
- `car(d, x, y, s, col)` · reel25
- `card(d, cx, cy, sc, label)` · reel
- `clock(d, cx, cy, r, t, ring=True)` · reel25
- `cloud(d, cx, cy, t)` · reel26
- `coffee_machine(d, x, y, s, t)` · reel8
- `corn(d, x, y, s)` · reel4
- `desk(d, x0, x1, y=None)` · reel15
- `earth(d, cx, cy, r)` · reel13
- `egg_raft(d, x, y, s=1.0, n=14)` · lib.objetos — Huevecillos (balsa de huevos) flotando.
- `flowerpot(d, x, y, s=1.0, water=True)` · lib.objetos — Maceta con plato de agua; y = piso.
- `freezer(d, x0, y1)` · reel
- `fruit(d, cx, ybot, col, fuzz=0.0, t=0.0, seed=1)` · reel26
- `garlic(d, cx, cy, r)` · reel14
- `glass(d, cx, ybot)` · reel27
- `heli(d, x, y, t)` · mision002
- `hive(d, x, y, t, shake=0.0)` · mision003
- `ice_machine(d, x, y, s, t, glow=1.0)` · reel8
- `icon(d, kind, cx, cy, k, t=0.0)` · reel
- `jar(d, x, ybot, text='MOSTAZA')` · reel26
- `jupiter(d, cx, cy, r, mood='neutral')` · reel23
- `keys(d, x, y, s, ang=0.0)` · reel4
- `land(d, flood=0.0)` · reel24
- `lettuce(d, cx, ybot, melt=0.0)` · reel26
- `magnifier(img, cx, cy, R, t, n_germs)` · reel2
- `meat(d, x, ybot)` · reel26
- `microwave(d, x, y)` · reel26
- `milk(d, x, ybot)` · reel26
- `mower(d, x, y, hx, hy, t)` · mision003
- `net(d, box, col=(255, 255, 255), step=26)` · lib.objetos — Mosquitero: rejilla dentro de box=(x0,y0,x1,y1).
- `offering(d, x, y, s)` · reel4
- `phone(d, cx, cy, s, glow=1.0)` · reel2
- `phone_small(d, x, y, s, glow=1.0, content=None)` · reel9
- `pie(d, cx, cy, r, frac, appear)` · reel12
- `pillow(d, cx, cy, s)` · reel12
- `pizza(d, cx, cy, s)` · reel2
- `plane(d, x, y, s)` · reel25
- `planet_earth(d, cx, cy, r, mood='happy')` · reel23
- `podium(d, cx, base, w=250, heights=(330, 230, 160), cols=((240, 190, 40), (190, 195, 205), (205, 130, 60)), appear=1.0)` · lib.objetos — Podio 1-2-3 (1 al centro, 2 izq, 3 der). Devuelve [(x, y_top)] en orden 1,2,3.
- `portal(d, cx, cy, r, t)` · reel24
- `pot(d, x, y, s, t)` · reel8
- `radar(d, cx, cy, rings, t=0.0)` · lib.objetos — rings=[(radio, texto, color, activo)] de mayor a menor.
- `rice_bowl(d, cx, ybot, s=1.0)` · reel26
- `salad(d, cx, ybot)` · reel26
- `sandal(d, cx, cy, s, ang=0.0)` · reel27
- `ship(d, x, y, s)` · reel13
- `shoe(d, x, y, s)` · reel12
- `skull(d, x, y, r=30, col=WHITE)` · lib.objetos — Calavera tipo ícono.
- `spin_earth(img, cx, cy, r, ang, mood='happy')` · reel25
- `spray(d, x, y, s=1.0, label='REPELENTE', t=0.0, mist=0.0)` · lib.objetos — Lata de spray; y = base.
- `street_sign(d, x, y, text)` · reel24
- `sun(d, cx, cy, r, t, mood='happy')` · reel23
- `table(d, cx, y, s)` · reel13
- `taco(d, x, y, s)` · reel24
- `tank(d, x, y, s, t)` · reel24
- `taper(d, x, y, w=360, h=170, lid=(60, 140, 220), food=(150, 80, 40), label=None)` · reel26
- `thermo(d, x, y, s, frac, label='45 °C')` · reel19
- `ticket(d, cx, cy, sc)` · reel19
- `tire(d, x, y, s=1.0, water=True)` · lib.objetos — Llanta tirada; y = piso.
- `toilet_seat(d, cx, cy, s=1.0, sparkle_t=None)` · reel2
- `trompo(d, x, y, s, t, k_pastor=1.0, pineapple=True)` · reel24
- `truck(d, x, y, s=1.0)` · reel8
- `ufo(d, x, y, big=1, t=0, beam=False, beam_h=120)` · alien
- `vacuum(d, cx, cy, s, t, ls)` · reel5
- `voyager(d, x, y, s=1.0)` · reel23
- `washer(d, cx, cy, s, t)` · reel5
- `wave(d, t, k)` · reel25
- `window_frame(d, x, y, w, h, broken=0.0)` · reel13

## lib.fondos

- `altar_pixel(d)` · ofrenda
- `city(snow=True, flash=0.0)` · reel13
- `desert_pixel(d, t, noon=False)` · mision002
- `desk_glow(img)` · reel2
- `forest_pixel(d, t)` · oso
- `garden_pixel(d, t)` · mision003
- `kitchen()` · reel16
- `make_bath()` · reel7
- `make_coldroom_in()` · reel
- `make_field()` · reel23
- `make_fridge(tint=(225, 238, 248))` · reel26
- `make_jungle()` · reel4
- `make_kitchen()` · reel27
- `make_milky()` · reel23
- `make_outside(w, h)` · reel
- `make_room(dark=False)` · reel9
- `make_sea()` · reel3
- `make_space()` · reel13
- `make_store()` · reel
- `make_street()` · reel9
- `moon(d, x, y, r)` · reel17
- `night(moon_on=True)` · reel17
- `night_room(lamp=True)` · reel14
- `office(night=False)` · reel15
- `outside_day(w, h)` · reel8
- `room(mess=0.0, dark=0.0, seed=1)` · reel12
- `skyline(d, y, s=1.0, col=(50, 40, 80))` · reel24
- `store_bg(t)` · reel14
- `store_day(t, zombies_at_door=True)` · reel8
- `town(d, lit, rng)` · reel25
