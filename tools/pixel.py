"""Minimal pixel canvas (stdlib only): Canvas -> RGBA PNG. Pillow is not installed."""
import zlib, struct

def rgb(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

class Canvas:
    def __init__(self, w, h, bg=(0, 0, 0, 0)):
        self.w, self.h = w, h; self.px = [[bg] * w for _ in range(h)]
    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.px[y][x] = c
    def rect(self, x, y, w, h, c):
        for j in range(y, y + h):
            for i in range(x, x + w): self.set(i, j, c)
    def frame(self, x, y, w, h, c):
        self.rect(x, y, w, 1, c); self.rect(x, y + h - 1, w, 1, c); self.rect(x, y, 1, h, c); self.rect(x + w - 1, y, 1, h, c)
    def art(self, x, y, rows, pal):
        """rows: list of strings, '.' = transparent, other characters per pal."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.': self.set(x + i, y + j, pal[ch])
    def scaled(self, k):
        o = Canvas(self.w * k, self.h * k)
        for y in range(o.h):
            for x in range(o.w): o.px[y][x] = self.px[y // k][x // k]
        return o
    def save(self, path):
        raw = b''.join(b'\x00' + b''.join(bytes(p) for p in row) for row in self.px)
        def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
        open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

import math

def _ellipse(self, cx, cy, rx, ry, c, fill=False):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if (d <= 1) if fill else (0.7 <= d <= 1.15): self.set(x, y, c)

def _line(self, x0, y0, x1, y1, c):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1): self.set(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

def _paste(self, other, ox, oy):
    for y in range(other.h):
        for x in range(other.w):
            if other.px[y][x][3]: self.set(ox + x, oy + y, other.px[y][x])

def _rotated(self, deg, w, h):
    """Rotation by deg degrees (nearest neighbour) onto a new w x h canvas, centre to centre."""
    o = Canvas(w, h); a = math.radians(-deg); ca, sa = math.cos(a), math.sin(a)
    for y in range(h):
        for x in range(w):
            dx, dy = x - w / 2, y - h / 2
            sx, sy = int(dx * ca - dy * sa + self.w / 2), int(dx * sa + dy * ca + self.h / 2)
            if 0 <= sx < self.w and 0 <= sy < self.h: o.px[y][x] = self.px[sy][sx]
    return o

Canvas.ellipse, Canvas.line, Canvas.paste, Canvas.rotated = _ellipse, _line, _paste, _rotated
