from common import *

P = 'a'
W, H = 1200, 560
CW = 584


def f(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))


def header(x, y, kicker, title):
    return t(x, y, kicker, 12, 'JB', 400, FAINT) + t(x, y + 26, title, 22, 'SG', 700, INK)


# ================================================================ LEFT CARD
LX0 = 0
BX, BY, BW, BH = 24, 84, 536, 236
lap_w, lap_h = ASSETS['laptop_size']
IH = 226
IW = lap_w * IH / lap_h
code = [
    [('const ', VIOLET), ('akeshi', CYAN), (' = {', MUTED)],
    [('  role', INK), (': ', MUTED), ('"Software Engineer"', PINK), (',', MUTED)],
    [('  base', INK), (': ', MUTED), ('"Colombo, LK"', PINK), (',', MUTED)],
    [('  team', INK), (': ', MUTED), ('"WindsorGaming"', PINK), (',', MUTED)],
    [('  loves', INK), (': [', MUTED), ('"music"', PINK), (', ', MUTED), ('"art"', PINK), (',', MUTED)],
    [('    ', INK), ('"anime"', PINK), (', ', MUTED), ('"games"', PINK), ('],', MUTED)],
    [('  coffee', INK), (': ', MUTED), ('true', CYAN)],
    [('};', MUTED)],
]
code_svg = []
for i, line in enumerate(code):
    x = BX + 22
    y = BY + 66 + i * 20
    parts = []
    for txt, col in line:
        parts.append(f'<tspan fill="{col}">{escape(txt)}</tspan>')
        measure(txt, 'JB', 400, 12.5)
    code_svg.append(f'<text class="fu" style="animation-delay:{0.5 + i * 0.12:.2f}s" x="{x}" y="{y}" font-family="Mono" font-size="12.5" xml:space="preserve">{"".join(parts)}</text>')
    code_svg.append(t(BX + 4, y, str(i + 1), 10, 'JB', 400, '#3a3e58'))
url = 'akeshi.dev/about'
ux = BX + 104
url_w = measure(url, 'JB', 400, 12)
browser = f'''
  <g class="fu" style="animation-delay:.1s">
    <rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="14" fill="#11121d" stroke="#ffffff" stroke-opacity="0.09"/>
    <path d="M{BX} {BY + 34} H{BX + BW}" stroke="#ffffff" stroke-opacity="0.07"/>
    <circle cx="{BX + 18}" cy="{BY + 17}" r="5" fill="#ff5f57" fill-opacity="0.8"/>
    <circle cx="{BX + 35}" cy="{BY + 17}" r="5" fill="#febc2e" fill-opacity="0.8"/>
    <circle cx="{BX + 52}" cy="{BY + 17}" r="5" fill="#28c840" fill-opacity="0.8"/>
    <rect x="{BX + 80}" y="{BY + 7}" width="{BW - 100}" height="20" rx="10" fill="#ffffff" fill-opacity="0.05"/>
    <path d="M{BX + 92} {BY + 16} v-2.5 a3 3 0 0 1 6 0 v2.5" fill="none" stroke="{MUTED}" stroke-width="1.3"/>
    <rect x="{BX + 90.5}" y="{BY + 15.5}" width="9" height="7" rx="1.5" fill="{MUTED}"/>
    {t(ux, BY + 21, url, 12, 'JB', 400, MUTED)}
    <rect x="{ux + url_w + 2:.1f}" y="{BY + 10}" width="1.6" height="14" fill="{CYAN}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.05s" begin="0s" repeatCount="indefinite"/>
    </rect>
    <g clip-path="url(#{P}-winclip)">
      <rect x="{BX}" y="{BY + 34}" width="{BW}" height="{BH - 34}" fill="url(#{P}-winbg)"/>
      <circle cx="{BX + BW - 110}" cy="{BY + 150}" r="92" fill="{VIOLET}" fill-opacity="0.18" filter="url(#{P}-glow)"/>
      {''.join(code_svg)}
      <g class="float">
        <image x="{BX + BW - IW - 6:.0f}" y="{BY + BH - IH + 14}" width="{IW:.0f}" height="{IH}" href="data:image/png;base64,{ASSETS['laptop']}"/>
      </g>
      <g font-family="Mono" font-size="15" font-weight="700">
        <text class="bob" x="{BX + BW - 236}" y="{BY + 78}" fill="{CYAN}" fill-opacity="0.75">&lt;/&gt;</text>
        <text class="bob" style="animation-delay:-1.3s" x="{BX + BW - 44}" y="{BY + 70}" fill="{PINK}" fill-opacity="0.75">{{ }}</text>
      </g>
    </g>
  </g>'''

# capability rows
caps = [
    ('Teamwork', 'Pair up, unblock others, share the win.', CYAN,
     '<circle cx="-4" cy="-3" r="3"/><circle cx="5" cy="-2" r="2.4"/><path d="M-10 7 c0-5 3-6.5 6-6.5 s6 1.5 6 6.5 M3 2.5 c3.5-.6 7 .8 7 4.5"/>'),
    ('Leadership', 'Set direction, keep the team calm and moving.', VIOLET,
     '<path d="M-6 9 V-8 M-6 -8 h11 l-2.5 4 2.5 4 h-11"/>'),
    ('Communication', 'Clear updates, kind reviews, no surprises.', PINK,
     '<path d="M-9 -6 h18 v11 h-9 l-5 4 v-4 h-4 z M-5 -1 h10 M-5 2 h6"/>'),
]
rows = []
for i, (title, sub, col, glyph) in enumerate(caps):
    y = 342 + i * 58
    rows.append(f'''
  <g class="fu" style="animation-delay:{0.9 + i * 0.15:.2f}s">
    <rect x="24" y="{y}" width="44" height="44" rx="12" fill="{col}" fill-opacity="0.1" stroke="{col}" stroke-opacity="0.4"/>
    <g transform="translate(46 {y + 22})" fill="none" stroke="{col}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>
    {t(84, y + 19, title, 16, 'SG', 700, INK)}
    {t(84, y + 38, sub, 13.5, 'SG', 500, MUTED)}
    <rect x="{CW - 70}" y="{y + 18}" width="44" height="6" rx="3" fill="#ffffff" fill-opacity="0.06"/>
    <rect x="{CW - 70}" y="{y + 18}" width="{[40, 34, 38][i]}" height="6" rx="3" fill="{col}" class="grow" style="animation-delay:{1.2 + i * 0.15:.2f}s"/>
  </g>''')
# more soft skills as chips
extra = ['Problem-solving', 'Adaptability', 'Creativity', 'Time management', 'Empathy']
cx = 24
chips = [t(24, 530, '+', 14, 'JB', 700, FAINT)]
cx = 42
for i, s in enumerate(extra):
    w = measure(s, 'SG', 500, 12) + 20
    chips.append(f'''<g class="fu" style="animation-delay:{1.5 + i * 0.08:.2f}s">
      <rect x="{cx:.1f}" y="514" width="{w:.1f}" height="24" rx="12" fill="#ffffff" fill-opacity="0.04" stroke="#ffffff" stroke-opacity="0.1"/>
      {t(cx + w / 2, 530, s, 12, 'SG', 500, MUTED, 'middle')}</g>''')
    cx += w + 8
assert cx < CW - 16, cx
left = card(P, 1, 1, CW - 2, H - 2) + header(24, 38, '// about.me', 'What I bring to a team') + browser + ''.join(rows) + ''.join(chips)

# ================================================================ RIGHT CARD
X0 = W - CW
SX, SY, SW, SH = X0 + 24, 96, CW - 48, 282
N, SLOT, TR = 4, 4.0, 0.5
LOOP = N * SLOT

# segment progress bars
seg_gap = 6
seg_w = (SW - seg_gap * (N - 1)) / N
segs = []
for i in range(N):
    x = SX + i * (seg_w + seg_gap)
    a, z = i * SLOT / LOOP, (i + 1) * SLOT / LOOP
    if i == 0:
        vals, kts = f'0;{seg_w:.1f};{seg_w:.1f}', f'0;{f(z)};1'
    elif i == N - 1:
        vals, kts = f'0;0;{seg_w:.1f}', f'0;{f(a)};1'
    else:
        vals, kts = f'0;0;{seg_w:.1f};{seg_w:.1f}', f'0;{f(a)};{f(z)};1'
    base = seg_w if i == 0 else 0
    segs.append(f'''<rect x="{x:.1f}" y="76" width="{seg_w:.1f}" height="3" rx="1.5" fill="#ffffff" fill-opacity="0.12"/>
    <rect x="{x:.1f}" y="76" width="{base:.1f}" height="3" rx="1.5" fill="{INK}">
      <animate attributeName="width" values="{vals}" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></rect>''')


def slide_anim(i):
    """opacity + slide transform for slide i on the shared 16s timeline (crossfade during TR)."""
    s, e = i * SLOT, (i + 1) * SLOT
    if i == 0:
        kts = f'0;{f((e - TR) / LOOP)};{f(e / LOOP)};{f((LOOP - TR) / LOOP)};1'
        return (f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;-70 0;70 0;0 0" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>')
    if i == N - 1:
        kts = f'0;{f((s - TR) / LOOP)};{f(s / LOOP)};{f((e - TR) / LOOP)};1'
        return (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="70 0;70 0;0 0;0 0;-70 0" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>')
    kts = f'0;{f((s - TR) / LOOP)};{f(s / LOOP)};{f((e - TR) / LOOP)};{f(e / LOOP)};1'
    return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="70 0;70 0;0 0;0 0;-70 0;-70 0" keyTimes="{kts}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>')


# --- illustrations, drawn in stage-local coordinates (0..SW, 0..SH), centre ~ (SW/2, 140)
cxs = SW / 2


def bars(x0, y0, n, w, gap, hmax, col, period=1.2):
    out = []
    for k in range(n):
        h1, h2, h3 = [hmax * v for v in ((0.3 + 0.7 * ((k * 37) % 10) / 10), (0.25 + 0.75 * ((k * 53 + 3) % 10) / 10), (0.35 + 0.65 * ((k * 71 + 5) % 10) / 10))]
        x = x0 + k * (w + gap)
        out.append(f'''<rect x="{x:.1f}" y="{y0 - h1:.1f}" width="{w}" height="{h1:.1f}" rx="{w / 2}" fill="{col}">
          <animate attributeName="height" values="{h1:.1f};{h2:.1f};{h3:.1f};{h1:.1f}" dur="{period + (k % 3) * 0.17:.2f}s" begin="0s" repeatCount="indefinite"/>
          <animate attributeName="y" values="{y0 - h1:.1f};{y0 - h2:.1f};{y0 - h3:.1f};{y0 - h1:.1f}" dur="{period + (k % 3) * 0.17:.2f}s" begin="0s" repeatCount="indefinite"/></rect>''')
    return ''.join(out)


def note(x, y, col, d, delay):
    return f'''<g transform="translate({x} {y})"><g class="note" style="animation-delay:{delay}s">
      <path d="M0 0 v-22 l12 -4 v20" fill="none" stroke="{col}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      <ellipse cx="-3.5" cy="0" rx="5" ry="3.8" fill="{col}"/><ellipse cx="8.5" cy="-6" rx="5" ry="3.8" fill="{col}"/></g></g>'''


music = f'''
  <rect width="{SW}" height="{SH}" fill="url(#{P}-s0)"/>
  <g transform="translate({cxs - 70} 52)">
    <path d="M10 92 V70 a60 60 0 0 1 120 0 V92" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>
    <path d="M10 92 V70 a60 60 0 0 1 120 0 V92" fill="none" stroke="{VIOLET}" stroke-width="4" stroke-linecap="round" stroke-opacity="0.6"/>
    <rect x="-8" y="78" width="34" height="58" rx="15" fill="url(#{P}-cup)"/>
    <rect x="114" y="78" width="34" height="58" rx="15" fill="url(#{P}-cup)"/>
    <rect x="-1" y="88" width="20" height="38" rx="9" fill="{BG}" fill-opacity="0.35"/>
    <rect x="121" y="88" width="20" height="38" rx="9" fill="{BG}" fill-opacity="0.35"/>
  </g>
  <g>{bars(cxs - 112, 250, 19, 8, 4.5, 56, f"url(#{P}-eq)")}</g>
  {note(80, 120, CYAN, '', 0)}{note(SW - 92, 98, PINK, '', -1.4)}{note(SW - 150, 210, VIOLET, '', -2.6)}'''

# drawing: a sketch that draws itself, with a pencil and swatches
sketch = 'M60 160 C 70 80, 150 60, 170 120 S 250 190, 280 110 M190 70 l8 16 18 2 -13 12 3 18 -16 -9 -16 9 3 -18 -13 -12 18 -2 z'
drawing = f'''
  <rect width="{SW}" height="{SH}" fill="url(#{P}-s1)"/>
  <g transform="translate({cxs - 170} 34) rotate(-4 170 110)">
    <rect x="0" y="0" width="340" height="220" rx="12" fill="#f5f3ff" fill-opacity="0.95"/>
    <g stroke="#c4b5fd" stroke-opacity="0.35">{''.join(f'<line x1="18" x2="322" y1="{28 + k * 22}" y2="{28 + k * 22}"/>' for k in range(8))}</g>
    <path d="{sketch}" fill="none" stroke="#7c3aed" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="0">
      <animate attributeName="stroke-dashoffset" values="900;0;0" keyTimes="0;0.6;1" dur="4s" begin="0s" repeatCount="indefinite"/>
    </path>
    <circle cx="300" cy="190" r="10" fill="{PINK}"/><circle cx="276" cy="196" r="8" fill="{CYAN}"/><circle cx="256" cy="200" r="6" fill="#facc15"/>
  </g>
  <g transform="translate({cxs + 120} 70) rotate(35)">
    <animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;-14 10;6 -6;0 0" dur="2.2s" begin="0s" repeatCount="indefinite"/>
    <rect x="-7" y="-70" width="14" height="70" rx="3" fill="#facc15"/>
    <rect x="-7" y="-80" width="14" height="12" rx="3" fill="{PINK}"/>
    <path d="M-7 0 L0 16 L7 0 z" fill="#f5d0a9"/><path d="M-2.5 10 L0 16 L2.5 10 z" fill="#1f2937"/>
  </g>'''

# anime: a little screen with a play button, falling sakura petals, a speech bubble
petals = []
for k in range(9):
    x = 30 + (k * 61) % (SW - 60)
    dur = 4.5 + (k % 4) * 0.8
    off = (k * 0.37) % 1
    petals.append(f'''<path d="M0 0 c4 -6 10 -6 10 0 c0 6 -6 9 -10 12 c-4 -3 -10 -6 -10 -12 c0 -6 6 -6 10 0z" fill="{PINK}" fill-opacity="{0.45 + (k % 3) * 0.15:.2f}" transform="scale(0.8)">
      <animateMotion path="M{x} -20 C {x + 40} 60, {x - 40} 160, {x + 20} {SH + 20}" keyPoints="{f(off)};1;0;{f(off)}" keyTimes="0;{f(1 - off)};{f(1 - off)};1" calcMode="linear" dur="{dur}s" begin="0s" repeatCount="indefinite" rotate="auto"/></path>''')
anime = f'''
  <rect width="{SW}" height="{SH}" fill="url(#{P}-s2)"/>
  <g transform="translate({cxs - 120} 46)">
    <rect x="0" y="0" width="240" height="150" rx="16" fill="#0b0c14" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="2"/>
    <rect x="10" y="10" width="220" height="130" rx="10" fill="url(#{P}-screen)"/>
    <circle cx="70" cy="110" r="38" fill="#ffffff" fill-opacity="0.12"/>
    <path d="M150 140 q30 -60 70 -40 v40 z" fill="#ffffff" fill-opacity="0.1"/>
    <circle cx="120" cy="75" r="26" fill="#ffffff" fill-opacity="0.92"/>
    <path d="M112 62 L134 75 L112 88 z" fill="{VIOLET}"/>
    <rect x="96" y="150" width="48" height="10" fill="#1a1b2b"/><rect x="72" y="160" width="96" height="8" rx="4" fill="#1a1b2b"/>
    <rect x="10" y="130" width="220" height="4" fill="#ffffff" fill-opacity="0.15"/>
    <rect x="10" y="130" width="160" height="4" fill="{PINK}">
      <animate attributeName="width" values="40;220" dur="4s" begin="0s" repeatCount="indefinite"/></rect>
  </g>
  <g transform="translate({cxs + 120} 46)"><g class="bob">
    <path d="M0 0 h86 a12 12 0 0 1 12 12 v26 a12 12 0 0 1 -12 12 h-56 l-14 12 v-12 h-16 a12 12 0 0 1 -12 -12 v-26 a12 12 0 0 1 12 -12z" fill="#ffffff" fill-opacity="0.92"/>
    {t(43, 32, 'one more', 13, 'SG', 700, '#4c1d95', 'middle')}
  </g></g>
  {''.join(petals)}'''

# games: a controller with glowing buttons, pixel hearts and a 1UP
heart = '<path d="M2 0h2v1h1V0h2v1h1v3H7v1H6v1H5v1H3V6H2V5H1V4H0V1h1V0z" />'
games = f'''
  <rect width="{SW}" height="{SH}" fill="url(#{P}-s3)"/>
  <g transform="translate({cxs - 130} 70)">
    <path d="M60 0 h140 c40 0 60 40 60 90 c0 40 -30 60 -55 40 l-30 -24 h-90 l-30 24 c-25 20 -55 0 -55 -40 c0 -50 20 -90 60 -90z" fill="#1c1d2e" stroke="{VIOLET}" stroke-opacity="0.6" stroke-width="2"/>
    <path d="M52 52 h14 v-14 h14 v14 h14 v14 h-14 v14 h-14 v-14 h-14z" fill="#3b3f5c"/>
    <circle cx="190" cy="44" r="10" fill="{CYAN}"><animate attributeName="fill-opacity" values="1;0.3;1" dur="1.2s" begin="0s" repeatCount="indefinite"/></circle>
    <circle cx="210" cy="64" r="10" fill="{PINK}"><animate attributeName="fill-opacity" values="0.3;1;0.3" dur="1.2s" begin="0s" repeatCount="indefinite"/></circle>
    <circle cx="170" cy="64" r="10" fill="#facc15"><animate attributeName="fill-opacity" values="1;0.3;1" dur="0.9s" begin="0s" repeatCount="indefinite"/></circle>
    <circle cx="190" cy="84" r="10" fill="{VIOLET}"><animate attributeName="fill-opacity" values="0.3;1;0.3" dur="0.9s" begin="0s" repeatCount="indefinite"/></circle>
    <circle cx="105" cy="100" r="13" fill="#2a2c42"/><circle cx="160" cy="100" r="13" fill="#2a2c42"/>
  </g>
  <g fill="{PINK}" transform="translate(40 40) scale(4)">{heart}<g transform="translate(10 0)">{heart}</g><g transform="translate(20 0)" fill-opacity="0.25">{heart}</g></g>
  <g class="bob">{t(SW - 40, 66, '1UP', 26, 'JB', 700, '#4ade80', 'end')}</g>
  {t(SW - 40, 260, 'HI 042069', 13, 'JB', 700, MUTED, 'end')}'''

slides = [
    (music, 'Music', 'lo-fi while I code, everything else while I don\'t.'),
    (drawing, 'Drawing', 'sketching characters and doodling ideas.'),
    (anime, 'Watching anime', 'slice-of-life to shonen. one more episode.'),
    (games, 'Playing games', 'co-op nights, boss fights, chasing high scores.'),
]
def caption_anim(i):
    """captions swap without overlapping: old one is gone in the first half of the transition, new one fades in during the second."""
    s, e, h = i * SLOT, (i + 1) * SLOT, TR / 2
    if i == 0:
        return f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;{f((e - TR) / LOOP)};{f((e - h) / LOOP)};{f((LOOP - h) / LOOP)};1" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'
    if i == N - 1:
        return f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f((s - h) / LOOP)};{f(s / LOOP)};{f((e - TR) / LOOP)};{f((e - h) / LOOP)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'
    return f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f((s - h) / LOOP)};{f(s / LOOP)};{f((e - TR) / LOOP)};{f((e - h) / LOOP)};1" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'


slide_svg = [f'<g clip-path="url(#{P}-stage)">']
cap_svg = []
for i, (art, ttl, cap) in enumerate(slides):
    base = '1' if i == 0 else '0'
    slide_svg.append(f'<g opacity="{base}">{slide_anim(i)}<g transform="translate({SX} {SY})">{art}</g></g>')
    cap_svg.append(f'''<g opacity="{base}">{caption_anim(i)}
    {t(SX, SY + SH + 34, ttl, 19, 'SG', 700, INK)}
    {t(SX + measure(ttl, 'SG', 700, 19) + 10, SY + SH + 34, '— ' + cap, 14.5, 'SG', 500, MUTED)}</g>''')
    assert measure(ttl, 'SG', 700, 19) + 10 + measure('— ' + cap, 'SG', 500, 14.5) < SW, ttl
slide_svg.append('</g>')
slide_svg += cap_svg

story_head = f'''
  <g>
    <circle cx="{SX + 26}" cy="{SY + 26}" r="15" fill="none" stroke="url(#{P}-aurora)" stroke-width="2"/>
    <clipPath id="{P}-av"><circle cx="{SX + 26}" cy="{SY + 26}" r="12"/></clipPath>
    <image x="{SX + 12}" y="{SY + 12}" width="28" height="28" clip-path="url(#{P}-av)" href="data:image/png;base64,{ASSETS['face']}"/>
    {t(SX + 48, SY + 30, 'amyrouge', 13, 'SG', 700, INK)}
    {t(SX + 48 + measure('amyrouge', 'SG', 700, 13) + 8, SY + 30, '· off the clock', 12, 'SG', 500, '#c9cbe0')}
  </g>'''

# daily rings (concentric, Apple-style), fill on an 8s loop
RX, RY = X0 + 70, 490
RL = 8.0
rings = [('Code', 'build something', 0.82, CYAN, 36), ('Create', 'draw · listen', 0.64, VIOLET, 26), ('Play', 'games · anime', 0.48, PINK, 16)]
ring_svg = []
legend = []
for i, (lbl, sub, p, col, r) in enumerate(rings):
    C = 2 * math.pi * r
    end = C * (1 - p)
    a0, a1, a2 = 0.05 + i * 0.06, 0.32 + i * 0.06, 0.92
    ring_svg.append(f'''<circle cx="{RX}" cy="{RY}" r="{r}" fill="none" stroke="{col}" stroke-opacity="0.14" stroke-width="8"/>
    <circle cx="{RX}" cy="{RY}" r="{r}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-dasharray="{C:.2f}" stroke-dashoffset="{end:.2f}" transform="rotate(-90 {RX} {RY})">
      <animate attributeName="stroke-dashoffset" values="{C:.2f};{C:.2f};{end:.2f};{end:.2f};{C:.2f}" keyTimes="0;{f(a0)};{f(a1)};{f(a2)};1" calcMode="spline" keySplines="0 0 1 1;0.3 0.7 0.2 1;0 0 1 1;0.6 0 0.8 0.4" dur="{RL}s" begin="0s" repeatCount="indefinite"/></circle>''')
    lx = X0 + 140 + i * 140
    legend.append(f'''<g>
      <circle cx="{lx + 5}" cy="{RY - 14}" r="5" fill="{col}"/>
      {t(lx + 16, RY - 9.5, lbl, 14, 'SG', 700, INK)}
      {t(lx, RY + 12, f'{round(p * 100)}%', 20, 'JB', 700, col)}
      {t(lx, RY + 32, sub, 12, 'SG', 500, MUTED)}</g>''')
rings_block = f'''<g class="fu" style="animation-delay:.6s">
  <line x1="{SX}" y1="{RY - 54}" x2="{SX + SW}" y2="{RY - 54}" stroke="#ffffff" stroke-opacity="0.07"/>
  {''.join(ring_svg)}{''.join(legend)}
  {t(X0 + CW - 24, RY - 30, 'daily rings', 11, 'JB', 400, FAINT, 'end')}</g>'''

right = (card(P, X0 + 1, 1, CW - 2, H - 2) + header(SX, 38, '// off.the.clock', 'Life outside the IDE')
         + ''.join(segs) + f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="16" fill="#0a0b12"/>'
         + ''.join(slide_svg) + f'<rect x="{SX + 0.5}" y="{SY + 0.5}" width="{SW - 1}" height="{SH - 1}" rx="15.5" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>'
         + story_head + rings_block)

css = f'''
.fu{{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes fu{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.float{{animation:float 5s ease-in-out infinite both}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.bob{{animation:bob 3s ease-in-out infinite both}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
.note{{animation:note 3.6s ease-in-out infinite both}}
@keyframes note{{0%,100%{{transform:translate(0,0) rotate(-6deg)}}50%{{transform:translate(0,-14px) rotate(8deg)}}}}
.grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1.2s cubic-bezier(.2,.7,.2,1) both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
'''


def grad(id_, c1, c2, o1=0.35, o2=0.05):
    return f'''<linearGradient id="{P}-{id_}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c1}" stop-opacity="{o1}"/><stop offset="1" stop-color="{c2}" stop-opacity="{o2}"/></linearGradient>'''


defs = card_defs(P) + f'''
  <clipPath id="{P}-winclip"><rect x="{BX}" y="{BY + 34}" width="{BW}" height="{BH - 34}" rx="0"/></clipPath>
  <clipPath id="{P}-stage"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="16"/></clipPath>
  <linearGradient id="{P}-winbg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#161829"/><stop offset="1" stop-color="#0f1019"/></linearGradient>
  <linearGradient id="{P}-cup" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <linearGradient id="{P}-eq" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <linearGradient id="{P}-screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f9a8d4"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="#38bdf8"/></linearGradient>
  {grad('s0', VIOLET, CYAN)}{grad('s1', PINK, VIOLET)}{grad('s2', PINK, '#38bdf8', 0.3)}{grad('s3', CYAN, VIOLET, 0.3)}'''

svg = svg_doc(W, H, 'About Akeshi & life outside the IDE',
              'Left: what I bring to a team — teamwork, leadership, communication. Right: a carousel of hobbies (music, drawing, anime, games) and daily activity rings.',
              defs, left + right, css)
open(os.path.join(OUT, 'about-life.svg'), 'w', encoding='utf-8').write(svg)
print('about-life.svg', len(svg) // 1024, 'KB')
