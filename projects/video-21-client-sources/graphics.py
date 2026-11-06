"""Đồ hoạ video 21 — Salon Setup: How to find clients (4 client sources).
Video thô đã dựng sẵn cảnh + voice; style editorial theo video mẫu, theme branding salon_setup. Không SFX.
Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from editorial import *

words = load_words(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"))
HOOK_END, CARD, END = 3.68, (2.30, 3.68), 58.60
ACC = THEMES["salon_setup"]["accent"]

caps = phrases(words, skip=[(0, HOOK_END)],
               emph={18: "big", 27: "acc", 43: "pop", 48: "ital", 67: "pop", 87: "ital", 90: "ital", 103: "acc",
                     120: "ital", 123: "pop", 125: "acc", 129: "script", 139: "pop", 155: "pop", 160: "ital",
                     179: "acc", 183: "script"},
               circle={169})

E = []
# hook — hiện đủ ngay từ 0s, giữ qua câu giới thiệu
E.append(el(-1, HOOK_END, 60, 190, '<div class="capbox">How to find'
            f'<br><span class="in"><span class="script">clients?</span>{ellipse(360, 130, 0.5, color=ACC)}</span></div>',
            w=960, anim="fade"))
E.append(sticker(0.2, HOOK_END, 860, 30, "💅", rot=10))
# thẻ tiêu đề series (lúc "Theresa, a salon owner in Toronto")
E.append(card(CARD[0], CARD[1], "Salon", "Setup", ["salon owner · Toronto", "@nailart.bytheresa"],
              y=640, top_note="where my clients come from"))

# 4 nguồn khách — chip 1/3 dưới
BUCKETS = [(9.12, 18.22, "Search (SEO)", "“nail salon near me” = ready to book", "🔎"),
           (18.22, 29.16, "Social media", "they check your work first", "📱"),
           (29.16, 38.34, "Ads", "measure cost per booking, not views", "📣"),
           (38.34, 48.80, "Your old clients", "rebook · thank referrals", "💞")]
for k, (a, b, tt, sub, emo) in enumerate(BUCKETS, 1):
    star = f'<span class="of" style="color:{ACC};font-size:40px;font-weight:800">★ the cheapest</span>' if k == 4 else ""
    size = 46 if len(sub) > 32 else 54
    E.append(el(a + .1, b, 70, 1400, f'<div class="chip"><div class="no">bucket {k}<span class="of">/ 4</span> {sparkle(34, ACC)}{star}</div>'
                f'<div class="tt">{tt}</div><div class="amt" style="font-size:{size}px">{sub}</div></div>', w=940, anim="fade"))
    E.append(sticker(a + .3, b, 860 if k % 2 else 80, 30, emo, rot=8 if k % 2 else -8))

# ghi chú cần chú ý: câu hỏi cho mọi khách
E.append(el(48.92, 55.30, 60, 1400, f'<div class="chip"><div class="no">pro tip {sparkle(34, ACC)}</div>'
            '<div class="tt">Ask every client:</div><div class="amt" style="font-size:58px">“How did you hear about us?”</div></div>',
            w=960, anim="pop"))
E.append(sticker(49.0, 55.30, 860, 30, "❓", rot=8))

# kết
E.append(el(55.38, END, 0, 1500, f'<div class="handle" style="text-align:center">{sparkle(34, ACC)} @nailart.bytheresa</div>',
            w=1080, anim="fade"))

build(E, caps, os.path.join(sys.argv[1], "overlay.html"), theme="salon_setup")
