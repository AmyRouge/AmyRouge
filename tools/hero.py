from common import *

P = 'h'
W, H = 1200, 470
FPS, NF = 24, len(ASSETS['frames'])
PLAY = NF / FPS            # ~2.67s of clip
HOLD = 1.4
FADE = 0.25
D = round(PLAY + HOLD + FADE, 3)   # loop length (~4.3s)


def f(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))


# ---------------------------------------------------------------- video
VX, VY, VW, VH = 800, 46, 330, 360
frames = []
for i, b in enumerate(ASSETS['frames']):
    a, z = i / FPS / D, (i + 1) / FPS / D
    if i == 0:
        anim = f'values="1;0" keyTimes="0;{f(z)}"'
    elif i == NF - 1:
        anim = f'values="0;1" keyTimes="0;{f(a)}"'
    else:
        anim = f'values="0;1;0" keyTimes="0;{f(a)};{f(z)}"'
    frames.append(
        f'<image x="{VX}" y="{VY}" width="{VW}" height="{VH}" href="data:image/jpeg;base64,{b}">'
        f'<animate attributeName="opacity" {anim} calcMode="discrete" dur="{D}s" begin="0s" repeatCount="indefinite"/></image>')
fade_in, fade_out = 0.12 / D, (D - FADE) / D
video = f'''
  <g mask="url(#{P}-vmask)">
    <g>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{f(fade_in)};{f(fade_out)};1" dur="{D}s" begin="0s" repeatCount="indefinite"/>
      {''.join(frames)}
    </g>
  </g>'''

# viewfinder chrome
BX0, BY0, BX1, BY1, L = VX - 14, VY - 10, VX + VW + 14, VY + VH + 6, 26
brackets = ''.join(
    f'<path class="br" style="animation-delay:{0.15 + i * 0.12:.2f}s" d="{d}"/>' for i, d in enumerate([
        f'M{BX0} {BY0 + L} V{BY0} H{BX0 + L}', f'M{BX1 - L} {BY0} H{BX1} V{BY0 + L}',
        f'M{BX1} {BY1 - L} V{BY1} H{BX1 - L}', f'M{BX0 + L} {BY1} H{BX0} V{BY1 - L}']))
thirds = ''.join([
    f'<line x1="{VX + VW / 3:.1f}" y1="{VY + 20}" x2="{VX + VW / 3:.1f}" y2="{VY + VH - 20}"/>',
    f'<line x1="{VX + 2 * VW / 3:.1f}" y1="{VY + 20}" x2="{VX + 2 * VW / 3:.1f}" y2="{VY + VH - 20}"/>',
    f'<line x1="{VX + 20}" y1="{VY + VH / 3:.1f}" x2="{VX + VW - 20}" y2="{VY + VH / 3:.1f}"/>',
    f'<line x1="{VX + 20}" y1="{VY + 2 * VH / 3:.1f}" x2="{VX + VW - 20}" y2="{VY + 2 * VH / 3:.1f}"/>'])
SY = BY1 + 26
pk = PLAY / D
scrub = f'''
  <g class="fu" style="animation-delay:.5s">
    <rect x="{VX}" y="{SY - 1.5}" width="{VW}" height="3" rx="1.5" fill="#ffffff" fill-opacity="0.08"/>
    <rect x="{VX}" y="{SY - 1.5}" width="{VW}" height="3" rx="1.5" fill="url(#{P}-aurora-u)">
      <animate attributeName="width" values="0;{VW};{VW}" keyTimes="0;{f(pk)};1" dur="{D}s" begin="0s" repeatCount="indefinite"/>
    </rect>
    <circle cx="{VX + VW}" cy="{SY}" r="5" fill="{INK}">
      <animate attributeName="cx" values="{VX};{VX + VW};{VX + VW}" keyTimes="0;{f(pk)};1" dur="{D}s" begin="0s" repeatCount="indefinite"/>
    </circle>
    {t(VX, SY + 20, 'wave_take_03', 11, 'JB', 400, FAINT)}
    {t(VX + VW, SY + 20, f'{FPS} fps · {NF} frames · loop', 11, 'JB', 400, FAINT, 'end')}
  </g>'''
rec = f'''
  <g class="fu" style="animation-delay:.6s">
    <rect x="{VX + 8}" y="{VY + 6}" width="62" height="22" rx="11" fill="{BG}" fill-opacity="0.7"/>
    <circle cx="{VX + 21}" cy="{VY + 17}" r="4.5" fill="#ff4d6d">
      <animate attributeName="opacity" values="1;1;0.15;0.15" keyTimes="0;0.5;0.55;1" dur="1.1s" begin="0s" repeatCount="indefinite"/>
    </circle>
    {t(VX + 31, VY + 21.5, 'REC', 11, 'JB', 700, INK)}
    <rect x="{VX + VW - 132}" y="{VY + 6}" width="124" height="22" rx="11" fill="{BG}" fill-opacity="0.7"/>
    {t(VX + VW - 70, VY + 21.5, 'akeshi_hi.mp4', 11, 'JB', 400, MUTED, 'middle')}
  </g>'''

# ---------------------------------------------------------------- left column
LX = 64
pill_txt = 'open to collabs'
pw = measure(pill_txt, 'JB', 400, 13) + 46
pill = f'''
  <g class="fu" style="animation-delay:.05s">
    <rect x="{LX}" y="48" width="{pw:.0f}" height="30" rx="15" fill="{CYAN}" fill-opacity="0.07" stroke="{CYAN}" stroke-opacity="0.35"/>
    <circle cx="{LX + 18}" cy="63" r="4" fill="{CYAN}" fill-opacity="0.5">
      <animate attributeName="r" values="4;11;11" keyTimes="0;0.7;1" dur="1.8s" begin="0s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" values="0.5;0;0" keyTimes="0;0.7;1" dur="1.8s" begin="0s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{LX + 18}" cy="63" r="4" fill="{CYAN}"/>
    {t(LX + 32, 67.5, pill_txt, 13, 'JB', 400, CYAN)}
  </g>'''

# typed greeting: a clip rect that grows one character at a time, with a caret riding along
greet = "Hi there, I'm"
GS, GY = 21, 128
cw = measure('a', 'JB', 400, GS)
n = len(greet)
TD = 2.0                              # one-shot typing timeline
t0, step = 0.35, 0.075
times = [0] + [(t0 + i * step) / TD for i in range(n + 1)]
widths = [0] + [cw * i for i in range(n + 1)]
type_kt = ';'.join(f(x) for x in times)
type_w = ';'.join(f'{x:.1f}' for x in widths)
type_x = ';'.join(f'{LX + x:.1f}' for x in widths)
greeting = f'''
  <clipPath id="{P}-type"><rect x="{LX}" y="{GY - 24}" width="{cw * n:.1f}" height="34">
    <animate attributeName="width" values="{type_w}" keyTimes="{type_kt}" calcMode="discrete" dur="{TD}s" begin="0s" fill="freeze"/>
  </rect></clipPath>
  <g clip-path="url(#{P}-type)">{t(LX, GY, greet, GS, 'JB', 400, MUTED)}</g>
  <rect x="{LX + cw * n + 3:.1f}" y="{GY - 18}" width="10" height="22" fill="{PINK}">
    <animate attributeName="x" values="{type_x}" keyTimes="{type_kt}" calcMode="discrete" dur="{TD}s" begin="0s" fill="freeze" additive="replace"/>
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="0s" repeatCount="indefinite"/>
  </rect>'''

# name: animated gradient fill, revealed by a rising mask
name = 'Akeshi Dewmini'
NS, NY = 70, 208
nw = measure(name, 'SG', 700, NS, -1.5)
name_svg = f'''
  <linearGradient id="{P}-namegrad" gradientUnits="userSpaceOnUse" x1="{LX}" y1="0" x2="{LX + nw:.0f}" y2="0" spreadMethod="repeat">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.33" stop-color="{VIOLET}"/>
    <stop offset="0.66" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{nw:.0f} 0" dur="7s" begin="0s" repeatCount="indefinite"/>
  </linearGradient>
  <mask id="{P}-rise" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
    <rect x="{LX - 10}" y="{NY - 80}" width="{nw + 40:.0f}" height="104" fill="#fff">
      <animate attributeName="y" values="{NY + 24};{NY + 24};{NY - 80}" keyTimes="0;0.55;1" calcMode="spline" keySplines="0 0 1 1;0.2 0.8 0.2 1" dur="2.6s" begin="0s" fill="freeze"/>
    </rect>
  </mask>'''
name_body = f'''
  <g mask="url(#{P}-rise)">
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 46;0 46;0 0" keyTimes="0;0.55;1" calcMode="spline" keySplines="0 0 1 1;0.2 0.8 0.2 1" dur="2.6s" begin="0s" fill="freeze"/>
      {t(LX - 3, NY, name, NS, 'SG', 700, f'url(#{P}-namegrad)', extra='letter-spacing="-1.5"')}
    </g>
  </g>'''

# cycling role lines
roles = ['Software Engineer @ WindsorGaming', 'Full-stack web · Java · Android',
         'Teamwork · Leadership · Communication', 'Fuelled by music, anime & games']
RY, RD = 254, 12.0
seg = 1 / len(roles)
role_svg = [f'<path d="M{LX} {RY - 12} l7 6 l-7 6" fill="none" stroke="{CYAN}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>']
for i, r in enumerate(roles):
    a, z = i * seg, (i + 1) * seg
    e = 0.03
    if i == 0:
        ov, okt = '1;1;0;0;1', f'0;{f(z - e)};{f(z)};{f(1 - e)};1'
        tv, tkt = '0 0;0 0;0 -12;0 12;0 0', okt
    else:
        ov, okt = '0;0;1;1;0;0', f'0;{f(a - e)};{f(a)};{f(z - e)};{f(z)};1'
        tv, tkt = '0 12;0 12;0 0;0 0;0 -12;0 -12', okt
    base = '1' if i == 0 else '0'
    role_svg.append(f'''<g opacity="{base}">
      <animate attributeName="opacity" values="{ov}" keyTimes="{okt}" dur="{RD}s" begin="0s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="{tv}" keyTimes="{tkt}" dur="{RD}s" begin="0s" repeatCount="indefinite"/>
      {t(LX + 20, RY, r, 19, 'JB', 400, INK)}</g>''')
roles_block = f'''
  <clipPath id="{P}-roleclip"><rect x="{LX}" y="{RY - 24}" width="660" height="34"/></clipPath>
  <g class="fu" style="animation-delay:1.3s"><g clip-path="url(#{P}-roleclip)">{''.join(role_svg)}</g></g>'''

pitch1 = 'I turn ideas into friendly, reliable software'
pitch2 = 'and help the team around me ship it together.'
pitch = f'''
  <g class="fu" style="animation-delay:1.5s">
    {t(LX, 302, pitch1, 18, 'SG', 500, MUTED)}
    {t(LX, 328, pitch2, 18, 'SG', 500, MUTED)}
  </g>'''

# meta row with small drawn icons
MY = 384
pin = f'<path class="dr" d="M0 -7 a6 6 0 0 1 6 6 c0 4.5 -6 10 -6 10 s-6 -5.5 -6 -10 a6 6 0 0 1 6 -6 z M0 -3.2 a2.2 2.2 0 1 0 0.01 0"/>'
bld = f'<path class="dr" d="M-6 9 V-6 h8 v15 M2 -1 h5 v10 M-9 9 h18 M-3.5 -2.5 h3 M-3.5 1.5 h3 M-3.5 5.5 h3"/>'
star = f'<path class="dr" d="M0 -7.5 l2.3 4.8 5.2 .7 -3.8 3.6 .9 5.2 -4.6 -2.5 -4.6 2.5 .9 -5.2 -3.8 -3.6 5.2 -.7 z"/>'
metas = [(pin, 'Colombo, Sri Lanka', CYAN), (bld, 'WindsorGaming', VIOLET), (star, '3 stars · 9 repos', PINK)]
mx = LX
meta_svg = []
for i, (ic, label, col) in enumerate(metas):
    meta_svg.append(f'''<g class="fu" style="animation-delay:{1.7 + i * 0.12:.2f}s">
      <g transform="translate({mx + 8} {MY - 5})" stroke="{col}" style="animation-delay:{1.8 + i * 0.15:.2f}s">{ic.replace('class="dr"', f'class="dr" style="animation-delay:{1.8 + i * 0.15:.2f}s"')}</g>
      {t(mx + 24, MY, label, 14, 'JB', 400, INK)}</g>''')
    mx += 24 + measure(label, 'JB', 400, 14) + 30
meta_block = ''.join(meta_svg) + f'<line x1="{LX}" y1="{MY - 36}" x2="{LX + 560}" y2="{MY - 36}" stroke="#ffffff" stroke-opacity="0.07"/>'

css = f'''
.fu{{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes fu{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.br{{fill:none;stroke:{INK};stroke-width:2.2;stroke-linecap:round;stroke-dasharray:60;animation:dr 1s ease-out both}}
.dr{{fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:80;animation:dr 1.4s ease-out both}}
@keyframes dr{{from{{stroke-dashoffset:60}}to{{stroke-dashoffset:0}}}}
.blob{{animation:drift 16s ease-in-out infinite alternate both}}
@keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-40px,26px)}}}}
'''

defs = card_defs(P) + f'''
  <linearGradient id="{P}-aurora-u" gradientUnits="userSpaceOnUse" x1="{VX}" y1="0" x2="{VX + VW}" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <filter id="{P}-feather" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter>
  <mask id="{P}-vmask" maskUnits="userSpaceOnUse" x="{VX - 40}" y="{VY - 40}" width="{VW + 80}" height="{VH + 80}">
    <rect x="{VX + 26}" y="{VY + 22}" width="{VW - 52}" height="{VH - 58}" rx="30" fill="#fff" filter="url(#{P}-feather)"/>
  </mask>
  <clipPath id="{P}-cardclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20"/></clipPath>''' + name_svg

body = f'''{card(P, 1, 1, W - 2, H - 2)}
  <g clip-path="url(#{P}-cardclip)" opacity="0.9">
    <circle class="blob" cx="980" cy="150" r="170" fill="{VIOLET}" fill-opacity="0.16" filter="url(#{P}-blur40)"/>
    <circle class="blob" style="animation-delay:-6s" cx="1120" cy="420" r="130" fill="{CYAN}" fill-opacity="0.10" filter="url(#{P}-blur40)"/>
    <circle class="blob" style="animation-delay:-11s" cx="160" cy="460" r="150" fill="{PINK}" fill-opacity="0.07" filter="url(#{P}-blur40)"/>
  </g>
  {pill}
  {greeting}
  {name_body}
  {roles_block}
  {pitch}
  {meta_block}
  {video}
  <g stroke="#ffffff" stroke-opacity="0.06" stroke-width="1">{thirds}</g>
  {brackets}
  {rec}
  {scrub}'''

svg = svg_doc(W, H, 'Akeshi Dewmini — Software Engineer',
              "Animated intro card: Hi there, I'm Akeshi Dewmini, Software Engineer at WindsorGaming in Colombo, with a waving character video in a camera viewfinder.",
              defs, body, css)
open(os.path.join(OUT, 'hero.svg'), 'w', encoding='utf-8').write(svg)
print('hero.svg', len(svg) // 1024, 'KB; loop', D, 's')
