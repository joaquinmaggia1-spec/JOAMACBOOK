import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[1],device="cpu",compute_type="int8")
out={}
for f in sys.argv[3:]:
    import numpy as np,wave; wf=wave.open(f); aud=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(aud,language="es",word_timestamps=True,vad_filter=False,beam_size=5)
    ws=[]
    for s in segs:
        for w in s.words: ws.append({"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)})
    out[f.split('/')[-1]]=ws
    print(f.split('/')[-1],' '.join(x['w'] for x in ws),flush=True)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
