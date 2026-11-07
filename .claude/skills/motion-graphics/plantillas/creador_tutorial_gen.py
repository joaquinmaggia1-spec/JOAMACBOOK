import sys, os

P = sys.argv[1]
CUT = os.path.exists(os.path.join(P, "assets/v/hook_cut.webm"))

# tiempos raíz de cada bloque
T_HOOK, T_SPLIT, T_EST, T_REM, T_OUT = 0.0, 4.0, 9.47, 11.03, 16.43
DUR = 19.43
YEL, LEMON = "#FFD60A", "#EEF25A"

# subtítulos palabra por palabra: (texto, inicio, fin, top_px)
caps = []
def add(block_start, items, top):
    for txt, s, e in items:
        caps.append((txt, round(block_start + s, 3), round(block_start + e, 3), top))

add(T_SPLIT, [("PRIMERO", 0.08, 0.56), ("NO PAGUES", 1.12, 1.58), ("LA CUOTA", 1.58, 2.04),
              ("NOMÁS", 2.04, 2.50), ("VENÍ AL", 2.50, 2.96), ("GIMNASIO", 2.96, 3.50),
              ("HACÉ", 3.50, 3.98), ("ESO TE", 4.24, 4.68), ("LO DIJO", 4.68, 5.14)], 572)
add(T_EST, [("NECESITAMOS", 0.0, 0.46), ("SÍ O SÍ", 0.46, 1.56)], 1420)
add(T_REM, [("¿CUÁNTAS", 0.12, 0.57), ("PLATAFORMAS", 0.57, 1.02), ("ESTÁS PAGANDO?", 1.02, 1.97),
            ("VENÍ A", 1.97, 2.42), ("ENTRENAR", 2.42, 2.92), ("HERMANO", 3.09, 3.70)], 1440)

cap_html = "\n".join(
    f'<div class="cap" id="cap{i}" style="top:{top}px">{t}</div>' for i, (t, s, e, top) in enumerate(caps))
cap_js = "\n".join(
    f'pop("#cap{i}", {s}, {e});' for i, (t, s, e, top) in enumerate(caps))

# efectos de sonido: (archivo, inicio, volumen)
sfx = [("impact-bass-1", 0.00, 0.45), ("whoosh-short", 0.85, 0.5), ("pop", 2.92, 0.5),
       ("whoosh-short", 3.80, 0.55), ("impact-bass-2", 4.56, 0.4), ("sparkle", 7.70, 0.35),
       ("whoosh-short", 9.30, 0.5), ("pop", 10.42, 0.55), ("whoosh-short", 10.86, 0.5),
       ("click-soft", 11.62, 0.5), ("click-soft", 11.86, 0.5), ("click-soft", 12.10, 0.5),
       ("sparkle", 13.52, 0.35), ("impact-bass-1", 14.10, 0.4), ("whoosh-short", 16.25, 0.5),
       ("pop", 16.62, 0.5)]
durs = {"impact-bass-1": 2.11, "impact-bass-2": 2.59, "whoosh-short": 0.57, "pop": 0.72,
        "sparkle": 1.80, "click-soft": 0.36}
sfx_html = "\n".join(
    f'<audio id="sfx{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{s}" data-duration="{durs[f]}" '
    f'data-volume="{v}" data-track-index="{20 + i}"></audio>' for i, (f, s, v) in enumerate(sfx))

cut_html = (f'<video id="hook-cut" class="clip" src="assets/v/hook_cut.webm" data-start="0" data-duration="4" '
            f'data-media-start="0" muted playsinline data-track-index="3"></video>') if CUT else ""

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Anton"; src: url("assets/fonts/anton.woff2") format("woff2"); }}
@font-face {{ font-family: "Bebas Neue"; src: url("assets/fonts/bebas.woff2") format("woff2"); }}
@font-face {{ font-family: "Playfair Display"; font-style: italic; font-weight: 900; src: url("assets/fonts/playfair-900i.woff2") format("woff2"); }}
@font-face {{ font-family: "Playfair Display"; font-style: italic; font-weight: 700; src: url("assets/fonts/playfair-700i.woff2") format("woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
.wrap {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
/* gancho */
#t-5 {{ position: absolute; left: 0; right: 0; top: 90px; text-align: center; font-family: "Anton"; font-size: 270px;
        line-height: .98; color: {YEL}; letter-spacing: -2px; z-index: 2; text-shadow: 0 10px 40px rgba(0,0,0,.25); }}
#t-5 span {{ display: block; }}
#t-5a {{ font-size: 360px; }}
#t-para {{ position: absolute; left: 0; right: 0; top: 1205px; text-align: center; z-index: 5;
          font-family: "Playfair Display"; font-style: italic; font-weight: 700; font-size: 58px; color: {YEL};
          text-shadow: 0 3px 14px rgba(0,0,0,.55); }}
#t-masa {{ position: absolute; left: 0; right: 0; top: 1290px; text-align: center; z-index: 5;
          font-family: "Playfair Display"; font-style: italic; font-weight: 900; font-size: 168px; line-height: .92;
          background: linear-gradient(180deg, #ffffff 0%, #ffffff 45%, #b9c0cc 100%); -webkit-background-clip: text;
          background-clip: text; color: transparent; filter: drop-shadow(0 8px 22px rgba(0,0,0,.55)); }}
#t-masa span {{ display: block; }}
/* split */
#split-top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 630px; overflow: hidden; z-index: 1; }}
#split-top video {{ position: absolute; left: 0; top: -110px; width: 1080px; height: 1920px; object-fit: cover; }}
#split-bot {{ position: absolute; left: 0; top: 630px; width: 1080px; height: 1290px; overflow: hidden; z-index: 1; }}
#split-bot video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1290px; object-fit: cover; }}
#seam {{ position: absolute; left: 0; top: 627px; width: 1080px; height: 6px; background: #000; z-index: 2; }}
#pill {{ position: absolute; left: 60px; top: 700px; z-index: 6; padding: 14px 30px; border-radius: 999px; background: {YEL};
        font-family: "Bebas Neue"; font-size: 52px; letter-spacing: 3px; color: #111; }}
#t-profe {{ position: absolute; left: 0; right: 0; top: 1060px; text-align: center; z-index: 6; font-family: "Anton"; font-size: 200px; line-height: 1; color: {YEL}; text-shadow: 0 10px 40px rgba(0,0,0,.45); }}
#t-entrena {{ position: absolute; left: 0; right: 0; top: 1010px; text-align: center; z-index: 6; font-family: "Anton";
             font-size: 250px; line-height: 1; color: {YEL}; text-shadow: 0 10px 40px rgba(0,0,0,.45); }}
.quote {{ position: absolute; left: 0; right: 0; text-align: center; z-index: 6; font-family: "Playfair Display";
          font-style: italic; font-weight: 900; color: {LEMON}; line-height: 1;
          text-shadow: 0 0 30px rgba(238,242,90,.55), 0 8px 24px rgba(0,0,0,.6); }}
#q-fuerza {{ top: 1130px; font-size: 230px; }}
#q-estimulo {{ top: 1080px; font-size: 200px; }}
#q-barato {{ top: 1010px; font-size: 190px; }}
/* captions */
.cap {{ position: absolute; left: 0; right: 0; text-align: center; z-index: 8; font-family: "Bebas Neue"; font-size: 112px;
        line-height: 1; color: #fff; letter-spacing: 2px; text-shadow: 0 4px 0 rgba(0,0,0,.35), 0 6px 26px rgba(0,0,0,.65); opacity: 0; }}
/* chips de suscripciones */
.chip {{ position: absolute; right: 70px; z-index: 6; padding: 22px 34px; border-radius: 26px; background: rgba(15,15,20,.62);
         border: 2px solid rgba(255,255,255,.28); font-family: "Bebas Neue"; font-size: 64px; letter-spacing: 2px; color: #fff; }}
.chip b {{ color: {YEL}; font-weight: 400; }}
/* cta */
#cta-a {{ position: absolute; left: 0; right: 0; top: 760px; text-align: center; z-index: 6; font-family: "Anton"; font-size: 220px;
          line-height: 1; color: {YEL}; text-shadow: 0 10px 40px rgba(0,0,0,.45); }}
#cta-b {{ position: absolute; left: 0; right: 0; top: 1010px; text-align: center; z-index: 6; font-family: "Playfair Display";
          font-style: italic; font-weight: 900; font-size: 92px; color: #fff; text-shadow: 0 6px 22px rgba(0,0,0,.6); }}
/* marca de agua */
#wm {{ position: absolute; left: 950px; top: 470px; width: 62px; height: 62px; z-index: 7; opacity: .95; }}
/* cierre */
#outro {{ position: absolute; inset: 0; background: #000; z-index: 9; opacity: 0; }}
#ig-c {{ position: absolute; left: 400px; top: 700px; width: 280px; height: 280px; }}
#outro-t {{ position: absolute; left: 0; right: 0; top: 1040px; text-align: center; font-family: "Bebas Neue"; font-size: 70px;
            letter-spacing: 6px; color: #fff; }}
#outro-s {{ position: absolute; left: 0; right: 0; top: 1125px; text-align: center; font-family: "Playfair Display";
            font-style: italic; font-weight: 700; font-size: 56px; color: {YEL}; }}
/* light leak + flash */
#leak {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; mix-blend-mode: screen; opacity: .75;
         background: radial-gradient(60% 40% at 15% 20%, rgba(255,150,60,.95), rgba(255,120,40,0) 70%),
                     radial-gradient(50% 35% at 90% 75%, rgba(255,230,180,.9), rgba(255,200,120,0) 70%); }}
#flash {{ position: absolute; inset: 0; z-index: 11; background: #fff; opacity: 0; pointer-events: none; }}
/* estados iniciales ocultos (el título del gancho se ve desde el frame 0) */
#t-para, #t-masa span, #pill, #t-profe, #t-entrena, .quote, .chip, #cta-a, #cta-b {{ opacity: 0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">

  <!-- 1. gancho: título detrás de la persona -->
  <div class="wrap" id="hook-w" style="z-index:1">
    <video id="hook" class="clip full" src="assets/v/hook.mp4" data-start="0" data-duration="4" data-media-start="0"
           playsinline data-has-audio="true" data-volume="1" data-track-index="1"></video>
  </div>
  <div id="t-5" data-layout-ignore><span id="t-5a">5</span><span id="t-5b">PILARES</span></div>
  <div class="wrap" id="cut-w" style="z-index:3; pointer-events:none">{cut_html}</div>
  <div id="t-para">para el desarrollo de la</div>
  <div id="t-masa"><span id="m1">masa</span><span id="m2">muscular</span></div>

  <!-- 2. pilar 1: pantalla dividida -->
  <div id="split-top">
    <video id="profe" class="clip" src="assets/v/profe.mp4" data-start="{T_SPLIT}" data-duration="5.47"
           playsinline data-has-audio="true" data-volume="1" data-track-index="4" data-layout-ignore></video>
  </div>
  <div id="split-bot">
    <video id="flex" class="clip" src="assets/v/flexiones.mp4" data-start="{T_SPLIT}" data-duration="5.47"
           muted playsinline data-track-index="5" data-layout-ignore></video>
  </div>
  <div id="seam" class="clip" data-start="{T_SPLIT}" data-duration="5.47" data-track-index="6"></div>
  <div id="pill">PILAR 01</div>
  <div id="t-entrena">ENTRENÁ</div>
  <div id="q-fuerza" class="quote">“fuerza”</div>
  <div id="t-profe">TU PROFE</div>

  <!-- 3. estímulo -->
  <div class="wrap" id="est-w" style="z-index:1">
    <video id="est" class="clip full" src="assets/v/estimulo.mp4" data-start="{T_EST}" data-duration="1.56"
           playsinline data-has-audio="true" data-volume="1" data-track-index="7"></video>
  </div>
  <div id="q-estimulo" class="quote">“estímulo”</div>

  <!-- 4. remate -->
  <div class="wrap" id="rem-w" style="z-index:1">
    <video id="rem" class="clip full" src="assets/v/remate.mp4" data-start="{T_REM}" data-duration="5.4"
           playsinline data-has-audio="true" data-volume="1" data-track-index="8"></video>
  </div>
  <div class="chip" id="chip1" style="top:820px">SUSCRIPCIÓN <b>$9.990</b></div>
  <div class="chip" id="chip2" style="top:950px">SUSCRIPCIÓN <b>$9.990</b></div>
  <div class="chip" id="chip3" style="top:1080px">SUSCRIPCIÓN <b>$9.990</b></div>
  <div id="q-barato" class="quote">“más barato”</div>
  <div id="cta-a">PILAR 02</div>
  <div id="cta-b">en el próximo video</div>

  <!-- subtítulos palabra por palabra -->
  {cap_html}

  <img id="wm" src="assets/logos/instagram.svg" alt="" data-layout-ignore />

  <!-- 5. cierre -->
  <div id="outro">
    <img id="ig-c" src="assets/logos/instagram_c.svg" alt="" />
    <div id="outro-t">SEGUIME</div>
    <div id="outro-s">los 5 pilares, uno por video</div>
  </div>

  <div id="leak" data-layout-ignore></div>
  <div id="flash" data-layout-ignore></div>

  {sfx_html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
function pop(sel, s, e) {{
  tl.fromTo(sel, {{ opacity: 0, scale: 1.12 }}, {{ opacity: 1, scale: 1, duration: 0.08, ease: "power3.out" }}, s);
  tl.to(sel, {{ opacity: 0, duration: 0.04 }}, e - 0.04);
}}
function cut(t) {{
  tl.to("#flash", {{ opacity: 0.55, duration: 0.05 }}, t - 0.05);
  tl.to("#flash", {{ opacity: 0, duration: 0.12 }}, t);
  tl.to("#leak", {{ opacity: 0.8, duration: 0.12 }}, t - 0.08);
  tl.to("#leak", {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, t + 0.05);
}}

// 1. gancho
tl.to("#leak", {{ opacity: 0, duration: 0.7, ease: "power2.out" }}, 0.02);
tl.fromTo("#hook-w", {{ scale: 1.0 }}, {{ scale: 1.06, duration: 4, ease: "none" }}, 0);
tl.fromTo("#t-5a", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.2, ease: "power3.out" }}, 0.22);
tl.fromTo("#t-5b", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.16, ease: "power3.out" }}, 0.9);
tl.fromTo("#t-para", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.18 }}, 1.58);
tl.fromTo("#m1", {{ opacity: 0, scale: 1.2 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power3.out" }}, 2.94);
tl.fromTo("#m2", {{ opacity: 0, scale: 1.2 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power3.out" }}, 3.28);
tl.to(["#t-5", "#t-para", "#t-masa"], {{ opacity: 0, duration: 0.04 }}, 3.96);

// 2. pilar 1
cut({T_SPLIT});
tl.fromTo("#pill", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out" }}, {T_SPLIT} + 0.05);
tl.to("#pill", {{ opacity: 0, duration: 0.04 }}, {T_EST} - 0.05);
tl.fromTo("#t-entrena", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power3.out" }}, {T_SPLIT} + 0.56);
tl.to("#t-entrena", {{ opacity: 0, duration: 0.15 }}, {T_SPLIT} + 1.75);
tl.fromTo("#q-fuerza", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2)" }}, {T_SPLIT} + 3.7);
tl.to("#q-fuerza", {{ opacity: 0, duration: 0.1 }}, {T_SPLIT} + 4.75);
tl.fromTo("#t-profe", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power3.out" }}, {T_SPLIT} + 4.76);
tl.to("#t-profe", {{ opacity: 0, duration: 0.04 }}, {T_EST} - 0.04);
tl.fromTo("#split-bot video", {{ scale: 1.0 }}, {{ scale: 1.12, duration: 5.47, ease: "none" }}, {T_SPLIT});

// 3. estímulo (punch-in)
cut({T_EST});
tl.fromTo("#est-w", {{ scale: 1.0 }}, {{ scale: 1.18, duration: 0.25, ease: "power2.out" }}, {T_EST});
tl.fromTo("#q-estimulo", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2)" }}, {T_EST} + 0.96);
tl.to("#q-estimulo", {{ opacity: 0, duration: 0.04 }}, {T_REM} - 0.04);

// 4. remate
cut({T_REM});
tl.fromTo("#chip1", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.16, ease: "power3.out" }}, {T_REM} + 0.59);
tl.fromTo("#chip2", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.16, ease: "power3.out" }}, {T_REM} + 0.83);
tl.fromTo("#chip3", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.16, ease: "power3.out" }}, {T_REM} + 1.07);
tl.to(["#chip1", "#chip2", "#chip3"], {{ opacity: 0, x: 60, duration: 0.12 }}, {T_REM} + 2.4);
tl.fromTo("#q-barato", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2)" }}, {T_REM} + 2.49);
tl.to("#q-barato", {{ opacity: 0, duration: 0.06 }}, {T_REM} + 3.07);
tl.fromTo("#rem-w", {{ scale: 1.0 }}, {{ scale: 1.2, duration: 0.18, ease: "power2.out" }}, {T_REM} + 3.07);
tl.to("#rem-w", {{ scale: 1.0, duration: 0.25, ease: "power2.out" }}, {T_REM} + 3.65);
tl.fromTo("#cta-a", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.15, ease: "power3.out" }}, {T_REM} + 3.75);
tl.fromTo("#cta-b", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {T_REM} + 3.8);

// subtítulos
{cap_js}

// 5. cierre
tl.to(["#wm", "#cta-a", "#cta-b"], {{ opacity: 0, duration: 0.05 }}, {T_OUT} - 0.05);
cut({T_OUT});
tl.fromTo("#outro", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06 }}, {T_OUT} - 0.03);
tl.fromTo("#ig-c", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, {T_OUT} + 0.15);
tl.to("#ig-c", {{ scale: 1.08, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {T_OUT} + 0.8);
tl.fromTo("#outro-t", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {T_OUT} + 0.45);
tl.fromTo("#outro-s", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {T_OUT} + 0.65);

window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(os.path.join(P, "index.html"), "w", encoding="utf-8").write(html)
print("ok cutout=", CUT, "caps", len(caps), "sfx", len(sfx))
