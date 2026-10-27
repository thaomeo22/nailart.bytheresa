"""Đồ hoạ video 18 — Salon Setup: Monthly operating costs (14 costs).
Video thô đã dựng sẵn cảnh; style editorial theo video mẫu, theme branding salon_setup (Montserrat / Open Sans, cam #ff802e).
Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from editorial import *

words = load_words(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"))
HOOK_END, CARD, END = 3.72, (4.94, 6.22), 80.08
ACC = THEMES["salon_setup"]["accent"]

emph = {i: "acc" for i, w in enumerate(words) if re.match(r"^\$?[\d.,]+%?[.,]?$", w["w"])}   # số tiền / % màu cam
emph.update({181: "ital", 186: "script", 194: "pop"})
caps = phrases(words, skip=[(0, HOOK_END), CARD], emph=emph, circle={181})

E = []
# hook — hiện đủ ngay từ 0s
E.append(el(-1, HOOK_END, 60, 150, '<div class="capbox"><span class="big">14</span>costs every month'
            '<br>before your business'
            f'<br><span class="in"><span class="script">makes a profit</span>{ellipse(560, 130, 2.6, color=ACC)}</span></div>',
            w=960, anim="fade"))
E.append(sticker(1.0, HOOK_END, 830, 60, "💸", rot=10))
# thẻ tiêu đề series
E.append(card(CARD[0], CARD[1], "Salon", "Setup", ["salon owner · Toronto", "@nailart.bytheresa"],
              y=560, top_note="monthly operating costs"))

# 14 khoản — chip 1/3 dưới: số thứ tự, tên khoản, số tiền
ITEMS = [(10.38, 14.82, "Rent, TMI &amp; HST", "$5,000–$20,000", "/ month", "🏠"),
         (14.82, 20.04, "Commission or payroll", "40–55%", "of service revenue", "💅"),
         (20.04, 24.10, "Receptionist &amp; manager", "$3,500–$9,000", "/ month", "🧑‍💼"),
         (24.10, 28.94, "Supplies &amp; disposables", "5–12%", "of revenue", "🧴"),
         (28.94, 34.26, "Electricity, gas &amp; water", "$700–$2,000", "/ month", "💡"),
         (34.26, 38.50, "Internet, phone &amp; security", "$200–$600", "/ month", "📶"),
         (38.50, 42.14, "Booking platform &amp; POS", "$200–$1,000", "/ month", "📅"),
         (42.14, 45.82, "Card processing", "1–3.5%", "of card sales", "💳"),
         (45.82, 48.74, "Business insurance", "$50–$500", "/ month", "🛡️"),
         (48.74, 53.24, "Cleaning, laundry &amp; garbage", "$400–$1,500", "/ month", "🧺"),
         (53.24, 56.54, "Marketing", "$500–$3,000", "/ month", "📣"),
         (56.54, 61.50, "Accounting &amp; payroll", "$300–$1,200", "/ month", "📊"),
         (61.50, 67.56, "Repairs &amp; replacement", "$300–$1,500", "/ month", "🔧"),
         (67.56, 72.34, "Bank fees &amp; chargebacks", "$100–$800", "/ month", "🏦")]
for k, (a, b, tt, amt, unit, emo) in enumerate(ITEMS, 1):
    E.append(el(a + .1, b, 70, 1400, f'<div class="chip"><div class="no">no. {k}<span class="of">/ 14</span> {sparkle(34, ACC)}</div>'
                f'<div class="tt">{tt}</div><div class="amt">{amt}<small>{unit}</small></div></div>', w=940, anim="fade"))
    E.append(sticker(a + .3, b, 860 if k % 2 else 80, 40, emo, rot=8 if k % 2 else -8))

# hiệu ứng âm thanh (pipeline/sfx.py) — như video mẫu: hook thu hút, mỗi mục mới, số tiền, ghi chú cần chú ý
cue(0.0, "impact"); cue(0.0, "whoosh", -2); cue(0.08, "pop")          # hook: "14" bật ra
cue(1.0, "chaching")                                                    # 💸
cue(2.6, "shimmer", 2)                                                  # elip quanh "makes a profit"
cue(CARD[0] - 0.12, "whoosh"); cue(CARD[0] + 0.1, "shimmer")            # thẻ Salon Setup
for k, (a, b, *_rest) in enumerate(ITEMS, 1):
    cue(a - 0.05, "whoosh", -3); cue(a + 0.12, "pop")                   # mở mục mới + chip hiện
    money = [w["s"] for w in words if a <= w["s"] < b and re.match(r"^\$?[\d.,]+%?[.,]?$", w["w"])]
    if money:
        cue(money[0], "coin", -2)                                       # số tiền đầu tiên của mục
cue(72.34, "pop"); cue(73.33, "swish")                                  # "every salon is different" + elip "estimates"
cue(75.16, "shimmer", -2)
cue(75.78, "pop"); cue(79.58, "ding", -3)                               # @handle, "Bye!"

# kết
E.append(el(72.34, 75.70, 0, 1440, f'<div class="chip" style="text-align:center"><div class="tt">every salon is <i>different</i></div></div>',
            w=1080, anim="fade"))
E.append(el(75.78, END, 0, 1500, f'<div class="handle" style="text-align:center">{sparkle(34, ACC)} @nailart.bytheresa</div>',
            w=1080, anim="fade"))

build(E, caps, os.path.join(sys.argv[1], "overlay.html"), theme="salon_setup")
