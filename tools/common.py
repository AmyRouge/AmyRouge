"""Shared building blocks for the profile SVGs: fonts, palette, card chrome, icons, text metrics."""
import base64, json, math, os
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')          # fonts + icon paths (committed)
CACHE = os.path.join(HERE, '.cache')       # cutouts, frames, encoded assets (generated)
OUT = os.path.join(HERE, '..', 'assets')   # finished SVGs

BG = '#0d0e16'
CYAN, VIOLET, PINK = '#22d3ee', '#a78bfa', '#f472b6'
INK, MUTED, FAINT = '#e7e9f5', '#9aa0bf', '#5d6283'

ASSETS = json.load(open(os.path.join(CACHE, 'assets.json')))
ICONS = json.load(open(os.path.join(DATA, 'icons.json')))

# ---------------------------------------------------------------- fonts
_FONT_FILES = {('SG', 500): 'sg500', ('SG', 700): 'sg700', ('JB', 400): 'jb400', ('JB', 700): 'jb700'}
_FONTS = {k: TTFont(os.path.join(DATA, v + '.woff2')) for k, v in _FONT_FILES.items()}
_USED = set()


def font_css(families=('SG', 'JB')):
    css = []
    for (fam, w), f in _FONT_FILES.items():
        if fam not in families:
            continue
        data = base64.b64encode(open(os.path.join(DATA, f + '.woff2'), 'rb').read()).decode()
        name = 'Grotesk' if fam == 'SG' else 'Mono'
        css.append(f"@font-face{{font-family:'{name}';font-weight:{w};font-style:normal;"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return '\n'.join(css)


def measure(text, fam='SG', weight=500, size=16, spacing=0.0):
    """Advance width of text in px (no kerning) — good enough to lay out chips and caret positions."""
    f = _FONTS[(fam, weight)]
    cmap, hmtx = f.getBestCmap(), f['hmtx']
    upm = f['head'].unitsPerEm
    w = 0
    for ch in text:
        if ord(ch) not in cmap:
            raise ValueError(f'glyph {ch!r} (U+{ord(ch):04X}) missing from {fam}{weight}')
        w += hmtx[cmap[ord(ch)]][0]
    return w * size / upm + spacing * max(len(text) - 1, 0)


def t(x, y, text, size=16, fam='SG', weight=500, fill=INK, anchor=None, extra=''):
    measure(text, fam, weight, size)  # validates glyph coverage
    family = 'Grotesk' if fam == 'SG' else 'Mono'
    a = f' text-anchor="{anchor}"' if anchor else ''
    return (f'<text x="{x:g}" y="{y:g}" font-family="{family}, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{a} {extra}>{escape(text)}</text>')


# ---------------------------------------------------------------- icons
def lighten_if_dark(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return '#e7e9f5' if lum < 60 else '#' + hexcol


def icon(slug, x, y, size, color=None, extra=''):
    """Simple Icons glyph (24x24 viewBox) placed with its top-left at x,y."""
    ic = ICONS[slug]
    s = size / 24
    col = color or lighten_if_dark(ic['hex'])
    return f'<path transform="translate({x:g} {y:g}) scale({s:g})" d="{ic["path"]}" fill="{col}" {extra}/>'


def icon_color(slug):
    return lighten_if_dark(ICONS[slug]['hex'])


# ---------------------------------------------------------------- card chrome
def card_defs(p):
    """Defs shared by every card: dot texture, aurora ramps, hairline border gradient, soft glow filter."""
    return f'''
  <pattern id="{p}-dots" width="16" height="16" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="0.9" fill="#ffffff" fill-opacity="0.055"/>
  </pattern>
  <linearGradient id="{p}-aurora" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="{p}-hair" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.75"/>
    <stop offset="0.35" stop-color="#ffffff" stop-opacity="0.08"/>
    <stop offset="0.65" stop-color="{VIOLET}" stop-opacity="0.18"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity="0.7"/>
  </linearGradient>
  <radialGradient id="{p}-sheen" cx="0.15" cy="0" r="0.9">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.10"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <filter id="{p}-glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
  <filter id="{p}-blur40" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="40"/>
  </filter>'''


def card(p, x, y, w, h, rx=20):
    return f'''
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{BG}"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{p}-sheen)"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{p}-dots)"/>
    <rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{rx - 0.5}" fill="none" stroke="url(#{p}-hair)" stroke-width="1"/>
  </g>'''


def svg_doc(w, h, title, desc, defs, body, css='', families=('SG', 'JB')):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<style>
{font_css(families)}
{css}
</style>
<defs>{defs}
</defs>
{body}
</svg>
'''


# ---------------------------------------------------------------- SMIL helpers
def kt(*vals):
    """Format keyTimes / keyPoints, clamped & monotonic-safe."""
    return ';'.join(f'{min(max(v, 0), 1):.4f}'.rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v)) for v in vals)


def ellipse_path(cx, cy, rx, ry, rot_deg, n=96, start_deg=0):
    """Closed polyline path around a rotated ellipse (so things riding it stay upright)."""
    r = math.radians(rot_deg)
    pts = []
    for i in range(n + 1):
        a = math.radians(start_deg) + 2 * math.pi * i / n
        ex, ey = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + ex * math.cos(r) - ey * math.sin(r), cy + ex * math.sin(r) + ey * math.cos(r)))
    return 'M' + ' L'.join(f'{px:.1f} {py:.1f}' for px, py in pts) + ' Z', pts
