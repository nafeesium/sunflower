import math as m
import random as r
import turtle as t
import tkinter.font as tkf

DURATION = 10
TICK = 16
ANIM = 42
LIFT = 34
GAP = 7
SIZES = (9, 10, 11, 12)
FONT = "Arial"
BG = "#060208"

HX, HY = 0, 168
DISC_R = 84
PETALS = 14
PETAL_START = 66
PETAL_LEN = 126
PETAL_W = 40
PETAL_R = PETAL_START + PETAL_LEN
STEP = 2 * m.pi / PETALS

STEM_W = 36
STEM_BOTTOM = -378
STEM_TOP = HY - 150
LEAVES = [
    (-120, m.radians(152), 180, 52),
    (-230, m.radians(28), 180, 52),
]

BROWN_D = (0.50, 0.25, 0.07)
BROWN_L = (0.76, 0.42, 0.15)
GOLD = (1.00, 0.72, 0.04)
LEMON = (1.00, 0.90, 0.22)
LEAF_D = (0.10, 0.50, 0.14)
LEAF_L = (0.34, 0.76, 0.22)
STEM_D = (0.12, 0.52, 0.14)
STEM_L = (0.28, 0.70, 0.20)
FLASH = (1.0, 0.96, 0.75)

s = t.Screen()
s.setup(800, 800)
s.bgcolor(BG)
s.title("Sunflower")
s.tracer(0)

cv = s.getcanvas()
rng = r.Random(11)

PHRASES = [
    "I love you", "Seni seviyorum", "Te amo", "Je t'aime",
    "Ich liebe dich", "Ti amo", "Eu te amo", "Я тебя люблю",
    "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करता हूँ",
    "Σ' αγαπώ", "Ik hou van jou", "Jag älskar dig", "Kocham cię",
    "ฉันรักเธอ", "Anh yêu em", "Aku cinta kamu", "Я тебе кохаю",
]

BGC = tuple(int(BG[i:i + 2], 16) / 255 for i in (1, 3, 5))
_fonts = {}


def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(
            root=cv, family=FONT, size=size, weight="bold"
        )
    return _fonts[size]


def clamp(v):
    return max(0.0, min(1.0, v))


def hx(c):
    return "#%02x%02x%02x" % tuple(int(clamp(v) * 255) for v in c)


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def dim(c, k):
    return tuple(v * k for v in c)


def stem_x(y):
    return 14 * m.sin((y - STEM_BOTTOM) / 120)


def region_at(x, y):
    dx, dy = x - HX, y - HY
    d = m.hypot(dx, dy)

    if d <= DISC_R:
        return "disc"

    if y <= STEM_TOP and abs(x - stem_x(y)) <= STEM_W and y >= STEM_BOTTOM:
        return "stem"

    if d <= PETAL_R:
        ang = m.atan2(dy, dx) - m.pi / 2
        k = round(ang / STEP)
        for j in (k - 1, k, k + 1):
            da = ang - j * STEP
            u = d * m.cos(da)
            if u < PETAL_START:
                continue
            tt = (u - PETAL_START) / PETAL_LEN
            if tt > 1:
                continue
            if abs(d * m.sin(da)) <= PETAL_W * m.sin(
                m.pi * (0.15 + 0.85 * tt ** 0.8)
            ):
                return "petal"

    for ay, th, ln, lw in LEAVES:
        lx, ly = x - stem_x(ay), y - ay
        u = lx * m.cos(th) + ly * m.sin(th)
        v = -lx * m.sin(th) + ly * m.cos(th)
        tt = u / ln
        if 0 <= tt <= 1 and abs(v) <= lw * m.sin(m.pi * tt ** 0.75):
            return "leaf"

    return None


XS = range(-300, 301, 2)


def band(y, half):
    out = []
    cur = None
    start = prev = 0
    for x in XS:
        a = region_at(x, y + half)
        b = region_at(x, y)
        c = region_at(x, y - half)
        reg = b if (b == a or b == c) else None
        if reg != cur:
            if cur:
                out.append((cur, start, prev))
            cur, start = reg, x
        prev = x
    if cur:
        out.append((cur, start, prev))
    return out


def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        yield from order


def paint(p):
    reg, x, y = p["region"], p["x"], p["y"]
    d = m.hypot(x - HX, y - HY)
    if reg == "disc":
        k = d / DISC_R
        return mix(BROWN_D, BROWN_L, clamp(0.55 * k + rng.uniform(0, 0.45)))
    if reg == "petal":
        k = clamp((d - DISC_R) / (PETAL_R - DISC_R))
        return mix(GOLD, LEMON, clamp(0.7 * k + rng.uniform(0, 0.3)))
    if reg == "leaf":
        return mix(LEAF_D, LEAF_L, rng.uniform(0, 1))
    return mix(STEM_D, STEM_L, rng.uniform(0, 1))


def build():
    cycle = phrase_cycle()
    row_h = max(font_for(z).metrics("linespace") for z in SIZES) + 4
    half = row_h / 2
    placed = []

    y = HY + PETAL_R - half
    while y > STEM_BOTTOM + half:
        for reg, lo, hi in band(y, half):
            lo += 4
            hi -= 4
            if hi - lo < 20:
                continue
            cur = lo + rng.uniform(0, 8)
            line = []

            while True:
                fit = None
                for _ in range(30):
                    text = next(cycle)
                    size = rng.choice(SIZES)
                    w = font_for(size).measure(text)
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + GAP

            if not line:
                continue

            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2

            for x, text, size, w in line:
                placed.append(
                    dict(x=x, y=y, text=text, size=size, region=reg)
                )

        y -= row_h

    for p in placed:
        p["color"] = paint(p)

    groups = {"stem": [], "leaf": [], "disc": [], "petal": []}
    for p in placed:
        groups[p["region"]].append(p)

    groups["stem"].sort(key=lambda p: p["y"])
    groups["leaf"].sort(key=lambda p: abs(p["x"] - stem_x(p["y"])))
    groups["disc"].sort(
        key=lambda p: m.hypot(p["x"] - HX, p["y"] - HY) + rng.uniform(0, 8)
    )
    groups["petal"].sort(
        key=lambda p: (m.pi / 2 - m.atan2(p["y"] - HY, p["x"] - HX))
        % (2 * m.pi)
    )
    return groups["stem"] + groups["leaf"] + groups["disc"] + groups["petal"]


main_ids = []
active = []


def spawn(p):
    x, y = p["x"], -p["y"]
    size, text, c = p["size"], p["text"], p["color"]
    font = (FONT, size, "bold")
    big = (FONT, size + 1, "bold")

    shadow = cv.create_text(x + 2, y + 3, text=text, font=font, fill=BG)
    halo = cv.create_text(x, y, text=text, font=big, fill=BG)
    main = cv.create_text(x, y - LIFT, text=text, font=font, fill=BG)

    p.update(shadow=shadow, halo=halo, main=main,
             f=0, dx=rng.uniform(-10, 10))
    main_ids.append((main, c))
    active.append(p)


def animate(p):
    p["f"] += 1
    u = clamp(p["f"] / ANIM)
    e = 1 - (1 - u) ** 3
    c = p["color"]
    x, y = p["x"], -p["y"]
    px = x + p["dx"] * (1 - e)
    py = y - (1 - e) * LIFT

    cv.itemconfig(p["shadow"], fill=hx(mix(BGC, dim(c, 0.30), e)))
    cv.itemconfig(p["halo"], fill=hx(mix(BGC, dim(c, 0.20), e * e)))
    cv.coords(p["halo"], px, py)

    flash = 0.75 * m.sin(m.pi * clamp((u - 0.55) / 0.45))
    col = mix(mix(BGC, c, e ** 1.5), FLASH, flash)
    cv.itemconfig(p["main"], fill=hx(col))
    cv.coords(p["main"], px, py)

    if u >= 1:
        cv.coords(p["halo"], x, y)
        cv.coords(p["main"], x, y)
        cv.itemconfig(p["main"], fill=hx(c))
        return False
    return True


ORDER = build()
items = iter(ORDER)
RATE = len(ORDER) / (DURATION * 1000 / TICK)
acc = 0.0
spawning = True


def step():
    global spawning, acc
    if spawning:
        acc += RATE
        try:
            while acc >= 1:
                acc -= 1
                spawn(next(items))
        except StopIteration:
            spawning = False

    active[:] = [p for p in active if animate(p)]

    if not spawning and not active:
        shimmer()
        return
    cv.after(TICK, step)


def _safe(i, c):
    try:
        cv.itemconfig(i, fill=hx(c))
    except Exception:
        pass


def shimmer():
    i, c = rng.choice(main_ids)
    _safe(i, mix(c, FLASH, 0.6))
    cv.after(260, lambda: _safe(i, c))
    cv.after(140, shimmer)


try:
    cv.after(200, step)
    t.done()
except (t.Terminator, Exception):
    pass