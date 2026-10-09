from common import *

P = 's'
W, H = 1200, 580

# ---- edit me: the stack ------------------------------------------------------
ORBITS = [  # (rx, ry, tilt°, seconds per lap, icons)
    (240, 112, -16, 30, ['react', 'nodedotjs', 'openjdk', 'mysql']),
    (172, 74, 22, 21, ['javascript', 'html5', 'css3', 'php', 'git']),
    (112, 70, 78, 14, ['android', 'firebase', 'figma']),
]
MOONS = ['vite', 'redux']          # small moons orbiting React
GROUPS = [
    ('Frontend', CYAN, ['html5', 'css3', 'javascript', 'typescript', 'react', 'tailwindcss', 'bootstrap']),
    ('Backend', VIOLET, ['nodedotjs', 'express', 'php', 'openjdk', 'springboot']),
    ('Mobile & Tools', PINK, ['android', 'kotlin', 'git', 'github', 'figma', 'postman', 'vite']),
    ('Data', CYAN, ['mysql', 'firebase', 'mongodb', 'postgresql']),
    ('AI', VIOLET, ['python', 'jupyter', 'tensorflow', 'huggingface', 'googlegemini']),
]
LABEL = {'openjdk': 'Java', 'nodedotjs': 'Node.js', 'tailwindcss': 'Tailwind', 'googlegemini': 'Gemini',
         'huggingface': 'Hugging Face', 'springboot': 'Spring Boot'}
# ------------------------------------------------------------------------------


def f(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))


CX, CY = 290, 330
CORE_R = 40
TILE_R = 19
MOON_ORBIT, MOON_SIZE = 33, 18
MOON_DUR = 7

# clearance: React's closest approach is the minor radius of its ellipse; the moons must stay clear of the core glow
react_orbit = next(o for o in ORBITS if 'react' in o[4])
moon_reach = MOON_ORBIT + MOON_SIZE * 0.75
clear = react_orbit[1] - moon_reach - (CORE_R + 12)
assert clear > 4, f'moons would touch the core (clearance {clear:.1f}px)'
for rx, ry, *_ in ORBITS:
    assert ry - TILE_R > CORE_R + 6, 'an orbit passes through the core'

orbit_lines, riders = [], []
for oi, (rx, ry, tilt, dur, icons) in enumerate(ORBITS):
    d, pts = ellipse_path(CX, CY, rx, ry, tilt, n=120)
    orbit_lines.append(f'<path d="{d}" fill="none" stroke="url(#{P}-orbit{oi})" stroke-width="1.2" stroke-dasharray="2 5"/>')
    for k, slug in enumerate(icons):
        phase = k / len(icons) + oi * 0.07
        phase %= 1
        i0 = round(phase * 120) % 120
        sx, sy = pts[i0]
        rel = ellipse_path(CX - sx, CY - sy, rx, ry, tilt, n=120)[0]
        col = icon_color(slug)
        moons = ''
        if slug == 'react':
            ms = []
            for mi, m in enumerate(MOONS):
                ang = mi * 180
                mc = icon_color(m)
                ms.append(f'''<g transform="rotate({ang})"><g transform="translate({MOON_ORBIT} 0)">
                  <g transform="rotate({-ang})"><animateTransform attributeName="transform" type="rotate" values="{-ang};{-ang - 360}" dur="{MOON_DUR}s" begin="0s" repeatCount="indefinite"/>
                  <circle r="{MOON_SIZE / 2 + 3}" fill="#151626" stroke="{mc}" stroke-opacity="0.6"/>
                  {icon(m, -MOON_SIZE / 2 + 2, -MOON_SIZE / 2 + 2, MOON_SIZE - 4)}</g></g></g>''')
            moons = f'''<circle r="{MOON_ORBIT}" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-dasharray="1.5 4"/>
              <g><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{MOON_DUR}s" begin="0s" repeatCount="indefinite"/>{''.join(ms)}</g>'''
        riders.append(f'''
  <g transform="translate({sx:.1f} {sy:.1f})">
    <animateMotion path="{rel}" keyPoints="{f(phase)};1;0;{f(phase)}" keyTimes="0;{f(1 - phase)};{f(1 - phase)};1" calcMode="linear" dur="{dur}s" begin="0s" repeatCount="indefinite"/>
    {moons}
    <circle r="{TILE_R + 6}" fill="{col}" fill-opacity="0.10" filter="url(#{P}-glow)"/>
    <circle r="{TILE_R}" fill="#121320" stroke="{col}" stroke-opacity="0.55"/>
    {icon(slug, -11, -11, 22)}
  </g>''')

core = f'''
  <circle cx="{CX}" cy="{CY}" r="{CORE_R + 30}" fill="url(#{P}-coreglow)">
    <animate attributeName="r" values="{CORE_R + 24};{CORE_R + 36};{CORE_R + 24}" dur="4s" begin="0s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{CX}" cy="{CY}" r="{CORE_R}" fill="url(#{P}-core)"/>
  <circle cx="{CX}" cy="{CY}" r="{CORE_R}" fill="none" stroke="#ffffff" stroke-opacity="0.35"/>
  <circle cx="{CX}" cy="{CY}" r="{CORE_R - 8}" fill="none" stroke="#ffffff" stroke-opacity="0.15" stroke-dasharray="3 6">
    <animateTransform attributeName="transform" type="rotate" values="0 {CX} {CY};360 {CX} {CY}" dur="18s" begin="0s" repeatCount="indefinite"/>
  </circle>
  {t(CX, CY + 7, '</>', 20, 'JB', 700, '#ffffff', 'middle')}'''

# ---- chip grid
GX, GW = 612, 560
chips = []
y = 98
all_chips = []
for gi, (gname, gcol, slugs) in enumerate(GROUPS):
    chips.append(f'<g class="fu" style="animation-delay:{0.2 + gi * 0.12:.2f}s">')
    chips.append(f'<rect x="{GX}" y="{y - 11}" width="3" height="14" rx="1.5" fill="{gcol}"/>')
    chips.append(t(GX + 12, y, gname.upper(), 11.5, 'JB', 700, gcol, extra='letter-spacing="1.2"'))
    chips.append(f'<line x1="{GX + 24 + measure(gname.upper(), "JB", 700, 11.5, 1.2):.0f}" y1="{y - 4}" x2="{GX + GW}" y2="{y - 4}" stroke="#ffffff" stroke-opacity="0.06"/>')
    x, cy = GX, y + 14
    for slug in slugs:
        label = LABEL.get(slug, ICONS[slug]['title'])
        w = 16 + 18 + 8 + measure(label, 'SG', 500, 13) + 6
        if x + w > GX + GW:
            x, cy = GX, cy + 38
        all_chips.append((x, cy, w, gcol, slug, label))
        x += w + 8
    for (cx_, cy_, w, col, slug, label) in [c for c in all_chips if c[1] >= y]:
        pass
    y = cy + 30 + 30
    chips.append('§')  # placeholder: chips of this group are inserted below
    chips.append('</g>')
assert y - 30 < H - 20, y

# glow sequence: chip borders light up one after another
NCH = len(all_chips)
STEP = 0.32
GL = round(NCH * STEP + 1.5, 2)
chip_svg_by_group = []
group_bounds = []
idx = 0
for gi, (gname, gcol, slugs) in enumerate(GROUPS):
    out = []
    for _ in slugs:
        x, cy, w, col, slug, label = all_chips[idx]
        a = idx * STEP / GL
        b = min((idx * STEP + 0.45) / GL, 0.999)
        c = min((idx * STEP + 1.3) / GL, 1)
        anim = f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{f(a)};{f(b)};{f(c)};1" dur="{GL}s" begin="0s" repeatCount="indefinite"/>'
        out.append(f'''<g>
      <rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="30" rx="15" fill="#ffffff" fill-opacity="0.035" stroke="#ffffff" stroke-opacity="0.11"/>
      <rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="30" rx="15" fill="none" stroke="{col}" stroke-width="3" opacity="0" filter="url(#{P}-soft)">{anim}</rect>
      <rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="30" rx="15" fill="{col}" fill-opacity="0.06" stroke="{col}" stroke-width="1.3" opacity="0">{anim}</rect>
      {icon(slug, x + 14, cy + 7, 16)}
      {t(x + 38, cy + 20, label, 13, 'SG', 500, INK)}</g>''')
        idx += 1
    chip_svg_by_group.append(''.join(out))
chips_svg = ''.join(chips)
for g in chip_svg_by_group:
    chips_svg = chips_svg.replace('§', g, 1)

css = f'''
.fu{{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes fu{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.spin-in{{transform-origin:{CX}px {CY}px;animation:si 1.4s cubic-bezier(.2,.7,.2,1) both}}
@keyframes si{{from{{opacity:0;transform:scale(.8) rotate(-12deg)}}to{{opacity:1;transform:none}}}}
'''
orbit_grads = ''.join(f'''<linearGradient id="{P}-orbit{i}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c1}" stop-opacity="0.7"/><stop offset="1" stop-color="{c2}" stop-opacity="0.25"/></linearGradient>'''
                      for i, (c1, c2) in enumerate([(CYAN, PINK), (VIOLET, CYAN), (PINK, VIOLET)]))
defs = card_defs(P) + orbit_grads + f'''
  <radialGradient id="{P}-core" cx="0.35" cy="0.3" r="0.8">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/><stop offset="0.25" stop-color="{CYAN}"/>
    <stop offset="0.65" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></radialGradient>
  <radialGradient id="{P}-coreglow"><stop offset="0.45" stop-color="{VIOLET}" stop-opacity="0.45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <filter id="{P}-soft" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>'''

body = f'''{card(P, 1, 1, W - 2, H - 2)}
  {t(28, 40, '// stack.orbit', 12, 'JB', 400, FAINT)}
  {t(28, 66, 'Tools I build with', 22, 'SG', 700, INK)}
  {t(GX, 40, '// grouped', 12, 'JB', 400, FAINT)}
  <g class="spin-in">
    {''.join(orbit_lines)}
    {core}
    {''.join(riders)}
  </g>
  <line x1="{GX - 22}" y1="40" x2="{GX - 22}" y2="{H - 40}" stroke="#ffffff" stroke-opacity="0.06"/>
  {chips_svg}'''

svg = svg_doc(W, H, 'Tech stack', 'Tech icons orbiting a glowing core, plus a grouped chip grid: Frontend, Backend, Mobile & Tools, Data, AI.', defs, body, css)
open(os.path.join(OUT, 'stack.svg'), 'w', encoding='utf-8').write(svg)
print('stack.svg', len(svg) // 1024, 'KB; chips', NCH, 'glow loop', GL, 's; moon clearance', round(clear, 1), 'px')
