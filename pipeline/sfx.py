"""Hiệu ứng âm thanh (SFX) tự tổng hợp bằng numpy — không dùng file có bản quyền.
graphics.py ghi danh sách cue vào <work>/sfx.json ([{t, name, gain_db}]) qua editorial.cue();
make_video.sh bước final gọi:  python3 pipeline/sfx.py <work>/sfx.json <duration> <out.wav>
Tên SFX: impact, riser, whoosh, swish, pop, ding, coin, chaching, shimmer, click."""
import json, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def _t(d):
    return np.arange(int(SR * d)) / SR


def _env(n, a=0.005, r=None, curve=4.0):
    """Envelope: attack tuyến tính a giây, rồi tắt dần mũ."""
    e = np.ones(n)
    na = max(1, int(SR * a))
    e[:na] = np.linspace(0, 1, na)
    k = np.linspace(0, 1, n - na)
    e[na:] = np.exp(-curve * k) if r is None else np.exp(-k * (n - na) / (SR * r))
    return e


def _bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def _sweep_noise(d, f0, f1, q=0.35):
    """Noise lọc dải với tâm quét f0 → f1 (whoosh)."""
    n = int(SR * d)
    out = np.zeros(n)
    seg = 1024
    for i in range(0, n, seg // 2):
        m = min(seg, n - i)
        p = i / n
        fc = f0 * (f1 / f0) ** p
        chunk = _bandnoise(m, fc * (1 - q), fc * (1 + q)) * np.hanning(m)
        out[i:i + m] += chunk
    return out / (np.abs(out).max() + 1e-9)


def whoosh(d=0.45):
    n = int(SR * d)
    x = _sweep_noise(d, 400, 5000)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return x * env


def swish(d=0.25):
    n = int(SR * d)
    return _sweep_noise(d, 3000, 9000, 0.25) * np.sin(np.linspace(0, np.pi, n)) ** 3


def pop():
    t = _t(0.09)
    f = 900 * np.exp(-t * 35) + 250            # giọt nước / bong bóng: tần số rơi nhanh
    y = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return y * _env(len(t), 0.002, curve=9)


def click():
    n = int(SR * 0.025)
    return _bandnoise(n, 2000, 9000) * _env(n, 0.0005, curve=14)


def ding(f=1568.0, d=1.1):
    t = _t(d)
    y = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (3 + 2 * h)) for h, a in [(1, 1), (2.76, .35), (5.4, .15)])
    return y * _env(len(t), 0.002, curve=0.1) / 1.5


def coin():
    a = ding(1975.5, 0.5)
    b = ding(2637.0, 0.6)
    out = np.zeros(int(SR * 0.65))
    out[:len(a)] += a
    o = int(SR * 0.07)
    out[o:o + len(b)] += b[:len(out) - o]
    return out / 1.6


def chaching():
    out = np.zeros(int(SR * 1.2))
    c = click() * 1.2
    for o in (0.0, 0.06):                       # "cha" — 2 tiếng cơ khí
        i = int(SR * o)
        out[i:i + len(c)] += c
    d = ding(2093.0, 1.0) + ding(2637.0, 1.0) * .6   # "ching"
    i = int(SR * 0.14)
    out[i:i + len(d)] += d[:len(out) - i]
    return out / (np.abs(out).max() + 1e-9)


def shimmer(d=0.9):
    out = np.zeros(int(SR * d))
    for k in range(9):
        f = rng.uniform(2500, 6500)
        o = int(SR * k * d / 12)
        g = ding(f, d * 0.6) * rng.uniform(.3, .7)
        out[o:o + len(g)] += g[:len(out) - o]
    return out / (np.abs(out).max() + 1e-9)


def riser(d=0.8):
    t = _t(d)
    n = len(t)
    tone = np.sin(2 * np.pi * np.cumsum(200 * (8 ** (t / d))) / SR)
    x = _sweep_noise(d, 300, 7000) * 0.7 + tone * 0.3
    return x * np.linspace(0, 1, n) ** 2


def impact():
    t = _t(0.9)
    f = 110 * np.exp(-t * 6) + 42               # boom: sine trầm rơi tần số
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.002, curve=5)
    n = int(SR * 0.12)
    y[:n] += _bandnoise(n, 800, 8000) * _env(n, 0.001, curve=10) * 0.5
    return y / (np.abs(y).max() + 1e-9)


SFX = dict(impact=impact, riser=riser, whoosh=whoosh, swish=swish, pop=pop, ding=ding,
           coin=coin, chaching=chaching, shimmer=shimmer, click=click)
LEVEL_DB = dict(impact=-8, riser=-11, whoosh=-11, swish=-13, pop=-8, ding=-13, coin=-12, chaching=-10, shimmer=-15, click=-12)


def render(cues, dur, out):
    track = np.zeros(int(SR * dur) + SR)
    for c in cues:
        y = SFX[c["name"]]()
        g = 10 ** ((LEVEL_DB[c["name"]] + c.get("gain_db", 0)) / 20)
        i = int(SR * max(0.0, c["t"]))
        track[i:i + len(y)] += (y * g)[:len(track) - i]
    track = track[:int(SR * dur)]
    peak = np.abs(track).max()
    if peak > 0.9:
        track *= 0.9 / peak
    st = (np.repeat(track[:, None], 2, axis=1) * 32767).astype(np.int16)
    w = wave.open(out, "wb")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(st.tobytes()); w.close()
    print(f"sfx: {len(cues)} cue -> {out}")


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), float(sys.argv[2]), sys.argv[3])
