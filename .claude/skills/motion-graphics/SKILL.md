---
name: motion-graphics
description: Pipeline completo para identificar ("robar") el estilo de edición de videos de referencia de Pinterest y replicarlo en videos verticales nuevos con otros guiones. Usar cuando el usuario pase links de Pinterest (pin.it o pinterest.com/pin) para copiar un estilo, pida un video de motion graphics, un reel de pauta/marketing, un video "con este estilo", o edite piezas con HyperFrames, Nano Banana, Seedance o efectos de sonido de /media-use.
---

# Motion graphics: identificar un estilo y replicarlo

Dos fases, siempre en este orden:
- **A. Robar el estilo** de los videos de referencia → una ficha en `estilos/<nombre>.md` con coordenadas, tipografías, colores, ritmo y sonido.
- **B. Replicarlo** con el guion nuevo del usuario → proyecto HyperFrames → MP4 1080×1920.

Estilos ya analizados (leer el que corresponda antes de montar):
- `estilos/editorial-mg.md`: motion graphics construido en código (fondos diseñados, objetos que reemplazan letras, UI mockups). Videos: Brasil, pauta, casino Kriptonita.
- `estilos/creador-tutorial.md`: creador hablando a cámara con subtítulos palabra por palabra, título gigante detrás de la persona, pantalla dividida con grabación de pantalla, palabras-acento en serif itálica.

## Instalación (si el contenedor es nuevo)
```bash
pip3 install -U gallery-dl yt-dlp           # gallery-dl necesita yt-dlp para bajar los mp4
npm install -g hyperframes                  # Node >= 22 y FFmpeg
hyperframes skills < /dev/null              # instala hyperframes, hyperframes-cli, hyperframes-registry, media-use,
                                            # figma, remotion-to-hyperframes, reverse-any-video, slideshow, style-sampling
```
Red del entorno "EDICION DE VIDEO": pin.it, api.pinterest.com, ar/www.pinterest.com, v1/i.pinimg.com (Pinterest), d8j0ntlcm91z4.cloudfront.net (CDN de Higgsfield), cdn.jsdelivr.net (logos de theSVG), api.openverse.org y cdn.freesound.org (sfx), pixabay.com (música). Si algo da 403, pedir el host exacto con `update_environment`; nunca esquivar el proxy.

## Fase A: robar el estilo (los pasos que pidió el usuario)

1. **Descargar con gallery-dl**, partir en partes por cortes y armar contact sheets:
   `bash <skill>/scripts/analizar_referencias.sh <scratchpad>/ref <link1> <link2> <link3>`
   - Los `pin.it/...` se resuelven solos a `/pin/<id>/`.
   - La detección de escenas es ruidosa con destellos/light leaks: revisar los cortes a mano.
   - Hoja de contacto: 2 fps (<30 s) o 1 fps; filas calculadas con la duración real.
2. **Mirar las hojas** (Read) y **sacar frames clave** a 360×640 (cada coordenada ×3 = 1080×1920). Mirar: gancho del frame 0, títulos, subtítulos, transiciones, cierre.
3. **Escribir la ficha** `estilos/<nombre>.md` con: formato y ritmo; capas (fondo, persona, texto, UI); **coordenadas en 1080×1920** de cada elemento; tipografías (y equivalente disponible: Montserrat, Playfair Display, Bebas Neue / Anton / Oswald vía Google Fonts vendorizado); paleta en HEX; animaciones (entrada, duración, easing); transiciones; sonido; cierre. Con estructura de secciones = una por referencia.
4. Guardar hojas y frames clave en `referencias/<nombre>/` (solo referencia; **nunca** se reutiliza el footage de los pins en el video final).

## Fase B: replicar con otro guion

1. **Guion primero**: duración objetivo, escenas con tiempos, texto en pantalla, efectos por corte, qué se genera. Mostrarlo antes de gastar créditos (salvo que el usuario diga "avancemos" / "hacelo como mejor resuelvas").
2. **Costo**: `balance` y `get_cost` de cada tipo de generación; si no alcanza, parar y preguntar.
3. **Generación**: imágenes en lote (`generate_image_batch`) → `jobs_wait` → descargar con curl del CDN. Clips con `generate_video` usando la imagen como `start_image`.
4. **Montaje**: `npx hyperframes init <proyecto> --skip-skills --skill=hyperframes` → `index.html` raíz + `compositions/*.html` por escena (o un generador Python que escriba el HTML) + captions.
5. **Validación**: `npx hyperframes check --json` hasta 0 errores y 0 advertencias.
6. **Revisión**: `npx hyperframes snapshot --at t1,t2,...` y mirar el contact sheet.
7. **Audio**: sfx de `/media-use` en su propia pista cada uno; música de `recursos/musica/`.
8. **Render**: `npx hyperframes render -o salida.mp4` en segundo plano; verificar con ffprobe y `volumedetect`.
9. **Entrega**: `SendUserFile` con el MP4 + qué se usó, créditos gastados y pendientes.

## Qué es "motion graphics" aquí (lo más importante)
Un video de fotos a pantalla completa con texto encima NO es motion graphics: es un slideshow, y el usuario lo rechazó. El estilo de referencia se construye en código, por capas:
- **Fondos diseñados**, no fotos: gris claro (#ECECEC), negro con grilla, navy con orbes de luz y grano, papel crema.
- **Objetos recortados** que actúan con la tipografía: el objeto reemplaza una letra (BR[coco]SIL), cae, se agranda, abre la transición. Se generan con Nano Banana sobre blanco puro y se funden con `mix-blend-mode: multiply` en fondos claros (subir blancos con `colorlevels` si el fondo no es #FFF).
- **Objetos sobre fondos oscuros** necesitan alfa real: `python3 -I <skill>/scripts/cutout_edges.py entrada.png salida.png 600` (borra solo el blanco conectado al borde; un `colorkey` blanco también borra los brillos del objeto).
- **Logos de marca** (Instagram, WhatsApp, Meta…): oficiales, nunca redibujados. `NODE_USE_ENV_PROXY=1 npx hyperframes media-use resolve --type logo --entity <marca> --intent "<marca> logo" --project .` (sin `NODE_USE_ENV_PROXY=1` Node no usa el proxy y falla; el CDN es `cdn.jsdelivr.net`). Si una marca sale de la caché como avatar de GitHub, ingerir el SVG de theSVG con `--from`. Si el mismo logo aparece dos veces en una sección, usar una copia del archivo (evita `duplicate_media_discovery_risk`).
- **Personas**: Nano Banana sobre blanco puro, plano medio, y recorte con `cutout_edges.py`. Para ropa clara: `cutout_edges.py in.png out.png 900 250 6 3 4`.
- **Las fotos van dentro de contenedores**: post de Instagram con likes, tarjetas redondeadas con etiqueta en píldora, máscaras circulares. Nunca a pantalla completa como plano principal (excepción: el estilo `creador-tutorial`, donde la persona a cámara SÍ es el plano principal).
- **UI y mockups**: burbujas de chat azules con "escribiendo…", comentarios en vidrio (fondo rgba + borde fino, sin backdrop-filter), contadores numéricos.
- **Tipografía que actúa**: palabras de a una, mezcla de Montserrat 900 y Playfair itálica, letras que suben desde una máscara, listas con viñetas en serif.
- **Detalles HUD** (con `data-layout-ignore`): handle, textos verticales con mucho tracking, fechas en monoespaciada, zigzags, reglas, líneas que se dibujan (stroke-dashoffset).
- **Ritmo**: algo se mueve cada 0.5 s; transiciones con máscara circular, barridos y objetos que tragan el cuadro.
- **Estados iniciales ocultos en CSS**, no con `tl.set` en 0 (no se pinta en el primer frame). El frame 0 debe mostrar ya el gancho (la miniatura).
- Antes de generar, proponer la estructura por secciones (una por referencia) y gastar créditos solo en objetos, no en fondos.

## Reglas (obligatorias)

1. **Descargas de referencias**: gallery-dl para pins de Pinterest. Solo sirven de referencia de estilo. Nunca se reutiliza su footage en el video final.
2. **Efectos de sonido**: salen de `/media-use` (`npx hyperframes media-use resolve --type sfx --intent "..."`). Si Openverse no responde, se usa la biblioteca local de media-use (`~/.claude/skills/media-use/audio/assets/sfx/`: whoosh, impact-bass-1, pop, click-soft, riser, chime…). Medir con `volumedetect` antes de recortar un tramo (algunos tienen la energía al principio).
3. **Música**: sale de Pixabay (https://pixabay.com/es/music/). Pista por pista, nunca el catálogo completo. Si Pixabay bloquea la descarga automática (Cloudflare), no se esquiva: se pide al usuario que la baje y la deje en `recursos/musica/`.
4. **Biblioteca de recursos**: todo recurso nuevo va a `recursos/` y se registra en `recursos/manifest.json` (`file`, `source`, `license`, `downloaded_at`). Nada se descarga en masa.
5. **Imágenes**: Higgsfield con Nano Banana 2.1 (`nano_banana_2_1`), 9:16, **2K por defecto** (2 créditos). Antes, `get_cost`.
6. **Clips**: Seedance 2.5 (`seedance_2_5`) en **borrador 480p, 4 s** por defecto (12 créditos). El 1080p cuesta 35 créditos por 5 s: no se genera sin preguntar. Si hace falta más duración: `minterpolate` y escalar a 1080×1920.
7. **Presupuesto**: `balance` antes de un lote. Si no cabe, parar y preguntar.
8. **Formato por defecto**: 1080×1920, 30 fps, vertical.
9. **Montaje**: HyperFrames. GSAP vendorizado en `assets/vendor/gsap.min.js` (desde `npm pack gsap@3.15.0`; el render no alcanza jsDelivr). Fuentes incluidas (Montserrat, Playfair Display) o vendorizadas en `assets/fonts/`.
10. **Captions**: grupos cortos con tiempos absolutos y kill duro al final de cada grupo. Acentos en serif itálica. Nada de texto sobre la cara.
11. **Contraste y solapes**: revisar `hyperframes check --json` y dejar 0 errores y 0 advertencias. Ninguna línea en pantalla menos de ~1.05 s si tiene 3+ palabras (`line_unread`).
12. **Audio**: ningún `<audio>` puede terminar después de la duración de la raíz. Cada efecto con su propio `data-track-index`.
13. **Revisión visual**: `hyperframes snapshot` en los momentos clave antes de renderizar.
14. **Entrega**: `SendUserFile` con ruta completa; decir qué se usó, créditos y pendientes.
15. **Git**: no se hace commit ni push sin que el usuario lo pida.

## Errores que ya ocurrieron (no repetir)
- Slideshow de fotos con subtítulos en lugar de motion graphics → ver sección de arriba.
- GSAP desde jsDelivr falla en el render → vendorizar.
- Recorte de audio desde un punto silencioso → medir con `volumedetect` antes.
- Dos textos con el mismo `bottom` que aparecen a la vez → revisar tiempos de grupos consecutivos.
- Hoja de contacto con filas calculadas desde frames a 30 fps → calcular con la duración.
- Expresiones de ffmpeg con `<` → usar `lt()` / `gte()`.
- Node no usa `HTTPS_PROXY` sin `NODE_USE_ENV_PROXY=1`.
- Whisper/faster-whisper: el modelo baja de huggingface.co → us.aws.cdn.hf.co; usar `HF_HUB_DISABLE_XET=1` (si no, pide cas-server.xethub.hf.co). Con PyAV nuevo, pasar el audio ya decodificado (numpy) en vez de la ruta.
- El título gigante de 430 px se salía del ancho: medir el ancho real (Anton ≈ 0.45 em por letra) y partir en líneas.
- La skill y `recursos/` vivían solo en el contenedor y se perdieron → ahora la skill está en el repo (`.claude/skills/motion-graphics/`); commitear cuando el usuario lo pida.
