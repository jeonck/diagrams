"""시퀀스 다이어그램을 SVG/HTML 과 .excalidraw 로 함께 뽑는다."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ex import Doc

# 문서 머리말(스타일 포함)은 템플릿 파일 하나에서 온다.
# 예전에는 산출물인 mvc-structure/diagram.html 을 읽었는데, 산출물이 생성기의
# 입력이 되는 순환 구조였다.
HEAD = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html'),
               encoding='utf-8').read()
EX_FILL = {'input': '#a5d8ff', 'process': '#d0bfff', 'storage': '#c3fae8',
           'external': '#ffd8a8', 'neutral': '#e9ecef', 'risk': '#ffc9c9'}
BAR = 6

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def build(path_html, path_ex, doc_title, w, h, title, subtitle, actors, msgs, selfs, bars, notes, seed=1):
    """actors: [(cx, cls, name, sub)]  msgs: [(y, from_cx, to_cx, label, is_return)]
       selfs: [(cx, y0, y1, label)]     bars: [(cx, y0, y1, cls)]"""
    HEAD_Y, HEAD_H, HEAD_W = 96, 80, 230
    top, bot = HEAD_Y + HEAD_H, max([m[0] for m in msgs] + [s[2] for s in selfs]) + 70

    # ── SVG ──
    b = ['  <svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (w, h, esc(doc_title)), '    <defs>',
'      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
'        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line)" />', '      </marker>',
'      <marker id="ret" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">',
'        <path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="var(--line)" stroke-width="1.4" />',
'      </marker>', '    </defs>', '',
'    <text class="title" x="24" y="34">%s</text>' % esc(title),
'    <text class="small" x="24" y="56">%s</text>' % esc(subtitle), '',
'    <!-- 생명선 -->']
    for cx, _, _, _ in actors:
        b.append('    <line class="zone" x1="%d" y1="%d" x2="%d" y2="%d" />' % (cx, top, cx, bot))
    b += ['', '    <!-- 메시지: 노드보다 먼저 그려 화살표가 상자 뒤로 간다 -->']
    for y, a, z, label, ret in msgs:
        x1 = a + BAR if z > a else a - BAR
        x2 = z - BAR if z > a else z + BAR
        b.append('    <path class="edge" d="M %d %d L %d %d"%s marker-end="url(#%s)" />'
                 % (x1, y, x2, y, ' stroke-dasharray="7 5"' if ret else '', 'ret' if ret else 'arrow'))
    for cx, y0, y1, _ in selfs:
        b.append('    <path class="edge" d="M %d %d L %d %d L %d %d L %d %d" marker-end="url(#arrow)" />'
                 % (cx + BAR, y0, cx + 66, y0, cx + 66, y1, cx + BAR, y1))
    b += ['', '    <!-- 활성 구간 -->']
    for cx, y0, y1, cls in bars:
        b.append('    <rect class="node %s" x="%d" y="%d" width="%d" height="%d" rx="2" />'
                 % (cls, cx - BAR, y0 - 12, BAR * 2, y1 - y0 + 24))
    b += ['', '    <!-- 참여자 -->']
    for cx, cls, _, _ in actors:
        b.append('    <rect class="node %s" x="%d" y="%d" width="%d" height="%d" rx="8" />'
                 % (cls, cx - HEAD_W // 2, HEAD_Y, HEAD_W, HEAD_H))
    b.append('')
    for cx, _, name, sub in actors:
        b.append('    <text class="label" x="%d" y="%d" text-anchor="middle">%s</text>' % (cx, HEAD_Y + 32, esc(name)))
        b.append('    <text class="small" x="%d" y="%d" text-anchor="middle">%s</text>' % (cx, HEAD_Y + 54, esc(sub)))
    b.append('')
    for y, a, z, label, ret in msgs:
        b.append('    <text class="small" x="%d" y="%d" text-anchor="middle">%s</text>' % ((a + z) // 2, y - 10, esc(label)))
    for cx, y0, y1, label in selfs:
        b.append('    <text class="small" x="%d" y="%d">%s</text>' % (cx + 78, (y0 + y1) // 2 + 4, esc(label)))
    for i, n in enumerate(notes):
        b.append('    <text class="small" x="24" y="%d">%s</text>' % (h - 34 - (len(notes) - 1 - i) * 22, esc(n)))
    b.append('  </svg>')
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(doc_title), HEAD, count=1)
    io.open(path_html, 'w', encoding='utf-8').write(head + '<main>\n' + '\n'.join(b) + '\n</main>\n')

    # ── Excalidraw ──
    d = Doc(seed)
    d.note('t', title, 40, 24, 28)
    d.note('s', subtitle, 40, 62, 16, '#5b6475')
    for i, (cx, _, _, _) in enumerate(actors):
        d.link('life%d' % i, [[cx, top], [cx, bot]], dashed=True, head=None)
    for i, (cx, y0, y1, cls) in enumerate(bars):
        d.rect('bar%d' % i, cx - BAR, y0 - 12, BAR * 2, y1 - y0 + 24, EX_FILL[cls], round=False)
    for i, (y, a, z, label, ret) in enumerate(msgs):
        x1 = a + BAR if z > a else a - BAR
        x2 = z - BAR if z > a else z + BAR
        d.link('m%d' % i, [[x1, y], [x2, y]], label, dashed=ret)
    for i, (cx, y0, y1, label) in enumerate(selfs):
        d.link('sf%d' % i, [[cx + BAR, y0], [cx + 66, y0], [cx + 66, y1], [cx + BAR, y1]], label)
    for i, (cx, cls, name, sub) in enumerate(actors):
        d.rect('h%d' % i, cx - HEAD_W // 2, HEAD_Y, HEAD_W, HEAD_H, EX_FILL[cls], name + '\n' + sub, size=18)
    d.note('n', '\n'.join(notes), 40, bot + 60, 16, '#5b6475')
    return d.save(path_ex)
