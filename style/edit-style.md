# Style dựng video — nailart.bytheresa

> Học từ video mẫu chủ kênh gửi (`video-sample.mp4`, Drive id `1KOKjyDPRQPGqhLztdnfVx1RBA9OFnYq4`, trong `00 Kế hoạch`).
> Đồ hoạ: `pipeline/gfx/editorial.py` (mẫu dùng: `projects/video-01-thu/graphics.py`). Style scrapbook cũ (`lib.py`) không dùng cho kênh này.

## Branding (chủ kênh, 27/10)
- **Font chính:** Montserrat (phụ đề, tiêu đề, số) và Open Sans (chữ nhỏ, @handle). Được thêm font phụ kiểu video mẫu làm điểm nhấn
  (Instrument Serif nghiêng, Pinyon Script) nhưng không thay font chính.
- **Salon Setup:** màu chữ nhấn **cam `#ff802e`** (số tiền, từ khoá, chữ viết tay, dấu chấm thẻ tiêu đề). Dùng `build(..., theme="salon_setup")`.
- **Fix Your Foundation:** chưa chốt màu riêng — hỏi chủ kênh trước video FYF đầu tiên.
- **Giữ nguyên màu gốc của video** (`project.json` → `"grade": "null"`), không chỉnh màu, không làm đẹp.
- Video thô chủ kênh đã tự dựng sẵn cảnh (vd "14 cost.mp4"): giữ nguyên cảnh và thứ tự, chỉ chuẩn hoá 1080×1920@30 (edl 1 dòng, zoom 0) rồi thêm đồ hoạ + phụ đề.

## Khung hình
- 1080×1920, 30fps, dài đúng bằng voice.
- **Cảnh theo thứ tự thời gian quay** (`creation_time`): chạy hết clip này rồi mới sang clip khác, **không cắt xen kẽ**, không quay lại clip cũ.
  Chỉ cắt ở ranh giới câu (lấy từ `transcript.json`); bỏ bớt phần đầu/cuối clip nếu dư.
- Nhịp nhanh như video mẫu: clip dài thì **cắt nhảy trong cùng clip** (vẫn đúng thứ tự, bỏ đoạn giữa), mỗi đoạn 2–7s;
  đoạn sau của cùng clip dùng zoom `2` (cận hơn 12%) để cú cắt rõ ràng. Mọi đoạn zoom chậm 7%.
- Clip ngắn hơn đoạn voice cần phủ: chạy chậm nhẹ (cột speed trong `edl.txt`, không dưới 0.85).

## Màu
**Không làm đẹp mặt / chỉnh dáng tự động.** (Chỉ dùng khi chủ kênh muốn chỉnh màu — mặc định giữ màu gốc.) Tông ấm vàng như video mẫu:
`colortemperature=temperature=4200:mix=0.7,eq=saturation=1.1:contrast=1.05,vignette=angle=PI/4.5`

## Chữ (theo video mẫu)
- **Phụ đề chính** ở 1/3 trên (top ≈ 200px): serif **Instrument Serif** trắng 84px, bóng mờ; cụm 1–3 chữ, **hiện từng chữ** đúng lúc nói (mờ → rõ, nhích lên).
- **Từ nhấn mạnh** (chọn 1 từ khoá / câu):
  - `pop` — **Inter Tight 800**, vàng chanh `#eef36a`, xuống dòng riêng, to hơn 1.2×.
  - `script` — chữ viết tay **Pinyon Script** vàng chanh, to 1.55×, nghiêng nhẹ.
  - `ital` — serif nghiêng. `big` — số rất to (vd "6").
  - `circle` — vòng elip trắng vẽ tay quanh cụm + ngôi sao lấp lánh.
- **Hook hiện đủ ngay từ 0s** (khối chữ nhiều dòng cùng style, không hiện từng chữ) — người xem biết ngay video nói gì.
- **Thẻ tiêu đề** lúc chủ kênh giới thiệu bản thân (như "Journalist becoming Creator / Eps #03" trong mẫu):
  chữ viết tay tên series + chữ đậm + dấu chấm vàng, dòng nhỏ "salon owner · Toronto", "@nailart.bytheresa", ghi chú nhỏ có elip ở trên.
- **Chip ý đánh số** ở 1/3 dưới (y ≈ 1430): "no. N ✦" viết tay vàng + tên ý serif 96px, giữ suốt đoạn ý đó.
- **Emoji sticker** (Noto Color Emoji) cạnh phụ đề, ở mép trên (y ≈ 40) để không đè chữ, nghiêng ±8°.
- Dải tối mờ ở trên và dưới khung để chữ trắng đọc được trên nền tường trắng.
- Kết: "✦ @nailart.bytheresa" ở dưới.

## Âm thanh
highpass 80Hz → khử ồn → compressor → loudnorm −14 LUFS. Chưa có nhạc nền (chờ chủ kênh gửi nhạc).
