"""저장소의 svg-template 스타일을 그대로 쓰는 다이어그램 생성 헬퍼."""
import io, re

_SRC = io.open('/home/user/diagrams/projects/order-platform/diagrams/mvc-structure/diagram.html', encoding='utf-8').read()
HEAD = _SRC[:_SRC.index('<main>')]

ARROW = '''      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line)" />
      </marker>'''
OPEN = '''      <marker id="open" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto">
        <path d="M 1 1 L 11 6 L 1 11" fill="none" stroke="var(--line)" stroke-width="1.5" />
      </marker>'''
TRI = '''      <marker id="tri" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="11" markerHeight="11" orient="auto">
        <path d="M 0 0 L 12 6 L 0 12 Z" fill="var(--bg)" stroke="var(--line)" stroke-width="1.5" />
      </marker>'''
DIAMOND = '''      <marker id="diamond" viewBox="0 0 16 12" refX="0" refY="6" markerWidth="13" markerHeight="10" orient="auto">
        <path d="M 0 6 L 8 1 L 16 6 L 8 11 Z" fill="var(--line)" />
      </marker>'''

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def T(cls, x, y, s, anchor=None, extra=''):
    a = ' text-anchor="%s"' % anchor if anchor else ''
    return '    <text class="%s" x="%s" y="%s"%s%s>%s</text>' % (cls, x, y, a, extra, esc(s))

def R(x, y, w, h, cls, rx=8):
    return '    <rect class="node %s" x="%s" y="%s" width="%s" height="%s" rx="%s" />' % (cls, x, y, w, h, rx)

def zone(x, y, w, h, rx=10):
    return '    <rect class="zone" x="%s" y="%s" width="%s" height="%s" rx="%s" />' % (x, y, w, h, rx)

def hair(x1, y1, x2, y2):
    return '    <path class="edge" d="M %s %s L %s %s" stroke-width="1" />' % (x1, y1, x2, y2)

def edge(d, marker='arrow', start=None, dashed=False):
    bits = ['    <path class="edge" d="%s"' % d]
    if dashed:
        bits.append(' stroke-dasharray="6 5"')
    if start:
        bits.append(' marker-start="url(#%s)"' % start)
    if marker:
        bits.append(' marker-end="url(#%s)"' % marker)
    bits.append(' />')
    return ''.join(bits)

def line(x1, y1, x2, y2, **kw):
    return edge('M %s %s L %s %s' % (x1, y1, x2, y2), **kw)

def box(x, y, w, h, cls, title, subs=(), tsize='label'):
    """제목 + 부제 몇 줄이 든 상자. (rect, texts) 를 돌려준다."""
    cx = x + w // 2
    n = len(subs)
    top = y + (h - (22 + n * 20)) // 2 + 16
    texts = [T(tsize, cx, top, title, 'middle')]
    for i, s in enumerate(subs):
        texts.append(T('small', cx, top + 22 + i * 20, s, 'middle'))
    return R(x, y, w, h, cls), texts

def uml_class(x, y, w, name, attrs, ops, cls='process', stereo=None):
    """UML 클래스 상자: 이름 / 속성 / 오퍼레이션."""
    h = 34 + 20 * len(attrs) + 20 + 20 * len(ops) + 20
    if stereo:
        h += 18
    rects = [R(x, y, w, h, cls)]
    cx = x + w // 2
    ty = y + 23
    texts = []
    if stereo:
        texts.append(T('small', cx, y + 20, stereo, 'middle'))
        ty = y + 41
    texts.append(T('label', cx, ty, name, 'middle'))
    band = y + 34 + (18 if stereo else 0)
    rects.append(hair(x, band, x + w, band))
    for i, a in enumerate(attrs):
        texts.append(T('small', x + 16, band + 24 + i * 20, a))
    sep = band + 20 * len(attrs) + 10
    rects.append(hair(x, sep, x + w, sep))
    for i, o in enumerate(ops):
        texts.append(T('small', x + 16, sep + 24 + i * 20, o))
    return rects, texts, h

def page(path, doc_title, w, h, title, subtitle, defs, edges, nodes, texts, notes=()):
    body = ['  <svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (w, h, esc(doc_title))]
    if defs:
        body += ['    <defs>'] + defs + ['    </defs>', '']
    body += [T('title', 24, 34, title), T('small', 24, 56, subtitle), '']
    if edges:
        body += ['    <!-- 연결선을 먼저 그려 화살표가 상자 뒤로 가게 한다 -->'] + edges + ['']
    body += nodes + [''] + texts
    if notes:
        body += ['']
        for i, n in enumerate(notes):
            body.append(T('small', 24, h - 40 + i * 22 - (len(notes) - 1) * 22, n))
    body.append('  </svg>')
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(doc_title), HEAD, count=1)
    io.open(path, 'w', encoding='utf-8').write(head + '<main>\n' + '\n'.join(body) + '\n</main>\n')
    return path
