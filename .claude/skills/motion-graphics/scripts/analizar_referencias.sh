#!/usr/bin/env bash
# Paso 1 del método: descargar pins, detectar cortes, partir en partes y armar contact sheets.
# Uso: analizar_referencias.sh <carpeta_salida> <url_pin_o_pin.it> [<url> ...]
# Requiere: gallery-dl + yt-dlp (pip), ffmpeg. Hosts: pin.it, api.pinterest.com, ar/www.pinterest.com, v1/i.pinimg.com
set -euo pipefail
OUT=$1; shift
mkdir -p "$OUT/pins" "$OUT/partes" "$OUT/contact" "$OUT/frames"
i=1
for u in "$@"; do
  # los links cortos pin.it se resuelven a /pin/<id>/
  if [[ $u == *pin.it/* ]]; then
    u=$(curl -sSL -o /dev/null -w '%{url_effective}' "$u" | grep -oE 'pin/[0-9]+' | head -1)
    u="https://ar.pinterest.com/$u/"
  fi
  before=$(ls "$OUT/pins" | wc -l)
  gallery-dl -D "$OUT/pins" "$u" >/dev/null
  f=$(ls -t "$OUT/pins"/*.mp4 | head -1)
  ln -sf "$(basename "$f")" "$OUT/pins/v$i.mp4"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "== v$i  $(ffprobe -v error -show_entries stream=width,height,r_frame_rate -of csv=p=0 -select_streams v:0 "$f")  ${dur}s"
  # cortes de escena (revisar a mano si es ruidoso: destellos dan falsos cortes)
  cuts=$(ffmpeg -hide_banner -nostats -i "$f" -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 \
         | grep -oE 'pts_time:[0-9.]+' | sed 's/pts_time://' | awk -v p=0 '$1-p>0.5{print; p=$1}' | tr '\n' ' ')
  echo "   cortes: $cuts"
  prev=0; n=1
  for t in $cuts END; do
    [ "$t" = END ] && end=$dur || end=$t
    ffmpeg -hide_banner -loglevel error -y -i "$f" -ss $prev -to $end -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -an "$OUT/partes/v${i}_parte$(printf %02d $n).mp4"
    prev=$end; n=$((n+1))
  done
  # contact sheet: 2 fps si dura <30 s, 1 fps si es más largo. Filas calculadas con la DURACIÓN, no con frames a 30 fps.
  fps=$(python3 -c "print(2 if $dur<30 else 1)"); cols=8
  rows=$(python3 -c "import math;print(math.ceil(math.ceil($dur*$fps)/$cols))")
  ffmpeg -hide_banner -loglevel error -y -i "$f" -vf "fps=$fps,scale=180:320,pad=180:320:0:0:black,tile=${cols}x${rows}:padding=4:margin=8:color=0x222222" -frames:v 1 "$OUT/contact/contacto_v$i.png"
  i=$((i+1))
done
echo "Listo: $OUT/contact/*.png (mirarlas), $OUT/partes/*.mp4"
echo "Siguiente: sacar frames clave a 360x640 con  ffmpeg -ss <t> -i v1.mp4 -frames:v 1 -vf scale=360:640 frames/x.png  y medir coordenadas (x3 = 1080x1920)."
