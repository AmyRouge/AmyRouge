from common import *
import random

P = 'd'
W, H = 1200, 600

# ---- edit me: data (public GitHub numbers for AmyRouge, Oct 2026) -------------
KPIS = [('Public repos', 9, 'JS · Java · HTML · CSS'), ('Stars earned', 3, 'Technovas leads'),
        ('Public commits', 17, 'across 7 repos'), ('Years on GitHub', 4, 'since March 2022')]
STARRED = [('Technovas', 2), ('Ultroid (fork)', 1), ('Minions', 0), ('RecipeApp', 0), ('MyPortfolio', 0)]
NOW = [('building', 'this animated profile'), ('learning', 'system design patterns'),
       ('sketching', 'character art'), ('watching', 'seasonal anime'), ('playing', 'co-op games with friends')]
# ------------------------------------------------------------------------------


def f(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))


# ================================================================ LANYARD BADGE
PX, PY = 214, 0                     # pivot: where the strap leaves the top of the card
BX, BY, BWd, BHt = 92, 176, 244, 368
BCX = BX + BWd / 2

# damped pendulum: lands at T_LAND, then theta = A e^(-t/tau) sin(w t)
T_LAND, SW_DUR = 0.75, 6.0
A, TAU, OMEGA = 9.0, 1.15, 2 * math.pi / 1.25
ts = [0, T_LAND] + [T_LAND + k * 0.0625 for k in range(1, int((SW_DUR - T_LAND) / 0.0625))] + [SW_DUR]
vals = [0, 0] + [A * math.exp(-(tt - T_LAND) / TAU) * math.sin(OMEGA * (tt - T_LAND)) for tt in ts[2:-1]] + [0]
swing_vals = ';'.join(f'{v:.2f} {PX} {PY}' for v in vals)
swing_kt = ';'.join(f(tt / SW_DUR) for tt in ts)

# strap: two bands meeting at the clasp, long enough to stay on screen during the drop
strapL = f'M{PX - 30} -700 L{PX - 30} 0 L{PX - 9} 146'
strapR = f'M{PX + 30} -700 L{PX + 30} 0 L{PX + 9} 146'
strap_text = ' AMYROUGE · SOFTWARE ENGINEER · WINDSORGAMING · ' * 3


def strap(d, id_):
    return f'''<path id="{P}-{id_}" d="{d}" fill="none" stroke="url(#{P}-strap)" stroke-width="22" stroke-linejoin="round"/>
    <text font-family="Mono" font-size="8.5" font-weight="700" fill="#ffffff" fill-opacity="0.85" letter-spacing="1.5" dy="3"><textPath href="#{P}-{id_}" startOffset="560">{strap_text}</textPath></text>'''


clasp = f'''
    <rect x="{PX - 14}" y="138" width="28" height="18" rx="5" fill="url(#{P}-metal)" stroke="#6b7280" stroke-width="0.8"/>
    <rect x="{PX - 4}" y="154" width="8" height="12" fill="url(#{P}-metal)"/>
    <circle cx="{PX}" cy="{BY - 4}" r="11" fill="none" stroke="url(#{P}-metal)" stroke-width="4"/>
    <circle cx="{PX - 6}" cy="145" r="1.6" fill="#ffffff" fill-opacity="0.8"/>'''

# barcode
rng = random.Random(320)
bars, x = [], BX + 22
while x < BX + BWd - 26:
    w = rng.choice([1, 1, 2, 3])
    bars.append(f'<rect x="{x}" y="{BY + 318}" width="{w}" height="26" fill="#e7e9f5"/>')
    x += w + rng.choice([1, 2, 2, 3])
FR = 70                             # portrait frame half-size
FX, FY = BCX - FR, BY + 52
perim = 4 * (2 * FR - 2 * 18) + 2 * math.pi * 18
chip = f'''
    <g transform="translate({BX + 22} {BY + 266})">
      <rect width="40" height="30" rx="6" fill="url(#{P}-gold)" stroke="#a16207" stroke-width="0.8"/>
      <path d="M0 10 h13 M0 20 h13 M27 10 h13 M27 20 h13 M13 0 v30 M27 0 v30 M13 15 h14" stroke="#854d0e" stroke-width="0.9" fill="none" stroke-opacity="0.7"/>
    </g>
    {t(BX + 74, BY + 278, 'ID  AD-0322', 11, 'JB', 700, INK)}
    {t(BX + 74, BY + 293, 'Colombo · LK', 11, 'JB', 400, MUTED)}'''
badge = f'''
    <rect x="{BX}" y="{BY}" width="{BWd}" height="{BHt}" rx="20" fill="#11121e"/>
    <rect x="{BX}" y="{BY}" width="{BWd}" height="{BHt}" rx="20" fill="url(#{P}-dots)"/>
    <path d="M{BX} {BY + 20} a20 20 0 0 1 20 -20 h{BWd - 40} a20 20 0 0 1 20 20 v20 h-{BWd} z" fill="url(#{P}-aurora)" fill-opacity="0.9"/>
    <rect x="{BCX - 22}" y="{BY + 8}" width="44" height="8" rx="4" fill="#0d0e16"/>
    {t(BX + 18, BY + 33, 'WINDSORGAMING', 9.5, 'JB', 700, '#0d0e16', extra='letter-spacing="1.2"')}
    {t(BX + BWd - 18, BY + 33, 'STAFF', 9.5, 'JB', 700, '#0d0e16', 'end', 'letter-spacing="1.2"')}
    <clipPath id="{P}-face"><rect x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" rx="18"/></clipPath>
    <rect x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" rx="18" fill="url(#{P}-facebg)"/>
    <image x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" clip-path="url(#{P}-face)" href="data:image/png;base64,{ASSETS['face']}"/>
    <rect x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="2"/>
    <rect x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" rx="18" fill="none" stroke="url(#{P}-aurora)" stroke-width="5" stroke-linecap="round" stroke-dasharray="70 {perim - 70:.1f}" filter="url(#{P}-soft)">
      <animate attributeName="stroke-dashoffset" values="0;-{perim:.1f}" dur="3.2s" begin="0s" repeatCount="indefinite"/></rect>
    <rect x="{FX}" y="{FY}" width="{2 * FR}" height="{2 * FR}" rx="18" fill="none" stroke="url(#{P}-aurora)" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="70 {perim - 70:.1f}">
      <animate attributeName="stroke-dashoffset" values="0;-{perim:.1f}" dur="3.2s" begin="0s" repeatCount="indefinite"/></rect>
    {t(BCX, BY + 224, 'Akeshi Dewmini', 22, 'SG', 700, INK, 'middle')}
    {t(BCX, BY + 244, 'Software Engineer', 12, 'JB', 400, CYAN, 'middle')}
    <line x1="{BX + 22}" y1="{BY + 256}" x2="{BX + BWd - 22}" y2="{BY + 256}" stroke="#ffffff" stroke-opacity="0.08"/>
    {chip}
    {''.join(bars)}
    <g clip-path="url(#{P}-badgeclip)">
      <rect x="{BX - 200}" y="{BY - 60}" width="140" height="{BHt + 120}" fill="url(#{P}-holo)" transform="rotate(18 {BCX} {BY + BHt / 2})" opacity="0.55">
        <animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 0;560 0;560 0" keyTimes="0;0.3;0.62;1" dur="5.5s" begin="0s" repeatCount="indefinite"/>
      </rect>
    </g>
    <rect x="{BX + 0.5}" y="{BY + 0.5}" width="{BWd - 1}" height="{BHt - 1}" rx="19.5" fill="none" stroke="url(#{P}-hair)"/>'''

lanyard = f'''
  <g clip-path="url(#{P}-cardclip)">
   <g>
    <animateTransform attributeName="transform" type="translate" values="0 -640;0 -640;0 14;0 -6;0 0" keyTimes="0;0.06;0.7;0.86;1" calcMode="spline" keySplines="0 0 1 1;0.55 0 0.9 0.6;0.2 0.6 0.4 1;0.4 0 0.6 1" dur="{T_LAND + 0.25}s" begin="0s" fill="freeze"/>
    <g>
     <animateTransform attributeName="transform" type="rotate" values="{swing_vals}" keyTimes="{swing_kt}" dur="{SW_DUR}s" begin="0s" fill="freeze"/>
     <g>
      <animateTransform attributeName="transform" type="rotate" values="0 {PX} {PY};1.1 {PX} {PY};0 {PX} {PY};-1.1 {PX} {PY};0 {PX} {PY}" dur="5s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1"/>
      <ellipse cx="{BCX}" cy="{BY + BHt + 22}" rx="110" ry="10" fill="#000000" fill-opacity="0.35" filter="url(#{P}-glow)"/>
      {strap(strapL, 'sl')}{strap(strapR, 'sr')}
      {badge}
      {clasp}
     </g>
    </g>
   </g>
  </g>'''

# ================================================================ DASHBOARD
DX, DW = 420, W - 420 - 28
dash = [t(DX, 40, '// dashboard', 12, 'JB', 400, FAINT), t(DX, 66, 'At a glance', 22, 'SG', 700, INK),
        f'''<g><circle cx="{DX + DW - 132}" cy="57" r="4" fill="#4ade80">
          <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" begin="0s" repeatCount="indefinite"/></circle>
          {t(DX + DW, 61, 'public GitHub data', 11.5, 'JB', 400, MUTED, 'end')}</g>''']

# KPI tiles with count-up numbers (discrete text swaps, one-shot, frozen on the final value)
GAP = 14
TW = (DW - GAP * 3) / 4
KY, KH = 88, 100
CU = 2.6                              # count-up timeline length
for i, (label, val, sub) in enumerate(KPIS):
    x = DX + i * (TW + GAP)
    t_start, t_end = 0.4 + i * 0.15, 1.7 + i * 0.15
    steps = list(range(0, val + 1)) if val <= 20 else [round(val * k / 20) for k in range(21)]
    nums = []
    for k, sv in enumerate(steps):
        # ease-out timing for each step
        u0 = 1 - (1 - k / len(steps)) ** 2
        u1 = 1 - (1 - (k + 1) / len(steps)) ** 2
        a = (t_start + (t_end - t_start) * u0) / CU
        b = (t_start + (t_end - t_start) * u1) / CU
        final = k == len(steps) - 1
        if k == 0:
            anim = f'values="1;0" keyTimes="0;{f(b)}"'
        elif final:
            anim = f'values="0;1" keyTimes="0;{f(a)}"'
        else:
            anim = f'values="0;1;0" keyTimes="0;{f(a)};{f(b)}"'
        nums.append(f'<g opacity="{1 if final else 0}"><animate attributeName="opacity" {anim} calcMode="discrete" dur="{CU}s" begin="0s" fill="freeze"/>'
                    f'{t(x + 18, KY + 62, str(sv), 36, "SG", 700, INK)}</g>')
    col = [CYAN, VIOLET, PINK, CYAN][i]
    dash.append(f'''<g class="fu" style="animation-delay:{0.1 + i * 0.1:.2f}s">
      <rect x="{x:.1f}" y="{KY}" width="{TW:.1f}" height="{KH}" rx="14" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.08"/>
      <rect x="{x + 18:.1f}" y="{KY}" width="28" height="2.5" rx="1.25" fill="{col}"/>
      {t(x + 18, KY + 26, label, 12.5, 'SG', 500, MUTED)}
      {''.join(nums)}
      {t(x + 18, KY + 84, sub, 11, 'JB', 400, FAINT)}</g>''')

# bar chart: single hue, horizontal, direct value labels, 4px rounded data ends
CX0, CY0, CWd, CHt = DX, 210, 400, 346
dash.append(f'''<g class="fu" style="animation-delay:.5s">
  <rect x="{CX0}" y="{CY0}" width="{CWd}" height="{CHt}" rx="14" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.08"/>
  {t(CX0 + 20, CY0 + 32, 'Most-starred repos', 15, 'SG', 700, INK)}
  {t(CX0 + CWd - 20, CY0 + 32, 'stars', 11, 'JB', 400, FAINT, 'end')}</g>''')
NAME_W = 118
bx0 = CX0 + 20 + NAME_W
bmax = CX0 + CWd - 50 - bx0
vmax = max(v for _, v in STARRED) or 1
rowh = 50
for i, (name, v) in enumerate(STARRED):
    yy = CY0 + 66 + i * rowh
    w = max(bmax * v / vmax, 4)
    dash.append(f'''<g class="fu" style="animation-delay:{0.7 + i * 0.1:.2f}s">
      {t(CX0 + 20, yy + 14, name, 13, 'SG', 500, INK if v else MUTED)}
      <rect x="{bx0}" y="{yy + 1}" width="{bmax:.1f}" height="18" rx="4" fill="#ffffff" fill-opacity="0.03"/>
      <rect class="bar" style="animation-delay:{0.9 + i * 0.12:.2f}s" x="{bx0}" y="{yy + 1}" width="{w:.1f}" height="18" rx="4" fill="{VIOLET}" fill-opacity="{1 if v else 0.35}"/>
      {t(bx0 + w + 8, yy + 15, str(v), 13, 'JB', 700, INK if v else MUTED)}</g>''')
dash.append(f'''<g class="fu" style="animation-delay:1.2s">
  <line x1="{bx0}" y1="{CY0 + 56}" x2="{bx0}" y2="{CY0 + 66 + len(STARRED) * rowh - 22}" stroke="#ffffff" stroke-opacity="0.18"/>
  {t(CX0 + 20, CY0 + CHt - 22, 'Star a repo you like — it helps!', 12, 'SG', 500, FAINT)}</g>''')

# now panel
NX0, NWd = CX0 + CWd + GAP, DW - CWd - GAP
NOW_ICONS = {
    'building': '<path d="M-6 6 l8 -8 M0 -6 l6 6 M-2 -4 l4 -4 4 4 -4 4z"/>',
    'learning': '<path d="M-8 -2 l8 -4 8 4 -8 4z M-5 0 v4 c3 2 7 2 10 0 v-4"/>',
    'sketching': '<path d="M-6 6 l2 -6 8 -8 4 4 -8 8z M-4 0 l4 4"/>',
    'watching': '<rect x="-8" y="-6" width="16" height="11" rx="2"/><path d="M-2 -3 l5 2.5 -5 2.5z M-4 8 h8"/>',
    'playing': '<path d="M-8 2 c0 -5 3 -7 8 -7 s8 2 8 7 c0 4 -3 5 -5 2 l-1 -1 h-4 l-1 1 c-2 3 -5 2 -5 -2z M-5 -1 v3 M-6.5 .5 h3"/>',
}
now = [f'''<g class="fu" style="animation-delay:.6s">
  <rect x="{NX0:.1f}" y="{CY0}" width="{NWd:.1f}" height="{CHt}" rx="14" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.08"/>
  {t(NX0 + 20, CY0 + 32, 'now', 15, 'SG', 700, INK)}
  <circle cx="{NX0 + 58}" cy="{CY0 + 27}" r="3.5" fill="{PINK}"><animate attributeName="r" values="3.5;5;3.5" dur="1.4s" begin="0s" repeatCount="indefinite"/></circle>
  <g transform="translate({NX0 + NWd - 54} {CY0 + 33})">{''.join(
      f'<rect x="{k * 7}" y="-12" width="4" height="12" rx="2" fill="{PINK}" fill-opacity="0.8"><animate attributeName="height" values="4;12;6;10;4" dur="{0.9 + k * 0.13:.2f}s" begin="0s" repeatCount="indefinite"/><animate attributeName="y" values="-4;-12;-6;-10;-4" dur="{0.9 + k * 0.13:.2f}s" begin="0s" repeatCount="indefinite"/></rect>' for k in range(5))}</g>
  </g>''']
for i, (verb, what) in enumerate(NOW):
    yy = CY0 + 70 + i * 54
    col = [CYAN, VIOLET, PINK, CYAN, VIOLET][i]
    now.append(f'''<g class="fu" style="animation-delay:{0.8 + i * 0.1:.2f}s">
      <rect x="{NX0 + 20:.1f}" y="{yy - 4}" width="36" height="36" rx="10" fill="{col}" fill-opacity="0.1" stroke="{col}" stroke-opacity="0.35"/>
      <g transform="translate({NX0 + 38:.1f} {yy + 14})" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{NOW_ICONS[verb]}</g>
      {t(NX0 + 70, yy + 9, verb, 11, 'JB', 400, FAINT)}
      {t(NX0 + 70, yy + 27, what, 14, 'SG', 500, INK)}</g>''')
    assert 70 + measure(what, 'SG', 500, 14) < NWd - 12, what

css = f'''
.fu{{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes fu{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.bar{{transform-box:fill-box;transform-origin:left center;animation:grow 1.3s cubic-bezier(.2,.7,.2,1) both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
'''
defs = card_defs(P) + f'''
  <clipPath id="{P}-cardclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20"/></clipPath>
  <clipPath id="{P}-badgeclip"><rect x="{BX}" y="{BY}" width="{BWd}" height="{BHt}" rx="20"/></clipPath>
  <linearGradient id="{P}-strap" x1="0" x2="0" gradientUnits="userSpaceOnUse" y1="-700" y2="150">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.75" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <linearGradient id="{P}-metal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#f1f5f9"/><stop offset="0.45" stop-color="#94a3b8"/><stop offset="0.6" stop-color="#e2e8f0"/><stop offset="1" stop-color="#64748b"/></linearGradient>
  <linearGradient id="{P}-gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fde68a"/><stop offset="0.5" stop-color="#d4a017"/><stop offset="1" stop-color="#fcd34d"/></linearGradient>
  <linearGradient id="{P}-holo" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.3" stop-color="{CYAN}" stop-opacity="0.35"/>
    <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="0.7" stop-color="{PINK}" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
  <linearGradient id="{P}-facebg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2e1065"/><stop offset="1" stop-color="#0e7490"/></linearGradient>
  <filter id="{P}-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>'''

body = card(P, 1, 1, W - 2, H - 2) + lanyard + ''.join(dash) + ''.join(now)
svg = svg_doc(W, H, 'ID badge & dashboard',
              'A lanyard ID badge for Akeshi Dewmini, Software Engineer, beside a dashboard: 9 public repos, 3 stars, 17 public commits, 4 years on GitHub; most-starred repos chart; what I am doing now.',
              defs, body, css)
open(os.path.join(OUT, 'id-dashboard.svg'), 'w', encoding='utf-8').write(svg)
print('id-dashboard.svg', len(svg) // 1024, 'KB')
