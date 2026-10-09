from common import *

P = 'c'
W, H = 1200, 420

pw, ph = ASSETS['point_size']
IH = 384
IW = pw * IH / ph
IX, IY = 54, 22
TIP = (IX + 661 * IH / 1410, IY + 326 * IH / 1410)   # fingertip in card coords

pin = '<path d="M0 -9 a7 7 0 0 1 7 7 c0 5.5 -7 12 -7 12 s-7 -6.5 -7 -12 a7 7 0 0 1 7 -7 z M0 -4.6 a2.6 2.6 0 1 0 0.01 0"/>'
bld = '<path d="M-7 10 V-8 h9 v18 M2 -2 h6 v12 M-10 10 h20 M-4 -4 h3 M-4 0 h3 M-4 4 h3"/>'
LINKS = [
    ('github', None, 'GitHub', 'github.com/AmyRouge', 'code, side projects & experiments'),
    ('gmail', None, 'Email', 'akeshidewmini@gmail.com', 'the best way to reach me'),
    (None, bld, 'WindsorGaming', 'github.com/WindsorGaming', 'where I work'),
    (None, pin, 'Based in', 'Colombo, Sri Lanka', 'GMT+5:30 · open to remote'),
]
LX, LY = 360, 132
GAP = 16
CWd = (W - 28 - LX - GAP) / 2
CHt = 116
cards = []
for i, (slug, glyph, title, handle, sub) in enumerate(LINKS):
    x = LX + (i % 2) * (CWd + GAP)
    y = LY + (i // 2) * (CHt + GAP)
    col = icon_color(slug) if slug else [CYAN, VIOLET, PINK, CYAN][i]
    accent = [CYAN, PINK, VIOLET, CYAN][i]
    tile = (icon(slug, x + 32, y + 32, 28) if slug else
            f'<g transform="translate({x + 46} {y + 46})" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>')
    assert 92 + measure(handle, 'JB', 700, 14) < CWd - 56, handle
    cards.append(f'''
  <g class="fu" style="animation-delay:{0.35 + i * 0.12:.2f}s">
    <rect x="{x:.1f}" y="{y}" width="{CWd:.1f}" height="{CHt}" rx="16" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.09"/>
    <rect x="{x:.1f}" y="{y}" width="{CWd:.1f}" height="{CHt}" rx="16" fill="none" stroke="{accent}" stroke-width="1.2" opacity="0">
      <animate attributeName="opacity" values="0;0;0.8;0;0" keyTimes="0;{i * 0.2:.2f};{i * 0.2 + 0.08:.2f};{i * 0.2 + 0.24:.2f};1" dur="8s" begin="0s" repeatCount="indefinite"/></rect>
    <rect x="{x + 22}" y="{y + 22}" width="48" height="48" rx="13" fill="{accent}" fill-opacity="0.09" stroke="{accent}" stroke-opacity="0.35"/>
    {tile}
    {t(x + 88, y + 38, title, 17, 'SG', 700, INK)}
    {t(x + 88, y + 60, handle, 14, 'JB', 700, accent)}
    {t(x + 88, y + 90, sub, 13, 'SG', 500, MUTED)}
    <g transform="translate({x + CWd - 40:.1f} {y + CHt / 2})">
      <g class="nudge" style="animation-delay:{i * 0.18:.2f}s">
        <circle r="15" fill="#ffffff" fill-opacity="0.05" stroke="#ffffff" stroke-opacity="0.12"/>
        <path d="M-5 0 h10 M1 -5 l5 5 -5 5" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
  </g>''')

sparkle = 'M0 -8 C1 -2 2 -1 8 0 C2 1 1 2 0 8 C-1 2 -2 1 -8 0 C-2 -1 -1 -2 0 -8z'
sparks = ''.join(f'''<g transform="translate({sx} {sy}) scale({sc})"><path d="{sparkle}" fill="{col}">
    <animate attributeName="opacity" values="0.2;1;0.2" dur="{d}s" begin="0s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="scale" values="0.7;1.15;0.7" dur="{d}s" begin="0s" repeatCount="indefinite"/></path></g>'''
                 for sx, sy, sc, col, d in [(TIP[0] + 30, TIP[1] - 30, 1.2, CYAN, 1.8), (TIP[0] + 58, TIP[1] + 4, 0.8, PINK, 2.3),
                                            (IX + 20, IY + 160, 0.9, VIOLET, 2.0), (IX + IW - 10, IY + 250, 0.7, CYAN, 2.6)])

# a dashed "look here" trail from the fingertip towards the cards
trail = f'M{TIP[0] + 14:.0f} {TIP[1]:.0f} C {TIP[0] + 70:.0f} {TIP[1] - 50:.0f}, {LX - 60} {LY - 70}, {LX - 14} {LY - 14}'
body = f'''{card(P, 1, 1, W - 2, H - 2)}
  <g clip-path="url(#{P}-cardclip)">
    <circle class="blob" cx="{IX + IW / 2:.0f}" cy="{H - 60}" r="150" fill="{VIOLET}" fill-opacity="0.18" filter="url(#{P}-blur40)"/>
  </g>
  <ellipse cx="{IX + IW / 2:.0f}" cy="{IY + IH + 2}" rx="70" ry="8" fill="#000000" fill-opacity="0.4" filter="url(#{P}-glow)"/>
  <g class="float">
    <image x="{IX}" y="{IY}" width="{IW:.0f}" height="{IH}" href="data:image/png;base64,{ASSETS['point']}"/>
  </g>
  {sparks}
  <path d="{trail}" fill="none" stroke="url(#{P}-aurora)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="3 7">
    <animate attributeName="stroke-dashoffset" values="0;-40" dur="1.2s" begin="0s" repeatCount="indefinite"/></path>
  <path d="M{LX - 22} {LY - 16} l8 2 -2 -8" fill="none" stroke="{PINK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" transform="rotate(0)"/>
  <g class="fu" style="animation-delay:.1s">
    {t(LX, 50, '// connect', 12, 'JB', 400, FAINT)}
    {t(LX, 84, "Let's build something together", 28, 'SG', 700, f'url(#{P}-aurora)')}
    {t(LX, 110, 'Collabs, questions, or just to say hi — my inbox is open.', 15, 'SG', 500, MUTED)}
  </g>
  {''.join(cards)}'''

css = '''
.fu{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes fu{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.float{animation:float 4.5s ease-in-out infinite both}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.nudge{animation:nudge 1.6s ease-in-out infinite both}
@keyframes nudge{0%,55%,100%{transform:translateX(0)}25%{transform:translateX(6px)}}
.blob{animation:drift 12s ease-in-out infinite alternate both}
@keyframes drift{from{transform:translate(0,0)}to{transform:translate(30px,-20px)}}
'''
defs = card_defs(P) + f'''
  <clipPath id="{P}-cardclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20"/></clipPath>'''
svg = svg_doc(W, H, "Let's connect",
              'Character pointing at contact cards: GitHub github.com/AmyRouge, email akeshidewmini@gmail.com, WindsorGaming, based in Colombo, Sri Lanka.',
              defs, body, css)
open(os.path.join(OUT, 'connect.svg'), 'w', encoding='utf-8').write(svg)
print('connect.svg', len(svg) // 1024, 'KB')
