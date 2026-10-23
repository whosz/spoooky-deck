"""Arkusz miniatur do przeglądu: render wielu kart do jednego PNG (cols kolumn)."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import W, H, P
from pixel import Canvas
def sheet(canvases, path, cols=6, gap=6, scale=1):
    rows = (len(canvases) + cols - 1) // cols
    s = Canvas(cols * (W + gap) + gap, rows * (H + gap) + gap, P['ink'])
    for i, c in enumerate(canvases): s.paste(c, gap + (i % cols) * (W + gap), gap + (i // cols) * (H + gap))
    (s.scaled(scale) if scale > 1 else s).save(path)
