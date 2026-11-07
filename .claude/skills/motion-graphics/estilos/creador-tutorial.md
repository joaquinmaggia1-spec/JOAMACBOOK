# Estilo: creador tutorial (talking head + subtítulos cinéticos + pantalla dividida)

Origen (solo referencia, no reutilizar footage):
- v1 `pin.it/2ByxRAZUr` → pin 468233692528933321 · 14.0 s · 720×1280 · 30 fps · tutorial de DaVinci "cómo crear textos como estos".
- v2 `pin.it/6icWxSLD7` → pin 889812838908940853 · 64.9 s · 23.976 fps · @billycreative_, texto detrás de la persona en Premiere.
- v3 `pin.it/1G3i4JBox` → pin 889812838912268223 · 72.5 s · 23.976 fps · @billycreative_, "transición brazo robótico" con IA (Higgsfield/Seedance).

Hojas y frames clave: `referencias/creador-tutorial/`.

Coordenadas en **1080×1920** (medidas sobre frames a 360×640 y llevadas ×3; aproximadas ±20 px).

## 1. Estructura (la misma en los 3)
| Tramo | Duración | Qué pasa |
|---|---|---|
| Gancho | 0-6 s | Persona a cámara + **título gigante detrás de la persona** (la persona tapa parte de las letras) + palabra-acento en serif. El frame 0 ya muestra el título. |
| Promesa | 6-10 s | Plano cerrado a cámara (punch-in), palabra-acento ("en Premiere", "Evidentemente", "Let's Go!"). |
| Tutorial | 10 s-final-6 s | **Pantalla dividida**: arriba la persona (0-630 px), abajo la grabación de pantalla (630-1920 px) con cursor visible. Subtítulo palabra por palabra en la costura. Cada 6-10 s vuelve un plano completo a cámara para respirar. |
| Remate | últimos 6-10 s | Plano a cámara, otro ángulo (gran angular / contrapicado), **palabra-cita gigante** ("Edit", "IA") y resultado final. |
| Cierre | 3-5 s | Negro, logo de Instagram centrado que alterna blanco ↔ degradado IG, handle debajo. |

Cortes de cámara cada 2-10 s; el texto cambia cada 0.25-0.5 s (palabra por palabra), así que siempre hay movimiento.

## 2. Capas y coordenadas

### Título gancho detrás de la persona (lo más característico)
- Orden de capas: fondo (video) → **texto** → **persona recortada** (máscara/rotoscopia del mismo video) → subtítulos. Así la cabeza/cuerpo tapa las letras.
- v2: "Así · es · como" amarillo, sans 600, ~70 px, repartido a lo ancho en y≈250. "PUEDES" sans condensada ultra-negra (tipo Anton / Bebas Neue Black), amarillo **#FFD60A**, y 290-600, x 130-940 (≈75 % del ancho). Debajo "colocar texto": serif bold itálica (tipo Playfair Display 900 italic), blanca con degradado a gris y sombra suave, y 780-1200, centrado, ~300 px. Palabra pequeña "por" serif amarilla en y≈1310.
- v1: "COMO" sans extendida 900 (tipo Montserrat 900 con tracking ancho), relleno degradado blanco → durazno #F3C4A3 → azul acero #7FA3C8, y 290-550, casi a ancho completo (x 50-1040). Luego "CREAR" (y≈945, alineado a la izquierda, mismo degradado) y "TEXTOS" (y≈1260) + "COMO ESTOS" pequeño blanco (y≈1400). Entran una a una.
- v3: rojo **#F04A3C**. "ESTE" serif condensada y≈160, "EFECTO" gigante y 230-650 detrás de la persona, "SE ··· LLAMA" serif a izquierda/derecha en y≈660. Después "TRANSICIÓN" serif (y≈290) + "BRAZO ROBOTICO" sans 900 en 2 líneas (y 350-650). Light leak/halación sobre el título.
- Animación: cada palabra aparece de golpe (0 → 100 % en 2-4 frames) con leve escala 108 % → 100 %; a veces blur-in de 6 frames. Sale con corte seco.

### Subtítulos palabra por palabra
- Sans condensada bold en MAYÚSCULAS (tipo Bebas Neue / Oswald 700), blanca, sombra negra suave, ~95 px de alto de fuente.
- Plano completo: centrado, y≈1400 (v1). Pantalla dividida: sobre la costura, y≈600-630 (v2, v3).
- 1-2 palabras por vez, una por sílaba tónica de la voz (0.2-0.5 s cada una). Sin caja de fondo.
- Variante v2/v3 en plano a cámara: subtítulo **serif minúscula amarilla #F2D04B**, pequeño (~52 px), y≈1320 ("hacer este efecto", "encima", "pasarnos").

### Palabras-acento
- "en **Premiere**": "en" serif pequeña blanca + "Premiere" serif bold itálica ~250 px con degradado rosa #F06BD0 → violeta #9B5CF6, brillo blanco arriba y glow; y 1150-1350.
- "Evidentemente", "Let's Go!": serif bold itálica con degradado (rosa-violeta o amarillo), y≈1200.
- Cita gigante final: `"Edit"` / `"IA"` con comillas, serif bold itálica ~230 px, amarillo limón **#EEF25A** con glow, y 1070-1330; entra con escala 130 % → 100 % y un destello.

### Marca de agua fija
- Ícono de Instagram (contorno blanco, ~60 px) en x≈965, y≈485, y debajo el handle en sans 600 ~22 px, alineado a la derecha en x≈1000, y≈565. Siempre visible (excepto en el cierre, donde va al centro).

### Pantalla dividida
- Arriba: video de la persona recortado a 1080×630 (encuadre de cara y manos).
- Abajo: captura de la app (Premiere, DaVinci, Higgsfield) 1080×1290, con zoom 110-140 % hacia donde está el cursor; el cursor y los clics se ven. Paneles oscuros #1E1E1E.
- Inserto opcional dentro de la UI: grilla de miniaturas ("Captura 1 + Captura 2"), resultado del render, logo de la app (Pr) que aparece con pop.

## 3. Movimiento y transiciones
- **Punch-in**: alternar escala del talking head 100 % ↔ 115-125 % en cada corte de frase (jump cut).
- **Whip / blur de movimiento** entre plano a cámara y pantalla dividida (6-8 frames).
- **Light leak / halación** naranja-blanca sobre títulos y cortes (v1 "EXT", v3).
- **Gran angular / ojo de pez** en tomas de remate (contrapicado, persona agachada).
- Rótulos de planos ("Plano 1", "Plano 2", "Plano 3"): sans 700 blanca ~110 px, y≈790, blur-in, el anterior se desvanece.

## 4. Sonido
- Voz en off/directa protagonista (−14 a −16 dB medio). Música de fondo suave por debajo.
- sfx: whoosh en cada whip, pop en cada palabra-acento, click en los clics de cursor, impacto grave en la cita final y en el título gancho, riser antes del resultado.

## 5. Cómo replicarlo con otro guion
1. **Necesita a una persona hablando a cámara.** Opciones: (a) el usuario graba su toma vertical; (b) se genera con Higgsfield (AI Influencer / Seedance) — costoso, preguntar.
2. Transcribir la voz (`hyperframes` / media-use transcript) para tener tiempos por palabra → subtítulos palabra por palabra.
3. Recortar la persona para el título detrás: `media-use` cutout del video (o rotoscopia por frame); si no hay recorte, poner el título arriba de la cabeza (y 150-550) sin solaparse.
4. Gancho = la promesa del guion en 2-3 palabras gigantes + 1-2 palabras serif.
5. Tutorial: grabación de pantalla del usuario en la mitad inferior; si no hay, mockups de UI en HTML.
6. Cita final con la palabra clave del guion entre comillas, en amarillo limón.
7. Cierre negro con el Instagram y el handle del usuario.
