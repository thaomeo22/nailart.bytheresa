"""Đồ hoạ video 19 — Salon Setup: Choosing an online booking system (part 1 — 7 things to check).
Video thô đã dựng sẵn cảnh; style editorial theo video mẫu, theme branding salon_setup (Montserrat / Open Sans, cam #ff802e) + SFX.
Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html + sfx.json)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from editorial import *

words = load_words(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"))
HOOK_END, CARD, END = 3.66, (4.88, 6.16), 63.41
ACC = THEMES["salon_setup"]["accent"]

caps = phrases(words, skip=[(0, HOOK_END), CARD],
               emph={20: "big", 45: "ital", 56: "acc", 105: "pop", 106: "acc", 123: "pop", 136: "ital", 144: "pop",
                     147: "acc", 152: "ital", 155: "ital", 163: "script", 167: "pop", 171: "acc", 189: "pop"},
               circle={34, 189})

E = []
# hook — hiện đủ ngay từ 0s
E.append(el(-1, HOOK_END, 60, 230, '<div class="capbox">The <span class="acc">cheapest</span> booking app'
            '<br>can be the'
            f'<br><span class="in"><span class="script">most expensive</span>{ellipse(560, 130, 2.6, color=ACC)}</span>one.</div>',
            w=960, anim="fade"))
E.append(sticker(0.3, HOOK_END, 860, 30, "📱", rot=10)); E.append(sticker(2.5, HOOK_END, 80, 30, "💸", rot=-10))
# thẻ tiêu đề series
E.append(card(CARD[0], CARD[1], "Salon", "Setup", ["salon owner · Toronto", "@nailart.bytheresa"],
              y=560, top_note="choosing a booking system"))
# "the last one is extremely important" — ghi chú cần chú ý
E.append(sticker(10.6, 13.3, 860, 40, "⚠️", rot=8))

# 7 điều cần kiểm tra — chip 1/3 dưới: số thứ tự, tên, ý phụ (cam)
ITEMS = [(13.36, 17.34, "Easy for clients to book", "under a minute", "⏱️"),
         (17.34, 21.74, "Easy for you &amp; your staff", "manage it from your phone", "📱"),
         (21.74, 27.70, "Service time per technician", "new tech = more time", "🧑‍🎨"),
         (27.70, 33.58, "Reminders, deposits &amp; policies", "reduce no-shows", "🔔"),
         (33.58, 39.10, "Commission, tips &amp; payroll", "export payroll reports", "💰"),
         (39.10, 46.48, "The <i>total</i> cost", "monthly + staff + SMS + card fees", "🧾"),
         (46.48, 55.52, "Demo + 2-week trial", "test on quiet &amp; busy days", "🧪")]
for k, (a, b, tt, sub, emo) in enumerate(ITEMS, 1):
    star = f'<span class="of" style="color:{ACC};font-size:40px;font-weight:800">★ most important</span>' if k == 7 else ""
    size = 52 if len(sub) > 28 else 60
    E.append(el(a + .1, b, 70, 1400, f'<div class="chip"><div class="no">no. {k}<span class="of">/ 7</span> {sparkle(34, ACC)}{star}</div>'
                f'<div class="tt">{tt}</div><div class="amt" style="font-size:{size}px">{sub}</div></div>', w=940, anim="fade"))
    E.append(sticker(a + .3, b, 860 if k % 2 else 80, 40, emo, rot=8 if k % 2 else -8))

# kết: bài học + kêu gọi bình luận
E.append(sticker(55.84, 59.16, 860, 40, "💸", rot=8))
E.append(el(59.24, END, 0, 1380, '<div class="chip" style="text-align:center"><div class="tt">Comment <span style="color:%s">"YES"</span> 👇</div>'
            '<div class="handle" style="margin-top:18px">%s @nailart.bytheresa</div></div>' % (ACC, sparkle(34, ACC)), w=1080, anim="fade"))

# hiệu ứng âm thanh — hook thu hút, mỗi mục mới, ghi chú cần chú ý
cue(0.0, "impact"); cue(0.0, "whoosh", -2); cue(0.34, "pop")           # hook, "cheapest"
cue(2.56, "chaching"); cue(2.7, "shimmer", 2)                           # "most expensive" + elip
cue(CARD[0] - 0.12, "whoosh"); cue(CARD[0] + 0.1, "shimmer")            # thẻ Salon Setup
cue(6.72, "pop", 2)                                                     # "7" to
cue(10.74, "swish"); cue(10.9, "shimmer"); cue(10.6, "click", 2)        # "extremely important" + elip + ⚠️
for k, (a, b, *_rest) in enumerate(ITEMS, 1):
    if k == 7:
        cue(a - 0.8, "riser", -2); cue(a, "impact", -6)                 # mục quan trọng nhất
    cue(a - 0.05, "whoosh", -3); cue(a + 0.12, "pop")
cue(32.84, "ding", -2)                                                  # "no-shows"
cue(40.5, "coin", -2)                                                   # "total cost"
cue(55.84, "chaching", -2)                                              # "lost a lot of money"
cue(59.24, "whoosh", -3); cue(61.5, "pop", 2); cue(61.6, "shimmer")     # "Comment YES"
cue(63.1, "ding", -3)

build(E, caps, os.path.join(sys.argv[1], "overlay.html"), theme="salon_setup")
