"""Đồ hoạ video thử — Salon Setup: 6 things before putting down the deposit.
Style editorial theo video mẫu. Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from editorial import *

words = load_words(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"))
HOOK_END, CARD = 4.74, (5.50, 7.10)

caps = phrases(words, skip=[(0, HOOK_END), CARD],
               emph={25: "big", 33: "pop", 46: "ital", 57: "pop", 65: "script", 75: "ital", 88: "pop",
                     109: "script", 112: "ital", 113: "pop", 117: "pop", 131: "pop", 147: "pop", 150: "ital",
                     160: "ital", 162: "script", 183: "pop", 190: "script", 195: "ital"},
               circle={31, 141, 166})

E = []
# hook — hiện đủ ngay từ 0s (t0 âm)
E.append(el(-1, HOOK_END, 60, 170, '<div class="capbox">You could waste'
            '<span class="pop">tens of thousands</span>of dollars renting'
            f'<br><span class="in"><span class="script">a wrong space</span>{ellipse(560, 130, 3.4)}</span><br>'
            '<i>for your salon.</i></div>', w=960, anim="fade"))
E.append(sticker(2.5, HOOK_END, 830, 120, "💸", rot=10))
# thẻ tiêu đề (như "Journalist becoming Creator" trong video mẫu)
E.append(card(CARD[0], CARD[1], "Salon", "Setup", ["salon owner · Toronto", "@nailart.bytheresa"],
              y=560, top_note="the salon owner's notebook"))

# 6 ý — chip ở 1/3 dưới, giữ suốt đoạn
POINTS = [(10.14, 18.64, "Zoning"), (18.64, 27.88, "Plumbing &amp; <i>hot water</i>"),
          (27.88, 36.04, "Electrical &amp; <i>ventilation</i>"), (36.04, 43.70, "The <i>real</i> cost of rent"),
          (43.70, 50.40, "Rent-free <i>time</i>"), (50.40, 62.60, "Lease <i>term</i>")]
for k, (a, b, tt) in enumerate(POINTS, 1):
    E.append(el(a + .1, b, 70, 1430, f'<div class="chip"><div class="no">no. {k} {sparkle(34, LIME)}</div>'
                f'<div class="tt">{tt}</div></div>', w=940, anim="fade"))

# emoji sticker cạnh phụ đề
for t0, t1, x, y, e, r in [(10.42, 14.38, 850, 40, "📍", 8), (13.92, 14.38, 90, 40, "💅", -10),
                           (19.04, 22.06, 860, 40, "🚰", 8), (24.02, 27.88, 80, 40, "🛁", -8),
                           (28.66, 31.88, 860, 40, "⚡", 10), (34.28, 36.04, 80, 40, "💸", -8),
                           (38.72, 43.70, 860, 40, "🧾", 8), (46.74, 50.40, 860, 40, "🗓️", 8),
                           (51.08, 54.90, 80, 40, "📝", -8), (55.98, 58.20, 860, 40, "⚠️", 8),
                           (68.68, 70.10, 860, 40, "🌱", 8)]:
    E.append(sticker(t0, t1, x, y, e, rot=r))

# kết
E.append(el(70.10, 74.37, 0, 1500, f'<div class="handle" style="text-align:center">{sparkle(34, LIME)} @nailart.bytheresa</div>',
            w=1080, anim="fade"))

build(E, caps, os.path.join(sys.argv[1], "overlay.html"))
