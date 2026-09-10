"""하나의 좌표계에서 SVG/HTML 과 .excalidraw 를 함께 뽑는다."""
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ex import Doc

# 문서 머리말(스타일 포함)은 템플릿 파일 하나에서 온다.
# 예전에는 산출물인 mvc-structure/diagram.html 을 읽었는데, 산출물이 생성기의
# 입력이 되는 순환 구조였다.
HEAD = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html'),
               encoding='utf-8').read()

EX_FILL = {'input': '#a5d8ff', 'process': '#d0bfff', 'storage': '#c3fae8',
           'external': '#ffd8a8', 'neutral': '#e9ecef', 'risk': '#ffc9c9'}

MARKERS = {
    'arrow': '''      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line)" />
      </marker>''',
    'open': '''      <marker id="open" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto">
        <path d="M 1 1 L 11 6 L 1 11" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
    'tri': '''      <marker id="tri" viewBox="0 0 14 12" refX="14" refY="6" markerWidth="12" markerHeight="11" orient="auto">
        <path d="M 0 0 L 14 6 L 0 12 Z" fill="var(--bg)" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
    'diamond': '''      <marker id="diamond" viewBox="0 0 16 12" refX="0" refY="6" markerWidth="14" markerHeight="11" orient="auto">
        <path d="M 0 6 L 8 1 L 16 6 L 8 11 Z" fill="var(--line)" />
      </marker>''',
    'one': '''      <marker id="one" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="10" markerHeight="10" orient="auto">
        <path d="M 6 1 L 6 11" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
    'one-s': '''      <marker id="one-s" viewBox="0 0 12 12" refX="0" refY="6" markerWidth="10" markerHeight="10" orient="auto">
        <path d="M 6 1 L 6 11" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
    'many': '''      <marker id="many" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="10" markerHeight="10" orient="auto">
        <path d="M 0 6 L 12 0 M 0 6 L 12 6 M 0 6 L 12 12" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
    'many-s': '''      <marker id="many-s" viewBox="0 0 12 12" refX="0" refY="6" markerWidth="10" markerHeight="10" orient="auto">
        <path d="M 12 6 L 0 0 M 12 6 L 0 6 M 12 6 L 0 12" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>''',
}

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class N:
    """노드. kind='box' 는 제목+부제, kind='class' 는 UML 클래스 칸."""
    def __init__(self, x, y, w, h, cls, title, subs=(), kind='box', attrs=(), ops=(), stereo=None, rx=8):
        self.__dict__.update(locals()); del self.self

class E:
    def __init__(self, pts, label=None, dashed=False, head='arrow', start=None, lx=None, ly=None):
        self.__dict__.update(locals()); del self.self

class Z:
    def __init__(self, x, y, w, h, label=None, rx=10):
        self.__dict__.update(locals()); del self.self

def emit_svg(path, doc_title, w, h, title, subtitle, nodes, edges, zones=(), notes=(), labels=()):
    used = set()
    for e in edges:
        if e.head: used.add(e.head)
        if e.start: used.add(e.start)
    body = ['  <svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (w, h, esc(doc_title))]
    if used:
        body += ['    <defs>'] + [MARKERS[m] for m in MARKERS if m in used] + ['    </defs>', '']
    body += ['    <text class="title" x="24" y="34">%s</text>' % esc(title),
             '    <text class="small" x="24" y="56">%s</text>' % esc(subtitle), '']
    body.append('    <!-- 연결선을 먼저 그려 화살표가 상자 뒤로 가게 한다 -->')
    for e in edges:
        d = 'M ' + ' L '.join('%s %s' % (p[0], p[1]) for p in e.pts)
        bits = ['    <path class="edge" d="%s"' % d]
        if e.dashed: bits.append(' stroke-dasharray="6 5"')
        if e.start: bits.append(' marker-start="url(#%s)"' % e.start)
        if e.head: bits.append(' marker-end="url(#%s)"' % e.head)
        bits.append(' />')
        body.append(''.join(bits))
    body.append('')
    for z in zones:
        body.append('    <rect class="zone" x="%s" y="%s" width="%s" height="%s" rx="%s" />' % (z.x, z.y, z.w, z.h, z.rx))
    for n in nodes:
        if n.kind == 'diamond':
            cx, cy = n.x + n.w / 2, n.y + n.h / 2
            body.append('    <path class="node %s" d="M %s %s L %s %s L %s %s L %s %s Z" />'
                        % (n.cls, cx, n.y, n.x + n.w, cy, cx, n.y + n.h, n.x, cy))
        elif n.kind == 'ellipse':
            body.append('    <ellipse class="node %s" cx="%s" cy="%s" rx="%s" ry="%s" />'
                        % (n.cls, n.x + n.w / 2, n.y + n.h / 2, n.w / 2, n.h / 2))
        else:
            body.append('    <rect class="node %s" x="%s" y="%s" width="%s" height="%s" rx="%s" />' % (n.cls, n.x, n.y, n.w, n.h, n.rx))
        if n.kind == 'entity':
            body.append('    <path class="edge" d="M %s %s L %s %s" stroke-width="1" />' % (n.x, n.y + 34, n.x + n.w, n.y + 34))
        if n.kind == 'class':
            band = n.y + 34 + (18 if n.stereo else 0)
            sep = band + 20 * len(n.attrs) + 10
            body.append('    <path class="edge" d="M %s %s L %s %s" stroke-width="1" />' % (n.x, band, n.x + n.w, band))
            body.append('    <path class="edge" d="M %s %s L %s %s" stroke-width="1" />' % (n.x, sep, n.x + n.w, sep))
    body.append('')
    for z in zones:
        if z.label:
            body.append('    <text class="small" x="%s" y="%s">%s</text>' % (z.x + 2, z.y - 10, esc(z.label)))
    for n in nodes:
        cx = n.x + n.w // 2
        if n.kind == 'entity':
            body.append('    <text class="label" x="%s" y="%s" text-anchor="middle">%s</text>' % (cx, n.y + 23, esc(n.title)))
            for i, a in enumerate(n.attrs):
                body.append('    <text class="small" x="%s" y="%s">%s</text>' % (n.x + 16, n.y + 58 + i * 20, esc(a)))
        elif n.kind == 'class':
            ty = n.y + 23
            if n.stereo:
                body.append('    <text class="small" x="%s" y="%s" text-anchor="middle">%s</text>' % (cx, n.y + 20, esc(n.stereo)))
                ty = n.y + 41
            body.append('    <text class="label" x="%s" y="%s" text-anchor="middle">%s</text>' % (cx, ty, esc(n.title)))
            band = n.y + 34 + (18 if n.stereo else 0)
            for i, a in enumerate(n.attrs):
                body.append('    <text class="small" x="%s" y="%s">%s</text>' % (n.x + 16, band + 24 + i * 20, esc(a)))
            sep = band + 20 * len(n.attrs) + 10
            for i, o in enumerate(n.ops):
                body.append('    <text class="small" x="%s" y="%s">%s</text>' % (n.x + 16, sep + 24 + i * 20, esc(o)))
        elif n.title:
            k = len(n.subs)
            top = n.y + (n.h - (22 + k * 20)) // 2 + 16
            body.append('    <text class="label" x="%s" y="%s" text-anchor="middle">%s</text>' % (cx, top, esc(n.title)))
            for i, s in enumerate(n.subs):
                body.append('    <text class="small" x="%s" y="%s" text-anchor="middle">%s</text>' % (cx, top + 22 + i * 20, esc(s)))
    for e in edges:
        if e.label:
            m = len(e.pts) // 2
            lx = e.lx if e.lx is not None else (e.pts[m - 1][0] + e.pts[m][0]) // 2
            ly = e.ly if e.ly is not None else (e.pts[m - 1][1] + e.pts[m][1]) // 2 - 8
            body.append('    <text class="small" x="%s" y="%s" text-anchor="middle">%s</text>' % (lx, ly, esc(e.label)))
    for lx, ly, s, anc in labels:
        body.append('    <text class="small" x="%s" y="%s"%s>%s</text>' % (lx, ly, (' text-anchor="%s"' % anc) if anc else '', esc(s)))
    for i, n in enumerate(notes):
        body.append('    <text class="small" x="24" y="%s">%s</text>' % (h - 34 - (len(notes) - 1 - i) * 22, esc(n)))
    body.append('  </svg>')
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(doc_title), HEAD, count=1)
    io.open(path, 'w', encoding='utf-8').write(head + '<main>\n' + '\n'.join(body) + '\n</main>\n')

def emit_ex(path, title, subtitle, nodes, edges, zones=(), notes=(), labels=(), seed=20260909):
    d = Doc(seed)
    d.note('t', title, 40, 24, 28)
    d.note('s', subtitle, 40, 62, 16, '#5b6475')
    for i, z in enumerate(zones):
        d.rect('z%d' % i, z.x, z.y, z.w, z.h, 'transparent', dashed=True)
        if z.label:
            d.note('zl%d' % i, z.label, z.x + 8, z.y - 26, 16, '#5b6475')
    for i, e in enumerate(edges):
        head = None if e.head is None else ('arrow' if e.head in ('arrow', 'open', 'tri') else None)
        d.link('e%d' % i, [list(p) for p in e.pts], e.label, dashed=e.dashed, head=head)
    for i, n in enumerate(nodes):
        shape = {'diamond': 'diamond', 'ellipse': 'ellipse'}.get(n.kind, 'rectangle')
        text = n.title
        if text:
            extra = list(n.attrs) + list(n.ops) if n.kind in ('class', 'entity') else list(n.subs)
            if extra:
                text += '\n' + '\n'.join(extra)
        d.rect('n%d' % i, n.x, n.y, n.w, n.h, EX_FILL[n.cls], text or None, shape=shape)
    for i, (lx, ly, s, anc) in enumerate(labels):
        d.note('l%d' % i, s, lx, ly - 14, 16, '#5b6475')
    if notes:
        bottom = max([n.y + n.h for n in nodes] + [z.y + z.h for z in zones]) + 60
        d.note('nt', '\n'.join(notes), 40, bottom, 16, '#5b6475')
    return d.save(path)
