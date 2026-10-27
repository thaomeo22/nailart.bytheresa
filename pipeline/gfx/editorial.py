"""Đồ hoạ kiểu "editorial" (theo video mẫu của nailart.bytheresa, xem style/edit-style.md):
phụ đề serif hiện từng chữ ở 1/3 trên, từ nhấn mạnh in đậm vàng chanh / chữ viết tay, vòng elip vẽ tay, sao lấp lánh,
emoji sticker, thẻ tiêu đề. Mỗi project viết graphics.py:
    from editorial import *
    words = load_words(transcript, lines)      # in chỉ số từ: print_words(words)
    caps = phrases(words, emph={idx: "pop"|"script"|"ital"|"big"}, circle={idx, ...}, skip=[(t0, t1)])
    E = [sticker(...), card(...), el(...)]
    build(E, caps, out_html)"""
import json, os, glob, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = os.path.join(ROOT, ".cache", "fonts")
LIME = "#eef36a"


def load_words(transcript_path, lines_path):
    """Từ + mốc thời gian (Whisper) ghép với chữ đã sửa chính tả trong lines.txt (1 dòng = 1 segment, cùng số từ)."""
    segs = json.load(open(transcript_path))
    fixed = [l.split() for l in open(lines_path, encoding="utf-8") if l.strip()]
    assert len(fixed) == len(segs), f"lines.txt có {len(fixed)} dòng, transcript có {len(segs)} segment"
    out = []
    for si, (seg, cw) in enumerate(zip(segs, fixed)):
        ws = seg["words"]
        assert len(cw) == len(ws), f"dòng {si + 1}: {len(cw)} từ, Whisper có {len(ws)} từ"
        out += [{"s": w["s"], "e": w["e"], "w": c, "seg": si} for w, c in zip(ws, cw)]
    return out


def print_words(words):
    print("  ".join(f"{i}:{w['w']}@{w['s']:.2f}" for i, w in enumerate(words)))


def phrases(words, emph=None, circle=(), skip=(), max_words=3, max_dur=1.1):
    """Chia từ thành cụm 1–3 chữ (ngắt ở dấu câu / khoảng lặng). Cụm hiện tới khi cụm sau bắt đầu (tối đa +0.7s sau từ cuối)."""
    emph = emph or {}
    groups, cur = [], []
    for i, w in enumerate(words):
        if any(a <= w["s"] < b for a, b in skip):
            if cur: groups.append(cur); cur = []
            continue
        if cur and (len(cur) >= max_words or w["s"] - words[cur[0]]["s"] > max_dur
                    or w["s"] - words[cur[-1]]["e"] > 0.35 or w["seg"] != words[cur[-1]]["seg"]
                    or emph.get(i) in ("pop", "script", "big") and len(cur) >= 2):
            groups.append(cur); cur = []
        cur.append(i)
        if w["w"][-1] in ",.!?:":
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    caps = []
    for k, g in enumerate(groups):
        t0 = words[g[0]]["s"]
        nxt = words[groups[k + 1][0]]["s"] if k + 1 < len(groups) else words[g[-1]]["e"] + 0.7
        t1 = min(nxt, words[g[-1]]["e"] + 0.7)
        caps.append({"t0": round(t0, 2), "t1": round(t1, 2), "circle": any(i in circle for i in g),
                     "words": [{"t": round(words[i]["s"], 2), "txt": words[i]["w"].rstrip(",.:") if i == g[-1] else words[i]["w"],
                                "cls": emph.get(i, "")} for i in g]})
    return caps


def el(t0, t1, x, y, html, rot=0, w=None, cls="", anim="pop"):
    style = f"left:{x}px;top:{y}px;--r:{rot}deg;" + (f"width:{w}px;" if w else "")
    return f'<div class="el {cls}" data-anim="{anim}" data-t0="{t0}" data-t1="{t1}" style="{style}">{html}</div>'


def sticker(t0, t1, x, y, emoji, size=120, rot=-8):
    return el(t0, t1, x, y, f'<span class="emo" style="font-size:{size}px">{emoji}</span>', rot=rot)


def sparkle(size=46, color="#fff"):
    return (f'<svg class="spk" width="{size}" height="{size}" viewBox="0 0 40 40"><path d="M20 0 C21 14 26 19 40 20 C26 21 21 26 20 40 '
            f'C19 26 14 21 0 20 C14 19 19 14 20 0Z" fill="{color}"/></svg>')


def ellipse(w, h, t, color="#fff", stroke=3):
    """Elip vẽ tay, tự vẽ dần từ thời điểm t."""
    return (f'<svg class="ell" data-t="{t}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible">'
            f'<path pathLength="1" d="M{w*.08:.0f} {h*.62:.0f} C{w*.02:.0f} {h*.1:.0f} {w*.85:.0f} {-h*.05:.0f} {w*.97:.0f} {h*.38:.0f} '
            f'C{w*1.04:.0f} {h*.8:.0f} {w*.3:.0f} {h*1.05:.0f} {w*.07:.0f} {h*.7:.0f} C{w*.0:.0f} {h*.55:.0f} {w*.12:.0f} {h*.3:.0f} {w*.3:.0f} {h*.2:.0f}" '
            f'fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/></svg>')


def card(t0, t1, script_word, bold_word, small_lines, y=760, top_note=""):
    """Thẻ tiêu đề kiểu "Journalist / becoming / Creator." + vài dòng chữ nhỏ (series, nơi chốn, @handle)."""
    note = (f'<div class="note"><span>{top_note}</span>{ellipse(520, 70, t0 + .1, stroke=2)}</div>' if top_note else "")
    small = "".join(f"<div>{l}</div>" for l in small_lines)
    html = (f'{note}<div class="card"><div class="c-script">{script_word}</div><div class="c-bold">{bold_word}'
            f'<span class="c-dot">.</span>{sparkle(40)}</div><div class="c-small">{small}</div></div>')
    return el(t0, t1, 0, y, html, w=1080, anim="fade")


def _ff(name, pat, weight, style="normal"):
    hits = glob.glob(f"{FONTS}/*/**/files/{pat}", recursive=True)
    if not hits:
        sys.exit(f"Thiếu font {pat} — chạy bash setup.sh")
    return (f"@font-face{{font-family:'{name}';src:url('file://{hits[0]}') format('woff2');"
            f"font-weight:{weight};font-style:{style};}}")


def build(E, caps, out_html, cap_top=200):
    fonts = "".join(_ff(n, f"{fam}-{sub}-{w}-{st}.woff2", w, st)
                    for n, fam, w, st in [("Serif", "instrument-serif", 400, "normal"), ("Serif", "instrument-serif", 400, "italic"),
                                          ("Bold", "inter-tight", 800, "normal"), ("Script", "pinyon-script", 400, "normal")]
                    for sub in ("latin", "latin-ext"))
    css = """
    html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
    *{box-sizing:border-box}
    .el{position:absolute;opacity:0;transform-origin:50%% 50%%;will-change:transform}
    .emo{font-family:'Noto Color Emoji';line-height:1;filter:drop-shadow(0 6px 10px rgba(0,0,0,.3))}
    #cap{position:absolute;left:60px;right:60px;top:%dpx}
    .capbox{text-align:center;font-family:Serif;font-size:84px;line-height:.98;color:#fff;
      text-shadow:0 2px 5px rgba(0,0,0,.5),0 0 28px rgba(0,0,0,.45);letter-spacing:-.5px}
    .shade{position:absolute;left:0;width:1080px;pointer-events:none}
    .shade.top{top:0;height:760px;background:linear-gradient(rgba(0,0,0,.34),rgba(0,0,0,.16) 55%%,rgba(0,0,0,0))}
    .shade.bot{bottom:0;height:640px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.16) 45%%,rgba(0,0,0,.36))}
    .capbox .in{position:relative;display:inline-block}
    .capbox .w{display:inline-block;margin:0 .1em}
    #cap .w{opacity:0}
    .capbox .pop{display:block;font-family:Bold;font-weight:800;font-size:1.22em;letter-spacing:-.045em;color:%s;line-height:.92}
    .capbox .script{display:block;font-family:Script;font-size:1.55em;color:%s;line-height:.9;transform:rotate(-4deg)}
    .capbox .ital{font-style:italic}
    .capbox .big{display:block;font-size:2.6em;line-height:.85}
    .capbox .ell{position:absolute;left:-7%%;top:-12%%;width:114%%;height:124%%}
    .capbox .spk{position:absolute;left:-4%%;top:-26px}
    .ell path{stroke-dasharray:1;stroke-dashoffset:var(--d,1)}
    .note{position:relative;width:520px;margin:0 auto 26px;text-align:center;font-family:Serif;font-size:34px;color:#fff;padding:14px 0;
      text-shadow:0 1px 3px rgba(0,0,0,.4)}
    .note .ell{position:absolute;left:0;top:0}
    .card{text-align:center;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.35)}
    .c-script{font-family:Script;font-size:150px;line-height:.8;margin-left:-160px}
    .c-bold{position:relative;display:inline-block;font-family:Bold;font-weight:800;font-size:170px;letter-spacing:-.06em;line-height:.85}
    .c-dot{color:%s}
    .c-bold .spk{position:absolute;right:-48px;top:-6px}
    .c-small{font-family:Serif;font-size:38px;line-height:1.1;margin:30px 0 0 360px;text-align:left}
    .chip{font-family:Serif;color:#fff;text-shadow:0 2px 4px rgba(0,0,0,.4),0 0 20px rgba(0,0,0,.3)}
    .chip .no{font-family:Script;font-size:76px;color:%s;line-height:.8}
    .chip .tt{font-size:96px;line-height:.95}
    .chip .tt i{font-style:italic}
    .handle{font-family:Serif;font-style:italic;font-size:58px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.45)}
    """ % (cap_top, LIME, LIME, LIME, LIME)
    css = fonts + css

    js = """
    const CAPS=%s;
    const cap=document.getElementById('cap');
    const els=[...document.querySelectorAll('.el')];
    const ease=x=>1-Math.pow(1-x,3), cl=x=>Math.max(0,Math.min(1,x));
    const back=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
    const drawEll=(root,t)=>{for(const s of root.querySelectorAll('.ell')){s.style.setProperty('--d',1-ease(cl((t-(+s.dataset.t))/0.45)))}};
    let cur=null;
    window.setT=function(t){
      for(const e of els){
        const t0=+e.dataset.t0,t1=+e.dataset.t1;
        if(t<t0-0.01||t>t1+0.01){e.style.opacity=0;continue}
        const a=cl((t-t0)/0.25), b=cl((t1-t)/0.15);
        const sc=e.dataset.anim==='pop'?(a<1?0.6+0.4*back(a):1):1;
        e.style.opacity=Math.min(ease(a),b);
        e.style.transform=`translateY(${(1-ease(a))*16}px) rotate(var(--r)) scale(${sc})`;
        drawEll(e,t);
      }
      const c=CAPS.find(c=>t>=c.t0&&t<c.t1);
      if(c!==cur){
        cur=c;
        cap.innerHTML=c?'<span class="in">'+c.words.map(w=>`<span class="w ${w.cls}" data-t="${w.t}">${w.txt}</span>`).join(' ')
          +(c.circle?`<svg class="ell" data-t="${c.words[0].t+0.15}" viewBox="0 0 100 40" preserveAspectRatio="none"><path pathLength="1" vector-effect="non-scaling-stroke" d="M8 25 C2 4 85 -2 97 15 C104 32 30 42 7 28 C0 22 12 12 30 8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>`+%s:'')+'</span>':'';
      }
      if(!c) return;
      const out=cl((c.t1-t)/0.12);
      cap.style.opacity=out;
      for(const w of cap.querySelectorAll('.w')){
        const p=ease(cl((t-(+w.dataset.t))/0.14));
        w.style.opacity=p; w.style.filter=`blur(${(1-p)*6}px)`;
        w.style.transform=`translateY(${(1-p)*10}px)`+(w.classList.contains('script')?' rotate(-4deg)':'');
      }
      drawEll(cap,t);
    };
    """ % (json.dumps(caps, ensure_ascii=False), json.dumps(sparkle(40)))

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body><div class="shade top"></div><div class="shade bot"></div>{''.join(E)}<div id="cap" class="capbox"></div><script>{js}</script></body></html>"""
    open(out_html, "w").write(html)
    print(len(E), "elements,", len(caps), "phrases ->", out_html)
