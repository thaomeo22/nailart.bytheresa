"""Đồ hoạ video 20 — Salon Setup: Choosing an online booking platform (part 2 — my $20,000 story).
Video thô đã dựng sẵn cảnh; style editorial theo video mẫu, theme branding salon_setup. Không SFX.
Ảnh bằng chứng (email ưu đãi của nền tảng cũ) đã cắt + che thông tin doanh nghiệp: work/video-20-booking2/proof/.
Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from editorial import *

words = load_words(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"))
words[238]["w"] = "Salon Pilot."                       # tên app như trên App Store
HOOK_END, CARD, END = 3.42, (5.16, 6.62), 92.60
ACC = THEMES["salon_setup"]["accent"]
PROOF = os.path.abspath(os.path.join(sys.argv[1], "proof"))

caps = phrases(words, skip=[(0, HOOK_END), CARD],
               emph={50: "acc", 52: "acc", 79: "ital", 89: "pop", 123: "acc", 133: "pop", 137: "acc", 145: "script",
                     152: "pop", 167: "ital", 168: "ital", 179: "pop", 186: "script", 214: "acc", 216: "pop", 230: "ital",
                     238: "pop", 249: "ital"},
               circle={129, 238})

E = []
# hook — hiện đủ ngay từ 0s
E.append(el(-1, HOOK_END, 60, 210, '<div class="capbox">I spent<span class="big">$20,000</span>learning how to choose'
            f'<br><span class="in"><span class="script">a booking platform</span>{ellipse(600, 130, 2.6, color=ACC)}</span></div>',
            w=960, anim="fade"))
E.append(sticker(0.6, HOOK_END, 860, 30, "💸", rot=10))
# thẻ tiêu đề series
E.append(card(CARD[0], CARD[1], "Salon", "Setup", ["salon owner · Toronto", "@nailart.bytheresa"],
              y=560, top_note="my booking app story"))

# các mốc câu chuyện — chip 1/3 dưới
BEATS = [(10.36, 24.40, "The “famous” platform", "$400–$800 / month + fees"),
         (24.54, 40.70, "Something felt <i>off</i>", "“every client came from us”"),
         (40.82, 45.30, "2 months", "to collect &amp; present proof"),
         (53.64, 64.10, "Slow &amp; buggy", "the hardest time in my business"),
         (64.18, 79.00, "Built for my salon", "fast booking · no hidden fees")]
for k, (a, b, tt, sub) in enumerate(BEATS, 1):
    E.append(el(a + .1, b, 70, 1430, f'<div class="chip"><div class="no">{sparkle(34, ACC)}</div>'
                f'<div class="tt">{tt}</div><div class="amt" style="font-size:52px">{sub}</div></div>', w=940, anim="fade"))

# bằng chứng: email ưu đãi của nền tảng cũ (đã che tên doanh nghiệp, người gửi, link, SĐT)
PCARD = ('<div style="text-align:center"><div class="chip" style="margin-bottom:14px"><span class="no">the email they sent me</span></div>'
         '<div style="background:#fff;border-radius:22px;padding:{pad};box-shadow:0 18px 40px rgba(0,0,0,.35);transform:rotate(-1.5deg)">'
         '<img src="file://{img}" style="width:100%;display:block"></div>'
         '<div class="small" style="margin-top:14px;font-size:26px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.6)">business info hidden</div></div>')
E.append(el(45.30, 47.70, 10, 600, PCARD.format(pad="18px 10px", img=os.path.join(PROOF, "proof_redacted.png")), w=1060, anim="pop"))
zoom = PCARD.format(pad="26px 26px", img=os.path.join(PROOF, "proof_zoom.png"))
zoom = zoom.replace('<img', f'<div style="position:relative"><img').replace('display:block">', 'display:block">'
        + f'<svg class="ell" data-t="48.9" width="560" height="110" viewBox="0 0 560 110" style="position:absolute;left:30px;top:-20px;overflow:visible">'
        + f'<path pathLength="1" d="M45 68 C14 9 470 -6 540 40 C590 78 160 118 40 76 C12 64 40 40 120 26" fill="none" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/></svg></div>', 1)
E.append(el(47.70, 53.64, 40, 640, zoom, w=1000, anim="fade"))

# Salon Pilot — app của bạn chủ kênh (logo vẽ lại theo ảnh App Store chủ kênh gửi: ô teal bo góc, nét cong trắng có chấm tròn)
LOGO = ('<svg width="190" height="190" viewBox="0 0 100 100"><defs><linearGradient id="sp" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2f7268"/><stop offset="1" stop-color="#1f5a52"/></linearGradient></defs>'
        '<rect x="2" y="2" width="96" height="96" rx="24" fill="url(#sp)"/>'
        '<path d="M18 74 C40 74 58 62 70 33" fill="none" stroke="#e9e7e1" stroke-width="7" stroke-linecap="round"/>'
        '<circle cx="73" cy="27" r="8.5" fill="#e9e7e1"/></svg>')
APP = ('<div style="display:flex;align-items:center;gap:34px;background:rgba(20,20,20,.55);border-radius:40px;padding:30px 40px;'
       'box-shadow:0 18px 40px rgba(0,0,0,.35)">' + LOGO +
       '<div class="chip" style="text-shadow:none"><div class="tt" style="font-size:84px;line-height:1">Salon Pilot</div>'
       '<div class="small" style="font-size:34px;color:#fff;margin-top:8px">booking app built for salons</div>'
       f'<div class="amt" style="font-size:44px;margin-top:10px">compare a few others too</div></div></div>')
E.append(el(80.40, 88.20, 50, 1360, APP, w=980, anim="pop"))

# sticker cảm xúc theo câu chuyện
for t0, t1, x, e, r in [(0.6, 0, 0, "", 0), (26.2, 30.4, 860, "🤔", 8), (45.4, 53.6, 860, "📩", 8), (55.6, 59.0, 80, "🐢", -8),
                        (60.0, 64.1, 860, "💔", 8), (64.8, 69.0, 80, "👩‍💻", -8), (72.3, 74.5, 860, "🚀", 8), (88.3, 92.0, 860, "🙏", 8)]:
    if e:
        E.append(sticker(t0, t1, x, 30, e, rot=r))

# kết
E.append(el(88.30, END, 0, 1500, f'<div class="handle" style="text-align:center">{sparkle(34, ACC)} @nailart.bytheresa</div>',
            w=1080, anim="fade"))

build(E, caps, os.path.join(sys.argv[1], "overlay.html"), theme="salon_setup")
