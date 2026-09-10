"""스펙 한 장 → 산출물 두 개(diagram.html · diagram.excalidraw).

스펙 파일은 좌표와 문구만 갖고, 어디에 쓸지는 여기서 정한다.
DIAGRAM_OUT_ROOT 를 주면 그 아래에 쓴다 (재생성 검증용).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec import N, E, Z, emit_svg, emit_ex          # noqa: F401  (스펙이 그대로 가져다 쓴다)
import seq as _seq

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))


def out_dir(project, slug):
    root = os.environ.get('DIAGRAM_OUT_ROOT') or REPO
    d = os.path.join(root, 'projects', project, 'diagrams', slug)
    os.makedirs(d, exist_ok=True)
    return d


def emit(project, slug, doc, w, h, title, sub, nodes, edges,
         zones=(), notes=(), labels=(), seed=1):
    d = out_dir(project, slug)
    emit_svg(os.path.join(d, 'diagram.html'), doc, w, h, title, sub, nodes, edges, zones, notes, labels)
    n = emit_ex(os.path.join(d, 'diagram.excalidraw'), title, sub, nodes, edges, zones, notes, labels, seed)
    print('%-22s %2d elements' % (slug, n))
    return n


def emit_seq(project, slug, doc, w, h, title, sub, actors, msgs, selfs, bars, notes, seed=1):
    """시퀀스는 좌표계가 달라 전용 방출기를 쓴다."""
    d = out_dir(project, slug)
    n = _seq.build(os.path.join(d, 'diagram.html'), os.path.join(d, 'diagram.excalidraw'),
                   doc, w, h, title, sub, actors, msgs, selfs, bars, notes, seed)
    print('%-22s %2d elements' % (slug, n))
    return n
