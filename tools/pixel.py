"""Minimalny rysownik pikseli (tylko stdlib): Canvas -> PNG RGBA. Pillow nie jest zainstalowany."""
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
        """rows: lista napisow, znak '.' = przezroczysty, inne wg pal."""
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
