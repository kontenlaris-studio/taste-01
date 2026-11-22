"""Draw the taste-01 artwork: golden honey, one ingredient, macro shot.

Procedural Pillow drawing, no assets: warm amber backdrop, a honeycomb
cluster, a wooden honey dipper pouring a thick glossy ribbon, drips and a
honey pool. Built at build time only; main.py serves the stored PNG.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(
            int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def hex_points(cx, cy, r, rot=0.0):
    return [(cx + r * math.cos(rot + math.radians(60 * k)),
             cy + r * math.sin(rot + math.radians(60 * k))) for k in range(6)]


def gloss(draw, box, alpha=90):
    """Soft white specular ellipse on an RGBA overlay."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse(box, fill=(255, 250, 230, alpha))
    ov = ov.filter(ImageFilter.GaussianBlur(6))
    draw._image.paste(ov, (0, 0), ov)


def build_artwork_bytes():
    # --- backdrop: warm amber gradient + radial glow top-left ---
    img = vgrad(W, H, (58, 30, 8), (24, 12, 4))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-500, -500, 700, 700], fill=(255, 170, 60, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)

    # --- honeycomb cluster (center-right, tilted) ---
    comb_cx, comb_cy = 560, 560
    cell_r = 92
    cells = []
    for row in range(4):
        for col in range(4):
            x = comb_cx + (col - 1.5) * cell_r * 1.72 + (row % 2) * cell_r * 0.86
            y = comb_cy + (row - 1.5) * cell_r * 1.55
            cells.append((x, y))
    for (x, y) in cells:
        pts = hex_points(x, y, cell_r, rot=math.radians(30))
        d.polygon(pts, fill=(176, 104, 8), outline=(90, 48, 4))
        inner = hex_points(x, y, cell_r * 0.80, rot=math.radians(30))
        d.polygon(inner, fill=(232, 148, 18), outline=(255, 190, 60))
        # glossy top-left facet on each cell
        d.polygon([inner[0], inner[1], (x, y)], fill=(255, 205, 90))
        d.polygon(inner, outline=(120, 66, 6))

    # --- thick honey ribbon pouring from top-left: smooth wavy band ---
    def stream_x(y):
        t = (y + 20) / 10.4
        return 205 + 55 * math.sin(t * 0.16) + 18 * math.sin(t * 0.42)

    left, right = [], []
    for y in range(-20, 881, 12):
        wdt = 30 + 6 * math.sin(y / 260.0)
        left.append((stream_x(y) - wdt, y))
        right.append((stream_x(y) + wdt, y))
    d.polygon(left + right[::-1], fill=(244, 164, 22))
    # smooth highlight band along the stream's left edge
    hl_l, hl_r = [], []
    for y in range(-20, 881, 12):
        wdt = 30 + 6 * math.sin(y / 260.0)
        hl_l.append((stream_x(y) - wdt + 8, y))
        hl_r.append((stream_x(y) - wdt + 20, y))
    d.polygon(hl_l + hl_r[::-1], fill=(255, 220, 130))
    # splash mound where the stream lands on the pool
    d.ellipse([160, 836, 330, 926], fill=(244, 164, 22))
    d.ellipse([190, 856, 300, 906], fill=(255, 210, 100))

    # --- wooden honey dipper, diagonal across upper area ---
    dip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dip)
    # handle
    dd.line([(700, 120), (470, 330)], fill=(122, 74, 30, 255), width=34)
    dd.line([(700, 120), (470, 330)], fill=(160, 100, 44, 255), width=20)
    # grooved head (stacked rounded discs, spaced so grooves read)
    for i in range(5):
        cx = 430 - i * 30
        cy = 360 + i * 30
        dd.ellipse([cx - 46, cy - 22, cx + 46, cy + 22], fill=(146, 90, 36, 255))
        dd.ellipse([cx - 46, cy - 22, cx + 46, cy - 2], fill=(186, 118, 48, 255))
    dip = dip.filter(ImageFilter.GaussianBlur(1))
    img = Image.alpha_composite(img, dip)
    d = ImageDraw.Draw(img)
    # honey coating on dipper head + drip falling from it
    d.ellipse([322, 448, 408, 508], fill=(244, 164, 22))
    d.ellipse([336, 458, 392, 494], fill=(255, 210, 100))
    d.polygon([(352, 520), (368, 520), (388, 640), (372, 700), (352, 640)],
              fill=(244, 164, 22))
    d.ellipse([352, 660, 392, 720], fill=(244, 164, 22))
    d.ellipse([358, 668, 380, 700], fill=(255, 214, 110))

    # --- honey pool at the bottom ---
    d.ellipse([120, 880, 940, 1010], fill=(226, 138, 14))
    d.ellipse([170, 900, 890, 985], fill=(244, 164, 22))
    d.ellipse([260, 912, 700, 952], fill=(255, 205, 92))
    d.ellipse([300, 918, 520, 940], fill=(255, 232, 160))

    # --- final gloss + vignette: small sharp speculars only ---
    gloss(d, [640, 660, 830, 760], alpha=45)
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-260, -260, W + 260, H + 260], outline=(0, 0, 0, 80), width=180)
    vig = vig.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, vig)

    out = img.convert("RGB")
    import io
    buf = io.BytesIO()
    out.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


if __name__ == "__main__":
    data = build_artwork_bytes()
    open("artwork.png", "wb").write(data)
    print("artwork.png:", len(data), "bytes")
